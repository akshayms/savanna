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

OS_USERNAME = 'qa-user'  # username for nova
OS_PASSWORD = 'swordfish'  # password for nova
OS_TENANT_NAME = 'qa'
OS_AUTH_URL = 'http://172.18.168.5:35357/v2.0/'  # URL for keystone

SAVANNA_HOST = '172.18.168.169'  # IP for Savanna API
SAVANNA_PORT = '8386'  # port for Savanna API

#IMAGE_ID = '39d3d9ff-bbd7-49be-955d-8b3f01a68409'  # ID for instance image
IMAGE_ID = '4f0af83a-d7cd-4ae7-b6f1-0c26ab274673'
FLAVOR_ID = '42'

NODE_USERNAME = 'ubuntu'  # username for master node

CLUSTER_NAME_CRUD = 'VR-cluster-crud'  # cluster name for crud operations
CLUSTER_NAME_HADOOP = 'VR-cluster-hadoop'  # cluster name for hadoop testing

TIMEOUT = 15  # cluster creation timeout (in minutes)

HADOOP_VERSION = '1.1.2'
HADOOP_DIRECTORY = '/usr/share/hadoop'
HADOOP_LOG_DIRECTORY = '/mnt/log/hadoop/hadoop/userlogs'

SSH_KEY = 'vrovachev'
PLUGIN_NAME = 'vanilla'
PATH_TO_SSH = '/home/vadim/.ssh/id_rsa_new'

NAMENODE_CONFIG = {'Name Node Heap Size': 1234}
JOBTRACKER_CONFIG = {'Job Tracker Heap Size': 1345}
DATANODE_CONFIG = {'Data Node Heap Size': 1456}
TASKTRACKER_CONFIG = {'Task Tracker Heap Size': 1567}
GENERAL_CONFIG = {'Enable Swift': True}
CLUSTER_HDFS_CONFIG = {'dfs.replication': 2}
CLUSTER_MAPREDUCE_CONFIG = {'mapred.map.tasks.speculative.execution': False,
                            'mapred.child.java.opts': '-Xmx100m'}
