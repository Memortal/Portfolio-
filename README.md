# MEMO Portfolio — Wix archive and project gallery

A public, searchable archive of portfolio media migrated from the owner's two Wix sites:
- **Alireza Memarian** — architectural work, MAK Studio, DesignHive, fabrication studies, and other portfolio projects
- **Portal Universalis** — installation visuals and associated media

**Deliberately excluded:** the entire *Automated Master Pla* Wix site, files explicitly labeled AMP or Automated Master Plan, résumé/CV documents and their scanned image versions, and unrelated or ambiguous videos pending review.

## How it works

1. `data/media-manifest.json` is a filename-and-URL inventory from Wix. It preserves source URLs and provenance.
2. `scripts/import_wix_media.py` downloads and optimizes eligible images and selected project videos into `assets/`. It writes a `localPath` for successful files.
3. The import workflow commits the optimized files back into this repository.
4. `index.html` loads the manifest and displays a responsive, searchable portfolio archive.

Images originally uploaded at full resolution have been converted to web-friendly versions for this public repository. **The optimized copies are not a full-resolution backup.** Keep originals in private storage; Wix source URLs are retained as reference links.

## Project authorship and rights

Historic media from multiple collaborative studios is presented as an archive of prior work, **not a claim of sole authorship or ownership**. Confirm project titles, roles, collaborators, image rights, and credits before using images in a formal application or public-facing final portfolio.

## Website

This repository includes a static site ready for GitHub Pages. To publish, open **Settings → Pages**, select **Deploy from a branch**, and select `main` and `/(root)`. The expected user-facing address after publication is `https://memortal.github.io/Portfolio-/`, but only GitHub Pages can confirm when it is live.

## Import updates

Run the **Import Wix media** GitHub Actions workflow from the Actions tab if you need to retry failed downloads. The generated manifest records each file's import status. Large and ambiguous videos remain linked from Wix when they cannot safely be put into GitHub.
