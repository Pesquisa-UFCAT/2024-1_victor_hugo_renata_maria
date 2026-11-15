Downloads
=========

Os dados e os notebooks permitem reproduzir os estudos de vento e temperatura do artigo.

.. container:: download-panel

   **Pacote completo**

   :download:`Baixar dados, os dois notebooks e as instruções (.zip) <../../downloads/supplementary-materials.zip>`

   Extraia o arquivo antes de abrir os notebooks. A organização das pastas já está pronta para execução.

Arquivos individuais
--------------------

* :download:`Dataset — estação A001, médias diárias (.csv) <../../data/estacao_A001_diario.csv>`
* :download:`Notebook em português (.ipynb) <../../notebooks/distribuicoes_flexiveis_pt.ipynb>`
* :download:`Notebook em inglês (.ipynb) <../../notebooks/distribuicoes_flexiveis_en.ipynb>`
* :download:`Dependências para execução (.txt) <../../requirements-notebooks.txt>`
* :download:`Ficha dos dados em português (.md) <../../data/README.pt.md>`
* :download:`Ficha dos dados em inglês (.md) <../../data/README.en.md>`
* :download:`Checksum SHA-256 do dataset <../../data/SHA256SUMS>`

Como executar
-------------

Use Python 3.11. Na raiz da pasta extraída, instale as dependências e abra o Jupyter:

.. code-block:: console

   python -m pip install -r requirements-notebooks.txt
   python -m jupyterlab

Abra o notebook desejado na pasta ``notebooks/`` e execute todas as células na ordem.
Os resultados são gravados em ``outputs/pt/`` ou ``outputs/en/``. O bootstrap com
reajuste dos modelos pode levar vários minutos. O site não executa os notebooks
durante a publicação; eles são executados localmente pelo leitor.

Se baixar os arquivos individualmente, coloque o CSV na mesma pasta do notebook
ou em ``data/`` na raiz do projeto.

Origem e citação
--------------------

Os dados meteorológicos provêm do `INMET / BDMEP <https://bdmep.inmet.gov.br/>`_.
A :doc:`ficha dos dados <data-notes>` registra as unidades, o período e as informações
de proveniência ainda pendentes de confirmação pelos autores.

**[TODO: referência bibliográfica definitiva e DOI do artigo após publicação.]**

**[TODO: definir a licença do código e dos textos e confirmar os termos de redistribuição dos dados do INMET.]**

