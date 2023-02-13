#!/bin/env python3

import netifaces
from scapy.all import *

"""
The first two functions (cidrtion, cidr4) is used to translate an ip address into its CIDR form.

The main function logic goes like this:
1. Find all active interfaces on your local device (if netifaces.AF_INET in addr: )
2. For each active interface, print the name, IP address in CIDR form, MAC address (if they have one) and network mask (Section 2)
3. For each active interface that is not a vbox/loopback interface, search the network for online devices using the ARP request method.
 (Section 3)
* For the number of unresponding hosts, I basically calculated the total number of possible IP addresses based on the subnet mask value 
and then deducted the number of hosts that responded.

"""



def cidrtion(mask):
    sum1 = 0
    multi = 1
    bits = 0

    for part in reversed(mask.split(".")):
        sum1 += int(part) * multi
        multi *= 2 ** 8

    while sum1:
        sum1 &= sum1 - 1
        bits += 1

    return bits
    

def cidr(addr, mask):
    return "{addr}/{bits}".format(addr=addr, bits=cidrtion(mask))

#print(netifaces.interfaces())
#print(netifaces.ifaddresses('en0')[netifaces.AF_LINK])

def main():
    print("Active Interfaces")
    for iface in netifaces.interfaces():
        addr = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addr: # Section 2
            details = addr[netifaces.AF_INET][0]
            ip = details["addr"]
            mask = details["netmask"]
            

            print(iface + ": active")
            print(cidr(details["addr"], details["netmask"]))
            print("Network Mask is: " + details["netmask"])
            if netifaces.AF_LINK in addr:
                print("{addr}:{value}".format(addr="Mac Address is", value=netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]["addr"]))
                print("")
            else:
                print("")

            # Section 3

            if iface == 'lo0' or iface.startswith('vbox'):
                continue
            else:
                arp = ARP(pdst=cidr(details["addr"], details["netmask"]))
                ether = Ether(dst="ff:ff:ff:ff:ff:ff")
                
                total_in_network = 0

                if cidrtion(details["netmask"]) == 1:
                    total_in_network = 1
                else:
                    total_in_network = 2 ** (32-int(cidrtion(details["netmask"]))) 

                result = srp(ether/arp, timeout=3, verbose=0)[0]
                #result.show()
                print("Number of hosts that responded: " + str(len(result)))
                print("Number of hosts that did not respond: " + str(total_in_network-len(result)))
                

                hearback = []

                for sent, received in result:
                    hearback.append({'ip': received.psrc, 'mac': received.hwsrc})

                
                print("I found some online devices for interface {value}:".format(value=iface))
                
                for i in hearback:
                    
                    print("IP: "+i['ip'] + " " * 10 + "MAC: "+ i['mac'])

main()

    


    