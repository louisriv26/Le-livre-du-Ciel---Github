# Le Livre du Ciel — v2.19.7-R1B

## LDC-AFLP-SUP-T1-RA2C-INTERACTION-HARMONISATION — fermeture de l’alignement interactionnel

**Statut du ZIP :** `CANDIDAT / FINAL REOPEN EXTERNE REQUIS / NOT_DEPLOYED`  
**Lignée source originale :** v2.18.9-R1B / GR9, SHA-256 `cc0759f1c635b0b2be8d58bd2c97305b11168e5b3ab90d194f757340f14c5f90`  
**Baseline immédiate du correctif RA2A :** v2.19.4-R1B, SHA-256 `02f546409fa2f46c340db8b4d393c5ab4028f81d1e3effdf894f2f34895c6f86`  
**Backbone AFLP immuable :** `G036-AFLP-R1B-UWR2`  
**Vue composite :** `G036-AFLP-R1B-SUP-T1`

### Portée éditoriale

Translation Set 1 ajoute, dans une couche `LDCSUP` séparée du backbone AFLP :

- **2 compléments internes** : Tome 4 — 30 janvier 1901 ; Tome 5 — 29 octobre 1903 ;
- **12 entrées datées complètes** absentes de l'édition AFLP ;
- **79 paragraphes français** ;
- **79 enregistrements de recherche** ;
- **52 segments de locuteur**.

Les traductions françaises ont été établies directement à partir d'**IT-PM**. Queen et Hugh Owen sont utilisés uniquement comme traductions comparatives. Chaque complément porte une provenance structurée et un badge visible **`COMPLÉMENT · IT-PM`**.

### Contrat de lecture

- **ENRICHI** est la vue par défaut : corpus ALIGNÉ + compléments approuvés.
- **ALIGNÉ** affiche les 2 312 entrées du corpus français aligné sur le périmètre de l’édition AFLP de référence. Le terme « aligné » décrit le périmètre éditorial des textes/dates ; il ne signifie pas que chaque formulation française reproduit nécessairement mot pour mot la traduction imprimée AFLP.
- **COMPLÉMENT** isole les 14 compléments approuvés : 12 entrées complètes + 2 compléments internes, traduits directement depuis IT-PM, avec ancrage explicite et action « Voir dans le contexte ».
- Le sélecteur **ALIGNÉ · COMPLÉMENT · ENRICHI** est visible dans Bibliothèque, dans chaque Tome et dans le lecteur ; le choix est mémorisé.
- Le style du locuteur reste indépendant de la provenance : Jésus garde le style Jésus, Luisa le style Luisa, etc.
- La provenance est indiquée au niveau du conteneur/badge afin de ne pas entrer en conflit avec les surlignages personnels.
- Les favoris, notes, surlignages et états de lecture existants restent attachés à leurs identifiants stables ; les compléments ont leur propre identité `LDCSUP` et leur propre version de traduction.

### Protection du backbone

Les **220 actifs corpus/offline hérités de GR9 restent byte-identical**. Aucun texte, ID, ordre, offset de locuteur, recherche ou métadonnée canonique R1B n'est réécrit par Translation Set 1. Les compléments sont chargés dynamiquement dans une couche séparée.

Backbone : **2 312 entrées · 74 348 paragraphes · 74 348 recherches · 65 107 segments sémantiques**.  
Vue enrichie : **2 324 entrées visibles · 74 427 paragraphes visibles**, dont 79 paragraphes `LDCSUP`.

### Recherche

La recherche lexicale/BM25 couvre le backbone et les compléments. Les embeddings R1B de 74 348 paragraphes sont conservés comme artefact historique du backbone mais **la recherche vectorielle est désactivée dans cette génération composite**, car ces vecteurs ne couvrent pas les 79 nouveaux paragraphes. Elle ne doit pas être réactivée sans reconstruction et validation contre le texte composite exact.

### Hors ligne / PWA

La préparation hors ligne inclut les 220 actifs hérités et les 4 fichiers du supplément. L'identité de cache, le manifeste hors ligne et son content binding sont versionnés pour v2.19.7-R1B.

### Limites de décision

Translation Set 1 améliore la complétude par rapport à AFLP, mais **ne certifie pas la complétude absolue des 36 tomes**. Les autres différences propositionnelles ou généalogiques restent hors de cette tranche.

Les validations physiques restent distinctes : iPhone/iPad/Samsung, PWA installée, mode avion, cycle de mise à jour, lecteur d'écran et origine GitHub Pages exacte ne peuvent être déclarés PASS sans tests réels sur ce paquet exact.

### Baseline UX préservée

La ligne GR9 reste la base fonctionnelle : surlignage aligné avec 24 Heures, continuité visuelle du locuteur extérieur, favoris avec cœur dans le répertoire de Tome, statut explicite `Lu`, navigation contextuelle, mode clair/sombre, mise à jour PWA et intégrité offline. Le détail historique demeure dans `ldc-state.md`; il n'est pas dupliqué dans ce README de déploiement.


## RA1 deep re-audit repair (2026-08-14)

