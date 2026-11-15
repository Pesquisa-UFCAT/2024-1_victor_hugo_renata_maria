from pathlib import Path
import collections
import contextlib
import hashlib
import importlib.metadata as md
import json
import os
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'paper_final/rbef_manuscrito_revisado'
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT / 'packages'))
COPY = OUT / 'reproduction'
COPY.mkdir(exist_ok=True)
for p in SRC.iterdir():
    if p.is_file() and p.suffix in ('.tex', '.csv', '.ipynb', '.png'):
        shutil.copy2(p, COPY / p.name)
shutil.copytree(SRC / 'codigo', COPY / 'codigo', dirs_exist_ok=True)

texts = {p.name: p.read_text(encoding='utf-8') for p in SRC.glob('*.tex')}
labels, refs, cites, bibs = [], [], [], []
files = []
for fn, txt in texts.items():
    for n, raw in enumerate(txt.splitlines(), 1):
        line = re.split(r'(?<!\\)%', raw)[0]
        for m in re.finditer(r'\\label\{([^}]+)\}|\blabel\s*=\s*([^,\]\s]+)', line):
            labels.append((m.group(1) or m.group(2), fn, n))
        for m in re.finditer(r'\\(?:eqref|ref|autoref|pageref)\{([^}]+)\}', line):
            refs.append((m.group(1), fn, n))
        for m in re.finditer(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}', line):
            cites.extend((k.strip(), fn, n) for k in m.group(1).split(','))
        bibs.extend((m.group(1), fn, n) for m in re.finditer(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', line))
        for m in re.finditer(r'\\(input|include|includegraphics|lstinputlisting)(?:\[[^\]]*\])?\{([^}]+)\}', line):
            target = SRC / m.group(2)
            if not target.suffix and m.group(1) in ('input', 'include'):
                target = target.with_suffix('.tex')
            files.append((str(target.relative_to(SRC)), target.exists(), fn, n))
lc = collections.Counter(x[0] for x in labels)
bk = {x[0] for x in bibs}
result = dict(labels=len(labels), references=len(refs), bibliography=len(bibs),
    citations=len(cites), duplicate_labels=[k for k,v in lc.items() if v > 1],
    missing_refs=[r for r in refs if r[0] not in lc],
    missing_cites=[c for c in cites if c[0] not in bk],
    missing_files=[f for f in files if not f[1]],
    unused_bibitems=[b for b in bibs if b[0] not in {c[0] for c in cites}],
    source_sha256={fn:hashlib.sha256((SRC/fn).read_bytes()).hexdigest() for fn in texts},
    versions={p:md.version(p) for p in ['numpy','pandas','scipy','matplotlib','pyglam']},
    python=sys.version)
(OUT / 'static_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k != 'source_sha256'}, ensure_ascii=False), flush=True)

if '--latex' in sys.argv:
    for i in range(1, 3):
        p = subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'], cwd=COPY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (OUT/f'latex_pass_{i}.txt').write_bytes(p.stdout)
        print('latex pass', i, 'exit', p.returncode, flush=True)
        if p.returncode: break
    log = (COPY/'main.log').read_text(errors='replace')
    print('\n'.join(l for l in log.splitlines() if any(t in l for t in ['Warning','Overfull','Underfull','Output written','!'])), flush=True)

if '--notebook' in sys.argv:
    os.environ['MPLBACKEND'] = 'Agg'
    nb = json.loads((COPY/'rbef_notebook.ipynb').read_text(encoding='utf-8'))
    os.chdir(COPY)
    ns = {'__name__':'__main__'}
    with (OUT/'notebook_reproduced.txt').open('w', encoding='utf-8') as f:
        for i, cell in enumerate(nb['cells'], 1):
            if cell['cell_type'] == 'code':
                print('Executing cell', i, flush=True)
                with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
                    exec(compile(''.join(cell['source']), f'notebook_cell_{i}', 'exec'), ns)
                f.flush()
    import numpy as np
    df, v, t = ns['df'], ns['v'], ns['t']
    valid = df[df.vento_ms.notna()]
    gaps = valid.data.diff().dt.days
    series = df.set_index('data').vento_ms
    extra = {'table_matches': {f: (SRC/f).read_text(encoding='utf-8') == (COPY/f).read_text(encoding='utf-8') for f in ['tab_descritiva.tex','tab_vento.tex','tab_temperatura.tex']},
        'params_wind':ns['sol_v'].x.tolist(), 'params_temperature':ns['sol_t'].x.tolist(),
        'gaps_between_valid_wind':int((gaps>1).sum()), 'max_gap_days':float(gaps.max()),
        'date_range_days':int((df.data.max()-df.data.min()).days+1),
        'q_bootstrap_wind_std':ns['bv'].std(axis=0).tolist(),
        'q_bootstrap_temperature_std':ns['bt'].std(axis=0).tolist(),
        'wind_ac1_calendar':float(series.corr(series.shift(1))),
        'wind_year_means':df.groupby('ano').vento_ms.mean().to_dict(),
        'wind_month_means':df.groupby('mes').vento_ms.mean().to_dict(),
        'july_missing':int(((df.mes==7)&df.temperatura_c.isna()).sum()),
        'rain_years':df[df.precipitacao_mm.notna()].groupby('ano').precipitacao_mm.count().to_dict()}
    (OUT/'numeric_audit.json').write_text(json.dumps(extra, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(extra, ensure_ascii=False), flush=True)
