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
import tempfile
import unittest
import uuid
import os

import eventlet
from oslo.config import cfg

from savanna.main import make_app
from savanna.service import api
from savanna.storage.defaults import setup_defaults
from savanna.storage.models import Node, NodeTemplate
from savanna.storage.db import DB
import savanna.main
from savanna.utils import scheduler
from savanna.utils.openstack import nova
from savanna.openstack.common import log as logging

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
    return [u'test-image']


CONF = cfg.CONF
CONF.import_opt('debug', 'savanna.openstack.common.log')
CONF.import_opt('allow_cluster_ops', 'savanna.config')
CONF.import_opt('database_uri', 'savanna.storage.db', group='sqlalchemy')
CONF.import_opt('echo', 'savanna.storage.db', group='sqlalchemy')


class TestValidationApi(unittest.TestCase):
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

        app = make_app()

        DB.drop_all()
        DB.create_all()
        setup_defaults(True, True)

        LOG.debug('Test db path: %s', self.db_path)
        LOG.debug('Test app.config: %s', app.config)

        self.app = app.test_client()
        self.url = '/v0.2/some-tenant-id/clusters.json'
        self.url_not_json = '/v0.2/some-tenant-id/clusters/'

        self.cluster_data_jtnn_ttdn = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'jt_nn.medium': 1,
                    'tt_dn.small': 5
                }
            ))

        self.cluster_data_jt_nn_ttdn = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    'nn.medium': 1,
                    'tt_dn.small': 5
                }
            ))

        self.cluster_data_jtnn = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'jt_nn.medium': 1
                }
            ))

        self.cluster_data_jt_nn = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    'nn.medium': 1
                }
            ))

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
        LOG.debug(name)
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

    def _assert_bad_node_template(self, body, node_type, count):
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


    # def test_positive_scripts(self):
    #     rv = self.app.get(self.url)
    #     self.assertEquals(rv.status_code, 200)
    #     data = json.loads(rv.data)
    #     data = data['clusters']
    #     self.assertEquals(data, [])
    #
    #     rv = self.app.post(self.url, data=json.dumps(self.cluster_data))
    #     self.assertEquals(rv.status_code, 202)
    #     data = json.loads(rv.data)
    #     data = data['cluster']
    #     cluster_id = data.pop(u'id')
    #     self.assertEquals(data, {
    #             u'status': u'Starting',
    #             u'service_urls': {},
    #         u'name': u'test-cluster',
    #         u'base_image_id': u'test-image',
    #         u'node_templates': {
    #             u'jt_nn.medium': 1,
    #             u'tt_dn.small': 5
    #         },
    #         u'nodes': []
    #     })
    #
    #     get = self.app.get(self.url_not_json + cluster_id)
    #     self.assertEquals(get.status_code, 200)
    #     get_data = json.loads(get.data)
    #     get_data = get_data['cluster']
    #     self.assertEquals(get_data.pop(u'id'), cluster_id)
    #     self.assertEquals(get_data, {
    #                                     u'status': u'Starting',
    #                                     u'service_urls': {},
    #                                     u'name': u'test-cluster',
    #                                     u'base_image_id': u'test-image',
    #                                     u'node_templates':
    #                                     {
    #                                         u'jt_nn.medium': 1,
    #                                         u'tt_dn.small': 5
    #                                     },
    #                                     u'nodes': []
    #                                 })
    #
    #     rv = self.app.delete(self.url_not_json + cluster_id)
    #     self.assertEquals(rv.status_code, 204)
    #
    #     sec_get = self.app.get(self.url_not_json + cluster_id)
    #     self.assertEquals(sec_get.status_code, 200)
    #     sec_get_data = json.loads(sec_get.data)
    #     sec_get_data = sec_get_data['cluster']
    #     self.assertEquals(sec_get_data.pop(u'id'), cluster_id)
    #     self.assertEquals(sec_get_data, {
    #                                         u'base_image_id': u'test-image',
    #                                         u'name': u'test-cluster',
    #                                         u'node_templates':
    #                                         {
    #                                             u'jt_nn.medium': 1,
    #                                             u'tt_dn.small': 5
    #                                         },
    #                                         u'nodes': [],
    #                                         u'service_urls': {},
    #                                         u'status': u'Stoping'
    #                                     })

    #Negative tests cluster creation
    def test_cluster_name_validation(self):
        self._assert_bad_cluster_name('')
        self._assert_bad_cluster_name('@#$')
        self._assert_bad_cluster_name('ab cd')

        str = "a"
        name = "b"
        while len(name) < 241:
            name += str
        self._assert_bad_cluster_name(name)

    def test_duplicate_cluster_creation(self):
        body = self.cluster_data_jtnn_ttdn.copy()
        self._create_cluster(body)
        resp = self._create_cluster(body)

        self._assert_error(resp, u'CLUSTER_NAME_ALREADY_EXISTS', 400)

    def test_base_image_id_validation(self):
        self._assert_bad_base_image_id('')
        self._assert_bad_base_image_id('abc')

    def test_node_template_validation(self):
        body = self.cluster_data_jtnn_ttdn

        self._assert_bad_node_template(body, 'jt_nn.medium', -1)
        self._assert_bad_node_template(body, 'tt_dn.small', -1)
        self._assert_bad_node_template(body, 'jt_nn.medium', 0)
        self._assert_bad_node_template(body, 'tt_dn.small', 0)

        self._assert_bad_node_template(body, 'jt_nn.medium', 'abc')
        self._assert_bad_node_template(body, 'tt_dn.small', 'abc')
        self._assert_bad_node_template(body, 'jt_nn.medium', None)
        self._assert_bad_node_template(body, 'tt_dn.small', None)

        body = self.cluster_data_jt_nn_ttdn

        self._assert_bad_node_template(body, 'jt.medium', -1)
        self._assert_bad_node_template(body, 'nn.medium', -1)
        self._assert_bad_node_template(body, 'tt_dn.small', -1)
        self._assert_bad_node_template(body, 'jt.medium', 0)
        self._assert_bad_node_template(body, 'nn.medium', 0)
        self._assert_bad_node_template(body, 'tt_dn.small', 0)

        self._assert_bad_node_template(body, 'jt.medium', 'abc')
        self._assert_bad_node_template(body, 'nn.medium', 'abc')
        self._assert_bad_node_template(body, 'tt_dn.small', 'abc')
        self._assert_bad_node_template(body, 'jt.medium', None)
        self._assert_bad_node_template(body, 'nn.medium', None)
        self._assert_bad_node_template(body, 'tt_dn.small', None)

        body = self.cluster_data_jtnn

        self._assert_bad_node_template(body, 'jt_nn.medium', -1)
        self._assert_bad_node_template(body, 'jt_nn.medium', 0)

        self._assert_bad_node_template(body, 'jt_nn.medium', 'abc')
        self._assert_bad_node_template(body, 'jt_nn.medium', None)

        body = self.cluster_data_jt_nn

        self._assert_bad_node_template(body, 'jt.medium', -1)
        self._assert_bad_node_template(body, 'nn.medium', -1)
        self._assert_bad_node_template(body, 'jt.medium', 0)
        self._assert_bad_node_template(body, 'nn.medium', 0)

        self._assert_bad_node_template(body, 'jt.medium', 'abc')
        self._assert_bad_node_template(body, 'nn.medium', 'abc')
        self._assert_bad_node_template(body, 'jt.medium', None)
        self._assert_bad_node_template(body, 'nn.medium', None)

        body = dict(
            cluster=dict(
                name='test-cluster-1',
                base_image_id='test-image',
                node_templates={
                    '': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-2',
                base_image_id='test-image',
                node_templates={
                    'abc': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-3',
                base_image_id='test-image',
                node_templates={
                    'jt_nn.medium': 1,
                    '': 5
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-4',
                base_image_id='test-image',
                node_templates={
                    'jt_nn.medium': 1,
                    'abc': 5
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-5',
                base_image_id='test-image',
                node_templates={
                    'tt_dn.small': 5
                }
            ))
        self._assert_bad_node_template_without_node_type_nn(body)

        body = dict(
            cluster=dict(
                name='test-cluster-6',
                base_image_id='test-image',
                node_templates={
                    '': 1,
                    'nn.medium': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-7',
                base_image_id='test-image',
                node_templates={
                    'abc': 1,
                    'nn.medium': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-8',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    '': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-9',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    'abc': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-10',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    'nn.medium': 1,
                    '': 5
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-11',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    'nn.medium': 1,
                    'abc': 5
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-12',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_bad_node_template_without_node_type_nn(body)

        body = dict(
            cluster=dict(
                name='test-cluster-13',
                base_image_id='test-image',
                node_templates={
                    'nn.medium': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_bad_node_template_without_node_type_jt(body)

        body = dict(
            cluster=dict(
                name='test-cluster-14',
                base_image_id='test-image',
                node_templates={
                    '': 1
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-14',
                base_image_id='test-image',
                node_templates={
                    'abc': 1
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster-15',
                base_image_id='test-image',
                node_templates={}
            ))
        self._assert_bad_node_template_without_node_type_nn(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    '': 1
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    'abc': 1
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1
                }
            ))
        self._assert_bad_node_template_without_node_type_nn(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    '': 1,
                    'nn.medium': 1
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'abc': 1,
                    'nn.medium': 1
                }
            ))
        self._assert_bad_node_template_with_wrong_node_type(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'nn.medium': 1
                }
            ))
        self._assert_bad_node_template_without_node_type_jt(body)

    def test_validation_cluster_body(self):
        self._assert_bad_cluster_body('name')
        self._assert_bad_cluster_body('base_image_id')
        self._assert_bad_cluster_body('node_templates')
