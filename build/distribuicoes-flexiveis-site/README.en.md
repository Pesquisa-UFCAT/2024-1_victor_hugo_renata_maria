# Flexible distributions

Paper text and supplementary materials for modeling physical phenomena with the
generalized lambda distribution (GLD-FKML) and `pyGLAM`.

[Instruções em português](README.md)

Expected site after enabling Pages: https://wmpjrufg.github.io/distribuicoes-flexiveis/

## Repository structure

- `docs/en/` and `docs/pt/`: complete manuscript text with matching pages and navigation.
- `docs/conf_shared.py`, `_static/`, `_templates/`: shared configuration, styles and language switch.
- `data/`: supplied CSV, provenance sheets and SHA-256 checksum.
- `notebooks/`: English and Portuguese notebooks.
- `tools/`: site build, validation and optional notebook execution.
- `.github/workflows/pages.yml`: automatic build and GitHub Pages deployment.

Separate language directories suit the two existing complete manuscripts and let
authors edit each text directly, without gettext catalogs. The language switch
opens the equivalent page. Configuration is shared.

## Build the site

Use Python 3.11. Create a virtual environment and activate it:

```console
python -m venv .venv
```

Windows: `.venv\Scripts\Activate.ps1`. Linux/macOS: `source .venv/bin/activate`.

```console
python -m pip install -r requirements-docs.txt
python tools/build_site.py
python -m http.server 8000 --directory _build/html
```

Open http://localhost:8000. Sphinx warnings fail the build. The build also checks
matching language pages, local links, anchors, notebook metadata and downloads,
and packages the supplementary ZIP automatically.

## Run the notebooks

```console
python -m pip install -r requirements-notebooks.txt
python -m jupyterlab
```

Open either notebook in `notebooks/` and run all cells in order. Both use the same
CSV, seeds, models and resampling counts. Outputs go to `outputs/en/` or
`outputs/pt/`. Bootstrap resampling with model refitting can take several minutes.

Optional sequential execution without a graphical interface:

```console
python tools/check_notebooks.py --execute en
python tools/check_notebooks.py --execute pt
```

## Enable GitHub Pages

1. Commit the source files and push to the repository's default branch (`main`).
2. Open **Settings → Pages → Build and deployment → Source → GitHub Actions**.
3. Under **Settings → Actions → General**, enable Actions and allow the official
   actions in the workflow. No personal access token is required.
4. If the **github-pages** environment restricts deployment branches, allow the
   default branch. The workflow already requests `pages: write` and `id-token: write`.
5. Monitor **Actions → Build and publish Sphinx**. If Pages was enabled after the
   first push, select **Run workflow** on `main`.
6. Open the deployment URL after both `build` and `deploy` succeed.

Every push triggers a build, without path filters; pull requests are also checked.
Only the default branch deploys. Manual runs are supported.
See the [official GitHub guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Content and pending information

The web chapters preserve the supplied Portuguese and English manuscripts,
including their results, equations, tables, figures and citations. No translation
runs during the build. Edit the matching pages in both language directories and
rebuild after changes.

The dataset was copied unchanged. Consult `data/README.en.md` for provenance and
`data/SHA256SUMS` for integrity verification.

- **[TODO: complete outstanding dataset-provenance fields.]**
- **[TODO: add the final paper citation and DOI after publication.]**
- **[TODO: choose licenses for text/code and confirm applicable dataset terms.]**

Generated `_build/`, `downloads/` and `outputs/` directories are ignored by Git.
Commit the source files, not compiled HTML or notebook results.
