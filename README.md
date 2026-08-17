# Le Livre du Ciel — v2.19.17-R1B

## RA7 — identité finale Collection Luisa / icône Livre du Ciel (2026-08-17)

RA7 part exactement des octets v2.19.16-R1B (`a4b0754f700ed6bdeca62822df9d31dbcff77a9814475896f521c893fa0a8c1c`) et ne modifie aucune donnée de corpus ni logique de lecture. Il remplace l’ancienne identité d’icône par la famille **Collection Luisa v1.0 FINAL_LOCKED** du 15 août 2026, variante `ldc` / `Le Livre du Ciel`.

- Les neuf actifs runtime sont ceux du lock : favicon 16/32/ICO, Apple touch 60/120/180, PWA 192/512 et maskable 512.
- Les trois anciens `icon-source-*.svg`, non référencés, sont supprimés afin qu’aucune ancienne identité graphique ne subsiste dans le paquet de déploiement.
- `index.html`, `manifest.json` et le shell du service worker référencent uniquement les actifs finaux.
- Tous les fichiers `corpus/**` restent byte-identical à v2.19.16. RA6 (Explications Tome 1 + navigation basse véritablement fixe) est préservé.
- L’identité cache/offline est rebondée à v2.19.17-R1B; la liste des 224 actifs du corpus hors ligne reste inchangée.


## RA6 — Explications éditoriales du Tome 1 + vraie navigation basse fixe (2026-08-16)

RA6 part exactement des octets v2.19.15-R1B (`e0fe99803194f4030ae66c240783f7e48374620e2d3e2bab75793242ea7f4231`) et corrige deux défauts de présentation sans modifier le corpus canonique.

- Les 16 enregistrements `LDC.T01.EDITORIAL.EXPLICATIONS.NOTE001..NOTE016` restent conservés byte-for-byte dans le corpus comme matériel éditorial de l’appendice 2021, mais ne sont plus présentés ni comptés comme les 16 premières entrées du Tome 1. La liste commence désormais par `Luisa commence à écrire`.
- Un seul appendice non compté, `Explications éditoriales`, reprend les 16 notes dans leur ordre source. Le scan exact du corps du Tome 1 ne trouve que trois repères numérotés : `(3)` à `LDC.T01.SEC081.P005`, `(4)` à `LDC.T01.SEC082.P001` et `(5)` à `LDC.T01.SEC082.P009`. Des liens sont ajoutés uniquement à ces trois passages. Aucun rattachement contextuel n’est inféré pour les notes 1, 2 et 6–16.
- Les résultats de recherche et anciens liens ciblant une pseudo-entrée éditoriale ouvrent l’appendice correspondant au lieu d’un lecteur normal.
- La barre `Accueil · Tomes · Recherche · Mon Espace` est maintenant réellement fixée au viewport (`position: fixed; left:0; right:0; bottom:0`) avec réserve de hauteur et safe area. Toast, bannière de mise à jour, panneau contextuel et sélecteur de couleur se placent au-dessus.
- Les 224 fichiers `corpus/**`, tous les paragraphes, recherches, locuteurs, display/flow, suppléments, IDs et offsets restent byte-identical à v2.19.15. Le total technique du backbone reste 2 312 records d’entrée, dont 16 records éditoriaux non comptés comme entrées de lecture ; le dénominateur utilisateur ALIGNÉ devient 2 296 entrées de lecture.


## RA5C — réconciliation ciblée des locuteurs (2026-08-16)

RA5C part exactement du ZIP v2.19.14-R1B bloqué (`16b9d2377a0d29db7e81d6b1cff546cd9f14ccee3a47973d0a4a825c25639ee1`). Il ne rouvre pas l’adjudication générale du corpus. Les décisions antérieures fondées sur le français, Queen et Hugh Owen restent l’autorité; RA5C réconcilie uniquement sept paragraphes où les offsets/structures de citation n’étaient plus synchronisés avec le texte canonique final ou avec la projection locuteur extérieur/intérieur.

- Tome 11: trois dérives d’offset après réparations typographiques/de guillemets sont resynchronisées, sans changement d’identité du locuteur.
- Tome 23 E0040 P117-P118: le tour extérieur continu de Jésus est restauré; les citations illustratives internes restent visibles et sont structurellement imbriquées.
- Tome 25 E0035 P040: le mot `seule` est réintégré dans `«Une seule»`; la citation interne reste visible.
- Tome 20 E0012 P073: Jésus reste le locuteur extérieur; la prière complète déjà identifiée par les preuves antérieures comme parole du Fiat personnifié est `PERSONIFIED_VOICE` en profondeur 2 et hérite visuellement de la typographie de Jésus.

