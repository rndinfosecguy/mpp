# mpp

My Pineapple Pager Payloads

## Features

| Feature | Description |  
| --------- | ------------- |  
| start_dns_tcpdump | starts `tcpdump` to capture DNS requests on the pine AP interface |
| stop_dns_tcpdump | stops `tcpdump` to capture DNS requests on the pine AP interface |
| show_dns_traffic | shows captured dns traffic in a pcap file |
| show_gathered_credentials | shows credentials which were collected by Evil Portal |

## Installation

The module `show_dns_traffic` needs `scapy` installed to work.

1. SSH onto your pager
2. Run the following commands

```bash
opkg update
opkg install -d mmc scapy
```

3. Copy the repository into `/mmc/root/payloads/user/`
