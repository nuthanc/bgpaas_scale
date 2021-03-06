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
vnc_lib = VncApi(username='admin', password='BC95C7C422B2', tenant_name='admin', api_server_host='10.87.64.129', api_server_port=8082, auth_host='10.87.64.129')

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
#hc_obj = vnc_lib.service_health_check_read(id="d297ff01-0b8b-43b8-940b-18e50b417f5e")
vmis = vnc_lib.virtual_machine_interfaces_list()['virtual-machine-interfaces']
proj_obj = vnc_lib.project_read(fq_name=tenant_name)  
hc_objs = proj_obj.get_service_health_checks() 
for vmi in vmis:
    print vmi
    print vmi['fq_name']

    hc_obj = hc_objs[k]
    if 'test-bfd-2-hc-vmi' in vmi['fq_name'][2]:
       if 'test-bfd-2-hc-vmi.st0' not in vmi['fq_name']:
           if not (i % 450): 
               k = k+1
               hc_obj = hc_objs[k]
           vmi_obj = vnc_lib.virtual_machine_interface_read(fq_name=vmi['fq_name'])
           vmi_obj.add_service_health_check(hc_obj)
           vnc_lib.virtual_machine_interface_update(vmi_obj)
    i = i+1
