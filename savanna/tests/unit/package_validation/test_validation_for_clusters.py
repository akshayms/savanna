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
from savanna.openstack.common import log as logging
from savanna.tests.unit.package_validation.validation_db \
    import ValidationTestCase


LOG = logging.getLogger(__name__)


class TestValidationApiForClusters(ValidationTestCase):
    #-------------------------------------------------------------------------
    #Negative tests cluster deletion and get cluster
    #-------------------------------------------------------------------------
    def test_nonexistent_cluster_deletion_and_get(self):
        body = self.cluster_data_jtnn_ttdn.copy()

        data = self._post_object(self.url_cluster, body, 202)
        data = data['cluster']
        cluster_id = data.pop(u'id')
        self.assertEquals(data, {
            u'status': u'Starting',
            u'service_urls': {},
            u'name': u'test-cluster',
            u'base_image_id': u'base-image-id',
            u'node_templates':
            {
                u'jt_nn.medium': 1,
                u'tt_dn.small': 5
            },
            u'nodes': []
        })

        data_del = self.app.delete(self.url_cluster + '/' + cluster_id)
        self.assertEquals(data_del.status_code, 204)

        #-------------------return 500--------------------------------------
        #time.sleep(1)
        #rv_del = self.app.delete(self.url + '/' + cluster_id)
        #self.assertEquals(rv_del.status_code, 404)

        #-------------------return 500--------------------------------------
        #get = self.app.get(self.url + '/' + cluster_id)
        #self.assertEquals(get.status_code, 404)
        #-------------------------------------------------------------------

    #-------------------------------------------------------------------------
    #Negative tests cluster creation
    #-------------------------------------------------------------------------
    def test_cluster_name_validation(self):
        self._assert_incorrect_cluster_name('')
        self._assert_incorrect_cluster_name('ab@#cd')
        self._assert_incorrect_cluster_name('ab cd')

        str = "a"
        name = "b"
        while len(name) < 241:
            name += str
        self._assert_incorrect_cluster_name(name)

    def test_cluster_creation_with_empty_body(self):
        body = dict(cluster=dict())
        resp = self._post_object(self.url_cluster, body, 400)
        self._assert_error(resp, u'VALIDATION_ERROR', 400)

    #----------------------return 500---------------------------
    #def test_cluster_creation_with_empty_json(self):
        #body = dict()
        #resp = self._create_cluster(body)
    #-----------------------------------------------------------

    def test_duplicate_cluster_creation(self):
        body = self.cluster_data_jtnn_ttdn.copy()
        self.resp = self._post_object(self.url_cluster, body, 202)
        resp = self._post_object(self.url_cluster, body, 400)
        self._assert_error(resp, u'CLUSTER_NAME_ALREADY_EXISTS', 400)

    def test_base_image_id_validation(self):
        self._assert_incorrect_base_image_id('')
        self._assert_incorrect_base_image_id('abc')

    def test_node_template_validation(self):
        body = self.cluster_data_jtnn_ttdn

        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', -1)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', 0)
        self._assert_not_single_jt_nn(body, 'jt_nn.medium', 2)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', 0)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'tt_dn.small', -1)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'tt_dn.small', 0)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', 'abc')
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'tt_dn.small', 'abc')
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', None)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'tt_dn.small', None)

        body = self.cluster_data_jt_nn_ttdn

        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt.medium', -1)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt.medium', 0)
        self._assert_not_single_jt_nn(body, 'jt.medium', 2)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'nn.medium', -1)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'nn.medium', 0)
        self._assert_not_single_jt_nn(body, 'nn.medium', 2)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'tt_dn.small', -1)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'tt_dn.small', 0)

        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt.medium', 'abc')
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'nn.medium', 'abc')
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'tt_dn.small', 'abc')
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt.medium', None)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'nn.medium', None)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'tt_dn.small', None)

        body = self.cluster_data_jtnn

        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', -1)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', 0)
        self._assert_not_single_jt_nn(body, 'jt_nn.medium', 2)

        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', 'abc')
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', None)

        body = self.cluster_data_jt_nn

        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt.medium', -1)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt.medium', 0)
        self._assert_not_single_jt_nn(body, 'jt.medium', 2)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'nn.medium', -1)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'nn.medium', 0)
        self._assert_not_single_jt_nn(body, 'nn.medium', 2)

        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt.medium', 'abc')
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'nn.medium', 'abc')
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt.medium', None)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'nn.medium', None)

        body = dict(
            cluster=dict(
                name='test-cluster-1',
                base_image_id='test-image',
                node_templates={
                    '': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster-2',
                base_image_id='test-image',
                node_templates={
                    'abc': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster-3',
                base_image_id='test-image',
                node_templates={
                    'jt_nn.medium': 1,
                    '': 5
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster-4',
                base_image_id='test-image',
                node_templates={
                    'jt_nn.medium': 1,
                    'abc': 5
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster-5',
                base_image_id='test-image',
                node_templates={
                    'tt_dn.small': 5
                }
            ))
        self._assert_node_template_without_node_nn(body)

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
        self._assert_node_template_with_incorrect_node(body)

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
        self._assert_node_template_with_incorrect_node(body)

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
        self._assert_node_template_with_incorrect_node(body)

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
        self._assert_node_template_with_incorrect_node(body)

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
        self._assert_node_template_with_incorrect_node(body)

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
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster-12',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster-13',
                base_image_id='test-image',
                node_templates={
                    'nn.medium': 1,
                    'tt_dn.small': 5
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster-14',
                base_image_id='test-image',
                node_templates={
                    '': 1
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster-14',
                base_image_id='test-image',
                node_templates={
                    'abc': 1
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster-15',
                base_image_id='test-image',
                node_templates={}
            ))
        self._assert_node_template_without_node_nn(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    '': 1
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1,
                    'abc': 1
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'jt.medium': 1
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    '': 1,
                    'nn.medium': 1
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'abc': 1,
                    'nn.medium': 1
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

        body = dict(
            cluster=dict(
                name='test-cluster',
                base_image_id='test-image',
                node_templates={
                    'nn.medium': 1
                }
            ))
        self._assert_node_template_with_incorrect_node(body)

    def test_validation_cluster_body(self):
        self._assert_bad_cluster_body('name')
        self._assert_bad_cluster_body('base_image_id')
        self._assert_bad_cluster_body('node_templates')
