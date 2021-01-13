from vnc_api.vnc_api import *
import socket
import struct
import random
from netaddr import *

alloc_addr_list = list()

parent_vmi_1_uuid = '18f383be-d8fb-454d-aed8-28f60213ab13'
parent_vmi_2_uuid = '36922cc4-737c-4154-bfda-f80e6d82ba64'

client = VncApi(username='admin', password='BC95C7C422B2', tenant_name='admin')

for vlan in range(2, 452):
    p_vmi_1 = client.virtual_machine_interface_read(id=parent_vmi_1_uuid)
    p_vmi_2 = client.virtual_machine_interface_read(id=parent_vmi_2_uuid)
    for p_vmi in [p_vmi_1, p_vmi_2]:
        vmi_fq_name = ['default-domain', 'admin', p_vmi.name+'-%s'%vlan]
        vmi_obj = client.virtual_machine_interface_read(fq_name=vmi_fq_name)
        #import pdb ; pdb.set_trace()
        vmi_obj.set_virtual_machine_interface_disable_policy(False)
        client.virtual_machine_interface_update(vmi_obj)

