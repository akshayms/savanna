from savanna.openstack.common import log as logging
from savanna.tests.integration.db import ValidationTestCase

LOG = logging.getLogger(__name__)

class LoadTest(ValidationTestCase):

    def test_01_telnet(self):
        self._tn()
