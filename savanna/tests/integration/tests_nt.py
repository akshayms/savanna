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

from savanna.openstack.common import log as logging
import savanna.tests.integration.config as config
from savanna.tests.integration.db import ValidationTestCase
import savanna.tests.integration.utils as utils

LOG = logging.getLogger(__name__)


class TestValidationApiForNodetemplates(ValidationTestCase):
    def setUp(self):
        super(TestValidationApiForNodetemplates, self).setUp()
        utils.telnet(config.SAVANNA_HOST, config.SAVANNA_PORT)

    def test_crud_nt_jtnn(self):
        self._crud_object(self.jtnn, self.get_jtnn.copy(),
                          self.url_nt)

    def test_crud_nt_ttdn(self):
        self._crud_object(self.ttdn, self.get_ttdn.copy(),
                          self.url_nt)

    def test_crud_nt_nn(self):
        self._crud_object(self.nn, self.get_nn.copy(),
                          self.url_nt)

    def test_crud_nt_jt(self):
        self._crud_object(self.jt, self.get_jt.copy(),
                          self.url_nt)
