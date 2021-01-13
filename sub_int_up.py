import sys
import ipaddr
from netaddr import IPNetwork
from vnc_api.vnc_api import VncApi
from vnc_api.gen.resource_client import *
from vnc_api.gen.resource_xsd import *
import random

#tenant_name  = ['default-domain','bgpaas-scale-3']
#ipam_fq_name = [ 'default-domain', 'bgpaas-scale-3', 'bgpaas-3.ipam']

tenant_name  = ['default-domain','admin']
ipam_fq_name = [ 'default-domain', 'default-project', 'default-network-ipam']

cidr = "80.0.0.0/24"

def generate_random_mac():
#    return "02:c0:69:3d:5d:f4"
    mac = [ 0x00, 0x16, 0x3e,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

class CIDR:

   def __init__(self,cidr):
       self.index = 0
       self.cidr = cidr
       self.ip_network = IPNetwork(self.cidr)
       self.ip_addr = ipaddr.IPAddress(IPNetwork(self.cidr)[0])
       self.cidr_net,self.cidr_mask = cidr.split("/")

   def get_next_cidr(self):
       ip_network_next = self.ip_network.next()[0]
       ip_addr_next = ipaddr.IPAddress(ip_network_next)
       cidr = ip_addr_next._explode_shorthand_ip_string()
       cidr = cidr + "/" + self.cidr_mask
       self.ip_network = IPNetwork(cidr)
       return cidr

cidr_obj = CIDR(cidr)

vnc_lib = VncApi(username='admin', password='BC95C7C422B2', tenant_name='admin', api_server_host='10.87.64.129', api_server_port=8082, auth_host='10.87.64.129')

vlan_tag = 2 
proj_obj = vnc_lib.project_read(fq_name=tenant_name)
ipam_obj = vnc_lib.network_ipam_read(fq_name=ipam_fq_name)

sec_grp_obj = vnc_lib.security_group_read(fq_name = [u'default-domain', u'admin', u'default'])

hcs = proj_obj.get_service_health_checks()
for hc  in hcs:
    #import pdb;pdb.set_trace()
    hc_obj=vnc_lib.service_health_check_read(id=hc['uuid']) 
    prop = hc_obj.get_service_health_check_properties()
    prop.set_delay(delay=0) 
    prop.set_delayUsecs(delayUsecs=25000)
    prop.set_timeout(timeout=0)
    prop.set_max_retries(max_retries=5)
    prop.set_timeoutUsecs(timeoutUsecs=25000)
    hc_obj.set_service_health_check_properties(prop)
    vnc_lib.service_health_check_update(hc_obj)


#vn_obj = VirtualNetwork(vn_name,parent_obj=proj_obj)


exit(0)

