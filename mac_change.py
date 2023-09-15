import subprocess
from optparse import *
import re


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


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_add_search_result = re.search(r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", str(ifconfig_result))
    if mac_add_search_result:
        return mac_add_search_result.group(0)
    else:
        print("failed to read")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print(f"The current MAC add is {str(current_mac)}")
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(f"Successfully changed to {current_mac}")
else:
    print("not changed")
"""
subprocess.call(f"ifconfig {interface} down", shell=True)
subprocess.call(f"ifconfig {interface} hw ether {new_mac} ", shell=True)
subprocess.call(f"ifconfig {interface} up", shell=True)
"""