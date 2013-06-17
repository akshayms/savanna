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


from savanna.tests.integration.db import ITestCase
import telnetlib


class TestsCRUDClusterClusterTemplates(ITestCase):

    def setUp(self):
        super(TestsCRUDClusterClusterTemplates, self).setUp()

        telnetlib.Telnet(self.host, self.port)

        self.id_tt = self.get_object_id(
            'node_group_template', self._post_object(
                self.url_ngt, self.make_node_group_template(
                    "worker_tt", "qa probe", "TT"), 202))
        self.id_jt = self.get_object_id(
            'node_group_template', self._post_object(
                self.url_ngt, self.make_node_group_template(
                    "master_jt", "qa probe", "JT"), 202))

        self.id_nn = self.get_object_id(
            'node_group_template', self._post_object(
                self.url_ngt, self.make_node_group_template(
                    "master_nn", "qa probe", "NN"), 202))

        self.id_dn = self.get_object_id(
            'node_group_template', self._post_object(
                self.url_ngt, self.make_node_group_template(
                    "worker_dn", "qa probe", "DN"), 202))

        self.id_tt_dn = self.get_object_id(
            'node_group_template', self._post_object(
                self.url_ngt, self.make_node_group_template(
                    "worker_tt_dn", "qa probe", "TT+DN"), 202))

        self.id_jt_nn = self.get_object_id(
            'node_group_template', self._post_object(
                self.url_ngt, self.make_node_group_template(
                    "master_jt_nn", "qa probe", "JT+NN"), 202))

    def crud_clstr_cltr_tmpl(self, node_list):
        cl_tmpl_id = ''
        try:
            cl_tmpl_body = self.make_cluster_template("cl-tmpl", node_list)
            cl_tmpl_id = self.get_object_id(
                'cluster_template', self._post_object(self.url_cl_tmpl,
                                                      cl_tmpl_body, 202))
            clstr_body = self.make_cl_body_with_cl_tmpl(
                'vanilla', '1.1.1', cl_tmpl_id)
            self._crud_object(clstr_body, self.url_cluster)
        except Exception as e:
            self.fail('fail: ' + e.message)
        finally:
            self._del_object(self.url_cl_tmpl_with_slash, cl_tmpl_id, 204)

    def test_cluster_nnjt_dntt(self):
        node_list = {self.id_jt_nn: 1, self.id_tt_dn: 1}
        self.crud_clstr_cltr_tmpl(node_list)

    def test_cluster_nn_jt_dn_tt(self):
        node_list = {self.id_nn: 1, self.id_jt: 1,
                     self.id_dn: 1, self.id_tt: 1}
        self.crud_clstr_cltr_tmpl(node_list)

    def tearDown(self):
       self._del_object(self.url_ngt_with_slash, self.id_jt_nn, 204)
       self._del_object(self.url_ngt_with_slash, self.id_jt, 204)
       self._del_object(self.url_ngt_with_slash, self.id_nn, 204)
       self._del_object(self.url_ngt_with_slash, self.id_tt, 204)
       self._del_object(self.url_ngt_with_slash, self.id_dn, 204)
       self._del_object(self.url_ngt_with_slash, self.id_tt_dn, 204)