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

from savanna.openstack.common import log as logging
from savanna.tests.unit.package_validation.validation_db \
    import ValidationTestCase

LOG = logging.getLogger(__name__)


class ValidationTestForNTApi(ValidationTestCase):

#-----------------------positive_tests-----------------------------------------

    def test_crud_nt(self):
        self._crud_object(self.jtnn.copy(), self.get_jtnn.copy(),
                          self.url_nt, 202, 200, 204)
        # self._crud_object(self.ttdn.copy(), self.get_ttdn.copy(),
        #                   self.url_nt, 202, 200, 204)
        self._crud_object(self.nn.copy(), self.get_nn.copy(),
                          self.url_nt, 202, 200, 204)
        self._crud_object(self.jt.copy(), self.get_jt.copy(),
                          self.url_nt, 202, 200, 204)

    def test_list_node_templates(self):
        data = self._list_objects(self.url_nt, 200)
        for idx in xrange(0, len(data.get(u'node_templates'))):
            del data.get(u'node_templates')[idx][u'id']
        self.assertEquals(data, _get_templates_stub_data())

#-----------------------negative_tests-----------------------------------------

    def test_create_nt_tt_and_dn(self):
        data = self._post_object(self.url_nt, self.tt.copy(), 400)
        self.assertEquals(data['error_name'], u'NODE_TYPE_NOT_FOUND')
        data = self._post_object(self.url_nt, self.dn.copy(), 400)
        self.assertEquals(data['error_name'], u'NODE_TYPE_NOT_FOUND')

    def test_secondary_delete_and_get_node_template(self):
        nt_id = self._crud_object(self.jt.copy(), self.get_jt.copy(),
                                          self.url_nt, 202, 200, 204)
        get_data = self._get_object(self.url_nt_not_json, nt_id, 404)
        self.assertEquals(get_data['error_name'], 'NODE_TEMPLATE_NOT_FOUND')
        del_data = self._del_object(self.url_nt_not_json, nt_id, 404)
        self.assertEquals(del_data['error_name'], 'NODE_TEMPLATE_NOT_FOUND')

    def test_get_not_exist_nt(self):
        get_data = self._get_object(self.url_nt_not_json, "0000000001", 404)
        self.assertEquals(get_data['error_name'], 'NODE_TEMPLATE_NOT_FOUND')

    def test_delete_not_exist_nt(self):
        delete_data = self._del_object(self.url_nt_not_json, "000000001", 404)
        self.assertEquals(delete_data['error_name'],
                          'NODE_TEMPLATE_NOT_FOUND')

    def test_create_nt_with_already_used_name(self):
        body = self.jtnn.copy()
        body['node_template']['name'] = 'sec-name'
        data = self._post_object(self.url_nt, body, 202)
        data = data['node_template']
        nt_id = data.pop(u'id')
        sec_body = self.ttdn.copy()
        sec_body['node_template']['name'] = 'sec-name'
        sec_data = self._post_object(self.url_nt, sec_body, 400)
        self.assertEquals(sec_data['error_name'],
                          'NODE_TEMPLATE_ALREADY_EXISTS')
        self._del_object(self.url_nt_not_json, nt_id, 204)
        thr_data = self._post_object(self.url_nt, sec_body, 202)
        thr_data = thr_data['node_template']
        sec_id = thr_data.pop(u'id')
        self._del_object(self.url_nt_not_json, sec_id, 204)

