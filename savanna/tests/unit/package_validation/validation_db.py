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

import eventlet
import json
import os
from oslo.config import cfg
import random as random_number
from savanna.service import api
from savanna.storage.db import DB
from savanna.storage.defaults import setup_defaults
from savanna.storage.models import Node, NodeTemplate
import savanna.main
from savanna.main import make_app
from savanna.openstack.common import log as logging
from savanna.utils.openstack import nova
from savanna.utils import scheduler
import tempfile
import unittest
import uuid

LOG = logging.getLogger(__name__)


def _stub_vm_creation_job(template_id):
    template = NodeTemplate.query.filter_by(id=template_id).first()
    eventlet.sleep(2)
    return 'ip-address', uuid.uuid4().hex, template.id


def _stub_launch_cluster(headers, cluster):
    LOG.debug('stub launch_cluster called with %s, %s', headers, cluster)
    pile = eventlet.GreenPile(scheduler.POOL)

    for elem in cluster.node_counts:
        node_count = elem.count
        for _ in xrange(0, node_count):
            pile.spawn(_stub_vm_creation_job, elem.node_template_id)

    for (ip, vm_id, elem) in pile:
        DB.session.add(Node(vm_id, cluster.id, elem))
        LOG.debug("VM '%s/%s/%s' created", ip, vm_id, elem)


def _stub_stop_cluster(headers, cluster):
    LOG.debug("stub stop_cluster called with %s, %s", headers, cluster)


def _stub_auth_token(*args, **kwargs):
    LOG.debug('stub token filter called with %s, %s', args, kwargs)

    def _filter(app):
        def _handler(env, start_response):
            env['HTTP_X_TENANT_ID'] = 'tenant-id-1'
            return app(env, start_response)

        return _handler

    return _filter


def _stub_auth_valid(*args, **kwargs):
    LOG.debug('stub token validation called with %s, %s', args, kwargs)

    def _filter(app):
        def _handler(env, start_response):
            return app(env, start_response)

        return _handler

    return _filter


def _stub_get_flavors(headers):
    LOG.debug('Stub get_flavors called with %s', headers)
    return [u'test_flavor', u'test_flavor_2']


def _stub_get_images(headers):
    LOG.debug('Stub get_images called with %s', headers)
    return [u'base-image-id', u'base-image-id_2']


CONF = cfg.CONF
CONF.import_opt('debug', 'savanna.openstack.common.log')
CONF.import_opt('allow_cluster_ops', 'savanna.config')
CONF.import_opt('database_uri', 'savanna.storage.db', group='sqlalchemy')
CONF.import_opt('echo', 'savanna.storage.db', group='sqlalchemy')


class ValidationTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.maxDiff = 10000

        # override configs
        CONF.set_override('debug', True)
        CONF.set_override('allow_cluster_ops', True)  # stub process
        CONF.set_override('database_uri', 'sqlite:///' + self.db_path,
                          group='sqlalchemy')
        CONF.set_override('echo', False, group='sqlalchemy')

        # store functions that will be stubbed
        self._prev_auth_token = savanna.main.auth_token
        self._prev_auth_valid = savanna.main.auth_valid
        self._prev_cluster_launch = api.cluster_ops.launch_cluster
        self._prev_cluster_stop = api.cluster_ops.stop_cluster
        self._prev_get_flavors = nova.get_flavors
        self._prev_get_images = nova.get_images

        # stub functions
        savanna.main.auth_token = _stub_auth_token
        savanna.main.auth_valid = _stub_auth_valid
        api.cluster_ops.launch_cluster = _stub_launch_cluster
        api.cluster_ops.stop_cluster = _stub_stop_cluster
        nova.get_flavors = _stub_get_flavors
        nova.get_images = _stub_get_images

        app = savanna.main.make_app()

        DB.drop_all()
        DB.create_all()
        setup_defaults(True, True)

        LOG.debug('Test db path: %s', self.db_path)
        LOG.debug('Test app.config: %s', app.config)

        self.app = app.test_client()

        self.long_field = "qwertyuiop"
        for i in range(23):
            self.long_field += "%d" % random_number.randint(1000000000,
                                                        9999999999)

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

        #----------------------add_value_for_clusters--------------------------
        self.url = '/v0.2/some-tenant-id/clusters'

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

    def tearDown(self):
        # unstub functions
        savanna.main.auth_token = self._prev_auth_token
        savanna.main.auth_valid = self._prev_auth_valid
        api.cluster_ops.launch_cluster = self._prev_cluster_launch
        api.cluster_ops.stop_cluster = self._prev_cluster_stop
        nova.get_flavors = self._prev_get_flavors
        nova.get_images = self._prev_get_images

        os.close(self.db_fd)
        os.unlink(self.db_path)

