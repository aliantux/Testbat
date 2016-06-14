#!/bin/sh
#
# sleep 20
/usr/bin/python /home/pi/adc/testbat.py > tbatsh.log
/bin/sh /home/pi/adc/graph.sh >> tbatsh.log