#--------------------incorrect_JSON--------------------------------------------

    def test_create_nt_with_empty_json(self):
        rv = self._post_object(self.url_nt, dict(), 400)
        self.assertEquals(rv['error_name'], 'VALIDATION_ERROR')
        rv = self._post_object(self.url_nt, dict(cluster=dict()), 400)
        self.assertEquals(rv['error_name'], 'VALIDATION_ERROR')
        #test_create_nt_without_name_json
        body = self.nn.copy()
        del body['node_template']['name']
        rv = self._post_object(self.url_nt, body, 400)
        self.assertEquals(rv['error_name'], 'VALIDATION_ERROR')
        #test_create_nt_without_node_type_json
        body = self.nn.copy()
        del body['node_template']['node_type']
        rv = self._post_object(self.url_nt, body, 400)
        self.assertEquals(rv['error_name'], 'VALIDATION_ERROR')
        #test_create_nt_without_flavor_id_json
        body = self.nn.copy()
        del body['node_template']['flavor_id']
        rv = self._post_object(self.url_nt, body, 400)
        self.assertEquals(rv['error_name'], 'VALIDATION_ERROR')
        #test_create_nt_without_node_param_json_nn
        body = self.nn.copy()
        del body['node_template']['name_node']
        rv = self._post_object(self.url_nt, body, 400)
        self.assertEquals(rv['error_name'], 'VALIDATION_ERROR')
        #test_create_nt_without_node_param_json_jt
        body = self.jt.copy()
        del body['node_template']['job_tracker']
        rv = self._post_object(self.url_nt, body, 400)
        self.assertEquals(rv['error_name'], 'VALIDATION_ERROR')
        #test_create_nt_without_node_param_json_jtnn
        body = self.jtnn.copy()
        del body['node_template']['job_tracker']
        del body['node_template']['name_node']
        rv = self._post_object(self.url_nt, body, 400)
        self.assertEquals(rv['error_name'], 'VALIDATION_ERROR')
        #test_create_nt_without_node_param_json_ttdn
        body = self.ttdn.copy()
        del body['node_template']['task_tracker']
        del body['node_template']['data_node']
        rv = self._post_object(self.url_nt, body, 400)
        self.assertEquals(rv['error_name'], 'VALIDATION_ERROR')

#-------------------------incorrect_value--------------------------------------

    def test_create_nt_with_incorrect_name_ttdn(self):
        param = self.ttdn.copy()
        self._post_incorrect_nt(param, 'name', '', 400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'name', '-p', 400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'name', '1p', 400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'name', '#p', 400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'name', '-', 400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'name', '1', 400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'name', '#', 400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'name', '*', 400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'name', 'node_template_2',
                                    400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'name', '!@#$%^&*()_+|{}:"<>?',
                                    400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'name', self.long_field + "q",
                                    400, 'VALIDATION_ERROR')

    def test_create_nt_with_name_with_240_symbols(self):
        body = self.jtnn.copy()
        body['node_template']['name'] = 'w'
        data = self._post_object(self.url_nt, body, 202)
        LOG.debug(data)
        data = data['node_template']
        nt_id = data.pop(u'id')
        self._del_object(self.url_nt_not_json, nt_id, 204)

    def test_create_nt_with_name_with_1_symbol(self):
        body = self.jtnn.copy()
        body['node_template']['name'] = self.long_field
        data = self._post_object(self.url_nt, body, 202)
        data = data['node_template']
        nt_id = data.pop(u'id')
        self._del_object(self.url_nt_not_json, nt_id, 204)

    def test_create_nt_with_incorrect_node_type_flavor_id(self):
        param = self.ttdn.copy()
        self._post_incorrect_nt(param, 'node_type', '*', 400,
                                'NODE_TYPE_NOT_FOUND')
        self._post_incorrect_nt(param, 'node_type', 'T', 400,
                                'NODE_TYPE_NOT_FOUND')
        self._post_incorrect_nt(param, 'node_type', '%', 400,
                                'NODE_TYPE_NOT_FOUND')
        self._post_incorrect_nt(param, 'node_type', '',
                                400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', self.long_field + "q",
                                400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'flavor_id', '',
                                400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'flavor_id', self.long_field + 'q',
                                400, 'VALIDATION_ERROR')

