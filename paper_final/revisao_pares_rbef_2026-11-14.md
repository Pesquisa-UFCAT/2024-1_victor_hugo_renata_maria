# 🔬 PEER REVIEW REPORT

**Modelagem flexível de fenômenos físicos com a distribuição lambda generalizada: uma abordagem computacional didática com o pyGLAM**

**Parecer simulado em 14/11/2026: revisão maior antes da submissão.** O trabalho tem aderência à RBEF e uma contribuição didática defensável. Os principais problemas são corrigíveis e se concentram na interpretação das simulações, na reamostragem temporal, na documentação dos dados e na apresentação da proposta de ensino. Não identifiquei um impedimento científico irremediável que justifique recomendar rejeição.

**Escopo da revisão:** versão local de `paper_final/rbef_manuscrito_revisado`, incluindo todos os 15 arquivos `.tex`, três scripts, notebook, CSV, cinco figuras em português e log de compilação. As localizações abaixo são relativas a essa pasta; as linhas do notebook correspondem ao arquivo JSON original. A revisão se baseia nas fontes LaTeX, e não na leitura do PDF. O manuscrito original não foi editado. As verificações foram realizadas em `build/rbef_review_2026-11-14`.

**Calibração:** artigo expositivo e computacional com finalidade didática; física, modelagem probabilística e estatística; GLD na parametrização **FKML**, ajustada por momentos com `pyglam==1.1.0`, comparada a Rayleigh, Weibull e normal. O desenho não exige ensaio educacional, p-valores ou divisão treino/teste para sustentar uma demonstração descritiva. Tais exigências só seriam pertinentes a alegações adicionais de eficácia educacional, significância ou capacidade preditiva.

**Verificação computacional concluída:** todas as células de código do notebook foram executadas em sequência, sem modificar seu conteúdo, numa cópia isolada. Ambiente: Python 3.11.18, pyglam 1.1.0, NumPy 1.26.4, SciPy 1.17.1, pandas 3.0.5 e Matplotlib 3.8.4. As três tabelas reproduziram exatamente o texto fornecido, normalizadas as terminações de linha; os valores reportados de simulação e bootstrap também coincidiram na precisão publicada. Duas tentativas de otimização não selecionadas apresentaram pequenas diferenças em relação ao log fornecido, sem mudar as métricas finais ou a contagem de convergências. As figuras foram regeneradas, mas não são idênticas pixel a pixel aos PNGs originais; não foi estabelecida reprodução gráfica binária entre ambientes. Recomenda-se registrar também as versões das dependências no suplemento, para documentar essas diferenças. Esta execução verifica o percurso a partir do CSV, não a obtenção/transformação dos dados primários do INMET.

