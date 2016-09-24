#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
# 
# Copyright (c) 2016 Puru
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Nagios (NRPE) plugin for checking bandwidth speed limit.
'''

from argparse import ArgumentParser
from time import sleep
from sys import exit
from os.path import isdir
import re

__description__ = 'Nagios (NRPE) plugin for checking bandwidth speed limit.'
__author__ = "Puru Tuladhar <tuladharpuru@gmail.com>"
__github__ = "https://github.com/tuladhar/check_bandwidth"
__version__ = "%(prog)s v1.0 by {0} ({1})".format(__author__, __github__)

# See: /usr/lib64/nagios/plugins/utils.sh
STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3
STATE_DEPENDENT=4

PLUGIN_NAME="BANDWIDTH"
THRESHOLD_REGEX=re.compile('(\d+)([K|M|G])$')

def exit_ok(msg):
        print "{0} OK - {1}".format(PLUGIN_NAME, msg)
        exit(STATE_OK)

def exit_warning(msg):
        print "{0} WARNING - {1}".format(PLUGIN_NAME, msg)
        exit(STATE_WARNING)

def exit_critical(msg):
        print "{0} CRITICAL - {1}".format(PLUGIN_NAME, msg)
        exit(STATE_CRITICAL)

def exit_unknown(msg):
        print "{0} UNKNOWN - {1}".format(PLUGIN_NAME, msg)
        exit(STATE_UNKNOWN)

def get_network_bytes(interface):
        dev_path = '/sys/class/net/'+interface
        if not isdir(dev_path):
                msg = "no such interface: "+interface
                exit_unknown(msg)
        rx_bytes_path = dev_path+"/statistics/rx_bytes"
        tx_bytes_path = dev_path+"/statistics/tx_bytes"
        rx_bytes = open(rx_bytes_path, 'r').read()
        tx_bytes = open(tx_bytes_path, 'r').read()
        return int(rx_bytes), int(tx_bytes)

def convert_unit(value, unit):
        if unit == 'K':
                v = int(value) * 10**3
        if unit == 'M':
                v = int(value) * 10**6
        if unit == 'G':
                v = int(value) * 10**9
        return v

def main():
        ap = ArgumentParser(description=__description__)
        ap.add_argument('-v', '--version', action='version', version=__version__)
        ap.add_argument('-i', '--interface', metavar='name', dest='interface', help='interface to use (default: eth0)', default='eth0')
        ap.add_argument('-w', '--warning', metavar='threshold', dest='warning', help="threshold in bits. Appending 'K' will count the number as Kilobits, 'M' as Megabits, 'G' as Gigabits. Examples: 200K, 3M and 1G")
        ap.add_argument('-c', '--critical', metavar='threshold', dest='critical', help="threshold in bits. Appending 'K' will count the number as Kilobits, 'M' as Megabits and 'G' as Gigabits. Examples: 200K, 3M and 1G")
        args = ap.parse_args()

        interface = args.interface
        if not args.warning or not args.critical:
                ap.error('required options: --warning, --critical')

        # parse and convert to bits
        m1, m2 = THRESHOLD_REGEX.match(args.warning), THRESHOLD_REGEX.match(args.critical)
        if not m1 or not m2:
                ap.error("supported threshold units: K, M, G")
        warning_bits = convert_unit(*m1.groups())
        critical_bits = convert_unit(*m2.groups())

        warning_rx_bits = warning_tx_bits = warning_bits
        critical_rx_bits = critical_tx_bits = critical_bits

        # get network transfer bytes and convert to bits
        o_rx_bytes, o_tx_bytes = get_network_bytes(interface); sleep(1.0)
        n_rx_bytes, n_tx_bytes = get_network_bytes(interface)
        rx_bits, tx_bits = (n_rx_bytes - o_rx_bytes)*8, (n_tx_bytes - o_tx_bytes)*8

        # convert bandwidth bits back to unit
        down = up = None
        kbits, mbits, gbits = float(10**3), float(10**6), float(10**9)
        if rx_bits < kbits:
                down = "{0:.2f} bps".format(rx_bits)
        if rx_bits >= kbits:
                down = "{0:.2f} Kbps".format(rx_bits / kbits)
        if rx_bits >= mbits:
                down = "{0:.2f} Mbps".format(rx_bits / mbits)
        if rx_bits >= gbits:
                down = "{0:.2f} Gbps".format(rx_bits / gbits)
        if tx_bits < kbits:
                up = "{0:.2f} bps".format(tx_bits)
        if tx_bits >= kbits:
                up = "{0:.2f} Kbps".format(tx_bits / kbits)
        if tx_bits >= mbits:
                up = "{0:.2f} Mbps".format(tx_bits / mbits)
        if tx_bits >= gbits:
                up = "{0:.2f} Gbps".format(tx_bits / gbits)

        # check threshold and exit appropriately
        msg = "{0}: DOWN: {1}, UP: {2}".format(interface, down, up)
        if rx_bits > critical_rx_bits or tx_bits > critical_tx_bits:
                exit_critical(msg)
        elif rx_bits > warning_rx_bits or tx_bits > warning_tx_bits:
                exit_warning(msg)
        else:
                exit_ok(msg)

if __name__ == '__main__':
        main()
