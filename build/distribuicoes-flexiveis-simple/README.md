# Distribuições flexíveis

Site simples e bilíngue: uma introdução, uma explicação curta da FKML e downloads.
O conteúdo do manuscrito não faz parte do site. O link do artigo será incluído
em `docs/pt/index.rst` e `docs/en/index.rst` somente após a publicação.

Endereço: https://wmpjrufg.github.io/distribuicoes-flexiveis/

## Estrutura

- `docs/pt/` e `docs/en/`: apenas `index.rst` e `downloads.rst` em cada idioma.
- `data/`: dataset original e fichas de proveniência.
- `notebooks/`: notebooks em português e inglês e instruções de execução.
- `tools/`: build e verificação dos materiais.
- `.github/workflows/pages.yml`: build em cada push; publicação pela branch padrão.

## Construir localmente

Use Python 3.11, preferencialmente em um ambiente virtual:

```console
python -m pip install -r requirements-docs.txt
python tools/build_site.py
python -m http.server 8000 --directory _build/html
```

Abra http://localhost:8000. Cada build limpa o HTML anterior, impedindo que páginas
removidas continuem publicadas. Dados e notebooks entram automaticamente no ZIP.

## Publicar

1. Em **Settings → Pages → Source**, selecione **GitHub Actions**.
2. Verifique se Actions estão habilitadas e se o ambiente `github-pages` permite a branch padrão.
3. Faça commit e push; acompanhe **Actions → Build and publish Sphinx**.
4. Se necessário, use **Run workflow** na branch padrão.

Os endereços `/pt/downloads.html` e `/en/downloads.html` são os citados nos papers.
Não altere esses caminhos ao atualizar o conteúdo.

Os detalhes de execução estão em `notebooks/README.md`. As pendências de origem
dos dados permanecem identificadas nas fichas em `data/`.

**[TODO: definir a licença dos textos e do código e confirmar os termos aplicáveis aos dados.]**

Não versione `_build/`, `downloads/` ou `outputs/`; essas pastas estão no `.gitignore`.
