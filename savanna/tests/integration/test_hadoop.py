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
            get_data = self._get_object(self.url_cl_wj, object_id, 200)
            get_data = get_data['cluster']
            del get_data[u'id']
            self._response_cluster(
                get_body, get_data, self.url_cl_wj, object_id)
            get_data = self._get_object(self.url_cl_wj, object_id, 200)
            namenode_ip = get_data[u'service_urls'][u'name_node']
            jobtracker_ip = get_data[u'service_urls'][u'job_tracker']
            p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
            m = search(p, namenode_ip)
            t = search(p, jobtracker_ip)
            namenode_ip = m.group('host')
            namenode_port = m.group('port')
            jobtracker_ip = t.group('host')
            jobtracker_port = t.group('port')
            Telnet(namenode_ip, namenode_port)
            Telnet(jobtracker_ip, jobtracker_port)
            this_dir = getcwd()
            _execute_transfer_on_node(
                namenode_ip, '%s/script.sh' % this_dir, '/script.sh')
            try:
                self.assertEquals(
                    _execute_command_on_node(namenode_ip,
                                             "cd .. && ./script.sh"), 0)
            except Exception as e:
                _execute_transfer_from_node(
                    namenode_ip, '/outputTestMapReduce/log.txt',
                    '%s' % this_dir)
                self.fail("run script is failure" + e.message)
        except Exception as e:
            self.fail("failure:" + str(e))
        finally:
            self._del_object(self.url_cl_wj, object_id, 204)

    def test_hadoop_single_master(self):
        data_nt_master = self._post_object(
            self.url_nt, self.make_nt('master_node.medium', 'JT+NN',
                                      1234, 2345), 202)
        data_nt_worker = self._post_object(
            self.url_nt, self.make_nt('worker_node.medium', 'TT+DN',
                                      1234, 2345), 202)
        try:
            self._hadoop_testing(
                'QA-cluster', 'master_node.medium', 'worker_node.medium', 2)
        finally:
            self.delete_node_template(data_nt_master)
            self.delete_node_template(data_nt_worker)

    # def test_hadoop(self):
    #     cluster_body = self.make_cluster_body(
    #         'QA-cluster', 'master_node.medium', 'worker_node.medium', 2)
    #     data = self._post_object(self.url_cluster, cluster_body, 202)
    #     try:
    #         data = data["cluster"]
    #         object_id = data.pop(u'id')
    #         get_data = self._get_object(self.url_cl_wj,
    #                                     object_id, 200)
    #         get_body = self._get_body_cluster(
    #             'QA-cluster', 'master_node.medium', 'worker_node.medium', 2)
    #         self._response_cluster(get_body, get_data,
    #                                self.url_cl_wj, object_id)
    #         get_data = self._get_object(self.url_cl_wj,
    #                                     object_id, 200)
    #         ip = get_data[u'service_urls'][u'namenode']
    #         p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
    #         m = search(p, ip)
    #         ip = m.group('host')
    #         this_dir = getcwd()
    #         _execute_transfer_on_node(
    #             ip, '%s/script.sh' % this_dir, '/script.sh')
    #         try:
    #             self.assertEquals(
    #                 _execute_command_on_node(ip, "cd .. && ./script.sh"), 0)
    #         except Exception:
    #             _execute_transfer_from_node(
    #                 ip, '/outputTestMapReduce/log.txt', '%s' % this_dir)
    #             self.fail("run script is failure")
    #     except Exception as e:
    #         print("failure:" + str(e))
    #     finally:
    #         self._del_object(self.url_cl_wj, id, 204)
