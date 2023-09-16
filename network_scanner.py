#!/usr/bin/env python

import scapy.all as scapy


def scan(ip):
    arp_request = scapy.ARP(pdst = ip)
    # print(arp_request.summary())
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # print(broadcast.summary())
    arp_broadcast = broadcast/arp_request
    # arp_broadcast.show()
    ans_list= scapy.srp(arp_broadcast, timeout=1)[0]
    for i in ans_list:
        print(f"client MAC = {i[1].hwsrc}")
        print(f"client IP = {i[1].psrc}")
        print("------------\n------------")


scan("192.168.58.2/24")
