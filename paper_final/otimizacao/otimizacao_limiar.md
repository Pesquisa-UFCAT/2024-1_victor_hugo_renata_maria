# Otimização do limiar de reparo e do intervalo de inspeção — formulação e roteiro

Documento de trabalho para construir o problema de otimização: **com que margem g_lim reparar e com que frequência inspecionar, para ter o menor número de manutenções em 100 anos sem violar a confiabilidade exigida.**

- Catálogo de ações de manutenção e custos: [acoes_manutencao_custos.md](acoes_manutencao_custos.md).
- Código-base: [otimizacao_limiar.py](otimizacao_limiar.py). Ele roda de ponta a ponta. Com os `.pkl` do emulador em `durability/`, usa o PyGLAM. Sem eles, usa um substituto com a mesma interface (quantis do Possan).
- Saída de referência: [saida_referencia/](saida_referencia/). Foi gerada com o **substituto**, porque os `.pkl` não estavam no repositório. Com o emulador, os números mudam um pouco.

---

## 1. A pergunta e por que ela precisa de uma restrição

> Qual margem de segurança g_lim, e com que intervalo de inspeção Δt, minimiza o número de reparos ao longo de 100 anos?

Se o único objetivo for "menos reparos", a resposta é **nunca reparar**: zero reparos e 89 % das vigas despassivadas aos 100 anos, no caso-base. O problema só tem solução útil quando o número de reparos é minimizado **sujeito a uma exigência de desempenho**: β ≥ β_alvo, um custo, ou um segundo objetivo de risco. Toda a literatura citada na Seção 6 faz isso de algum modo.

---

## 2. Notação

| Símbolo | Significado |
|---|---|
| x = (f_c, UR, c_nom) | Projeto da viga (MPa, %, mm) |
| G(u, τ; x) | Nuvem do emulador: margem da trajetória de quantil u ∈ (0,1) na idade τ do material, para o projeto x |
| T = 100 anos | Horizonte |
| θ = (t₁, Δt, g_lim, f_c,rep) | Política: 1ª inspeção, intervalo, limiar de reparo, resistência da argamassa |
| σ_g = √(σ_y² + σ_c²) = 2,92 mm | Erro da margem medida (fenolftaleína + pacômetro) |
| d = 1/(1+r), r = 4 % | Fator de desconto |
| λ_insp, λ_prev, λ_corr, λ_dep | Custos (× C₀): inspeção, reparo preventivo, reparo corretivo, risco por ano despassivado |

---

## 3. Modelo da política

### 3.1 Trajetória de uma viga com reparos

A viga *i* começa com o quantil u_{i,0} ~ U(0,1) no projeto original x₀ = x. Depois do k-ésimo reparo, feito no ano t_{i,k}, ela passa a seguir uma trajetória nova, no projeto da argamassa e com idade zerada:

$$
g_i(t) = G\big(u_{i,k},\; t - t_{i,k};\; x_k\big), \qquad x_k = (f_{c,\mathrm{rep}},\, UR,\, c_\mathrm{nom}),\quad u_{i,k}\sim U(0,1),\quad t_{i,0}=0 .
$$

Dentro de cada ciclo, g não cresce: no código, aplica-se o mínimo acumulado.

### 3.2 Inspeção e regra de reparo

As inspeções ocorrem em τ_j = t₁ + (j−1)·Δt, para τ_j < T. A leitura é

$$
\hat g_{ij} = g_i(\tau_j) + \varepsilon_{ij}, \qquad \varepsilon_{ij} \sim N(0, \sigma_g^2).
$$

**Regra:** repara se ĝ_ij ≤ g_lim. O reparo é **preventivo** se a armadura ainda está passivada (g_i(τ_j) > 0) e **corretivo** se já despassivou.

### 3.3 Hipóteses a declarar no paper

