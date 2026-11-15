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