#-----------mismatch_node_type_and_object--------------------------------------

    def test_create_nt_ttdn_with_wront_objects(self):
        param = self.jtnn.copy()
        self._post_incorrect_nt(param, 'node_type', 'TT+DN',
                                    400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'NN',
                                     400, 'NODE_PROCESS_DISCREPANCY')
        self._post_incorrect_nt(param, 'node_type', 'JT',
                                     400, 'NODE_PROCESS_DISCREPANCY')
        param = self.jt.copy()
        self._post_incorrect_nt(param, 'node_type', 'TT+DN',
                                  400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'JT+NN',
                                   400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'NN',
                                   400, 'VALIDATION_ERROR')
        param = self.nn.copy()
        self._post_incorrect_nt(param, 'node_type', 'TT+DN',
                                  400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'JT+NN',
                                   400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'JT',
                                   400, 'VALIDATION_ERROR')
        param = self.ttdn.copy()
        self._post_incorrect_nt(param, 'node_type', 'JT+NN',
                                     400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'NN',
                                 400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'JT',
                                 400, 'VALIDATION_ERROR')
        param = self.tt.copy()
        self._post_incorrect_nt(param, 'node_type', 'TT+DN',
                                  400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'JT+NN',
                                   400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'JT',
                                   400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'NN',
                                   400, 'VALIDATION_ERROR')
        param = self.dn.copy()
        self._post_incorrect_nt(param, 'node_type', 'TT+DN',
                                  400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'JT+NN',
                                   400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'NN',
                                   400, 'VALIDATION_ERROR')
        self._post_incorrect_nt(param, 'node_type', 'JT',
                                   400, 'VALIDATION_ERROR')

    def test_create_nt_with_wrong_heap_size(self):
        data = self._change_int_value(self.url_nt, self.jt.copy(),
                                      "job_tracker", "heap_size", -2, 202)
        self._del_object(self.url_nt_not_json, data, 204)
        data = self._change_int_value(self.url_nt, self.jt.copy(),
                                      "job_tracker", "heap_size", 1, 202)
        self._del_object(self.url_nt_not_json, data, 204)
        data = self._change_int_value(self.url_nt, self.jt.copy(),
                                      "job_tracker", "heap_size", 'abs', 202)
        self._del_object(self.url_nt_not_json, data, 204)

    def test_create_nt_with_wtong_field(self):
        data = self._change_field(self.url_nt, self.jt,
                                  "name", "mame", 400)
        self.assertEquals(data, 'VALIDATION_ERROR')


def _get_templates_stub_data():
    return {
        u'node_templates': [
            {
                u'job_tracker': {
                    u'heap_size': u'896'
                },
                u'name': u'jt_nn.small',
                u'node_type': {
                    u'processes': [
                        u'job_tracker', u'name_node'
                    ],
                    u'name': u'JT+NN'
                },
                u'flavor_id': u'm1.small',
                u'name_node': {
                    u'heap_size': u'896'
                }
            },
            {
                u'job_tracker': {
                    u'heap_size': u'1792'
                },
                u'name': u'jt_nn.medium',
                u'node_type': {
                    u'processes': [
                        u'job_tracker', u'name_node'
                    ], u'name': u'JT+NN'
                },
                u'flavor_id': u'm1.medium',
                u'name_node': {
                    u'heap_size': u'1792'
                }
            },
            {
                u'name': u'tt_dn.small',
                u'task_tracker': {
                    u'heap_size': u'896'
                },
                u'data_node': {
                    u'heap_size': u'896'
                },
                u'node_type': {
                    u'processes': [
                        u'task_tracker', u'data_node'
                    ],
                    u'name': u'TT+DN'
                },
                u'flavor_id': u'm1.small'
            },
            {
                u'name': u'tt_dn.medium',
                u'task_tracker': {
                    u'heap_size': u'1792'
                },
                u'data_node': {
                    u'heap_size': u'1792'
                },
                u'node_type': {
                    u'processes': [
                        u'task_tracker', u'data_node'
                    ],
                    u'name': u'TT+DN'
                },
                u'flavor_id': u'm1.medium'
            }
        ]
    }
