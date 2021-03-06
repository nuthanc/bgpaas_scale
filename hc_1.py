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


hc_objs = []
k = 0
i = 0
vmis = vnc_lib.virtual_machine_interfaces_list()['virtual-machine-interfaces']
proj_obj = vnc_lib.project_read(fq_name=tenant_name)  
hc_objs = proj_obj.get_service_health_checks() 
#for i in range(2,425):
for i in range(420,425):
#for vmi in vmis:
#    print vmi
#    print vmi['fq_name']
    vmi_fq_name = ['default-domain','admin','test-bfd-hc-vmi.st%d'%i]
    vmi_obj = vnc_lib.virtual_machine_interface_read(fq_name=vmi_fq_name)
    bfd_name = 'bfd-hc-%d'%i
    prop = ServiceHealthCheckType()
    prop.set_health_check_type('link-local')
    prop.set_monitor_type('BFD')
    prop.set_delay(delay=0) 
    prop.set_delayUsecs(delayUsecs=25000)
    prop.set_timeout(timeout=0)
    prop.set_max_retries(max_retries=5)
    prop.set_timeoutUsecs(timeoutUsecs=3000)
    hc_obj = ServiceHealthCheck(name=bfd_name,parent_obj=proj_obj,service_health_check_properties=prop)
    uuid = vnc_lib.service_health_check_create(hc_obj)
    vmi_obj.add_service_health_check(hc_obj)
    vnc_lib.virtual_machine_interface_update(vmi_obj)
