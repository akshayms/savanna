__author__ = 'akuznetsov'

import eventlet
import paramiko
from savanna.db.models import Instance
from savanna.openstack.common import log as logging
from savanna.utils.key_utils import generate_private_key
from savanna.utils.key_utils import get_public_key_openssh
from savanna.utils.key_utils import get_user_public_key
from savanna.utils.key_utils import read_private_key


LOG = logging.getLogger(__name__)


class SchedulingError(Exception):
    def __init__(self, message):
        self.message = message


class ClusterProvisionOperation:
    def __init__(self, nova_client):
        self.nova_client = nova_client
        self.running_instances = []

    """
    @param cluster: cluster object based on vm will provisioned
    @type cluster: L{Cluster}
    @param user_key: name of user public key
    """
    def prepare_cluster(self, cluster, user_key):
        try:
            self._create_credentials(cluster)
            self._creates_vms(cluster, user_key)
            self._await_start_up(cluster)
            self._configure_etc_hosts(cluster)
        except SchedulingError:
            LOG.debug("can't start cluster %s because can't "
                      "scheduling vm on different hosts", cluster.name)
            self._shut_down(cluster)
        except Exception as ex:
            LOG.debug("can't start cluster %s reason %s", cluster.name, ex)
            self._shut_down(cluster)
        return ""

    def _create_credentials(self, cluster):
        cluster.key = generate_private_key()
        cluster.user = "root"

    def _create_keys(self, cluster, user_key):
        user_key = get_user_public_key(self.nova_client, user_key)

        if cluster.user == "root":
            path_to_root = "/root"
        else:
            path_to_root = "home/" + cluster.user

        authorized_keys = user_key.public_key + "\n"
        authorized_keys += get_public_key_openssh(cluster.key)

        return {
            path_to_root + "/.ssh/authorized_keys": authorized_keys,
            path_to_root + "/.ssh/id_rsa": cluster.key
        }

    def _creates_vms(self, cluster, user_key):
        aa_groups = dict([
            (node_group.anti_affinity_group,
             [instance.id for instance in node_group.instances])
            for node_group in cluster.node_groups
            if node_group.instances is list])

        files = self._create_keys(cluster, user_key)

        for node_group in cluster.node_groups:
            for i in range(1, node_group.count + 1):
                name = cluster.name + "-" + node_group.name + "-" + str(i)
                LOG.info("Starting vm: %s", name)

                aa_group = node_group.anti_affinity_group
                if aa_group is None:
                    vm = self.nova_client.servers.create(name,
                                                         node_group.image_id,
                                                         node_group.flavor_id,
                                                         files=files)
                else:
                    aa_group = aa_groups.get(aa_group, [])
                    hints = {"different_host": aa_group[:]}

                    vm = self.nova_client.servers.create(name,
                                                         node_group.image_id,
                                                         node_group.flavor_id,
                                                         scheduler_hints=hints,
                                                         files=files)
                    aa_group.append(vm.id)
                    aa_groups[aa_group] = aa_group

                instance = Instance(node_group.id, vm.id, None)
                #todo save node into database
                instance.name = name
                node_group.instances.append(instance)

    def _await_start_up(self, cluster):
        all_set = False
        key = read_private_key(cluster.key)

        while not all_set:
            print all_set
            all_set = True
            for node_group in cluster.node_groups:
                for instance in node_group.instances:
                    if not self._check_if_up(instance, cluster.user, key):
                        all_set = False
            print all_set
            eventlet.sleep(1)

    def _check_if_up(self, instance, user, key):
        if instance in self.running_instances:
            return True

        server = self.nova_client.servers.get(instance.instance_id)
        LOG.info("node %s status %s", server.name, server.status)
        if server.status == "ERROR":
            raise SchedulingError("node %s has error status" % server.name)

        print server.networks
        if len(server.networks) == 0:
            return False

        if instance.management_ip is None:
            ip = server.networks.values()[0][1]
            if not ip:
                return False

            instance.management_ip = ip
            #todo set correct model
            instance.internal_id = server.networks.values()[0][0]
            LOG.debug("assign to node %s management ip %s internal ip %s",
                      server.name,
                      ip,
                      instance.internal_id)

        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                instance.management_ip,
                username=user,
                pkey=key
            )
            chan = ssh.get_transport().open_session()
            chan.exec_command("chmod 400 .ssh/id_rsa")
        except Exception as ex:
            LOG.debug("can't login to node %s reason %s", server.name, ex)
            return False
        finally:
            ssh.close()

        print "running " + instance.name
        self.running_instances.append(instance)

        return True

    def _shut_down(self, cluster):
        for node_group in cluster.node_groups:
            for instance in node_group.instances:
                self.nova_client.servers.delete(instance.instance_id)

    def _configure_etc_hosts(self, cluster):
        hosts = "127.0.0.1 localhost\n"
        for node_group in cluster.node_groups:
            for instance in node_group.instances:
                #todo change the ip address
                hosts += "%s %s\n" % (instance.management_ip, instance.name)

        key = read_private_key(cluster.key)

        for node_group in cluster.node_groups:
            for instance in node_group.instances:
                ssh = paramiko.SSHClient()
                try:
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(
                        instance.management_ip,
                        username=cluster.user,
                        pkey=key
                    )
                    sftp = ssh.open_sftp()

                    fl = sftp.file('/etc/hosts', 'w')
                    fl.write(hosts)
                    fl.close()
                finally:
                    ssh.close()
