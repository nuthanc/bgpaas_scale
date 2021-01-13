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

vnc_lib = VncApi(username='admin', password='x8DusH7B3agbdQ2CuyNhQXMgN', tenant_name='admin', api_server_host='10.0.0.40', api_server_port=8082, auth_host='192.168.24.14')

vlan_tag = 2 
proj_obj = vnc_lib.project_read(fq_name=tenant_name)
ipam_obj = vnc_lib.network_ipam_read(fq_name=ipam_fq_name)

sec_grp_obj = vnc_lib.security_group_read(fq_name = [u'default-domain', u'admin', u'default'])

for i in xrange(0,450):
#for i in xrange(0,3):
    vn_name = "VN.hc.st" + str(i)
#    import pdb;pdb.set_trace()
#    networks = proj_obj.get_virtual_networks()
    vn_obj = VirtualNetwork(vn_name,parent_obj=proj_obj)
    ipv4_cidr = cidr_obj.get_next_cidr()

    ipv4_network,ipv4_prefix = ipv4_cidr.split("/")
    ipam_sn_lst = []
    ipam_sn = IpamSubnetType(subnet=SubnetType(ipv4_network, int(ipv4_prefix)),addr_from_start=True)
    ipam_sn.set_subnet_name(vn_name+"_ipv4_subnet")
    ipam_sn_lst.append(ipam_sn)

    vn_obj.add_network_ipam(ipam_obj,VnSubnetsType(ipam_sn_lst))

    vnc_lib.virtual_network_create(vn_obj)

    instance_ip_name = 'bfd-iip.st%d'%i
    bgpaas_name = 'bgpaas-scale-3.st%d'%i
    bfd_name = 'bfd-hc-%d'%i
    vmi_fq_name = ['default-domain','admin','test-bfd-hc-vmi.st%d'%i]

    vmi_obj = VirtualMachineInterface(fq_name=vmi_fq_name, parent_type='project')

    if i != 0 :
       vmi_prop = VirtualMachineInterfacePropertiesType()
       vmi_prop.set_sub_interface_vlan_tag(vlan_tag)
       vlan_tag += 1
       vmi_obj.set_virtual_machine_interface_properties(vmi_prop)
       vmi_obj.add_virtual_machine_interface(vmi_obj_m)
       vmi_obj.add_security_group(sec_grp_obj)
       vmi_obj.set_virtual_machine_interface_mac_addresses(vmi_obj_m.virtual_machine_interface_mac_addresses)
#       import pdb;pdb.set_trace()
    vmi_obj.add_virtual_network(vn_obj)
    if i == 0:
       mac_address_obj = MacAddressesType()
       mac_address_obj.set_mac_address([])
       mac_address_obj.set_mac_address([generate_random_mac()])
       vmi_obj.set_virtual_machine_interface_mac_addresses(mac_address_obj)
    vnc_lib.virtual_machine_interface_create(vmi_obj)
    ip_obj = InstanceIp(name=instance_ip_name)
    ip_obj.set_virtual_machine_interface(vmi_obj)
    ip_obj.set_virtual_network(vn_obj)
    iip_id = vnc_lib.instance_ip_create(ip_obj)
    if i != 0:
        prop = ServiceHealthCheckType()
        prop.set_health_check_type('link-local')
        prop.set_monitor_type('BFD')
        prop.set_delay(delay=0) 
        prop.set_delayUsecs(delayUsecs=10000)
        prop.set_timeout(timeout=0)
        prop.set_max_retries(max_retries=5)
        prop.set_timeoutUsecs(timeoutUsecs=10000)
        hc_obj = ServiceHealthCheck(name=bfd_name,parent_obj=proj_obj,service_health_check_properties=prop)
        uuid = vnc_lib.service_health_check_create(hc_obj)
        hc_obj = vnc_lib.service_health_check_read(id=uuid) 
        vmi_obj.add_service_health_check(hc_obj)
        vnc_lib.virtual_machine_interface_update(vmi_obj)

    if i == 0:
       vmi_obj_m = vmi_obj
