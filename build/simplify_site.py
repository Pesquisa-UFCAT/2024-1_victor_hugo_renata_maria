from pathlib import Path
import shutil
import textwrap

SOURCE = Path('C:/Users/User/Desktop/github/distribuicoes-flexiveis')
STAGE = Path(__file__).resolve().parent / 'distribuicoes-flexiveis-simple'
STAGE.mkdir(exist_ok=True)
for folder in ['data', 'notebooks', 'tools', '.github', 'docs/_static', 'docs/_templates']:
    shutil.copytree(SOURCE/folder, STAGE/folder, dirs_exist_ok=True)
for name in ['.gitignore', 'requirements-docs.txt', 'requirements-notebooks.txt', 'docs/conf_shared.py', 'docs/pt/conf.py', 'docs/en/conf.py']:
    (STAGE/name).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE/name, STAGE/name)

def write(name, content):
    (STAGE/name).write_text(textwrap.dedent(content).lstrip(), encoding='utf-8', newline='\n')

write('docs/pt/index.rst', r'''
Distribuições flexíveis
========================

Uma breve introdução à distribuição lambda generalizada e materiais para explorar
dados de vento e temperatura com Python e ``pyGLAM``.

:doc:`Baixar dados e notebooks <downloads>`

A FKML em poucas palavras
----------------------------

A distribuição lambda generalizada, na parametrização FKML, permite representar
formas simétricas ou assimétricas, com caudas limitadas ou não. Ela é definida pela
função quantil: para uma probabilidade :math:`u`, :math:`Q(u)` fornece o valor abaixo
do qual está essa fração da distribuição. Por exemplo, :math:`Q(0{,}5)` é a mediana.

.. math::

   Q(u)=\lambda_1+\frac{1}{\lambda_2}
   \left[\frac{u^{\lambda_3}-1}{\lambda_3}
   -\frac{(1-u)^{\lambda_4}-1}{\lambda_4}\right],
   \qquad 0<u<1,\quad\lambda_2>0.

* :math:`\lambda_1` desloca a distribuição.
* :math:`\lambda_2` controla a escala inversamente: aumentá-lo reduz a dispersão.
* :math:`\lambda_3` e :math:`\lambda_4` controlam a forma, principalmente nos lados
  esquerdo e direito, respectivamente.

Quando um parâmetro de forma é zero, a fração correspondente é substituída pelo
limite logarítmico. O ajuste pode ser feito pelo método dos momentos, como nos
notebooks. Além da concordância com os dados, é necessário verificar se o suporte
do modelo é adequado à grandeza física e às observações.

Artigo
--------

O artigo será disponibilizado aqui após a publicação.

.. TODO: adicionar a referência e o link do artigo somente após a publicação.

.. toctree::
   :hidden:

   downloads
''')

write('docs/en/index.rst', r'''
Flexible distributions
========================

A brief introduction to the generalized lambda distribution and materials for
exploring wind and temperature data with Python and ``pyGLAM``.

:doc:`Download data and notebooks <downloads>`

FKML in a nutshell
---------------------

The generalized lambda distribution, in the FKML parameterization, can represent
symmetric or asymmetric shapes with bounded or unbounded tails. It is defined by
its quantile function: for a probability :math:`u`, :math:`Q(u)` gives the value
below which that fraction of the distribution lies. For example, :math:`Q(0.5)` is
the median.

.. math::

   Q(u)=\lambda_1+\frac{1}{\lambda_2}
   \left[\frac{u^{\lambda_3}-1}{\lambda_3}
   -\frac{(1-u)^{\lambda_4}-1}{\lambda_4}\right],
   \qquad 0<u<1,\quad\lambda_2>0.

* :math:`\lambda_1` shifts the distribution.
* :math:`\lambda_2` inversely controls scale: increasing it reduces dispersion.
* :math:`\lambda_3` and :math:`\lambda_4` control shape, mainly on the left and
  right sides, respectively.

When a shape parameter is zero, the corresponding fraction is replaced by its
logarithmic limit. Parameters can be fitted by the method of moments, as in the
notebooks. Besides agreement with the data, the model's support must be checked
against the physical quantity and the observations.

Paper
--------

The paper will be made available here after publication.

.. TODO: add the paper citation and link only after publication.

.. toctree::
   :hidden:

   downloads
''')

