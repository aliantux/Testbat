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
Ubat = readAdc(adcU) * ( 3.3 / 1024.0) * 5
Ibat = readAdc(adcI) * ( 3.3 / 1024.0)

print "\tHeure mesure:"+strTime
print "\ttension : %0.2f V" % Ubat
print "\tIntensité : %0.2f A" % Ibat
print "\tPuissance : %0.2f W" % (Ubat * Ibat)

# stockage en rrd
ret = rrd_update(batPath+'acu.rrd', 'N:%s:%s' %(Ubat,Ibat));
print 'Result rrdSto: ', ret

# test conditions brk
if Ubat >= 15 or (Ubat > 1 and Ubat < Umin):
	testBrk="1"
	relUdem="0"
	rel1st = commutRel(R1,0)
	rel2st = commutRel(R2,0)
	rel3st = commutRel(R3,0)
	tsFin=str(int(time.time()))
	testSt="0"

# test fin test 
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
	# commut batterie si pas déjà fait
	rel1st=commutRel(R1,1)
	#connexion charge 1 (0.5A)
	rel2st=commutRel(R2,1)
	# Adj une charge si bat 14 A/H
	if batCap =="14":
		rel3st=commutRel(R3,1)

# test modif charge
if testSt =="1" and tsDeb != "0":
	if rel2st=="0":
		rel2st=commutRel(R2,1)
		print"R2 On"
	if batCap =="14":
		if rel3st=="0":
			rel3st=commutRel(R3,1)
			print"R3 On"
		else:
			rel3st=commutRel(R3,0)
			print"R3 Off"

#test pas de test
if testSt == "0":
	print "Pas de test: raz charges"
	if rel2st == "1":
		rel2st=commutRel(R2,0)
		print "R2 Off"
	if rel3st == "1":
		rel3st=commutRel(R3,0)
		print "R3 Off"

#raz R1 1h après fin test
if testFin=="1" and durdeb > maxsec+3600 and rel1St=="1":
    rel1st = commutRel(R1,0)
    relUdem = "0"
    print "R1 Off"

# stockage des new params
fstoparam(immat,batNum,batCap,testSt,testFin,testBrk,relUdem,rel1st,rel2st,rel3st,rel4st,tsDeb,tsFin)

