# Le Livre du Ciel — v2.18.3-R1B

Application PWA de lecture des 36 tomes du *Livre du Ciel* de Luisa Piccarreta.

## État de ce paquet

- **Étape : LDC-GR3 — stabilisation du surlignage navigateur/iPhone + clarification Bibliothèque, sur la base LDC-GR2**
- **Candidat : NON DÉPLOYÉ**
- **Base corrective : v2.18.1-R1B / LDC-GR** — SHA-256 `0a5c100012e4f3ba4592fc1b44ee2a7f4dfcfa6109561be928e5686b2d9ed3f3`.
- **Autorisation propriétaire : `Do it`** — autorise la réparation LDC-GR; **ne vaut pas** validation utilisateur de LDC-F ni preuve physique PWA/appareil.
- **LDC-F owner/user acceptance : PENDING** — les 10 scénarios d’acceptation doivent encore être exécutés et acceptés explicitement.
- **Corpus : G036-AFLP-R1B-UWR2** — 2 312 entrées · 74 348 paragraphes · 74 348 enregistrements de recherche · 65 107 segments de parole.
- Les fichiers `corpus/` sont protégés et ne sont pas modifiés par LDC-GR.

## Corrections LDC-GR héritées

1. Chaque asset de préparation hors ligne est vérifié **avant mise en cache** par taille attendue + SHA-256 attendu.
2. Un HTTP 200 contenant des octets erronés/tronqués est rejeté et ne peut jamais conduire à `READY`.
3. La lignée LDC-GR utilise un namespace hors ligne versionné; les anciens marqueurs non vérifiés ne sont pas hérités.
4. `READY` est lié à une empreinte immuable du manifeste hors ligne (`content_binding_sha256`) et au SHA-256 de `corpus/manifest.json`.
5. Les réponses mises en cache portent des marqueurs de vérification SHA-256/taille/binding; une entrée sans marqueurs valides est invalidée lors du scan.
6. La liste des fichiers en échec est conservée et affichée dans l’interface hors ligne.
7. Au démarrage, un ancien `READY` IndexedDB n’est plus affiché comme fiable avant réponse corrélée du service worker; absence de réponse => `ERROR`.
8. La métadonnée erronée assimilant `Do ldc G` à l’acceptation LDC-F est corrigée : l’acceptation reste `PENDING` jusqu’à preuve.
9. Les anciens rapports LDC-G sont conservés comme historique `history_ldcg_pre_gr`, pas comme preuve courante.

## Gate LDC-GR

Les réparations statiques/code/package peuvent être auditées ici. Le **PASS complet de LDC-G reste impossible** tant que les preuves suivantes ne sont pas exécutées : acceptation utilisateur LDC-F, smoke appareil hérité A/C, iPhone/iPad/Samsung installés PWA, mode avion/offline reopen/update et live GitHub Pages. LDC-H reste bloqué jusque-là.

## Corrections LDC-GR2 — retours d’acceptation propriétaire du 12 août 2026

1. Le sélecteur d’édition d’un surlignage utilise exactement la palette utilisateur courante : **Or · Jaune · Bleu · Vert**. Violet/Rose restent lisibles/importables uniquement pour compatibilité avec d’anciennes données.
2. Le jaune dispose désormais d’un rendu explicite clair/sombre; il ne dépend plus du jaune par défaut du navigateur.
3. Le favori d’une entrée datée reste un favori d’entrée à ID stable. Un **cœur visible dans le lecteur** se remplit lorsqu’il est actif; la même entrée apparaît dans **Mon Espace → Favoris**.
4. La lecture n’est plus déclarée automatiquement à l’ouverture. Le statut **Lu** est une action explicite en bas du lecteur, entre Précédente et Suivante.
5. Les anciens enregistrements « lecture » créés automatiquement sont conservés dans les sauvegardes mais ne sont pas comptés comme « Lu » tant que l’utilisateur ne confirme pas explicitement.
6. Dans un Tome, une entrée non lue est plus marquée typographiquement; une entrée lue est atténuée et porte une coche explicite.
7. Le petit point qui signalait « contient des paroles de Jésus » dans la liste des entrées est retiré : il était ambigu avec la progression de lecture.
8. Les cartes de Tome affichent uniquement le nombre d’entrées (ex. **184 entrées**) et plus le nombre de paragraphes.

**Acceptation propriétaire : PENDING RETEST.** Ces corrections répondent aux constats de test mais ne constituent pas elles-mêmes l’acceptation finale LDC-F/G ni la preuve appareil/PWA.

## Corrections LDC-GR3 — stabilité du surlignage et Bibliothèque

1. Le point vert à droite des cartes de Tome était un ancien indicateur technique « Tome validé ». Comme les 36 Tomes actifs sont validés, il n’apportait plus d’information et pouvait être confondu avec la lecture : il est supprimé de la Bibliothèque.
2. Une sélection texte n’applique plus de contour à tout le paragraphe. L’ancien `outline` sur un `span` multi-ligne produisait sur iPhone plusieurs rectangles autour des lignes voisines. Le contour reste réservé à l’activation volontaire d’un paragraphe entier.
3. Les deux extrémités d’une sélection doivent maintenant appartenir à de vrais fragments canoniques du lecteur. Une sélection qui déborde hors du lecteur est rejetée au lieu d’être « accrochée » à un fragment éloigné, ce qui pouvait transformer une petite sélection en plage très large sur navigateur.
4. Le clic généré juste après un glisser-sélection sur ordinateur n’est plus réinterprété comme activation du paragraphe entier.
5. Sur iPhone/iPad, l’app mémorise les offsets canoniques puis libère la sélection native avant d’ouvrir la palette. Elle ne recrée plus le `Range` avec `addRange()`, ce qui pouvait provoquer des rectangles de sélection et un auto-scroll Safari.
6. Ajouter, recolorer ou supprimer un surlignage ne reconstruit plus toute l’entrée. Le DOM concerné est mis à jour localement. Les marques ont `padding:0`, afin de ne pas modifier la mise en ligne.
7. Le `scrollTop` précédant la palette est conservé et réappliqué après le dessin local pour neutraliser un éventuel auto-scroll différé de Safari.

Aucun texte canonique, ID, offset de parole, corpus, index de recherche ou donnée utilisateur n’est modifié par cette réparation.
