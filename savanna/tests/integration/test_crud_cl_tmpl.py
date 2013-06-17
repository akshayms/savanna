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
#
#
# from savanna.tests.integration.db import ITestCase
# from telnetlib import Telnet
#
#
# class Test_crud_cl_tmpl(ITestCase):
#
#     def setUp(self):
#         super(Test_crud_cl_tmpl, self).setUp()
#
#         Telnet(self.host, self.port)
#
#         self.id_tt = self.get_object_id(
#             'node_group_template', self._post_object(
#                 self.url_ngt, self.make_node_group_template(
#                     "worker_tt", "qa probe", "TT"), 202))
#         self.id_jt = self.get_object_id(
#             'node_group_template', self._post_object(
#                 self.url_ngt, self.make_node_group_template(
#                     "master_jt", "qa probe", "JT"), 202))
#
#         self.id_nn = self.get_object_id(
#             'node_group_template', self._post_object(
#                 self.url_ngt, self.make_node_group_template(
#                     "master_nn", "qa probe", "NN"), 202))
#
#         self.id_dn = self.get_object_id(
#             'node_group_template', self._post_object(
#                 self.url_ngt, self.make_node_group_template(
#                     "worker_dn", "qa probe", "DN"), 202))
#
#         self.id_tt_dn = self.get_object_id(
#             'node_group_template', self._post_object(
#                 self.url_ngt, self.make_node_group_template(
#                     "worker_tt_dn", "qa probe", "TT+DN"), 202))
#
#         self.id_jt_nn = self.get_object_id(
#             'node_group_template', self._post_object(
#                 self.url_ngt, self.make_node_group_template(
#                     "master_jt_nn", "qa probe", "JT+NN"), 202))
#
#     def test_crud_cl_tmpl_with_nnjt_dntt(self):
#         node_list = {self.id_jt_nn: 1, self.id_tt_dn: 2}
#         cl_tmpl_body = self.make_cluster_template("cl_tmpl_1", node_list)
#         self._crud_object(cl_tmpl_body, self.url_cl_tmpl)
#
#     def test_crud_cl_tmpl_with_nn_jt_dn_tt(self):
#         node_list = {self.id_nn: 1, self.id_jt: 1, self.id_tt: 5, self.id_dn: 5}
#         cl_tmpl_body = self.make_cluster_template("cl_tmpl_2", node_list)
#         self._crud_object(cl_tmpl_body, self.url_cl_tmpl)
#
#     def test_crud_cl_tmpl_with_nn_jt_dntt(self):
#         node_list = {self.id_jt: 1, self.id_nn: 1, self.id_tt_dn: 7}
#         cl_tmpl_body = self.make_cluster_template("cl_tmpl_3", node_list)
#         self._crud_object(cl_tmpl_body, self.url_cl_tmpl)
#
#     def test_crud_cl_tmpl_with_nn(self):
#         node_list = {self.id_nn: 1}
#         cl_tmpl_body = self.make_cluster_template("cl_tmpl_4", node_list)
#         self._crud_object(cl_tmpl_body, self.url_cl_tmpl)
#
#     def test_crud_cl_tmpl_with_nn_dn(self):
#         node_list = {self.id_nn: 1, self.id_dn: 7}
#         cl_tmpl_body = self.make_cluster_template("cl_tmpl_5", node_list)
#         self._crud_object(cl_tmpl_body, self.url_cl_tmpl)
#
#     def test_crud_cl_tmpl_with_nn_jt_dn(self):
#         node_list = {self.id_nn: 1, self.id_jt: 1, self.id_dn: 7}
#         cl_tmpl_body = self.make_cluster_template("cl_tmpl_6", node_list)
#         self._crud_object(cl_tmpl_body, self.url_cl_tmpl)
#
#     def tearDown(self):
#         self._del_object(self.url_ngt_with_slash, self.id_jt_nn, 204)
#         self._del_object(self.url_ngt_with_slash, self.id_jt, 204)
#         self._del_object(self.url_ngt_with_slash, self.id_nn, 204)
#         self._del_object(self.url_ngt_with_slash, self.id_tt, 204)
#         self._del_object(self.url_ngt_with_slash, self.id_dn, 204)
#         self._del_object(self.url_ngt_with_slash, self.id_tt_dn, 204)