As [instruções da RBEF](https://www.scielo.br/journal/rbef/about/?ilang=pt_BR) contemplam artigos de física computacional com abordagem didática e materiais de ensino. A avaliação foi calibrada para essas modalidades, sem atribuir ao periódico um quartil ou fator de impacto não verificado.

## 👤 REVIEWER 1 — Metodologia

**Veredito: Major Revision.**

**Contribuição:** demonstra como interpretar, ajustar e criticar distribuições flexíveis usando dados meteorológicos reais. O contraste entre melhora descritiva e incompatibilidade de suporte é particularmente útil para ensinar que reproduzir momentos não basta para validar um modelo.

**Pontos fortes específicos:**

- `rbef_03_gld.tex:72`, `:75` e `:92` apresentam corretamente a derivada do quantil, a condição de validade e o domínio dos quatro momentos.
- `rbef_05_vento.tex:99` informa que “o modelo atribui probabilidade nula” a 84 observações e discute a consequência para a verossimilhança. Isso é uma limitação reconhecida e explorada didaticamente, não um erro oculto que, por si só, inviabilize o artigo.
- `rbef_04_dados_modelos.tex:80` distingue distância descritiva de teste de aderência; `rbef_06_temperatura.tex:15` reconhece dependência temporal e variabilidade interanual.
- Os três arquivos de tabelas podem ser confrontados diretamente com o CSV e o código de ajuste. A versão 1.1.0 da biblioteca foi obtida e usada na auditoria.

**Achados:**

1. **[MAJOR] Os blocos de vento não são necessariamente blocos de dias consecutivos.** `rbef_05_vento.tex:97`: “em blocos de dez dias consecutivos”. Entretanto, `rbef_notebook.ipynb:327` contém `serie_v = df['vento_ms'].dropna().to_numpy()` e a linha 329 aplica blocos de comprimento 10 a esse vetor. Ao remover os ausentes antes de construir os blocos, o código aproxima datas separadas por falhas. No CSV, há **101 intervalos maiores que um dia entre registros válidos**, e o maior é de **29 dias**. A autocorrelação calculada sobre esse mesmo vetor também não é estritamente a de defasagem de um dia; calculada por pares no calendário, ela ainda arredonda a 0,65, de modo que não se deve afirmar que esse número em particular esteja materialmente errado.

   **Correção:** preservar o calendário; formar blocos dentro de segmentos realmente consecutivos ou explicitar um tratamento de faltantes compatível com o alvo da análise. Calcular a autocorrelação com pares separados por um dia. Justificar o comprimento de dez dias e verificar sensibilidade a comprimentos próximos. Como a amostra agrega estações e anos — as médias mensais de vento variam aproximadamente de 2,10 a 2,75 m/s —, explicitar se o alvo é a distribuição histórica agregada e como a reamostragem trata essa heterogeneidade. Não é necessário transformar o artigo em estudo climatológico, mas é necessário que a incerteza estimada corresponda ao procedimento descrito.

2. **[MAJOR] A simulação não demonstra que quase todo o erro observado seja causado pelo arredondamento.** `rbef_05_vento.tex:97`: “quase todo o $D_n$ da GLD decorre da resolução das medições”; a afirmação reaparece em `rbef_07_consideracoes.tex:5`: “uma distância de Kolmogorov-Smirnov quase inteiramente explicada pelo arredondamento dos dados”. O experimento assume a GLD ajustada como verdadeira, gera observações independentes e compara a amostra ao modelo fixo. Isso mostra a escala que o arredondamento pode produzir **nesse cenário**, mas não decompõe a distância observada entre arredondamento, dependência, estimação e inadequação do modelo. Além disso, o valor observado 0,041 é maior que o percentil 95 simulado de 0,039. Isso não constitui um teste válido contra a GLD, mas tampouco autoriza tratá-lo como inteiramente explicado.

   **Correção mínima, suficiente para o caráter didático:** substituir a atribuição causal por “no cenário simulado de observações independentes, o arredondamento eleva a escala de referência de $D_n$ para valores próximos dos observados”. Manter explícitas as hipóteses e informar que não se trata de teste calibrado. Se desejarem concluir formalmente sobre aderência, o procedimento deve incorporar estimação, dependência e arredondamento, com reestimação quando pertinente. Não é obrigatório acrescentar esse teste se a redação permanecer descritiva.

3. **[MAJOR] A comparação entre desvio e erro-padrão é interpretada além do que foi calculado.** `rbef_05_vento.tex:97`: “Os desvios da GLD estão dentro dessa faixa” e “indica uma diferença real de forma”. A tabela informa desvio da mediana GLD de **+0,046 m/s**, enquanto o bootstrap fornece aproximadamente **0,033 m/s**. Eles são da mesma ordem, mas o primeiro não está dentro de uma faixa de um desvio padrão do segundo. Para o quantil de 5%, a saída apresenta desvio padrão bootstrap arredondado a **0,000**, mas o modelo difere em **−0,025 m/s**. O arredondamento torna o quantil empírico frequentemente idêntico entre reamostragens; isso não prova ausência de incerteza sobre o quantil da velocidade subjacente. Ademais, a incerteza de $Q_{empírico}$ não é automaticamente a incerteza de $Q_{modelo}-Q_{empírico}$, pois o modelo é estimado dos mesmos dados.

   **Correção:** apresentar uma pequena tabela com os três desvios e os três erros-padrão, identificar a degenerescência do quantil de 5% e distinguir o quantil dos registros arredondados do quantil da grandeza contínua. Empregar “mesma ordem de grandeza” e “diferença descritiva”, sem equivaler a um teste de significância. Se mantiverem uma conclusão inferencial sobre diferenças entre modelos, reamostrar e reajustar os modelos para avaliar a discrepância de interesse. A leitura da normal em `rbef_06_temperatura.tex:58` pode permanecer como argumento de parcimônia descritiva, sem ser apresentada como validação formal da adequação.

4. **[MAJOR] Falta documentar a construção das médias diárias e separar precisão de registro de resolução instrumental.** `rbef_04_dados_modelos.tex:60` promete documentar “instrumental associado”; `rbef_05_vento.tex:11` informa “velocidades médias diárias” e “resolução de $0,1\,\text{m/s}$”. O suplemento começa com o CSV já agregado. O notebook estima essa suposta resolução pelo menor espaçamento entre valores distintos; isso identifica a grade dos registros, não necessariamente a resolução do sensor. Não se especifica se a média diária veio pronta do INMET ou foi calculada, quais horários a compõem, o fuso, o requisito de completude nem o tratamento de dias parcialmente observados. A afirmação em `rbef_06_temperatura.tex:58` de que a incerteza do sensor “pouco altera a forma” também não é sustentada por metadados instrumentais.

   **Correção:** incluir uma ficha dos dados com produto/consulta exata, data de obtenção, campos originais, definição de média diária, critérios de completude e etapas de transformação; fornecer o script de preparação ou documentar o produto diário oficial, conforme o caso. Identificar sensor, altura de medição do vento e mudanças conhecidas quando disponíveis; caso não disponíveis, declarar a limitação. Usar “passo de registro/arredondamento de 0,1 m/s” até haver documentação metrológica. O [portal oficial do INMET](https://portal.inmet.gov.br/dadoshistoricos) é um ponto de acesso verificável, mas o link genérico não substitui a identificação do produto efetivamente usado.

5. **[MINOR] O coeficiente de variação em Celsius não tem interpretação física invariável.** `tab_descritiva.tex:5`: “Coeficiente de variação & 0{,}303 & 0{,}076”. O valor da temperatura resulta de dividir o desvio padrão pela média em Celsius. A mesma série em kelvin produz aproximadamente **0,00501**, sem qualquer mudança na variabilidade física. **Correção:** retirar a célula da temperatura e explicar por quê, ou calcular em kelvin e informar a escala. Essa restrição é explicitada pelo [NIST](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/coefvari.htm). O CV do vento continua apropriado.

## 👤 REVIEWER 2 — Domínio e novidade

**Veredito: Major Revision.**

**Preenche uma lacuna real?** Há espaço para um percurso em português que articule quantis, momentos, suporte, arredondamento e interpretação física com código acessível. A contribuição é a organização didática dessa sequência e dos dois exemplos. A GLD, a parametrização FKML e o ajuste de distribuições por software são anteriores ao artigo; isso já é reconhecido no histórico e na tabela de ferramentas. O [artigo de Su sobre GLDEX](https://www.jstatsoft.org/article/view/v021i09) e a [documentação do pacote gld](https://cran.r-project.org/web/packages/gld/gld.pdf) confirmam a existência prévia de ajustes e diagnósticos. Não encontrei base para alegar inexistência de contribuição, nem para certificar uma prioridade mundial a partir de uma busca bibliográfica dirigida.

**Achados:**

1. **[MAJOR] A proposta precisa tornar mais concreta sua contribuição para o professor e o estudante.** `rbef_02_introducao.tex:58`: “Ao final do percurso proposto, o leitor deverá ser capaz de interpretar a matemática de uma função quantil”. Há objetivos gerais e boa exposição, mas não se delimitam com clareza público, pré-requisitos, duração ou atividades pelas quais o estudante demonstraria essas capacidades. O notebook tem código e títulos de etapas, mas poucas intervenções para provocar previsões e discutir respostas.

   **Correção:** acrescentar uma subseção curta com público-alvo e pré-requisitos — probabilidade básica, cálculo e Python, conforme a intenção dos autores —, roteiro de uso e três ou quatro tarefas com respostas esperadas. Exemplos diretamente ligados ao conteúdo: prever o efeito de dobrar $\lambda_2$; explicar por que momentos coincidentes não garantem suporte adequado; justificar a manutenção da normal no exemplo de julho; explicar por que médias diárias não determinam potência eólica. Uma tabela “objetivo → atividade → evidência esperada” basta. **Não exijo aplicação em sala:** `rbef_07_consideracoes.tex:9` já afirma corretamente que o trabalho “não permite afirmar ganhos de aprendizagem”.

2. **[MINOR] A premissa educacional do resumo é mais abrangente que a evidência apresentada.** `rbef_01_resumo.tex:2`: “A distribuição normal costuma ser a única referência apresentada aos estudantes”. A introdução documenta sua centralidade em textos de erros e incertezas, não que seja a única referência oferecida aos estudantes em geral. **Correção:** trocar por “A distribuição normal ocupa posição central em muitos cursos introdutórios de tratamento de dados” e ajustar o resumo em inglês. Alternativamente, delimitar cursos e sustentar a afirmação com pesquisa curricular pertinente.

3. **[MINOR] Uma referência não sustenta o uso específico que lhe é atribuído.** `rbef_02_introducao.tex:9`: “propagação de distribuições por simulação de Monte Carlo~\cite{gums1,ribeiro2025}”. O [artigo de Ribeiro-Silva e Ribeiro-Silva](https://www.scielo.br/j/rbef/a/Q8wQCgsgLYFSSRnbtFFJZHF/?format=html) trata de mínimos quadrados e propagação de incertezas sem derivadas; seu conteúdo consultado não apresenta a propagação por Monte Carlo atribuída nessa frase. **Correção:** manter `gums1` para Monte Carlo e deslocar `ribeiro2025` para a contextualização de abordagens didáticas de ajuste e incertezas, ou substituir por uma referência que efetivamente demonstre a técnica mencionada.

4. **[MINOR] A explicação meteorológica é plausível, mas apresentada como mecanismo identificado na amostra.** `rbef_06_temperatura.tex:62`: “Essa assimetria tem uma origem física identificável” e “sem um mecanismo equivalente que produza dias anormalmente quentes na mesma proporção”. O artigo analisa a temperatura, sem classificar frentes ou massas de ar nos eventos observados. **Correção:** citar literatura climatológica específica e escrever “uma explicação física plausível é...”. Atribuir os dias extremos a eventos determinados exigiria evidência adicional; essa atribuição não é necessária para o objetivo didático.

## 👤 REVIEWER 3 — Lógica, narrativa e apresentação

**Veredito: Minor Revision nos aspectos próprios de apresentação; acompanha Major Revision nas interpretações metodológicas identificadas acima.**

**Achados:**

1. **[MINOR] Parâmetros transcritos e precisão do suporte não são consistentes.** `rbef_05_vento.tex:50` informa “(2,191;\, 1,727;\, 0,556;\, 0,099)”, enquanto `saida_notebook.txt:20` registra `[2.191 1.727 0.555 0.099]`. Em `rbef_06_temperatura.tex:30`, o parâmetro de forma esquerdo é “0,018”; em `saida_notebook.txt:43`, aparece `1.7000e-02`. Usando literalmente os parâmetros de temperatura impressos na equação de suporte, obtém-se limite inferior de aproximadamente **−32,3 °C**, e não os **−33,9 °C** informados em `rbef_06_temperatura.tex:60`. A discrepância não invalida o ajuste, mas dificulta reproduzir o exemplo no próprio texto. **Correção:** gerar parâmetros automaticamente da execução e apresentar casas suficientes para reproduzir os limites, ou avisar que estes usam parâmetros não arredondados disponibilizados no suplemento.

2. **[MINOR] O número de anos da precipitação precisa distinguir duração e anos civis.** `rbef_06_temperatura.tex:70`: “uma série de 25 anos fornece no máximo 25 máximas anuais”. O arquivo abrange partes de **26 anos civis**, 2000–2025, e `saida_notebook.txt:56` informa “Anos com dados: 26”. Há 24 anos civis integralmente contidos no intervalo, 2001–2024, antes de avaliar faltantes. **Correção:** substituir por “cerca de duas dezenas de blocos anuais completos, após os critérios de completude” ou fornecer a contagem segundo um critério explícito. Os **25 julhos** de 2000–2024 estão corretos e não devem ser alterados.

3. **[MINOR] O gráfico Q-Q omite justamente os valores excluídos pelo suporte, sem informar o recorte na legenda.** `rbef_05_vento.tex:87` descreve apenas “gráfico quantil-quantil”; `rbef_notebook.ipynb:370` usa `pr = np.linspace(0.01, 0.99, 99)`. Os 84 valores fora do suporte representam 0,95% da amostra e ficam abaixo do início desse diagnóstico. O problema é discutido honestamente no texto, mas pouco visível na figura que deveria apoiar a discussão. **Correção:** explicitar na legenda o intervalo 1%–99% e incluir um detalhe da cauda inferior ou a linha vertical do suporte com destaque para as observações excluídas. Informar também o recorte do Q-Q de temperatura, que reutiliza a grade.

4. **[MINOR] Ajustes editoriais e de compilação antes de empacotar a submissão.** `preamble.tex:13` contém `\usepackage{orcidlink}`; o log confirma que ele carrega `tikz.sty` indiretamente. As instruções da RBEF dizem que “não deve ser utilizado o pacote TikZ”. `referencias.tex:37` usa “P. Virtanen, R. Gommers, T.E. Oliphant \textit{et al.}”, enquanto a orientação atual só admite abreviar após o décimo autor. **Correção:** substituir os ícones ORCID por links de texto e adequar a entrada do SciPy. A revista aceita fontes `.tex`, utiliza `\bibitem` e não exige template oficial; portanto, a ausência de `.bib` ou de classe própria da RBEF não é problema. [Instruções aos autores](https://www.scielo.br/journal/rbef/about/?ilang=pt_BR).

**Auditoria cruzada de consistência — divergências encontradas:**

| Localizações | Evidência e divergência | Classificação / encaminhamento |
|---|---|---|
| `rbef_05_vento.tex:50`; `saida_notebook.txt:20` | $\lambda_3$ do vento 0,556 no texto; 0,555 na saída | MINOR: sincronizar parâmetros e precisão |
| `rbef_06_temperatura.tex:30`; `:60`; `saida_notebook.txt:43` | $\lambda_3$ da temperatura 0,018 versus 0,017; parâmetros impressos dão limite −32,3 °C, texto dá −33,9 °C | MINOR: usar parâmetros consistentes e suficientemente precisos |
| `rbef_05_vento.tex:50`; `saida_notebook.txt:25`; `:30` | Texto: “dois terminaram em outra solução válida”; saída: vetores distintos, com $\lambda_3$ 0,2127 e 0,2489 e custos 0,0279 e 0,0282 | MINOR: escrever “duas tentativas terminaram em soluções válidas de maior resíduo”, sem sugerir uma única raiz alternativa |
| `rbef_05_vento.tex:97`; `tab_vento.tex:3`; `saida_notebook.txt:51` | “dentro dessa faixa”: desvio da mediana 0,046 m/s, DP bootstrap 0,033 m/s | Parte do MAJOR metodológico: mesma ordem não significa dentro de um DP |
| `rbef_01_resumo.tex:2`; `rbef_07_consideracoes.tex:5`; `saida_notebook.txt:51` | Generalização “ao nível da incerteza amostral” para os quantis; DP bootstrap de $Q_{0,05}$ aparece como 0,000 e desvio GLD é −0,025 m/s | Parte do MAJOR metodológico: distinguir quantis e efeito da discretização |
| `rbef_05_vento.tex:97`; `rbef_notebook.ipynb:327` | “dez dias consecutivos” versus vetor com `dropna()` | MAJOR: corrigir calendário e reamostragem |
| `rbef_04_dados_modelos.tex:64`; `rbef_05_vento.tex:11`; `rbef_06_temperatura.tex:13` | Protocolo anuncia janelas homogêneas; temperatura estratifica julho, vento reúne todo o período | Esclarecer o alvo histórico agregado; não é proibido modelar uma mistura, mas isso precisa ser coerente com o protocolo |
| `rbef_06_temperatura.tex:70`; `saida_notebook.txt:56` | Máximo de 25 blocos anuais versus 26 anos civis representados | MINOR: separar anos completos de frações de ano |
| `rbef_notebook.ipynb:176`; `:213`; `:261` e ordem das tabelas LaTeX | Notebook chama as tabelas numéricas de 2, 3 e 4; no artigo são 4, 5 e 6, após ferramentas, parâmetros e modelos físicos | MINOR: corrigir títulos do notebook |

**Valores conferidos sem divergência relevante:**

- 9.121 registros = 8.840 registros válidos de vento + 281 ausentes; período de 06/05/2000 a 25/04/2025, sem datas duplicadas.
- 768 temperaturas válidas de julho em 25 anos, de 2000 a 2024; faltam sete dos 775 dias de julho possíveis.
- Médias, desvios padrão com divisor $n$, assimetrias, curtoses, extremos e quantis das tabelas concordam com o CSV nos algarismos publicados.
- Distâncias de vento 0,242 / 0,085 / 0,041 e de temperatura 0,064 / 0,041 concordam entre tabelas, narrativa e saída computacional; os desvios quantílicos também concordam.
- 84/8.840 = 0,9502%, coerente com 0,95%; 11 de 15 tentativas próximas da solução selecionada, duas outras válidas e duas fora do domínio totalizam 15.
- 8.759 observações de precipitação, das quais 5.675 são zero, concordam com o CSV.
- Os resumos português e inglês mantêm a mesma mensagem. Não há no resumo uma métrica numérica conflitante com o corpo.

**Auditoria de alegações do resumo e da conclusão:**

| Alegação | Suporte encontrado | Avaliação |
|---|---|---|
| Ensino da FKML, quatro parâmetros e momentos (`rbef_01_resumo.tex:2`) | Equações, tabela de parâmetros, figuras e código | Sustentada |
| Dois conjuntos INMET e comparações com Rayleigh/Weibull/normal (`:2`) | CSV, critérios de recorte e tabelas | Sustentada; completar proveniência |
| Vento: redução de discrepâncias e exclusão de dias fracos (`:2`; `rbef_07_consideracoes.tex:5`) | Tabela e 84 observações fora do suporte | Sustentada como descrição da amostra |
| Desvios de vento “ao nível da incerteza amostral” (`:2`; conclusão `:5`) | Simulação e bootstrap dos quantis | Parcial; delimitar quantis e corrigir os pontos metodológicos |
| Distância “quase inteiramente explicada” pelo arredondamento (conclusão `:5`) | Cenário simulado com GLD fixa e independência | Excesso de conclusão causal; é uma estimativa condicional, não uma decomposição medida |
| Normal defensável para julho (`rbef_01_resumo.tex:2`; conclusão `:5`) | Discrepâncias pequenas em relação à escala bootstrap reportada | Defensável como julgamento descritivo para os quantis analisados; não como validação geral de aplicações térmicas |
| Vantagem dos quantis e da transformação inversa (conclusão `:7`) | Derivações e exemplos de código | Sustentada matematicamente; propagação de incertezas é uma aplicação possível, não um estudo de caso executado |
| Ausência de ganhos de aprendizagem demonstrados (conclusão `:9`) | Sem intervenção educacional relatada | Limitação corretamente declarada |
| Notebook reproduz o material (resumo `:2`; conclusão `:11`) | Todas as células executadas; tabelas, métricas e simulações conferidas | Sustentada na precisão publicada para os resultados centrais; registrar ambiente, pequenas variações de candidatos e proveniência anterior ao CSV |

**Auditoria de integridade LaTeX:**

- **32 rótulos, 38 chamadas de referências cruzadas e 26 entradas bibliográficas**; nenhum rótulo duplicado, alvo ausente ou chave de citação inexistente. Todas as entradas bibliográficas são citadas.
- Bibliografia manual em `referencias.tex`, com `\bibitem`; não há `.bib` nesta versão e isso não é defeito.
- Todos os arquivos chamados por `\input`, `\includegraphics` e `\lstinputlisting` existem. As cinco figuras foram inspecionadas: não identifiquei troca de painéis, eixos ou modelos.
- Não foram encontrados `TODO`, `FIXME`, placeholders ou marcações de revisão em vermelho nos `.tex` e scripts examinados.
- O `main.log` original termina com “There were undefined citations” (`main.log:1512`) e “There were undefined references” (`:1526`). Na cópia isolada, **duas passagens de `pdflatex` concluíram com sucesso**, resolveram esses avisos e geraram 26 páginas. Trata-se de artefato de compilação incompleta, não de alvos ausentes nas fontes. O título foi alterado depois do PDF/log original, que portanto também estava desatualizado em relação a essa fonte.
- Persistem quatro avisos `Overfull \hbox`, aproximadamente 2,0; 8,7; 13,4 e 7,1 pt: dois na tabela de ferramentas (`rbef_02_introducao.tex:44` e `:47`), um no parágrafo da representação paramétrica da densidade (`rbef_03_gld.tex:21`) e um na tabela de parâmetros (`:49`). Verificar larguras de colunas e quebra da expressão matemática antes da versão final; avisos `Underfull` são de espaçamento, sem evidência de conteúdo perdido.
- Remover a dependência indireta de TikZ indicada acima e conferir o PDF gerado pelo sistema de submissão. Não enviar arquivos auxiliares `.aux`, `.log`, `.out` e `.synctex.gz` como conteúdo científico.

## 🎓 DECISÃO EDITORIAL

**Consenso:** a matemática central e as comparações numéricas são defensáveis; os autores reconhecem corretamente a limitação de suporte e a ausência de validação educacional. A parte mais frágil é o salto da descrição para a interpretação de incerteza e de causas das discrepâncias. A contribuição pedagógica ficará mais clara com um roteiro curto de uso, e a documentação dos dados precisa permitir reconstruir o significado das médias diárias.

**Decisão realista simulada para a RBEF: Major Revision.** Não recomendaria submeter esta versão antes de resolver os itens metodológicos. Não identifiquei um **[BLOCKER] científico** que exija abandonar o artigo ou obter um novo conjunto de dados. Os requisitos formais de submissão precisam ser atendidos mesmo quando a correção é simples. Esta é uma simulação, não uma previsão da decisão do editor.

**Adequação:** melhor enquadramento em **Artigos Gerais**, com ênfase didática e computacional; **Produtos e Materiais Didáticos para o Ensino de Física** pode ser considerado se o roteiro educacional ganhar protagonismo. Eu manteria a RBEF como alvo. Não vejo necessidade de sugerir outro periódico, nem de converter o trabalho em pesquisa empírica de aprendizagem. [Escopo e modalidades da RBEF](https://www.scielo.br/journal/rbef/about/?ilang=pt_BR).

**Ações priorizadas:**

1. Corrigir o bootstrap do vento para respeitar datas, justificar os blocos e verificar quanto isso altera as incertezas publicadas.
2. Reescrever a interpretação de $D_n$ e dos desvios quantílicos; sincronizar corpo, resumo português, abstract e conclusão. Se o objetivo continuar descritivo, não é necessário acrescentar testes de hipóteses.
3. Documentar a origem e a construção das médias diárias; distinguir grade de registro, resolução instrumental e incerteza amostral.
4. Acrescentar público-alvo, pré-requisitos, roteiro e tarefas com respostas esperadas, sem alegar eficácia não avaliada.
5. Corrigir o CV da temperatura, as transcrições dos parâmetros, o número de blocos anuais, a citação de Monte Carlo e as afirmações meteorológicas excessivamente categóricas.
6. Tornar visível o problema de suporte no gráfico; atualizar os títulos das tabelas no notebook; adequar ORCID/referências às instruções da RBEF; recompilar o pacote final.

**Sugestão de redação para a conclusão, após a revisão da reamostragem:** “Nos dados de vento, a GLD ajustada por momentos apresentou menores discrepâncias nos quantis examinados que os modelos de referência, embora seu suporte exclua 0,95% das observações. As simulações ilustram que o arredondamento modifica substancialmente a escala da distância de Kolmogorov–Smirnov, sem estabelecer uma decomposição das causas da discrepância observada. Nas temperaturas de julho, as diferenças nos quantis avaliados são pequenas diante das escalas de variabilidade amostral estimadas, tornando a normal uma alternativa parcimoniosa para essa descrição. Os exemplos constituem uma proposta didática cuja eficácia educacional permanece por avaliar.”
