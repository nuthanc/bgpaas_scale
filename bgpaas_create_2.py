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
#vnc_lib = VncApi(username='admin', password='BC95C7C422B2', tenant_name='admin', api_server_host='10.87.64.129', api_server_port=8082, auth_host='10.87.64.129')
vnc_lib = VncApi(username='admin', password='c0ntrail123', tenant_name='admin', api_server_host='10.87.64.129', api_server_port=8082, auth_host='5.5.5.251')
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
proj_obj = vnc_lib.project_read(fq_name=tenant_name) 
hc_objs = proj_obj.get_service_health_checks() 
k = 0
#vmis = vnc_lib.virtual_machine_interfaces_list()['virtual-machine-interfaces']
#for vmi in vmis:
#for i in range(400,425):
for i in range(400,425):
    vmi_fq_name = ['default-domain','admin','test-bfd-2-hc-vmi.st%d'%i]
    vmi_obj  = vnc_lib.virtual_machine_interface_read(fq_name=vmi_fq_name)
    bgpaas_name = 'bgpaas-scale-2.st%d'%i
    bgpaas_obj = BgpAsAService(name=bgpaas_name, parent_obj=proj_obj)
    bgpaas_obj.add_virtual_machine_interface(vmi_obj)
    bgpaas_obj.set_autonomous_system(str(i+1999))
    bgp_addr_fams = AddressFamilies(['inet'])
    bgp_sess_attrs = BgpSessionAttributes(address_families=bgp_addr_fams,hold_time=300,passive=True,loop_count=2)
    bgpaas_obj.set_bgpaas_session_attributes(bgp_sess_attrs)
    vnc_lib.bgp_as_a_service_create(bgpaas_obj)
    i = i+1
    print i
