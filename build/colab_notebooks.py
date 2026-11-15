from pathlib import Path
import json
import shutil
import textwrap
import nbformat

REPO = Path('C:/Users/User/Desktop/github/distribuicoes-flexiveis')
OUT = Path(__file__).resolve().parent/'distribuicoes-flexiveis-colab'
OUT.mkdir(exist_ok=True)
for p in REPO.iterdir():
    if p.name in {'.git', '.venv', '_build', 'outputs', 'downloads'}:
        continue
    if p.is_dir():shutil.copytree(p, OUT/p.name, dirs_exist_ok=True)
    else:shutil.copy2(p, OUT/p.name)

def write(path, text):
    (OUT/path).write_text(textwrap.dedent(text).strip()+'\n',encoding='utf-8')

for lang in ['pt','en']:
    pt = lang=='pt'
    colab = f'https://colab.research.google.com/github/wmpjrufg/distribuicoes-flexiveis/blob/main/notebooks/distribuicoes_flexiveis_{lang}.ipynb'
    content = []
    def md(text):content.append(nbformat.v4.new_markdown_cell(textwrap.dedent(text).strip()))
    def code(text):content.append(nbformat.v4.new_code_cell(textwrap.dedent(text).strip()))

    md(('''# Distribuições flexíveis: vento e temperatura

Execute as células de cima para baixo. Quando aparecer o botão de upload,
selecione **`estacao_A001_diario.csv`**.

Vamos ajustar a GLD-FKML e compará-la com distribuições clássicas.
''' if pt else '''# Flexible distributions: wind and temperature

Run the cells from top to bottom. When the upload button appears,
select **`estacao_A001_diario.csv`**.

We will fit the GLD-FKML and compare it with classical distributions.
''')+f'\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab})')
    code('''
    %pip install -q pyglam==1.1.0

    import io
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy import stats
    from pyglam import GlamFKML
    from google.colab import files
    ''')
    md('''## 1. Enviar e ler os dados

O CSV contém as colunas `data`, `vento_ms` e `temperatura_c`.
''' if pt else '''## 1. Upload and read the data

The CSV contains `data` (date), `vento_ms` (wind speed in m/s)
and `temperatura_c` (temperature in °C). The column names stay unchanged.
''')
    code('''
    uploaded = files.upload()
    df = pd.read_csv(io.BytesIO(next(iter(uploaded.values()))))
    df['data'] = pd.to_datetime(df['data'])
    df.head()
    ''')
    md('''## 2. Uma função para comparar os ajustes

O gráfico mostra o histograma e as densidades. A tabela mostra a distância
de Kolmogorov–Smirnov (`Dn`) e os desvios dos quantis de 5%, 50% e 95%.
Desvio = quantil do modelo − quantil dos dados. Quanto mais perto de zero, melhor.
Usamos `Dn` apenas como medida descritiva, sem teste de hipótese.
''' if pt else '''## 2. A function to compare fits

The plot shows the histogram and densities. The table shows the Kolmogorov–Smirnov
distance (`Dn`) and deviations at the 5%, 50% and 95% quantiles.
Deviation = model quantile − data quantile. Values closer to zero indicate better agreement.
We use `Dn` only as a descriptive measure, not as a hypothesis test.
''')
    code(f'''
    def compare(x, models, xlabel):
        p = np.array([0.05, 0.50, 0.95])
        empirical = np.quantile(x, p)
        grid = np.linspace(x.min(), x.max(), 400)
        rows = []
        plt.figure(figsize=(7, 4))
        plt.hist(x, bins=30, density=True, alpha=0.3, color='gray')
        for name, model in models.items():
            plt.plot(grid, model.pdf(grid), label=name)
            delta = model.ppf(p) - empirical
            rows.append([name, stats.ks_1samp(x, model.cdf).statistic, *delta])
        plt.xlabel(xlabel)
        plt.ylabel('{'Densidade' if pt else 'Density'}')
        plt.legend()
        plt.show()
        return pd.DataFrame(rows, columns=['{'Modelo' if pt else 'Model'}', 'Dn', 'Δ5%', 'Δ50%', 'Δ95%']).round(3)
    ''')
    md('''## 3. Velocidade média diária do vento

Usamos os valores disponíveis, sem preencher as falhas. A GLD é ajustada
pelo método dos momentos; Rayleigh e Weibull, por máxima verossimilhança,
com a origem fixada em zero.
''' if pt else '''## 3. Daily mean wind speed

We use available observations without filling gaps. The GLD is fitted by
the method of moments; Rayleigh and Weibull use maximum likelihood,
with their origin fixed at zero.
''')
    code(f'''
    wind = df['vento_ms'].dropna().to_numpy()
    fit_wind = GlamFKML().fit_lambdas(wind, n_starts=15, seed=0)
    gld_wind = GlamFKML(*fit_wind.x)
    _, rayleigh_scale = stats.rayleigh.fit(wind, floc=0)
    shape, _, scale = stats.weibull_min.fit(wind, floc=0)

    print('n =', len(wind))
    print('λ =', fit_wind.x.round(4))
    compare(wind, {{
        'Rayleigh': stats.rayleigh(scale=rayleigh_scale),
        'Weibull': stats.weibull_min(shape, scale=scale),
        'GLD-FKML': gld_wind,
    }}, '{'Velocidade do vento (m/s)' if pt else 'Wind speed (m/s)'}')
    ''')
    md('''### O suporte também importa

Um bom ajuste dos momentos não garante que o modelo inclua todos os dados.
Vamos contar quantos dias ficam fora dos limites da GLD ajustada.
''' if pt else '''### Support matters too

A good moment fit does not guarantee that the model includes all observations.
Let us count how many days fall outside the fitted GLD bounds.
''')
    code(f'''
    l1, l2, l3, l4 = fit_wind.x
    lower = l1 - 1 / (l2 * l3) if l3 > 0 else -np.inf
    upper = l1 + 1 / (l2 * l4) if l4 > 0 else np.inf
    outside = np.sum((wind < lower) | (wind > upper))
    print(f"{'Suporte' if pt else 'Support'}: {{lower:.3f}} {'a' if pt else 'to'} {{upper:.3f}} m/s")
    print(f"{'Dias fora do suporte' if pt else 'Days outside support'}: {{outside}} ({{100 * outside / len(wind):.2f}}%)")
    ''')
    md('''## 4. Temperatura média diária de julho

Selecionamos julho para reduzir a mistura entre estações do ano.
Comparamos a GLD-FKML com a distribuição normal.
''' if pt else '''## 4. Daily mean temperature in July

We select July to reduce mixing across seasons.
We compare the GLD-FKML with the normal distribution.
''')
    code(f'''
    temperature = df.loc[df['data'].dt.month == 7, 'temperatura_c'].dropna().to_numpy()
    fit_temperature = GlamFKML().fit_lambdas(temperature, n_starts=15, seed=0)
    gld_temperature = GlamFKML(*fit_temperature.x)
    mean, std = stats.norm.fit(temperature)

    print('n =', len(temperature))
    print('λ =', fit_temperature.x.round(4))
    compare(temperature, {{
        'Normal': stats.norm(mean, std),
        'GLD-FKML': gld_temperature,
    }}, '{'Temperatura' if pt else 'Temperature'} (°C)')
    ''')
    md('''## Para pensar

- Qual modelo tem os menores desvios de quantis no vento?
- O que significa a GLD excluir alguns dias do seu suporte?
- A melhora no ajuste da temperatura justifica usar quatro parâmetros em vez de dois?

Estes são ajustes descritivos. Os dados diários têm dependência temporal,
e a incerteza amostral não é avaliada neste exemplo curto.
''' if pt else '''## Questions to explore

- Which model has the smallest wind quantile deviations?
- What does it mean for the GLD to exclude some days from its support?
- Does the improved temperature fit justify four parameters instead of two?

These are descriptive fits. Daily observations are temporally dependent,
and this short example does not assess sampling uncertainty.
''')
    book = nbformat.v4.new_notebook(cells=content, metadata={
        'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
        'language_info':{'name':'python'},
    })
    for i,cell in enumerate(book.cells):
        cell.id=f'cell-{i:02d}'
        cell.metadata={}
    nbformat.validate(book)
    nbformat.write(book,OUT/'notebooks'/f'distribuicoes_flexiveis_{lang}.ipynb')

    heading = 'Rodar no Google Colab' if pt else 'Run in Google Colab'
    intro = 'Abra o notebook, execute as células e envie o CSV quando solicitado.' if pt else 'Open the notebook, run the cells and upload the CSV when prompted.'
    label = 'Abrir no Colab' if pt else 'Open in Colab'
    (OUT/f'docs/{lang}/downloads.rst').write_text(f'''Downloads
=========

{heading}
--------------------------

{intro}

.. image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: {colab}
   :alt: {label}

`{label} <{colab}>`_

* :download:`{'Baixar o dataset (.csv)' if pt else 'Download the dataset (.csv)'} <../../data/estacao_A001_diario.csv>`
* :download:`{'Notebook em português' if pt else 'Portuguese notebook'} <../../notebooks/distribuicoes_flexiveis_pt.ipynb>`
* :download:`{'Notebook em inglês' if pt else 'English notebook'} <../../notebooks/distribuicoes_flexiveis_en.ipynb>`
* :download:`{'Pacote completo (.zip)' if pt else 'Complete package (.zip)'} <../../downloads/supplementary-materials.zip>`
* :download:`{'Ficha dos dados' if pt else 'Data sheet'} <../../data/README.{lang}.md>`

{'Não é preciso instalar Python no computador. A primeira célula instala o pyglam no Colab; os gráficos e as tabelas aparecem no próprio notebook.' if pt else 'No local Python installation is needed. The first cell installs pyglam in Colab; plots and tables appear directly in the notebook.'}

{'Fonte dos dados' if pt else 'Data source'}: `INMET / BDMEP <https://bdmep.inmet.gov.br/>`_.
''',encoding='utf-8')

