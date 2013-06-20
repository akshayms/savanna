# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
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

        self.create_node_group_template()

    def test_crud_cluster_ngt_jtnn_ttdn(self):
        ngt_id_list = {self.id_jt_nn: 1, self.id_tt_dn: 2}
        body = self.make_cl_body_node_groups_templates(ngt_id_list)
        self.crud_object(body, self.url_cluster)
        print '=================', body

    def tearDown(self):
        self.delete_node_group_template()
