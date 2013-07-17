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

from savanna.tests.ui import base


class UIClusterCreate(base.UITestCase):

    def setUp(self):
        super(UIClusterCreate, self).setUp()

    def test_create_cluster(self):
        self._login()
        self._create_ngt()
        self._create_cl_tmpl()
        self._create_cluster()

    def tearDown(self):
        super(UIClusterCreate, self).tearDown()