A four-pass audit of the written v2.19.0 ZIP found and corrected three runtime/data issues that the earlier static suite had missed: (1) six inherited lexical/BM25 helper functions were accidentally deleted by the v2.19.0 vector-disable patch, which could make body search fail at runtime; (2) enriched `searchMetadataIndex` retained the backbone paragraph count and changed `volume_counts` object values into numbers; and (3) public diagnostics referenced the undefined `metadataSearchIndex` variable. The re-audit also replaces the prior key-claim-only report check with exhaustive active-report line/row reconciliation and exact shipped-function extraction tests. At the RA1 stage, the R1B backbone and all 14 Translation Set 1 texts remained unchanged. The RA2 section below supersedes that translation-freeze statement for exactly two source-controlled amendments; the R1B backbone remains unchanged.


## RA2 deep recheck corrections (2026-08-14)

A fresh audit of the written RA1 ZIP found three classes not covered by the prior suite: (1) shared/deep links and Mon Espace targets pointing to an inline `LDCSUP` paragraph could fail when the saved reading mode was `AFLP uniquement`; complete-supplement deep links could also fail before `openEntry()` had a chance to enable enriched mode; (2) two Translation Set 1 items required source-controlled amendment — Tome 6, 5 May 1905 heading restored to the masculine `figlio` wording of IT-PM, and Tome 14, 9 September 1922 restored the human will as grammatical agent in the sentence corroborated by both Queen and Hugh Owen; (3) the four core supplement bootstrap JSON files are now in the service-worker shell as well as the verified full-offline manifest, so the enriched app can bootstrap offline without depending on an opportunistic runtime-cache fill. Original R1B files remain untouched.



## RA2 strict three-source execution

Le correctif RA2A courant est reconstruit déterministiquement depuis le ZIP exact v2.19.4-R1B (SHA-256 `02f546409fa2f46c340db8b4d393c5ab4028f81d1e3effdf894f2f34895c6f86`). La lignée éditoriale de Translation Set 1 remonte à RA1/v2.19.1 et à GR9, mais ces versions ne sont pas l'entrée directe du build RA2A. Les valeurs internes du mode de source sont `aflp`, `additions` et `enriched`. À l’étape RA2, les anciens libellés utilisateur étaient AFLP, AJOUTS et ENRICHI ; ils sont historiques et sont remplacés dans RA2B par ALIGNÉ, COMPLÉMENT et ENRICHI. Deux amendements de fidélité de Translation Set 1 avaient été revalidés avant l'intégration RA2.


## RA2A deep four-pass repair (2026-08-14)

A new independent audit of the written v2.19.4 package found release-evidence and runtime edge-case defects not covered by the previous exact-function suite. RA2A corrects source-selector accessibility, gives inline supplements their own favourite/read/reading-position identity instead of mutating the AFLP host entry, exposes correct IT-PM provenance in Infos et source and support reports, visibly labels supplement-owned Mon Espace records, keeps Accueil/Parcours actions safe in the internal `additions` mode, and makes date navigation include both inline supplements in that mode. The former AJOUTS user label is historical and superseded by COMPLÉMENT in RA2B. The 14 supplement texts and all inherited R1B corpus files are unchanged.


## RA2B terminology / About update (2026-08-14)

Le correctif RA2B part du ZIP exact v2.19.5-R1B. Il ne modifie aucun fichier `corpus/`, aucune traduction Translation Set 1, aucun ID et aucun schéma de données utilisateur. Il remplace uniquement la terminologie visible des trois vues par **ALIGNÉ · COMPLÉMENT · ENRICHI**, remplace le badge utilisateur `AJOUT · IT-PM` par **`COMPLÉMENT · IT-PM`**, met à jour l'Aide et ajoute un véritable écran **À propos** expliquant la portée de l'alignement AFLP, la provenance IT-PM des 14 compléments, le rôle comparatif de Queen/Hugh Owen, l'absence de revendication de complétude absolue et la conservation locale des données Mon Espace. Les valeurs techniques internes `aflp`, `additions` et `enriched`, ainsi que les noms de fichiers/IDs `LDCSUP`, restent inchangés pour éviter tout risque de migration inutile.


## RA2C interaction harmonisation (2026-08-15)

RA2C part du ZIP exact v2.19.6-R1B (SHA-256 `64872f494449c2be5e54da67e0b14acb8825fe0a5b6cafb7fd78d86348f92638`). Cette tranche est limitée à l'interface : elle fusionne **À propos** dans la fin de **Aide** sous **À propos et sources**, sans réécrire la provenance éditoriale, et réduit la barre contextuelle primaire à **Surligner · Note · Copier · Fermer**. **Partager la référence** et **Copier le lien** restent dans les outils du lecteur ; **Ajouter à une collection** reste une action secondaire propre au Livre du Ciel.

Aucun fichier `corpus/`, aucune traduction Translation Set 1, aucun ID, aucun segment de locuteur, aucun index de recherche, aucun schéma de données utilisateur et aucun comportement de sélection Android/iPhone/iPad n'est modifié par RA2C. La palette reste **Jaune · Bleu · Vert · Violet · Rose**. Les validations physiques iPhone/iPad/Samsung, PWA installée, mode avion, origine GitHub Pages exacte et lecteurs d'écran restent externes à cette tranche.