1. **H-a, cobrimento após o reparo:** o reparo refaz o cobrimento com a argamassa e nova variabilidade de execução. Por isso u_{i,k} é sorteado de novo. Manter o cobrimento real da viga ("Solução 1" pura) exige emular y(t) e tratar c à parte; fica como alternativa.
2. **H-b, independência:** u_{i,k} é independente de u_{i,k−1}. O ambiente (UR) é o mesmo, então há alguma correlação real. Testar a sensibilidade com cópula ou com o mesmo latente de UR.
3. **H-c, CO₂ no calendário:** o emulador foi treinado com construção em 1980. Uma argamassa aplicada em 2030 vê mais CO₂ na mesma idade. Como o Possan responde pouco ao CO₂ (+800 ppm dá ×1,03 na profundidade), o erro é pequeno, mas precisa ser declarado. A alternativa é treinar o emulador com o ano de construção como entrada.
4. **H-d, argamassa:** a argamassa usa os mesmos coeficientes do Possan (CP II F), mudando só f_c. f_c,rep tem de ficar dentro do domínio do emulador (20–50 MPa).

---

## 4. Medidas de desempenho (estimadas por Monte Carlo com M vigas)

| Medida | Definição | Estimador |
|---|---|---|
| Nº de reparos | N_rep,i = Σ_j 1[ĝ_ij ≤ g_lim] | E[N_rep] ≈ (1/M) Σ_i N_rep,i |
| Nº de inspeções | N_insp = #{j : τ_j < T} | Determinístico |
| Risco ao longo da vida | P_desp = P(∃ t ≤ T : g(t) ≤ 0) | Fração das vigas que despassivaram ao menos uma vez |
| Confiabilidade instantânea | P_f(t) = P[g(t) ≤ 0]; β(t) = −Φ⁻¹(P_f(t)) | Fração em cada ano |
| Repetição | P(N_rep ≥ 2) | Fração |
| Custo do ciclo de vida | C_i = Σ_j d^{τ_j}[λ_insp + λ_prev·1_prev + λ_corr·1_corr] + λ_dep Σ_t d^t·1[g_i(t) ≤ 0] | E[C] ≈ média |

O erro padrão de P_desp é √(p(1−p)/M). Com p ≈ 0,097 e M = 20 000, ele vale 0,002.

**Qual medida de confiabilidade usar como restrição?** A fib 34 define a despassivação como evento de primeira passagem até a vida útil, ou seja, P_desp. Com reparos, P_f(t) instantânea fica serrilhada (cai depois de cada reparo). Recomendo usar P_desp como restrição principal e mostrar β(t) como figura.

---

## 5. Formulações

### F1 — menor número de reparos com confiabilidade garantida

$$
\min_{\theta}\; \mathbb{E}[N_\mathrm{rep}(\theta)]
\quad\text{s.a.}\quad P_\mathrm{desp}(\theta) \le \Phi(-\beta_\mathrm{alvo}) = 0{,}097\ (\beta_\mathrm{alvo}=1{,}3),
\qquad N_\mathrm{insp}(\theta) \le N_\mathrm{max}.
$$

Sem o limite N_max, o ótimo empurra para inspeções muito frequentes, porque inspecionar mais permite uma margem menor. Na prática, **inspeção também é manutenção**. Use N_max, ou desempate por N_insp.

### F2 — menor custo do ciclo de vida com confiabilidade garantida

$$
\min_{\theta}\; \mathbb{E}[C(\theta)] \quad\text{s.a.}\quad P_\mathrm{desp}(\theta) \le \Phi(-\beta_\mathrm{alvo}).
$$

É a formulação clássica (Kong & Frangopol 2003; Mori & Ellingwood 1994). O ótimo em g_lim é interior: margem pequena gera corretivo e anos despassivados; margem grande gera reparos demais.

### F3 — multiobjetivo, recomendada como resultado principal

$$
\min_{\theta}\; \Big\{\, \mathbb{E}[N_\mathrm{rep}(\theta)],\; N_\mathrm{insp}(\theta),\; P_\mathrm{desp}(\theta) \,\Big\}
\quad\Rightarrow\quad \text{fronteira de Pareto.}
$$

O gestor escolhe na fronteira. A restrição β entra como um corte vertical. Esse é o formato de Liu & Frangopol (2005), Okasha & Frangopol (2010) e Barone & Frangopol (2014).

### F4 — projeto + manutenção (extensão)

Inclua c_nom (e/ou f_c) em θ, com custo inicial C₀(c_nom):

$$
\min_{\theta,\,c_\mathrm{nom}}\; C_0(c_\mathrm{nom}) + \mathbb{E}[C(\theta; c_\mathrm{nom})]
\quad\text{s.a.}\quad P_\mathrm{desp} \le \Phi(-\beta_\mathrm{alvo}).
$$

