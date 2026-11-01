# Tutorial do paper final — "Quando vale a pena inspecionar?"

Roteiro para escrever o paper final da dissertação do Victor, em fases, com o que fazer, o que entregar e como saber que a fase terminou. O benchmark numérico tem tutorial próprio: [tutorial_benchmark.md](C:/Users/Storm/.claude-science/orgs/4f502a69-7cb9-4430-95d9-22d1f1625710/artifacts/proj_aa9f76ff3f27/57146a92-6097-466c-a438-b4b01a5fe7dd/v92a49361_tutorial_benchmark.md) e o script [tutorial_benchmark_g.py](tutorial_benchmark_g.py).

---

## 0. Esse é o paper?

**Sim, desde que três condições sejam cumpridas.** A pergunta é de engenharia, tem resposta numérica, usa o que o Victor já construiu (o emulador de g(t)) e ocupa um espaço que os dois concorrentes diretos deixam aberto:

- [Guo & Liang 2026](https://doi.org/10.1016/j.ress.2025.111761) decidem *quando inspecionar* um estado abstrato de carbonatação, sem medida física, sem espaço de projeto e sem valor da informação.
- [Wu et al. 2026](https://doi.org/10.1016/j.ress.2026.112817) calculam o valor da informação para cloretos, num único horizonte, sem idade de inspeção.

As três condições:

1. **Emulador validado pela decisão.** O Passo 2 do benchmark mostrou que o emulador atual subestima a cauda em idades baixas: P_f aos 20 anos é 0,005, contra 0,045 no simulador. Com inspeção isso quase não muda a decisão (arrependimento ≤ 0,0011·C₀), mas sem inspeção muda (0,0071·C₀). Retreinar o emulador ou apresentar esse diagnóstico como resultado é parte do paper, não um detalhe.
2. **Custos e erros de medida defensáveis.** Os λ precisam de fonte ou de faixa de sensibilidade, e σ_y e σ_c precisam de referência. Sem isso, um revisor da RESS ou da Structural Safety derruba o artigo.
3. **Resposta clara ao "por que emulador?".** O Possan é fórmula fechada e Monte Carlo direto é barato. A resposta honesta tem três partes:
   - o caso Possan é o banco de prova onde dá para *validar a decisão* tomada com o emulador contra a verdade;
   - os mapas no espaço de projeto exigem milhares de nuvens (pontos de projeto × idades × leituras);
   - o mesmo procedimento serve para modelos caros (numéricos, EDP), onde MC direto não cabe.

   Isso vai explícito na introdução e na discussão.

**Escopo recomendado para caber numa dissertação:** benchmark + mapas de VoI + validação pela decisão. As políticas de ciclo de vida com o reparo "Solução 1" (150 anos, sucessivos reparos) ficam como seção opcional ou como o paper seguinte.

**Revista-alvo:**
- Primeira opção: *Structural Safety* ou *Reliability Engineering & System Safety*, as duas onde os concorrentes publicaram.
- Plano B: *Structure and Infrastructure Engineering* ou *ASCE-ASME J. Risk Uncertainty Eng. Syst.*

Decidam a revista antes da Fase 5, porque ela muda o tamanho e o tom do texto.

---

## 1. Pergunta, título, contribuições e hipóteses (fixar na primeira semana)

**Pergunta.** Quando e o que vale a pena medir na gestão da durabilidade de elementos de concreto armado sujeitos à carbonatação?

**Título de trabalho.** *When is an inspection worth it? Value of condition information for carbonating reinforced concrete using a time-dependent stochastic emulator.*

**Contribuições** (texto já em inglês):
1. A pre-posterior value-of-information analysis of physical condition measurements (carbonation depth and cover) for carbonating RC elements, as a function of inspection age and over the design space {f_c, RH, c_nom}.
2. A conditioning scheme that turns a time-dependent stochastic emulator of the limit-state margin into a posterior predictor after an inspection, using the quantile coupling of the emulator, with no retraining.
3. A decision-oriented validation of the emulator: policy regret against direct Monte Carlo, showing when emulator error matters for the decision and when an inspection makes the decision robust to it.

**Hipóteses e o que já se sabe:**

| Hipótese | Enunciado | Evidência atual |
|---|---|---|
| H1 | O VoI tem pico numa idade intermediária | ✓ Pico aos 20 anos; paga o ensaio entre 15 e 45 anos (Passo 6) |
| H2 | A idade ótima depende de λ_corr/λ_prev e do erro de medida, mas fica numa faixa estreita | ✓ 15–25 anos nas 15 combinações consistentes do Passo 7 (emulador); 15–30 anos nas 21 consistentes da varredura anterior por MC |
| H3 | Com inspeção, a decisão tomada pelo emulador tem arrependimento desprezível | ✓ ≤ 0,0011·C₀ (Passo 6) |
| H4 | O VoI muda com o projeto: concreto fraco e cobrimento pequeno → pico mais cedo | A testar nos mapas (Fase 3) |
| H5 (opcional) | Medir o cobrimento vale tanto quanto medir a profundidade | Só com emulador de y(t); no protótipo por MC, o pacômetro aumentou o VoI de 0,0109 para 0,0148 |

---

## 2. Fases de trabalho

### Fase 0 — Preparação (semana 1)

- [ ] Ler os dois concorrentes com o quadro comparativo do [plano_redacao_paper_final.md](apoio/plano_redacao_paper_final.md).
- [ ] Ler Benítez et al. 2019, Lee et al. 2020 e Truong et al. 2022 (os trabalhos de inspeção/manutenção por carbonatação mais próximos). Anotar para cada um o modelo, o que é medido, a decisão e o que falta.
- [ ] Rodar o [tutorial_benchmark_g.py](tutorial_benchmark_g.py) e conferir com o [log de referência](saida_referencia/tutorial_run_log.txt).
- [ ] Decidir a revista-alvo.

**Pronto quando:** o Victor reproduz o benchmark sozinho e consegue explicar a tabela do Passo 4 no quadro.

### Fase 1 — Corrigir e validar o emulador (semanas 2–4)

- [ ] Diagnóstico (já feito): os 84,86 % do manuscrito são do emulador; o simulador dá 88 %. Registrar isso no Paper 1, se ainda estiver em revisão.
- [ ] Retreinar com mais nós de tempo (0, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100) e/ou com λ₃ e λ₄ previstos pela NN.
- [ ] Repetir os Passos 2 e 6. Meta: P_f do emulador dentro de ±0,01 do simulador entre 15 e 50 anos, e arrependimento sem inspeção próximo de zero.
- [ ] Se a meta não for atingida, manter o emulador atual e transformar o diagnóstico em resultado ("o erro de cauda muda a decisão a priori; a inspeção a corrige").

**Pronto quando:** a tabela do Passo 6 estiver final, com o emulador que vai para o paper.

### Fase 2 — Benchmark final (semanas 4–6)

- [ ] Fixar os custos:
  - λ_prev e λ_corr pelo SINAPI (reparo localizado em R$/m² ÷ custo da viga por m² de superfície);
  - λ_dep acima do limite físico (Passo 0), com sensibilidade 0,02–0,04;
  - λ_insp pela composição do ensaio.
- [ ] Fixar σ_y e σ_c com referência. Se não houver, usar uma faixa (1,5–5 mm) e mostrar a sensibilidade (Passo 7).
- [ ] Rodar o benchmark com m = 20 000 vigas virtuais e mostrar a convergência (m = 1000 / 5000 / 20 000 com 3 sementes).
- [ ] Fazer as figuras de publicação (Seção 4 abaixo).

**Pronto quando:** as Figuras 2–4 e as Tabelas 2–3 estiverem prontas.

### Fase 3 — Mapas de VoI no espaço de projeto (semanas 6–9)

- [ ] Montar uma grade f_c ∈ {20, 25, 30, 35, 40, 50} × c_nom ∈ {15, 20, 25, 30, 40, 50}, com UR = 55 % e mais um corte com UR = 75 %.
- [ ] Para cada ponto: nuvem do emulador (Passo 1) → VoI × idade (Passo 5) → idade ótima, VoI máximo e janela em que o ensaio se paga.
- [ ] Validar 6 pontos da grade contra o simulador (Passo 6). Esse é o teste de H3 fora do caso-base.
- [ ] Produzir mapas da idade ótima e do VoI máximo em (f_c × c_nom).

**Pronto quando:** existir o mapa e for possível escrever uma recomendação prática, por exemplo "para c_nom ≤ 20 mm e f_c ≤ 25 MPa, inspecionar entre X e Y anos".

### Fase 4 (opcional) — Políticas de ciclo de vida (semanas 9–11)

Fazer só se as Fases 1–3 fecharem no prazo. Comparar a política por cronograma com a política por condição em 150 anos, com o reparo "Solução 1". O protótipo E2 deu −38 % de custo. É preciso refazer com o objetivo corrigido (λ_dep e valor terminal).

### Fase 5 — Escrita (semanas 8–14, em paralelo)

Ordem de redação: Método → Resultados → Discussão → Introdução → Resumo e Conclusões.

### Fase 6 — Revisão e submissão (semanas 15–16)

- [ ] Pré-revisão interna (Marcos, Renata, Ketson), com a pergunta "o que um revisor da revista X atacaria?".
- [ ] Paper 1 submetido ou em preprint, porque o paper final cita o emulador.
- [ ] Código e dados num repositório com DOI (Zenodo), como a RESS e a Structural Safety esperam.

---

## 3. O paper seção por seção

| Seção | Tamanho | Conteúdo | Material pronto |
|---|---|---|---|
| 1 Introdução | 1,5 pág. | Problema do proprietário; o que Guo e Wu fizeram e o que falta; pergunta; 3 contribuições | Parágrafo de lacuna no [plano](apoio/plano_redacao_paper_final.md); [revisão integrada](apoio/revisao_bibliografica_integrada.md) |
| 2.1 Margem e modelo | 0,5 pág. | g = c − y, Possan, latentes, SSP2-4.5 | Manuscrito, Seção 4.1 (encurtar) |
| 2.2 Emulador | 0,5 pág. | Resumo do PyGLAM e acoplamento quantílico; citar o Paper 1 | Paper 1 |
| 2.3 Inspeção e atualização | 0,7 pág. | g_obs = c_obs − y_obs, σ_g, pesos w_u, posterior de g(t) | Passos 1 e 4 do benchmark |
| 2.4 Decisão e custos | 0,7 pág. | Ações R e E; custos; desconto; limite físico de λ_dep | Passos 0 e 3 |
| 2.5 VoI pré-posterior | 0,5 pág. | Experimento gêmeo; VoI; convergência | Passo 5 |
| 2.6 Validação pela decisão | 0,4 pág. | Os três mundos a/b/c; arrependimento | Passo 6 |
| 3.1 Exemplo de referência | 1,5 pág. | Nuvem, filtro, regra g* = 7,7 mm, VoI × idade | Passos 4–6, Fig. 2–3 |
| 3.2 Mapas de projeto | 1,5 pág. | Idade ótima e VoI máximo em (f_c × c_nom) | Fase 3 |
| 3.3 Validação e sensibilidade | 1 pág. | Arrependimento; λ, σ | Passos 6–7 e Fase 3 |
| 4 Discussão | 1,5 pág. | Recomendação prática; por que o emulador; limitações | — |
| 5 Conclusões | 0,5 pág. | 4–5 frases numeradas com números | — |

### Frases-guia para começar cada seção (em inglês, para adaptar)

- **Intro, 1º parágrafo:** "Owners of ageing reinforced concrete structures exposed to carbonation must decide when to inspect and when to repair, long before visible damage appears."
- **Intro, lacuna:** usar o parágrafo pronto do plano.
- **2.3:** "An inspection at age t_m provides a phenolphthalein carbonation depth y_obs and a cover-meter reading c_obs, from which the observed margin g_obs = c_obs − y_obs is formed with error standard deviation σ_g = (σ_y² + σ_c²)^{1/2}."
- **2.5:** "Since no field data are used, inspection outcomes are generated synthetically from the prior model (a twin experiment): each virtual element has a true trajectory, a noisy reading, an action chosen from the reading and a true cost."
- **3.1:** "At 20 years, the optimal rule is to repair if g_obs < 7.7 mm and to wait otherwise (Fig. X)."
- **4, por que emulador:** "The Possan model is a closed-form expression and direct Monte Carlo is inexpensive; it is used here precisely because it allows the emulator-based decisions to be checked against the exact ones."
- **4, limitações:** single element without spatial correlation; synthetic measurements; assumed measurement errors; Possan without independent validation and with weak CO₂ sensitivity; the combined-margin emulator cannot separate the value of each test.

---

## 4. Figuras e tabelas

| Nº | Conteúdo | Origem |
|---|---|---|
| Fig. 1 | Fluxograma: emulador → nuvem → leitura → filtro → custos → decisão → VoI | Desenhar |
| Fig. 2 | (a) nuvem e trajetórias filtradas para 3 leituras; (b) P_f(t) a priori e após cada leitura | Passos 1 e 4 |
| Fig. 3 | (a) custos esperados × g_obs e a regra g*; (b) VoI × idade (emulador, simulador, perfeita, custo do ensaio) | Passos 4–6 ([figura de trabalho](saida_referencia/passo8_figura_trabalho.png)) |
| Fig. 4 | P_f emulador × simulador por idade e arrependimento por idade | Passos 2 e 6 |
| Fig. 5 | Mapas de idade ótima e VoI máximo em (f_c × c_nom) | Fase 3 |
| Fig. 6 | Sensibilidade: VoI máximo e idade ótima × σ_g e × λ_corr/λ_prev | Passo 7 |
| Tab. 1 | Variáveis, distribuições e custos | Passo 0 |
| Tab. 2 | Exemplo numérico de três leituras: frações por tipo, E[R], E[E], decisão | Passo 4 ([CSV](saida_referencia/passo4_vigas_custos.csv)) |
| Tab. 3 | VoI e arrependimento por idade | Passo 6 ([CSV](saida_referencia/passo6_voi_idade.csv)) |

As figuras finais devem ter rótulos em inglês, unidades nos eixos e painéis (a), (b).

---

## 5. Perguntas que um revisor vai fazer (e a resposta)

| Pergunta | Resposta preparada |
|---|---|
| Por que um emulador, se o Possan é barato? | Caso de validação (Seção 4); mapas exigem milhares de nuvens; método vale para modelos caros |
| De onde vêm os custos? | SINAPI + faixa de sensibilidade; limite físico de λ_dep; resultado robusto (idade ótima de 15–25 anos) |
| As medidas são reais? | Não; experimento gêmeo, declarado no método. Campo é trabalho futuro |
| O emulador erra a cauda? | Sim, mostrado e quantificado; com inspeção o arrependimento é ≤ 0,0011·C₀ (ou: retreinado e corrigido) |
| E o clima? | O Possan quase não responde ao CO₂ (efeito < 1 ano na mediana de T); declarar e citar. A decisão de inspeção não depende do cenário |
| Diferença para Wu et al.? | Carbonatação, medida de condição, idade da inspeção como variável de decisão, espaço de projeto |
| Diferença para Guo & Liang? | Medida física, VoI explícito, espaço de projeto, validação da decisão contra MC |
| Por que o g e não y e c separados? | Suficiente para a decisão de curto prazo; separar os ensaios exige emular y(t), o que fica como extensão (ou Fase 1 alternativa) |

---

## 6. Cronograma resumido

| Semanas | Atividade | Entregável |
|---|---|---|
| 1 | Fase 0 | Benchmark reproduzido; revista escolhida |
| 2–4 | Fase 1 | Emulador retreinado ou diagnóstico final |
| 4–6 | Fase 2 | Figs. 2–4, Tabs. 1–3 |
| 6–9 | Fase 3 | Figs. 5–6 |
| 8–14 | Fase 5 | Rascunho completo |
| 9–11 | Fase 4 (opcional) | Seção de políticas |
| 15–16 | Fase 6 | Submissão |

---

## 7. Material de apoio

- [tutorial_benchmark.md](C:/Users/Storm/.claude-science/orgs/4f502a69-7cb9-4430-95d9-22d1f1625710/artifacts/proj_aa9f76ff3f27/57146a92-6097-466c-a438-b4b01a5fe7dd/v92a49361_tutorial_benchmark.md) — o passo a passo numérico.
- [tutorial_benchmark_g.py](tutorial_benchmark_g.py) — o script.
- [plano_redacao_paper_final.md](apoio/plano_redacao_paper_final.md) — posicionamento frente aos concorrentes e parágrafo de lacuna.
- [revisao_bibliografica_integrada.md](apoio/revisao_bibliografica_integrada.md) — revisão com 461 estudos.
- [exemplo_referencia_paper.md](apoio/exemplo_referencia_paper.md) — versão anterior do benchmark, por MC direto e com y e c separados (base da H5).
