#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os, sys
from userParam import *
import RPi.GPIO as GPIO

# defs
OUTPUT = 0
INPUT = 1

print batPath

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# definition de l'interface SPI
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# definition des cdes relais 
GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)

# fonction de commutation des relais
def commutRel(R,st):
	print R,st
	if st==1:
		GPIO.output(R,True)
	else:
		GPIO.output(R,False)
	if GPIO.input(R)==True:
		return "1"
	else:
		return "0"		

#fonction lisant les donnees SPI de la puce MCP3008, parmi 8 entrees, de 0 a 7
def readAdc(adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(SPICS, True)
        GPIO.output(SPICLK, False)  # start clock low
        GPIO.output(SPICS, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(SPIMOSI, True)
                else:
                        GPIO.output(SPIMOSI, False)
                commandout <<= 1
                GPIO.output(SPICLK, True)
                GPIO.output(SPICLK, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(SPICLK, True)
                GPIO.output(SPICLK, False)
                adcout <<= 1
                if (GPIO.input(SPIMISO)):
                        adcout |= 0x1

        GPIO.output(SPICS, True)

        adcout /= 2       # first bit is 'null' so drop it
        return adcout

# ============================================================================
# Fonction qui enleve le caractère LF (\n) de la chaine passée en paramètre 
# et qui retourne la valeur du paramètre placé entre '=' et ';'
# exemple dans "immat=SPARE;    # immatriculation du planeur" retourne "SPARE"
# ==============================================================================
def fparam(strN):
    strP=strN.rstrip('\n')
    return strP[strP.find("=")+1:strP.find(";")]

# recup des paramètres
fh=open(batPath+"testbat.param","r")
#print fh.readlines();fh.seek(0)
immat=fparam(fh.readline())
batNum=fparam(fh.readline())
batCap=fparam(fh.readline())
testSt=fparam(fh.readline())
testFin=fparam(fh.readline())
testBrk=fparam(fh.readline())
relUdem=fparam(fh.readline())
rel1st=fparam(fh.readline())
rel2st=fparam(fh.readline())
rel3st=fparam(fh.readline())
rel4st=fparam(fh.readline())
tsDeb=fparam(fh.readline())
tsFin=fparam(fh.readline())
#print "immat:",immat,", batNum:",batNum,", batCap:",batCap,", testst:",testst,", testfin:",testfin,", testbrk:",testbrk,", relUdem:",relUdem,", rel1st:",rel1st,", rel2st:,",rel2st,", rel3st:",rel3st,", rel4st:",rel4st,", tsdeb:",tsdeb,", tsfin:",tsfin
fh.close

# ================================================================
# fonction de stockage des paramètre sous la forme "immat=F-CGUQ;"
# ================================================================
def fstoparam(immat,batNum,batCap,testSt,testFin,testBrk,relUdem,rel1st,rel2st,rel3st,rel4st,tsDeb,tsFin):
	fh=open(batPath+"testbat.param","w")
	fh.write('immat='+immat+';\n')
	fh.write('batNum='+batNum+';\n')
	fh.write('batCap='+batCap+';\n')
	fh.write('testSt='+testSt+';\n')
	fh.write('testFin='+testFin+';\n')
	fh.write('testBrk='+testBrk+';\n')
	fh.write('relUdem='+relUdem+';\n')
	fh.write('rel1st='+rel1st+';\n')
	fh.write('rel2st='+rel2st+';\n')
	fh.write('rel3st='+rel3st+';\n')
	fh.write('rel4st='+rel4st+';\n')
	fh.write('tsDeb='+tsDeb+';\n')
	fh.write('tsFin='+tsFin+';\n')
	fh.close
