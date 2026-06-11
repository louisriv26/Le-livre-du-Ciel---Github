# Livre du Ciel — PWA

Application de lecture du Livre du Ciel de Luisa Piccarreta.

## Tomes disponibles
Tomes 1–6 validés et inclus dans ce build.

## Architecture
- `index.html` — app shell complet
- `sw.js` — service worker (offline first)
- `manifest.json` — PWA manifest
- `corpus/` — données corpus (JSON par tome)
  - `manifest.json` — versions et tomes disponibles
  - `volume_NN.json` — entrées par tome
  - `paragraphs_NN.json` — paragraphes de lecture
  - `search_NN.json` — index de recherche

## Déploiement
Push sur `main` → GitHub Actions → GitHub Pages.

## Constitution du projet
Voir `Project_Constitution_v1.0.docx`.
