# Plano da Seção de Resultados — Paper Q1

**Título do paper:** *Forecasting Remaining Useful Life of Reinforced Concrete Structures Subjected to Carbonation-Induced Corrosion Using Emulators*

**Autores:** Couto, Pereira Jr., dos Santos, Henrique, Pensin
**Branch:** `paper`
**Status atual:** `Section_4.tex` contém apenas toy problem + RUL pontual. Caso real, sensibilidade, reliability curves e reparo estão ausentes.

---

## 1. Contexto e Motivação

O paper propõe um pipeline de emuladores **GLD → PCE → ANN** para prever a distribuição da função estado limite `g(t)` de vigas de concreto armado submetidas à corrosão induzida por carbonatação. O Monte Carlo direto é proibitivamente lento; o emulador fornece ganho de 1–2 ordens de magnitude com acurácia controlada.

Após orientação de colega do time, a Seção 4 será reestruturada em dois blocos:

- **Parte A — Desempenho do emulador** (treino, validação, custo computacional)
- **Parte B — Aplicação em cenários de RUL** (sem reparo e com reparo)

Este documento serve como blueprint para Victor regenerar resultados e reescrever `Section_4.tex`.

---

## 2. Decisões Acordadas

| Dimensão | Escolha |
|---|---|
| **Horizonte temporal** | 150 anos (retreinar PCE/ANN) |
| **Features do emulador real** | `{fck, UR, CO₂, tipo_cimento, exposição, t}` — conjunto completo da Seção 2 |
| **Modelo de reparo** | Restauração de cobrimento + repassivação: reset `y_carb=0`; `Δd` acumulado preservado; `c_f` recalculado com `t_corr` reiniciado |
| **Mecanismo** | Carbonatação apenas (consistente com título e Seção 2) |

---

## 3. Estrutura Proposta para `Section_4.tex`

### 4.1 Emulator construction, training, and validation

> **Objetivo:** demonstrar que o pipeline GLD → PCE → ANN reproduz a resposta probabilística do modelo de referência com alta acurácia e ganho computacional de 1–2 ordens de magnitude.

#### 4.1.1 Toy problem — validação da metodologia *(reestruturação do conteúdo atual)*

- Definição do problema (Equações 1 e 2 atuais — manter).
- Tabela de variáveis aleatórias (Tab. 1 atual — manter).
- Análise exploratória de `λ₁`–`λ₄` e justificativa estatística para treinar apenas `λ₁`, `λ₂` (scatter atual + Tabela R² atual).
- Validação do PCE por passo de tempo (KS, AD, quantile comparison — conteúdo atual).
- ANN para interpolação contínua (figura `z_temporal_evolution_ann_with_points_en.png` — atual).
- **Adicionar:** breakdown do custo computacional — geração de dados + ajuste PCE + treino ANN + inferência (hoje mostra só total 48.75s vs 0.66s).

#### 4.1.2 Real-data emulator — aplicação ao dataset de carbonatação *(NOVO)*

- **Definição do problema real:**
  - Limit-state `G(t) = M_{Rd,cor}(t) − (M_{Gk} + M_{Qk})` (mecânica da Seção 5).
  - Latente carbonatação: `y_carb(t) = k_c·√t`, com `k_c` parametrizado em `{fck, UR, CO₂, cimento, exposição}` via ML treinado em Couto et al. 2025 (Seção 2).
  - Faixas de entrada e sampling LHS (reportar `N_samples` e `n_time_steps`).
- **Treino** do GLD em 11 passos de tempo cobrindo [0, 150] anos.
- **Treino do PCE** para `λ₁`, `λ₂` em cada passo → tabela de R² análoga à do toy.
- **Treino da ANN** mapeando `{fck, UR, CO₂, cimento, exposição, t} → {λ₁, λ₂}`.
- **Validação cruzada** (k-fold ou hold-out): R², RMSE, MAE no test set.
- **Comparação probabilística emulador vs. Monte Carlo direto:**
  - KDE sobreposta em ≥3 pontos (ex.: t = 25, 75, 125 anos).
  - KS + Anderson–Darling + comparação de quantis extremos (0.1%, 1%, 99%, 99.9%).
