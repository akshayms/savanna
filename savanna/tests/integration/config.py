OS_USERNAME = 'admin' # username for nova
OS_PASSWORD = 'swordfish' # password for nova
OS_TENANT_NAME = 'admin'
OS_AUTH_URL = 'http://172.18.79.139:35357/v2.0/' # URL for keystone

SAVANNA_HOST = '172.18.79.209' # IP for Savanna API
SAVANNA_PORT = '8181' # port for Savanna API

IMAGE_ID = '51752c61-f73a-456c-98fb-192c0a448554' # ID for instance image
FLAVOR_ID = '2'

IP_PREFIX = '172.' # prefix for IP address which is used for ssh connect to worker nodes

NODE_USERNAME = 'username' # username for master node
NODE_PASSWORD = 'password' # password for master node

CLUSTER_NAME_CRUD = 'cluster-name-crud' # cluster name for crud operations
CLUSTER_NAME_HADOOP = 'cluster-name-hadoop' # cluster name for hadoop testing

TIMEOUT = 15 # cluster creation timeout (in minutes)

HADOOP_VERSION = '1.1.1'
HADOOP_DIRECTORY = '/usr/share/hadoop'
HADOOP_LOG_DIRECTORY = '/mnt/log/hadoop/hadoop/userlogs'

SSH_KEY = 'vrovachev'
PLUGIN_NAME = 'vanilla'