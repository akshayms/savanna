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
import copy
import random as random_number
from savanna.openstack.common import log as logging
#from savanna.tests.unit.base import SavannaTestCase
import requests
import unittest

LOG = logging.getLogger(__name__)


class ValidationTestCase(unittest.TestCase):
    def setUp(self):
        self.long_field = "qwertyuiop"
        for i in range(23):
            self.long_field += "%d" % random_number.randint(
                1000000000, 9999999999)

#----------------------add_value_for_node_templates----------------------------

        self.baseurl = 'http://127.0.0.1:8080'
        self.tenant = '6b26f08455ec449ea7a2d3da75339255'
        self.token = 'd194713645e94d3c965f41e9b95c03bb'
        self.url_nt = '/v0.2/%s/node-templates.json' % self.tenant
        self.url_nt_not_json = '/v0.2/%s/node-templates/' % self.tenant

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

#----------------------add_value_for_clusters----------------------------------

        self.url_cluster = '/v0.2/%s/clusters.json' % self.tenant
        self.url_cluster_without_json = '/v0.2/%s/clusters/' % self.tenant

        self.cluster_data_jtnn_ttdn = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='base-image-id',
                node_templates={
                    'jt_nn.medium': 1,
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

        self.get_cluster_body = {
            u'status': u'Active',
            u'service_urls': {},
            u'name': u'test-cluster',
            u'base_image_id': u'base-image-id',
            u'node_templates':
            {
                u'jt_nn.medium': 1,
                u'tt_dn.small': 5
            },
            u'nodes': []
        }

#---------------------close_setUp----------------------------------------------

    def post(self, url, body):
        URL = self.baseurl + url
        resp = requests.post(URL, data=body, headers={
            "x-auth-token": self.token, "Content-Type": "application/json"})
        print("URL = %s\ndata = %s\nresponse = %s\n"
              % (URL, body, resp.status_code))
        return resp


    def put(self, url, body):
        URL = self.baseurl + url
        resp = requests.put(URL, data=body, headers={
            "x-auth-token": self.token, "Content-Type": "application/json"})
        print("URL = %s\ndata = %s\nresponse = %s\n"
              % (URL, body, resp.status_code))
        return resp


    def get(self, url):
        URL = self.baseurl + url
        resp = requests.get(URL, headers={"x-auth-token": self.token})
        print("URL = %s\nresponse = %s\n" % (URL, resp.status_code))
        return resp


    def delete(self, url):
        URL = self.baseurl + url
        resp = requests.delete(URL, headers={"x-auth-token": self.token})
        print("URL = %s\nresponse = %s\n" % (URL, resp.status_code))
        return resp

    def _post_object(self, url, body, code):
        LOG.debug(body)
        post = self.post(url, json.dumps(body))
        self.assertEquals(post.status_code, code)
        data = json.loads(post.content)
        return data

    def _get_object(self, url, obj_id, code):
        rv = self.get(url + obj_id)
        self.assertEquals(rv.status_code, code)
        data = json.loads(rv.content)
        return data

    def _del_object(self, url, obj_id, code):
        rv = self.delete(url + obj_id)
        self.assertEquals(rv.status_code, code)
        if rv.status_code != 204:
            data = json.loads(rv.content)
            return data

    def _list_objects(self, url, code):
        rv = self.get(url)
        self.assertEquals(rv.status_code, code)
        data = json.loads(rv.content)
        return data

    def _crud_object(self, body, get_body, url, p_code, g_code, d_code):
        data = self._post_object(url, body, p_code)
        LOG.debug("`````````````(two)`````````````")
        LOG.debug(data)
        object = "cluster"
        get_url = self.url_cluster_without_json
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

    def _change_int_value(self, url, param, f_field, sec_field, value, code):
        body = copy.deepcopy(param)
        object = "cluster"
        if url != self.url_cluster:
            object = "node_template"
        body["%s" % object]["%s" % f_field]["%s" % sec_field] = value
        data = self._post_object(url, body, code)
        if code != 202:
            return data['error_name']
        return data['%s' % object]['id']

    def _change_field(self, url, param, old_field, new_field, code):
        body = copy.deepcopy(param)
        object = "cluster"
        if url != self.url_cluster:
            object = "node_template"
        value = body["%s" % object]["%s" % old_field]
        del body["%s" % object]["%s" % old_field]
        body["%s" % object]["%s" % new_field] = value
        data = self._post_object(url, body, code)
        if code != 202:
            return data['error_name']
        return data['%s' % object]['id']

#---------------------for_node_templates---------------------------------------

    def _post_incorrect_nt(self, param, field, value, code, error):
        body = copy.deepcopy(param)
        body['node_template']['%s' % field] = value
        rv = self._post_object(self.url_nt, body, code)
        self.assertEquals(rv['error_name'], '%s' % error)

#---------------------for_clusters---------------------------------------------

    def _assert_error(self, body, error_name):
        resp = self._post_object(self.url_cluster, body, 400)
        self.assertEquals(resp['error_name'], error_name)

    def _assert_delete_part_of_cluster_body(self, body, del_node_type):
        del body['cluster']['node_templates'][del_node_type]
        return body

    def _assert_change_cluster_body(
            self, body, del_node_type, set_node_type):
        data = copy.deepcopy(body)
        value = data['cluster']['node_templates'][del_node_type]
        data = self._assert_delete_part_of_cluster_body(data, del_node_type)
        data['cluster']['node_templates'][set_node_type] = value
        return data

    def _assert_incorrect_value_of_field(self, field, value_of_field):
        body = copy.deepcopy(self.cluster_data_jtnn_ttdn)
        if field == 'name':
            body['cluster']['name'] = value_of_field
            self._assert_error(body, u'VALIDATION_ERROR')
        else:
            body['cluster']['base_image_id'] = value_of_field
            resp = self._post_object(self.url_cluster, body, 400)
            if value_of_field == '':
                self.assertEquals(resp['error_name'], u'VALIDATION_ERROR')
            else:
                self.assertEquals(resp['error_name'], u'IMAGE_NOT_FOUND')

    def _assert_not_single_jt_nn(self, body, node_type, count):
        data = copy.deepcopy(body)
        data['cluster']['node_templates'][node_type] = count
        resp = self._post_object(self.url_cluster, data, 400)
        if (node_type == 'jt_nn.medium') or (node_type == 'nn.medium'):
            self.assertEquals(resp['error_name'], u'NOT_SINGLE_NAME_NODE')
        else:
            self.assertEquals(resp['error_name'], u'NOT_SINGLE_JOB_TRACKER')

    def _assert_node_template_with_incorrect_number_of_node(self, body,
                                                            node_type, count):
        data = copy.deepcopy(body)
        data['cluster']['node_templates'][node_type] = count
        self._assert_error(data, u'VALIDATION_ERROR')

    def _assert_node_template_without_node_nn(self, body):
        self._assert_error(body, u'NOT_SINGLE_NAME_NODE')

    def _assert_node_template_without_node_jt(self, body):
        self._assert_error(body, u'NOT_SINGLE_JOB_TRACKER')

    def _assert_node_template_with_incorrect_node(self, body):
        self._assert_error(body, u'NODE_TEMPLATE_NOT_FOUND')

    def _assert_bad_cluster_body(self, component):
        body = copy.deepcopy(self.cluster_data_jtnn_ttdn)
        body['cluster'].pop(component)
        self._assert_error(body, u'VALIDATION_ERROR')

    def _assert_incorrect_fields_of_cluster_body(self, old_field, new_field):
        body = copy.deepcopy(self.cluster_data_jtnn_ttdn)
        resp = self._change_field(self.url_cluster, body, old_field,
                                  new_field, 400)
        self.assertEquals(resp, u'VALIDATION_ERROR')

    def _assert_incorrect_field_cluster(self, field):
        body = copy.deepcopy(self.cluster_data_jtnn_ttdn)
        data = body['cluster']
        del body['cluster']
        body[field] = data
        self._assert_error(body, u'VALIDATION_ERROR')