Le texte dévotionnel canonique, les IDs, l’ordre, la recherche, les suppléments, les cartes display/flow, `speech_model.js` et les schémas de données utilisateur ne sont pas modifiés. Les seuls fichiers `corpus/**` modifiés par RA5C sont `corpus/manifest.json` et les quatre shards de locuteurs `speakers_11.json`, `speakers_20.json`, `speakers_23.json`, `speakers_25.json`. Le total de segments backbone devient 65 110, dont 59 009 JESUS et 468 PERSONIFIED_VOICE.


## RA5B — recheck profond performance + intégrité des preuves (2026-08-16)

RA5B repart des octets v2.19.13-R1B (`65ade47bf7baa385bf4b5951d91e11780c41a58e341d16253131c084bed15044`). Le recheck a confirmé les trois objectifs RA5 mais a trouvé un défaut de profondeur dans le chargement : les chemins légers (`boot`, Tomes, index de Tome, statistiques/dates) appelaient encore le chargeur de suppléments monolithique et téléchargeaient aussi `supplement_search.json` et `supplement_speakers.json` avant que Recherche ou le lecteur n'en aient besoin. Les chargeurs sont maintenant séparés : registre+manifeste pour la navigation/index, locuteurs uniquement pour le lecteur/filtre locuteur, recherche uniquement pour les recherches textuelles. La sémantique du corpus et des compléments ne change pas.

Le recheck a aussi invalidé l'ancien paquet de preuves RA5 comme preuve autonome : plusieurs scripts dépendaient de chemins absolus `/mnt/data/ra5_exec` et le rebuild déterministe exigeait un ZIP baseline absent du paquet de preuves. Le nouveau paquet de preuves RA5B inclut donc la baseline v2.19.13 et des outils relatifs/portables.

À l’étape historique RA5B, les **224 fichiers `corpus/**`, `speech_model.js`, les IDs, offsets de locuteur, la recherche, les schémas utilisateurs et la palette active Jaune · Bleu · Vert · Violet · Rose restaient inchangés**. La navigation basse persistante et le chargement Tier-1/Tier-2 RA5 sont conservés.

**Blocage découvert par le recheck global des paroles directes.** Le test RA4C/RA5 prouvait que chaque *segment déjà validé comme Jésus/Marie* commençait en bloc, mais il ne prouvait pas que la géométrie de tous les segments couvrait l'intégralité de chaque parole directe. Le recheck a trouvé plusieurs sous-couvertures certaines (notamment T11 24-02-1912 P009, T11 14-10-1914 P004, T11 14-12-1916 P007, T23 E0040 P117-P118 et T25 E0035 P040) ainsi qu'un cas imbriqué T20 E0012 P073 où le discours extérieur de Jésus contient une citation personnifiée du Fiat. Ce dernier cas interdit une expansion automatique sans adjudication source/locuteur. **Historique RA5B : v2.19.14 était donc un candidat correctif de travail, non autorisé au déploiement.** Ce blocage est précisément celui traité par RA5C; les validations physiques/PWA restent séparées et externes.


## RA5 — navigation persistante, ouverture rapide des Tomes et palette unique (2026-08-16)

RA5 part des octets v2.19.12-R1B (`cc1522e9c5480eef558ac1090467a54778bea874937894df26837314bb0108d4`). RA5 avait traité le bandeau principal `Accueil · Tomes · Recherche · Mon Espace` comme structurellement persistant parce qu'il était un sibling flex hors des écrans. RA6 a ensuite démontré que cette preuve était insuffisante : le bandeau n'était pas réellement fixé au viewport et pouvait être déplacé/poussé par la géométrie du shell. La vraie fixation viewport est donc une correction RA6.

L'ouverture d'un Tome utilise maintenant deux niveaux : le fichier léger `volume_NN.json` suffit pour afficher la liste des entrées, tandis que `paragraphs_NN.json`, `speakers_NN.json`, `display_NN.json` et `flow_NN.json` sont chargés séparément lorsque le lecteur en a besoin ou en préchargement non bloquant après l'affichage de la liste. Les index légers peuvent rester en mémoire pour la session ; le LRU de 4 volumes ne concerne que les données lourdes du lecteur. Les métadonnées `volume_NN.json` sont servies cache-first par le service worker versionné, avec repli réseau.

