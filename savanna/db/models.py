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

import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from savanna.db import model_base as mb
from savanna.utils.openstack.nova import novaclient
from savanna.utils.sqlatypes import JsonDictType
from savanna.utils.sqlatypes import JsonListType


class Cluster(mb.SavannaBase, mb.IdMixin, mb.TenantMixin,
              mb.PluginSpecificMixin, mb.ExtraMixin):
    """Contains all info about cluster."""

    _resource_name = 'cluster'
    __table_args__ = (
        sa.UniqueConstraint('name', 'tenant_id'),
    )

    name = sa.Column(sa.String(80), nullable=False)
    default_image_id = sa.Column(sa.String(36))
    cluster_configs = sa.Column(JsonDictType())
    node_groups = relationship('NodeGroup', cascade="all,delete",
                               backref='cluster')
    status = sa.Column(sa.String(80))
    status_description = sa.Column(sa.String(200))
    # todo instances' credentials should be stored in cluster
    base_cluster_template_id = sa.Column(sa.String(36),
                                         sa.ForeignKey('ClusterTemplate.id'))
    base_cluster_template = relationship('ClusterTemplate',
                                         backref="clusters")

    def __init__(self, name, tenant_id, plugin_name, hadoop_version, status,
                 status_description=None, default_image_id=None,
                 cluster_configs=None, node_groups=None, extra=None):
        self.name = name
        self.tenant_id = tenant_id
        self.plugin_name = plugin_name
        self.hadoop_version = hadoop_version
        # todo we need statuses enum
        self.status = status
        self.status_description = status_description
        self.default_image_id = default_image_id
        self.cluster_configs = cluster_configs or {}
        self.node_groups = node_groups or []
        self.extra = extra or {}


class NodeGroup(mb.SavannaBase, mb.IdMixin, mb.ExtraMixin):
    """Specifies group of nodes within a cluster."""

    _resource_name = 'node_group'
    __table_args__ = (
        sa.UniqueConstraint('name', 'cluster_id'),
    )

    cluster_id = sa.Column(sa.String(36), sa.ForeignKey('Cluster.id'))
    name = sa.Column(sa.String(80), nullable=False)
    flavor_id = sa.Column(sa.String(36), nullable=False)
    image_id = sa.Column(sa.String(36), nullable=False)
    node_processes = sa.Column(JsonListType())
    node_configs = sa.Column(JsonDictType())
    anti_affinity_group = sa.Column(sa.String(36), nullable=False)
    count = sa.Column(sa.Integer, nullable=False)
    instances = relationship('Instance', cascade="all,delete",
                             backref='node_group')
    base_node_group_template_id = sa.Column(sa.String(36),
                                            sa.ForeignKey(
                                                'NodeGroupTemplate.id'))
    base_node_group_template = relationship('NodeGroupTemplate',
                                            backref="node_groups")

    def __init__(self, name, flavor_id, image_id, node_processes, count,
                 node_configs=None, anti_affinity_group=None, extra=None):
        self.name = name
        self.flavor_id = flavor_id
        self.image_id = image_id
        self.node_processes = node_processes
        self.count = count
        self.node_configs = node_configs or {}
        self.anti_affinity_group = anti_affinity_group or {}
        self.extra = extra or {}


class Instance(mb.SavannaBase, mb.ExtraMixin):
    """An OpenStack instance created for the cluster."""

    _resource_name = 'instance'
    __table_args__ = (
        sa.UniqueConstraint('instance_id', 'node_group_id'),
    )

    node_group_id = sa.Column(sa.String(36), sa.ForeignKey('NodeGroup.id'))
    instance_id = sa.Column(sa.String(36), primary_key=True)
    management_ip = sa.Column(sa.String(15), nullable=False)

    def info(self, ctx):
        """Returns info from nova about instance."""
        return novaclient(ctx.headers).servers.get(self.instance_id)

    def __init__(self, node_group_id, instance_id, management_ip, extra=None):
        self.node_group_id = node_group_id
        self.instance_id = instance_id
        self.management_ip = management_ip
        self.extra = extra or {}


class NodeGroupTemplate(mb.SavannaBase, mb.IdMixin, mb.TenantMixin,
                        mb.PluginSpecificMixin):
    """Template for NodeGroup."""

    _resource_name = 'node_group_template'
    __table_args__ = (
        sa.UniqueConstraint('name', 'tenant_id'),
    )

    name = sa.Column(sa.String(80), nullable=False)
    description = sa.Column(sa.String(200))
    flavor_id = sa.Column(sa.String(36), nullable=False)
    node_processes = sa.Column(JsonListType())
    node_configs = sa.Column(JsonDictType())

    def __init__(self, name, tenant_id, flavor_id, plugin_name,
                 hadoop_version, node_processes, node_configs=None,
                 description=None):
        self.name = name
        self.tenant_id = tenant_id
        self.flavor_id = flavor_id
        self.plugin_name = plugin_name
        self.hadoop_version = hadoop_version
        self.node_processes = node_processes
        self.node_configs = node_configs or {}
        self.description = description


class ClusterTemplate(mb.SavannaBase, mb.IdMixin, mb.TenantMixin,
                      mb.PluginSpecificMixin):
    """Template for Cluster."""

    _resource_name = 'cluster_template'
    __table_args__ = (
        sa.UniqueConstraint('name', 'tenant_id'),
    )

    name = sa.Column(sa.String(80), nullable=False)
    description = sa.Column(sa.String(200))
    cluster_configs = sa.Column(JsonDictType())

    # todo add node_groups_suggestion helper

    def __init__(self, name, tenant_id, plugin_name, hadoop_version,
                 cluster_configs=None, description=None):
        self.name = name
        self.tenant_id = tenant_id
        self.plugin_name = plugin_name
        self.hadoop_version = hadoop_version
        self.cluster_configs = cluster_configs or {}
        self.description = description

    def add_node_group_template(self, node_group_template, name, count):
        relation = TemplatesRelation(self.id, node_group_template.id, name,
                                     count)
        self.templates_relations.append(relation)
        node_group_template.templates_relations.append(relation)
        return relation

    def remove_node_group_template(self, node_group_template):
        # todo impl
        pass


class TemplatesRelation(mb.SavannaBase):
    """NodeGroupTemplate - ClusterTemplate relationship."""

    _resource_name = 'templates_relation'

    cluster_template_id = sa.Column(sa.String(36),
                                    sa.ForeignKey('ClusterTemplate.id'),
                                    primary_key=True)
    node_group_template_id = sa.Column(sa.String(36),
                                       sa.ForeignKey('NodeGroupTemplate.id'),
                                       primary_key=True)
    cluster_template = relationship(ClusterTemplate,
                                    backref='templates_relations')
    node_group_template = relationship(NodeGroupTemplate,
                                       backref='templates_relations')
    name = sa.Column(sa.String(80), nullable=False)
    count = sa.Column(sa.Integer, nullable=False)

    def __init__(self, cluster_template_id, node_group_template_id, name,
                 count):
        self.cluster_template_id = cluster_template_id
        self.node_group_template_id = node_group_template_id
        self.name = name
        self.count = count


ClusterTemplate.node_group_templates = association_proxy("templates_relations",
                                                         "node_group_template")
NodeGroupTemplate.cluster_templates = association_proxy("templates_relations",
                                                        "cluster_template")
