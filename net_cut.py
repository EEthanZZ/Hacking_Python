import netfilterqueue as net
import scapy.all as scapy


def process_packet(packet):
    scapy_packets = scapy.IP(packet.get_payload())
    if scapy_packets.haslayer(scapy.DNSRR):
        print(scapy_packets.show())
    # packet.accept()
    """
    packet.accept()  # the packet will be sent to the target
    packet.drop()  #drop the packet at here
    """
    # iptables -I FORWARD -j NFQUEUE --queue-num 0


queue = net.NetfilterQueue()
queue.bind(0, process_packet)
# connect the queue created in system and call back
# the function process_packet
queue.run()
