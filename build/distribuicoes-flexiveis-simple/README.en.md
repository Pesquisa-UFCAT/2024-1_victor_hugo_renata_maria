# Flexible distributions

A small bilingual site: an introduction, a brief FKML explanation and downloads.
The manuscript text is not part of the website. Add the paper link to
`docs/en/index.rst` and `docs/pt/index.rst` only after publication.

Website: https://wmpjrufg.github.io/distribuicoes-flexiveis/

## Structure

- `docs/en/` and `docs/pt/`: only `index.rst` and `downloads.rst` in each language.
- `data/`: original dataset and provenance sheets.
- `notebooks/`: both notebooks and execution instructions.
- `tools/`: build and material validation.
- `.github/workflows/pages.yml`: builds on every push; deploys from the default branch.

## Local build

Use Python 3.11, preferably in a virtual environment:

```console
python -m pip install -r requirements-docs.txt
python tools/build_site.py
python -m http.server 8000 --directory _build/html
```

Open http://localhost:8000. Each build clears old HTML so removed pages cannot
remain published. The data and notebooks are packaged into a ZIP automatically.

## Publish

1. Select **Settings → Pages → Source → GitHub Actions**.
2. Enable Actions and allow the default branch in the `github-pages` environment.
3. Commit and push; monitor **Actions → Build and publish Sphinx**.
4. If needed, select **Run workflow** on the default branch.

Keep `/en/downloads.html` and `/pt/downloads.html` unchanged: the papers cite them.
See `notebooks/README.md` for execution instructions and `data/` for provenance.

**[TODO: choose text/code licenses and confirm applicable dataset terms.]**

Generated `_build/`, `downloads/` and `outputs/` directories are ignored by Git.
