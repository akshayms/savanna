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

import telnetlib

from savanna.tests.integration import base


class TestsCRUDClusterNodeProcessesNodeGroupsTemplates(base.ITestCase):

    def setUp(self):
        super(TestsCRUDClusterNodeProcessesNodeGroupsTemplates, self).setUp()

        telnetlib.Telnet(self.host, self.port)

        self.create_node_group_template()

    def test_crud_cluster_jtnn_ttdn(self):
        node_processes = {'JT+NN': 1}
        ngt_id_list = {self.id_tt_dn: 2}
        body = self.make_cl_node_processes_ngt(node_processes, ngt_id_list)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_jt_nn_tt_dn(self):
        node_processes = {'JT': 1, 'NN': 1}
        ngt_id_list = {self.id_tt: 1, self.id_dn: 1}
        body = self.make_cl_node_processes_ngt(node_processes, ngt_id_list)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_nn_dn(self):
        node_processes = {'NN': 1}
        ngt_id_list = {self.id_dn: 2}
        body = self.make_cl_node_processes_ngt(node_processes, ngt_id_list)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_nn_jt_dn(self):
        node_processes = {'NN': 1, 'JT': 1}
        ngt_id_list = {self.id_dn: 2}
        body = self.make_cl_node_processes_ngt(node_processes, ngt_id_list)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_nn_jt_ttdn(self):
        node_processes = {'NN': 1, 'JT': 1}
        ngt_id_list = {self.id_tt_dn: 2}
        body = self.make_cl_node_processes_ngt(node_processes, ngt_id_list)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_nnttdn_jt(self):
        node_processes = {'NN+TT+DN': 1}
        ngt_id_list = {self.id_jt: 1}
        body = self.make_cl_node_processes_ngt(node_processes, ngt_id_list)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_jtttdn_nn(self):
        node_processes = {'NN': 1}
        ngt_id_list = {self.id_jt_tt_dn: 1}
        body = self.make_cl_node_processes_ngt(node_processes, ngt_id_list)
        self.crud_object(body, self.url_cluster)

    def tearDown(self):
        self.delete_node_group_template()