- **Análise de sensibilidade global** (índices de Sobol de 1ª ordem e totais) sobre `λ₁(t)` para t fixo — identifica drivers dominantes.
- **Tabela de custo computacional** no caso real (MC bruto vs. emulador em escala realista).

#### 4.1.3 Síntese de desempenho

- Tabela consolidando métricas (R², KS, speed-up) dos dois problemas.
- Parágrafo de fechamento conectando com a Parte B.

---

### 4.2 Application — Remaining Useful Life assessment

> **Objetivo:** demonstrar o valor do emulador em manutenção, cobrindo operação sem intervenção vs. operação com reparo programado.

#### 4.2.1 Baseline scenario — RUL sem reparo *(expansão do conteúdo atual)*

- Viga de referência: parâmetros da Seção 5 (referenciar, não duplicar).
- Cenário ambiental de referência (fck, UR, CO₂, cimento, exposição) em Tabela.
- **Saídas probabilísticas:**
  - KDEs de `G(t)` em t = {25, 50, 75, 100, 125, 150} anos (painel de 6 subfigs ou heatmap de densidade temporal).
  - Curva `P_f(t)` para 0–150 anos.
  - Curva `β(t)` correspondente.
  - Fragility curve: `P(G < 0 | t)`.
- **RUL a partir de inspeção:**
  - `t_insp = 35` anos (atual) e também `t_insp = 75` anos (cenário intermediário).
  - KDE de `G(t_insp)`, KDE do tempo-até-falha, KDE de RUL — estender para 150 anos.
  - VaR₅%, CVaR₅% tabelados.
- **Estudo paramétrico** (emulador torna barato — é o grande argumento):
  - Varredura `fck ∈ {20, 25, 30, 40, 50}` MPa.
  - Varredura `UR ∈ {50, 65, 75, 85}%`.
  - Varredura em concentração de CO₂ (baixa/média/alta via bins da Seção 2).
  - Família de curvas `β(t)` por varredura; identificar driver dominante de vida útil.

#### 4.2.2 Repair scenario — RUL com intervenção *(NOVO — coração da contribuição)*

- **Definição formal do modelo de reparo:**
  - Gatilho: baseado em condição (`P_f(t) ≥ P_f,target` ou `β(t) ≤ β_target`) E/OU temporal fixo (`t_rep = 50, 75, 100` anos).
  - Ação física: reset `y_carb(t_rep⁺) = 0`; `Δd` acumulado permanece; `c_f` recalculado com `t_corr` reiniciado.
  - Efeito no emulador: nova curva `g(t)` pós-reparo via mesmo ANN com entrada temporal deslocada e estado inicial degradado.
- **Resultados:**
  - Painel comparativo: `β(t)` sem reparo vs. com reparo em `t_rep = {50, 75, 100}` anos.
  - KDE de RUL pós-reparo vs. baseline.
  - Ganho de RUL (`ΔRUL` em anos) em função de `t_rep` — mostra existência de janela ótima.
  - Métricas VaR/CVaR pós-reparo tabeladas.
- **Discussão de implicações práticas:**
  - Quanto pode-se adiar o reparo mantendo `β_target`?
  - Reparo é mais eficaz cedo ou tarde no contexto só-cobertura?
  - Limitação: `Δd` residual cria ceiling na RUL recuperável.

#### 4.2.3 Final discussion

- Síntese do valor do emulador (acurácia + velocidade + estudos paramétricos viáveis).
- Relação com decisões informadas por risco em gestão de ativos.
- Ponte para Conclusões.

---

## 4. O Que é Novo vs. o Que Reaproveita

