Measuring the actual capacity of a battery by an controlled discharge

Contexte :
==========
C'est la seule source d'énergie disponible à bord pendant tout un vol qui peut durer de 5 minutes à 10 heures avec des vols habituels de 3 à 5 heures

Il est donc important de savoir sur quelle quantité d'énergie on peut compter.

Tous les instruments de base du pilotage fonctionnent avec des pressions d'air ( statique, dynamique   …), la batterie n'est pas « vitale » pour assurer le pilotage mais est devenue indispensable en terme de sécurité.
La batterie a été introduite dans un premier temps afin de faire fonctionner la radio, puis les variomètres électroniques sont apparus puis les calculateurs de vols avec GPS, et enfin les systèmes anti-collision (Flarm).
Certain planeurs sont même aujourd'hui équipés de transpondeurs et de feux à éclats afin d'être vus plus tôt par les autres  pilotes.

Compte tenu de tout ces équipements, la consommation moyenne lors d'un vol est comprise entre 0,5 et 1 A ( 2 à 3 A de plus lors d'un message radio.)

C'est pourquoi on dispose à bord d'une ou deux batteries ( voir 3) de 7 ou 14 A/H, elles ont amovibles et rechargées systématiquement après chaque vol dans un local dédié à cet usage.

Actuellement les batteries plomb étanches sont les plus courantes.
Lors des visites annuelles pendant la période hivernale, j'ai conçu ce testeur afin d'avoir l'image la plus juste de l'état de la batterie et de déceler à coup sur les batteries défectueuses.

Principe :
=========
Le principe est de prendre une batterie chargée et de la décharger au 1/10 de sa capacité (correspondant grosso-modo aux conditions de vol) pendant une durée max de 10 heures avec arrêt automatique du test si la tension batterie descend au dessous de 11 V.
Les mesures et un graph de suivi sont effectuées toutes les minutes via une tache cron, le paramétrage, la commande du test et la visualisation sont réalisés via une interface web et les données stockées sur une base rrd

Hardware :
==========
Le hardware est basé sur le populaire Raspberry-PI , à l'origine un modèle B mais est tout à fait transposable sur un B+, un 2 et même testé sur un PI-0.
J'ai créé une platine complémentaire comportant des relais de commutation de la batterie et des résistances de décharge, un convertisseur analogique numérique, des systèmes de protection, avec en option une horloge RTC, un mini écran 2,5" afin de rendre l'appareil autonome.

Software :
==========
L'applicatif utilise une page web php qui renseigne un fichier d'échange et assure la visualisation instantanée de l'avancement du test  et  un programme en python qui assure le contrôle, les mesures et le stockage des données
