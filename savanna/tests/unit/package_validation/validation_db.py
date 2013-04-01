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

import json
import random as random_number
from savanna.openstack.common import log as logging
from savanna.tests.unit.base import SavannaTestCase

LOG = logging.getLogger(__name__)


class ValidationTestCase(SavannaTestCase):
    def setUp(self):
        self.long_field = "qwertyuiop"
        for i in range(23):
            self.long_field += "%d" % random_number.randint(
                1000000000, 9999999999)

    #----------------------add_value_for_node_templates------------------------

        self.url_nt = '/v0.2/some-tenant-id/node-templates.json'
        self.url_nt_not_json = '/v0.2/some-tenant-id/node-templates/'

        self.jtnn = dict(
            node_template=dict(
                name='test-template-1',
                node_type='JT+NN',
                flavor_id='test_flavor',
                job_tracker={
                    'heap_size': '1234'
                },
                name_node={
                    'heap_size': '2345'
                }
            ))
        self.ttdn = dict(
            node_template=dict(
                name='test-template-2',
                node_type='TT+DN',
                flavor_id='test_flavor',
                task_tracker={
                    'heap_size': '1234'
                },
                data_node={
                    'heap_size': '2345'
                }
            ))
        self.jt = dict(
            node_template=dict(
                name='test-template-3',
                node_type='JT',
                flavor_id='test_flavor',
                job_tracker={
                    'heap_size': '1234'
                }
            ))
        self.nn = dict(
            node_template=dict(
                name='test-template-4',
                node_type='NN',
                flavor_id='test_flavor',
                name_node={
                    'heap_size': '2345'
                }
            ))
        self.tt = dict(
            node_template=dict(
                name='test-template-5',
                node_type='TT',
                flavor_id='test_flavor',
                task_tracker={
                    'heap_size': '2345'
                }
            ))
        self.dn = dict(
            node_template=dict(
                name='test-template-6',
                node_type='DN',
                flavor_id='test_flavor',
                data_node={
                    'heap_size': '2345'
                }
            ))

        self.get_ttdn = {
            u'name': u'test-template-2',
            u'data_node': {u'heap_size': u'2345'},
            u'task_tracker': {u'heap_size': u'1234'},
            u'node_type': {
                u'processes': [u'task_tracker',
                               u'data_node'],
                u'name': u'TT+DN'},
            u'flavor_id': u'test_flavor'
        }

        self.get_jtnn = {
            u'name': u'test-template-1',
            u'name_node': {u'heap_size': u'2345'},
            u'job_tracker': {u'heap_size': u'1234'},
            u'node_type': {
                u'processes': [u'job_tracker',
                               u'name_node'],
                u'name': u'JT+NN'},
            u'flavor_id': u'test_flavor'
        }

        self.get_nn = {
            u'name': u'test-template-4',
            u'name_node': {u'heap_size': u'2345'},
            u'node_type': {
                u'processes': [u'name_node'],
                u'name': u'NN'},
            u'flavor_id': u'test_flavor'
        }

        self.get_jt = {
            u'name': u'test-template-3',
            u'job_tracker': {u'heap_size': u'1234'},
            u'node_type': {
                u'processes': [u'job_tracker'],
                u'name': u'JT'},
            u'flavor_id': u'test_flavor'
        }

        #----------------------add_value_for_clusters--------------------------

        self.url_cluster = '/v0.2/some-tenant-id/clusters'

        self.cluster_data_jtnn_ttdn = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='base-image-id',
                node_templates={
                    'jt_nn.medium': 1,
                    'tt_dn.small': 5
                }
            ))

        self.cluster_data_jt_nn_ttdn = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='base-image-id',
                node_templates={
                    'jt.medium': 1,
                    'nn.medium': 1,
                    'tt_dn.small': 5
                }
            ))

        self.cluster_data_jtnn = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='base-image-id',
                node_templates={
                    'jt_nn.medium': 1
                }
            ))

        self.cluster_data_jt_nn = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='base-image-id',
                node_templates={
                    'jt.medium': 1,
                    'nn.medium': 1
                }
            ))
        super(ValidationTestCase, self).setUp()

