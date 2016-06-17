<?php /*	========= Testbat-x.y.php =======================
			Test des batteries en liaison avec testbat-x.y.py
			par passage des paramètres dans  testbat.param
			(c)aliantux.org jdb 2015-2016
			=================================================
*/
require "params.inc.php";
require "toppage.inc.php";
date_default_timezone_set ("Europe/Paris");
//============ A valider après débug ========
//ini_set('display_errors', 1);
error_reporting(E_ALL);
//error_reporting(0);
$row=array();
echo "<body>\n";
//date_default_timezone_set("Europe/Paris");echo "Europe/Paris:".time(); 
// ========== récupération des paramètres ======
echo "<p class=inf1>\n";
$f = fopen($batPath."testbat.param", "r");
	$immat=fparam(fgets($f));//print $immat.", ";
	$batNum=fparam(fgets($f));//print $batNum.", ";
	$batCap=fparam(fgets($f));//print $batCap.", ";
	$testSt=fparam(fgets($f));//print $testSt.", ";
	$testFin=fparam(fgets($f));//print $testFin.", ";
	$testBrk=fparam(fgets($f));//print $testBrk.", ";
	$relUdem=fparam(fgets($f));//print $relUdem.", ";
	$rel1st=fparam(fgets($f));//print $rel1st.", ";
	$rel2st=fparam(fgets($f));//print $rel2st.", ";
	$rel3st=fparam(fgets($f));//print $rel3st.", ";
	$rel4st=fparam(fgets($f));//print $rel4st.", ";
	$tsDeb=fparam(fgets($f));//print $tsDeb.", ";
	$tsFin=fparam(fgets($f));//print $tsFin."\n";
fclose($f);
echo "</p>\n";

// ============== récup des paramètres ============
$kimmat=$immat;
$kbn=$batNum; 
$kbc=$batCap;
$ktst=$testSt;
$ktf=$testFin;
$kbrk=$testBrk;
$krud=$relUdem;
if ($tsDeb=="0")$dift="0";
else $dift=time()-$tsDeb;
/*echo time()."<br>";
echo $dift."<br>";
echo date('H:i:s   Y-m-d',time())."<br>";
echo date('H:i:s   Y-m-d',$tsDeb)."<br>";
echo strftime('%T',$dift)."<br>";
echo gmstrftime('%T',$dift)."<br>";*/

// ========== Images par défaut ======================
$ledbrk="img/led-rd.png";
$bat="img/bat-gy.png";//$led="img/led-gy.png";
if ($rel2st=="1") $lr2="img/lOn.png"; else $lr2="img/lOff.png"; 
if ($rel3st=="1") $lr3="img/lOn.png"; else $lr3="img/lOff.png"; 
if ($rel4st=="1") $lr4="img/lOn.png"; else $lr4="img/lOff.png"; 

// ========== récupération du status des relais ======
if ($rel1st==0 and $rel2st==0){
	$bat="img/bat-gy.png";//$led="img/led-gy.png";
	}
elseif($rel1st==1 and $rel2st==0){
	$bat="img/bat-gn.png";//$led="img/led-gy.png";
	}
elseif($rel1st==1 and $rel2st==1){
	$bat="img/bat-or.png";//$led="img/led-rd.png";
	}

// ============== test des actions POST =====================
if (isset($_POST['cmd'])){
	//echo "<br>".$_POST['cmd']."  ".$_POST['immat']."  ".$_POST['Nb']."  ".$_POST['Cb']."<br>";
	if ($_POST['cmd']=='ENREGISTRER'){
		$kimmat=$_POST['immat']; $kbn=$_POST['Nb']; $kbc=$_POST['Cb'];
		$krud=$_POST['Bat'];
		wrtParam($batPath,$kimmat,$kbn,$kbc,$ktst,$ktf,$kbrk,$krud,$rel1st,$rel2st,$rel3st,$rel4st,$tsDeb,$tsFin);
	}
	elseif ($_POST['cmd']=='Deb_Test') {
		if ($kbrk=='1'){
			//echo" BRK=1";
			$strMsg="Impossible: BREAK en cours";
			echo '<script type="text/javascript"> alert("Test : '.$strMsg.'")</script>';
			$krud="0";$ktst="0";
		}
		elseif ($ktst=="1") {
			$strMsg="Test déjà en cours!";
            echo '<script type="text/javascript"> alert("Test : '.$strMsg.'")</script>';
		}
		elseif ($ktf=="1") {
			$strMsg="Faire une RAZ Test au préalable";
            echo '<script type="text/javascript"> alert("Test : '.$strMsg.'")</script>';
		}
		else {
			//$date_debut = new DateTime(); c'est python qui mettra le timestamp de début
			//echo "date_debut". $date_debut->format('%h:%i:%s')."<br>";
			$ktst="1";$ktf="0";
			$kimmat=$_POST['immat']; $kbn=$_POST['Nb']; $kbc=$_POST['Cb'];
			$krud="1";$tsFin="0";
			wrtParam($batPath,$kimmat,$kbn,$kbc,$ktst,$ktf,$kbrk,$krud,$rel1st,$rel2st,$rel3st,$rel4st,$tsDeb,$tsFin);
		}
	}
	elseif ($_POST['cmd']=='Fin_Test') {
		//$tsFin=time(); c'est python qui mettra le timestamp de fin
		$ktf=1;// c'est python qui mettra à zero $ktst
		wrtParam($batPath,$kimmat,$kbn,$kbc,$ktst,$ktf,$kbrk,$krud,$rel1st,$rel2st,$rel3st,$rel4st,$tsDeb,$tsFin);
		}
	elseif ($_POST['cmd']=='Raz_Brk') {
		$kbrk="0";
		wrtParam($batPath,$kimmat,$kbn,$kbc,$ktst,$ktf,$kbrk,$krud,$rel1st,$rel2st,$rel3st,$rel4st,$tsDeb,$tsFin);
		}
	elseif ($_POST['cmd']=='Raz_Test') {
		$tsDeb='0';$tsFin="0";$ktf="0";$ktst="0";
		wrtParam($batPath,$kimmat,$kbn,$kbc,$ktst,$ktf,$kbrk,$krud,$rel1st,$rel2st,$rel3st,$rel4st,$tsDeb,$tsFin);
		}
	}
