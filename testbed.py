from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@5.5.5.129'
host2 = 'root@5.5.5.130'
host3 = 'root@5.5.5.131'

#External routers if any
#for eg.
#ext_routers = [('mx1', '10.204.216.253')]
ext_routers = []

#Autonomous system number
router_asn = 64512

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3],
    'contrail-controller': [host1],
    'openstack': [host1],
    'contrail-compute': [host2, host3],
    'contrail-analytics': [host1],
    'contrail-analyticsdb': [host1],
}

#Hostnames
env.hostnames = {
    # for multi node setup, add comma separated values of hostnames (within quotes)
    'all': ['5b4s2', '5b4s4', '5b4s6']
}

# Passwords of each host
# for passwordless login's no need to set env.passwords,
# instead populate env.key_filename in testbed.py with public key.
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
}
# The default WebUI password is the same as keystone admin password
# You can modify it as follows:
# env.keystone = {
#     'admin_password': '<Password value>'
# }

# SSH Public key file path for passwordless logins
# if env.passwords is not specified.
#env.key_filename = '/root/.ssh/id_rsa.pub'

#For reimage purpose
env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
}

env.kernel_upgrade=False
env.openstack = {
    'manage_amqp': "true"
}

