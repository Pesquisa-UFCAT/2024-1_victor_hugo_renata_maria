# Manuscrito revisado para a RBEF — LEIAME

## Conteúdo
- `main.tex` + `rbef_*.tex` + `preamble.tex`: manuscrito revisado (LaTeX, UTF-8, sem comentários, sem TikZ).
- `referencias.tex`: bibliografia em `\bibitem`, numerada na ordem de citação (26 referências), conforme as normas da RBEF. Substitui `references.bib`/biblatex APA.
- `rbef_notebook.ipynb`: notebook único e reprodutível (caminho relativo, executável de cima para baixo). Gera as Figuras 1–5 (PT e EN), `tab_descritiva.tex`, `tab_vento.tex`, `tab_temperatura.tex`, a tabela de candidatos do ajuste, a contagem fora do suporte e as simulações de incerteza. Substitui o `task_01.ipynb`.
- `codigo/`: Códigos 1–3 citados no texto (inalterados; já usam `n_starts=15`).
- Figuras: a Figura 1 foi regenerada (vírgula decimal nos eixos da versão PT). As Figuras 2–5 são as originais até o notebook ser executado com os dados reais.

## Principais alterações no texto
1. Citações numéricas (`\cite`) e equações referidas como "equação (n)", conforme a RBEF.
2. Introdução: ligação com teoria de erros, GUM e Monte Carlo (Vuolo; JCGM 100/101; Ribeiro-Silva e Ribeiro-Silva, RBEF 2025, antes citado no .bib mas não no texto).
3. Seção 3: Gilchrist (função quantil), Ramberg et al. 1979 (método dos momentos para a GLD), Karian e Dudewicz; caso λ = 0 incluído; critério de seleção do `pyglam` descrito como a biblioteca realmente faz; estimadores alternativos (percentis, L-momentos, máxima verossimilhança).
4. Seção 4: alcance da dedução da Rayleigh (intervalos curtos vs médias diárias; Justus 1978; Carta 2009); ligação com Maxwell-Boltzmann; Lilliefors; bootstrap em blocos (Künsch 1989).
5. Seção 5 (vento): metadados da A001 (OMM 86715, ~15,79° S, 47,93° W, 1.161 m, desde maio/2000); piso de D_n imposto pelo arredondamento (simulação: mediana 0,034, P95 0,039; 0,009 sem arredondamento); incerteza amostral dos quantis (~0,05 m/s); verossimilhança nula da GLD por momentos; ⟨v³⟩ = ∫Q(u)³du como extensão.
6. Seção 6 (temperatura): argumento da "incerteza do sensor" substituído pela incerteza amostral dos quantis (DP ~0,15 °C em Q05 e ~0,09 °C em Q95, amostras independentes) e pelo valor crítico de Lilliefors (0,032), com a ressalva da dependência; origem física da assimetria negativa (frentes frias / massas de ar polar); item das "24 máximas anuais" reescrito sem números não reproduzíveis.
7. Resumo/abstract e considerações finais atualizados de acordo.
8. Referências corrigidas: Zhu e Sudret, p. 1345–1380; MF-GLaM publicado (CMAME 448, 118498, 2026); Ribeiro-Silva com os dois autores. Todas as referências de periódico foram conferidas no CrossRef.

## Verificação com os dados reais (estacao_A001_diario.csv)
O notebook foi executado com o CSV real (saída completa em `saida_notebook.txt`). As tabelas regeneradas são idênticas às do manuscrito, e os números do texto foram conferidos:
- 84 dias (0,95%) abaixo do suporte da GLD (1,148 m/s) — confirmado;
- 11 dos 15 pontos iniciais convergiram para a solução selecionada (2 para outra solução válida de resíduo maior, 2 fora do domínio dos momentos) — agora escrito no texto;
- piso de D_n por arredondamento: mediana 0,034, P95 0,039 (0,008 sem arredondamento);
- autocorrelação de defasagem 1: 0,65 (vento e julho); bootstrap em blocos de 10 dias (vento): DP de Q50 e Q95 = 0,03 e 0,06 m/s; bootstrap por anos inteiros (julho): DP de Q05, Q50 e Q95 = 0,38, 0,10 e 0,21 °C — incluídos nas seções 5 e 6;
- precipitação: 8.759 válidos, 5.675 iguais a zero — confirmado.
As Figuras 1–5 (PT e EN) foram regeneradas com os dados reais na paleta Okabe–Ito (GLD #0072B2, Rayleigh/Normal #D55E00, Weibull #009E73, julho #E69F00).

## Pendências dos autores (antes de submeter)
1. **Compilar o PDF localmente** (`pdflatex main` duas vezes) e revisar a diagramação. A checagem estática (chaves, ambientes, rótulos, citações, arquivos) passou, mas não foi possível compilar no ambiente do revisor.
2. Opcional: números de processo das bolsas (CNPq/FAPEG) nos agradecimentos.
3. Na submissão: seção "Artigos Gerais"; anexar como material suplementar `rbef_notebook.ipynb`, `estacao_A001_diario.csv` e a pasta `codigo/`.
