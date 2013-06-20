OS_USERNAME = 'admin'  # username for nova
OS_PASSWORD = 'swordfish'  # password for nova
OS_TENANT_NAME = 'admin'
OS_AUTH_URL = 'http://172.18.79.139:35357/v2.0/'  # URL for keystone

SAVANNA_HOST = '172.18.79.209'  # IP for Savanna API
SAVANNA_PORT = '8080'  # port for Savanna API

IMAGE_ID = '39d3d9ff-bbd7-49be-955d-8b3f01a68409'  # ID for instance image
FLAVOR_ID = '42'

IP_PREFIX = '172.'  # prefix for IP address which is used for ssh connect
                                                        # to worker nodes

NODE_USERNAME = 'username'  # username for master node
NODE_PASSWORD = 'password'  # password for master node

CLUSTER_NAME_CRUD = 'YL-cluster_crud'  # cluster name for crud operations
CLUSTER_NAME_HADOOP = 'YL-cluster_hadoop'  # cluster name for hadoop testing

TIMEOUT = 15  # cluster creation timeout (in minutes)

HADOOP_VERSION = '1.1.2'
HADOOP_DIRECTORY = '/usr/share/hadoop'
HADOOP_LOG_DIRECTORY = '/mnt/log/hadoop/hadoop/userlogs'

SSH_KEY = 'vrovachev'
PLUGIN_NAME = 'vanilla'
PATH_TO_SSH = '/home/user/.ssh/id_rsa'
PASS_FROM_SSH = '20091100'
