# Port para o modelo — o que foi feito

**Data:** 2026-07-19
**Pasta gerada:** `papers/final/`
**Idioma:** português (traduzido apenas o *scaffolding* do modelo)
**Fonte do conteúdo:** `papers/old/` (texto dos alunos) + `papers/paper_model/` (template)

---

## 1. Decisões adotadas

| Decisão | Escolha | Motivo |
|---|---|---|
| Idioma | Português | Preservar 100% do texto dos alunos; dissertação em PT. Tradução para EN fica para a passada final se houver submissão internacional. |
| Estrutura | Documento único estendido | Conforme sua orientação: escrever tudo em um só e depois deletar o que for para artigo. |
| Nova ordem de seções | Introdução → Emuladores → Aprendizado de Máquina → Metodologia → Resultados → Conclusões | Estrutura que você propôs. |
| Bibliografia | `biblatex` + `biber` (APA), como no modelo | `\citep`/`\citet` → `\parencite`/`\textcite` (conversão completa). |
| Marcação de pendências | Macros `\falta{...}` (vermelho) e `\faltanum` | Tornar visível, na compilação, tudo que ainda falta escrever/calcular. |

---

## 2. Estrutura de arquivos de `papers/final/`

```
main.tex                  ← ordem das seções (nova estrutura)
preamble.tex              ← preâmbulo do modelo + babel PT + macros \falta
references.bib            ← cópia do mybibfile.bib dos alunos (38 refs)
title_authors.tex         ← título (PT+EN), autores, afiliações
abstract_keywords.tex     ← RESUMO redigido (rascunho) + palavras-chave PT/EN
00_nomenclature.tex       ← nomenclatura construída a partir dos símbolos do paper
01_introducao.tex         ← S1 dos alunos (verbatim) + roteiro reescrito p/ nova estrutura
02_emuladores.tex         ← teoria: simulador estocástico, GLD, MoM, PCE (de S4)
03_aprendizado_maquina.tex← SEÇÃO NOVA: fundamentos de ML + subseção Redes Neurais
04_metodologia.tex        ← carbonatação (S2) + resistência residual/g (S3) +
                            construção do emulador (S4) + ponte para RUL (S5)
05_resultados.tex         ← Ex.1 benchmark (verbatim) + Ex.2 e Ex.3 (estrutura + \falta)
06_conclusoes.tex         ← S7 dos alunos
declarations.tex          ← conflitos/CRediT/financiamento/dados (traduzido, com \falta)
appendices.tex            ← Apêndice A: exemplo passo a passo t=40 anos (preservado de old/old)
+ 32 imagens z_*.png/jpg   ← copiadas de old/
```

## 3. Mapa: seções antigas → nova estrutura

| Antiga (`old/`) | Vai para (`final/`) |
|---|---|
| S1 Introdução | §1 Introdução (verbatim; só o parágrafo-roteiro mudou) |
| S2 Carbonatação (fenômeno, Possan, dataset, CO₂) | §4.1 Metodologia |
| S3 Resistência residual + função g | §4.2 Metodologia |
| S4 Emulador (simulador, GLD, MoM, PCE) | §2 Emuladores |
| S4 Emulador (camada temporal, métricas de validação) | §3 ML + §4.3 Metodologia |
| S5 Da distribuição emulada à RUL | §4.4 Metodologia |
| S6 Resultados (Ex.1, Ex.2, Ex.3) | §5 Resultados |
| S7 Conclusões | §6 Conclusões |
| old/old Section_5 (exemplo passo a passo) | Apêndice A |

## 4. O que foi **preservado** (texto dos alunos, quase verbatim)

- Toda a Introdução, a fenomenologia da carbonatação, o modelo de Possan, o dataset,
  a formulação de resistência residual e a função de estado limite.
- A teoria do emulador (GLD, método dos momentos, PCE) e a ponte para RUL/VaR/CVaR.
- **O Exemplo 1 (benchmark) completo**, com todos os números, tabelas e figuras —
  exatamente como você pediu (você deleta depois, se quiser).
- O exemplo numérico passo a passo (t = 40 anos, g(40) = 10,39 kN·m) → Apêndice A.

## 5. O que foi **escrito novo** (por mim)

- **§3 Aprendizado de Máquina** inteira: framing de regressão supervisionada como camada
  do emulador + subseção **Redes Neurais** (MLP: forward pass, ativação, treino,
  regularização, restrição λ₂>0). Marcado com `\falta` onde vocês precisam inserir a
  arquitetura e a biblioteca efetivamente usadas.
- Resumo (abstract) em rascunho.
- Nomenclatura completa.
- Textos de transição/costura entre as seções reordenadas.
- Scaffolding traduzido (declarações, apêndices, legendas).

## 6. Como compilar

Projeto pronto para **Overleaf** (ou local com `latexmk`):

```
latexmk -pdf -bibtex- -pdflatex main.tex   # usa biber automaticamente
# ou no Overleaf: compilador pdfLaTeX, que já chama biber
```

- As macros `\falta{...}` aparecem em **vermelho** no PDF — são o seu mapa de pendências.
- Se uma imagem faltar, o preâmbulo desenha uma caixa "Figura ausente" em vez de quebrar.
- Antes de submeter: remover as macros `\falta`/`\faltanum` (basta redefini-las como vazias
  no preâmbulo) e conferir os metadados marcados `[XXXX]` no `references.bib`
  (refs do grupo: `couto2025`, `pires2024`, e datas de acesso do NOAA).

> O plano de melhorias para transformar isto em artigo de revista Q1/JCR está em
> `PLANO_MELHORIAS_JCR_Q1.md`.
