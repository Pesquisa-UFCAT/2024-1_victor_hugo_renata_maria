Downloads
=========

The data and notebooks reproduce the wind and temperature case studies in the paper.

.. container:: download-panel

   **Complete package**

   :download:`Download the data, both notebooks and instructions (.zip) <../../downloads/supplementary-materials.zip>`

   Extract the archive before opening the notebooks. Its folder structure is ready for execution.

Individual files
----------------

* :download:`Dataset — station A001, daily means (.csv) <../../data/estacao_A001_diario.csv>`
* :download:`English notebook (.ipynb) <../../notebooks/distribuicoes_flexiveis_en.ipynb>`
* :download:`Portuguese notebook (.ipynb) <../../notebooks/distribuicoes_flexiveis_pt.ipynb>`
* :download:`Execution dependencies (.txt) <../../requirements-notebooks.txt>`
* :download:`English data sheet (.md) <../../data/README.en.md>`
* :download:`Portuguese data sheet (.md) <../../data/README.pt.md>`
* :download:`Dataset SHA-256 checksum <../../data/SHA256SUMS>`

How to run
----------

Use Python 3.11. From the extracted folder's root, install the dependencies and launch Jupyter:

.. code-block:: console

   python -m pip install -r requirements-notebooks.txt
   python -m jupyterlab

Open the desired notebook in ``notebooks/`` and run all cells in order.
Results are written to ``outputs/en/`` or ``outputs/pt/``. Bootstrap resampling
with model refitting may take several minutes. Publishing the site does not
execute the notebooks; readers run them locally.

If downloading files individually, place the CSV beside the notebook
or in the project's root ``data/`` folder.

Source and citation
-------------------

The meteorological data come from `INMET / BDMEP <https://bdmep.inmet.gov.br/>`_.
The :doc:`data sheet <data-notes>` records the units, period and provenance details
that still require confirmation by the authors.

**[TODO: final bibliographic reference and paper DOI after publication.]**

**[TODO: choose licenses for the code and text and confirm the INMET data redistribution terms.]**