Responde à pergunta "vale mais pôr 5 mm a mais de cobrimento ou inspecionar mais?". É aqui que o emulador se paga, porque cada c_nom é uma nuvem nova.

### Variáveis e domínio

| Variável | Tipo | Faixa sugerida | Observação |
|---|---|---|---|
| t₁ | inteira | 5–30 anos | A 1ª inspeção tem de vir antes da cauda inicial de despassivação |
| Δt | inteira | 5–25 anos | |
| g_lim | contínua | 0–16 mm | O Paper 1 já usa 0–12 mm |
| f_c,rep | contínua | 25–50 MPa | Domínio do emulador: 20–50 MPa |
| c_nom (F4) | contínua | 15–60 mm | Domínio do emulador |

**Armadilha a evitar.** Se a argamassa melhor não custar mais, o otimizador sempre escolhe f_c,rep = 50 MPa (é o que acontece na saída de referência). Para f_c,rep ser variável de decisão de verdade, é preciso um custo crescente, por exemplo λ_prev(f_c,rep) = λ_prev,0·[1 + a(f_c,rep − 30)/20]. Se não houver dado de custo, **fixe f_c,rep** e trate como sensibilidade.

---

## 6. Como outros autores formularam problemas parecidos

A coluna "fonte" diz de onde vem a descrição. **Texto completo**: lido nesta análise. **Resumo**: só o resumo foi lido. **Conhecimento geral**: descrição do trabalho clássico que **precisa ser conferida no PDF** antes de citar. Os PDFs da Elsevier e da ASCE não estavam acessíveis daqui.

| Trabalho | Degradação | O que se observa | Variáveis de decisão | Objetivo | Restrição | Renovação | Solução | Fonte |
|---|---|---|---|---|---|---|---|---|
| Park 1988, IEEE TR | Desgaste estocástico | Nível de desgaste em inspeção periódica | Limite de controle (*control limit*) | Custo médio por unidade de tempo (longo prazo) | — | Perfeita (substituição) | Analítica (renovação) | Conhecimento geral |
| Grall, Bérenguer & Dieulle 2002, RESS | Processo gama | Nível exato de degradação | **Limiar preventivo ξ** + regra de agendamento da próxima inspeção | Custo médio assintótico por unidade de tempo (propriedade semirregenerativa) | — | Perfeita | Analítica/numérica | Conhecimento geral |
| Kallen & van Noortwijk 2005, RESS | Processo gama com taxa atualizada (Bayes) | Medida **com erro** (inspeção imperfeita) | Intervalo de inspeção e limiar preventivo | Custo esperado | — | Perfeita | Numérica | Conhecimento geral |
| van Noortwijk & Frangopol 2004, PEM | Dois modelos: condição (gama) × confiabilidade (perfis de β) | Condição / β | Intervalos e ações | Custo do ciclo de vida | β ≥ β_alvo (modelo de confiabilidade) | Perfeita / melhoria | Renovação; simulação | Conhecimento geral |
| Mori & Ellingwood 1994, JSE | Resistência que degrada | Inspeção com probabilidade de detecção | Instantes de inspeção | Custo total esperado (inspeção + reparo + falha) | Implícita no custo de falha | Reparo ao detectar | Otimização numérica | Conhecimento geral |
| Kong & Frangopol 2003, JSE | Perfis de β(t) com efeitos empíricos de manutenção | Nenhuma (previsão) | Tipos e instantes de manutenção | Custo presente | **β(t) ≥ β_alvo** em toda a vida | Ações com efeito empírico em β | Busca combinatória | Conhecimento geral |
| Liu & Frangopol 2005, JSE | Índices de condição e segurança | Nenhuma (previsão) | Instantes e tipos de manutenção | **Multiobjetivo:** condição, segurança, custo | — | Efeitos por ação | Algoritmo genético (Pareto) | Conhecimento geral |
| Okasha & Frangopol 2010, JSE | Confiabilidade de sistema | Nenhuma | Manutenção preventiva e essencial | Multiobjetivo: custo, confiabilidade e redundância mínimas | — | Por ação | Algoritmo genético | Conhecimento geral |
| Barone & Frangopol 2014, RESS | Resistências que degradam (sistemas série/paralelo) | Nenhuma | **Limiar de desempenho**: restauração total quando o indicador (β anual, risco anual, vida) atinge o limiar | Comparação de indicadores e custo | Limiar prescrito | **Restauração total** | Simulação | Resumo |
| Barone & Frangopol 2014, Struct. Saf. | Idem | Nenhuma | Cronograma de manutenção essencial | **Multiobjetivo:** indicador (β, risco, disponibilidade, *hazard*) × custo | — | Restauração | Algoritmo genético; frentes de Pareto | Resumo |
| Kim, Frangopol & Soliman 2013, JSE | Genérica | Inspeção com probabilidade de detecção | Instantes (e qualidade) de inspeção | Atraso esperado de detecção/manutenção e custo | — | Por árvore de eventos | Algoritmo genético | Conhecimento geral |
| Kumar & Gardoni 2014, Struct. Saf. | Desgaste gradual + choques | — | — (base analítica) | E[nº de renovações], custo do ciclo de vida | — | Perfeita | **Teoria da renovação** | Conhecimento geral |
| Lee et al. 2020, JMCE | Carbonatação em concreto com reparo superficial | Nenhuma | Instantes de reparo | Custo do ciclo de vida probabilístico | Vida útil | **Dois materiais** (reparo superficial) | Simulação | Corpus da revisão (título e codificação) |
| Guo & Liang 2026, RESS | Carbonatação (EDP por PINN) → estados *phase-type* | Estado discreto com acerto de 0,9 | Ação por estado + data da próxima inspeção (limiar de RUL) | Custo (POMDP preditivo) | — | **Renovação perfeita** | Programação dinâmica | **Texto completo** |
| **Este trabalho** | **Possan + latentes via emulador GLD-PCE-NN** | **Margem física medida com erro (mm)** | **t₁, Δt, g_lim, f_c,rep (c_nom em F4)** | **E[N_rep], N_insp, P_desp; custo** | **P_desp ≤ Φ(−1,3) (fib 34 / ISO 16204)** | **Não idêntica (argamassa, idade zerada)** | **MC sobre nuvens + grade / NSGA-II** | — |

