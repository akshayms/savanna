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
from savanna.tests.integration.db import ITestCase
import  telnetlib


class TestsClusterCRUD(ITestCase):

    def setUp(self):
        super(TestsClusterCRUD, self).setUp()

        telnetlib.Telnet(self.host, self.port)

    def test_crud_cluster_nnjt_dntt(self):
        node_processes = {1: ['jobtracker', 'namenode'],
                          2: ['tasktracker', 'datanode']}
        body = self.make_cl_body_with_ngt(node_processes)
        self._crud_object(body, self.url_cluster)

    def test_crud_cluster_nn_jtdntt(self):
        node_processes = {1: ['jobtracker'],
                          2: ['namenode', 'tasktracker', 'datanode']}
        body = self.make_cl_body_with_ngt(node_processes)
        self._crud_object(body, self.url_cluster)

    def test_crud_cluster_nn_jtdntt(self):
        node_processes = {1: ['namenode'],
                          2: ['jobtracker', 'tasktracker', 'datanode']}
        body = self.make_cl_body_with_ngt(node_processes)
        self._crud_object(body, self.url_cluster)

    def test_crud_cluster_nnjtdntt(self):
        node_processes = {1: ['jobtracker', 'namenode',
                              'tasktracker', 'datanode']}
        body = self.make_cl_body_with_ngt(node_processes)
        self._crud_object(body, self.url_cluster)

    def test_crud_cluster_nnjt_dntt(self):
        node_processes = {1: ['jobtracker'], 1: ['namenode'],
                          3: ['tasktracker', 'datanode']}
        body = self.make_cl_body_with_ngt(node_processes)
        self._crud_object(body, self.url_cluster)
