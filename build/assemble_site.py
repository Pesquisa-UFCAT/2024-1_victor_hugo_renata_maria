from pathlib import Path
import ast
import copy
import hashlib
import json
import re
import shutil
import textwrap
from urllib.parse import quote
import pypandoc

WORK = Path(__file__).resolve().parent.parent
OUT = WORK / 'build/distribuicoes-flexiveis-site'
BASE = WORK / 'paper_final/rbef_manuscrito_revisao2'
SOURCES = {'pt': BASE / 'rbef_revisao2', 'en': BASE / 'rbef_revisao2_en'}
URL = 'https://wmpjrufg.github.io/distribuicoes-flexiveis'

def write(path, text):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text).lstrip('\n'), encoding='utf-8', newline='\n')

def rst(text):
    return pypandoc.convert_text(text, 'rst', format='latex', extra_args=['--wrap=none']).replace('\r', '').strip()

def resize_tables(text):
    def resize(m):
        indent = m[1]
        lines = m[0].splitlines()
        rows = [line.strip()[1:-1].split('|') for line in lines if line.strip().startswith('|')]
        widths = [max(len(row[i].strip()) for row in rows)+2 for i in range(len(rows[0]))]
        result = []
        for line in lines:
            if line.strip().startswith('|'):
                cells = line.strip()[1:-1].split('|')
                result.append(indent+'|'+'|'.join(' '+v.strip().ljust(w-2)+' ' for v,w in zip(cells,widths))+'|')
            else:
                fill = '=' if '=' in line else '-'
                result.append(indent+'+'+'+'.join(fill*w for w in widths)+'+')
        return '\n'.join(result)+'\n'
    return re.sub(r'(?m)^([ ]*)\+[-+=]+\+\n(?:\1[|+].*\n)*', resize, text+'\n').rstrip()

CHAPTERS = [
    ('introduction', 'rbef_02_introducao'),
    ('distribution', 'rbef_03_gld'),
    ('data', 'rbef_04_dados_modelos'),
    ('wind', 'rbef_05_vento'),
    ('temperature', 'rbef_06_temperatura'),
    ('classroom', 'rbef_065_roteiro'),
    ('conclusions', 'rbef_07_consideracoes'),
]

# Read the existing manuscript labels; do not infer scientific quantities.
aux = (SOURCES['pt'] / 'main.aux').read_text(encoding='utf-8')
numbers = dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}', aux))
listing_count = 0
for _, name in CHAPTERS:
    for listing_options in re.findall(r'\\lstinputlisting\[(.*?)\]', (SOURCES['pt']/f'{name}.tex').read_text(encoding='utf-8'), re.S):
        listing_count += 1
        label = re.search(r'label=([^,\]]+)', listing_options)[1].strip()
        numbers[label] = str(listing_count)
citations = re.findall(r'\\bibcite\{([^}]+)\}\{\{(\d+)\}', aux)
if not citations:
    # Citation order is derived from the text when no bibliography was compiled.
    keys = []
    for _, name in CHAPTERS:
        for group in re.findall(r'\\cite\w*\{([^}]+)\}', (SOURCES['pt']/f'{name}.tex').read_text(encoding='utf-8')):
            for key in group.split(','):
                if key not in keys:
                    keys.append(key)
    citations = [(key, str(i+1)) for i,key in enumerate(keys)]
citenums = dict(citations)

