#!/bin/sh
#
# attente de la fin des mesures par testbat.py 
sleep 3

# cree le rep /tmp/bat if not exist
[ -d /tmp/bat ] || mkdir /tmp/bat

# recup params
. /home/jdb/bat/testbat.param
. /home/jdb/bat/ip.param

inf=`date +'Debut test le %d/%m %H:%M' -d @$tsDeb`
orgr=`date +'%H:%M' -d @$tsDeb`
fin=`date +'le %d/%m  %H:%M' -d @$tsFin`
dur=`echo $(($tsFin - $tsDeb))`
echo $tsDeb  $tsFin $dur $testFin

if [ "$tsDeb" = "0" ] # && [" $tsFin" = "0" ]
then
	inf="--:--"
	orgr="--:--"
fi
if [ "$testFin" = "1" ] || [ "$testBrk" = "1" ]
then
	inf=`date +'Duree test %H:%M' -d @$dur`
fi
echo $inf

#	`date +"%d-%m-%Y"`" "`date +"%H:%M:%S"` \
# tim=`date +"%H:%M"`
#batCap=`echo $batCap | sed "s/0//"`

#creation du graph web
rrdtool graph /tmp/bat/ubat.png \
    --imgformat PNG --width 480 --height 240 \
    --title  "CSVVA - Planeur $immat - Bat. N.$batNum : $batCap A/H   $inf"\
	--vertical-label "U batterie (V)" \
    --start=now-13h --end=now \
    --lower-limit 0 --upper-limit 15 --rigid \
	--right-axis-label 'I decharge (A)'\
    --right-axis .1:0               \
	--right-axis-format %1.1lf		\
    DEF:Ubat=/home/jdb/bat/acu.rrd:adc0:AVERAGE \
    DEF:Ibat=/home/jdb/bat/acu.rrd:adc1:AVERAGE \
	CDEF:Ig=Ibat,10,*	\
    AREA:Ubat#21fd93 \
    AREA:Ig#fd7921 \
	LINE2:Ig#fd3021:Ibat \
	GPRINT:Ibat:LAST:"%4.2lf A" \
	LINE1:Ubat#0000FF:Ubat \
    GPRINT:Ubat:LAST:"%4.2lf V" \
	VDEF:VM=Ubat,MAXIMUM         \
    COMMENT:"Vmax\:" GPRINT:VM:"%4.2lf V" \
	GPRINT:VM:"%H\:%M\:%S":strftime \
	VDEF:Vm=Ubat,MINIMUM         \
    COMMENT:"Vmin\:" GPRINT:Vm:"%4.2lf V" \
	GPRINT:Vm:"Hmes\: %H\:%M\:%S":strftime \
	HRULE:11#FF0000:"Limite basse"
#
# creation du graph reduit pour aff 320x240
rrdtool graph /tmp/bat/ubatr.png \
    --imgformat PNG --width 320 --height 240 --full-size-mode \
	--color CANVAS#000000                   \
    --color BACK#101010                     \
    --color FONT#C0C0C0                     \
    --color MGRID#404040                    \
    --color GRID#202020                     \
    --color FRAME#404040                    \
    --color ARROW#FFFFFF                    \
    --title "CSVVA $immat Bat$batNum $batCap A/H Deb:$orgr" \
	--vertical-label "U bat \ I bat(*10)" \
    --start=now-13h --end=now \
    --lower-limit 0 --upper-limit 15 --rigid \
    DEF:Ubat=/home/jdb/bat/acu.rrd:adc0:AVERAGE \
    DEF:Ibat=/home/jdb/bat/acu.rrd:adc1:AVERAGE \
	CDEF:Ig=Ibat,10,*	\
    AREA:Ubat#21fd93 \
    AREA:Ig#fd7921 \
	LINE2:Ig#fd3021:Ibat \
	GPRINT:Ibat:LAST:"%4.2lf A" \
	LINE1:Ubat#0000FF:Ub \
    GPRINT:Ubat:LAST:"%2.2lfV" \
	HRULE:11#FF0000:"U.min"		\
	COMMENT:"IP="$wip				
#    PRINT:Ubat:LAST:"%4.2lf V" 
	#COMMENT:"  "$deb	\
	#COMMENT:"Début test\: 10\:24"	\
    #--title  "CSVVA - Planeur $Ps - Batterie N°$Nb : $Cb A/H      "`date +"%H:%M:%S"` \
	
#VDEF:VM=Ubat,MAXIMUM         \
#   COMMENT:"Mx\:" GPRINT:VM:"%2.2lfV" \
