# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import getcwd
import paramiko
from re import search
from savanna.tests.integration.db import ITestCase
import savanna.tests.integration.parameters as param
from savanna.service.cluster_ops import _setup_ssh_connection
from telnetlib import Telnet
import json
from novaclient import client as nc


def _open_transport_chanel(transport):
    transport.connect(
        username=param.NODE_USERNAME, password=param.NODE_PASSWORD)
    return paramiko.SFTPClient.from_transport(transport)


def _execute_transfer_to_node(host, locfile, nodefile):
    try:
        transport = paramiko.Transport(host)
        sftp = _open_transport_chanel(transport)
        sftp.put(locfile, nodefile)

    finally:
        sftp.close()
        transport.close()


def _execute_transfer_from_node(host, nodefile, localfile):
    try:
        transport = paramiko.Transport(host)
        sftp = _open_transport_chanel(transport)
        sftp.get(nodefile, localfile)

    finally:
        sftp.close()
        transport.close()


def _open_channel_and_execute(ssh, cmd, print_output):
    chan = ssh.get_transport().open_session()
    chan.exec_command(cmd)
    stdout = chan.makefile('rb', -1)
    chan.set_combine_stderr(True)
    if print_output:
        return stdout.read()
    return chan.recv_exit_status()


def _execute_command_on_node(host, cmd, print_output=False):
    ssh = paramiko.SSHClient()
    try:
        _setup_ssh_connection(host, ssh)
        return _open_channel_and_execute(ssh, cmd, print_output)
    finally:
        ssh.close()


def _transfer_script_to_node(host, directory):
    _execute_transfer_to_node(
        str(host), '%s/integration/script.sh' % directory, 'script.sh')
    _execute_command_on_node(str(host), "chmod 777 script.sh")


class TestHadoop(ITestCase):

    def setUp(self):
        super(TestHadoop, self).setUp()
        Telnet(self.host, self.port)

    def _hadoop_testing(self, cluster_name, nt_name_master,
                        nt_name_worker, number_workers):
        object_id = None
        cluster_body = self.make_cluster_body(
            cluster_name, nt_name_master, nt_name_worker, number_workers)
        data = self._post_object(self.url_cluster, cluster_body, 202)

        try:
            data = data['cluster']
            object_id = data.pop(u'id')
            get_body = self._get_body_cluster(
                cluster_name, nt_name_master, nt_name_worker, number_workers)
            get_data = self._get_object(self.url_cl_with_slash, object_id, 200)
            get_data = get_data['cluster']
            del get_data[u'id']
            self._await_cluster_active(
                get_body, get_data, self.url_cl_with_slash, object_id)

            get_data = self._get_object(
                self.url_cl_with_slash, object_id, 200, True)
            get_data = get_data['cluster']
            namenode = get_data[u'service_urls'][u'namenode']
            jobtracker = get_data[u'service_urls'][u'jobtracker']
            nodes = get_data[u'nodes']
            worker_ips = []
            nova = nc.Client(version="2",
                             username=param.OS_USERNAME,
                             api_key=param.OS_PASSWORD,
                             auth_url=param.OS_AUTH_URL,
                             project_id=param.OS_TENANT_NAME)
            for node in nodes:
                if node[u'node_template'][u'name'] == nt_name_worker:
                    v = nova.servers.get("%s" % node[u'vm_id'])
                    for network, address in v.addresses.items():
                        instance_ips = json.dumps(address)
                        instance_ips = json.loads(instance_ips)
                    for instance_ip in instance_ips:
                        if instance_ip[u'addr'][0:3] == "172":
                            worker_ips.append(instance_ip[u'addr'])
            p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
            m = search(p, namenode)
            t = search(p, jobtracker)
            namenode_ip = m.group('host')
            namenode_port = m.group('port')
            jobtracker_ip = t.group('host')
            jobtracker_port = t.group('port')
            try:
                Telnet(str(namenode_ip), str(namenode_port))
                Telnet(str(jobtracker_ip), str(jobtracker_port))
            except Exception as e:
                self.fail("telnet nn or jt is failure" + e.message)
            this_dir = getcwd()
            try:
                _transfer_script_to_node(namenode_ip, this_dir)
                for worker_ip in worker_ips:
                    _transfer_script_to_node(worker_ip, this_dir)
            except Exception as e:
                self.fail("failure in transfer script" + e.message)
            try:
                self.assertEqual(int(_execute_command_on_node(
                        namenode_ip, "./script.sh lt", True)), number_workers)
            except Exception as e:
                self.fail(
                    "compare number active trackers is failure"
                    + e.message)
            try:
                self.assertEquals(
                    _execute_command_on_node(
                        namenode_ip, "./script.sh pi -nc %s" % number_workers),
                    0)
            except Exception as e:
                _execute_transfer_from_node(
                    namenode_ip,
                    '/outputTestMapReduce/log.txt', '%s/errorLog' % this_dir)
                self.fail("run pi script is failure" + e.message)
            try:
                job_name = _execute_command_on_node(
                    namenode_ip, "./script.sh gn", True)
                for worker_ip in worker_ips:
                    self.assertEquals(
                        _execute_command_on_node(
                            worker_ip,
                            "./script.sh ed -jn %s" % job_name), 0)
            except Exception as e:
                self.fail("get run in active trackers is failure" + e.message)

            try:
                self.assertEquals(
                    _execute_command_on_node(
                        namenode_ip, "./script.sh mr"),
                    0)
            except Exception as e:
                _execute_transfer_from_node(
                    namenode_ip,
                    '/outputTestMapReduce/log.txt', '%s/errorLog' % this_dir)
                self.fail("run hdfs script is failure" + e.message)

        except Exception as e:
            self.fail(e.message)

        finally:
            self._del_object(self.url_cl_with_slash, object_id, 204)

    def test_hadoop_single_master(self):
        data_nt_master = self._post_object(
            self.url_nt, self.make_nt('master_node.medium', 'JT+NN',
                                      1234, 2345), 202)
        data_nt_worker = self._post_object(
            self.url_nt, self.make_nt('worker_node.medium', 'TT+DN',
                                      1234, 2345), 202)

        try:
            self._hadoop_testing(
                'QA-hadoop', 'master_node.medium', 'worker_node.medium', 3)

        except Exception as e:
            self.fail(e.message)

        finally:
           self.delete_node_template(data_nt_master)
           self.delete_node_template(data_nt_worker)
