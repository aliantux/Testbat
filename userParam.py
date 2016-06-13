#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Définitions propres à chaque utilisateur emplacement de la base rrd
batPath ="/home/pi/adc/"

# ces numeros de pins GPIO doivent etre modifies pour correspondre aux broches utilisees.
# Pseudo SPI pour mizar:
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
#

# Def des pins GPIO des relais
R1 = 28
R2 = 29
R3 = 30
R4 = 31

# cannaux ADC
adcU = 6
adcI = 7
