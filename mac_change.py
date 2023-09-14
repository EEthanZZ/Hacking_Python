import subprocess
from optparse import *

parser = OptionParser()


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_arguments():
    parser.add_option("-i", "--interface", help="Interface to change its MAC address", dest="INTERFACE")
    parser.add_option("-M", "--MAC", dest="new_mac", help="define the new MAC Address")
    return parser.parse_args()


(options, args) = parser.parse_args()
change_mac(options.interface, options.new_mac)



"""
subprocess.call(f"ifconfig {interface} down", shell=True)
subprocess.call(f"ifconfig {interface} hw ether {new_mac} ", shell=True)
subprocess.call(f"ifconfig {interface} up", shell=True)
"""


