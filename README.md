# Livre du Ciel — PWA v2.1.0

Application de lecture et d'étude du Livre du Ciel de Luisa Piccarreta.

## Corpus
- **36 tomes complets** · 74 476 paragraphes · 2 307 entrées
- **20 552 corrections** appliquées (v3→v7)
- Texte revalidé · pronoms divins capitalisés · parole resynchronisée
- Corpus version : v7 (15 juin 2026)

## Fonctionnalités
- Lecteur avec Mode Lire / Mode Étudier
- Recherche L1–L3 (exacte + normalisée + 13 familles thématiques)
- Collections : créer, réordonner, annoter, exporter
- Autour de ce passage (3 sections)
- Mon Espace : notes, surlignages, favoris, collections
- Mode jour/nuit · taille de texte · aide in-app
- PWA offline-first · aucun compte requis

## Architecture
```
index.html          — app shell (108 Ko)
sw.js               — service worker (cache key: ldc-v2.1.0)
manifest.json       — PWA manifest
corpus/
  manifest.json     — version v7, 36 tomes
  volume_NN.json    — entrées (métadonnées)
  paragraphs_NN.json — texte d'affichage
  search_NN.json    — index de recherche normalisé
  speakers_NN.json  — segments de parole resynchronisés
icons/              — 512px, 192px, 32px, apple-touch-icon
.github/workflows/  — deploy.yml → GitHub Pages
```

## Déploiement
Push sur `main` → GitHub Actions → GitHub Pages (automatique).

## Version
Pour vérifier la version déployée : ouvrir l'app, taper le bouton **?**.
Le badge `v2.1.0 · 2026-06-15` doit apparaître.

## Corpus — note pour développeur
`human_review_flags_v7.csv` contient 1 passage à vérifier par un théologien :
- LDC.T02.1899-10-28.E001.P007 : `séchés` vs `essuyés` (allusion à Marie-Madeleine)

## Constitution du projet
Voir `Project_Constitution_v1.0.docx`.
