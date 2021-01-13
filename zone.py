from vnc_api.vnc_api import VncApi                                                                                                                              
from vnc_api.vnc_api import ControlNodeZone                                                                                                                     
from vnc_api.gen.resource_client import *                                                                                                                       
from vnc_api.gen.resource_xsd import *                                                                                                                          
import time                                                                                                                                                     
                                                                                                                                                                
vnc = VncApi(                                                                                                                                                   
        api_server_host = "10.87.64.129",                                                                                                                       
        auth_host = '5.5.5.251',                                                                                                                            
        username = 'admin',                                                                                                                                     
        password = 'c0ntrail123',                                                                                                                               
        tenant_name = 'admin')                                                                                                                                  
fq_name = 'default-global-system-config'                                                                                                                        
gsc_obj = vnc.global_system_config_read(id='b411d9a8-3f89-457c-864f-882ad37dc726');                                                                             
#gsc_name = "default-global-system-config"                                                                                                                      
                                                                                                                                                                
bgp_routers = ['5b4s2.novalocal','5b4s6','5b4s4']                                                                                                                         
                                                                                                                                                                
def create_zones():
    for i in range(0,2):
        cnz_name = "test-cnz-%s"%i
        cnz = ControlNodeZone(name=cnz_name, parent_obj=gsc_obj)
        vnc.control_node_zone_create(cnz);
        print("zone %s created"%cnz_name)

def delete_zones():
    for i in range(0,2):
        cnz_name = [ "default-global-system-config", "test-cnz-%s"%i]
        vnc.control_node_zone_read(fq_name = cnz_name)
        vnc.control_node_zone_delete(fq_name = cnz_name)
        print("zone %s deleted"%cnz_name)

def add_bgp_router():
    for i in range(0,2):
        fq_name = ["default-domain", "default-project", "ip-fabric", "__default__", bgp_routers[i]]
        bgp_router_obj = vnc.bgp_router_read(fq_name=fq_name)
        cnz_name = [ "default-global-system-config", "test-cnz-%s"%i]
        cnz_obj = vnc.control_node_zone_read(fq_name = cnz_name)
        bgp_router_obj.set_control_node_zone(cnz_obj)
        vnc.bgp_router_update(bgp_router_obj)

def del_bgp_router():
    for i in range(0,2):
        fq_name = ["default-domain", "default-project", "ip-fabric", "__default__", bgp_routers[i]]
        bgp_router_obj = vnc.bgp_router_read(fq_name=fq_name)
        cnz_name = [ "default-global-system-config", "test-cnz-%s"%i]
        cnz_obj = vnc.control_node_zone_read(fq_name = cnz_name)
        bgp_router_obj.del_control_node_zone(cnz_obj)
        vnc.bgp_router_update(bgp_router_obj)

def add_bgpaas_zone():
    bgpaas_name = ["default-domain","admin",'bgpaas-scale-1.st%d'%0]
    bgpaas_obj = vnc.bgp_as_a_service_read(fq_name=bgpaas_name)
    cnz_name = [ "default-global-system-config", "test-cnz-%s"%0]
    cnz_obj = vnc.control_node_zone_read(fq_name=cnz_name)
    attr = BGPaaSControlNodeZoneAttributes("primary")
    bgpaas_obj.add_control_node_zone(cnz_obj, attr)
    vnc.bgp_as_a_service_update(bgpaas_obj)
    cnz_name = [ "default-global-system-config", "test-cnz-%s"%1]
    cnz_obj = vnc.control_node_zone_read(fq_name=cnz_name)
    attr = BGPaaSControlNodeZoneAttributes("secondary")
    bgpaas_obj.add_control_node_zone(cnz_obj, attr)
    vnc.bgp_as_a_service_update(bgpaas_obj)

def del_bgpaas_zone():
    bgpaas_name = ["default-domain","admin",'bgpaas-scale-1.st%d'%0]
    bgpaas_obj = vnc.bgp_as_a_service_read(fq_name=bgpaas_name)
    cnz_name = [ "default-global-system-config", "test-cnz-%s"%0]
    cnz_obj = vnc.control_node_zone_read(fq_name=cnz_name)
    bgpaas_obj.del_control_node_zone(cnz_obj)
    vnc.bgp_as_a_service_update(bgpaas_obj)
    cnz_name = [ "default-global-system-config", "test-cnz-%s"%1]
    cnz_obj = vnc.control_node_zone_read(fq_name=cnz_name)
    bgpaas_obj.del_control_node_zone(cnz_obj)
    vnc.bgp_as_a_service_update(bgpaas_obj)


def add_bgpaas_zone_scale(num):
    for i in range(2,425):
        bgpaas_name = ["default-domain","admin",'bgpaas-scale-%s.st%d'%(num,i)]
        bgpaas_obj = vnc.bgp_as_a_service_read(fq_name=bgpaas_name)
        cnz_name = [ "default-global-system-config", "test-cnz-%s"%0]
        cnz_obj = vnc.control_node_zone_read(fq_name=cnz_name)
        attr = BGPaaSControlNodeZoneAttributes("primary")
        bgpaas_obj.add_control_node_zone(cnz_obj, attr)
        vnc.bgp_as_a_service_update(bgpaas_obj)
        cnz_name = [ "default-global-system-config", "test-cnz-%s"%1]
        cnz_obj = vnc.control_node_zone_read(fq_name=cnz_name)
        attr = BGPaaSControlNodeZoneAttributes("secondary")
        bgpaas_obj.add_control_node_zone(cnz_obj, attr)
        vnc.bgp_as_a_service_update(bgpaas_obj)

def del_bgpaas_zone_scale(num):
    for i in range(2,425):
        bgpaas_name = ["default-domain","admin",'bgpaas-scale-%s.st%d'%(num,i)]
        bgpaas_obj = vnc.bgp_as_a_service_read(fq_name=bgpaas_name)
        cnz_name = [ "default-global-system-config", "test-cnz-%s"%0]
        cnz_obj = vnc.control_node_zone_read(fq_name=cnz_name)
        bgpaas_obj.del_control_node_zone(cnz_obj)
        vnc.bgp_as_a_service_update(bgpaas_obj)
        cnz_name = [ "default-global-system-config", "test-cnz-%s"%1]
        cnz_obj = vnc.control_node_zone_read(fq_name=cnz_name)
        bgpaas_obj.del_control_node_zone(cnz_obj)
        vnc.bgp_as_a_service_update(bgpaas_obj)



#create_zones()
#add_bgp_router()
#add_bgpaas_zone_scale('1')
#add_bgpaas_zone_scale('2')
del_bgpaas_zone_scale('1')
del_bgpaas_zone_scale('2')
del_bgp_router()
delete_zones()

#for i in range(0,1000):
#    create_zones()
#    add_bgp_router()
#    add_bgpaas_zone()
#    time.sleep(300000)
#    del_bgpaas_zone()
#    del_bgp_router()
#    delete_zones()
#    time.sleep(10)

