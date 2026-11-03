# Viga de referência para os custos de manutenção

O objetivo é sair dos custos relativos chutados (λ_prev = 0,08, λ_corr = 0,32 etc.) e chegar a custos **levantados**. A receita: uma viga concreta, quantidades de cada serviço e preços unitários do SINAPI ou de cotação. Cada λ = C_ação / C₀ sai da mesma viga.

- Planilha para preencher: [viga_referencia_custos.xlsx](viga_referencia_custos.xlsx). As quantidades já estão calculadas por fórmula. Basta preencher as células amarelas de **preço unitário**, e a aba `Resumo` dá os λ e as verificações de consistência.
- Catálogo das ações: [../acoes_manutencao_custos.md](../acoes_manutencao_custos.md).

---

## 1. A viga

| Item | Valor | Comentário |
|---|---|---|
| Esquema | Biapoiada, vão L = 5,0 m | Viga de edifício (piso), face inferior e laterais expostas ao ar |
| Seção | b × h = 20 × 50 cm, laje de 10 cm | A parte exposta da viga é a que fica abaixo da laje (40 cm) |
| Concreto | C25 (f_ck = 25 MPa), CP II F | Caso-base do Paper 1 |
| Aço | CA-50 (longitudinal), CA-60 (estribos) | |
| Cobrimento | c_nom = 25 mm (até o estribo) | Caso-base do Paper 1 |
| Ambiente | Externo protegido da chuva (PEA no Possan), UR = 55 % | Caso-base do Paper 1 |
| Cargas | g_k = 15 kN/m (inclui peso próprio de 2,5 kN/m), q_k = 5 kN/m | Hipótese típica de viga de piso; pode ajustar |

> **Atenção à classe de agressividade.** Pela NBR 6118 (Tab. 7.1 e 7.2), c_nom = 25 mm em viga corresponde à **CAA I**. Em ambiente urbano (CAA II) a norma pede 30 mm e C25. Duas saídas: (i) declarar a viga como CAA I ou como execução abaixo da norma (caso realista de estrutura antiga, construída em 1980); ou (ii) fazer uma segunda viga com 30 mm e comparar. A planilha aceita a troca: basta mudar o cobrimento na aba `Entradas`.

### Dimensionamento simplificado (só para o levantamento de quantidades)

Verificação de ELU à flexão e ao cisalhamento. Não é um projeto completo: não verifica ELS, e a ancoragem foi simplificada.

| Grandeza | Valor |
|---|---|
| M_k = p·L²/8 | 62,5 kN·m |
| M_d = 1,4·M_k | 87,5 kN·m |
| d = h − (c + φ_t + φ_l/2) | 463,8 mm |
| K_md = M_d/(b·d²·f_cd) | 0,114; x/d = 0,181 (domínio 2) |
| A_s necessária | 4,68 cm² → **4 φ 12,5** (4,91 cm²); A_s,mín = 1,50 cm² |
| V_d | 70,0 kN; V_c = 71,4 kN → estribo mínimo |
| A_sw/s,mín = 0,2·f_ctm/f_ywk·b | 2,05 cm²/m → **φ 5,0 c/18** (2 ramos) |
| Porta-estribos | 2 φ 8,0 |

### Quantidades de construção (C₀)

| Item | Quantidade |
|---|---|
| Concreto | V = 0,20 × 0,50 × 5,0 = **0,50 m³** |
| Fôrma (fundo + 2 laterais) | (0,20 + 2 × 0,50) × 5,0 = **6,0 m²** |
| Aço CA-50 φ12,5 | 20,8 kg |
| Aço CA-50 φ8,0 | 4,3 kg |
| Aço CA-60 φ5,0 (28 estribos de 1,30 m) | 5,6 kg |
| Total de aço (sem perdas) | 30,7 kg (61 kg/m³); a planilha aplica 10 % de perda |

**Definição de C₀:** custo **direto** da viga (concreto, fôrma, escoramento, armação, lançamento, cura), sem a parcela do edifício. Assim todos os λ ficam na mesma base.

---

## 2. Quantidades das ações de manutenção

Área exposta, usada nas ações de superfície:

A_exp = (b + 2·(h − h_laje))·L = (0,20 + 2 × 0,40) × 5,0 = **5,0 m²**

### O ponto que mais pesa: o volume removido no reparo "Solução 1"

A Solução 1 remove o concreto carbonatado **até 15–20 mm atrás da armadura**:

profundidade = c + φ_estribo + φ_long + folga = 25 + 5 + 12,5 + 20 = **62,5 mm**

| Extensão do reparo | Área | Volume removido | % do volume da viga |
|---|---|---|---|
| Toda a superfície exposta (fundo + laterais) | 5,0 m² | **0,31 m³** | **62 %** |
| Só a zona inferior (fundo + 15 cm das laterais) | 2,5 m² | 0,16 m³ | 31 % |

