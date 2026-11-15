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
