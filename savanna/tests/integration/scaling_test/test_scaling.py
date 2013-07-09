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

        self.id_dn = self.get_object_id(
            'node_group_template', self.post_object(
                self.url_ngt, self.make_node_group_template(
                    'dn', 'bla-bla-bla', 'DN'), 202))

    def correct_scaling_work(self, cluster_id):
        instances_ip = self.get_instances_ip_and_node_processes_list(
            cluster_id)

        data = self.get_namenode_ip_and_tt_dn_count(instances_ip)

        self.await_active_workers_for_namenode(data)

    def implement_scaling(self, cluster_id, scaling_body):
        self.put_object(self.url_cluster_with_slash, cluster_id,
                        scaling_body, 202)

        self.await_cluster_active(self.url_cluster_with_slash, cluster_id)

    def cluster_scaling_existing_node_group(self, cluster_body, ng_name,
                                            node_count):
        cluster_body['name'] = 'cluster-scaling-existing-ng'
        cluster_id = self.create_cluster_and_get_id(cluster_body)

        self.implement_scaling(cluster_id, {
            'resize_node_groups': [
            {
                'name': ng_name,
                'count': node_count

            }
            ]
        })

    def test_scaling(self):
        node_processes = {'JT': 1, 'NN': 1, 'TT': 1}
        ngt_id_list = {self.id_dn: 1}

        cluster_body = self.make_cl_node_processes_ngt(node_processes,
                                                       ngt_id_list)



