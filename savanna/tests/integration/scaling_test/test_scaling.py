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

import telnetlib

from savanna.tests.integration import base


class ClusterScalingTest(base.ITestCase):

    def setUp(self):
        super(ClusterScalingTest, self).setUp()
        telnetlib.Telnet(self.host, self.port)
        self.create_node_group_templates()

    def correct_scaling_work(self, cluster_id):
        instances_ip = self.get_instances_ip_and_node_processes_list(
            cluster_id)

        data = self.get_namenode_ip_and_tt_dn_count(instances_ip)

        self.await_active_workers_for_namenode(data)

    def implement_scaling(self, cluster_id, scaling_body):
        self.put_object(self.url_cluster_with_slash, cluster_id,
                        scaling_body, 202)

        self.await_cluster_active(cluster_id)

    def cluster_scaling_existing_node_group(self, cluster_id, ngt_id,
                                            node_count):
        ng_name = self.get_object(
            self.url_ngt_with_slash,
            ngt_id, 200)['node_group_template']['name']
        self.implement_scaling(cluster_id, {
            'resize_node_groups': [
            {
                'name': ng_name,
                'count': node_count

            }
            ]
        })

    def check_cluster_nodes(self, cluster_id):
        ip_instances = self.get_instances_ip_and_node_processes_list(
            cluster_id)
        try:
            clstr_info = self.get_namenode_ip_and_tt_dn_count(ip_instances)
            self.await_active_workers_for_namenode(clstr_info)
            return clstr_info
        except Exception as e:
            self.fail(str(e))

    def test_scaling(self):
        node_list = {self.id_jt_nn: 1, self.id_tt_dn: 1}
        cluster_id = self.create_cluster_using_ngt_and_get_id(
            node_list, 'scaling_cluster')
        try:
            before_scal_cl_info = self.check_cluster_nodes(cluster_id)
            self.cluster_scaling_existing_node_group(cluster_id, self.id_tt_dn, 2)
            after_scal_cl_info = self.check_cluster_nodes(cluster_id)
            self.assertEqual(before_scal_cl_info['tasktracker_count']-after_scal_cl_info['tasktracker_count'], 1)
            self.assertEqual(before_scal_cl_info['datanode_count']-after_scal_cl_info['datanode_count'], 1)
        except Exception as e:
            print(str(e))
        finally:
            self.del_object(self.url_cluster_with_slash, cluster_id, 204)

    def tearDown(self):
        self.delete_node_group_templates()


