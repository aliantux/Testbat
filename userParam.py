#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Définitions propres à chaque utilisateur
batPath ="/home/pi/bat/"

# ces numeros de pins GPIO doivent etre modifies pour correspondre aux broches utilisees.

# Pseudo SPI pour mizar:
SPICLK = 9
SPIMISO = 8
SPIMOSI = 10
SPICS = 11

# Pseudo SPI pour regulus:
# SPICLK = 23; SPIMISO = 22; SPIMOSI = 17; SPICS = 7 

# Def des pins des relais
R1 = 28
R2 = 29
R3 = 30
R4 = 31

# cannaux ADC
adcU = 0
adcI = 2