#---------------------close_setUp----------------------------------------------

    def _post_object(self, url, body, code):
        LOG.debug(body)
        post = self.app.post(url, data=json.dumps(body))
        self.assertEquals(post.status_code, code)
        data = json.loads(post.data)
        return data

    def _get_object(self, url, obj_id, code):
        rv = self.app.get(url + obj_id)
        self.assertEquals(rv.status_code, code)
        data = json.loads(rv.data)
        return data

    def _del_object(self, url, obj_id, code):
        rv = self.app.delete(url + obj_id)
        self.assertEquals(rv.status_code, code)
        if rv.status_code != 204:
            data = json.loads(rv.data)
            return data

    def _list_objects(self, url, code):
        rv = self.app.get(url)
        self.assertEquals(rv.status_code, code)
        data = json.loads(rv.data)
        return data

    def _grud_object(self, body, get_body, url, p_code, g_code, d_code):
        data = self._post_object(url, body, p_code)
        object = "cluster"
        get_url = self.url
        if url == self.url_nt:
            object = "node_template"
            get_url = self.url_nt_not_json
        data = data["%s" % object]
        nt_id = data.pop(u'id')
        self.assertEquals(data, get_body)
        get_data = self._get_object(get_url, nt_id, g_code)
        get_data = get_data['%s' % object]
        del get_data[u'id']
        self.assertEquals(get_data, get_body)
        self._del_object(get_url, nt_id, d_code)
        return nt_id

#---------------------for_node_templates---------------------------------------

    def _post_incorrect_nt(self, body, field, value, code, error):
        body['node_template']['%s' % field] = '%s' % value
        rv = self._post_object(self.url_nt, body, code)
        self.assertEquals(rv['error_name'], '%s' % error)

#---------------------for_clusters---------------------------------------------

    def _assert_error(self, resp, name, code):
        self.assertEquals(resp['error_name'], name)
        self.assertEquals(resp['error_code'], code)

    def _assert_incorrect_cluster_name(self, name):
        body = self.cluster_data_jtnn_ttdn.copy()
        body['cluster']['name'] = name
        resp = self._post_object(self.url_cluster, body, 400)
        self._assert_error(resp, u'VALIDATION_ERROR', 400)

    def _assert_incorrect_base_image_id(self, base_image_id):
        body = self.cluster_data_jtnn_ttdn.copy()
        body['cluster']['base_image_id'] = base_image_id
        resp = self._post_object(self.url_cluster, body, 400)
        if base_image_id == '':
            self._assert_error(resp, u'VALIDATION_ERROR', 400)
        else:
            self._assert_error(resp, u'IMAGE_NOT_FOUND', 400)

    def _assert_not_single_jt_nn(self, body, node_type, count):
        body['cluster']['node_templates'][node_type] = count
        resp = self._post_object(self.url_cluster, body, 400)
        if (node_type == 'jt_nn.medium') or (node_type == 'nn.medium'):
            self._assert_error(resp, u'NOT_SINGLE_NAME_NODE', 400)
        else:
            self._assert_error(resp, u'NOT_SINGLE_JOB_TRACKER', 400)

    def _assert_node_template_with_incorrect_number_of_node(self, body,
                                                            node_type, count):
        body['cluster']['node_templates'][node_type] = count
        resp = self._post_object(self.url_cluster, body, 400)
        self._assert_error(resp, u'VALIDATION_ERROR', 400)

    def _assert_node_template_without_node_nn(self, body):
        resp = self._post_object(self.url_cluster, body, 400)
        self._assert_error(resp, u'NOT_SINGLE_NAME_NODE', 400)

    def _assert_node_template_without_node_jt(self, body):
        resp = self._post_object(self.url_cluster, body, 400)
        self._assert_error(resp, u'NOT_SINGLE_JOB_TRACKER', 400)

    def _assert_node_template_with_incorrect_node(self, body):
        resp = self._post_object(self.url_cluster, body, 400)
        self._assert_error(resp, u'NODE_TEMPLATE_NOT_FOUND', 400)

    def _assert_bad_cluster_body(self, component):
        body = self.cluster_data_jtnn_ttdn.copy()
        body['cluster'].pop(component)
        resp = self._post_object(self.url_cluster, body, 400)
        self._assert_error(resp, u'VALIDATION_ERROR', 400)
