#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# defs
OUTPUT = 0
INPUT = 1

#init gpio externe
mcp = Adafruit_MCP230XX(busnum = 1, address = 0x20, num_gpios = 8 )

# Set pins 0, 6 and 7 to output 
mcp.config(0, mcp.OUTPUT)   # Pin0
mcp.output(0, 1)            # Hight led bleue on
mcp.config(6, mcp.OUTPUT)   # Pin6
mcp.output(6, 0)            # Low led jaune off
mcp.config(7, mcp.OUTPUT)   # Pin7
mcp.output(7, 0)            # Low led rouge off, board bleue on

# Set pin 1,2,3,4,5 to input with the pullup resistor enabled
mcp.config(1, mcp.INPUT)    # poussoir
mcp.pullup(1, 1)
mcp.config(2, mcp.INPUT)    # push codeur
mcp.pullup(2, 1)
mcp.config(3, mcp.INPUT)    # codeur P1
mcp.pullup(3, 1)
mcp.config(4, mcp.INPUT)    # codeur P2
mcp.pullup(4, 1)
mcp.config(5, mcp.INPUT)    # Inter
mcp.pullup(5, 1)

# ===================== fonctions ================
# fonction de commutation des leds
def commutLed(L,st):
	mcp.output(L,st )
