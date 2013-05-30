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

from savanna.context import ctx
import savanna.db.models as m
from savanna.tests.unit.db.models.base import ModelTestCase


class ClusterModelTest(ModelTestCase):
    def testCreateCluster(self):
        session = ctx().session
        with session.begin():
            c = m.Cluster('c-1', 't-1', 'p-1', 'hv-1', 's')
            session.add(c)

        with session.begin():
            res = session.query(m.Cluster).filter_by().first()

            self.assertIsValidModelObject(res)
