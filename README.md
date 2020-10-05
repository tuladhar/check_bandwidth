# check_bandwidth.py

## Installation

Clone the repository : 

```
git clone https://github.com/tuladhar/check_bandwidth.git 
cd check_bandwidth
```

Use the following command to install check_bandwidth.py

```
make install
make install INSTALL_PATH=/usr/lib/nagios/plugins # or specify a path where you want to install the plugin
```

To remove the plugin use the following command : 

```
make uninstall
make uninstall INSTALL_PATH=/usr/lib/nagios/plugins # or specify the path where the plugin is located 
```

## Usage

Nagios (NRPE) plugin for checking bandwidth speed limit.

```usage
usage: check_bandwidth.py [-h] [-v] [-i name] [-w threshold] [-c threshold]

Nagios (NRPE) plugin for checking bandwidth speed limit.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i name, --interface name
                        interface to use (default: eth0)
  -w threshold, --warning threshold
                        threshold in bits. Appending 'K' will count the number
                        as Kilobits, 'M' as Megabits, 'G' as Gigabits.
                        Examples: 200K, 3M and 1G
  -c threshold, --critical threshold
                        threshold in bits. Appending 'K' will count the number
                        as Kilobits, 'M' as Megabits and 'G' as Gigabits.
                        Examples: 200K, 3M and 1G
```

```shell
$ nagios/plugins/check_bandwidth.py -i venet0 -w 25M -c 50M
BANDWIDTH OK - venet0: DOWN: 11.85 Mbps, UP: 456.23 Kbps

$ nagios/plugins/check_bandwidth.py -i venet0 -w 25M -c 50M
BANDWIDTH WARNING - venet0: DOWN: 38.50 Mbps, UP: 519.87 Kbps

$ nagios/plugins/check_bandwidth.py -i venet0 -w 1M -c 10M
BANDWIDTH CRITICAL - venet0: DOWN: 38.57 Mbps, UP: 850.02 Kbps
```

## Authors
- [Puru Tuladhar](https://github.com/tuladhar)
