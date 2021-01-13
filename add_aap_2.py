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


hc_objs = []
k = 0
i = 0
vmis = vnc_lib.virtual_machine_interfaces_list()['virtual-machine-interfaces']
proj_obj = vnc_lib.project_read(fq_name=tenant_name)  
hc_objs = proj_obj.get_service_health_checks() 
for i in range(3,450):
#for vmi in vmis:
#    print vmi
#    print vmi['fq_name']
    prefix_len = '32'
    aap_mode='active-standby'
    vmi_fq_name = ['default-domain','admin','test-bfd-2-hc-vmi.st%d'%i]
    vmi = vnc_lib.virtual_machine_interface_read(fq_name=vmi_fq_name)
    ins_ip_uuid = vmi.get_instance_ip_back_refs()[0]['uuid']
    ipaddr = vnc_lib.instance_ip_read(id=ins_ip_uuid).get_instance_ip_address()
    prefix = str(IPNetwork(ipaddr+'/24')[100])
    ip = SubnetType(ip_prefix=prefix, ip_prefix_len=prefix_len)
    aap = AllowedAddressPair(ip=ip, mac='')
    aap.set_address_mode(aap_mode)
    aaps = AllowedAddressPairs(allowed_address_pair=[aap])
    vmi.set_virtual_machine_interface_allowed_address_pairs(aaps)
    vnc_lib.virtual_machine_interface_update(vmi)