write('docs/pt/downloads.rst', '''
Downloads
=========

Dados meteorológicos e notebooks com exemplos de ajuste de distribuições.

.. container:: download-panel

   :download:`Baixar o pacote completo (.zip) <../../downloads/supplementary-materials.zip>`

   Inclui o dataset, os notebooks em português e inglês e as instruções de execução.

Arquivos individuais
----------------------

* :download:`Dataset da estação A001 (.csv) <../../data/estacao_A001_diario.csv>`
* :download:`Notebook em português (.ipynb) <../../notebooks/distribuicoes_flexiveis_pt.ipynb>`
* :download:`Notebook em inglês (.ipynb) <../../notebooks/distribuicoes_flexiveis_en.ipynb>`
* :download:`Dependências (.txt) <../../requirements-notebooks.txt>`
* :download:`Ficha dos dados (.md) <../../data/README.pt.md>`

Como usar
------------

Extraia o pacote, use Python 3.11 e execute na pasta extraída:

.. code-block:: console

   python -m pip install -r requirements-notebooks.txt
   python -m jupyterlab

Abra um notebook em ``notebooks/`` e execute as células na ordem. Se baixar
arquivos individuais, coloque o CSV junto do notebook ou em ``data/`` na raiz.

Fonte dos dados: `INMET / BDMEP <https://bdmep.inmet.gov.br/>`_.
''')

write('docs/en/downloads.rst', '''
Downloads
=========

Meteorological data and notebooks with distribution-fitting examples.

.. container:: download-panel

   :download:`Download the complete package (.zip) <../../downloads/supplementary-materials.zip>`

   Includes the dataset, English and Portuguese notebooks, and execution instructions.

Individual files
-------------------

* :download:`Station A001 dataset (.csv) <../../data/estacao_A001_diario.csv>`
* :download:`English notebook (.ipynb) <../../notebooks/distribuicoes_flexiveis_en.ipynb>`
* :download:`Portuguese notebook (.ipynb) <../../notebooks/distribuicoes_flexiveis_pt.ipynb>`
* :download:`Dependencies (.txt) <../../requirements-notebooks.txt>`
* :download:`Data sheet (.md) <../../data/README.en.md>`

Getting started
------------------

Extract the package, use Python 3.11 and run from the extracted folder:

.. code-block:: console

   python -m pip install -r requirements-notebooks.txt
   python -m jupyterlab

Open a notebook in ``notebooks/`` and run its cells in order. For individual
downloads, place the CSV beside the notebook or in the root ``data/`` folder.

Data source: `INMET / BDMEP <https://bdmep.inmet.gov.br/>`_.
''')

conf = (STAGE/'docs/conf_shared.py').read_text(encoding='utf-8')
conf = conf.replace("'sidebar/search.html',", '')
conf += '\nhtml_use_index = False\n'
write('docs/conf_shared.py', conf)

build = (STAGE/'tools/build_site.py').read_text(encoding='utf-8')
build = build.replace('import os\n', 'import os\nimport shutil\n')
build = build.replace("run('tools/check_notebooks.py')", """# A clean output prevents removed manuscript chapters from remaining public.
assert BUILD.resolve() == (ROOT.resolve()/'_build'/'html'), 'Unexpected build path'
assert not BUILD.is_symlink(), 'Build directory must not be a symlink'
if BUILD.exists():
    shutil.rmtree(BUILD)
run('tools/check_notebooks.py')""")
build = build.replace('Dados · Notebooks · Texto do artigo', 'Introdução · FKML · Downloads').replace('Data · Notebooks · Paper text', 'Introduction · FKML · Downloads')
write('tools/build_site.py',build)

write('README.md', '''
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
''')
write('README.en.md', '''
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
''')
print(STAGE)
