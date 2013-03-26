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

        self.cluster_data = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'jt_nn.medium': 1,
                    'tt_dn.small': 5
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

    def test_required_cluster_name(self):
        body = self.cluster_data.copy()
        body['cluster'].pop('name')
        rv = self.app.post(self.url, data=json.dumps(body))
        self.assertEquals(rv.status_code, 400)
        resp = json.loads(rv.data)
        self.assertEquals(resp['error_name'], u'VALIDATION_ERROR')
        self.assertEquals(resp['error_code'], 400)

    def test_blank_cluster_name(self):
        body = self.cluster_data.copy()
        body['cluster']['name'] = ''
        # LOG.debug(body)
        rv = self.app.post(self.url, data=json.dumps(body))

        self.assertEquals(rv.status_code, 400)
        resp = json.loads(rv.data)
        # LOG.debug(resp)
        self.assertEquals(resp['error_name'], u'VALIDATION_ERROR')
        self.assertEquals(resp['error_code'], 400)