**Leitura.** Numa viga de 20 cm de largura, recompor todo o cobrimento até atrás das barras significa remover e refazer **mais da metade da viga**, com escoramento. Com mão de obra de demolição e argamassa polimérica (bem mais cara por m³ que concreto novo), é provável que λ_prev saia **bem acima de 0,08**, talvez da ordem de C₀. A planilha vai responder isso. Se confirmar, há três consequências para o modelo:

1. o reparo completo deixa de ser "preventivo barato" e passa a competir com a **substituição** da viga;
2. as ações de superfície (P1 pintura, P3 realcalinização) ganham peso como preventivas de verdade;
3. a fração reparada α (parâmetro na planilha) vira uma decisão relevante, e não um detalhe.

### Serviços por ação

São os mesmos blocos da aba `Acoes` da planilha. As quantidades são calculadas pelas fórmulas a partir da aba `Entradas`.

| Ação | Serviços | Quantidade por viga |
|---|---|---|
| **MOB** — mobilização por campanha | Mobilização da equipe (verba ÷ nº de vigas da campanha); andaime ou plataforma; isolamento | 1/20 vb; 5,0 m²; 1/20 vb |
| **I1** — fenolftaleína + pacômetro | Pontos de fenolftaleína; recomposição dos furos; pacometria; horas de engenheiro (laudo) | 3 un; 3 un; 5,0 m; 1 h |
| **P1** — pintura anticarbonatação | Limpeza / hidrojateamento; revestimento anticarbonatação em 2 demãos | 5,0 m²; 5,0 m² |
| **P2** — aumento de cobrimento (Δc = 15 mm) | Apicoamento; ponte de aderência; argamassa | 5,0 m²; 5,0 m²; 0,075 m³ |
| **P3** — realcalinização | Serviço especializado (cotação) | 5,0 m² |
| **R1** — reparo preventivo (Solução 1) | Escoramento; remoção do concreto; limpeza da armadura; argamassa polimérica estrutural; cura; entulho | 5,0 m; 0,31 m³; 5,0 m²; 0,31 m³; 5,0 m²; 0,31 m³ |
| **R2** — reparo corretivo | R1 + limpeza até metal branco + primer anticorrosivo + reposição de 10 % da armadura longitudinal | Idem R1; 5,0 m²; 5,0 m²; 2,3 kg |

---

## 3. Como preencher

1. **Escolher a base de preços e manter até o fim:** SINAPI de um estado e de um mês de referência (por exemplo GO), desonerado ou não. Anotar a escolha na planilha.
2. **Preencher o preço unitário (R$) de cada linha amarela** nas abas `C0_construcao` e `Acoes`. A coluna "O que buscar" diz o serviço. Para cada um, procurar a composição SINAPI equivalente e **anotar o código ao lado**.
3. **O que não estiver no SINAPI** vem de cotação, com 2 ou 3 fornecedores: realcalinização, ensaios de fenolftaleína e pacometria, pintura anticarbonatação específica, argamassa polimérica estrutural. Registrar a fonte.
4. **Ajustar as entradas** que são decisões de engenharia:
   - α_prev e α_corr: fração da área reparada;
   - nº de vigas por campanha: rateio da mobilização;
   - pontos de ensaio por viga;
   - Δc.
5. **Ler a aba `Resumo`:**
   - λ de cada ação;
   - razão λ_corr/λ_prev (o modelo supunha entre 2 e 8);
   - verificações P1 < R1 < R2;
   - λ_dep mínimo pela regra física.
6. **Levar os λ para o código:** o dicionário `CUSTOS` em [../otimizacao_limiar.py](../otimizacao_limiar.py), e para a tabela de [../acoes_manutencao_custos.md](../acoes_manutencao_custos.md).

> A planilha foi testada com preços fictícios de R$ 100 em todas as linhas, só para conferir as fórmulas. Todas calcularam sem erro. Os λ que saem disso não têm significado.

---

## 4. Decisões que a viga de referência obriga a tomar

- [ ] CAA I com 25 mm, ou CAA II com 30 mm, ou as duas.
- [ ] Extensão do reparo: toda a superfície exposta ou só a zona da armadura longitudinal (α).
- [ ] Se o reparo completo sair perto de C₀: incluir **S — substituição da viga** como ação explícita, com custo ≈ C₀ + demolição + escoramento.
- [ ] Nº de vigas por campanha (edifício de referência). Isso define quanto a mobilização pesa no "número de manutenções".
- [ ] Custo da inspeção por viga: o laboratório costuma cobrar por ponto de ensaio mais a visita.
