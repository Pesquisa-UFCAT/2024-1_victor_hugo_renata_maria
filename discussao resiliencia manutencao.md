# Contexto para continuação — Paper de Otimização de Manutenção (Vitor) e Extensão para Resiliência

> Documento de transferência de contexto. Objetivo: retomar a discussão técnica abaixo em outra sessão, já com os dados reais do repositório/emulador (PyGLAM) para gerar os resultados numéricos e fechar as decisões de modelagem.

---

## 1. Contexto do trabalho

Grupo de pesquisa (UFCAT/UMN/NICEN) desenvolveu o **PyGLAM**, um emulador estocástico que combina:

- **GLD** (Generalized Lambda Distribution) — devolve a distribuição completa, não ponto estimado
- **PCE** (Polynomial Chaos Expansion)
- **Camada temporal de ML** — captura dependência entre passos de tempo

Aplicação: **corrosão de armadura induzida por carbonatação** em concreto armado, usando o **modelo de Possan (2010)** como modelo mecanístico de referência para treino.

Limite de estado (fase de iniciação apenas, não propagação):

$$g(t) = c - x_c(t)$$

onde $c$ é o cobrimento e $x_c(t)$ a profundidade de carbonatação. $g \le 0$ marca o fim do período de iniciação (despassivação), **não** falha estrutural — importante deixar isso explícito no texto para evitar crítica de revisor.

Dois papers em andamento:

1. **Paper RUL** — em estágio inicial, foco em Remaining Useful Life probabilístico.
2. **Paper de manutenção (com Vitor)** — quase pronto, é o objeto desta discussão. Aplica o emulador a otimização de política de manutenção. Alvo: **Reliability Engineering & System Safety** (IF ~9).

---

## 2. Estrutura do modelo de Possan usada (relevante para a extensão de cenários de CO₂)

A forma do modelo tem CO₂ entrando **aditivamente no expoente**, não dentro de uma integral temporal:

$$e_c \propto \sqrt{f(f_{ck})} \cdot \sqrt{t} \cdot \exp\!\left[\text{termo}_{ad} + k_{CO2}\frac{\sqrt{CO2}}{60+f_{ck}} - \text{termo}_{UR}\right]$$

**Resultado derivado (proposição candidata para o paper):** como o termo de CO₂ é aditivo no expoente, ele fatoriza multiplicativamente. Trocar de cenário de CO₂ equivale a multiplicar $e_c$ por um fator $\rho(t, f_{ck})$ que depende só de CO₂ e $f_{ck}$ — não de UR, cobrimento, tipo de cimento. Isso implica:

$$g_{\text{cenário}}(t) = c\,(1-\rho) + \rho\, g_{\text{ref}}(t)$$

— uma **transformação afim** de $g$. A GLD é fechada sob transformação afim ($\lambda_3,\lambda_4$ de forma inalterados; $\lambda_1,\lambda_2$ transformam analiticamente). **Consequência prática:** transferência entre cenários de CO₂ sem retreinar o emulador. Ainda a validar numericamente contra o modelo mecanístico bruto.

Observação importante: a Possan foi calibrada com teor de CO₂ ambiente **urbano** (Helene 1993: 0,1%–1,2%), não concentração atmosférica global. A variação entre cenários climáticos globais (SSP1-2.6 a SSP5-8.5, ~0,04% a ~0,1%) é pequena frente à dispersão urbana local — achado que pode reformular o enquadramento do exemplo de cenários ("microclima urbano domina o sinal climático global").

---

## 3. Modelo de reparo — decisão fechada

**Reparo mais comum em vigas (referência de prática):** reconstituição localizada do cobrimento (*patch repair*), removendo o concreto carbonatado **além da posição da armadura** (15–20 mm extra, para garantir envolvimento completo da barra). Isso foi confirmado como prática dominante tanto na literatura quanto na execução real.

### Erro identificado e corrigido durante a discussão

Proposta inicial (rejeitada): após reparo, cobrimento restaurado como $c' = \gamma \cdot c_{\text{nom}}$, com $\gamma$ variável aleatória. **Isso está errado** — o cobrimento é distância física até a armadura, que não se move. Reduzir o cobrimento simularia mover a armadura, o que não corresponde à física do reparo.

