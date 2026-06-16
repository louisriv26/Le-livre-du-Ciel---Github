# Livre du Ciel — PWA v2.5.9

Application de lecture et d'étude du Livre du Ciel de Luisa Piccarreta.

## Corpus
- **36 tomes complets** · 74 476 paragraphes · 2 307 entrées
- **20 554 corrections** appliquées (v3→v8)
- Parole de Jésus rendue inline — 52 205 segments visibles dans les 36 tomes
- Parole de Marie rendue inline — 154 segments visibles
- Corpus version : v9 (16 juin 2026)
- Couche parole auditée : 0 segment invalide · 0 chevauchement

## Fonctionnalités
- Mode Prier : parole de Jésus en italique brun foncé + bordure or · sans label
- Mode Étudier : label « Jésus » (or) / « Marie » (violet) · confiance medium affichée
- Listes à tirets : 3 passes (clusters, continuation, énumérations embarquées)
- Recherche L1–L3 sur 36 tomes avec précharge en arrière-plan
- Recherche : garde stopwords (résultat vide + message si requête trop courte)
- Collections : créer, réordonner, annoter, exporter
- Autour de ce passage (3 sections)
- Mon Espace : notes, surlignages (avec offsets), favoris, collections
- Surlignage : stocke start_char, end_char, occurrence_index, para_fingerprint
- Notes : stockent volume, titre d'entrée, date, para_fingerprint
- Mode jour/nuit · taille de texte · aide in-app
- Badge version visible · vérificateur de mise à jour
- PWA offline · aucun compte requis

## Statut des tests
- ⚠ Tests Samsung et iPhone **pas encore effectués** — bloquants pour distribution publique
- ✓ Tests navigateur desktop : validés
- ✓ Couche parole corpus v9 : auditée et validée

## Architecture
```
index.html              — app shell
sw.js                   — service worker (cache key: ldc-v2.5.9)
manifest.json           — PWA manifest (#1A2A4A theme)
corpus/manifest.json    — version v9, 36 tomes
corpus/volume_NN.json   — entrées (métadonnées)
corpus/paragraphs_NN.json — texte d'affichage
corpus/search_NN.json   — index de recherche normalisé
corpus/speakers_NN.json — segments de parole audités v9
icons/                  — 512px, 192px, 32px, apple-touch-icon
.github/workflows/deploy.yml — GitHub Actions → GitHub Pages
```

## Vérifier la version déployée
La version est visible en permanence dans la barre d'accueil (ex. `v2.5.9`).
Le bouton **?** affiche le badge version complet.

## Mise à jour
Quand une nouvelle version est déployée, une bannière apparaît en haut de l'accueil.
Appuyez dessus pour mettre à jour.

## Corpus — note
`human_review_flags_v9.csv` contient 1 passage à vérifier :
LDC.T02.1899-10-28.E001.P007 — `séchés` vs `essuyés`

## Constitution du projet
Voir `Project_Constitution_v1.0.docx` et `Continuite_Projet_Luisa_v6.0.docx`.