| Conteúdo atual | Ação |
|---|---|
| `Section_4.tex` — toy problem com 11 time steps até 100 anos | **Manter** e mover para 4.1.1 |
| Tabela R² PCE para `λ₁`–`λ₄` | **Manter** em 4.1.1 |
| KS/AD + quantile comparison | **Manter** em 4.1.1 |
| ANN interpolação contínua (toy) | **Manter** em 4.1.1 |
| Tabela custo computacional (48.75s vs 0.66s) | **Manter** em 4.1.1; **adicionar** breakdown |
| KDEs RUL, VaR/CVaR (toy) | **Mover** para 4.2.1 como baseline do caso real; regenerar com parâmetros da viga da Seção 5 e horizonte 150 anos |
| Seção 2 — dataset de carbonatação | **Referenciar** em 4.1.2 como fonte do modelo de `k_c` |
| Seção 5 — mecânica da viga (NBR 6118 + Azad & Al-Gohi + Peng & Stewart) | **Referenciar** em 4.2.1 (não duplicar); considerar converter em apêndice |

---

## 5. Resultados Novos a Gerar (Pipeline Python)

Notebooks em `beam_problem_1/01_glam_real_data/`. Victor precisa entregar:

1. Retreino do PCE e da ANN do toy problem com `t ∈ [0, 150]` anos.
2. Pipeline GLD + PCE + ANN no caso real com features `{fck, UR, CO₂, cimento, exposição, t}`.
3. Simulação Monte Carlo de referência (baseline para validar emulador no caso real; amostra reduzida é aceitável).
4. Rotina de cálculo `P_f(t)`, `β(t)`, fragility em grade densa de t.
5. Módulo de reparo: reset `y_carb = 0` preservando `Δd` acumulado.
6. Análise de sensibilidade Sobol (`SALib` ou equivalente).
7. Varreduras paramétricas em fck, UR, CO₂.
8. Geração de novas figuras com nomenclatura `z_real_*`, `z_repair_*`, `z_param_*` (manter padrão `_en`).

---

## 6. Arquivos do Repositório Afetados

| Arquivo | Ação |
|---|---|
| `Section_4.tex` | Reescrita quase completa; preservar blocos úteis |
| `Section_5.tex` | Considerar fundir com 4.2.1 ou manter como apêndice; remover duplicação |
| `main.tex` | Atualizar ordem — recomenda-se mover `GLaM_Marcos` para antes de Resultados (metodologia antes de resultados, padrão Q1) |
| `Section_2.tex` | Nota conectando `k_c` do dataset ao emulador GLD (4.1.2) |
| `mybibfile.bib` | Novas referências: Sobol indices, fragility, repair modeling (Li 2004, Val & Stewart, Enright & Frangopol) |
| **Figuras novas** | ~10–15 para 4.1.2 e 4.2; convenção `z_` + sufixo `_en` |

---

## 7. Verificação End-to-End (quando implementação estiver completa)

1. `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex` compila sem warnings de referências quebradas.
2. Todas as figuras novas (`z_*.png`) existem e são referenciadas.
3. Todas as tabelas têm label, caption e são citadas no texto.
4. Cada subseção (4.1.1, 4.1.2, 4.1.3, 4.2.1, 4.2.2, 4.2.3) tem ao menos uma figura OU tabela.
5. Abstract + Seção 4 sozinhos permitem entender a contribuição (teste "elevator pitch" Q1).

### Checklist Q1

- [ ] Novelty explícita no primeiro parágrafo de 4.1 e 4.2.
- [ ] Baseline de comparação (MC direto) em 4.1.2.
- [ ] Métricas quantitativas de acurácia E de custo.
- [ ] Análise de sensibilidade presente.
- [ ] Discussão de limitações explícita em 4.2.3.

---

## 8. Periódicos-Alvo Sugeridos (Q1, escopo compatível)

- *Structural Safety* — foco central em confiabilidade estrutural.
- *Reliability Engineering & System Safety* — surrogate models + RUL.
- *Engineering Structures* — aplicação a concreto armado.
- *Computers and Structures* — pipeline computacional.
- *Structure and Infrastructure Engineering* — gestão de ativos e manutenção.