### Solução adotada — "Solução 1"

Como a remoção **sempre ultrapassa a posição da armadura**, todo o cobrimento após reparo é do **material novo** (argamassa de reparo). Não há duas camadas, não há problema de material heterogêneo dentro do cobrimento. Estado após o $m$-ésimo reparo:

$$\mathbf{x}^{(m+1)} = \{f_{ck}^{\text{arg}},\ UR,\ c_{\text{nom}}\}, \qquad a \leftarrow 0$$

- **Cobrimento: inalterado** ($c_{\text{nom}}$, sempre)
- **$f_{ck}$: muda** para o $f_{ck}$ da argamassa de reparo (tipicamente superior ao concreto original)
- **Idade: reinicia** (zera o relógio de carbonatação)

Isso mantém o emulador dentro do domínio de treino (material homogêneo), sem necessidade de hipóteses extras.

### Solução 2 (guardada para apêndice / dissertação — não usar no exemplo principal)

Para o caso de remoção **parcial** (não ultrapassa a armadura), foi derivado um modelo de duas camadas usando o fato de que $e_c(t) = c - g(t)$ é recuperável do emulador. Por quantil $u$ fixo (assumindo comonotonicidade temporal):

$$e_c(a;u) = \begin{cases} A_{\text{arg}}(u)\sqrt{a}, & a \le t_1(u) \\ \sqrt{d^2 + A_0^2(u)(a-t_1(u))}, & a > t_1(u) \end{cases}, \qquad t_1(u) = \left(\frac{d}{A_{\text{arg}}(u)}\right)^2$$

Tempo total até despassivação: $T_{\text{desp}}(u) = \dfrac{d^2}{A_{\text{arg}}^2(u)} + \dfrac{c_{\text{nom}}^2 - d^2}{A_0^2(u)}$.

Fórmula fechada por quantil, sem retreino — mas exige a hipótese extra de comonotonicidade. Manter como extensão, não no exemplo principal.

### Verificação pendente antes da varredura de otimização

Como $f_{ck}^{\text{arg}} > f_{ck}^0$ tipicamente, o segundo ciclo de carbonatação dura mais que o primeiro (dentes do serrilhado ficam mais largos). Checar que, no horizonte de análise adotado ($T_{SL}$), ocorrem **pelo menos 2 reparos** — caso contrário a superfície de custo não tem vale e a otimização perde sentido. Se necessário: estender $T_{SL}$ para 150 anos, reduzir $f_{ck}^{\text{arg}}$, ou partir de $c_{\text{nom}}$ menor (25 mm, CAA II) / $f_{ck}^0$ menor (20 MPa).

---

## 4. Formulação da função objetivo (versão final acordada)

### Adimensionalização

$$\lambda_i = \frac{C_i}{C_0}, \qquad i \in \{\text{insp, prev, corr}\}$$

Custo de construção $C_0 \equiv 1$.

### Critério de gatilho — com margem $\varepsilon$

Decisão importante: usar margem de segurança ($\varepsilon = 10$ mm, por exemplo) em vez de esperar $g \le 0$, para refletir prática real de antecipação. Recomendação: **fixar $\varepsilon$** (não otimizar) e otimizar apenas $(p^*, \Delta t)$, com sensibilidade posterior em $\varepsilon$ — evita redundância entre variáveis de decisão.

$$\pi_j = \mathbb{P}\left[g^{(m_j)}(a_j) \le \varepsilon\right] = u^* : Q\left(u^*; \boldsymbol\lambda(a_j, \mathbf{x}^{(m_j)})\right) = \varepsilon$$

$Q$ = função quantílica da GLD devolvida pelo emulador. Inversão por **bisseção numérica** — sem Monte Carlo. Validar `pf_margem`/`pf_from_gld` contra MC bruto do modelo de Possan em 5–10 pontos antes de prosseguir.

### Gatilho

$$\delta_j = \mathbb{1}[\pi_j > p^*]$$

### Custo esperado do reparo (chave conceitual: não se decide corretivo/preventivo, pondera-se)

