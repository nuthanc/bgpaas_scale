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

cidr = "60.0.0.0/24"

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


interfaces = proj_obj.get_virtual_machine_interfaces()
for intf in interfaces:
    for name in intf['to']:
        if 'vmi.st0' in name:
            continue
        if 'vmi' in name: 
            print intf
            #print name 
            print "network delete %s"%intf['uuid']
            for i in range(1,1000):
                vmi_name_d = 'test-bfd-2-hc-vmi.st%s'%i
                if name == vmi_name_d:
                    print name
                    vmi_obj=vnc_lib.virtual_machine_interface_read(id=intf['uuid'])
                    hc_ref=vmi_obj.get_service_health_check_refs()
                    if hc_ref is not None:
                        hc_obj=vnc_lib.service_health_check_read(id=hc_ref[0]['uuid'])
                        vmi_obj.del_service_health_check(hc_obj) 
                        vnc_lib.virtual_machine_interface_update(vmi_obj)
                    ip_ref = vmi_obj.get_instance_ip_back_refs()
                    vnc_lib.instance_ip_delete(id=ip_ref[0]['uuid']) 
                    vnc_lib.virtual_machine_interface_delete(id=intf['uuid'])


#hcs = proj_obj.get_service_health_checks()
#for hc  in hcs:
#    vnc_lib.service_health_check_delete(id=hc['uuid'])

#networks = proj_obj.get_virtual_networks()
#for net in networks:
#    for name in net['to']:
#        if 'VN.hc.st0' in name:
#            continue
#        if 'VN.hc.st' in name: 
#            print net
#            print "network delete %s"%net['uuid']
#            vnc_lib.virtual_network_delete(id=net['uuid'])


#vn_obj = VirtualNetwork(vn_name,parent_obj=proj_obj)


exit(0)