#---------------------for_node_templates---------------------------------------

    def _post_incorrect_nt_ttdn(self, field, value, code, error):
        body = self.ttdn.copy()
        body['node_template']['%s' % field] = '%s' % value
        rv = self._post_object(self.url_nt, body, code)
        self.assertEquals(rv['error_name'], '%s' % error)

    def _post_incorrect_nt_jtnn(self, field, value, code, error):
        body = self.jtnn.copy()
        body['node_template']['%s' % field] = '%s' % value
        rv = self._post_object(self.url_nt, body, code)
        self.assertEquals(rv['error_name'], '%s' % error)

    def _post_incorrect_nt_jt(self, field, value, code, error):
        body = self.jt.copy()
        body['node_template']['%s' % field] = '%s' % value
        rv = self._post_object(self.url_nt, body, code)
        self.assertEquals(rv['error_name'], '%s' % error)

    def _post_incorrect_nt_nn(self, field, value, code, error):
        body = self.nn.copy()
        body['node_template']['%s' % field] = '%s' % value
        rv = self._post_object(self.url_nt, body, code)
        self.assertEquals(rv['error_name'], '%s' % error)

    def _post_incorrect_nt_tt(self, field, value, code, error):
        body = self.tt.copy()
        body['node_template']['%s' % field] = '%s' % value
        rv = self._post_object(self.url_nt, body, code)
        self.assertEquals(rv['error_name'], '%s' % error)

    def _post_incorrect_nt_dn(self, field, value, code, error):
        body = self.dn.copy()
        body['node_template']['%s' % field] = '%s' % value
        rv = self._post_object(self.url_nt, body, code)
        self.assertEquals(rv['error_name'], '%s' % error)

#---------------------for_clusters---------------------------------------------

    def _assert_error(self, resp, name, code):
        self.assertEquals(resp['error_name'], name)
        self.assertEquals(resp['error_code'], code)

    def _assert_validation_error_400(self, resp):
        self._assert_error(resp, u'VALIDATION_ERROR', 400)

    def _assert_image_not_found_400(self, resp):
        self._assert_error(resp, u'IMAGE_NOT_FOUND', 400)

    def _assert_node_template_not_found_400(self, resp):
        self._assert_error(resp, u'NODE_TEMPLATE_NOT_FOUND', 400)

    def _assert_not_single_name_node_400(self, resp):
        self._assert_error(resp, u'NOT_SINGLE_NAME_NODE', 400)

    def _assert_not_single_job_tracker_400(self, resp):
        self._assert_error(resp, u'NOT_SINGLE_JOB_TRACKER', 400)

    def _create_cluster(self, body):
        rv = self.app.post(self.url, data=json.dumps(body))
        resp = json.loads(rv.data)
        return resp

    def _assert_bad_cluster_name(self, name):
        body = self.cluster_data_jtnn_ttdn.copy()
        body['cluster']['name'] = name
        resp = self._create_cluster(body)
        self._assert_validation_error_400(resp)

    def _assert_bad_base_image_id(self, base_image_id):
        body = self.cluster_data_jtnn_ttdn.copy()
        body['cluster']['base_image_id'] = base_image_id
        resp = self._create_cluster(body)
        if base_image_id == '':
            self._assert_validation_error_400(resp)
        else:
            self._assert_image_not_found_400(resp)

    def _assert_n_t_with_not_single_jt_nn(self, body, node_type, count):
        body['cluster']['node_templates'][node_type] = count
        resp = self._create_cluster(body)
        if (node_type == 'jt_nn.medium') or (node_type == 'nn.medium'):
            self._assert_not_single_name_node_400(resp)
        else:
            self._assert_not_single_job_tracker_400(resp)

    def _assert_n_t_with_wrong_number_jt_nn(self, body, node_type, count):
        body['cluster']['node_templates'][node_type] = count
        resp = self._create_cluster(body)
        self._assert_validation_error_400(resp)

    def _assert_bad_node_template_with_wrong_node_type(self, body):
        resp = self._create_cluster(body)
        self._assert_node_template_not_found_400(resp)

    def _assert_bad_node_template_without_node_type_nn(self, body):
        resp = self._create_cluster(body)
        self._assert_not_single_name_node_400(resp)

    def _assert_bad_node_template_without_node_type_jt(self, body):
        resp = self._create_cluster(body)
        self._assert_not_single_job_tracker_400(resp)

    def _assert_bad_cluster_body(self, component):
        body = self.cluster_data_jtnn_ttdn.copy()
        body['cluster'].pop(component)
        resp = self._create_cluster(body)
        self._assert_validation_error_400(resp)