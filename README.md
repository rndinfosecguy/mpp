# My Pineapple Pager Payloads (MPP)

<p align="center">
    <img src="readme_assets/logo.png" width="350"/> 
</p>

The core of the repository is a dashboard which analyzes DNS traffic intercepted on `wlan0open` on the Wifi Pineapple Pager to fingerpint devices.

## Features

| Feature | Description |  
| --------- | ------------- |  
| start_dns_tcpdump | starts `tcpdump` to capture DNS requests on the pine AP interface |
| stop_dns_tcpdump | stops `tcpdump` to capture DNS requests on the pine AP interface |
| show_dns_traffic | shows captured dns traffic in a pcap file |
| show_gathered_credentials | shows credentials which were collected by Evil Portal |
| alert_evil_portal_credentials | alerts if Evil Portal captures new credentials |
| dashboard_start | starts the dashboard for data visualization |
| dashboard_stop | stops the dashboard for data visualization |

## Installation

The module `show_dns_traffic` needs `scapy` installed to work.

1. SSH onto your pager
2. Run the following commands

```bash
opkg update
opkg install -d mmc scapy
```

3. Copy the repository into `/mmc/root/payloads/user/`
4. The module `alert_evil_portal_credentials` needs to be copied to `/root/payloads/alerts/` in the category `new client connected`.

## Dashboard

Dashboard is a module which analyzes and visualizes data collected by `Evil Portal` (`credentials.json`) and the collected `dns` dumps from the moulde `start_dns_tcpdump`.

The idea is to have a simple overview over devices which are or were connected to `Evil Portal`/`open AP`. Also the module tries to identify what apps might be installed on the device based on `dns` queries the device made.

I recommend using the modified portals for `Evil Portal` I forked (https://github.com/rndinfosecguy/evilportals_pager) as there collected credentials are aggregated at one spot (`/mmc/root/logs/credentials.json`) and all hostnames of clients who visit the captive portal are stored regardless if the person enters credentials or not (`/mmc/root/logs/hostnames.csv`). Other versions of `Evil Portal` portals are not compatible with MPP and may lead to less data to be analyzed (no creds and hostnames).

### dashboard_start

This module performs multiple steps:

- go through every pcap file in `/root/loot/mpp/` and check for `dns` queries which indiciate a specific app might be installed on the connected mobile device
- go through the credentials entries of `Evil Portal` (`credentials.json`)
- go through collected hostnames (`hostnames.csv`)
- starting a web server which visualizes the collected data (`http://172.16.52.1:8000/cgi-bin/dashboard`)

The hardware of the Pineapple Pager does not have a good performance. Therefore the module remembers which `pcap` files it already processed when executing `dashboard_start`. This way the exeuction of the module is not additionally slowed down by processing known data again.

### dashboard_stop

Kills the python web server.

### UI Preview

<img src="readme_assets/dashboard_default.png" width="200"/> 

## License

My Pineapple Pager Payloads (MPP) is distributed under the GNU GENERAL PUBLIC LICENSE v3. See LICENSE for more information.

## Disclaimer

Usage of these code for attacking infrastructures without prior mutual consistency can be considered as an illegal activity. It is the final user's responsibility to obey all applicable local, state and federal laws. Authors assume no liability and are not responsible for any misuse or damage caused by this program.
