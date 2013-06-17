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


import savanna.tests.integration.base
import telnetlib


class TestsCRUDClusterNodeGroupsTemplates\
        (savanna.tests.integration.base.ITestCase):

    def setUp(self):
        super(TestsCRUDClusterNodeGroupsTemplates, self).setUp()

        telnetlib.Telnet(self.host, self.port)

        self.id_tt = self.get_object_id(
            'node_group_template', self.post_object(
                self.url_ngt, self.make_node_group_template(
                    "worker_tt", "qa probe", "TT"), 202))
        self.id_jt = self.get_object_id(
            'node_group_template', self.post_object(
                self.url_ngt, self.make_node_group_template(
                    "master_jt", "qa probe", "JT"), 202))

        self.id_nn = self.get_object_id(
            'node_group_template', self.post_object(
                self.url_ngt, self.make_node_group_template(
                    "master_nn", "qa probe", "NN"), 202))

        self.id_dn = self.get_object_id(
            'node_group_template', self.post_object(
                self.url_ngt, self.make_node_group_template(
                    "worker_dn", "qa probe", "DN"), 202))

        self.id_tt_dn = self.get_object_id(
            'node_group_template', self.post_object(
                self.url_ngt, self.make_node_group_template(
                    "worker_tt_dn", "qa probe", "TT+DN"), 202))

        self.id_jt_nn = self.get_object_id(
            'node_group_template', self.post_object(
                self.url_ngt, self.make_node_group_template(
                    "master_jt_nn", "qa probe", "JT+NN"), 202))

    def tearDown(self):
        self.del_object(self.url_ngt_with_slash, self.id_jt_nn, 204)
        self.del_object(self.url_ngt_with_slash, self.id_jt, 204)
        self.del_object(self.url_ngt_with_slash, self.id_nn, 204)
        self.del_object(self.url_ngt_with_slash, self.id_tt, 204)
        self.del_object(self.url_ngt_with_slash, self.id_dn, 204)
        self.del_object(self.url_ngt_with_slash, self.id_tt_dn, 204)