### O que adotar de cada um

1. **Da linha Grall / Park / Kallen:** a política de limiar com inspeção periódica e a inspeção imperfeita.
   - **Diferença:** eles minimizam custo por unidade de tempo em horizonte infinito, com renovação **perfeita**.
   - Aqui, o horizonte é finito (100 anos) e a renovação não é idêntica (outro material). Por isso não vale a fórmula de renovação e é preciso Monte Carlo.
   - Essa diferença é argumento de novidade, não fraqueza.
2. **Da linha Frangopol:** a restrição β ≥ β_alvo e o formato multiobjetivo com frente de Pareto.
   - **Diferença:** lá os limiares estão em β (modelo), não numa grandeza medida em campo. O nosso g_lim é em **mm**, a linguagem do engenheiro que faz a inspeção.
3. **De Kumar & Gardoni:** como checar E[N_rep] analiticamente num caso simples (renovação perfeita), para validar o simulador.
4. **De Guo & Liang:** é o concorrente mais próximo em carbonatação.
   - O que eles não têm e nós temos: margem física, argamassa diferente, β_alvo, espaço de projeto e cenários de CO₂.

---

## 7. Algoritmo

```
para cada política θ (na grade ou proposta pelo otimizador):
    usar as MESMAS sementes para todas as θ  (números aleatórios comuns)
    sortear u_i0 ~ U(0,1) e erros ε_ij ~ N(0, σ_g²) para i = 1..M
    para t = 1..T:
        g_i(t) = G(u_ik, t − t_ik; x_k)          (nuvem do material atual)
        acumular: despassivação, anos despassivados, custo de risco
        se t é instante de inspeção:
            ĝ = g_i(t) + ε_it
            se ĝ ≤ g_lim: reparo (preventivo ou corretivo); k ← k+1; t_ik ← t; sortear u_ik
    calcular E[N_rep], N_insp, P_desp, E[C] e os erros padrão
selecionar: F1 / F2 (restrição) ou F3 (Pareto)
```