La création et la modification d'un surlignage utilisent désormais une seule palette et le même sélecteur : **Jaune · Bleu · Vert · Violet · Rose** (`yellow · blue · green · purple · pink`). La valeur historique `gold` reste lisible/importable pour compatibilité mais n'est jamais proposée comme sixième choix actif ni écrite par une nouvelle création/recoloration.

À l’étape historique RA5, les **224 fichiers `corpus/**` étaient protégés et inchangés**. RA5 ne modifiait ni le texte, ni les IDs, ni les offsets de locuteur, ni la recherche, ni les schémas de données personnelles, ni le contrat RA4C des paroles directes. Une validation physique des octets v2.19.13 exacts restait requise.


## LDC-AFLP-SUP-T1-RA4C-DIRECT-SPEECH-BLOCK-START-GLOBAL-HARDENING — séparation globale des paroles directes

**Statut embarqué :** candidat non déployé ; la décision finale de release est portée par les audits externes du ZIP immuable et leur decision lock.  
**Lignée source originale :** v2.18.9-R1B / GR9, SHA-256 `cc0759f1c635b0b2be8d58bd2c97305b11168e5b3ab90d194f757340f14c5f90`  
**Baseline immédiate de RA4C :** v2.19.11-R1B, SHA-256 `949ec1e4b5af6f486c096e49fa071868749662d2e6809cd134d932b005a3a992`  
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

À l’étape historique RA4C, les **224 fichiers `corpus/**` du paquet de cette étape restaient byte-identical par rapport à v2.19.11**. Les 220 actifs hérités de GR9 constituaient le noyau historique ; les 4 fichiers de supplément ajoutés ensuite restaient eux aussi inchangés. Aucun texte, ID, ordre, offset de locuteur, recherche ou métadonnée canonique R1B n’était réécrit par ce recheck.

À l’étape historique RA4C, backbone : **2 312 entrées · 74 348 paragraphes · 74 348 recherches · 65 107 segments sémantiques**.  
Vue enrichie : **2 324 entrées visibles · 74 427 paragraphes visibles**, dont 79 paragraphes `LDCSUP`.

### Recherche

La recherche **métadonnées + lexicale/BM25** couvre le backbone et les compléments. Le sous-système vectoriel/embeddings dormant a été **retiré du paquet RA3**, y compris les trois artefacts R1B et le chargeur Xenova. `corpus/semantic_index.json` est conservé : il sert au classement lexical/BM25 et thématique, pas aux embeddings. Toute future recherche vectorielle nécessitera une reconstruction complète contre le corpus composite exact ainsi qu’un runtime bundlé ou auto-hébergé, dans une tranche séparément autorisée.

### Hors ligne / PWA

La préparation hors ligne inclut **224 actifs vérifiés** : les 220 actifs hérités et les 4 fichiers du supplément. L'identité de cache, le manifeste hors ligne et son content binding sont versionnés pour v2.19.16-R1B.

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

Le correctif RA2A historique a été reconstruit déterministiquement depuis le ZIP exact v2.19.4-R1B (SHA-256 `02f546409fa2f46c340db8b4d393c5ab4028f81d1e3effdf894f2f34895c6f86`). La lignée éditoriale de Translation Set 1 remonte à RA1/v2.19.1 et à GR9, mais ces versions ne sont pas l'entrée directe du build RA2A. Les valeurs internes du mode de source sont `aflp`, `additions` et `enriched`. À l’étape RA2, les anciens libellés utilisateur étaient AFLP, AJOUTS et ENRICHI ; ils sont historiques et sont remplacés dans RA2B par ALIGNÉ, COMPLÉMENT et ENRICHI. Deux amendements de fidélité de Translation Set 1 avaient été revalidés avant l'intégration RA2.


## RA2A deep four-pass repair (2026-08-14)

A new independent audit of the written v2.19.4 package found release-evidence and runtime edge-case defects not covered by the previous exact-function suite. RA2A corrects source-selector accessibility, gives inline supplements their own favourite/read/reading-position identity instead of mutating the AFLP host entry, exposes correct IT-PM provenance in Infos et source and support reports, visibly labels supplement-owned Mon Espace records, keeps Accueil/Parcours actions safe in the internal `additions` mode, and makes date navigation include both inline supplements in that mode. The former AJOUTS user label is historical and superseded by COMPLÉMENT in RA2B. The 14 supplement texts and all inherited R1B corpus files are unchanged.


## RA2B terminology / About update (2026-08-14)