//---------------------------------------

/* liste des planeurs*/
$f = fopen($batPath."planeur.lst", "r");
$n=0;
while(!feof($f)) {
    $n=++$n ;
    $lrow[$n]=rtrim(fgets($f));
	//echo $n." ".$lrow[$n]."  ".strlen($lrow[$n])."<br>\n";
	}
?>
<div id="page">
 <div id="header">
 <h1>Graphique test de décharge batterie </h1>
 </div>
 <div id="body">
	<!--<form method='POST' action='testbat.php'>-->
    <form method='POST' action="<?php echo $_SERVER['PHP_SELF']; ?>">
	<table border="0">
      <tr>
	    <td valign='top'>
			<a href="http://www.facebook.com/PlaneurChalles" target="_blank">
			<img src="img/brand-planeurschalles.png" border="0"></a>
		</td>
	    <td valign='top' align='center'>
			<br><select name='immat'>
			<?php
			// remplissage de la combo list
			for ($i=1; $i <= $n; $i++){
				//$id=$lrow[$i]['id_planneur'];
            	echo "<option"; //.$lrow[$i];
				if ($kimmat==$lrow[$i]){
					$immatSelected=$lrow[$i];
					echo " selected";
				}
				echo ">".$lrow[$i]."</option>\n";
				//echo $kimmat."  ".$lrow[$i]." immatselected:".$immatSelected."\n";
			}
			echo "</select>\n<br><br><hr>\n";
   	    echo "</td><td rowspan ='3' align='center'>\n";
			echo "<img src='img/ubat.png' alt='Ubat.png'>\n";
			//echo "<br>kbrk:".$stbrk." l:".strlen($stbrk).", ktst:".$ktest." l:".strlen($ktest)."<br>\n";
			if ($kbrk=='1'){
				echo "<h3 class='brk' >Break en cours !</h3>\n";
				}
			if ($ktst=='1' and $tsDeb !="0"){
				echo "<h3 class='tst' >Test en cours, durée: ".gmstrftime('%T',$dift)."</h3>\n";
				}
			if ($ktf=="1" and $ktst=="0") {
				echo "<h3 class='tst' >Test Terminé, durée: ".gmstrftime('%T',$tsFin-$tsDeb)."</h3>\n";
			}
		echo "</td>\n";
   	    echo "<td rowspan ='3' >\n";
		echo "&nbsp;&nbsp;\n";
		echo "</td>\n";
   	    echo "<td rowspan ='3' align='left' valign='top'>\n";
			//echo "<br><br>\n";
			echo "<p class='param'>\n";
			echo "Paramètres <br><br>\n";
			echo "immat = ".$kimmat."<br>\n";
			echo "batNum = ".$kbn."<br>\n";
			echo "batCap = ".$kbc."<br>\n";
			echo "testSt = ".$ktst."<br>\n";
			echo "testFin = ".$ktf."<br>\n";
			echo "testBrk = ".$kbrk."<br>\n";
			echo "relUdem = ".$krud."<br>\n";
			echo "rel1st = ".$rel1st."<br>\n";
			echo "rel2st = ".$rel2st."<br>\n";
			echo "rel3st = ".$rel3st."<br>\n";
			echo "rel4st = ".$rel4st."<br>\n";
			echo "tsDeb = ".$tsDeb."<br>\n";
			echo "tsFin = ".$tsFin."<br>\n";
			echo "</p>\n";
		echo "</td>\n";
	echo "</tr><tr>\n";
		echo "<td valign='top' align='left'>\n";
			echo "<img src='".$bat."' alt='bat'>&nbsp;&nbsp;<br>\n";
			echo "On:<input type='radio' name='Bat' value='1'";
            if ($krud=="1") echo " checked ><br>\n"; else echo " ><br>\n";
			echo "Off:<input type='radio' name='Bat' value='0'";
            if ($krud=="0") echo " checked >\n"; else echo " >\n";
			echo "<br><br>R2:<img src='".$lr2."' alt='r2'>\n";
			echo "<br>R3:<img src='".$lr3."' alt='r3'><br>\n";
			if ($rel4st=="1"){
				echo "R4:<img src='".$lr4."' alt='r4'>\n";
			}
		echo "</td>\n";
		echo "<td>\n";
			echo "Bat.Numéro:<br>\n";
			echo "1:<input type='radio' name='Nb' value='1'";
			if ($kbn=="1") echo " checked > &nbsp;\n"; else echo " > &nbsp;\n";
			echo "2:<input type='radio' name='Nb' value='2'";
			if ($kbn=="2") echo " checked > <br>\n"; else echo " > <br>\n";
			echo "3:<input type='radio' name='Nb' value='3'";
			if ($kbn=="3") echo " checked > &nbsp;\n"; else echo " > &nbsp;\n";
			echo "4:<input type='radio' name='Nb' value='4'";
			if ($kbn=="4") echo " checked > \n"; else echo " > \n";
			echo "<br><br>\n";
			echo "Bat.Capacité:<br>\n";
			echo "7:<input type='radio' name='Cb' value='7'";
			if ($kbc=="7") echo " checked > &nbsp;\n"; else echo " > &nbsp;\n";
			echo "14:<input type='radio' name='Cb' value='14'";
			if ($kbc=="14") echo " checked >\n"; else echo " >\n";
			echo "<input type='hidden'  name='Ps' value='".$immatSelected."'><br>\n";
			echo "<input type='hidden'  name='Ton' value='".$ktst."'><br>\n";
			?>
			<br>
			<input type='submit' value='ENREGISTRER' name='cmd'>&nbsp;&nbsp;
	        <br><br><hr>
		</td>
      </tr><tr>
		<td align='left' valign='top'>
			<?php if ($kbrk=="1"){
				echo "<br><br>&nbsp;<img src='".$ledbrk."' alt='break'>\n";
				echo "<br><b><font color='red'>&nbsp;Break!</font></b><br><br>\n";
            	echo "<input type='submit' value='Raz_Brk' name='cmd'>&nbsp;&nbsp;<br>&nbsp;\n";
			}?>
		</td>
		<td align='center'>
			<input type='submit' value='Deb_Test' name='cmd'>
	        <br><br>
			<input type='submit' value='Fin_Test' name='cmd'>
	        <br><br>
			<input type='submit' value='Raz_Test' name='cmd'>
		</td>
	</tr>
  </table>
  </form>
  <hr>
  <?php
