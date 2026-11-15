# Distribuições flexíveis

Texto e materiais suplementares do artigo sobre modelagem de fenômenos físicos com a distribuição lambda generalizada (GLD-FKML) e `pyGLAM`.

[English instructions](README.en.md)

**Endereço previsto após ativar o Pages:** https://wmpjrufg.github.io/distribuicoes-flexiveis/

- Português: https://wmpjrufg.github.io/distribuicoes-flexiveis/pt/
- English: https://wmpjrufg.github.io/distribuicoes-flexiveis/en/

## Estrutura

```text
docs/
  conf_shared.py          Configuração Sphinx comum
  pt/                    Texto completo em português
  en/                    Texto completo em inglês
  _static/               Estilos
  _templates/            Seletor de idioma
data/                    CSV, fichas de proveniência e checksum
notebooks/               Um notebook por idioma
tools/                   Build, verificação e execução opcional
.github/workflows/       Build automático e publicação no Pages
requirements-docs.txt    Dependências do site
requirements-notebooks.txt
```

As pastas `en/` e `pt/` têm as mesmas páginas e a mesma navegação. A configuração
é compartilhada. Essa abordagem é adequada para dois manuscritos já completos:
permite revisar o texto de cada idioma diretamente, sem manter catálogos gettext
ou duplicar a configuração. O seletor de idioma abre a página equivalente.

## Construir e visualizar o site

Requer Python 3.11. Na raiz deste repositório:

```console
python -m venv .venv
```

Ative o ambiente no Windows com `.venv\Scripts\Activate.ps1`, ou no Linux/macOS
com `source .venv/bin/activate`. Depois:

```console
python -m pip install -r requirements-docs.txt
python tools/build_site.py
python -m http.server 8000 --directory _build/html
```

Abra http://localhost:8000. O build trata avisos do Sphinx como erros, verifica a
simetria das páginas, os links locais, as âncoras e os arquivos de download. O ZIP
com os materiais é montado automaticamente; não é necessário versioná-lo.

## Executar os notebooks

```console
python -m pip install -r requirements-notebooks.txt
python -m jupyterlab
```

Abra `notebooks/distribuicoes_flexiveis_pt.ipynb` ou
`notebooks/distribuicoes_flexiveis_en.ipynb` e execute todas as células na ordem.
Ambos usam o mesmo CSV e preservam as sementes, os modelos e as contagens de
reamostragem do notebook do artigo. Gráficos e tabelas são gravados em `outputs/`.
O bootstrap com reajuste pode levar vários minutos.

Verificação opcional de todas as células, sem interface gráfica:

```console
python tools/check_notebooks.py --execute pt
python tools/check_notebooks.py --execute en
```

Os notebooks distribuídos têm saídas limpas e somente metadados de kernel/linguagem.
O verificador também impede a inclusão de metadados extras e resíduos editoriais.

## Publicar no GitHub Pages

1. Faça o commit dos arquivos e envie para a branch padrão do repositório (`main`).
2. No GitHub, abra **Settings → Pages → Build and deployment**.
3. Em **Source**, selecione **GitHub Actions**. Não selecione publicação a partir de `/docs`.
4. Em **Settings → Actions → General**, confira se as Actions estão habilitadas e
   se a política permite as actions oficiais usadas no workflow. Não é necessário PAT.
5. Se houver restrição em **Settings → Environments → github-pages**, permita a
   branch padrão. O workflow já solicita `pages: write` e `id-token: write` no job de publicação.
6. Em **Actions → Build and publish Sphinx**, acompanhe a execução. Se ativou o Pages
   depois do primeiro push, use **Run workflow** na branch `main`.
7. Após os jobs `build` e `deploy` terminarem, abra o endereço mostrado no ambiente
   `github-pages` ou em **Settings → Pages**.

Cada push dispara o build, sem filtros de caminho. Pull requests também são
verificados. Somente a branch padrão publica o site; alterações em outras branches
não substituem a versão pública. Há execução manual por `workflow_dispatch`.

O workflow segue as [instruções oficiais do GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Conteúdo, origem e pendências

As páginas foram transpostas dos manuscritos locais `rbef_revisao2` (português) e
`rbef_revisao2_en` (inglês). Os capítulos mantêm texto, resultados, tabelas, figuras,
equações e citações; a organização foi adaptada para navegação web. Não há tradução
automática durante o build. A numeração das referências cruzadas acompanha o manuscrito.

Para editar, atualize as páginas correspondentes em `docs/pt/` e `docs/en/` e rode
`python tools/build_site.py`. Para uma página nova, crie a equivalente no outro
idioma e acrescente-a aos dois índices.

- Dados originais: INMET/BDMEP. Consulte `data/README.pt.md` e `data/README.en.md`.
- O CSV foi copiado sem alteração. `data/SHA256SUMS` registra sua integridade.
- **[TODO: preencher os campos de proveniência ainda pendentes na ficha dos dados.]**
- **[TODO: incluir DOI e referência definitiva do artigo quando publicados.]**
- **[TODO: definir a licença dos textos e do código; confirmar os termos aplicáveis aos dados.]**

Os arquivos `_build/`, `downloads/` e `outputs/` são gerados localmente e ignorados
pelo Git. Não é preciso enviar o HTML compilado nem os resultados dos notebooks.

