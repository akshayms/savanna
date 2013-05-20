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
import savanna.plugins.base as plugin_base
from savanna.plugins.provisioning import ProvisioningPluginBase

LOG = logging.getLogger(__name__)


## Cluster ops
# todo check tenant_id

def get_clusters(**args):
    pass


def get_cluster(**args):
    pass


def create_cluster(values):
    pass


def terminate_cluster(**args):
    pass


## Plugins ops

def get_plugins():
    return plugin_base.PLUGINS.get_plugins(base=ProvisioningPluginBase)


def get_plugin(plugin_name, version=None):
    plugin = plugin_base.PLUGINS.get_plugin(plugin_name)
    res = plugin.as_resource()
    if version:
        res._info['configs'] = [c.dict for c in plugin.get_configs(version)]
        res._info['node_processes'] = plugin.get_node_processes(version)
    return res