**Como resolver:**
1. **Etapa 1, grade.** t₁ × Δt × g_lim × f_c,rep, como no código-base (252 políticas; cerca de 25 s com o substituto).
2. **Etapa 2, refinamento contínuo.** Use g_lim e f_c,rep contínuos, com t₁ e Δt fixos no melhor valor da grade, e Nelder-Mead ou busca dourada em g_lim. **Use números aleatórios comuns**; senão o ruído de MC cria ótimos falsos.
3. **Etapa 3, Pareto.** Use NSGA-II (`pymoo`), com as inteiras arredondadas. O *simulated annealing* sequencial de dos Santos et al. 2024 (Ketson é coautor) é uma alternativa da casa para o problema estocástico.
4. **Verificação.** Repita o ótimo com outra semente e M = 50 000. P_desp deve mudar menos que 2 erros padrão.

---

## 8. Saída de referência (substituto do Possan; caso-base 25 MPa / 55 % / 25 mm)

Comando: `python paper_final/otimizacao/otimizacao_limiar.py`, a partir da raiz do repositório. A saída vai para `paper2_otimizacao/`.

**Varredura em g_lim** (t₁ = 10, Δt = 10, f_c,rep = 40 MPa):

| g_lim (mm) | 0 | 2 | 4 | **6** | 8 | 10 | 12 |
|---|---|---|---|---|---|---|---|
| E[N_rep] | 0,88 | 0,95 | 1,04 | **1,17** | 1,36 | 1,62 | 1,98 |
| P_desp | 0,54 | 0,30 | 0,12 | **0,037** | 0,011 | 0,003 | 0,001 |
| Custo (× C₀) | 0,059 | 0,047 | 0,040 | **0,038** | 0,042 | 0,048 | 0,057 |

**Efeito da argamassa** (t₁ = 10, Δt = 10, g_lim = 6):

| f_c,rep | 30 MPa | 40 MPa | 50 MPa |
|---|---|---|---|
| E[N_rep] | 1,64 | 1,17 | 1,02 |
| P(N_rep ≥ 2) | 0,57 | 0,19 | 0,05 |

**Grade completa** (252 políticas, 132 viáveis com β ≥ 1,3):

| Política | Resultado |
|---|---|
| F1, menos reparos | E[N_rep] = 1,00 com t₁ = 20, Δt = 5, g_lim = 4, f_c,rep = 50 (16 inspeções) |
| F1 com até 9 inspeções | E[N_rep] = 1,02 com t₁ = 20 ou 10, Δt = 10, g_lim = 6, f_c,rep = 50 |
| F2, menor custo | 0,036·C₀ com t₁ = 15, Δt = 15, g_lim = 8, f_c,rep = 50 |
| F3 | 24 políticas na frente de Pareto (`pareto_N_insp_risco.csv`) |

O otimizador escolhe f_c,rep = 50 MPa em quase todas as políticas do topo. Isso é a armadilha da Seção 5: a argamassa melhor não custa mais. Os valores de custo são ilustrativos.

**Regra de engenharia para conferir.** g_lim ≈ avanço da frente no intervalo + folga para o erro da leitura:

$$
g_\mathrm{lim} \approx K\big(\sqrt{t+\Delta t}-\sqrt{t}\big) + z\,\sigma_g .
$$

Aos 40 anos, com K = 3,44 mm/√ano, Δt = 10 e z = 1,28: 2,6 + 3,7 ≈ **6,3 mm**, coerente com o ótimo da varredura. Mostrar que a otimização probabilística recupera essa regra simples é um bom resultado para o paper.

---

## 9. Cuidados

1. **Efeito de fim de horizonte.** Reparar perto de t = 100 não traz benefício dentro do horizonte, e o modelo tende a evitar esses reparos. Ou não se inspeciona nos últimos anos, ou se inclui um valor terminal (condição da viga em t = 100).
2. **Primeira inspeção.** Se t₁ for tarde, as vigas da cauda inicial despassivam antes, seja qual for o g_lim. Com o emulador atual, que subestima essa cauda, isso aparece menos do que no simulador. Vale um teste de sensibilidade.
3. **Ruído de Monte Carlo.** Compare políticas sempre com as mesmas sementes. Reporte o erro padrão de P_desp junto com a restrição.
4. **Domínio do emulador.** f_c 20–50 MPa, UR 20–80 %, c 15–60 mm, t 0–100 anos. Fora disso, a NN extrapola.
5. **Custos.** Use o SINAPI, ou adimensionais com faixa de sensibilidade. Respeite o limite físico λ_dep > λ_corr(1 − d¹⁰)/Σd^k (≈ 0,0123 para razão 4), senão esperar com a viga despassivada passa a "valer a pena".

