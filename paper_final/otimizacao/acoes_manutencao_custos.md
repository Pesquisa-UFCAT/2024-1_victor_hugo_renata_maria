# Ações de manutenção e modelo de custo — vigas de concreto armado sob carbonatação

Documento de base para montar o problema multiobjetivo. Para cada manutenção possível, ele diz:

- quando se aplica;
- o que ela faz fisicamente;
- **como entra no emulador de g(t)**;
- quanto custa (em termos relativos).

A formulação de otimização está em [otimizacao_limiar.md](otimizacao_limiar.md). Os custos de cada ação são levantados na viga de referência: [viga_referencia/viga_referencia.md](viga_referencia/viga_referencia.md).

> **Sobre os números de custo.** Os valores em λ (× C₀) são **hipóteses de trabalho** para montar e testar o problema. As faixas de mercado da Seção 4 servem só para a ordem de grandeza **relativa** entre as ações. Antes do paper, calibrar com SINAPI ou orçamentos de empresas de recuperação estrutural.

---

## 1. Estrutura do custo de uma intervenção

Toda ida à obra tem três parcelas:

$$
C_\text{interv} = \underbrace{C_\text{mob}}_{\text{acesso, andaime, interdição}} + \underbrace{\textstyle\sum_a c_a\,A_a}_{\text{serviços por m²}} + \underbrace{C_\text{ind}}_{\text{interrupção de uso}}
$$

Adimensionalizando pelo custo de construção do elemento, λ = C/C₀ (C₀ ≡ 1), como no documento de discussão.

**Por que isso importa para o multiobjetivo.**
- A mobilização (acesso, andaime, interdição) é paga **por campanha**, não por serviço. Inspecionar e reparar na mesma ida custa menos que em duas idas.
- Por isso o "número de manutenções" que você quer reduzir é, na prática, o **número de campanhas**. Ele mede custo de mobilização e transtorno ao usuário.
- Convém separar os dois na contabilidade: N_campanhas (vezes que se vai à obra) e N_reparos (vezes que se intervém no concreto).

---

## 2. Classificação das ações

Duas classificações se complementam:

- **Pelo estado da viga**, na linguagem da NBR 5674 (manutenção preventiva × corretiva):
  - preventiva: antes da despassivação, g > 0;
  - corretiva: depois da despassivação, g ≤ 0.
- **Pelo princípio da EN 1504-9**, a referência europeia de reparo e proteção do concreto. Para carbonatação interessam três:
  - Princípio 1: proteção contra o ingresso;
  - Princípio 7: preservar ou restaurar a passividade;
  - Princípio 11: controle das áreas anódicas, com tratamento da armadura.

O nosso modelo (Possan + g = c − y) representa só a **fase de iniciação**, até a despassivação. Ações que atuam na propagação da corrosão (hidrofugação para aumentar a resistividade, proteção catódica, reforço) não alteram g(t). Elas entram só como custo, ou ficam fora do escopo, declaradas como limitação.

---

## 3. Catálogo das ações

### 3.1 Inspeções (geram informação, não mudam g)

| Código | Ação | O que mede | Modelo | Custo (hipótese) |
|---|---|---|---|---|
| **I0** | Inspeção visual | Fissuras, manchas, destacamento | Detecta só corrosão avançada; não dá g. Útil apenas como gatilho tardio | λ ≈ 0,001 + mobilização |
| **I1** | Fenolftaleína + pacômetro (a do benchmark) | y_obs (σ_y ≈ 2,5 mm) e c_obs (σ_c ≈ 1,5 mm) | ĝ = c_obs − y_obs, σ_g = 2,92 mm | λ_insp ≈ 0,005 + mobilização |
| **I2** | I1 + ensaios de corrosão (potencial, resistividade) | Atividade de corrosão depois de g ≤ 0 | Separa "despassivada sem corrosão ativa" de "corroendo". Fora do modelo de iniciação; opcional | λ ≈ 0,008 + mobilização |

### 3.2 Ações preventivas (g > 0)

