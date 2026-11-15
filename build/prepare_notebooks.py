from pathlib import Path
import ast
import copy
import io
import json
import re
import tokenize
import nbformat

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'build/distribuicoes-flexiveis-site'
SOURCE = ROOT / 'paper_final/rbef_manuscrito_revisao2/rbef_revisao2/rbef_notebook.ipynb'
original = json.loads(SOURCE.read_text(encoding='utf-8'))
HEADINGS = {
    2: ('Estilo das figuras e formatação', 'Figure style and formatting'),
    4: ('Efeito de cada parâmetro', 'Effect of each parameter'),
    6: ('Leitura e exame de qualidade dos dados', 'Read and inspect the data'),
    8: ('Estatísticas descritivas', 'Descriptive statistics'),
    10: ('Vento: ajustes, suporte e comparação', 'Wind: fitting, support and comparison'),
    12: ('Temperatura de julho: ajustes e comparação', 'July temperature: fitting and comparison'),
    14: ('Arredondamento e incerteza amostral', 'Rounding and sampling uncertainty'),
    16: ('Figuras dos estudos de caso', 'Case-study figures'),
    18: ('Precipitação: contagem de dias sem chuva', 'Precipitation: count of rain-free days'),
}

# Translate reader-facing messages while retaining the CSV field names.
EN = {
 'Número formatado; vírgula decimal em português.': 'Format a number using the selected decimal separator.',
 'Rótulos dos eixos com vírgula decimal na versão em português.': 'Use decimal commas only for Portuguese axes.',
 'Número para as tabelas LaTeX, com vírgula decimal.': 'Format a number for a LaTeX table.',
 'Distância de Kolmogorov-Smirnov (Código 3 do artigo).': 'Kolmogorov-Smirnov distance (Code 3 in the paper).',
 'Figura 1 gravada': 'Figure 1 saved',
 'Figuras 2 a 5 gravadas': 'Figures 2 to 5 saved',
 'Período:': 'Period:',
 'Registros:': 'Records:',
 'datas repetidas:': 'duplicate dates:',
 'Vento: válidos': 'Wind: valid',
 'vazios': 'missing',
 'nulos ou negativos': 'zero or negative',
 'Menor passo entre valores distintos do vento (resolução):': 'Smallest step between distinct wind records (rounding):',
 'Julho: n =': 'July: n =',
 '| anos': '| years',
 'Média': 'Mean',
 'Mediana': 'Median',
 'Desvio padrão': 'Standard deviation',
 'Coeficiente de variação': 'Coefficient of variation',
 'Assimetria': 'Skewness',
 'Curtose (Pearson)': 'Kurtosis (Pearson)',
 'Mínimo; máximo': 'Minimum; maximum',
 'CV teórico': 'theoretical CV',
 'CV amostral': 'sample CV',
 '| suporte =': '| support =',
 'Observações fora do suporte:': 'Observations outside support:',
 'Pontos iniciais que convergiram para a solução selecionada:': 'Starting points converging to the selected solution:',
 ' de {len(cand)}': ' of {len(cand)}',
 '| fora:': '| outside:',
 'Valor crítico assintótico de Lilliefors (5%, dados independentes):': 'Asymptotic Lilliefors critical value (5%, independent data):',
 'Vento, Dn com modelo verdadeiro: contínuo mediana': 'Wind, Dn under the true model: continuous median',
 'arredondado mediana': 'rounded median',
 'Vento, DP dos quantis empíricos (amostras independentes):': 'Wind, SD of empirical quantiles (independent samples):',
 'Julho, DP dos quantis empíricos (amostras independentes):': 'July, SD of empirical quantiles (independent samples):',
 'Lacunas entre registros válidos de vento:': 'Gaps between valid wind records:',
 '| maior:': '| longest:',
 '} dias': '} days',
 'Autocorrelação de defasagem 1 (pares de dias consecutivos): vento': 'Lag-1 autocorrelation (consecutive calendar days): wind',
 'Autocorrelação das anomalias (sem ciclo anual), defasagens 1-10:': 'Anomaly autocorrelation (annual cycle removed), lags 1-10:',
 'Vento, DP bootstrap (blocos de': 'Wind, bootstrap SD (blocks of',
 ' dias) dos quantis empíricos:': ' days) of empirical quantiles:',
 'Q_0,05 empírico nas reamostras (valores distintos):': 'Empirical Q_0.05 in resamples (distinct values):',
 'DP do desvio GLD   :': 'SD of GLD deviation:',
 'DP do desvio Weibull:': 'SD of Weibull deviation:',
 'Autocorrelação média de defasagem 1 em julho:': 'Mean lag-1 autocorrelation in July:',
 'Julho, DP bootstrap por anos inteiros dos quantis:': 'July, whole-year bootstrap SD of quantiles:',
 'Precipitação: válidos': 'Precipitation: valid',
 'iguais a zero': 'equal to zero',
 'Anos com dados:': 'Years with data:',
 'Anos civis 2001-2024 com pelo menos 95% dos dias registrados:': 'Calendar years 2001-2024 with at least 95% recorded days:',
 'Coluna precipitacao_mm ausente no arquivo.': 'The file has no precipitacao_mm column.',
}

