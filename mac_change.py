import subprocess
from optparse import *


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_arguments():
    parser = OptionParser()
    parser.add_option("-i", "--interface", help="Interface to change its MAC address", dest="interface")
    parser.add_option("-M", "--MAC", dest="new_mac", help="define the new MAC Address")
    (options, args) = parser.parse_args()
    if not options.interface:
        parser.error("please specify the interface")
    elif not options.new_mac:
        parser.error("Please specify the new MAC address")
    return options


options = get_arguments()
change_mac(options.interface, options.new_mac)
ifconfig_result = subprocess.check_call(["ifconfig", options.interface])
print(ifconfig_result)

"""
subprocess.call(f"ifconfig {interface} down", shell=True)
subprocess.call(f"ifconfig {interface} hw ether {new_mac} ", shell=True)
subprocess.call(f"ifconfig {interface} up", shell=True)
"""