for lang, source in SOURCES.items():
    outdir = OUT / 'docs' / lang
    outdir.mkdir(parents=True, exist_ok=True)
    for path in source.glob(f'figura*_{lang}.png'):
        (outdir / 'images').mkdir(exist_ok=True)
        shutil.copy2(path, outdir / 'images' / path.name)
    for page, filename in CHAPTERS:
        text = (source / f'{filename}.tex').read_text(encoding='utf-8')
        snippets = {}

        def token(content):
            key = f'RBEFBLOCK{len(snippets):04d}TOKEN'
            snippets[key] = content
            return '\n\n' + key + '\n\n'

        def equation(match):
            body = match.group(1).strip()
            labels = re.findall(r'\\label\{([^}]+)\}', body)
            body = re.sub(r'\\label\{[^}]+\}', '', body).strip()
            label = labels[0] if labels else None
            prefix = f'.. _{label}:\n\n' if label else ''
            if label in numbers:
                body += '\n\\tag{' + numbers[label] + '}'
            return token(prefix + '.. math::\n\n' + textwrap.indent(body, '   '))

        def listing(match):
            options, path = match.groups()
            label = re.search(r'label=([^,\]]+)', options).group(1).strip()
            caption = re.search(r'caption=\{(.*)\},\s*label=', options, re.S).group(1)
            code = (source / path).read_text(encoding='utf-8').rstrip()
            title = ('Código' if lang == 'pt' else 'Code') + ' ' + numbers[label] + '. ' + rst(caption)
            return token(f'.. _{label}:\n\n**{title}**\n\n.. code-block:: python\n\n' + textwrap.indent(code, '   '))

        text = re.sub(r'\\input\{([^}]+)\}', lambda m:(source / (m[1] if m[1].endswith('.tex') else m[1]+'.tex')).read_text(encoding='utf-8').strip(), text)
        text = text.replace(r'\unskip', '')
        text = re.sub(r'\\lstinputlisting\[(.*?)\]\{([^}]+)\}', listing, text, flags=re.S)
        text = re.sub(r'\\begin\{equation\}(.*?)\\end\{equation\}', equation, text, flags=re.S)

        def crossref(m):
            label = m[2]
            if label not in numbers:
                raise ValueError(f'Unresolved manuscript reference: {label}')
            number = numbers[label]
            if m[1] == 'eqref':
                number = '(' + number + ')'
            key = f'RBEFINLINE{len(snippets):04d}TOKEN'
            snippets[key] = f':ref:`{number} <{label}>`'
            return key

        def citation(m):
            parts = []
            for key in m[1].split(','):
                key = key.strip()
                if key not in citenums:
                    citenums[key] = str(len(citenums)+1)
                parts.append(f':ref:`[{citenums[key]}] <ref-{key}>`')
            key = f'RBEFINLINE{len(snippets):04d}TOKEN'
            snippets[key] = ', '.join(parts)
            return key

        text = re.sub(r'\\(eqref|ref)\{([^}]+)\}', crossref, text)
        text = re.sub(r'\\cite\w*\{([^}]+)\}', citation, text)
        # Supply the identity revision macro used by earlier manuscript files.
        result = rst('\\newcommand{\\rev}[1]{#1}\n' + text)
        for key, value in snippets.items():
            result = result.replace(key, value)
        result = resize_tables(result)
        result = re.sub(r'(?m)^   name: (.+)$', r'   :name: \1', result)
        result = re.sub(r'(?m)^\.\. figure:: (figura[^\n]+)', r'.. figure:: images/\1', result)
        # Pandoc's named containers become explicit Sphinx reference targets.
        result = re.sub(r'\.\. container::\n   :name: ([^\n]+)\n', lambda m:f'.. _{m[1]}:\n\n.. container::\n', result)
        result = re.sub(r'(\.\. figure:: [^\n]+)\n   :name: ([^\n]+)', lambda m:f'.. _{m[2]}:\n\n{m[1]}', result)
        for figure_label in re.findall(r'\.\. _(fig:[^\n]+):\n', result):
            anchor = '.. _' + figure_label + ':'
            start = result.find(anchor)
            tail = result[start:]
            # Caption follows the image directive and its options.
            fm = re.search(r'(\.\. figure:: [^\n]+\n(?:   :[^\n]+\n)*\n)(   \S)', tail)
            if fm:
                offset = start + fm.start(2) + 3
                word = 'Figura' if lang == 'pt' else 'Figure'
                result = result[:offset]+f'{word} {numbers[figure_label]}. '+result[offset:]
        # Include the original global table/figure numbering in the captions.
        for env, caption_word in [('table', 'Tabela' if lang == 'pt' else 'Table'), ('figure', 'Figura' if lang == 'pt' else 'Figure')]:
            for match in re.finditer(r'\\begin\{'+env+r'\}.*?\\end\{'+env+r'\}', text, re.S):
                lm = re.search(r'\\label\{([^}]+)\}', match[0])
                if lm and lm[1] in numbers:
                    anchor = '.. _' + lm[1] + ':'
                    start = result.find(anchor)
                    if start >= 0 and env == 'table':
                        ti = result.find('.. table:: ', start)
                        if ti >= 0:
                            result = result[:ti] + result[ti:].replace('.. table:: ', f'.. table:: {caption_word} {numbers[lm[1]]}. ', 1)
        write(f'docs/{lang}/{page}.rst', result + '\n')

    abstract_tex = (source/'rbef_01_resumo.tex').read_text(encoding='utf-8').split('\\begin{abstract}',1)[1].split('\\medskip',1)[0]
    abstract = rst(abstract_tex)
    title = 'Distribuições flexíveis' if lang == 'pt' else 'Flexible distributions'
    intro = ('Material de estudo e reprodução do artigo sobre a distribuição lambda generalizada, com exemplos de vento e temperatura.' if lang == 'pt' else 'Study and reproduction materials for the paper on the generalized lambda distribution, with wind and temperature examples.')
    download = 'Baixar dados e notebooks' if lang == 'pt' else 'Download data and notebooks'
    write(f'docs/{lang}/index.rst', title+'\n'+'='*len(title)+'\n\n'+intro+f'\n\n:doc:`{download} <downloads>`\n\n'+('Resumo' if lang=='pt' else 'Abstract')+'\n--------\n\n'+abstract+'\n\n'+('Autoria' if lang=='pt' else 'Authors')+'\n--------\n\nRenata Maria Pensin · Wanderlei Malaquias Pereira Junior · Victor Hugo Moreira do Couto Souza · Marcos Luiz Henrique\n\n'+('Texto completo e materiais' if lang=='pt' else 'Full text and materials')+'\n---------------------------\n\n.. toctree::\n   :maxdepth: 2\n\n'+''.join('   '+p+'\n' for p,_ in CHAPTERS)+'   downloads\n   data-notes\n   references\n')

    bibliography = json.loads(pypandoc.convert_file(str(source/'referencias.bib'), 'csljson', format='biblatex'))
    reftext = ('Referências' if lang=='pt' else 'References')+'\n===========\n\n'
    by_id = {item['id']:item for item in bibliography}
    for key, number in sorted(citenums.items(), key=lambda x:int(x[1])):
        item = by_id[key]
        authors = '; '.join(x.get('literal') or ' '.join(filter(None,[x.get('given'),x.get('non-dropping-particle'),x.get('family'),x.get('suffix')])).strip() for x in item.get('author',[]))
        title = re.sub('<[^>]+>', '', item['title'])
        dates = item.get('issued', {}).get('date-parts', [[]])
        issued = dates[0][0] if dates and dates[0] else ('s.d.' if lang=='pt' else 'n.d.')
        venue = item.get('container-title',item.get('publisher',''))
        vol = str(item.get('volume',''))
        issue = str(item.get('issue',''))
        pages = str(item.get('page','')).replace('–','–')
        details = ', '.join(x for x in [venue, vol + (f'({issue})' if issue else ''),pages] if x)
        link = 'https://doi.org/'+item['DOI'] if item.get('DOI') else item.get('URL','')
        link = quote(link, safe=':/;?=&%')
        reftext += f'.. _ref-{key}:\n\n**[{number}]** {authors}. *{title}*. {details} ({issued}).'
        if link:
            reftext += f' `{"Fonte" if lang=="pt" else "Source"} <{link}>`__.'
        reftext += '\n\n'
    write(f'docs/{lang}/references.rst', reftext)