for language in ['pt', 'en']:
    nb = nbformat.v4.new_notebook()
    nb.metadata = {
        'kernelspec': {'display_name':'Python 3', 'language':'python', 'name':'python3'},
        'language_info': {'name':'python'},
    }
    for i, c in enumerate(original['cells']):
        source = ''.join(c['source'])
        if c['cell_type'] == 'markdown':
            if i == 0:
                if language == 'pt':
                    source = '''# Distribuições flexíveis: vento e temperatura

Este notebook reproduz os cálculos, as figuras e as tabelas dos estudos de caso do artigo sobre a distribuição lambda generalizada (GLD-FKML).

1. Instale as dependências com `python -m pip install -r requirements-notebooks.txt`, na raiz do repositório.
2. Abra este notebook no Jupyter e selecione **Restart Kernel and Run All Cells**.
3. Os resultados serão gravados em `outputs/pt/`. A reamostragem com reajuste dos modelos pode levar vários minutos.

**Dados:** `data/estacao_A001_diario.csv`. As colunas `data`, `vento_ms` e `temperatura_c` são obrigatórias; `precipitacao_mm` é opcional. O código encontra o arquivo a partir da raiz do repositório, da pasta `notebooks/` ou da mesma pasta do notebook.

**Fonte e limites:** consulte `data/README.pt.md`. As médias diárias não permitem recuperar a variabilidade horária; a qualidade do ajuste deve ser avaliada junto com o suporte e a incerteza amostral.
'''
                else:
                    source = '''# Flexible distributions: wind and temperature

This notebook reproduces the calculations, figures and tables of the case studies in the paper on the generalized lambda distribution (GLD-FKML).

1. Install the dependencies with `python -m pip install -r requirements-notebooks.txt` from the repository root.
2. Open this notebook in Jupyter and select **Restart Kernel and Run All Cells**.
3. Results are written to `outputs/en/`. Resampling with model refitting may take several minutes.

**Data:** `data/estacao_A001_diario.csv`. The `data` (date), `vento_ms` (wind speed in m/s) and `temperatura_c` (temperature in °C) columns are required; `precipitacao_mm` (precipitation in mm) is optional. The code locates the file from the repository root, the `notebooks/` folder or the notebook's own folder. Column names are kept unchanged from the supplied dataset.

**Source and limitations:** see `data/README.en.md`. Daily means cannot recover hourly variability; goodness of fit must be assessed together with support and sampling uncertainty.
'''
            else:
                source = '## ' + HEADINGS[i][language == 'en']
                if i == 14:
                    source += ('\n\nA comparação é descritiva. São preservadas as sementes e as contagens de reamostragem do notebook original.' if language == 'pt' else '\n\nThe comparison is descriptive. Random seeds and resampling counts are preserved from the original notebook.')
            cell = nbformat.v4.new_markdown_cell(source)
        else:
            if i == 1:
                source = source[:source.index('ARQUIVO_DADOS =')] + f'''LANGUAGE = '{language}'
_candidates = [Path('data/estacao_A001_diario.csv'),
               Path('../data/estacao_A001_diario.csv'),
               Path('estacao_A001_diario.csv')]
ARQUIVO_DADOS = next((p.resolve() for p in _candidates if p.is_file()), None)
if ARQUIVO_DADOS is None:
    raise FileNotFoundError({'"Baixe o CSV da página de downloads e coloque-o em data/ ou junto deste notebook."' if language == 'pt' else '"Download the CSV from the downloads page and place it in data/ or beside this notebook."'})
_root = ARQUIVO_DADOS.parent.parent if ARQUIVO_DADOS.parent.name == 'data' else ARQUIVO_DADOS.parent
SAIDA = _root / 'outputs' / LANGUAGE
SAIDA.mkdir(parents=True, exist_ok=True)
SEMENTE = 0
N_STARTS = 15
P = np.array([0.05, 0.50, 0.95])
'''
            source = source.replace("for lang in ['pt', 'en']:", 'for lang in [LANGUAGE]:')
            source = source.replace("def num(x, nd, lang='pt'):", 'def num(x, nd, lang=LANGUAGE):')
            if i == 3:
                tree = ast.parse(source)
                assignment = next(n for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'TXT')
                # The value consists solely of literal dictionaries and dict calls.
                labels = eval(compile(ast.Expression(assignment.value), '<labels>', 'eval'), {'__builtins__':{}, 'dict':dict})
                lines = source.splitlines(keepends=True)
                lines[assignment.lineno-1:assignment.end_lineno] = ['TXT = '+repr({language:labels[language]})+'\n']
                source = ''.join(lines)
                source = source.replace("return s.replace('.', '{,}')", "return s.replace('.', '{,}') if LANGUAGE == 'pt' else s")
            if language == 'en':
                # Code explanations are provided by the translated Markdown cells.
                tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
                source = tokenize.untokenize(t for t in tokens if t.type != tokenize.COMMENT)
                for old,new in sorted(EN.items(), key=lambda x:-len(x[0])):
                    source = source.replace(old,new)
                source = source.replace("'a', df['data'].max()", "'to', df['data'].max()")
                source = source.replace("'a', julho['ano'].max()", "'to', julho['ano'].max()")
                source = source.replace("def milhar(n): return f'{n:,}'.replace(',', '.')", "def milhar(n): return f'{n:,}'")
                source = source.replace("'$Q_{0{,}05}$; $Q_{0{,}50}$; $Q_{0{,}95}$'", "'$Q_{0.05}$; $Q_{0.50}$; $Q_{0.95}$'")
                source = source.replace("{'dias' if lang == 'pt' else 'days'}", "{'days'}")
                source = source.replace("['custo']", "['cost']").replace("['no_dominio']", "['in_domain']").replace("['dist_quantis']", "['quantile_distance']")
            # Normalize whitespace, and validate every code cell before saving.
            source = '\n'.join(line.rstrip() for line in source.splitlines()).strip()+'\n'
            ast.parse(source)
            cell = nbformat.v4.new_code_cell(source, execution_count=None, outputs=[])
        cell['id'] = f'cell-{i:02d}'
        cell['metadata'] = {}
        nb.cells.append(cell)
    nbformat.validate(nb)
    target = OUT/'notebooks'/f'distribuicoes_flexiveis_{language}.ipynb'
    target.parent.mkdir(exist_ok=True)
    nbformat.write(nb,target)
    print(language, len(nb.cells), 'cells')
