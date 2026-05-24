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

## License

Evil Portals is distributed under the GNU GENERAL PUBLIC LICENSE v3. See LICENSE for more information.

## Disclaimer

Usage of these code for attacking infrastructures without prior mutual consistency can be considered as an illegal activity. It is the final user's responsibility to obey all applicable local, state and federal laws. Authors assume no liability and are not responsible for any misuse or damage caused by this program.