# Preserve the supplied dataset byte-for-byte.
(OUT/'data').mkdir(exist_ok=True)
shutil.copy2(SOURCES['pt']/'estacao_A001_diario.csv', OUT/'data/estacao_A001_diario.csv')
data_notes = (SOURCES['pt']/'FICHA_DADOS.md').read_text(encoding='utf-8').replace('[AUTORES', '[TODO').replace('rbef_notebook.ipynb','distribuicoes_flexiveis_pt.ipynb')
write('data/README.pt.md', data_notes)
write('docs/pt/data-notes.md', data_notes)
write('data/README.en.md', '''
# Data sheet — automatic station A001 (Brasília, Brazil)

Items marked **[TODO]** must be completed or confirmed by the authors.

| Item | Value |
|---|---|
| Source | INMET Meteorological Database (BDMEP), https://bdmep.inmet.gov.br/ |
| Product / query | Daily automatic-station data **[TODO: exact product name and query parameters]** |
| Retrieval date | **[TODO: retrieval date]** |
| Station | A001, Brasília (DF), WMO 86715; 15.79° S, 47.93° W; elevation 1,161 m |
| File coverage | 2000-05-06 to 2025-04-25; 9,121 calendar days, no duplicate dates |
| Original fields | **[TODO: original BDMEP column names]** → `data`, `precipitacao_mm`, `temperatura_c`, `umidade_relativa_pct`, `vento_ms` |
| Daily-mean definition | Daily value supplied by INMET from hourly records; not recalculated by the authors **[TODO: confirm; specify hours and UTC time zone]** |
| Daily completeness criterion | **[TODO: INMET criterion for producing the daily value, if documented]** |
| Anemometer height | 10 m **[TODO: confirm against the station record]** |
| Sensor changes | Not documented in the file; not assessed |
| Recording step | 0.1 m/s (wind), 0.1 °C (temperature); file rounding, not metrological resolution |
| Wind gaps | 281 missing days; 101 gaps between valid records; longest gap 29 days |
| Authors' transformations | Column renaming and date conversion; no interpolation or missing-value imputation |
| Reading | “Read and inspect the data” cells of `distribuicoes_flexiveis_en.ipynb` |

The column names are retained in Portuguese in both notebooks to preserve the supplied CSV schema.
''')
shutil.copy2(OUT/'data/README.en.md', OUT/'docs/en/data-notes.md')
write('data/SHA256SUMS', hashlib.sha256((OUT/'data/estacao_A001_diario.csv').read_bytes()).hexdigest()+'  estacao_A001_diario.csv\n')

if __name__ == '__main__':
    print(OUT)