echo "<h3 class='inf' >Ne pas oublier de remettre la batterie en charge après le test</h3>\n";
echo "Derniere mise &agrave; jour le ".date("d-m-Y")." &agrave; ". date ("H\:i:s")."<br>\n";
echo "Le test s'arrêtera si la tension devient inférieure à 11V ou si la durée de décharge atteint 10 heures\n";
echo "</div>";
echo "<img src='img/ubatr.png' alt='Ubatr.png'>\n";
echo "</div>\n"; //fin de div page et div body
require "btmpage.inc.php";
// ************fonctions perso*************
// ================= Fonctions =============================
function fparam($strLine){
	# extraction du paramètre situé entre le "=" et le ";"
	$pos1 = strpos($strLine,"=");$pos2=strpos($strLine,";");
    $retpar = substr($strLine,$pos1+1,$pos2-$pos1-1);
	return $retpar;
}
//========== ecriture des parametres
function wrtParam($bpath,$wimmat,$wnb,$wnc,$wtst,$wtf,$wbrk,$wrud,$wr1st,$wr2st,$wr3st,$wr4st,$wtsDeb,$wtsFin){
	$handle = fopen($bpath."testbat.param", "w");
	fwrite($handle, "immat=".$wimmat.";\n");
	fwrite($handle, "batNum=".$wnb.";\n");
	fwrite($handle, "batCap=".$wnc.";\n");
	fwrite($handle, "testSt=".$wtst.";\n");
	fwrite($handle, "testFin=".$wtf.";\n");
	fwrite($handle, "testBrk=".$wbrk.";\n");
	fwrite($handle, "relUdem=".$wrud.";\n");
	fwrite($handle, "rel1st=".$wr1st.";\n");
	fwrite($handle, "rel2st=".$wr2st.";\n");
	fwrite($handle, "rel3st=".$wr3st.";\n");
	fwrite($handle, "rel4st=".$wr4st.";\n");
	fwrite($handle, "tsDeb=".$wtsDeb.";\n");
	fwrite($handle, "tsFin=".$wtsFin.";\n");
	fclose($handle);
	echo "<p class=inf2>\n";
		echo "Enregistrement params: Ok\n";
	echo "</p>\n";
}
?>
