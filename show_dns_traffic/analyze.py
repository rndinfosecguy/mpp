#!/usr/bin/env python3

from scapy.all import rdpcap, IP, DNS, DNSQR
import sys

def print_a_record_requests(pcap_file):
    packets = rdpcap(pcap_file)

    print("client ip, DNS request")
    for pkt in packets:
        # Check for IP + DNS query
        if pkt.haslayer(IP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
            dns = pkt[DNS]

            # qr == 0 means DNS request (not response)
            if dns.qr == 0:
                query = pkt[DNSQR]

                # qtype 1 = A record
                if query.qtype == 1:
                    src_ip = pkt[IP].src
                    domain = query.qname.decode(errors="ignore").rstrip(".")

                    ip = src_ip.strip()
                    print(f"{ip}, {domain}")


print_a_record_requests(sys.argv[1])
