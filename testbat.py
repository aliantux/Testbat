#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os, sys, time
from fbat import *
from rrdtool import update as rrd_update

os.chdir(batPath)

# Def des canaux ADC 
# ============> a inverser <==================
# inversion 0 et 1 car resistances sur adc2
adcU=1; adcI=0
Umin=11
maxh=1 #10 heures
maxsec=maxh*3600
# pour test to be remove!
#maxsec=70

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

if tsDeb !="0":
	print "Debut du test:", time.strftime("%d/%m/%Y  %H:%M", time.localtime(int(tsDeb)))
	# print "Test commencé depuis:", time.strftime("%j jours et %H:%M", time.localtime(int(time.time())-int(tsdeb)))
	durdeb=int(time.time())-int(tsDeb)
	print durdeb," secondes"
	if testSt=="1" and durdeb > maxsec:
		# forçage de la fin test sur durée max atteinte
		testFin="1"
		print "Durée Max atteinte! arret du test!"
	else:
		nhdeb=durdeb // 3600
		nmdeb=durdeb % 3600 / 60
		print "Test commencé depuis:",nhdeb,"heures",nmdeb,"minutes"
if tsFin !="0":
	print "Fin   du test:", time.strftime("%d/%m/%Y  %H:%M", time.localtime(int(tsFin)))
	durtest=int(tsFin)-int(tsDeb)
	nhtest=durtest // 3600
	nmtest=durtest % 3600 / 60
	print "Duree du test:",nhtest,"heures",nmtest,"minutes"

# commutation batterie si demande 
if relUdem == "1":
	commutRel(R1,1)
	rel1st = "1"
else:
	commutRel(R1,0)
	rel1st = "0"

# commutLed(6,1)

# lecture des données
strTime=time.strftime('%H:%M:%S', time.localtime())
Ubat = readAdc(adcU) * ( 3.3 / 1024.0) * 5
Ibat = readAdc(adcI) * ( 3.3 / 1024.0)

# ##############pour test break to be remove! ##############
if (tsDeb !="0" and nmdeb>3):
	Ubat=10.9
############################################################
print "\tHeure mesure:"+strTime
print "\ttension : %0.2f V" % Ubat
print "\tIntensité : %0.2f A" % Ibat
print "\tPuissance : %0.2f W" % (Ubat * Ibat)

# stockage en rrd
ret = rrd_update('/home/jdb/bat/acu.rrd', 'N:%s:%s' %(Ubat,Ibat));

# test conditions brk
if Ubat >= 15 or (Ubat > 1 and Ubat < Umin):
	testBrk="1"
	relUdem="0"
	commutRel(R1,0)
	rel1st = "0"	
	commutRel(R2,0)
	rel2st = "0"	
	commutRel(R3,0)
	rel3st = "0"	
	tsFin=str(int(time.time()))
	testSt="0"

# test fin test ********** a completer par test durée max *************
if testSt =="1" and testFin == "1":
	print "Fin du test"
	tsFin=str(int(time.time()))
	testSt="0"
	#commutRel(R2,0)
	#rel2st = "0"
	#commutRel(R3,0)
	#rel3st = "0"

# test début de test
if testSt =="1" and tsDeb == "0":
	print "Debut du test"
	tsDeb=str(int(time.time()))
	print tsDeb
	#tsDeb=str(int(time.mktime(time.localtime())))
	#print tsDeb
	#tsDeb=str(int(time.mktime(time.gmtime())))
	#print tsDeb
	# commut batterie si pas déjà fait
	commutRel(R1,1)
	rel1st = "1"
	#connexion charge 1 (0.5A)
	commutRel(R2,1)
	rel2st = "1"	
	# Adj une charge si bat 14 A/H
	if batCap =="14":
		commutRel(R3,1)
		rel3st = "1"	

# test modif charge
if testSt =="1" and tsDeb != "0":
    print "Modif de charge"
    commutRel(R2,1)
    rel2st = "1"
    print"R2 On"
    if batCap =="14":
        commutRel(R3,1)
        rel3st = "1"
        print"R3 On"
    else:
        commutRel(R3,0)
        rel3st = "0"
        print"R3 Off"

#test pas de test
if testSt == "0":
	print "Pas de test: raz charges"
	commutRel(R2,0)
	rel2st = "0"
	commutRel(R3,0)
	rel3st = "0"
	print "R2,R3 Off"

# stockage des new params
fstoparam(immat,batNum,batCap,testSt,testFin,testBrk,relUdem,rel1st,rel2st,rel3st,rel4st,tsDeb,tsFin)

