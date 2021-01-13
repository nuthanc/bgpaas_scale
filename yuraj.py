from vnc_api import vnc_api
from vnc_api.vnc_api import ControlNodeZone
vnc = vnc_api.VncApi(
          api_server_host = "10.87.64.129",
           auth_host = '5.5.5.251',
           username = 'admin',
           password = 'c0ntrail123',
           tenant_name = 'admin')
import pdb;pdb.set_trace()
gsc_fq_name = ['default-global-system-config']
gsc_obj = vnc.global_system_config_read(fq_name=gsc_fq_name);
br_fq_name = ['default-domain', 'default-project', 'ip-fabric', '__default__', '5b4s2.novalocal']
bgp_router_obj = vnc.bgp_router_read(fq_name=br_fq_name)
gsc_obj.add_bgp_router(bgp_router_obj)
vnc.global_system_config_update(gsc_obj)