| Código | Ação (princípio EN 1504-9) | Efeito físico | **Como entra no emulador de g(t)** | Vida da ação | Custo (hipótese) |
|---|---|---|---|---|---|
| **P1** | Revestimento anticarbonatação (Princ. 1; EN 1504-2) | Barreira à difusão de CO₂; não recupera o que já carbonatou | **Desacelera o relógio.** Durante a vida do revestimento, a idade efetiva avança mais devagar: a_ef(t) = a(t_r) + φ·(t − t_r), com 0 ≤ φ ≤ 1. Então g(t) = G(u, a_ef; x). Mesmo u, mesmo x | L_P1 ≈ 10–15 anos (reaplicar) — **a calibrar** | λ_P1 ≈ 0,01–0,02 |
| **P2** | Aumento de cobrimento com argamassa (Princ. 7.1) | Acrescenta Δc sobre a armadura | **Soma Δc à margem:** g(t) = G(u, a; x) + Δc. É conservador, porque ignora que a camada nova também atrasa a frente. A versão exata é a "Solução 2" de duas camadas do documento de discussão | Permanente | λ_P2 ≈ 0,03–0,05 |
| **P3** | Realcalinização eletroquímica ou por difusão (Princ. 7.3/7.4) | Restaura o pH do cobrimento carbonatado sem remover o concreto | **Zera a idade do mesmo concreto:** g(t) = G(u, t − t_r; x), com **o mesmo u e o mesmo x**, porque o concreto é o mesmo. Recarbonatação mais rápida = fator > 1 na idade — **a calibrar** | Incerta na literatura — **a calibrar** | λ_P3 ≈ 0,04–0,06 |
| **R1** | Reparo localizado preventivo, "Solução 1" (Princ. 7.2 + 3) | Remove o concreto carbonatado além da armadura e recompõe com argamassa | **Material novo, idade zero, cobrimento mantido:** x' = (f_c,arg, UR, c_nom), u' ~ U(0,1) sorteado de novo | Governada pelo próprio modelo | **λ_prev = 0,08** |
| **R1+P1** | Reparo + revestimento (prática usual) | R1 seguido de P1 | R1 e, em seguida, o relógio lento de P1 sobre a argamassa | — | λ_prev + λ_P1 |

### 3.3 Ações corretivas (g ≤ 0)

| Código | Ação | Efeito | Modelo | Custo (hipótese) |
|---|---|---|---|---|
| **R2** | Reparo corretivo: R1 + limpeza e tratamento da armadura (Princ. 7.2 + 11) | Igual a R1, com área maior e tratamento do aço | Mesmo modelo de R1 | **λ_corr = 0,32** (razão λ_corr/λ_prev = 4; sensibilidade 2–8) |
| **R2+P1** | Corretivo + revestimento | R2 seguido de P1 | R2 e relógio lento | λ_corr + λ_P1 |
| **S** | Reforço ou substituição (perda de seção) | Fora do modelo de iniciação | Entra como **custo de risco**: λ_dep por ano despassivado sem reparo, ou custo terminal | λ_dep ≈ 0,02/ano (respeitar o limite físico, Seção 5) |

### 3.4 Ações que não entram como variável de decisão

- **Hidrofugação (silano/siloxano, Princ. 8).** Reduz a umidade interna, o que pode até **acelerar** a carbonatação, embora reduza a taxa de corrosão depois da despassivação. Como o modelo é de iniciação, ela não traz benefício em g(t). Deixe fora ou cite como limitação.
- **Proteção catódica (Princ. 10).** É mais usada em cloretos e é cara. Fica fora do escopo.

---

## 4. Ordem de grandeza relativa (preços de mercado, só para calibrar razões)

Faixas indicativas publicadas por empresas de recuperação. Não servem para custo absoluto no Brasil:

