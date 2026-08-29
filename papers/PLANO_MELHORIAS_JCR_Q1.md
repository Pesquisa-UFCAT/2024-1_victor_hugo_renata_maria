# Plano de melhorias — de rascunho a artigo Q1 (JCR)

**Alvo:** periódico Q1 de durabilidade/confiabilidade estrutural.
**Estado atual:** metodologia sólida e bem escrita; Exemplo 1 (benchmark) concluído;
Exemplos 2–3 e vários experimentos-chave ainda por executar.

O que separa este manuscrito de um Q1 **não** é o texto — é a **evidência experimental**
que sustenta a alegação central ("emular a distribuição completa de g(t) no tempo é
acurado e ordens de grandeza mais barato"). Abaixo, em ordem de prioridade.

---

## Tier 0 — Sem isto o artigo não passa em Q1 (bloqueadores)

### 0.1 O experimento que *é* o artigo: generalização temporal em anos não vistos
A tese do paper é que a RNA interpola a **distribuição** de g entre os anos simulados.
Isso precisa ser **provado**, não afirmado. Experimento obrigatório:
- Treinar a camada temporal **omitindo** 1–2 passos (ex.: 35 e 65 anos).
- Nesses anos, comparar a PDF emulada com **Monte Carlo direto** do simulador.
- Reportar KS (valor-p), erro nos quantis P₅/P₅₀/P₉₅, divergência KL/Wasserstein e,
  sobretudo, **erro na cauda inferior (g ≤ 0) e em p_f**.
- Figura sobrepondo emulador × MC nos anos omitidos, com a região g ≤ 0 destacada.

> Já deixei o *placeholder* disto no Ex.1 (`\falta` na subseção da camada temporal) e
> uma tabela pronta no Ex.2 (`tab:ex2_validacao`). **É o primeiro resultado a rodar.**

### 0.2 Validar p_f(t) e β(t), não só os λ
R² alto em λ₁/λ₂ **não** é evidência suficiente para um revisor de confiabilidade —
um bom R² em λ pode conviver com erro grande em p_f (a cauda é o que importa).
Validar a saída de interesse: curva β(t) emulada × pontos de Monte Carlo em 3–4
anos-âncora, com erro relativo em p_f tabelado. (placeholder `fig:ex2_pf_beta` pronto.)

### 0.3 Custo computacional honesto e comparável
O "speed-up de 2 ordens" (48,75 s → 0,66 s) só convence se a comparação for **iso-acurácia**:
- Quantas avaliações do simulador o MC direto precisa para atingir o **mesmo** erro em p_f
  ao longo de *todo* o horizonte? Esse é o denominador justo.
- Contabilizar o **custo de treinamento** do emulador (M×N×Nt) no total, e separar o
  custo *online* (pós-processamento por cenário), que é onde o ganho real aparece na
  varredura de manutenção. (tabela `tab:ex2_custo` pronta.)

### 0.4 Fechar os metadados de referência
`references.bib` tem 3 entradas com `[XXXX]`: `couto2025` e `pires2024` (do grupo/benchmark)
e as datas de acesso do NOAA. Revisor de Q1 rejeita citação incompleta. O paper também
se apoia fortemente em `couto2025` (dataset + 7 modelos de ML): garantir que esteja
publicado/no prelo, ou o argumento de dados fica pendurado numa referência inacessível.

---

## Tier 1 — Decisões de modelagem que você levantou

### 1.1 Exemplo 2: `g = cobrimento − ataque` (sua ideia) **vs.** `g = M_Rd,cor − M_S`
Você mencionou montar o emulador para **g = cobrimento − profundidade de ataque**.
Isso é um **estado limite de durabilidade (despassivação)**:

```
g_desp(X, t) = c_nom − y_carb(X, t)        (falha = início da corrosão)
```

**Recomendação (forte): use os dois, como uma escada de dois degraus.**
- **Exemplo 2a — despassivação** `g = c_nom − y_carb(t)`: mais simples, depende só do
  modelo de Possan, e é o estado limite que *casa perfeitamente* com o dataset de
  `couto2025` (que é de profundidade de carbonatação). Ótimo para isolar e validar a
  emulação temporal sem o ruído do modelo mecânico de flexão.
- **Exemplo 2b — ULS de flexão** `g = M_Rd,cor − M_S`: o estado limite que já está todo
  formulado na §4.2. É o degrau "difícil" (não linearidade da bisseção + corrosão).

Vantagem: a despassivação dá uma RUL "até despassivar" e o ULS dá uma RUL "até ruptura";
juntos contam a história completa de durabilidade → segurança. Deixei uma nota `\falta`
na §4.2.4 apontando esse estado limite alternativo. **Confirme comigo qual caminho** e eu
ajusto a Metodologia e o Exemplo 2.

### 1.2 A parte final dos resultados (sua dúvida: "não sei o que fazer")
Seu colega sugeriu **otimização** ou **p_f em função de um *threshold***. As duas ideias
são boas e **compatíveis** — proponho a seguinte progressão (do mais barato ao mais forte):

**Opção A (recomendada, já quase pronta) — Política de manutenção por limiar.**
É o Exemplo 3 que já está estruturado: determinar `t*_man = inf{t : β(t) ≤ β_alvo}`
direto da curva β(t) emulada, aplicar o reparo (dente de serra) e medir ΔRUL. O gancho de
Q1 é: **varrer β_alvo e t_man é instantâneo com o emulador e intratável por MC** — mostre
uma *família* de curvas ΔRUL(t_man) para vários β_alvo. Isto responde ao "p_f em função de
threshold" do seu colega de forma natural.

**Opção B (o degrau Q1+) — Otimização de custo de ciclo de vida.**
Minimizar o custo esperado total escolhendo o instante de intervenção:

```
min_{t_man}  E[C] = C_insp + C_rep · (1 + r)^(−t_man) + C_falha · p_f(T_f | reparo em t_man)
```

Como cada avaliação de `p_f(T_f | t_man)` custa milissegundos no emulador, dá para varrer
`t_man` (e até múltiplas intervenções) e traçar a **curva de custo × instante de reparo**,
achando o ótimo. **Este é o argumento mais forte de "por que emular a distribuição inteira
importa"**: otimização precisa de milhares de reavaliações — exatamente o que o emulador
viabiliza e o MC não.

**Opção C (bônus, se sobrar fôlego) — p_f como função de um *threshold* de decisão.**
Curvas de p_f(t) para diferentes limiares de aceitação (ex.: perda de seção admissível,
abertura de fissura, ou o próprio β_alvo), ilustrando trade-off risco × intervenção.

> **Minha sugestão de composição final dos Resultados:**
> Ex.1 (benchmark, feito) → Ex.2 (despassivação + ULS, RUL) → Ex.3 (manutenção por limiar,
> Opção A) → **Ex.4 (otimização de custo, Opção B)** como clímax. Diga se topa e eu monto
> o esqueleto do Ex.4.

---

## Tier 2 — Rigor que revisor Q1 vai cobrar

- **Análise de sensibilidade (Sobol via PCE):** já tem placeholder (`fig:ex2_sobol`). Mostre
  a migração de importância no tempo: cobrimento e k dominam na iniciação; i_corr cresce na
  propagação. É barato (analítico dos coeficientes PCE) e muito convincente.
- **Robustez amostral do PyGLAM:** a Tabela `tab:pyglam_metricas` (ajuste GLD a Normal/
  Gumbel/Uniforme) precisa variar N (ex.: 50/200/1000) para mostrar convergência do MoM.
- **Justificar MoM vs. verossimilhança (GLaM original):** o texto já defende a escolha; um
  revisor vai perguntar quando o MoM falha (caudas pesadas, N pequeno) — 1 parágrafo de
  limitação honesta resolve.
- **Comparação com um baseline de emulação:** o Tier-1 diferencia de MC; para Q1, comparar
  ao menos *qualitativamente* (ou num apêndice) com uma alternativa — emular direto β(t) por
  GP/PCE, ou SPCE — e argumentar por que emular a **distribuição completa** ganha (dá RUL,
  VaR/CVaR e cenários de manutenção que o β(t)-direto não dá).
- **Hipótese de monotonicidade:** com ação variável (Gumbel) em M_Qk, g pode não ser
  monotônico → R(t) ≈ 1 − p_f(t) precisa de ressalva (problema de primeira passagem /
  outcrossing). Já deixei `\falta` na §4.4.1. Ou assuma monotonicidade explicitamente e
  justifique (degradação domina), ou trate o outcrossing.

---

## Tier 3 — Apresentação (importa mais do que parece em Q1)

- **Figuras em português e vetoriais.** Hoje os rótulos estão em inglês (várias `\falta`
  de "traduzir rótulos"). Regerar os gráficos com rótulos PT, fonte legível, sem moldura,
  em PDF/vetorial. Padronizar paleta e usar subfiguras (A)/(B) como no modelo.
- **Uma figura de "abstract gráfico"/fluxograma da metodologia:** simulador → GLD local →
  PCE → camada temporal (RNA) → p_f/β/RUL/VaR. Q1 adora um diagrama-mãe. (não existe ainda)
- **Algoritmo em pseudocódigo** do pipeline de treino+predição (o modelo já traz o ambiente
  `algorithm`). Aumenta reprodutibilidade e a percepção de rigor.
- **Reprodutibilidade:** liberar o PyGLAM (repositório + DOI Zenodo) e citar na "Data
  availability". Isso pesa positivamente na avaliação editorial.

---

## Tier 4 — Enquadramento e submissão

- **Novidade em uma frase:** "primeiro emulador estocástico que interpola a *distribuição
  condicional completa* de g no tempo e a lê diretamente como RUL probabilística, com
  ganho de ordens de grandeza sobre Monte Carlo em análise de manutenção." Garantir que
  Abstract, fim da Introdução e Conclusões repitam essa frase de forma consistente.
- **Posicionar contra a literatura recente** de confiabilidade dependente do tempo por
  carbonatação (emular β(t) ou momentos) — a Introdução já faz isso; reforçar com 3–5
  referências dos últimos ~3 anos para mostrar atualidade.
- **Periódicos-alvo sugeridos:** *Structural Safety*, *Reliability Engineering & System
  Safety*, *Engineering Structures*, *Structure and Infrastructure Engineering*,
  *Cement and Concrete Composites* (se o peso for durabilidade). RESS/Structural Safety
  valorizam justamente o emulador estocástico + UQ.
- **Checklist pré-submissão:** remover macros `\falta`; conferir `[XXXX]` do `.bib`;
  ORCID/afiliações; declaração CRediT; alt-text das figuras (o modelo pede); nº de palavras.

---

## Sequência prática sugerida (o que rodar, em ordem)

1. Definir estado(s) limite do Ex.2 (§1.1 acima) — **preciso da sua decisão**.
2. Rodar Ex.2: treino do emulador + **validação em anos não vistos** (Tier 0.1/0.2).
3. Custo iso-acurácia (Tier 0.3) + Sobol (Tier 2).
4. Ex.3 manutenção por limiar (Opção A) e, se topar, Ex.4 otimização (Opção B).
5. Regerar figuras em PT + fluxograma + pseudocódigo (Tier 3).
6. Fechar `.bib`, abstract com números reais, revisão final e remoção de `\falta`.

> **Podemos ir seção por seção.** Sugiro começar por **§4.2 + Exemplo 2** (a decisão do
> estado limite destrava o resto). Me diga por onde quer atacar primeiro.
