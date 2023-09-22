#!/usr/bin/env python

import scapy.all as scapy
import netfilterqueue
import re


def set_load(packet,payload):
    packet[scapy.Raw].load = payload
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(pkt):
    scapy_packet = scapy.IP(pkt.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] HTTP Request")
            modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "", scapy_packet[scapy.Raw].load)
            new_packet = set_load(scapy_packet, modified_load)
            pkt.setfieldval(bytes(new_packet))
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] HTTP Response")
            print(scapy_packet.show())

    pkt.accept()


def packet_show(pkt):
    print("[+] Printing Packets")
    scapy_pkt = scapy.IP(pkt.get_payload())
    print(scapy_pkt.show())


try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("\n \n [+] Detected ctrl+c ... Quitting ...!!!")