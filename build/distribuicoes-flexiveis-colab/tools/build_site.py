"""Build both Sphinx languages, package downloads and check local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import subprocess
import sys
import zipfile
import os
import shutil

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT/'_build/html'

def run(*args):
    subprocess.run([sys.executable,'-X','utf8',*args],cwd=ROOT,check=True,env={**os.environ,'PYTHONUTF8':'1'})

# A clean output prevents removed manuscript chapters from remaining public.
assert BUILD.resolve() == (ROOT.resolve()/'_build'/'html'), 'Unexpected build path'
assert not BUILD.is_symlink(), 'Build directory must not be a symlink'
if BUILD.exists():
    shutil.rmtree(BUILD)
run('tools/check_notebooks.py')
pages = {lang:{p.stem for p in (ROOT/'docs'/lang).iterdir() if p.suffix in {'.rst','.md'}} for lang in ['pt','en']}
assert pages['pt']==pages['en'], 'Language page structures differ'

downloads = ROOT/'downloads'
downloads.mkdir(exist_ok=True)
with zipfile.ZipFile(downloads/'supplementary-materials.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for directory in ['data','notebooks']:
        for path in sorted((ROOT/directory).rglob('*')):
            if path.is_file() and '.ipynb_checkpoints' not in path.parts:
                archive.write(path,path.relative_to(ROOT))
    for filename in ['requirements-notebooks.txt']:
        archive.write(ROOT/filename,filename)
    archive.write(ROOT/'notebooks/README.md','README.md')

for lang in ['pt','en']:
    run('-m','sphinx','-b','html','-W','--keep-going','-n',f'docs/{lang}',f'_build/html/{lang}')

BUILD.mkdir(parents=True,exist_ok=True)
(BUILD/'.nojekyll').touch()
(BUILD/'index.html').write_text('''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Distribuições flexíveis · Flexible distributions</title>
<meta name="description" content="Dados e notebooks sobre distribuições flexíveis. Data and notebooks on flexible distributions.">
<link rel="alternate" hreflang="pt" href="pt/index.html"><link rel="alternate" hreflang="en" href="en/index.html">
<style>
*{box-sizing:border-box}body{margin:0;background:#f5f3eb;color:#203f3c;font:18px/1.6 system-ui,sans-serif}
main{max-width:980px;margin:auto;padding:10vh 7vw}small{font-size:12px;text-transform:uppercase;letter-spacing:.13em}
h1{font:clamp(2.5rem,6vw,4.5rem)/1.08 Georgia,serif;letter-spacing:-.04em;margin:1.3rem 0}
h1 span{display:block;color:#63746c;font-size:.64em;margin-top:.65rem}p{max-width:580px;color:#4c6059}
nav{display:flex;gap:1rem;flex-wrap:wrap;margin:2.5rem 0}a{color:#fff;background:#12665e;padding:.8rem 1.5rem;border-radius:4px;text-decoration:none;font-weight:600}
a:focus-visible{outline:3px solid #b46e18;outline-offset:5px}a:hover{background:#0b5049}footer{border-top:1px solid #ccd3c8;padding-top:1rem;font-size:13px;color:#50645c}
</style></head><body><main><small>pyGLAM · GLD-FKML</small>
<h1>Distribuições flexíveis<span lang="en">Flexible distributions</span></h1>
<p>Do modelo aos dados: vento, temperatura e a interpretação física de um ajuste.</p>
<p lang="en">From models to data: wind, temperature and the physical interpretation of a fit.</p>
<nav aria-label="Idioma / Language"><a href="pt/index.html" lang="pt-BR">Português →</a><a href="en/index.html" lang="en">English →</a></nav>
<footer>Introdução · FKML · Downloads<br><span lang="en">Introduction · FKML · Downloads</span></footer>
</main></body></html>''',encoding='utf-8')

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets=set()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.targets.add(attrs['id'])
        if tag=='a' and 'name' in attrs:self.targets.add(attrs['name'])
        for key in ('href','src'):
            if key in attrs:self.links.append(attrs[key])

documents={}
for path in BUILD.rglob('*.html'):
    parser=Links()
    parser.feed(path.read_text(encoding='utf-8'))
    documents[path.resolve()]=parser
errors=[]
for path, document in documents.items():
    for link in document.links:
        url=urlsplit(link)
        if url.scheme or url.netloc or link.startswith('data:'):continue
        target=(path.parent/unquote(url.path)).resolve() if url.path else path
        if target.is_dir():target=target/'index.html'
        if not target.exists():errors.append(f'{path.name}: missing {link}')
        elif url.fragment and target in documents and unquote(url.fragment) not in documents[target].targets:
            errors.append(f'{path.name}: missing anchor {link}')
if errors:raise SystemExit('\n'.join(errors))
print(f'Validated {len(documents)} HTML pages, local links and downloadable files.')
print(f'Preview: python -m http.server 8000 --directory {BUILD}')