Le correctif RA2B part du ZIP exact v2.19.5-R1B. Il ne modifie aucun fichier `corpus/`, aucune traduction Translation Set 1, aucun ID et aucun schéma de données utilisateur. Il remplace uniquement la terminologie visible des trois vues par **ALIGNÉ · COMPLÉMENT · ENRICHI**, remplace le badge utilisateur `AJOUT · IT-PM` par **`COMPLÉMENT · IT-PM`**, met à jour l'Aide et ajoute un véritable écran **À propos** expliquant la portée de l'alignement AFLP, la provenance IT-PM des 14 compléments, le rôle comparatif de Queen/Hugh Owen, l'absence de revendication de complétude absolue et la conservation locale des données Mon Espace. Les valeurs techniques internes `aflp`, `additions` et `enriched`, ainsi que les noms de fichiers/IDs `LDCSUP`, restent inchangés pour éviter tout risque de migration inutile.


## RA4C direct-speech block-start global hardening (2026-08-16)

RA4C repart des octets immuables v2.19.11-R1B (SHA-256 `949ec1e4b5af6f486c096e49fa071868749662d2e6809cd134d932b005a3a992`). Le recheck global a trouvé une classe résiduelle importante : **287 tours de parole validés et visibles de Jésus/Marie restaient `inline`** sous l'heuristique RA4B (**281 Jésus, 6 Marie**). Cela signifiait que certaines paroles directes pouvaient encore commencer sur la même ligne que la narration précédente, même si les reprises de narration après la parole avaient déjà été largement corrigées.

Le contrat lecteur est maintenant explicite et global : **toute parole directe validée et visible de Jésus ou de Marie commence dans un nouveau paragraphe visuel** ; lorsqu'une narration de Luisa reprend après cette parole, elle commence également dans un nouveau paragraphe visuel. Les guillemets extérieurs redondants continuent d'être masqués uniquement dans la présentation ; le texte canonique, les offsets et les IDs restent inchangés. Les citations imbriquées/reportées que la projection attribue à Luisa restent du texte narratif et ne sont pas artificiellement transformées en parole directe.

À l’étape historique RA4C, les **224 fichiers `corpus/**` restaient byte-identical** à v2.19.11. Aucun texte dévotionnel, ID de paragraphe, offset de locuteur, index de recherche, complément, schéma utilisateur ou donnée personnelle n’était modifié. Une validation physique des octets exacts de cette étape restait requise sur iPhone/iPad/Samsung et pour le cycle PWA/live-origin.

## RA4B four-pass corrective recheck — superseded by RA4C (2026-08-16)

RA4B repart des octets immuables v2.19.10-R1B (SHA-256 `6eb568094178a3c745873792a97ddbf61fe296ef4e26a72fa5d33d16c0617367`). L'audit indépendant a reproduit le build mais a refusé la conclusion globale RA4 sur les frontières de parole. La correction reste strictement dans la couche de présentation : cinq fins de parole directe de Jésus précédemment `inline` créent désormais un nouveau paragraphe visuel pour la narration qui suit ; deux guillemets ouvrants non adjacents sont masqués uniquement lorsque le contexte contient une attribution explicite à Jésus/Marie et aucun guillemet imbriqué ; les deux cas du tome 4 ont conduit à un scan global qui a identifié et corrigé six guillemets fermants séparés de l'offset par de la ponctuation, sans masquer cette ponctuation. Les citations intégrées telles que « Je vous épouserai dans la foi » restent inline et les citations imbriquées/reportées restent visibles.

Le contraste du toast sombre validé en RA4 est conservé (12,17:1 en mode sombre ; 13,21:1 en mode clair). Aucun fichier `corpus/**`, aucun ID, aucun offset de locuteur, aucune donnée de recherche, aucun schéma utilisateur et aucune donnée personnelle ne change. À l’étape historique RA4B, une validation physique des octets v2.19.11 était encore requise sur iPhone/iPad/Samsung et pour le cycle PWA/live-origin.

## RA4 initial speech-boundary / dark-toast hardening — superseded by RA4B recheck (2026-08-15)

RA4 a corrigé le contraste des messages temporaires et une grande partie des guillemets/retours de narration sans modifier le corpus. Le recheck RA4B du 16 août a toutefois démontré que la couverture globale RA4 était incomplète : cinq fins de tours de parole directs encore classées `inline` laissaient la narration suivante sur la même ligne, deux guillemets ouvrants restaient visibles lorsque l'offset validé commençait après un court préfixe lexical explicitement attribué à Jésus, et deux cas du tome 4 ont révélé une classe de guillemets fermants restant visibles lorsque l'offset s'arrêtait avant la ponctuation terminale ; le scan global RA4B en a ensuite identifié six relevant de la même correction de présentation. Les preuves RA4 de type « 829/829 » ne couvraient que les cas déjà classés en bloc et ne constituaient donc pas une preuve exhaustive du défaut signalé. RA4B supersède cette conclusion.

