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
from savanna.service import api
import savanna.utils.api as u

LOG = logging.getLogger(__name__)

rest = u.Rest('v10', __name__)


## Cluster ops

@rest.get('/clusters')
def clusters_list(ctx):
    return u.render(clusters=[c.dict for c in api.get_clusters()])


@rest.post('/clusters')
def clusters_create(data):
    return u.render(api.create_cluster(data).wrapped_dict)


@rest.get('/clusters/<cluster_id>')
def clusters_get(cluster_id):
    return u.render(api.get_cluster(id=cluster_id))


@rest.put('/clusters/<cluster_id>')
def clusters_update(cluster_id):
    return u.internal_error(501, NotImplementedError(
        "Cluster update op isn't implemented (id '%s')"
        % cluster_id))


@rest.delete('/clusters/<cluster_id>')
def clusters_delete(cluster_id):
    api.terminate_cluster(id=cluster_id)
    return u.render()


## ClusterTemplate ops

@rest.get('/cluster-templates')
def cluster_templates_list():
    pass


@rest.post('/cluster-templates')
def cluster_templates_create(_data):
    pass


@rest.get('/cluster-templates/<cluster_template_id>')
def cluster_templates_get(_cluster_template_id):
    pass


@rest.put('/cluster-templates/<cluster_template_id>')
def cluster_templates_update(_cluster_template_id):
    pass


@rest.delete('/cluster-templates/<cluster_template_id>')
def cluster_templates_delete(_cluster_template_id):
    pass


## NodeGroupTemplate ops

@rest.get('/node-group-templates')
def node_group_templates_list():
    pass


@rest.post('/node-group-templates')
def node_group_templates_create(_data):
    pass


@rest.get('/node-group-templates/<node_group_template_id>')
def node_group_templates_get(_node_group_template_id):
    pass


@rest.put('/node-group-templates/<node_group_template_id>')
def node_group_templates_update(_node_group_template_id):
    pass


@rest.delete('/node-group-templates/<node_group_template_id>')
def node_group_templates_delete(_node_group_template_id):
    pass


## Plugins ops

@rest.get('/plugins')
def plugins_list():
    return u.render(plugins=[p.dict for p in api.get_plugins()])


@rest.get('/plugins/<plugin_name>')
def plugins_get(plugin_name):
    return u.render(api.get_plugin(plugin_name).wrapped_dict)


@rest.get('/plugins/<plugin_name>/<version>')
def plugins_get_version(plugin_name, version):
    return u.render(api.get_plugin(plugin_name, version).wrapped_dict)


## Image Registry ops

@rest.get('/images')
def images_list():
    pass


@rest.get('/image/<image_id>/description')
def image_descriptions_get(_image_id):
    pass


@rest.post('/image/<image_id>/description')
def image_descriptions_set(_image_id, _data):
    pass


@rest.get('/image/<image_id>/tags')
def image_tags_list(_image_id):
    pass


@rest.post('/image/<image_id>/tags')
def image_tags_add(_image_id):
    pass


@rest.delete('/image/<image_id>/tags')
def image_tags_delete(_image_id):
    pass
