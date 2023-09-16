#!/usr/bin/env python

import scapy.all as scapy


def scan(ip):
    arp_request = scapy.ARP(pdst = ip)
    # print(arp_request.summary())
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # print(broadcast.summary())
    arp_broadcast = broadcast/arp_request
    # arp_broadcast.show()
    ans_list = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
    # for i in ans_list:
    #    print(f"{i[1].hwsrc}\t{i[1].psrc}")
    client_list = []
    for i in ans_list:
        client_dict = {"ip": i[1].psrc, "mac": i[1].hwsrc}
        client_list.append(client_dict)
    return client_list


def print_result(result_list2):
    print("IP\t\t\tMAC\n---------------------------------------------")
    for i in result_list2:
        print(f"{i['ip']}\t\t{i['mac']}")


result_list = scan("192.168.58.2/24")
#print(result_list)
print_result(result_list)
