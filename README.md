# Props Roblox – quartier délabré

95 objets low-poly (100 fichiers `.fbx` avec les variantes) pour un jeu Roblox satirique dans un quartier pauvre :
mobilier urbain, véhicules, déchets, marché, chantier et décors de boutiques. Style « simulateur » cartoon,
formes arrondies, arêtes biseautées, couleurs vives mais salies, sans texture photo ni texte.

Tous les modèles sont générés par script avec Blender (module Python `bpy`), donc reproductibles et modifiables.

## Conventions

| | |
|---|---|
| Échelle | 1 stud = 0,28 m. Les fichiers sont en mètres à taille réelle ; la boîte englobante est recalée exactement sur les dimensions demandées (X × Y × Z = largeur × hauteur × profondeur). |
| Pivot | Centre de la base : objet posé à Y = 0, centré en X et Z. |
| Orientation | Face avant vers −Z (export « −Z forward, Y up », réglages Blender recommandés par Roblox). Les meubles dont la fiche met la longueur sur Z (canapé, banc, établi, portant, table haute) gardent cette orientation ; leur côté utile est indiqué dans la colonne Pièces ou les notes de `models/report.json`. |
| Triangles | Tous sous 5 000 (le plus lourd : l'étal de marché, 4 448). |
| Couleurs | Une seule texture partagée, `models/palette.png` (512 × 256, 128 cases unies avec un léger dégradé de crasse vers le bas), intégrée à chaque `.fbx`. |
| Pièces séparées | Tout ce qui bouge ou s'allume est une pièce nommée : `Couvercle`, `Porte…`, `Ampoule`, `Flammes`, `Vitre(s)`, `Ecran`, `Neon`, `Lumiere`, `Phares`, `Roue_AvG`… Les pièces mobiles ont leur origine sur la charnière ou l'axe. |
| Enseignes | Aucun texte : panneaux, ardoises, menus et le panneau « EN PANNE » sont des surfaces vierges à habiller en jeu. |

## Import dans Roblox Studio

1. *Avatar › Import 3D* (ou glisser le `.fbx`), unité du fichier : **mètre**.
2. Vérifier la taille du Model importé : elle doit correspondre au tableau ci-dessous.
3. Si la texture n'est pas reprise automatiquement, importer `models/palette.png` et l'assigner en `TextureID` à chaque MeshPart.
4. Conseillé : pièces lumineuses (`Ampoule`, `Neon`, `Feu_*`, `Ecran`, `Flammes`…) en `Material = Neon` ; vitres en `Transparency ≈ 0,5`.

## Régénérer

```bash
pip install bpy==4.2.0 pillow
python3 tools/build.py              # tout (export + vignettes dans renders/)
python3 tools/build.py 04 46        # seulement certains numéros
python3 tools/build.py --no-render  # sans les vignettes
python3 tools/readme_table.py       # met à jour le tableau ci-dessous
```

- `tools/lib.py` : primitives biseautées, palette, recalage des dimensions, export FBX.
- `tools/m_*.py` : un fichier par catégorie, une fonction par objet.
- `models/report.json` : dimensions, triangles et pièces de chaque fichier.
- `renders/` : vignettes de prévisualisation.

## Modèles

<!-- table -->
| # | Objet | Dimensions (X × Y × Z studs) | Triangles | Pièces | Fichier |
|---|---|---|---|---|---|
| 01 | Lampadaire | 1,4 × 14,5 × 2,6 | 720 | Poteau, TeteLampe, Ampoule | [01_lampadaire.fbx](models/01_rue/01_lampadaire.fbx) |
| 02 | Feu tricolore | 1,4 × 11 × 1,2 | 1124 | Poteau, Boitier, Feu_Rouge, Feu_Orange, Feu_Vert | [02_feu_tricolore.fbx](models/01_rue/02_feu_tricolore.fbx) |
| 03 | Corbeille de rue | 1,8 × 2,6 × 1,8 | 716 | Corbeille | [03_corbeille.fbx](models/01_rue/03_corbeille.fbx) |
| 04 | Benne à ordures | 6 × 4 × 3,4 | 1570 | Benne, Couvercle | [04_benne.fbx](models/01_rue/04_benne.fbx) |
| 05a | Sac poubelle A | 1,5 × 1,3 × 1,4 | 268 | Sac | [05a_sac_poubelle.fbx](models/01_rue/05a_sac_poubelle.fbx) |
| 05b | Sac poubelle B | 1,5 × 1,3 × 1,4 | 268 | Sac | [05b_sac_poubelle.fbx](models/01_rue/05b_sac_poubelle.fbx) |
| 05c | Sac poubelle C | 1,5 × 1,3 × 1,4 | 404 | Sac | [05c_sac_poubelle.fbx](models/01_rue/05c_sac_poubelle.fbx) |
| 06 | Baril de feu | 2,2 × 3,2 × 2,2 | 1296 | Fut, Braises, Flammes | [06_baril_feu.fbx](models/01_rue/06_baril_feu.fbx) |
| 07 | Abribus | 12 × 9,3 × 3,3 | 1176 | Structure, Toit, Vitres, Banc, PanneauHoraires | [07_abribus.fbx](models/01_rue/07_abribus.fbx) |
| 08 | Plaque d'égout | 2,6 × 0,1 × 2,6 | 812 | Plaque | [08_plaque_egout.fbx](models/01_rue/08_plaque_egout.fbx) |
| 09 | Armoire électrique | 2,6 × 4 × 1,4 | 828 | Caisson, PorteGauche, PorteDroite | [09_armoire_electrique.fbx](models/01_rue/09_armoire_electrique.fbx) |
| 10 | Poteau électrique en bois | 6 × 24 × 1 | 776 | Poteau | [10_poteau_electrique.fbx](models/01_rue/10_poteau_electrique.fbx) |
| 11 | Transformateur sur poteau | 1,8 × 2,6 × 1,8 | 1020 | Transformateur | [11_transformateur.fbx](models/01_rue/11_transformateur.fbx) |
| 12 | Haut-parleur pavillon | 1,6 × 1,3 × 1,3 | 444 | HautParleur | [12_haut_parleur.fbx](models/01_rue/12_haut_parleur.fbx) |
| 13 | Sacs de sable empilés | 2,4 × 1 × 1,4 | 308 | Sacs | [13_sacs_sable.fbx](models/01_rue/13_sacs_sable.fbx) |
| 14 | Clôture grillagée avec barbelés | 8 × 6 × 0,3 | 1434 | Poteaux, Grillage, Barbele | [14_cloture_grillagee.fbx](models/01_rue/14_cloture_grillagee.fbx) |
| 15 | Panneau de signalisation | 2 × 7 × 0,3 | 476 | Poteau, Panneau | [15_panneau_signalisation.fbx](models/01_rue/15_panneau_signalisation.fbx) |
| 16 | Passerelle métallique | 8 × 1 × 3 | 1196 | Passerelle | [16_passerelle.fbx](models/01_rue/16_passerelle.fbx) |
| 17 | Vieille voiture cabossée | 5,2 × 4,6 × 10,1 | 1960 | Carrosserie, Vitres, Phares, FeuxArriere, Roue_AvG, Roue_AvD, Roue_ArG, Roue_ArD | [17_vieille_voiture.fbx](models/02_vehicules/17_vieille_voiture.fbx) |
| 18 | Camionnette utilitaire | 5,6 × 6,2 × 11,3 | 2212 | Carrosserie, Vitres, Phares, FeuxArriere, Roue_AvG, Roue_AvD, Roue_ArG, Roue_ArD | [18_camionnette.fbx](models/02_vehicules/18_camionnette.fbx) |
| 19 | Petite citadine | 5 × 4,2 × 8,3 | 1740 | Carrosserie, Vitres, Phares, FeuxArriere, Roue_AvG, Roue_AvD, Roue_ArG, Roue_ArD | [19_citadine.fbx](models/02_vehicules/19_citadine.fbx) |
| 20 | Camion porteur avec caisse | 6,9 × 8,8 × 20,4 | 3104 | Chassis, Cabine, Vitres, Caisse, PorteArriere, Phares, FeuxArriere, Roue_AvG, Roue_AvD, Roue_Ar1G, Roue_Ar1D, Roue_Ar2G, Roue_Ar2D | [20_camion_porteur.fbx](models/02_vehicules/20_camion_porteur.fbx) |
| 21 | Épave de voiture brûlée | 4,8 × 4,6 × 10,1 | 976 | Epave | [21_epave_brulee.fbx](models/02_vehicules/21_epave_brulee.fbx) |
| 22a | Carton ouvert | 2,1 × 1,9 × 1,7 | 484 | Carton | [22a_carton_ouvert.fbx](models/03_dechets/22a_carton_ouvert.fbx) |
| 22b | Carton aplati | 2,1 × 1,9 × 1,7 | 164 | Carton | [22b_carton_aplati.fbx](models/03_dechets/22b_carton_aplati.fbx) |
| 23 | Matelas sale taché | 4,5 × 0,8 × 7 | 544 | Matelas | [23_matelas.fbx](models/03_dechets/23_matelas.fbx) |
| 24 | Pneu usé | 2,6 × 0,9 × 2,6 | 1152 | Pneu | [24_pneu.fbx](models/03_dechets/24_pneu.fbx) |
| 25 | Caddie de supermarché rouillé | 2,6 × 3 × 3,4 | 1060 | Caddie | [25_caddie.fbx](models/03_dechets/25_caddie.fbx) |
| 26 | Tente de fortune avec bâche | 7 × 5 × 7 | 592 | Structure, Bache | [26_tente_fortune.fbx](models/03_dechets/26_tente_fortune.fbx) |
| 27 | Sac de couchage / couverture en boule | 2 × 0,6 × 5 | 240 | SacCouchage | [27_sac_couchage.fbx](models/03_dechets/27_sac_couchage.fbx) |
| 28 | Bouteille vide | 0,35 × 1 × 0,35 | 200 | Bouteille | [28_bouteille.fbx](models/03_dechets/28_bouteille.fbx) |
| 29 | Canette écrasée | 0,35 × 0,6 × 0,35 | 204 | Canette | [29_canette.fbx](models/03_dechets/29_canette.fbx) |
| 30 | Gobelet | 0,3 × 0,4 × 0,3 | 256 | Gobelet | [30_gobelet.fbx](models/03_dechets/30_gobelet.fbx) |
| 31 | Journal froissé | 0,9 × 0,1 × 0,9 | 60 | Journal | [31_journal.fbx](models/03_dechets/31_journal.fbx) |
| 32 | Pigeon | 0,6 × 0,8 × 1 | 576 | Pigeon | [32_pigeon.fbx](models/03_dechets/32_pigeon.fbx) |
| 33 | Rat avec sa queue | 0,5 × 0,4 × 1,6 | 588 | Rat | [33_rat.fbx](models/03_dechets/33_rat.fbx) |
| 34 | Étal de marché | 13 × 9 × 5 | 4448 | Comptoir, Structure, Auvent, Panneau | [34_etal_marche.fbx](models/04_marche/34_etal_marche.fbx) |
| 35 | Cagette en bois vide | 2,4 × 1,6 × 2,4 | 736 | Cagette | [35_cagette_vide.fbx](models/04_marche/35_cagette_vide.fbx) |
| 36 | Cagette de fleurs pleine | 2,4 × 2 × 2,4 | 2638 | Cagette, Fleurs | [36_cagette_fleurs.fbx](models/04_marche/36_cagette_fleurs.fbx) |
| 37 | Cône de chantier | 1,2 × 2 × 1,2 | 196 | Cone | [37_cone_chantier.fbx](models/05_chantier/37_cone_chantier.fbx) |
| 38 | Fût rayé rouge et blanc | 2 × 3 × 2 | 1096 | Fut, Lampe | [38_fut_raye.fbx](models/05_chantier/38_fut_raye.fbx) |
| 39 | Toilettes de chantier | 3,4 × 7 × 3,4 | 1256 | Cabine, Porte | [39_toilettes_chantier.fbx](models/05_chantier/39_toilettes_chantier.fbx) |
| 40 | Bungalow de chantier | 14 × 7 × 6 | 2884 | Bungalow, Vitres, Porte, Lampe | [40_bungalow_chantier.fbx](models/05_chantier/40_bungalow_chantier.fbx) |
| 41 | Palette | 4 × 0,5 × 4 | 912 | Palette | [41_palette.fbx](models/05_chantier/41_palette.fbx) |
| 42 | Gros tuyau béton/acier | 16 × 1 × 1 | 524 | Tuyau | [42_gros_tuyau.fbx](models/05_chantier/42_gros_tuyau.fbx) |
| 43 | Tas de briques | 3 × 1,5 × 2 | 1892 | Briques | [43_tas_briques.fbx](models/05_chantier/43_tas_briques.fbx) |
| 44 | Tour d'éclairage mobile | 3 × 12 × 3 | 1464 | Remorque, Mat, Projecteurs, Boitiers | [44_tour_eclairage.fbx](models/05_chantier/44_tour_eclairage.fbx) |
| 45 | Camion toupie béton | 7 × 9 × 22 | 3344 | Chassis, Cabine, Vitres, Toupie, Goulotte, Phares, FeuxArriere, Roue_AvG, Roue_AvD, Roue_Av2G, Roue_Av2D, Roue_Ar1G, Roue_Ar1D, Roue_Ar2G, Roue_Ar2D | [45_camion_toupie.fbx](models/05_chantier/45_camion_toupie.fbx) |
| 46 | Grue à tour | 74 × 85 × 4 | 3998 | Mat, PartieTournante, Chariot, Crochet | [46_grue_tour.fbx](models/05_chantier/46_grue_tour.fbx) |
| 47a | Comptoir de boutique 5 | 5 × 3,4 × 1,6 | 528 | Comptoir | [47a_comptoir_boutique_5.fbx](models/06_magasins/47a_comptoir_boutique_5.fbx) |
| 47b | Comptoir de boutique 10 | 10 × 3,4 × 1,6 | 616 | Comptoir | [47b_comptoir_boutique_10.fbx](models/06_magasins/47b_comptoir_boutique_10.fbx) |
| 48 | Caisse enregistreuse | 1,2 × 1 × 1 | 816 | Caisse, Ecran, Tiroir | [48_caisse_enregistreuse.fbx](models/06_magasins/48_caisse_enregistreuse.fbx) |
| 49a | Étagère métal remplie 4 | 4 × 5 × 1,2 | 2248 | Etagere | [49a_etagere_metal_4.fbx](models/06_magasins/49a_etagere_metal_4.fbx) |
| 49b | Étagère métal remplie 8 | 8 × 5 × 1,2 | 4032 | Etagere | [49b_etagere_metal_8.fbx](models/06_magasins/49b_etagere_metal_8.fbx) |
| 50 | Frigo vitré à canettes | 2,6 × 6 × 1,6 | 1884 | Caisson, Porte, Vitre, Lumiere | [50_frigo_vitre.fbx](models/06_magasins/50_frigo_vitre.fbx) |
| 51 | Plafonnier néon | 3 × 0,2 × 0,8 | 284 | Boitier, Neon | [51_plafonnier_neon.fbx](models/06_magasins/51_plafonnier_neon.fbx) |
| 52 | Tabouret de bar | 1,2 × 2,5 × 1,2 | 384 | Tabouret | [52_tabouret_bar.fbx](models/06_magasins/52_tabouret_bar.fbx) |
| 53 | Chaise en bois | 1,5 × 3,6 × 1,5 | 516 | Chaise | [53_chaise_bois.fbx](models/06_magasins/53_chaise_bois.fbx) |
| 54 | Table bistrot ronde | 2,6 × 2,8 × 2,6 | 436 | Table | [54_table_bistrot.fbx](models/06_magasins/54_table_bistrot.fbx) |
| 55 | Table haute murale | 1,2 × 3,3 × 5 | 440 | Table | [55_table_haute_murale.fbx](models/06_magasins/55_table_haute_murale.fbx) |
| 56 | Plante en pot | 2,2 × 3,3 × 2,2 | 412 | Pot, Feuilles | [56_plante_pot.fbx](models/06_magasins/56_plante_pot.fbx) |
| 57 | Comptoir de bar en bois | 10 × 3,4 × 1,6 | 552 | Comptoir, ReposePieds | [57_comptoir_bar.fbx](models/06_magasins/57_comptoir_bar.fbx) |
| 58 | Étagère murale à bouteilles | 12 × 2 × 0,8 | 2488 | Etagere, Bouteilles | [58_etagere_bouteilles.fbx](models/06_magasins/58_etagere_bouteilles.fbx) |
| 59 | Miroir de bar | 12 × 1,6 × 0,1 | 356 | Cadre, Miroir | [59_miroir_bar.fbx](models/06_magasins/59_miroir_bar.fbx) |
| 60 | Cible de fléchettes | 1,8 × 1,8 × 0,2 | 880 | Cible, Flechettes | [60_cible_flechettes.fbx](models/06_magasins/60_cible_flechettes.fbx) |
| 61 | TV murale des courses | 4 × 2,4 × 0,3 | 144 | TV, Ecran | [61_tv_courses.fbx](models/06_magasins/61_tv_courses.fbx) |
| 62 | Billard avec queue et boules | 4 × 3 × 7 | 2192 | Table, Boules, Queue | [62_billard.fbx](models/06_magasins/62_billard.fbx) |
| 63 | Jukebox rétro | 2,5 × 4,5 × 1,5 | 1108 | Caisson, Vitre, Neon | [63_jukebox.fbx](models/06_magasins/63_jukebox.fbx) |
| 64 | Machine à café pro | 2 × 1,6 × 1 | 708 | Machine, Voyants | [64_machine_cafe.fbx](models/06_magasins/64_machine_cafe.fbx) |
| 65 | Vitrine à pâtisseries avec croissants | 2,6 × 1,2 × 1 | 1008 | Vitrine, Vitre | [65_vitrine_patisseries.fbx](models/06_magasins/65_vitrine_patisseries.fbx) |
| 66 | Ardoise menu | 7 × 2,6 × 0,2 | 248 | Cadre, Ardoise | [66_ardoise_menu.fbx](models/06_magasins/66_ardoise_menu.fbx) |
| 67 | Comptoir inox avec vitre anti-postillons | 9 × 4,7 × 1,6 | 544 | Comptoir, Vitre | [67_comptoir_inox.fbx](models/06_magasins/67_comptoir_inox.fbx) |
| 68 | Bacs à garnitures | 4,4 × 0,3 × 0,8 | 1268 | Bacs, Garnitures | [68_bacs_garnitures.fbx](models/06_magasins/68_bacs_garnitures.fbx) |
| 69 | Broche à kebab | 1,6 × 3,6 × 1,6 | 620 | Socle, Viande, Grill | [69_broche_kebab.fbx](models/06_magasins/69_broche_kebab.fbx) |
| 70 | Friteuse pro | 1,8 × 3,2 × 1,2 | 396 | Friteuse, Huile, Paniers | [70_friteuse_pro.fbx](models/06_magasins/70_friteuse_pro.fbx) |
| 71 | Four à pizza en briques | 3,2 × 3,6 × 2 | 684 | Four, Feu | [71_four_pizza.fbx](models/06_magasins/71_four_pizza.fbx) |
| 72 | Panneau menu lumineux | 9 × 2,6 × 0,2 | 148 | Cadre, Ecran | [72_panneau_menu_lumineux.fbx](models/06_magasins/72_panneau_menu_lumineux.fbx) |
| 73 | Comptoir de réception | 9 × 3,4 × 1,6 | 564 | Comptoir, Dessus | [73_comptoir_reception.fbx](models/06_magasins/73_comptoir_reception.fbx) |
| 74 | Sonnette de réception | 0,5 × 0,3 × 0,5 | 248 | Sonnette, Bouton | [74_sonnette_reception.fbx](models/06_magasins/74_sonnette_reception.fbx) |
| 75 | Tableau à clés | 4 × 3 × 0,2 | 1940 | Tableau, Cles | [75_tableau_cles.fbx](models/06_magasins/75_tableau_cles.fbx) |
| 76 | Canapé 3 places velours | 2,4 × 2,6 × 6 | 620 | Canape | [76_canape_velours.fbx](models/06_magasins/76_canape_velours.fbx) |
| 77 | Table basse | 2 × 1,4 × 3 | 340 | Table | [77_table_basse.fbx](models/06_magasins/77_table_basse.fbx) |
| 78 | Porte d'ascenseur | 4 × 6,5 × 0,3 | 548 | Encadrement, Indicateur, BoutonAppel, PorteGauche, PorteDroite, PanneauEnPanne | [78_porte_ascenseur.fbx](models/06_magasins/78_porte_ascenseur.fbx) |
| 79 | Valise | 1,5 × 2 × 0,8 | 448 | Valise | [79_valise.fbx](models/06_magasins/79_valise.fbx) |
| 80 | Lustre | 3 × 2 × 3 | 836 | Lustre, Ampoules | [80_lustre.fbx](models/06_magasins/80_lustre.fbx) |
| 81 | Présentoir mural à magazines | 3 × 3,5 × 0,6 | 692 | Presentoir, Magazines | [81_presentoir_magazines.fbx](models/06_magasins/81_presentoir_magazines.fbx) |
| 82 | Croix de pharmacie lumineuse | 2 × 2 × 0,3 | 164 | Support, Croix | [82_croix_pharmacie.fbx](models/06_magasins/82_croix_pharmacie.fbx) |
| 83 | Tableau d'acuité visuelle | 2 × 3 × 0,1 | 216 | Cadre, Tableau | [83_tableau_acuite.fbx](models/06_magasins/83_tableau_acuite.fbx) |
| 84 | Fauteuil de barbier | 1,8 × 4 × 1,8 | 664 | Pied, Siege | [84_fauteuil_barbier.fbx](models/06_magasins/84_fauteuil_barbier.fbx) |
| 85 | Miroir mural avec cadre | 2,4 × 3 × 0,1 | 248 | Cadre, Miroir | [85_miroir_mural.fbx](models/06_magasins/85_miroir_mural.fbx) |
| 86 | Enseigne poteau de barbier | 0,8 × 3 × 0,8 | 1276 | Support, Cylindre, Rayures | [86_enseigne_barbier.fbx](models/06_magasins/86_enseigne_barbier.fbx) |
| 87 | Lave-linge à hublot | 2,2 × 2,6 × 2,2 | 680 | Machine, Voyant, Hublot, VitreHublot | [87_lave_linge.fbx](models/06_magasins/87_lave_linge.fbx) |
| 88 | Banc d'attente | 1,2 × 1,6 × 5 | 584 | Banc | [88_banc_attente.fbx](models/06_magasins/88_banc_attente.fbx) |
| 89 | Banc de musculation | 4,5 × 3,6 × 4 | 1232 | Banc, Barre, Disques | [89_banc_muscu.fbx](models/06_magasins/89_banc_muscu.fbx) |
| 90 | Tapis de course | 2 × 4,6 × 5 | 392 | Chassis, Ecran, Tapis | [90_tapis_course.fbx](models/06_magasins/90_tapis_course.fbx) |
| 91 | Établi en bois | 1,6 × 3 × 4 | 688 | Etabli, Outils | [91_etabli_bois.fbx](models/06_magasins/91_etabli_bois.fbx) |
| 92 | Panneau perforé avec outils | 8 × 3 × 0,3 | 1848 | Panneau, Outils | [92_panneau_perfore.fbx](models/06_magasins/92_panneau_perfore.fbx) |
| 93 | Portant à vêtements | 1 × 4,5 × 5 | 2056 | Portant, Vetements | [93_portant_vetements.fbx](models/06_magasins/93_portant_vetements.fbx) |
| 94 | Seau en métal avec bouquet | 1,2 × 2,2 × 1,2 | 1044 | Seau, Bouquet | [94_seau_bouquet.fbx](models/06_magasins/94_seau_bouquet.fbx) |
| 95 | Comptoir à barreaux | 8 × 6,4 × 1,6 | 1048 | Comptoir, Barreaux, Guichet | [95_comptoir_barreaux.fbx](models/06_magasins/95_comptoir_barreaux.fbx) |
<!-- /table -->
