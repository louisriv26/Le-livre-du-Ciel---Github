# Le Livre du Ciel — v2.19.12-R1B

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

Les **224 fichiers `corpus/**` du paquet actuel restent byte-identical par rapport à v2.19.11**. Les 220 actifs hérités de GR9 constituent le noyau historique ; les 4 fichiers de supplément ajoutés ensuite restent eux aussi inchangés. Aucun texte, ID, ordre, offset de locuteur, recherche ou métadonnée canonique R1B n'est réécrit par ce recheck.

Backbone : **2 312 entrées · 74 348 paragraphes · 74 348 recherches · 65 107 segments sémantiques**.  
Vue enrichie : **2 324 entrées visibles · 74 427 paragraphes visibles**, dont 79 paragraphes `LDCSUP`.

### Recherche

La recherche **métadonnées + lexicale/BM25** couvre le backbone et les compléments. Le sous-système vectoriel/embeddings dormant a été **retiré du paquet RA3**, y compris les trois artefacts R1B et le chargeur Xenova. `corpus/semantic_index.json` est conservé : il sert au classement lexical/BM25 et thématique, pas aux embeddings. Toute future recherche vectorielle nécessitera une reconstruction complète contre le corpus composite exact ainsi qu’un runtime bundlé ou auto-hébergé, dans une tranche séparément autorisée.

### Hors ligne / PWA

La préparation hors ligne inclut **224 actifs vérifiés** : les 220 actifs hérités et les 4 fichiers du supplément. L'identité de cache, le manifeste hors ligne et son content binding sont versionnés pour v2.19.12-R1B.

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

Les **224 fichiers `corpus/**` restent byte-identical** à v2.19.11. Aucun texte dévotionnel, ID de paragraphe, offset de locuteur, index de recherche, complément, schéma utilisateur ou donnée personnelle n'est modifié. Une validation physique des octets v2.19.12 exacts reste requise sur iPhone/iPad/Samsung et pour le cycle PWA/live-origin.

## RA4B four-pass corrective recheck — superseded by RA4C (2026-08-16)

RA4B repart des octets immuables v2.19.10-R1B (SHA-256 `6eb568094178a3c745873792a97ddbf61fe296ef4e26a72fa5d33d16c0617367`). L'audit indépendant a reproduit le build mais a refusé la conclusion globale RA4 sur les frontières de parole. La correction reste strictement dans la couche de présentation : cinq fins de parole directe de Jésus précédemment `inline` créent désormais un nouveau paragraphe visuel pour la narration qui suit ; deux guillemets ouvrants non adjacents sont masqués uniquement lorsque le contexte contient une attribution explicite à Jésus/Marie et aucun guillemet imbriqué ; les deux cas du tome 4 ont conduit à un scan global qui a identifié et corrigé six guillemets fermants séparés de l'offset par de la ponctuation, sans masquer cette ponctuation. Les citations intégrées telles que « Je vous épouserai dans la foi » restent inline et les citations imbriquées/reportées restent visibles.

Le contraste du toast sombre validé en RA4 est conservé (12,17:1 en mode sombre ; 13,21:1 en mode clair). Aucun fichier `corpus/**`, aucun ID, aucun offset de locuteur, aucune donnée de recherche, aucun schéma utilisateur et aucune donnée personnelle ne change. Une validation physique des octets v2.19.11 exacts reste requise sur iPhone/iPad/Samsung et pour le cycle PWA/live-origin.

## RA4 initial speech-boundary / dark-toast hardening — superseded by RA4B recheck (2026-08-15)

RA4 a corrigé le contraste des messages temporaires et une grande partie des guillemets/retours de narration sans modifier le corpus. Le recheck RA4B du 16 août a toutefois démontré que la couverture globale RA4 était incomplète : cinq fins de tours de parole directs encore classées `inline` laissaient la narration suivante sur la même ligne, deux guillemets ouvrants restaient visibles lorsque l'offset validé commençait après un court préfixe lexical explicitement attribué à Jésus, et deux cas du tome 4 ont révélé une classe de guillemets fermants restant visibles lorsque l'offset s'arrêtait avant la ponctuation terminale ; le scan global RA4B en a ensuite identifié six relevant de la même correction de présentation. Les preuves RA4 de type « 829/829 » ne couvraient que les cas déjà classés en bloc et ne constituaient donc pas une preuve exhaustive du défaut signalé. RA4B supersède cette conclusion.

Le correctif de contraste RA4 est conservé. Les 224 fichiers `corpus/**`, les IDs et les offsets de locuteur restent inchangés.

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
