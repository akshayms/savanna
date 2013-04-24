from os import getcwd
import paramiko
from paramiko import client
from re import search
from savanna.tests.integration.db import ValidationTestCase
from telnetlib import Telnet


def _setup_ssh_connection(host, ssh):
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        host,
        username='root',
        password='swordfish'
        #assword='watchThis'
    )


def _open_channel_and_execute(ssh, cmd):
    chan = ssh.get_transport().open_session()
    chan.exec_command(cmd)
    return chan.recv_exit_status()


def _execute_command_on_node(host, cmd):
    ssh = paramiko.SSHClient()
    try:
        _setup_ssh_connection(host, ssh)
        return _open_channel_and_execute(ssh, cmd)
    finally:
        ssh.close()


def _execute_transfer_on_node(host, locfile, nodefile):
    ssh = paramiko.SSHClient()
    try:
        _setup_ssh_connection(host, ssh)
        scp = client(ssh.get_transport())
        scp.put(locfile, nodefile)
    finally:
        ssh.close()


def _execute_transfer_from_node(host, nodefile, localfile):
    ssh = paramiko.SSHClient()
    try:
        _setup_ssh_connection(host, ssh)
        scp = client(ssh.get_transport())
        scp.get(nodefile, localfile)
    finally:
        ssh.close()


class TestForHadoop(ValidationTestCase):

    def setUp(self):
        super(TestForHadoop, self).setUp()
        Telnet(self.host, self.port)

    def test_hadoop(self):
        cluster_body = self.make_cluster_body(
            'QA-cluster', 'master_node.medium', 'worker_node.medium', 2)
        data = self._post_object(self.url_cluster, cluster_body, 202)
        try:
            data = data["cluster"]
            object_id = data.pop(u'id')
            get_data = self._get_object(self.url_cl_wj,
                                        object_id, 200)
            get_body = self._get_body_cluster(
                'QA-cluster', 'master_node.medium', 'worker_node.medium', 2)
            self._response_cluster(get_body, get_data,
                                   self.url_cl_wj, object_id)
            get_data = self._get_object(self.url_cl_wj,
                                        object_id, 200)
            ip = get_data[u'service_urls'][u'namenode']
            p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
            m = search(p, ip)
            ip = m.group('host')
            this_dir = getcwd()
            _execute_transfer_on_node(
                ip, '%s/script.sh' % this_dir, '/script.sh')
            try:
                self.assertEquals(
                    _execute_command_on_node(ip, "cd .. && ./script.sh"), 0)
            except Exception:
                _execute_transfer_from_node(
                    ip, '/outputTestMapReduce/log.txt', '%s' % this_dir)
                self.fail("run script is failure")
        except Exception as e:
            print("failure:" + str(e))
        finally:
            self._del_object(self.url_cl_wj, id, 204)