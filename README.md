# Le Livre du Ciel — v2.18.1-R1B

Application PWA de lecture des 36 tomes du *Livre du Ciel* de Luisa Piccarreta.

## État de ce paquet

- **Étape : LDC-GR — réparation d’intégrité hors ligne + réconciliation des gates**
- **Candidat : NON DÉPLOYÉ**
- **Base corrective : v2.18.0-R1B / LDC-G** — SHA-256 `047a41c1d2ff34e61f8a89faee0d7cc7e3aa10195cd78117c7400ba4129f0727`.
- **Autorisation propriétaire : `Do it`** — autorise la réparation LDC-GR; **ne vaut pas** validation utilisateur de LDC-F ni preuve physique PWA/appareil.
- **LDC-F owner/user acceptance : PENDING** — les 10 scénarios d’acceptation doivent encore être exécutés et acceptés explicitement.
- **Corpus : G036-AFLP-R1B-UWR2** — 2 312 entrées · 74 348 paragraphes · 74 348 enregistrements de recherche · 65 107 segments de parole.
- Les fichiers `corpus/` sont protégés et ne sont pas modifiés par LDC-GR.

## Corrections LDC-GR

1. Chaque asset de préparation hors ligne est vérifié **avant mise en cache** par taille attendue + SHA-256 attendu.
2. Un HTTP 200 contenant des octets erronés/tronqués est rejeté et ne peut jamais conduire à `READY`.
3. Le cache hors ligne v18.1 utilise un nouveau namespace; les anciens marqueurs non vérifiés ne sont pas hérités.
4. `READY` est lié à une empreinte immuable du manifeste hors ligne (`content_binding_sha256`) et au SHA-256 de `corpus/manifest.json`.
5. Les réponses mises en cache portent des marqueurs de vérification SHA-256/taille/binding; une entrée sans marqueurs valides est invalidée lors du scan.
6. La liste des fichiers en échec est conservée et affichée dans l’interface hors ligne.
7. Au démarrage, un ancien `READY` IndexedDB n’est plus affiché comme fiable avant réponse corrélée du service worker; absence de réponse => `ERROR`.
8. La métadonnée erronée assimilant `Do ldc G` à l’acceptation LDC-F est corrigée : l’acceptation reste `PENDING` jusqu’à preuve.
9. Les anciens rapports LDC-G sont conservés comme historique `history_ldcg_pre_gr`, pas comme preuve courante.

## Gate LDC-GR

Les réparations statiques/code/package peuvent être auditées ici. Le **PASS complet de LDC-G reste impossible** tant que les preuves suivantes ne sont pas exécutées : acceptation utilisateur LDC-F, smoke appareil hérité A/C, iPhone/iPad/Samsung installés PWA, mode avion/offline reopen/update et live GitHub Pages. LDC-H reste bloqué jusque-là.
