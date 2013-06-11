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


from savanna.tests.integration.db import ITestCase
from telnetlib import Telnet


class TestNGT(ITestCase):

    def setUp(self):
        super(TestNGT, self).setUp()
        Telnet(self.host, self.port)

    def test_crud_for_ngt_nn(self):
        body_nn = self.make_node_group_template("master_nn", "qa probe", "NN")
        self._crud_object(body_nn, self.url_ngt)