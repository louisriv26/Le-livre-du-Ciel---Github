# Livre du Ciel — PWA v2.4.0

Application de lecture et d'étude du Livre du Ciel de Luisa Piccarreta.

## Corpus
- **36 tomes complets** · 74 476 paragraphes · 2 307 entrées
- **20 552 corrections** appliquées (v3→v7)
- Parole de Jésus rendue inline avec délimitation visuelle
- Corpus version : v7 (15 juin 2026)

## Fonctionnalités
- Lecteur avec Mode Lire (parole inline) / Mode Étudier (provenance + confiance)
- Rendu inline des paroles de Jésus et Marie (bordure gauche dorée/violette)
- Recherche L1–L3 sur 36 tomes avec précharge en arrière-plan
- Collections : créer, réordonner, annoter, exporter
- Autour de ce passage (3 sections)
- Mon Espace : notes, surlignages, favoris, collections
- Mode jour/nuit · taille de texte · aide in-app
- Badge version visible · vérificateur de mise à jour
- PWA offline · aucun compte requis

## Architecture
```
index.html              — app shell (120 Ko)
sw.js                   — service worker (cache key: ldc-v2.4.0)
manifest.json           — PWA manifest
corpus/manifest.json    — version v7, 36 tomes, speech_resynced: true
corpus/volume_NN.json   — entrées (métadonnées)
corpus/paragraphs_NN.json — texte d'affichage
corpus/search_NN.json   — index de recherche normalisé
corpus/speakers_NN.json — segments de parole resyncs (offsets utilisés en rendu)
icons/                  — 512px, 192px, 32px, apple-touch-icon
.github/workflows/deploy.yml — GitHub Actions → GitHub Pages
```

## Vérifier la version déployée
La version est visible en permanence dans la barre d'accueil (ex. `v2.4.0`).
Taper le bouton **?** affiche aussi le badge version complet.

## Mise à jour
Quand une nouvelle version est déployée, une bannière apparaît en haut de l'accueil.
Appuyez dessus pour mettre à jour.

## Corpus — note
`human_review_flags_v7.csv` contient 1 passage à vérifier :
LDC.T02.1899-10-28.E001.P007 — `séchés` vs `essuyés`

## Constitution du projet
Voir `Project_Constitution_v1.0.docx`.
