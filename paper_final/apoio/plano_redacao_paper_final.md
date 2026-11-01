# Plano de elaboração do paper final da dissertação do Victor Hugo

## Parte A — Posicionamento e pergunta

### Posição frente aos concorrentes

A leitura completa de [Guo & Liang 2026](https://doi.org/10.1016/j.ress.2025.111761) e [Wu et al. 2026](https://doi.org/10.1016/j.ress.2026.112817) confirma o espaço do paper e o torna mais preciso. Guo & Liang decidem **quando inspecionar** um estado abstrato de deterioração por carbonatação. Wu et al. decidem **onde e o que medir** (parâmetros D e C_s de cloretos) num único horizonte. Nenhum dos dois responde à pergunta do proprietário de uma estrutura carbonatando: **com que idade vale fazer o ensaio de fenolftaleína e a pacometria, e como isso muda com f_c, UR e cobrimento, quando o reparo troca o material e a peça precisa manter β ≥ 1,3?**

| Dimensão | Guo & Liang 2026 (RESS) | Wu et al. 2026 (RESS) | Paper do Victor |
|---|---|---|---|
| Mecanismo | Carbonatação | Cloretos | Carbonatação |
| Física | EDP 1D de difusão-advecção-reação do CO₂ resolvida por PINN (100 pontos), só D_s aleatório | Fick em forma fechada, t₀ por erf | Possan (calibrado no Brasil) com latentes em f_c, UR e cobrimento; fib como teste de forma |
| Representação da incerteza | 21 estados substitutos hipo-exponenciais | Bayesiano hierárquico + PI-BNN + subset simulation | Distribuição completa e contínua no tempo de y(t) \| x (GLD-PCE-NN) |
| O que se observa | Estado discreto, acerto de 0,9 | D ou C_s num de 96 elementos | Profundidade carbonatada (σ ≈ 2,5 mm) e cobrimento (σ ≈ 1,5 mm), grandezas físicas |
| Decisão | Ação (nenhuma/preventiva/substituição) e data da próxima inspeção | Qual medida em qual elemento | Quando e o que medir, e quando reparar |
| Reparo | Renovação perfeita ao estado inicial | Custo por estado, sem renovação | "Solução 1": troca f_c pelo da argamassa, zera a idade, mantém o cobrimento |
| Restrição de serviço | Limiar de RUL para agendar | Estados definidos por β(50) frente a 1,3 (ISO 16204) | β(t) ≥ 1,3 (fib 34 / ISO 16204) em todo o horizonte |
| Clima | Só motivação e sensibilidade de D_s e K_T | — | Trajetória SSP como entrada; sensibilidade declarada fraca no Possan |
| Espaço de projeto | Um sistema | Uma estrutura | Todo o espaço {f_c, UR, c_nom} |
| Valor da informação | Não calculado | Calculado (NMC com 20 resultados) | Calculado e mapeado por idade e projeto |

Guo & Liang citam o trabalho anterior do Victor (Couto et al.) como abordagem puramente orientada a dados, sem interpretabilidade. A introdução pode responder diretamente: o PyGLAM não é um ajuste de ML, e sim um emulador da distribuição de um modelo mecanístico.

### Pergunta, título e contribuições

**Pergunta.** Quando e o que vale a pena medir na gestão da durabilidade de elementos de concreto armado sujeitos à carbonatação?

**Título de trabalho.** *When is an inspection worth it? Value of condition information for maintenance of carbonating reinforced concrete using a time-dependent stochastic emulator.*

**Contribuições (redação para o paper).**

1. A pre-posterior value-of-information analysis of physical condition measurements (carbonation depth and cover) for carbonating RC elements, mapped over inspection age and over the design space {f_c, RH, c_nom}.
2. A condition-based inspection–repair policy with non-identical renewal (patch repair with a different mortar, age reset, cover preserved) under a serviceability reliability target, compared with a prediction-based schedule.
3. A conditioning scheme for time-dependent stochastic emulators that exploits the comonotonicity of carbonation-depth trajectories, and a decision-oriented validation of the emulator (policy regret against direct Monte Carlo).

A quarta contribuição, opcional, é a sensibilidade das conclusões à forma do modelo (Possan × fib). Ela só entra se couber sem alongar o manuscrito; senão, vira o paper seguinte.

### Achado que define o método

A medida tem de condicionar o emulador. Testamos em Monte Carlo direto (10⁵ amostras, três pontos de projeto) e encontramos uma estrutura simples. As trajetórias de **profundidade** y(t) são comonotônicas no tempo: o Spearman entre 20 e 50, 20 e 100 e 30 e 60 anos é 1,000, e o maior deslocamento de posto é 0,2%. As trajetórias da **margem** g = c − y não são (Spearman de 0,973 a 0,982), porque o cobrimento é independente da profundidade.

Daí a decisão de desenho: **emular y(t) | x e tratar o cobrimento c como variável separada**. Uma leitura de fenolftaleína y_obs fixa o quantil u da trajetória de profundidade (atualização unidimensional, quase exata). Uma leitura de pacômetro c_obs atualiza c de forma independente. A probabilidade que guia a decisão, P[g(t+Δt) ≤ ε | y_obs, c_obs], vira uma integral em duas dimensões, barata para qualquer x, t e Δt. Isso também usa diretamente o acoplamento quantílico já construído no Paper 1, agora aplicado à grandeza para a qual ele é válido.

### Hipóteses

1. H1: a política por condição reduz o custo de durabilidade frente ao cronograma por previsão, e o ganho cresce com a dispersão de execução e com λ_corr/λ_prev. O protótipo deu 38% no caso do documento de discussão.
2. H2: medir o cobrimento vale tanto quanto medir a profundidade. No protótipo, o pacômetro dobrou o valor da informação.
3. H3: o valor da informação tem um máximo em idade intermediária. Cedo, a medida informa pouco; tarde, a peça já despassivou e não há decisão a mudar.
4. H4: as decisões mudam pouco com o erro do emulador (arrependimento pequeno frente a MC).

## Parte B — Estrutura do manuscrito

### Esqueleto do paper

A coluna "origem" indica de onde vem o material: o manuscrito atual (Paper 1, `texto/artigo`), o documento de discussão, os protótipos ([exemplos_metodos_resultados.md](exemplos_metodos_resultados.md)) ou trabalho novo.

| Seção | Conteúdo | Origem | Estado |
|---|---|---|---|
| 1 Introdução | Problema de gestão; lacuna (Guo, Wu, Benítez, Lee); pergunta; contribuições | Revisão integrada | Rascunho do parágrafo de lacuna abaixo |
| 2.1 Margem e modelo | g = c − y, Possan, latentes, CO₂ SSP2-4.5 | Manuscrito, Seção 4.1 | Adaptar (encurtar) |
| 2.2 Modelo de inspeção | Fenolftaleína com σ_y, pacômetro com σ_c, custo λ_insp | Protótipo E2/E4 | Adaptar |
| 2.3 Ações e reparo | Esperar, reparar; "Solução 1" | Documento de discussão, Seção 3 | Pronto |
| 2.4 Objetivo | Custo descontado (r real), termo de risco por ano despassivado, valor terminal, β(t) ≥ 1,3 | Documento de discussão, Seção 4, corrigido | Novo termo de risco |
| 2.5 Políticas | P0 cronograma por previsão; P1 por condição com y; P2 com y e c | Protótipo E2 | Adaptar |
| 3.1 Emulador | Resumo do PyGLAM, retreinado para y(t) \| x | Paper 1 | Retreinar para y |
| 3.2 Condicionamento | Quantil u fixado por y_obs; atualização de c; integral 2D | "Achado que define o método" | Novo |
| 3.3 Pré-posterior | VoI = E[custo sem dado] − E[custo com dado]; NMC com resultados discretizados | Protótipo E4; Wu et al. como referência de procedimento | Adaptar |
| 3.4 Validação pela decisão | Arrependimento da política e erro de VoI frente a MC | Novo | Novo |
| 4.1 Exemplo 1 | Ponto-base: posterior, decisão, VoI; emulador × MC | E4 | Refazer com emulador |
| 4.2 Exemplo 2 | Mapas de VoI por idade de inspeção e por (f_c, c_nom) | Novo | Novo |
| 4.3 Exemplo 3 | Políticas P0/P1/P2 em 150 anos: Λ, β(t), CVaR do custo, número de reparos; sensibilidades | E2 | Refazer com objetivo corrigido |
| 4.4 Exemplo 4 (opcional) | Possan × fib | Novo | Opcional |
| 5 Discussão | Quando e o que medir; β implícito; recomendações práticas; limitações | — | Escrever por último |
| 6 Conclusões | — | — | Por último |

### Roteiro de figuras

1. F1: fluxograma do método (emulador de y, atualização, pré-posterior, política).
2. F2: trajetórias e posterior de T após uma medida, com três leituras diferentes (base: E4).
3. F3: VoI × idade da inspeção para quatro pontos de projeto (testa H3).
4. F4: mapa de VoI em (f_c × c_nom) numa idade fixa, só profundidade × profundidade + cobrimento (testa H2).
5. F5: superfícies de custo e serrilhado de P_f das três políticas (base: E2).
6. F6: sensibilidade a λ_corr/λ_prev, r, σ_y e β_alvo.
7. F7: arrependimento do emulador frente a MC (testa H4).
8. F8 (opcional): Possan × fib.

### Lições dos dois artigos

Ambos passaram pela RESS, então mostram o que os revisores dessa revista aceitam.

- **De Wu et al.** O β_alvo = 1,3 citando ISO 16204, além do fib 34. A verificação explícita da estabilidade da estimativa de VoI com o número de resultados discretizados (eles usam 20). O gráfico de VoI líquido × custo de inspeção, cuja inclinação é −1, o que mostra que o custo não altera o ranking. A comparação adaptativa × estática. A análise de como o erro do surrogate afeta a decisão (Kendall τ), que corresponde à nossa Seção 3.4.
- **De Guo & Liang.** A comparação com um benchmark periódico nas mesmas hipóteses. A sensibilidade à precisão da observação (0,9/0,7/0,5), que no nosso caso é a variação de σ_y e σ_c. A tabela de custos por estado inicial, que no nosso caso é por idade da estrutura.
- **O que evitar.** O benchmark de Guo & Liang é do próprio grupo, e os custos são absolutos e arbitrários. Usaremos custos adimensionais (λ = C/C₀) com faixa de sensibilidade e, se possível, calibrados no SINAPI, item que já estava pendente no documento de discussão.

### Parágrafo de lacuna (rascunho)

> Inspection is valuable only when it can change a decision. For chloride-exposed marine structures, Wu et al. [Wu 2026] showed that value-of-information analysis can rank where and which durability parameters to measure, using a physics-informed Bayesian surrogate to make nested Monte Carlo tractable. For carbonation, Guo and Liang [Guo 2026] scheduled inspections from the remaining-useful-life distribution of a phase-type surrogate Markov process, in which inspections reveal an abstract discrete state and preventive maintenance restores the initial condition. Neither study addresses the question faced by the owner of an ageing carbonating structure: at what age do a phenolphthalein test and a cover survey pay for themselves, and how does the answer change with concrete strength, humidity and cover when a patch repair replaces the carbonated cover with a different mortar and the element must stay above the serviceability reliability target? Answering it requires the full, time-dependent conditional distribution of the carbonation depth for every design point and every inspection outcome, which a time-dependent stochastic emulator provides at negligible cost [Paper 1].

## Parte C — Execução

### Primeiras quatro semanas

1. **Semana 1 — texto e decisões.** Fixar o parágrafo de lacuna e as contribuições (seções "Pergunta, título e contribuições" e "Parágrafo de lacuna"). Esboçar as oito figuras à mão. Reconciliar o caso-base do Paper 1: o MC direto dá P[T ≤ 100] = 0,885 e o manuscrito reporta 84,86%. Ler Benítez et al. 2019, Lee et al. 2020 e Truong et al. 2022.
2. **Semana 2 — Seção 2 escrita.** Quase todo o material existe. Decidir o termo de risco; recomendo um custo λ_dep por ano em estado despassivado, mais um valor terminal para eliminar o reparo artificial em t = T_SL. Fixar os custos adimensionais.
3. **Semana 3 — referência por MC.** Refazer E2 e E4 com o objetivo corrigido, usando o código dos protótipos ([e_common.py](e_common.py), [e_sim.py](e_sim.py)). Esses resultados são o gabarito para validar o emulador.
4. **Semana 4 — ponto de decisão do método.** Retreinar o PyGLAM para y(t) | x, implementar o condicionamento descrito em "Achado que define o método" e comparar P[g(t+Δt) ≤ ε | dados] e o VoI com o MC da semana 3. Se o erro na decisão for pequeno, seguir para os mapas (Seção 4.2). Se não, usar MC direto nos exemplos e reposicionar o emulador como acelerador validado em parte do domínio.

Depois disso: mapas de VoI e políticas (semanas 5–9), redação dos resultados conforme as figuras ficam prontas (semanas 8–12), introdução, discussão e conclusões por último (semanas 12–14), pré-revisão pelos coautores da UMN (semana 15).

### Dependências e riscos

- **Paper 1.** O paper final cita o emulador. O ideal é o Paper 1 estar submetido, ou ao menos em preprint, antes da submissão.
- **Possan.** O modelo não tem validação independente em revista JCR e quase não responde ao CO₂ atmosférico. Declarar isso nas limitações. As conclusões sobre quando e o que medir dependem pouco do CO₂, o que protege o paper.
- **Objetivo sem custo de risco.** Os protótipos mostram que, sem ele, o ótimo é deixar despassivar e há uma decisão perversa de esperar com a peça já despassivada. O termo de risco é obrigatório.
- **Concorrência.** Wu et al. ocupam "VoI com surrogate informado pela física" na RESS. A diferença tem de aparecer já no resumo: carbonatação, medida de condição, idade da inspeção, reparo com troca de material e espaço de projeto.
