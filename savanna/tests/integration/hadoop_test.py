import copy
import eventlet
import paramiko
from os import getcwd
from re import search
from savanna.openstack.common import log as logging
from savanna.tests.integration.db import ValidationTestCase
from scp import SCPClient

LOG = logging.getLogger(__name__)


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
        scp = SCPClient(ssh.get_transport())
        scp.put(locfile, nodefile)
    finally:
        ssh.close()


def _execute_transfer_from_node(host, nodefile, localfile):
    ssh = paramiko.SSHClient()
    try:
        _setup_ssh_connection(host, ssh)
        scp = SCPClient(ssh.get_transport())
        scp.get(nodefile, localfile)
    finally:
        ssh.close()


class TestForHadoop(ValidationTestCase):

    def test_01_telnet(self):
        self._tn()

    def test_hadoop(self):
        body = copy.deepcopy(self.cluster_data_jtnn_ttdn)
        body = self._assert_change_cluster_body(body, 'tt_dn.small',
                                                'tt_dn.medium')
        data = self._post_object(self.url_cluster, body, 202)
        data = data["cluster"]
        object_id = data.pop(u'id')
        get_data = self._get_object(self.url_cluster_without_json,
                                    object_id, 200)
        get_data = get_data['%s' % "cluster"]
        id = get_data[u'id']
        i = 1
        while get_data[u'status'] != u'Active':
            if i > 60:
                self._del_object(self.url_cluster_without_json,
                                 object_id, 204)
            get_data = self._get_object(self.url_cluster_without_json,
                                        object_id, 200)
            get_data = get_data['%s' % "cluster"]
            eventlet.sleep(10)
            i += 1
        print(get_data)
        ip = get_data[u'service_urls'][u'namenode']
        p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
        m = search(p, ip)
        ip = m.group('host')
        print("!!!!!!!!! start !!!!!!!!!!!!")
        print(ip)
        print("!!!!!!!!! end !!!!!!!!!!!!!!")
        #ip = '127.0.0.1'
        dir = getcwd()
        print(dir)
        _execute_transfer_on_node(
            ip, '%s/script.sh' % dir, '/script.sh')
        try:
            self.assertEquals(
                _execute_command_on_node(ip, "cd .. && ./script.sh"), 0)
        except Exception:
            _execute_transfer_from_node(
                ip, '/outputTestMapReduce/log.txt', '/home/hadoop/')
            self.fail("run script is failure")
            self._del_object(self.url_nt_not_json, id, 204)
        self._del_object(self.url_nt_not_json, id, 204)
