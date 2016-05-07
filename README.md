# check_bandwidth.py
Nagios (NRPE) plugin for checking bandwidth speed limit.

```bash
# /usr/local64/nagios/plugins/check_bandwidth.py -i eth0 -w 1M -c 10M
BANDWIDTH CRITICAL - eth0: DOWN: 38.57 Mbps, UP: 850.02 Kbps

# /usr/local64/nagios/plugins/check_bandwidth.py -i eth0 -w 25M -c 50M
BANDWIDTH OK - eth0: DOWN: 11.85 Mbps, UP: 456.23 Kbps

# /usr/local64/nagios/plugins/check_bandwidth.py -i eth0 -w 25M -c 50M
BANDWIDTH WARNING - eth0: DOWN: 38.50 Mbps, UP: 519.87 Kbps
```
