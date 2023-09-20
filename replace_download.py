import netfilterqueue as net
import scapy.all as scapy


file_formats = [".exe", ".jpeg", ".pdf"]

def process_packet(packet):
    scapy_packets = scapy.IP(packet.get_payload())
    if scapy_packets.haslayer(scapy.RAW): # all http packets
        if scapy_packets[scapy.TCP].dport == 80:
            print("HTTP Request:")
            for format in file_formats:
                if format in scapy_packets[scapy.RAW].load:
                    print("[+] Download Request:")
                    print(packet.show())
        elif scapy_packets[scapy.TCP].sport == 80:
            print("HTTP Response:")
            print(packet.show())

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
