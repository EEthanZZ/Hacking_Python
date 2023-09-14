import subprocess

interface = input("Interface> ")
new_mac = input("New MAC add> ")

print(f"[+] Changing MAC for {interface} to {new_mac}")


"""
subprocess.call(f"ifconfig {interface} down", shell=True)
subprocess.call(f"ifconfig {interface} hw ether {new_mac} ", shell=True)
subprocess.call(f"ifconfig {interface} up", shell=True)
"""

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
subprocess.call(["ifconfig", interface, "up"])
