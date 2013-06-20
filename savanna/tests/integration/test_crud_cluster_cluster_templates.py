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


class TestsCRUDClusterClusterTemplates(base.ITestCase):

    def setUp(self):
        super(TestsCRUDClusterClusterTemplates, self).setUp()

        telnetlib.Telnet(self.host, self.port)

        self.create_node_group_template()

    def crud_clstr_cltr_tmpl(self, node_list):
        cl_tmpl_id = ''
        try:
            cl_tmpl_body = self.make_cluster_template('cl-tmpl', node_list)
            cl_tmpl_id = self.get_object_id(
                'cluster_template', self.post_object(self.url_cl_tmpl,
                                                     cl_tmpl_body, 202))
            clstr_body = self.make_cl_body_cluster_template(
                'vanilla', '1.1.1', cl_tmpl_id)
            self.crud_object(clstr_body, self.url_cluster)
        except Exception as e:
            self.fail('fail: ' + e.message)
        finally:
            self.del_object(self.url_cl_tmpl_with_slash, cl_tmpl_id, 204)

    def test_cluster_nnjt_dntt(self):
        node_list = {self.id_jt_nn: 1, self.id_tt_dn: 1}
        self.crud_clstr_cltr_tmpl(node_list)

    def test_cluster_nn_jt_dn_tt(self):
        node_list = {self.id_nn: 1, self.id_jt: 1,
                     self.id_dn: 1, self.id_tt: 1}
        self.crud_clstr_cltr_tmpl(node_list)

    def test_cluster_nn(self):
        node_list = {self.id_nn: 1}
        self.crud_clstr_cltr_tmpl(node_list)

    def test_cluster_nn_dn(self):
        node_list = {self.id_nn: 1, self.id_dn: 1}
        self.crud_clstr_cltr_tmpl(node_list)

    def test_cluster_nn_jt_dn(self):
        node_list = {self.id_nn: 1, self.id_jt: 1, self.id_dn: 1}
        self.crud_clstr_cltr_tmpl(node_list)

    def test_cluster_nn_jt_ttdn(self):
        node_list = {self.id_nn: 1, self.id_jt: 1, self.id_tt_dn: 1}
        self.crud_clstr_cltr_tmpl(node_list)

    def test_cluster_nnttdn_jt(self):
        node_list = {self.id_nn_tt_dn: 1, self.id_jt: 1}
        self.crud_clstr_cltr_tmpl(node_list)

    def test_cluster_jtttdn_nn(self):
        node_list = {self.id_jt_tt_dn: 1, self.id_nn: 1}
        self.crud_clstr_cltr_tmpl(node_list)

    def tearDown(self):
        self.delete_node_group_template()