---

## 10. Roteiro de tarefas

- [ ] **1.** Rodar o código-base com o substituto e conferir com `saida_referencia/otimizacao_run_log.txt`.
- [ ] **2.** Recolocar os `.pkl` e rodar com o emulador. Comparar as tabelas da Seção 8.
- [ ] **3.** Decidir as hipóteses H-a a H-d (Seção 3.3) e escrever o parágrafo de método.
- [ ] **4.** Implementar o custo de f_c,rep, ou fixá-la (Seção 5, armadilha).
- [ ] **5.** Resolver F1 e F2 no caso-base: grade e depois refinamento de g_lim.
- [ ] **6.** Montar a frente de Pareto F3 com NSGA-II e escolher 3 políticas representativas.
- [ ] **7.** Conferir a regra g_lim ≈ K(√(t+Δt) − √t) + zσ_g contra os ótimos, para vários Δt.
- [ ] **8.** Mapear o g_lim ótimo e o E[N_rep] mínimo no espaço de projeto (f_c × c_nom; UR = 55 e 75 %).
- [ ] **9.** Fazer a sensibilidade a σ_g, β_alvo (1,3 e 1,5), custos e taxa de desconto.
- [ ] **10.** (Opcional) F4: projeto + manutenção.
- [ ] **11.** Conferir no PDF as descrições marcadas como "conhecimento geral" na tabela da Seção 6, antes de citar.

---

## 11. Referências (DOIs conferidos no CrossRef ou no corpus da revisão)

- Park (1988) IEEE Trans Reliab — doi:10.1109/24.3722
- Grall, Bérenguer & Dieulle (2002) RESS — doi:10.1016/s0951-8320(01)00148-x
- Dieulle, Bérenguer, Grall & Roussignol (2003) EJOR — doi:10.1016/s0377-2217(02)00593-3
- Kallen & van Noortwijk (2005) RESS — doi:10.1016/j.ress.2004.10.004
- van Noortwijk & Frangopol (2004) Probab Eng Mech — doi:10.1016/j.probengmech.2004.03.002
- van Noortwijk (2009) RESS — doi:10.1016/j.ress.2007.03.019
- Mori & Ellingwood (1994) J Struct Eng — doi:10.1061/(asce)0733-9445(1994)120:3(846)
- Kong & Frangopol (2003) J Struct Eng — doi:10.1061/(asce)0733-9445(2003)129:6(818)
- Liu & Frangopol (2005) J Struct Eng — doi:10.1061/(asce)0733-9445(2005)131:5(833)
- Okasha & Frangopol (2010) J Struct Eng — doi:10.1061/(asce)st.1943-541x.0000198
- Kim, Frangopol & Soliman (2013) J Struct Eng — doi:10.1061/(asce)st.1943-541x.0000676
- Barone & Frangopol (2014) RESS — doi:10.1016/j.ress.2013.09.013
- Barone & Frangopol (2014) Struct Saf — doi:10.1016/j.strusafe.2014.02.002
- Kumar & Gardoni (2014) Struct Saf — doi:10.1016/j.strusafe.2014.03.012
- Alaswad & Xiang (2017) RESS — doi:10.1016/j.ress.2016.08.009
- de Jonge & Scarf (2020) EJOR — doi:10.1016/j.ejor.2019.09.047
- Bastidas-Arteaga & Schoefs (2012) Eng Struct — doi:10.1016/j.engstruct.2012.03.011
- Stewart, Wang & Nguyen (2011) Eng Struct — doi:10.1016/j.engstruct.2011.01.010
- Lee et al. (2020) J Mater Civ Eng — doi:10.1061/(asce)mt.1943-5533.0003390
- Guo & Liang (2026) RESS — doi:10.1016/j.ress.2025.111761
- dos Santos et al. (2024) Eng Struct — doi:10.1016/j.engstruct.2024.117675
- Kim & Frangopol (2026) Probab Eng Mech — doi:10.1016/j.probengmech.2026.104060 (revisão sistemática recente)