write('requirements-notebooks.txt','''
pyglam==1.1.0
numpy
pandas
scipy
matplotlib
''')
write('notebooks/README.md','''
# Abrir, enviar o CSV e calcular / Open, upload the CSV and calculate

## Português

1. [Abra o notebook no Colab](https://colab.research.google.com/github/wmpjrufg/distribuicoes-flexiveis/blob/main/notebooks/distribuicoes_flexiveis_pt.ipynb).
2. Execute as células na ordem.
3. Na célula de upload, selecione `data/estacao_A001_diario.csv` deste pacote.

Os gráficos e tabelas aparecem no notebook. Não é preciso configurar pastas,
salvar figuras nem instalar Python localmente. A primeira célula instala o pyglam.
São comparados os ajustes de vento e temperatura, com uma verificação do suporte.
Este exemplo curto não executa bootstrap nem reproduz todas as análises do manuscrito.

## English

1. [Open the notebook in Colab](https://colab.research.google.com/github/wmpjrufg/distribuicoes-flexiveis/blob/main/notebooks/distribuicoes_flexiveis_en.ipynb).
2. Run the cells in order.
3. At the upload cell, select `data/estacao_A001_diario.csv` from this package.

Plots and tables appear in the notebook. No folder configuration, figure export
or local Python installation is needed. The first cell installs pyglam.
The examples compare wind and temperature fits and check the wind model's support.
This short example does not run bootstrap or reproduce every manuscript analysis.
''')

for lang,filename in [('pt','README.md'),('en','README.en.md')]:
    text=(OUT/filename).read_text(encoding='utf-8')
    title='## Usar os notebooks' if lang=='pt' else '## Use the notebooks'
    sentence=('Abra no Colab, execute as células e faça upload do CSV. Os gráficos e resultados aparecem no notebook.' if lang=='pt' else 'Open in Colab, run the cells and upload the CSV. Plots and results appear in the notebook.')
    link=f'https://colab.research.google.com/github/wmpjrufg/distribuicoes-flexiveis/blob/main/notebooks/distribuicoes_flexiveis_{lang}.ipynb'
    write(filename,text+'\n\n'+title+'\n\n'+sentence+f'\n\n[Google Colab]({link})\n')
print(OUT)
