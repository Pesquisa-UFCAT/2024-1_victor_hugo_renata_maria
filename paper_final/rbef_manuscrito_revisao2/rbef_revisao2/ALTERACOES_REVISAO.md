# Alterações feitas em resposta ao parecer simulado (14/11/2026)

No manuscrito, todo trecho novo ou reescrito aparece em vermelho (macro `\rev{}` ou bloco `{\color{red} ...}`).
Para a versão final, depois de ler tudo, basta trocar no `preamble.tex` a linha
`\newcommand{\rev}[1]{\textcolor{red}{#1}}` por `\newcommand{\rev}[1]{#1}` e apagar os `\color{red}` dos blocos
(em `rbef_05_vento.tex` e `rbef_065_roteiro.tex`). Procure também por `[AUTORES` — são dados que só vocês podem confirmar.

## Revisor 1
| Item | O que foi feito | Onde |
|---|---|---|
| M1 blocos não consecutivos | Série posta no calendário; só blocos de 10 dias sem falhas são sorteados. Autocorrelação recalculada com pares de dias consecutivos (0,65, inalterada). Justificativa do comprimento pela autocorrelação das anomalias (< 0,1 a partir de ~5 dias) e sensibilidade com 5, 10, 20 e 30 dias. Alvo declarado: distribuição histórica agregada. Novo DP da mediana: 0,021 m/s (antes 0,033); Q95: 0,055 (antes 0,055). | Seç. 5.2 e 5.6; Seç. 4.4; notebook, célula 15 |
| M2 atribuição causal do D_n | Texto passa a dizer que, no cenário simulado, o arredondamento leva D_n a valores próximos do observado; explicita que 0,041 > P95 0,039 e que não é decomposição nem teste. | Seç. 5.6, Conclusões, Resumo |
| M3 desvio × erro-padrão | Nova Tabela 6 com Δp e DP de Δp (500 reamostras, com reajuste dos modelos). Discussão da degenerescência do Q05 (sempre 1,4 m/s) e diferença entre quantil dos registros e da grandeza contínua. "Mesma ordem", "descritivo". | Seç. 5.6, `tab_vento_incerteza.tex` |
| M4 documentação dos dados | Parágrafo de proveniência, passo de registro × resolução, falhas, altura do sensor, ficha `FICHA_DADOS.md`. Sensor removido como argumento na temperatura. | Seç. 5.2, 6.4, Disponibilidade dos dados |
| m5 CV em Celsius | Célula removida da tabela; legenda explica (≈0,005 em kelvin). | Tabela 4 |

## Revisor 2
| Item | O que foi feito | Onde |
|---|---|---|
| M1 contribuição didática | Nova seção 7 "Sugestão de uso em sala": público, pré-requisitos, duração estimada (não testada), tabela objetivo → atividade → evidência e 4 tarefas com respostas esperadas. | `rbef_065_roteiro.tex` |
| m2 premissa do resumo | "ocupa posição central em muitos cursos introdutórios" (PT e EN). | Resumo/Abstract |
| m3 ribeiro2025 | Monte Carlo fica só com JCGM 101; Ribeiro-Silva passa a contextualizar ajuste e incertezas no ensino. | Introdução |
| m4 mecanismo meteorológico | "Uma explicação física plausível…", com Garreaud (2000), Mon. Wea. Rev. 128, 2544 (DOI conferido na CrossRef), e ressalva de que os eventos não foram identificados. | Seç. 6.4, referência 27 |

## Revisor 3
| Item | O que foi feito | Onde |
|---|---|---|
| m1 parâmetros | Vento λ3 = 0,555; temperatura com 4 casas (19,538; 1,0707; 0,0175; 0,1836); nota de que o limite −33,9 °C usa parâmetros não arredondados e de sua sensibilidade a λ3. Notebook imprime 4 casas. | Seç. 5.4, 6.3, 6.4 |
| "outra solução válida" | "duas tentativas terminaram em soluções válidas distintas, de resíduo maior". | Seç. 5.4 |
| m2 anos de precipitação | 18 anos civis (2001–2024) com ≥ 95% dos dias registrados; notebook calcula. | Seç. 6.5 |
| m3 Q-Q e suporte | Fig. 3 regenerada com faixa sombreada e linha do suporte (84 dias); legendas das Figs. 3 e 5 informam o recorte 1–99%. | Figs. 3 e 5 |
| m4 TikZ/ORCID e SciPy | `orcidlink` removido (carregava TikZ); ORCID em texto com link. SciPy com os 10 primeiros autores. Larguras das tabelas 1 e 2 e a expressão da Seç. 3.1 ajustadas para os Overfull hbox. | Título, referências, Seç. 2.4, 3.1–3.2 |
| Títulos do notebook | Tabelas 4, 5, 6 e 7, como no artigo. | Notebook |

## Redação
Além dos pontos dos pareceres, foram reescritas expressões de tom formulaico ("pilar", "é crucial destacar",
"transcende o mero ajuste de curvas", "é imperativo frisar", "é imprescindível", "cabe ressaltar", "mudança de paradigma",
"panaceia", "evidencia cuidados indispensáveis" etc.). Essas trocas também estão em vermelho.

## Não verificado aqui
- A compilação LaTeX não foi feita neste ambiente; compilar no Overleaf (pdfLaTeX, duas passagens, "Clear cached files").
- O notebook foi executado de ponta a ponta como script (Python 3.11.17, pyglam 1.1.0, NumPy 2.4.6, SciPy 1.17.1,
  pandas 2.3.3, Matplotlib 3.11.2); as tabelas 4, 5 e 7 saíram idênticas às anteriores.
