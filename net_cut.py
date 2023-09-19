import netfilterqueue as net


def process_packet(packet):
    print(packet)
    """
    packet.accept()  # the packet will be sent to the target
    packet.drop()  #drop the packet at here
    """

queue = net.NetfilterQueue()
queue.bind(0, process_packet)
# connect the queue created in system and call back
# the function process_packet
queue.run()
