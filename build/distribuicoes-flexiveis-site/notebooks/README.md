# Dados e notebooks / Data and notebooks

## Português

Extraia o pacote completo. Use Python 3.11 e execute, na raiz da pasta extraída:

```console
python -m pip install -r requirements-notebooks.txt
python -m jupyterlab
```

Abra `notebooks/distribuicoes_flexiveis_pt.ipynb` e execute todas as células na ordem.
O arquivo de dados fica em `data/estacao_A001_diario.csv`; os resultados são gravados
em `outputs/pt/`. O bootstrap com reajuste pode levar vários minutos.
Consulte `data/README.pt.md` para origem, unidades e pendências de documentação.

## English

Extract the complete package. Use Python 3.11 and run from the extracted root folder:

```console
python -m pip install -r requirements-notebooks.txt
python -m jupyterlab
```

Open `notebooks/distribuicoes_flexiveis_en.ipynb` and run all cells in order.
The dataset is `data/estacao_A001_diario.csv`; results go to `outputs/en/`.
Bootstrap resampling with refitting may take several minutes.
See `data/README.en.md` for provenance, units and pending documentation.

Site / Website: https://wmpjrufg.github.io/distribuicoes-flexiveis/
