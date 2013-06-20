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

import os
import paramiko
import telnetlib

from savanna.tests.integration import base
import savanna.tests.integration.parameters as param


def _setup_ssh_connection(host, ssh):
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        host,
        username=param.NODE_USERNAME,
        key_filename=param.PATH_TO_SSH
    )


def _open_transport_chanel(transport):
    rsa_key = paramiko.RSAKey.from_private_key_file(
        param.PATH_TO_SSH, password=param.PASS_FROM_SSH)
    transport.connect(
        username=param.NODE_USERNAME, pkey=rsa_key)
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
    _execute_command_on_node(str(host), 'chmod 777 script.sh')


class TestHadoop(base.ITestCase):

    def setUp(self):
        super(TestHadoop, self).setUp()
        telnetlib.Telnet(self.host, self.port)
        self.create_node_group_template()

    def _hadoop_testing(self, node_list):
        cl_tmpl_id = None
        cluster_id = None
        try:
            cl_tmpl_body = self.make_cluster_template('cl-tmpl', node_list)
            cl_tmpl_id = self.get_object_id(
                'cluster_template', self.post_object(self.url_cl_tmpl,
                                                     cl_tmpl_body, 202))
            clstr_body = self.make_cl_body_cluster_template(
                'vanilla', '1.1.2', cl_tmpl_id)
            data = self.post_object(self.url_cluster, clstr_body, 202)
            data = data['cluster']
            cluster_id = data.pop('id')
            self.await_cluster_active(self.url_cluster_with_slash, cluster_id)
            get_data = self.get_object(
                self.url_cluster_with_slash, cluster_id, 200, True)
            get_data = get_data['cluster']
            node_groups = get_data['node_groups']
            ip_instances = {}
            for node_group in node_groups:
                instances = node_group['instances']
                for instans in instances:
                    management_ip = instans['management_ip']
                    ip_instances['%s' % management_ip] = node_group[
                        'node_processes']
            namenode_ip = None
            tasktracker_count = 0
            datanode_count = 0
            node_count = 0
            for key, value in ip_instances.items():
                telnetlib.Telnet(key, '22')
                if 'namenode' in value:
                    namenode_ip = key
                    telnetlib.Telnet(key, '50070')
                if 'tasktracker' in value:
                    tasktracker_count += 1
                    telnetlib.Telnet(key, '50060')
                if 'datanode' in value:
                    datanode_count += 1
                    telnetlib.Telnet(key, '50075')
                if 'jobtracker' in value:
                    telnetlib.Telnet(key, '50030')
                node_count += 1
            this_dir = os.getcwd()

            try:
                for key in ip_instances:
                    _transfer_script_to_node(key, this_dir)
            except Exception as e:
                self.fail('failure in transfer script: ' + e.message)

            try:
                self.assertEqual(int(_execute_command_on_node(
                    namenode_ip, './script.sh lt -hd %s'
                                 % param.HADOOP_DIRECTORY, True)),
                                 tasktracker_count)
            except Exception as e:
                self.fail('compare number active trackers is failure: '
                          + e.message)
            try:
                self.assertEqual(int(_execute_command_on_node(
                    namenode_ip, './script.sh ld -hd %s'
                                 % param.HADOOP_DIRECTORY, True)),
                                 datanode_count)
            except Exception as e:
                self.fail('compare number active datanodes is failure: '
                          + e.message)

            try:
                _execute_command_on_node(
                    namenode_ip, './script.sh pi -nc %s -hv %s -hd %s'
                                 % (node_count, param.HADOOP_VERSION,
                                    param.HADOOP_DIRECTORY))
            except Exception as e:
                _execute_transfer_from_node(
                    namenode_ip,
                    '/outputTestMapReduce/log.txt', '%s/errorLog' % this_dir)
                self.fail(
                    'run pi script is failure: '
                    + e.message)

            try:
                job_name = _execute_command_on_node(
                    namenode_ip, './script.sh gn -hd %s'
                                 % param.HADOOP_DIRECTORY, True)
                if job_name == "JobId":
                    self.fail()
            except Exception as e:
                self.fail('fail in get job name: ' + e.message)

            try:
                for key, value in ip_instances.items():
                    if 'datanode' in value or 'tasktracker' in value:
                        self.assertEquals(
                            _execute_command_on_node(
                                key, './script.sh ed -jn %s -hld %s'
                                     % (job_name[:-1],
                                        param.HADOOP_LOG_DIRECTORY)), 0)
            except Exception as e:
                self.fail('fail in check run job in worker nodes: '
                          + e.message)

            try:
                self.assertEquals(
                    _execute_command_on_node(
                        namenode_ip, './script.sh mr -hv %s -hd %s'
                                     % (param.HADOOP_VERSION,
                                        param.HADOOP_DIRECTORY)), 0)
            except Exception as e:
                _execute_transfer_from_node(
                    namenode_ip,
                    '/outputTestMapReduce/log.txt', '%s/errorLog' % this_dir)
                self.fail('run hdfs script is failure: ' + e.message)
        except Exception as e:
            self.fail(e.message)

        finally:
            self.del_object(self.url_cl_tmpl_with_slash, cl_tmpl_id, 204)
            self.del_object(self.url_cluster_with_slash, cluster_id, 204)

    def test_hadoop_single_master(self):
        node_list = {self.id_jt_nn: 1, self.id_tt_dn: 1}
        self._hadoop_testing(node_list)

    def tearDown(self):
        self.delete_node_group_template()
