#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os, sys, time
from fbat import *
from rrdtool import update as rrd_update

os.chdir(batPath)

# Defs 
#adcU=0; adcI=2
Umin=11
maxh=10 # 10 heures
maxsec=maxh*3600

print "immat:",immat
print "batNum:",batNum
print "batCap:",batCap
print "testSt:",testSt
print "testFin:",testFin
print "testBrk:",testBrk
print "relUdem:",relUdem
print "rel1st:",rel1st
print "rel2st:",rel2st
print "rel3st:",rel3st
print "rel4st:",rel4st
print "tsDeb:",tsDeb
print "tsFin:",tsFin

# Si timeStamp du test tourne, (== test en cours ) verif si dur max atteinte
if tsDeb !="0":
	print "Debut du test:", time.strftime("%d/%m/%Y  %H:%M", time.localtime(int(tsDeb)))
	# print "Test commencé depuis:", time.strftime("%j jours et %H:%M", time.localtime(int(time.time())-int(tsdeb)))
	durdeb=int(time.time())-int(tsDeb)
	print durdeb," secondes"

	# forçage de la fin test sur durée max atteinte
	if testSt=="1" and durdeb > maxsec:
		testFin="1"
		print "Durée Max atteinte! arret du test!"
	else:
		nhdeb=durdeb // 3600
		nmdeb=durdeb % 3600 / 60
		print "Test commencé depuis:",nhdeb,"heures",nmdeb,"minutes"

# Si le timeStamp de fin est ecrit, affichage de la duree du test
if tsFin !="0":
	print "Fin   du test:", time.strftime("%d/%m/%Y  %H:%M", time.localtime(int(tsFin)))
	durtest=int(tsFin)-int(tsDeb)
	nhtest=durtest // 3600
	nmtest=durtest % 3600 / 60
	print "Duree du test:",nhtest,"heures",nmtest,"minutes"

# commutation batterie si demande 
if relUdem == "1" and rel1st=="0":
	rel1st=commutRel(R1,1)
if relUdem == "0" and rel1st=="1":
	rel1st=commutRel(R1,0)

# lecture des données
strTime=time.strftime('%H:%M:%S', time.localtime())
print 0, readAdc(0)
print 1, readAdc(1)
print 2, readAdc(2)
print 3, readAdc(3)
print 4, readAdc(4)
print 5, readAdc(5)
print 6, readAdc(6)
print 7, readAdc(7)
