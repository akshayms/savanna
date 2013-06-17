OS_USERNAME = 'qa-user'  # username for nova
OS_PASSWORD = 'swordfish'  # password for nova
OS_TENANT_NAME = 'qa'
OS_AUTH_URL = 'http://172.18.79.139:35357/v2.0/'  # URL for keystone

SAVANNA_HOST = '172.18.79.226'  # IP for Savanna API
SAVANNA_PORT = '8080'  # port for Savanna API

IMAGE_ID = 'ff27275f-27b0-443b-b5dc-6ae5f6264bd7'  # ID for instance image
FLAVOR_ID = '42'

IP_PREFIX = '172.'  # prefix for IP address which is used for ssh connect
                                                        # to worker nodes

NODE_USERNAME = 'username'  # username for master node
NODE_PASSWORD = 'password'  # password for master node

CLUSTER_NAME_CRUD = 'cluster_crud'  # cluster name for crud operations
CLUSTER_NAME_HADOOP = 'cluster_hadoop'  # cluster name for hadoop testing

TIMEOUT = 15  # cluster creation timeout (in minutes)

HADOOP_VERSION = '1.1.2'
HADOOP_DIRECTORY = '/usr/share/hadoop'
HADOOP_LOG_DIRECTORY = '/mnt/log/hadoop/hadoop/userlogs'

SSH_KEY = 'ylobankov'
PLUGIN_NAME = 'vanilla'