Le correctif de contraste RA4 est conservé. À l’étape historique RA4, les 224 fichiers `corpus/**`, les IDs et les offsets de locuteur restaient inchangés.

## RA3 four-pass corrective recheck (2026-08-15)

Ce successeur part du ZIP immuable v2.19.8-R1B (SHA-256 `9ede0aa80a46b76d3201d25d708ab669899cf2e7a5933ddb356874b00e079589`). Le runtime fonctionnel de RA3 est conservé : aucun texte `corpus/**`, aucun index de recherche, aucun complément, aucun schéma de données utilisateur et aucune interaction de lecture n'est modifié.

Le recheck corrige deux défauts de métadonnées embarquées et deux défauts de méthodologie d'audit : (1) `version.json` utilisait le nom `ra3_repairs` pour une ancienne tranche de modes de source, en conflit avec l'actuelle RA3 de retrait vectoriel ; cette provenance est maintenant explicitement historique ; (2) les champs génériques `baseline_candidate_*` pointaient encore vers v2.19.1 et sont rebondés sur la baseline immédiate v2.19.8 ; l'ancien champ générique `baseline_deploy_sha256`, qui contenait en réalité le hash historique GR9, est renommé explicitement ; (3) l'ancien audit « ligne par ligne » propageait simplement le statut du fichier à toutes ses lignes ; (4) l'ancien scanner de contradictions autorisait globalement tout `version.json`. Les audits du présent paquet doivent donc vérifier les claims réellement ligne par ligne et ne plus utiliser ces raccourcis.

Les validations physiques iPhone/iPad/Samsung, PWA installée/mode avion/origine live et VoiceOver/TalkBack/NVDA restent externes et ne sont pas promues par ce recheck machine.

## RA3 vector/embedding retirement (2026-08-15)

RA3 part du ZIP exact v2.19.7-R1B deep-recheck (SHA-256 `e34785817e0e02ec7ad47ea16f6f1c9454cef6d1ea01bfab3685905fcf1aad67`). Cette tranche retire uniquement le chemin de recherche vectorielle dormant : `embeddings_ldc.bin`, `embeddings_ldc_ids.json`, `embeddings_manifest.json`, le chargeur `@xenova/transformers`, les contrôles/états vectoriels et la branche de résultats « Par le sens ». Elle **ne modifie aucun fichier `corpus/`**, aucun texte AFLP/Translation Set 1, aucun ID, aucun segment de locuteur, aucun schéma de données utilisateur et aucune politique de sélection.

La recherche active reste : **métadonnées → lexical/BM25 → résultats**, avec le normaliseur français, les filtres de tomes/locuteur, les compléments et les liens profonds. `corpus/semantic_index.json` reste gouverné et inchangé parce qu’il fournit les IDF/repères thématiques utilisés par BM25 ; son nom ne signifie pas qu’il s’agit d’un embedding. Les anciennes préférences `vector_search_enabled` éventuellement présentes dans IndexedDB sont simplement ignorées ; aucun bump de schéma n’est requis.

Les validations physiques iPhone/iPad/Samsung, PWA installée/mode avion, origine live et VoiceOver/TalkBack/NVDA restent externes et ne sont pas promues par cette tranche machine.

## RA2C interaction harmonisation (2026-08-15)

RA2C part du ZIP exact v2.19.6-R1B (SHA-256 `64872f494449c2be5e54da67e0b14acb8825fe0a5b6cafb7fd78d86348f92638`). Cette tranche est limitée à l'interface : elle fusionne **À propos** dans la fin de **Aide** sous **À propos et sources**, sans réécrire la provenance éditoriale, et réduit la barre contextuelle primaire à **Surligner · Note · Copier · Fermer**. **Partager la référence** et **Copier le lien** restent dans les outils du lecteur ; **Ajouter à une collection** reste une action secondaire propre au Livre du Ciel.

Aucun fichier `corpus/`, aucune traduction Translation Set 1, aucun ID, aucun segment de locuteur, aucun index de recherche, aucun schéma de données utilisateur et aucun comportement de sélection Android/iPhone/iPad n'est modifié par RA2C. La palette reste **Jaune · Bleu · Vert · Violet · Rose**. Les validations physiques iPhone/iPad/Samsung, PWA installée, mode avion, origine GitHub Pages exacte et lecteurs d'écran restent externes à cette tranche.
