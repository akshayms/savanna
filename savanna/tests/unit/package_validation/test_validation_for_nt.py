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
    return [u'base-image-id', u'base-image-id_2']


CONF = cfg.CONF
CONF.import_opt('debug', 'savanna.openstack.common.log')
CONF.import_opt('allow_cluster_ops', 'savanna.config')
CONF.import_opt('database_uri', 'savanna.storage.db', group='sqlalchemy')
CONF.import_opt('echo', 'savanna.storage.db', group='sqlalchemy')


class ValidationTestForNTApi(unittest.TestCase):
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
        self.url = '/v0.2/some-tenant-id/node-templates.json'
        self.url_not_json = '/v0.2/some-tenant-id/node-templates/'
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

    def post_nt(self, body, code):
        LOG.debug(body)
        post = self.app.post(self.url, data=json.dumps(body))
        self.assertEquals(post.status_code, code)
        data = json.loads(post.data)
        return data

    def get_nt(self, ip, code):
        rv = self.app.get(self.url_not_json + ip)
        self.assertEquals(rv.status_code, code)
        data = json.loads(rv.data)
        return data

    def del_nt(self, ip, code):
        rv = self.app.delete(self.url_not_json + ip)
        self.assertEquals(rv.status_code, code)
        if rv.status_code!=204:
            data = json.loads(rv.data)
            return data

    def test_list_node_templates(self):
        rv = self.app.get(self.url)
        self.assertEquals(rv.status_code, 200)
        data = json.loads(rv.data)
        for idx in xrange(0, len(data.get(u'node_templates'))):
            del data.get(u'node_templates')[idx][u'id']

        self.assertEquals(data, _get_templates_stub_data())

    def test_create_and_delete_nt_ttdn(self):
        body = self.ttdn.copy()
        data = self.post_nt(body, 202)
        data = data['node_template']
        ip = data.pop(u'id')
        self.assertEquals(data,
                        {
                            u'name': u'test-template-2',
                            u'data_node': {u'heap_size': u'2345'},
                            u'task_tracker': {u'heap_size': u'1234'},
                            u'node_type':
                                {u'processes': [u'task_tracker', u'data_node'],
                                u'name': u'TT+DN'},
                            u'flavor_id': u'test_flavor'
                        }
        )
        get_data = self.get_nt(ip, 200)
        LOG.debug("!!!!!!!!!!!!!!!{}!!!!!!!!!!!!!!!!!!!!!")
        LOG.debug(get_data)
        get_data = get_data['node_template']
        del get_data[u'id']
        self.assertEquals(get_data,
                          {
                              u'name': u'test-template-2',
                              u'data_node': {u'heap_size': u'2345'},
                              u'task_tracker': {u'heap_size': u'1234'},
                              u'node_type':
                                {u'processes': [u'task_tracker', u'data_node'],
                                u'name': u'TT+DN'},
                              u'flavor_id': u'test_flavor'
                          }
        )
        self.del_nt(ip, 204)

    def test_create_and_delete_nt_jtnn(self):
        body = self.jtnn.copy()
        data = self.post_nt(body, 202)
        data = data['node_template']
        ip = data.pop(u'id')
        self.assertEquals(data,
                          {
                              u'name': u'test-template-1',
                              u'name_node': {u'heap_size': u'2345'},
                              u'job_tracker': {u'heap_size': u'1234'},
                              u'node_type':
                                  {u'processes': [u'job_tracker', u'name_node'],
                                   u'name': u'JT+NN'},
                              u'flavor_id': u'test_flavor'
                          }
        )
        get_data = self.get_nt(ip, 200)
        get_data = get_data['node_template']
        del get_data[u'id']
        self.assertEquals(get_data,
                          {
                              u'name': u'test-template-1',
                              u'name_node': {u'heap_size': u'2345'},
                              u'job_tracker': {u'heap_size': u'1234'},
                              u'node_type':
                                  {u'processes': [u'job_tracker', u'name_node'],
                                   u'name': u'JT+NN'},
                              u'flavor_id': u'test_flavor'
                          }
        )
        self.del_nt(ip, 204)

    def test_create_and_delete_nt_nn(self):
        body = self.nn.copy()
        data = self.post_nt(body, 202)
        data = data['node_template']
        ip = data.pop(u'id')
        self.assertEquals(data,
                          {
                              u'name': u'test-template-4',
                              u'name_node': {u'heap_size': u'2345'},
                              u'node_type':
                                  {u'processes': [u'name_node'],
                                   u'name': u'NN'},
                              u'flavor_id': u'test_flavor'
                          }
        )
        get_data = self.get_nt(ip, 200)
        get_data = get_data['node_template']
        del get_data[u'id']
        self.assertEquals(get_data,
                          {
                              u'name': u'test-template-4',
                              u'name_node': {u'heap_size': u'2345'},
                              u'node_type':
                                  {u'processes': [u'name_node'],
                                   u'name': u'NN'},
                              u'flavor_id': u'test_flavor'
                          }
        )
        delete = self.app.delete(self.url_not_json + ip)
        self.assertEquals(delete.status_code, 204)

    def test_create_and_delete_nt_jt(self):
        body = self.jt.copy()
        data = self.post_nt(body, 202)
        data = data['node_template']
        ip = data.pop(u'id')
        self.assertEquals(data,
                          {
                              u'name': u'test-template-3',
                              u'job_tracker': {u'heap_size': u'1234'},
                              u'node_type':
                                  {u'processes': [u'job_tracker'],
                                   u'name': u'JT'},
                              u'flavor_id': u'test_flavor'
                          }
        )
        get_data = self.get_nt(ip, 200)
        get_data = get_data['node_template']
        del get_data[u'id']
        self.assertEquals(get_data,
                          {
                              u'name': u'test-template-3',
                              u'job_tracker': {u'heap_size': u'1234'},
                              u'node_type':
                                  {u'processes': [u'job_tracker'],
                                   u'name': u'JT'},
                              u'flavor_id': u'test_flavor'
                          }
        )
        self.del_nt(ip, 204)

    def test_create_nt_tt(self):
        body = self.tt.copy()
        data = self.post_nt(body, 400)
        LOG.debug(data)
        self.assertEquals(data['error_name'], u'NODE_TYPE_NOT_FOUND')

    def test_create_nt_dn(self):
        body = self.dn.copy()
        data = self.post_nt(body, 400)
        LOG.debug(data)
        self.assertEquals(data['error_name'], u'NODE_TYPE_NOT_FOUND')

    def test_secondary_delete_and_get_node_template(self):
        body = self.jt.copy()
        data = self.post_nt(body, 202)
        data = data['node_template']
        ip = data.pop(u'id')
        self.assertEquals(data,
                          {
                              u'name': u'test-template-3',
                              u'job_tracker': {u'heap_size': u'1234'},
                              u'node_type':
                                  {u'processes': [u'job_tracker'],
                                   u'name': u'JT'},
                              u'flavor_id': u'test_flavor'
                          }
        )
        get_data = self.get_nt(ip, 200)
        get_data = get_data['node_template']
        del get_data[u'id']
        self.assertEquals(get_data,
                          {
                              u'name': u'test-template-3',
                              u'job_tracker': {u'heap_size': u'1234'},
                              u'node_type':
                                  {u'processes': [u'job_tracker'],
                                   u'name': u'JT'},
                              u'flavor_id': u'test_flavor'
                          }
        )
        self.del_nt(ip, 204)
    #     get_data = self.get_nt(ip, 404)
    #     self.assertEquals(get_data['error_name'], u'OBJECT_NOT_FOUND')
    #     del_data = self.del_nt(ip, 404)
    #     self.assertEquals(del_data['error_name'], u'OBJECT_NOT_FOUND')

    # def test_get_not_exist_nt(self):
    #     get_data = self.get_nt("000000001", 404)
    #     self.assertEquals(get_data['error_name'], 'OBJECT_NOT_FOUND')

    # def test_delete_not_exist_nt(self):
    #     delete_data = self.del_nt("00000001", 404)
    #     self.assertEquals(delete_data['error_name'], 'OBJECT_NOT_FOUND')
    #TODO: vrovacehv: need uncomment after fixing

    def test_create_nt_with_already_used_name(self):
        body = self.jtnn.copy()
        body['node_template']['name'] = 'sec-name'
        data = self.post_nt(body, 202)
        data = data['node_template']
        ip = data.pop(u'id')
        sec_body = self.ttdn.copy()
        sec_body['node_template']['name'] = 'sec-name'
        sec_data = self.post_nt(sec_body, 400)
        self.assertEquals(sec_data['error_name'], 'OBJECT_NOT_FOUND')
        self.del_nt(ip, 204)
        thr_data = self.post_nt(sec_body, 202)
        thr_data = thr_data['node_template']
        sec_ip = thr_data.pop(u'id')
        self.del_nt(sec_ip, 204)

    def test_create_nt_with_empty_json(self):
        body = {}
        rv = self.post_nt(body, 400)
        self.assertEquals(rv['error_name'], '')

    def test_create_nt_without_name_json(self):
        body = self.nn.copy()
        del body['node_template']['name']
        rv = self.post_nt(body, 400)
        self.assertEquals(rv['error_name'], '')

    def test_create_nt_without_node_type_json(self):
        body = self.nn.copy()
        del body['node_template']['node_type']
        rv = self.post_nt(body, 400)
        self.assertEquals(rv['error_name'], '')

    def test_create_nt_without_flavor_id_json(self):
        body = self.nn.copy()
        del body['node_template']['flavor_id']
        rv = self.post_nt(body, 400)
        self.assertEquals(rv['error_name'], '')

    def test_create_nt_without_node_param_json_nn(self):
        body = self.nn.copy()
        del body['node_template']['name_node']
        rv = self.post_nt(body, 400)
        self.assertEquals(rv['error_name'], '')

    def test_create_nt_without_node_param_json_jt(self):
        body = self.jt.copy()
        del body['node_template']['job_tracker']
        rv = self.post_nt(body, 400)
        self.assertEquals(rv['error_name'], '')

    def test_create_nt_without_node_param_json_jtnn(self):
        body = self.jtnn.copy()
        del body['node_template']['job_tracker']
        del body['node_template']['name_node']
        rv = self.post_nt(body, 400)
        self.assertEquals(rv['error_name'], '')

    def test_create_nt_without_node_param_json_ttdn(self):
        body = self.ttdn.copy()
        del body['node_template']['task_tracker']
        del body['node_template']['data_node']
        rv = self.post_nt(body, 400)
        self.assertEquals(rv['error_name'], '')

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
                u'job_tracker': {
                    u'heap_size': u'1792'
                },
                u'name': u'jt.small',
                u'node_type': {
                    u'processes': [
                        u'job_tracker'
                    ],
                    u'name': u'JT'
                },
                u'flavor_id': u'm1.small'
            },
            {
                u'job_tracker': {
                    u'heap_size': u'3712'
                },
                u'name': u'jt.medium',
                u'node_type': {
                    u'processes': [
                        u'job_tracker'
                    ],
                    u'name': u'JT'},
                u'flavor_id': u'm1.medium'
            },
            {
                u'name': u'nn.small',
                u'node_type': {
                    u'processes': [
                        u'name_node'
                    ],
                    u'name': u'NN'
                },
                u'flavor_id': u'm1.small',
                u'name_node': {
                    u'heap_size': u'1792'
                }
            },
            {
                u'name': u'nn.medium',
                u'node_type': {
                    u'processes': [
                        u'name_node'
                    ],
                    u'name': u'NN'
                },
                u'flavor_id': u'm1.medium',
                u'name_node': {
                    u'heap_size': u'3712'
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