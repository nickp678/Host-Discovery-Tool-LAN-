# Host-Discovery-Tool-LAN-


## Introduction

This is a host discovery tool made with Python. When run, it firsts lists all the active interfaces on the machine. Then for each active interface, except for the loopback interface, the script uses ARP requests to find any online machines within its subnet. Netifaces and Scapy are used so they are required to be installed first before you run the script.

## Prerequisites

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install both Netifaces and Scapy.

```bash
pip install netifaces
```
```bash
pip install scapy
```

Download the hostdiscover.py file from github

## Usage

To run the Input Aggregator, use the following command:

```bash
python3 inputaggregator.py
```

Have fun!