$$\lambda_{\text{rep}}(\pi_j) = \lambda_{\text{corr}}\,\pi_j + \lambda_{\text{prev}}\,(1-\pi_j)$$

Razão $\lambda_{\text{corr}}/\lambda_{\text{prev}} \in [2,8]$ — parâmetro econômico, não mecânico (o modelo não representa propagação de corrosão; isso deve ir para a seção de limitações).

### Função objetivo completa

$$\Lambda(p^*, \Delta t) = 1 + \sum_{j=1}^{J} \frac{\lambda_{\text{insp}} + \delta_j\left[\lambda_{\text{corr}}\pi_j + \lambda_{\text{prev}}(1-\pi_j)\right]}{(1+r)^{t_j}}, \qquad J = \left\lfloor \frac{T_{SL}}{\Delta t}\right\rfloor$$

### Problema de otimização

$$\begin{aligned}
(p^*, \Delta t)^\star = \; & \arg\min_{p^*,\Delta t} \Lambda(p^*,\Delta t) \\
\text{s.a.} \quad & \pi_j \le \Phi(-\beta_{\text{alvo}}) \quad \forall j \\
& \mathbf{x}^{(m)} \in \mathcal{X}_{\text{treino}} \quad \forall m
\end{aligned}$$

### Meta de reliability index

$\beta_{\text{alvo}} \approx 1{,}3$ (fib Bulletin 34, estado-limite de despassivação — **estado-limite de serviço**, não usar $\beta$ de colapso 3,8/4,3 do Eurocódigo). Confirmar valor exato na edição do fib 34 disponível. Fazer sensibilidade em $\beta_{\text{alvo}} \in \{1{,}0;\ 1{,}3;\ 1{,}5\}$. Interessante reportar também o $\beta$ implícito da solução puramente econômica (sem restrição) comparado ao normativo.

### Taxa de desconto

$r$ deve ser taxa **real** (já que custos foram adimensionalizados). Base: $r = 0{,}04$ (ISO 15686-5). Sensibilidade obrigatória em $r \in \{0{,}02;\ 0{,}04;\ 0{,}06\}$ — mecanismo: $r$ alto empurra a política ótima para "adiar/menos preventivo"; $r$ baixo empurra para mais preventivo. Boa figura candidata.

### Leitura do resultado

$$\Lambda - 1 = \text{custo de durabilidade (múltiplo do custo de construção)}$$

---

## 5. Plano de geração de resultados (ordem recomendada)

1. Validar `pf_from_gld`/`pf_margem` (inversão da quantílica) contra Monte Carlo bruto do modelo de Possan
2. Simular sem reparo (gatilho nunca dispara) → curva de $\pi(t)$ crescente monotônica, teste de sanidade
3. Simular com reparo (Solução 1) → conferir serrilhado, contar número de dentes em $T_{SL}$ (mínimo 2)
4. Varredura em grade 2D: $p^* \in [0{,}01, 0{,}45]$ (~40 valores) × $\Delta t \in \{2,5,10,15,20\}$ → superfície $\Lambda(p^*,\Delta t)$, identificar ótimo global
5. Introduzir incerteza nos inputs de reparo/entrada com Monte Carlo leve (~500 amostras, só sobre poucas dimensões, não sobre a cauda de $g$)
6. Sensibilidade: $r$, $\lambda_{\text{corr}}/\lambda_{\text{prev}}$, $\beta_{\text{alvo}}$, $\varepsilon$
7. Validação cruzada: recomputar 4–5 políticas com MC bruto no modelo mecanístico; checar preservação do **ranking** das políticas (mais importante que erro absoluto em $\Lambda$)

Parâmetros de partida sugeridos:

```python
par = dict(
    T_SL=150, r=0.04, eps=0.0,
    lam_insp=0.005, lam_prev=0.08, lam_corr=0.32,
    fck_0=20.0, fck_arg=30.0, ur=0.70, c_nom=25.0,
)
```

---

## 6. Extensão para resiliência — ideação (para segundo paper, não para o atual)

### Por que não usar "resiliência" ingenuamente

