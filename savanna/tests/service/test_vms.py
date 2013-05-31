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


import unittest

import mock
from savanna.db.models import Cluster
from savanna.db.models import NodeGroup
from savanna.service.vm import ClusterProvisionOperation
from savanna.utils.key_utils import generate_private_key
from savanna.utils.key_utils import get_public_key_openssh


class TestServiceLayer(unittest.TestCase):
    def scheduling_one_node_groups_and_one_affinity_group(self):
        nova_client = mock.Mock()

        p = ClusterProvisionOperation(nova_client)
        groups = [NodeGroup("test_group",
                            "test_flavor",
                            "test_image",
                            ["data node", "test tracker"],
                            2,
                            anti_affinity_group="1")]
        cluster = Cluster("test_cluster",
                          "tenant_id",
                          "mock_plugin",
                          "mock_version",
                          "initial",
                          node_groups=groups)
        cluster.user = "root"
        cluster.key = generate_private_key()

        cluster.node_groups = groups

        user_key = mock.Mock()
        user_key.public_key = "123"
        nova_client.keypairs.find.side_effect = [user_key]

        instance1 = mock.Mock()
        instance1.id = "123"
        instance2 = mock.Mock()
        instance2.id = "124"
        nova_client.servers.create.side_effect = [instance1, instance2]

        p._creates_vms(cluster, "test")
        key = get_public_key_openssh(cluster.key)

        files = {"/root/.ssh/authorized_keys": "123\n" + key,
                 '/root/.ssh/id_rsa': cluster.key}

        nova_client.servers.create.assert_has_calls(
            [mock.call("test_cluster-test_group-1",
                       "test_image",
                       "test_flavor",
                       scheduler_hints={'different_host': []},
                       files=files),
             mock.call("test_cluster-test_group-2",
                       "test_image",
                       "test_flavor",
                       scheduler_hints={'different_host': ["123"]},
                       files=files)],
            any_order=False)

        self.assertEqual(len(cluster.node_groups[0].instances), 2)

    def scheduling_one_node_groups_and_no_affinity_group(self):
        nova_client = mock.Mock()

        p = ClusterProvisionOperation(nova_client)
        groups = [NodeGroup("test_group",
                            "test_flavor",
                            "test_image",
                            ["data node", "test tracker"],
                            2)]
        cluster = Cluster("test_cluster",
                          "tenant_id",
                          "mock_plugin",
                          "mock_version",
                          "initial",
                          node_groups=groups)
        cluster.user = "root"
        cluster.key = generate_private_key()

        cluster.node_groups = groups

        user_key = mock.Mock()
        user_key.public_key = "123"
        nova_client.keypairs.find.side_effect = [user_key]

        instance1 = mock.Mock()
        instance1.id = "123"
        instance2 = mock.Mock()
        instance2.id = "124"
        nova_client.servers.create.side_effect = [instance1, instance2]

        p._creates_vms(cluster, "test")
        key = get_public_key_openssh(cluster.key)

        files = {"/root/.ssh/authorized_keys": "123\n" + key,
                 '/root/.ssh/id_rsa': cluster.key}

        nova_client.servers.create.assert_has_calls(
            [mock.call("test_cluster-test_group-1",
                       "test_image",
                       "test_flavor",
                       files=files),
             mock.call("test_cluster-test_group-2",
                       "test_image",
                       "test_flavor",
                       files=files)],
            any_order=False)

        self.assertEqual(len(cluster.node_groups[0].instances), 2)

    def scheduling_two_node_groups_and_one_affinity_group(self):
        nova_client = mock.Mock()

        p = ClusterProvisionOperation(nova_client)
        groups = [NodeGroup("test_group_1",
                            "test_flavor",
                            "test_image",
                            ["data node",
                             "test tracker"],
                            2,
                            anti_affinity_group="1"),
                  NodeGroup("test_group_2",
                            "test_flavor",
                            "test_image",
                            ["data node", "test tracker"],
                            1,
                            anti_affinity_group="1")]
        cluster = Cluster("test_cluster",
                          "tenant_id",
                          "mock_plugin",
                          "mock_version",
                          "initial",
                          node_groups=groups)
        cluster.user = "root"
        cluster.key = generate_private_key()

        cluster.node_groups = groups

        user_key = mock.Mock()
        user_key.public_key = "123"
        nova_client.keypairs.find.side_effect = [user_key]

        instance1 = mock.Mock()
        instance1.id = "123"
        instance2 = mock.Mock()
        instance2.id = "124"
        instance3 = mock.Mock()
        instance3.id = "125"
        nova_client.servers.create.side_effect = [instance1,
                                                  instance2,
                                                  instance3]

        p._creates_vms(cluster, "test")

        key = get_public_key_openssh(cluster.key)
        files = {"/root/.ssh/authorized_keys": "123\n" + key,
                 '/root/.ssh/id_rsa': cluster.key}
        nova_client.servers.create.assert_has_calls(
            [mock.call("test_cluster-test_group_1-1",
                       "test_image",
                       "test_flavor",
                       scheduler_hints={'different_host': []},
                       files=files),
             mock.call("test_cluster-test_group_1-2",
                       "test_image",
                       "test_flavor",
                       scheduler_hints={'different_host': ["123"]},
                       files=files),
             mock.call("test_cluster-test_group_2-1",
                       "test_image",
                       "test_flavor",
                       scheduler_hints={'different_host': ["123", "124"]},
                       files=files)],
            any_order=False)

        self.assertEqual(len(cluster.node_groups[0].instances), 2)
        self.assertEqual(len(cluster.node_groups[1].instances), 1)
