import sys
import ipaddr
from netaddr import IPNetwork

cidr = "60.0.0.0/24"
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

for i in range(2,1001):
    ipv4_cidr = cidr_obj.get_next_cidr()
    ipv4_network,ipv4_prefix = ipv4_cidr.split("/")
    print ipv4_cidr,ipv4_network
