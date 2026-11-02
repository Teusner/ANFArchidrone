# ANF ArchiDrone 2026 — Journée 2 : Robotique Marine & Sous-Marine

Ce dépôt contient l'ensemble des supports pédagogiques, codes sources LaTeX, scripts de démonstration et outils de génération pour le cours de **Robotique Marine et Sous-Marine pour l'Acquisition Scientifique**, dispensé lors de l'**Action Nationale de Formation (ANF) ArchiDrone 2026** pour les réseaux technologiques **Drone&Cap'** et **2RM** (Réseau Métier des Roboticiens et Mécatroniciens).

* **Date de la formation** : 04 Novembre 2026 (Jour 2 de l'ANF)
* **Formateur** : Quentin Brateau
* **Public** : Chercheurs, ingénieurs et techniciens des réseaux Drone&Cap' et 2RM (écologie marine, océanographie, géosciences, data science, mécatronique).

---

### 1. Organisation de la Journée & Contenu Technique Réel

Le cours s'appuie sur la réalité de fabrication et d'exploitation des plateformes ouvertes de référence (**BlueROV2**, **BlueBoat**, capteurs **Bar30/Bar02**, propulseurs **T200/T500**, carte **Navigator**, caissons étanches 3"/4", pénétrateurs **WetLink Standard** et **WetLink JPT**, batteries Li-ion et physique des pertes Joule, alimentation haute tension **OTPS 400V**, liaisons **Fathom-X** & boîtier **FXTI**, **BaseStation** WiFi, radiocommandes **RC**, système **BlueOS**, interface **Cockpit** et intégration **ROS 2**).

| Horaire | Module | Thématique principale & Contenu Matériel Réel |
| :--- | :--- | :--- |
| **08h30 -- 10h00** | **Module 1** | **Introduction, typologie des 5 grands vecteurs marins & similitudes avec l'aérien**<br/>*Panorama complet des vecteurs scientifiques : **ROV** (BlueROV2), **AUV** (Seaber YUCO), **ASV** (BlueBoat), **Gliders sous-marins** (Teledyne Slocum G3) et **Bouées dérivantes profilantes** (réseau mondial Argo / Provor / Apex). Photos HD, principes physiques (flottabilité variable vs propulsion hélice vs dérive lagrangienne), caractéristiques techniques (autonomie, élongation, capteurs CTD/BGC/PAM) et tableau comparatif des 5 familles. Ordres de grandeur des prix d'acquisition, acteurs mondiaux (~1m) et revendeurs français (SyERA, ROV Expert, Subsea Tech).* |
| *10h00 -- 10h30* | *Pause* | *Pause café & échanges informels* |
| **10h30 -- 12h00** | **Module 2** | **Présentation d'un drone sous-marin : différences avec l'aérien & fabrication**<br/>*Ruptures physiques ($\rho \times 850$), hydrostatique passive ($B$ au-dessus de $G$, flottabilité positive $+300\,\text{g}$), fabrication réelle des caissons étanches 3" et 4" (acrylique vs alu 6061-T6 anodisé dur, brides O-ring, cordon de verrouillage locking cord, flasques M10 et dômes optiques), la révolution des pénétrateurs mécaniques étanches : WetLink standard ($950\,\text{m}$) vs nouveau WetLink JPT (Jacket Pass-Through sans dénudage de gaine, $100\,\text{m}$), **connecteurs étanches débrochables** (**Blue Trail Engineering Cobalt** M10, **SubConn Micro Circular**) pour l'interchangeabilité en mer (remplacement express d'un propulseur défaillant sans ouvrir le caisson, ajout de capteurs à la volée sur ports auxiliaires pré-câblés, commande & puissance, distinction Dry-mate vs Wet-mate), test de vide terrain obligatoire (-0.5 bar), black-out GNSS et navigation par DVL (Water Linked DVL-A50) et USBL.* |
| *12h00 -- 13h30* | *Repas* | *Pause déjeuner & réseautage* |
| **13h30 -- 15h00** | **Module 3** | **Communications, architecture d'essais, alimentation OTPS, BlueOS & ROS 2**<br/>*Architecture d'essais terrain : station sol PC avec QGroundControl ou Cockpit, boîtier d'interface de surface FXTI pour ombilical Fathom-X (CPL 100 Mbps sur 300 m), BlueRobotics BaseStation WiFi 2.4 GHz pour ASV de surface, et liaison radiocommande RC manuelle (2.4 GHz SBUS direct sur Navigator) pour sécurité à la mise à l'eau et override matériel d'urgence. Alimentation haute tension par câble OTPS (Outland Technology Power Supply : 400V DC surface divisant le courant par 25 et les pertes Joule par ~700, carte abaisseuse sous-marine 15V DC 45A / 1000W pour plongées 24h/24). Système embarqué BlueOS (Docker), passerelle ROS 2 (topics sensor_msgs et enregistrement rosbag2 MCAP), fail-safes matériels.* |
| *15h00 -- 15h30* | *Pause* | *Pause café & échanges informels* |
| **15h30 -- 16h30** | **Module 4** | **Exemples de capteurs et mesures spécifiques : de la collecte à la donnée**<br/>*Sonars concrets pour la recherche (Ping Sonar 115 kHz, Ping360 à balayage 750 kHz, sonar d'imagerie Cerulean Omniscan 450 FS, bathymétrie multifaisceaux Cerulean Surveyor 240-16 MBES), méthodologie d'intégration d'un capteur scientifique tiers (sonde multiparamètre via WetLink M10 et USB/I2C), sondes CTD et calcul de célérité acoustique (TEOS-10), et formats de données FAIR (NetCDF-4, GeoTIFF, LAS).* |
| **16h30 -- 17h30** | **Module 5** | **Retours d'experience, cas concrets de labo & atelier projets**<br/>*Projet 1 : BlueROV2 échantillonneur benthique. Projet 2 : BlueBoat hydrographe bathymétrique relié au réseau Centipede RTK. Projet 3 : Micro-AUV YUCO (Seaber) pour transects CTD et sonar hauturier. Budgets réalistes. Les 10 règles d'or de terrain. Tour de table des projets des participants.* |

---

## 2. Structure du Dépôt

```text
2026 ANF ArchiDrone/
├── build.bat                            # Script batch de compilation tout-en-un
├── programme_anf_archidrone.png         # Planning officiel fourni par les organisateurs
├── README.md                            # Documentation complète du cours
├── imgs/                                # Banques d'images HD des composants réels (29 illustrations)
│   ├── t200_thruster.png, t500_thruster.jpg, newton_gripper.jpg   (Actionneurs)
│   ├── bar30_sensor.jpg, bar02_sensor.jpg, ping_echosounder.jpg   (Capteurs)
│   ├── ping360_sonar.jpg, cerulean_omniscan.jpg, cerulean_surveyor_mbes.jpg, dvl_a50.jpg
│   ├── bluerov2.jpg, blueboat.jpg, seaber_yuco.jpg, seaber_yuco_diagram.png (Motorisés)
│   ├── slocum_glider_clean.jpg, argo_float_clean.jpg (Gliders & Bouées Argo)
│   ├── navigator_board.jpg, pixhawk_autopilot.png, raspberry_pi_4.jpg (Calculateurs)
│   ├── watertight_enclosure.jpg, wetlink_penetrator.jpg, wetlink_jpt.jpg (Caissons & Pénétrateurs)
│   ├── bluetrail_cobalt.jpg, bluetrail_cobalt_pair.png, subconn_micro_circular.jpg (Connecteurs Étanches)
│   ├── battery_pack.jpg, otps_power_system.png (Énergie Li-ion & Haute Tension 400V)
│   └── fathom_x.png, fathom_tether.jpg, fxti_interface.jpg, basestation_wifi.jpg (Comms & Essais)
├── src/
│   ├── slides/                          # Support de présentation principal (LaTeX Beamer, 55 planches)
│   │   ├── main.tex                     # Fichier maître Beamer
│   │   ├── preambule.tex                # Thème personnalisé, charte océanographique & macros
│   │   ├── 00_introduction.tex          # Cadrage pédagogique, 5 familles de vecteurs (ROV, AUV, ASV, Gliders Slocum, Bouées Argo)
│   │   ├── 01_similitudes_aerien.tex    # Module 1 : Similitudes aérien, Seaber, Coûts, Acteurs, T200, Navigator, Batterie & Joule
│   │   ├── 02_differences_milieu.tex    # Module 2 : Caissons 3"/4", WetLink vs JPT, Connecteurs Cobalt & SubConn, test vide, DVL
│   │   ├── 03_comms_autonomie.tex       # Module 3 : Station sol, FXTI, BaseStation WiFi, lien RC, OTPS 400V, BlueOS & ROS 2
│   │   ├── 04_capteurs_donnees.tex      # Module 4 : Ping Sonar, Ping360, Omniscan, MBES, CTD TEOS-10
│   │   └── 05_synthese_discussion.tex   # Module 5 : Cas pratiques (BlueROV2/BlueBoat/Seaber YUCO), budgets, règles d'or
│   ├── handouts/                        # Fiche de synthèse technique (Mémento condensé 2 pages recto-verso)
│   │   └── fiche_memo_robotique_sous_marine.tex
│   └── demos/                           # Scripts Python pédagogiques de démonstration
│       ├── 01_dead_reckoning_dvl.py     # Simulation : dérive IMU vs DVL vs recalage USBL
│       └── 02_ctd_georeferencing.py     # Traitement : synchronisation et coupe 2D d'un profil CTD
└── build/                               # Fichiers finaux générés (créé automatiquement)
    ├── slides/
    │   └── slides_robotique_sous_marine.pdf
    ├── synthesis/
    │   └── fiche_synthese_robotique_sous_marine.pdf
    └── demos/
        ├── dvl_drift_comparison.png
        └── ctd_transect_profile.png
```

---

## 3. Génération Automatique des Supports (`build.bat`)

Pour compiler l'intégralité des supports :

```cmd
build.bat
```

Le script produit instantanément :
1. `build/slides/slides_robotique_sous_marine.pdf` (Présentation Beamer illustrée)
2. `build/synthesis/fiche_synthese_robotique_sous_marine.pdf` (Mémento technique condensé 2 pages recto-verso)
3. `build/demos/dvl_drift_comparison.png` (Visualisation dérive DVL vs IMU)
4. `build/demos/ctd_transect_profile.png` (Visualisation transect CTD 2D)
