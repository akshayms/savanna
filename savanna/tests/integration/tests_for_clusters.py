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
import copy
from savanna.openstack.common import log as logging
from savanna.tests.integration.db import ValidationTestCase


LOG = logging.getLogger(__name__)


class TestValidationApiForClusters(ValidationTestCase):

    def test_01_telnet(self):
        self._tn()

    # -------------------------------------------------------------------------
    # Positive tests crud operation for cluster
    # -------------------------------------------------------------------------
    def test_crud_operation_for_cluster_with_long_name(self):
        body = copy.deepcopy(self.cluster_data_jtnn_ttdn_small)
        get_body = copy.deepcopy(self.get_cluster_data_jtnn_ttdn_small)
        body['cluster']['name'] = self.long_field
        get_body[u'name'] = u'%s' % self.long_field
        self._crud_object(body, get_body, self.url_cluster)

    def test_crud_operation_for_cluster_with_one_node(self):
        body = copy.deepcopy(self.cluster_data_jtnn)
        get_body = copy.deepcopy(self.get_cluster_data_jtnn)
        self._crud_object(body, get_body, self.url_cluster)

    # -------------------------------------------------------------------------
    # Negative tests for cluster deletion and get cluster
    # -------------------------------------------------------------------------
    def test_nonexistent_cluster(self):
        body = copy.deepcopy(self.cluster_data_jtnn_ttdn)
        get_body = copy.deepcopy(self.get_cluster_data_jtnn_ttdn)

        #delete nonexistent cluster
        cluster_id = self._crud_object(body, get_body, self.url_cluster)
        data = self.delete(self.url_cluster_without_json + cluster_id)
        self.assertEquals(data.status_code, 404)

        #get nonexistent cluster
        data = self.get(self.url_cluster_without_json + cluster_id)
        self.assertEquals(data.status_code, 404)

    #--------------------------------------------------------------------------
    # Negative tests for cluster creation
    # -------------------------------------------------------------------------
    def test_cluster_name_validation(self):
        self._assert_incorrect_value_of_field('name', '')
        self._assert_incorrect_value_of_field('name', 'ab@#cd')
        self._assert_incorrect_value_of_field('name', 'ab cd')
        self._assert_incorrect_value_of_field('name', self.long_field + 'a')

    def test_cluster_creation_with_empty_body(self):
        self._assert_error(dict(cluster=dict()), u'VALIDATION_ERROR')

    def test_cluster_creation_with_empty_json(self):
        self._assert_error(dict(), u'VALIDATION_ERROR')

    def test_duplicate_cluster_creation(self):
        body = copy.deepcopy(self.cluster_data_jtnn_ttdn)
        data = self._post_object(self.url_cluster, body, 202)
        self._assert_error(body, u'CLUSTER_NAME_ALREADY_EXISTS')
        data = data['cluster']
        cluster_id = data.pop(u'id')
        i = 1
        while data[u'status'] != u'Active':
            if i > 60:
                self._del_object(self.url_cluster_without_json, cluster_id,
                                 204)
            data = self._get_object(self.url_cluster_without_json, cluster_id,
                                    200)
            data = data['cluster']
            eventlet.sleep(10)
            i += 1
        self._del_object(self.url_cluster_without_json, cluster_id, 204)
        eventlet.sleep(10)

    def test_base_image_id_validation(self):
        self._assert_incorrect_value_of_field('base_image_id', '')
        self._assert_incorrect_value_of_field('base_image_id', 'abc')

    def test_validation_cluster_body(self):
        self._assert_bad_cluster_body('name')
        self._assert_bad_cluster_body('base_image_id')
        self._assert_bad_cluster_body('node_templates')

    def test_node_template_validation(self):
        body = copy.deepcopy(self.cluster_data_jtnn_ttdn)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', -1)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', 0)
        self._assert_not_single_jt_nn(body, 'jt_nn.medium', 2)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'tt_dn.small', -1)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'tt_dn.small', 0)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.medium', 'abc')
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'tt_dn.small', 'abc')

        change_body = self._assert_change_cluster_body(
            body, 'jt_nn.medium', 'abc')
        self._assert_error(change_body, u'NODE_TEMPLATE_NOT_FOUND')

        change_body = self._assert_change_cluster_body(
            body, 'jt_nn.medium', '')
        self._assert_error(change_body, u'NODE_TEMPLATE_NOT_FOUND')

        change_body = self._assert_change_cluster_body(
            body, 'tt_dn.small', '')
        self._assert_error(change_body, u'NODE_TEMPLATE_NOT_FOUND')

        change_body = self._assert_change_cluster_body(
            body, 'tt_dn.small', 'abc')
        self._assert_error(change_body, u'NODE_TEMPLATE_NOT_FOUND')

        change_body = self._assert_delete_part_of_cluster_body(
            body, 'jt_nn.medium')
        self._assert_error(change_body, u'NOT_SINGLE_NAME_NODE')

        body = copy.deepcopy(self.cluster_data_jtnn)

        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.small', -1)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.small', 0)
        self._assert_not_single_jt_nn(body, 'jt_nn.medium', 2)
        self._assert_node_template_with_incorrect_number_of_node(
            body, 'jt_nn.small', 'abc')

        change_body = self._assert_change_cluster_body(
            body, 'jt_nn.small', '')
        self._assert_error(change_body, u'NODE_TEMPLATE_NOT_FOUND')

        change_body = self._assert_change_cluster_body(
            body, 'jt_nn.small', 'abc')
        self._assert_error(change_body, u'NODE_TEMPLATE_NOT_FOUND')

        change_body = self._assert_delete_part_of_cluster_body(
            body, 'jt_nn.small')
        self._assert_error(change_body, u'NOT_SINGLE_NAME_NODE')

    def test_validation_fields_of_cluster_body(self):
        self._assert_incorrect_fields_of_cluster_body('name', 'abc')
        self._assert_incorrect_fields_of_cluster_body('name', '')

        self._assert_incorrect_fields_of_cluster_body('base_image_id', 'abc')
        self._assert_incorrect_fields_of_cluster_body('base_image_id', '')

        self._assert_incorrect_fields_of_cluster_body('node_templates', 'abc')
        self._assert_incorrect_fields_of_cluster_body('node_templates', '')

        self._assert_incorrect_field_cluster('abc')
        self._assert_incorrect_field_cluster('')