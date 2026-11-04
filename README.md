# MEMO Portfolio — Competition-first project gallery

**Public gallery:** https://memortal.github.io/Portfolio-/

This website presents archived photographs and design materials by **project**, with work relevant to public-art competitions at the top.

## Featured project groups

1. **MAK Studio** — fabrication, prototyping and historical presentation boards
2. **Lotus Flower** — sculptural-art image set, with related TADA photographs (relationship to verify)
3. **DesignHive / Inventure** — spatial and interior work-area design
4. **Fabrication & Site Documentation** — workshop and site photo archive, attribution pending

Additional architectural proposals, presentation studies, interiors and computational-art images follow. Unidentified photos remain in a separate archive rather than receiving unsupported project credits.

## Data and images

- `data/projects.json`: project titles, order, descriptions, publication and attribution caveats
- `data/media-manifest.json`: every remaining media record, its project assignment and original Wix source URL
- `assets/images/portfolio/`: optimized locally hosted copies, imported from the owner's personal Wix media library
- `scripts/import_wix_media.py`: optional media-recovery importer; it reads only the curated manifest

**Excluded:** all Portal Universalis material, all Automated Master Plan/AMP material, personal CV/resume documents, and ambiguous or unrelated video files.

The current GitHub files are optimized for the public website, **not** an archival-quality backup of full-resolution Wix originals. Original Wix-hosted files were not changed.

## Authorship, collaboration and image permissions

Project grouping is based on available filenames. Do not interpret archived work as a claim of sole authorship. Verify precise project names, contributors, photography rights and the user's role before submitting to a public-art jury. Image captions or project pages should describe responsibilities accurately.

## Hosting

This static site is configured to work on GitHub Pages from `main` / root. The site's grouped projects can be edited through `data/projects.json` and the manifest. The manual/automatic importer may be run from GitHub Actions for assets listed in the current manifest.
