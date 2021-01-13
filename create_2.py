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
vnc_lib = VncApi(username='admin', password='x8DusH7B3agbdQ2CuyNhQXMgN', tenant_name='admin', api_server_host='10.0.0.40', api_server_port=8082, auth_host='192.168.24.14')
#hcs = proj_obj.get_service_health_checks()
#for hc  in hcs:
    #import pdb;pdb.set_trace()
#    hc_obj=vnc_lib.service_health_check_read(id=hc['uuid']) 
#    prop = hc_obj.get_service_health_check_properties()
#    prop.set_delay(delay=1) 
#    prop.set_delayUsecs(delayUsecs=10000)
##    prop.set_timeout(timeout=2)
#    prop.set_max_retries(max_retries=5)
#    prop.set_timeoutUsecs(timeoutUsecs=10000)
#    hc_obj.set_service_health_check_properties(prop)
#    vnc_lib.service_health_check_update(hc_obj)


sec_grp_obj = vnc_lib.security_group_read(fq_name = [u'default-domain', u'admin', u'default'])

vmi_fq_name  = [ 'default-domain', 'admin', '3c16b4a7-3613-41b0-828e-9b2e10e41003'] 

vmi_obj_m = vnc_lib.virtual_machine_interface_read(fq_name=vmi_fq_name)  

vlan_tag = 2
for i in range(1,450):
    instance_ip_name = 'bfd-iip-2.st%d'%i
    vn_name = "VN.hc.st"+str(i)
    vn_fq_name  = [ 'default-domain', 'admin', vn_name ] 
    vn_obj = vnc_lib.virtual_network_read(fq_name = vn_fq_name )
    vmi_fq_name = ['default-domain','admin','test-bfd-2-hc-vmi.st%d'%i]
    vmi_obj = VirtualMachineInterface(fq_name=vmi_fq_name, parent_type='project')                                                                                                                   
    if i != 0 :                                                                                                                                                                                     
       vmi_prop = VirtualMachineInterfacePropertiesType()                                                                                                                                           
       vmi_prop.set_sub_interface_vlan_tag(vlan_tag)                                                                                                                                                
       vlan_tag += 1                                                                                                                                                                                
       vmi_obj.set_virtual_machine_interface_properties(vmi_prop)                                                                                                                                   
       vmi_obj.add_virtual_machine_interface(vmi_obj_m)                                                                                                                                             
       vmi_obj.add_security_group(sec_grp_obj)                                                                                                                                                      
       vmi_obj.set_virtual_machine_interface_mac_addresses(vmi_obj_m.virtual_machine_interface_mac_addresses)                                                                                       
#   import pdb;pdb.set_trace()                                                                                                                                                                  
    vmi_obj.add_virtual_network(vn_obj) 
    vnc_lib.virtual_machine_interface_create(vmi_obj)
    ip_obj = InstanceIp(name=instance_ip_name)
    ip_obj.set_virtual_machine_interface(vmi_obj)
    ip_obj.set_virtual_network(vn_obj)
    iip_id = vnc_lib.instance_ip_create(ip_obj)
