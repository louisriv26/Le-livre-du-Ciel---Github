# Livre du Ciel — PWA v2.11.0-R1B

Application de lecture et d'étude du Livre du Ciel de Luisa Piccarreta.

> **Statut : candidat non déployé.** Cette version n'a pas encore été publiée ni
> validée sur appareil physique. Voir « Statut des tests ».

## Corpus
Corpus gouvernant : `G036-AFLP-R1B-UWR2`

- **36 tomes complets** · 74 348 paragraphes · 2 312 entrées
- Couche parole : **65 107 segments** — Jésus 59 007 · Marie 0 · Mary 226 · Luisa 4 556
- Couche parole : 0 offset hors-limites · 0 chevauchement (validation **structurelle**)
- Index de recherche : 74 348 enregistrements, `norm` vérifié à chaque build

> **Portée de la vérification.** La couche « parole » a été construite et corrigée par
> campagnes successives puis auditée sur un sous-ensemble à risque (relabels, Marie,
> lead-ins narratifs). La validation automatique couvre l'intégrité **structurelle**
> (offsets, chevauchements, alignement) — **pas** une vérification sémantique complète
> locuteur-par-locuteur ni une collation intégrale contre les sources. Elle ne doit pas
> être décrite comme « entièrement vérifiée ».

## Couches d'affichage dérivées
Le texte canonique n'est **jamais** modifié. Deux couches dérivées gouvernent le rendu :

- `corpus/flow_NN.json` — **flux d'affichage** : 11 498 groupes, 35 085 membres.
  23 530 jonctions de tirets héritées + 57 continuations sans tiret revues.
  Chaque paragraphe conserve son identifiant, son texte, son empreinte et ses offsets.
- `corpus/display_NN.json` — **projection typographique** (handoff structural-dash
  RECHECKED v2) : 25 193 opérations. Un marqueur de mise en page supprimé garde sa
  plage canonique `[début, fin)`, donc surlignages, notes et signets restent ancrés.

Rendu de la parole : 57 966 séquences locales au paragraphe, dont 20 467 liées
au-delà d'une frontière de fragment → **37 499 séquences affichées**.

## Fonctionnalités
- Mode Prier : parole de Jésus en italique brun foncé + bordure or · sans label
- Mode Étudier : label « Jésus » (or) / « Marie » (violet)
- Lecture continue : les fragments d'une même phrase s'affichent ensemble, sans
  fusion destructive du DOM et sans perte d'identité de paragraphe
- Recherche L1–L3 (BM25) sur 36 tomes avec précharge en arrière-plan
- Recherche vectorielle : **optionnelle**, activée par l'utilisateur
- Collections · Autour de ce passage · Mon Espace (notes, surlignages, favoris)
- Surlignage : ancré sur offsets canoniques ; une sélection qui traverse plusieurs
  paragraphes est stockée en **parties groupées** (`highlight_group_id`)
- Migration des données utilisateur : versionnée, idempotente, non destructive
- Mode jour/nuit · taille de texte · aide in-app · PWA hors-ligne · aucun compte

## Statut des tests
- ⚠ Tests Samsung et iPhone **pas encore effectués** — bloquants pour distribution publique
- ⚠ Paquet **non déployé** — aucune validation appareil / mise à jour / hors-ligne
- ✓ Tests navigateur desktop : validés
- ✓ Intégrité du texte visible : 74 348/74 348 paragraphes, 0 écart
- ✓ Matrice d'interaction (§11.6) : 11/11
- ✓ Migration données utilisateur : 5 classes de fixtures, idempotente

## Architecture
```
index.html              — app shell
sw.js                   — service worker (cache key: ldc-v2.5.57)
manifest.json           — PWA manifest (#1A2A4A theme)
corpus/manifest.json    — version v10, 36 tomes
corpus/volume_NN.json   — entrées (métadonnées)
corpus/paragraphs_NN.json — texte d'affichage
corpus/search_NN.json   — index de recherche normalisé
corpus/speakers_NN.json — segments de parole audités v10
icons/                  — 512px, 192px, 32px, apple-touch-icon
.github/workflows/deploy.yml — GitHub Actions → GitHub Pages
```

## Vérifier la version déployée
La version est visible en permanence dans la barre d'accueil (ex. `v2.5.52`).
Le bouton **?** affiche le badge version complet.

## Mise à jour
Quand une nouvelle version est déployée, une bannière apparaît en haut de l'accueil.
Appuyez dessus pour mettre à jour.

## Corpus — note
`human_review_flags_v9.csv` contient 1 passage à vérifier :
LDC.T02.1899-10-28.E001.P007 — `séchés` vs `essuyés`

## Constitution du projet
Voir `Project_Constitution_v1.0.docx` et `Continuite_Projet_Luisa_v6.0.docx`.
