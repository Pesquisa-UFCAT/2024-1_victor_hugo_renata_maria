from pathlib import Path
import os

DOCS = Path(__file__).resolve().parent
project = 'Distribuições flexíveis' if SITE_LANGUAGE == 'pt' else 'Flexible distributions'
author = 'Renata Maria Pensin, Wanderlei Malaquias Pereira Junior, Victor Hugo Moreira do Couto Souza, Marcos Luiz Henrique'
copyright = '2026, ' + author
language = 'pt_BR' if SITE_LANGUAGE == 'pt' else 'en'
extensions = ['myst_parser', 'sphinx.ext.mathjax']
myst_enable_extensions = ['dollarmath', 'colon_fence']
source_suffix = {'.rst': 'restructuredtext', '.md': 'markdown'}
root_doc = 'index'
exclude_patterns = []
html_theme = 'furo'
html_title = project
html_static_path = [str(DOCS/'_static')]
templates_path = [str(DOCS/'_templates')]
html_css_files = ['custom.css']
html_show_sourcelink = False
html_copy_source = False
html_show_sphinx = False
html_baseurl = os.environ.get('SITE_BASE_URL', 'https://wmpjrufg.github.io/distribuicoes-flexiveis').rstrip('/') + '/' + SITE_LANGUAGE + '/'
html_context = {'site_language': SITE_LANGUAGE, 'other_language': 'en' if SITE_LANGUAGE=='pt' else 'pt'}
html_sidebars = {'**':['sidebar/brand.html','language-switch.html','sidebar/scroll-start.html','sidebar/navigation.html','sidebar/scroll-end.html']}
html_theme_options = {
    'light_css_variables': {
        'color-brand-primary':'#12665e', 'color-brand-content':'#12665e',
        'color-background-primary':'#fcfbf7','color-background-secondary':'#f0f0e9',
        'color-foreground-primary':'#222f31','color-foreground-secondary':'#46575a',
    },
    'dark_css_variables': {'color-brand-primary':'#84d7c6','color-brand-content':'#84d7c6'},
    'navigation_with_keys': True,
}
mathjax3_config = {'tex': {'tags':'ams'}}
nitpicky = True
smartquotes = False


html_use_index = False
