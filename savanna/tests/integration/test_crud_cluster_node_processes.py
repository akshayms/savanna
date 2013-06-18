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


class TestsCRUDClusterNodeProcesses(savanna.tests.integration.base.ITestCase):

    def setUp(self):
        super(TestsCRUDClusterNodeProcesses, self).setUp()

        telnetlib.Telnet(self.host, self.port)

    def test_crud_cluster_jtnn_ttdn(self):
        node_processes = {'JT+NN': 1, 'TT+DN': 2}
        body = self.make_cl_body_node_processes(node_processes)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_nn_jt_dn_tt(self):
        node_processes = {'JT': 1, 'NN': 1, 'TT': 1, 'DN': 1}
        body = self.make_cl_body_node_processes(node_processes)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_nn(self):
        node_processes = {'NN': 1}
        body = self.make_cl_body_node_processes(node_processes)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_nn_dn(self):
        node_processes = {'NN': 1, 'DN': 2}
        body = self.make_cl_body_node_processes(node_processes)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_nn_jt_dn(self):
        node_processes = {'NN': 1, 'JT': 1, 'DN': 2}
        body = self.make_cl_body_node_processes(node_processes)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_nn_jt_ttdn(self):
        node_processes = {'NN': 1, 'JT': 1, 'TT+DN': 2}
        body = self.make_cl_body_node_processes(node_processes)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_nnttdn_jt(self):
        node_processes = {'NN+TT+DN': 1, 'JT': 1}
        body = self.make_cl_body_node_processes(node_processes)
        self.crud_object(body, self.url_cluster)

    def test_crud_cluster_jtttdn_nn(self):
        node_processes = {'JT+TT+DN': 1, 'NN': 1}
        body = self.make_cl_body_node_processes(node_processes)
        self.crud_object(body, self.url_cluster)
