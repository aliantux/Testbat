#!/bin/sh
#
/usr/bin/python /home/jdb/testbat/testbat.py > tbatsh.log
/bin/sh /home/jdb/testbat/graph.sh >> tbatsh.log
sleep 1

