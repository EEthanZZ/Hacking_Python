import scapy.all as scapy


def sniff(interface):
    # prn -> callback function
    # store -> store in Memory
    # prn -> each packet is processed by the other function
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    print(packet)


sniff("eth0")