Definição consolidada (Bruneau et al. 2003; Cimellaro): resiliência é sobre **perturbação súbita + recuperação**, métrica canônica $R = \int [1-Q(t)]\,dt$. Carbonatação é degradação lenta e monotônica — **não** é perturbação. Chamar isso de "resiliência" sem reformulação é vulnerável à crítica de uso de buzzword por revisor familiarizado com a literatura.

### Opção A (mais fraca) — recuperabilidade

Tratar o próprio reparo programado como "evento de recuperação", com $Q(t) = 1-\pi(t)$ ou $\beta(t)/\beta_0$. O serrilhado já existente vira a "assinatura" clássica. **Fraqueza:** não há perturbação exógena real — declínio e recuperação são ambos programados/determinísticos-em-tendência. Revisor atento identifica isso como "manutenção redesenhada como resiliência".

### Opção B (recomendada) — resiliência a choques exógenos na degradação

Introduzir um **choque real e exógeno** no ambiente ou na gestão:

- **Choque de CO₂** — mudança de uso do entorno (nova via expressa, industrialização) eleva o teor urbano de CO₂ em um instante $t_s$. Tratável **sem retreino**, via a transformação afim de cenário já derivada (Seção 2).
- **Choque de gestão** — interrupção orçamentária, suspensão de inspeções por $N$ anos (relevante e pouco explorado no contexto brasileiro).
- **Choque de exposição/umidade** — mudança de microclima.

**Pergunta de pesquisa:** a política ótima sob condições nominais permanece adequada após um choque, ou existe uma política subótima-no-nominal mais robusta?

### Métricas propostas

$$\mathcal{R}(\mathbf{d}) = \frac{\Lambda_{\text{nominal}}(\mathbf{d})}{\Lambda_{\text{choque}}(\mathbf{d})} \qquad \text{ou} \qquad \Delta\Lambda(\mathbf{d}, t_s) = \Lambda_{\text{choque}}(\mathbf{d}, t_s) - \Lambda_{\text{nominal}}(\mathbf{d})$$

Figura sugerida: mapa de $\Delta\Lambda$ no plano (instante do choque $t_s$ × intensidade do choque), comparando política ótima nominal vs. política robusta.

### Hipótese de resultado a testar

Políticas com $\Delta t$ curto (inspeção frequente) são mais caras no cenário nominal, mas **detectam o choque mais cedo** e permitem correção adaptativa; políticas com $\Delta t$ longo são "cegas" ao choque. Se confirmado: resultado do tipo "inspeção frequente compra informação, não só antecipação" — conecta com literatura de valor da informação (VoI), bem estabelecida em RESS.

### Recomendação de sequenciamento

Tratar como **segundo paper**, não como seção do paper atual — evita diluir a contribuição metodológica central (o emulador) e evita alongar demais o manuscrito 2. Ambos os papers compartilham a mesma base computacional (PyGLAM + Possan + formulação de custo), o que reduz custo marginal do segundo trabalho.

---

## 7. Pontos em aberto para a próxima sessão

- [ ] Confirmar exatamente como o Vitor implementou a dependência de $g$ em CO₂(t) — substituição direta na fórmula fechada da Possan, ou integração incremental? Decide se a invariância afim vale exatamente ou precisa de tabela de correção numérica.
- [ ] Rodar validação de `pf_from_gld` contra MC no repositório real
- [ ] Rodar checagem de número de dentes do serrilhado com os dados reais de treino (confirmar se $T_{SL}=150$ anos e os $f_{ck}$ escolhidos produzem ≥2 reparos)
- [ ] Confirmar valor exato de $\beta_{\text{alvo}}$ na edição do fib Bulletin 34 disponível
- [ ] Decidir se o exemplo final usa restrição de $\beta$ fixa (normativa) ou deixa $p^*$ livre e reporta o $\beta$ implícito do ótimo econômico
- [ ] Levantar fonte de custos unitários (SINAPI ou equivalente) para calibrar $\lambda_{\text{insp}}, \lambda_{\text{prev}}, \lambda_{\text{corr}}$
- [ ] Avaliar viabilidade de incluir um segundo modelo mecanístico de referência (além da Possan) para responder à crítica de dependência de um único modelo empírico brasileiro
