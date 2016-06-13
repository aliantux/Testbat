#!/bin/sh
#
TSTPATH="$HOME/adc"
TMPDIRUSER="/tmp/$USER"
TMPDIRTBAT="$TMPDIRUSER/bat"
echo $TSTPATH $TMPDIRTBAT
#
# attente de la fin des mesures par testbat.py 
sleep 3

# cree le rep /tmp/user if not exist
[ -d $TMPDIRUSER ] || mkdir $TMPDIRUSER

# cree le rep /tmp/user/bat if not exist
[ -d $TMPDIRTBAT ] || mkdir $TMPDIRTBAT

# recup params
. $TSTPATH/testbat.param

dtg=`date +'%H:%M'`
dtf=`date +'%d-%m-%Y'`

inf=`date +'Debut test le %d/%m %H:%M' -d @$tsDeb`
orgr=`date +'%H:%M' -d @$tsDeb`
fin=`date +'le %d/%m  %H:%M' -d @$tsFin`
dur=`echo $(($tsFin - $tsDeb))`
echo "datGraph	Deb		Fin		Dur		tstfin"
echo $dtg		$tsDeb	$tsFin	$dur 	$testFin

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

#`date +"%d-%m-%Y"`" "`date +"%H:%M:%S"` \
tim=`date +"%H:%M"`
#batCap=`echo $batCap | sed "s/0//"`

#--title  "CSVVA - Planeur $immat - Bat. N.$batNum : $batCap A/H   $inf"\

#creation du graph web
rrdtool graph $TMPDIRTBAT/ubat.png \
    --imgformat PNG --width 480 --height 240 \
    --title  "CSVVA - $immat -   $tim"\
	--vertical-label "U batterie (V) "$dtf" "$dtg \
    --start=now-13h --end=now \
    --lower-limit 0 --upper-limit 15 --rigid \
	--right-axis-label 'I charge (A)'\
    --right-axis .1:0               \
	--right-axis-format %1.1lf		\
    DEF:Ubat=$TSTPATH/acu.rrd:adc0:AVERAGE \
    DEF:Ibat=$TSTPATH/acu.rrd:adc1:AVERAGE \
	CDEF:Ig=Ibat,10,*	\
    AREA:Ubat#21fd93 \
    AREA:Ig#fd7921 \
	LINE1:Ubat#0000FF:Ubat \
    GPRINT:Ubat:LAST:"%4.2lf V" \
	VDEF:VM=Ubat,MAXIMUM         \
    COMMENT:"Vmax\:" GPRINT:VM:"%4.2lf V" \
	GPRINT:VM:"%H\:%M\:%S":strftime \
	VDEF:Vm=Ubat,MINIMUM         \
    COMMENT:"Vmin\:" GPRINT:Vm:"%4.2lf V" \
	GPRINT:Vm:"%H\:%M\:%S             ":strftime \
	LINE2:Ig#fd3021:Ibat \
	GPRINT:Ibat:LAST:"%4.2lf A" \
	VDEF:IM=Ibat,MAXIMUM         \
    COMMENT:"Imax\:" GPRINT:IM:"%4.2lf A" \
	GPRINT:IM:"%H\:%M\:%S             ":strftime \
	HRULE:11#FF0000:"Limite basse"		

#
# creation du graph reduit pour aff 320x240
rrdtool graph $TMPDIRTBAT/ubatr.png \
    --imgformat PNG --width 320 --height 240 --full-size-mode \
	--color CANVAS#000000                   \
    --color BACK#101010                     \
    --color FONT#C0C0C0                     \
    --color MGRID#404040                    \
    --color GRID#202020                     \
    --color FRAME#404040                    \
    --color ARROW#FFFFFF                    \
    --title "CSVVA $immat Bat$batNum $batCap A/H Deb:$orgr" \
	--vertical-label "U bat \ I bat(*10) "$dtf \
    --start=now-13h --end=now \
    --lower-limit 0 --upper-limit 15 --rigid \
    DEF:Ubat=$TSTPATH/acu.rrd:adc0:AVERAGE \
    DEF:Ibat=$TSTPATH/acu.rrd:adc1:AVERAGE \
	CDEF:Ig=Ibat,10,*	\
    AREA:Ubat#21fd93 \
    AREA:Ig#fd7921 \
	LINE2:Ig#fd3021:Ibat \
	GPRINT:Ibat:LAST:"%4.2lf A" \
	LINE1:Ubat#0000FF:Ub \
    GPRINT:Ubat:LAST:"%2.2lfV" \
	HRULE:11#FF0000:"U.min"		\
	COMMENT:"IP="$wip			\
