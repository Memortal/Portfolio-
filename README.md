# MEMO Studio Portfolio — Competition-Ready Selected Work

**Website:** https://memortal.github.io/Portfolio-/

A project-based portfolio featuring 160 reviewed images of sculpture, architectural installations, fabrication, built interiors and computational design. The strongest public-art and fabrication precedents are shown first.

## Highlighted projects

1. Aluminum Head — Faceted Metal Sculpture
2. MAK Studio — Thermoformed Corian Fin Wall
3. Austin Tessellated Installation
4. Interactive Outdoor Public Art
5. Perforated Metal Portrait Artwork
6. MAK Studio — CNC Patterned Feature Wall
7. Parametric Screens, Metal Mesh & Light

Other collections cover modular planters, DesignHive / Inventure, timber ceilings, Lotus Flower, architectural presentations, and computational research.

**Each project has image ordering and contextual notes** in `data/projects.json`. The entire photo catalog with original Wix links and group associations is in `data/media-manifest.json`.

## Images, privacy and ownership

The repository contains optimized web copies in `assets/images/portfolio/`. It does **not** contain full-resolution originals. Those remain on Wix and should be independently backed up in private storage.

The public branch and current manifest exclude unrelated Wix-site material, Automated Master Plan, personal photographs, images featuring identifiable real people where present, obvious AI-generated artwork and old résumé scans. No video files are part of the public gallery. This does not rewrite old Git history; images deleted in a commit may remain recoverable from prior commits until the repository history is rewritten.

Historic studio work is collaborative. Exact project credits, owner participation, client confidentiality and permission to publish photography need to be verified. Visual photo-grouping is best-effort, not definitive project attribution.

## Publishing

The portfolio is built from `index.html` and the catalog JSON. GitHub Pages publishes from the repository main branch. The import script is deliberately **manual-only** and uses the curated manifest, so it cannot automatically re-add media removed from the current catalog.

## Editing a project

Change the project's `title`, `summary`, `competitionFit`, `featured` or `priority` in `data/projects.json`. Change the images' `projectId` and `displayOrder` in `data/media-manifest.json`.