| Fonte | Revestimento anticarbonatação | Reparo completo (remoção + armadura + revestimento) | Razão reparo / revestimento |
|---|---|---|---|
| Reino Unido, 2026 ([MPS Concrete](https://www.mpsconcrete.com/concrete-repair-costs)) | £15–35/m² | £90–160/m² | ≈ 3–11 |
| Austrália (Sydney), 2026 ([Atomic Projects](https://www.atomicprojects.com.au/blog/can-concrete-cancer-be-fixed-sydney)) | A$45–95/m² | A$900–1800/m², incluindo acesso | ≈ 10–40 |

**Leitura.** O revestimento custa uma ordem de grandeza menos que o reparo. Com λ_prev = 0,08, isso dá λ_P1 ≈ 0,01–0,02, que é a hipótese da tabela. Calibrar no Brasil:
- SINAPI: composições de recuperação estrutural com argamassa polimérica, tratamento de armadura, pintura de proteção e andaime;
- orçamentos de 2 ou 3 empresas;
- divisão pelo custo de construção do elemento por m² de superfície.

---

## 5. Regras de consistência dos custos

1. **Limite físico do custo de risco.** Esperar Δt anos com a viga despassivada tem de custar mais que reparar já:
   λ_dep > λ_corr(1 − d^Δt) / Σ_{k=0}^{Δt−1} d^k.
   Para Δt = 10, r = 4 % e λ_corr = 0,32, isso dá λ_dep > 0,0123/ano.
2. **Preventivo mais barato que corretivo:** λ_prev < λ_corr. Senão nunca vale antecipar.
3. **Proteção mais barata que reparo:** λ_P1 < λ_prev. Senão o revestimento nunca entra na política.
4. **Argamassa melhor custa mais:** λ_prev(f_c,arg) crescente. Senão o otimizador sempre escolhe a de 50 MPa. Exemplo: λ_prev = 0,08·[1 + a(f_c,arg − 30)/20], com a a calibrar.
5. **Mobilização separada:** λ_mob por campanha (≈ 0,005–0,02, a calibrar). Isso torna vantajoso agrupar inspeção e reparo.
6. **Desconto real** r = 4 % (ISO 15686-5), com sensibilidade em 2–6 %.

---

## 6. Política com várias ações (o que vai para o multiobjetivo)

Com o catálogo, a política deixa de ter um único limiar e passa a ter **faixas de margem**, cada uma ligada a uma ação. A cada inspeção, com a leitura ĝ:

| Faixa da leitura | Ação |
|---|---|
| ĝ > g_A | Nada (A0) |
| g_B < ĝ ≤ g_A | Proteção (P1) se a viga ainda não tem revestimento válido |
| 0 < ĝ ≤ g_B | Reparo preventivo (R1, ou R1+P1), ou realcalinização (P3) |
| ĝ ≤ 0 | Reparo corretivo (R2, ou R2+P1) |

**Variáveis de decisão:**

θ = (t₁, Δt, g_A, g_B, f_c,arg, escolha R1 / R1+P1 / P3), com g_A ≥ g_B ≥ 0.

É uma política de controle com vários limiares, extensão direta da linha Grall/Park da [otimizacao_limiar.md](otimizacao_limiar.md).

**Objetivos sugeridos** (escolham 2 ou 3):

| Objetivo | Definição | Por quê |
|---|---|---|
| f₁ = E[LCC] | Custo descontado: inspeções + ações + mobilização + risco | Economia |
| f₂ = E[N_campanhas] ou E[N_reparos] | Idas à obra ou intervenções no concreto em 100 anos | Transtorno ao usuário (a sua pergunta original) |
| f₃ = P_desp ou min_t β(t) | Risco de despassivação na vida útil | Desempenho (fib 34, β_alvo = 1,3) |
| f₄ (opcional) | CO₂ incorporado das ações (argamassa, revestimento) | Sustentabilidade, tema em alta no SIE e no Struct. Saf. |

A restrição P_desp ≤ Φ(−β_alvo) pode entrar como restrição, ou f₃ fica como objetivo e o corte é feito depois, na frente de Pareto.

---

## 7. Estado de cada viga no simulador

Para o código ([otimizacao_limiar.py](otimizacao_limiar.py)) aceitar várias ações, cada viga carrega um estado:

| Variável de estado | Significado | Muda com |
|---|---|---|
| x | Material atual: original (f_c, UR, c_nom) ou argamassa (f_c,arg, UR, c_nom) | R1, R2 |
| u | Quantil da trajetória na nuvem de x | R1, R2 (sorteia de novo); P3 mantém |
| a | Idade efetiva da carbonatação | R1, R2, P3 zeram; P1 desacelera (fator φ) |
| t_P1 | Anos restantes do revestimento | P1 (= L_P1); diminui 1 por ano |
| Δc | Acréscimo de cobrimento | P2 |
| contadores e custos | N_campanhas, N_reparos, N_P1, custo descontado, anos despassivados | Cada ação |

Margem em cada ano:

$$
g(t) = G\big(u,\ a_\text{ef}(t);\ x\big) + \Delta c .
$$

Pseudocódigo de um ano t:

```
a_ef ← a_ef + (φ se t_P1 > 0 senão 1);  t_P1 ← max(t_P1 − 1, 0)
g ← G(u, a_ef; x) + Δc ;  g ← min(g, g_anterior do ciclo)
se g ≤ 0: anos_desp += 1; custo += λ_dep·d^t
se t é inspeção:
    custo += (λ_mob + λ_insp)·d^t ;  N_campanhas += 1
    ĝ ← g + ε
    aplicar a ação da faixa de ĝ (Seção 6); somar o custo da ação; atualizar o estado
```

---

## 8. Dados a levantar (checklist)

- [ ] Custos SINAPI (ou orçamentos) por m²: pintura anticarbonatação, argamassa de reparo com tratamento de armadura, realcalinização, andaime/acesso. Converter em λ = custo/C₀.
- [ ] Custo de construção C₀ do elemento por m² de superfície exposta (concreto + forma + armadura + mão de obra).
- [ ] Vida útil e eficiência do revestimento (L_P1, φ): literatura e fichas técnicas (resistência à difusão de CO₂ conforme EN 1504-2).
- [ ] Desempenho da realcalinização: duração do efeito e taxa de recarbonatação na literatura.
- [ ] f_c típico de argamassas de reparo (fichas técnicas), dentro do domínio do emulador (20–50 MPa).
- [ ] Emissões de CO₂ incorporado das ações, se f₄ for usado.
- [ ] Conferir na norma: definições da NBR 5674 (preventiva/corretiva) e da EN 1504-9 (princípios 1, 7, 11).

---

## 9. Referências

- EN 1504-9:2008 — princípios gerais de reparo e proteção do concreto; EN 1504-2 — sistemas de proteção superficial.
- ABNT NBR 5674 (manutenção de edificações), NBR 16747 (inspeção predial), NBR 15575 (vida útil de projeto), NBR 6118 (cobrimentos e classes de agressividade).
- fib Bulletin 34 (2006) — *Model Code for Service Life Design*, doi:10.35789/fib.bull.0034 (β_alvo na despassivação).
- ISO 15686-5 — custo do ciclo de vida (taxa de desconto real).
- Kong & Frangopol (2003) J Struct Eng — efeitos empíricos de ações de manutenção em β(t), doi:10.1061/(asce)0733-9445(2003)129:6(818).
- Lee et al. (2020) J Mater Civ Eng — LCC probabilístico de concreto carbonatado com reparo superficial, doi:10.1061/(asce)mt.1943-5533.0003390.
- Boschmann Käthler & Angst (2022) Struct Concrete — custo de estratégias de projeto e reparo, doi:10.1002/suco.202100784.
- Wittocx et al. (2022) J Build Eng — LCA/LCC de reparo de varandas com corrosão, doi:10.1016/j.jobe.2022.104436.
- Van Den Hende et al. (2024) Struct Concrete — estratégias de reparo na fase de iniciação, doi:10.1002/suco.202300784.
- Custos de mercado indicativos: MPS Concrete (Reino Unido, 2026) e Atomic Projects (Sydney, 2026), links na Seção 4.
