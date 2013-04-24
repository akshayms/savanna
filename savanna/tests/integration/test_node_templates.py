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

from savanna.tests.integration.db import ValidationTestCase
from telnetlib import Telnet


class TestValidationApiForNodetemplates(ValidationTestCase):
    def setUp(self):
        super(TestValidationApiForNodetemplates, self).setUp()
        Telnet(self.host, self.port)

    def test_crud_nt_jtnn(self):
        nt_jtnn = self.make_nt("master", "jtnn", 1024, 1024)
        get_jtnn = self._get_body_nt("jtnn", "master", 1024, 1024)
        self._crud_object(nt_jtnn, get_jtnn, self.url_nt)

    def test_crud_nt_ttdn(self):
        nt_ttdn = self.make_nt("worker", "jtnn", 1024, 1024)
        get_ttdn = self._get_body_nt("jtnn", "worker", 1024, 1024)
        self._crud_object(nt_ttdn, get_ttdn, self.url_nt)


    # def test_crud_nt_nn(self):
    #     self._crud_object(self.nn, self.get_nn.copy(),
    #                       self.url_nt)
    #
    # def test_crud_nt_jt(self):
    #     self._crud_object(self.jt, self.get_jt.copy(),
    #                       self.url_nt)
