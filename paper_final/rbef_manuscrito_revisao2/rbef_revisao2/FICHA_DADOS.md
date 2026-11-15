# Ficha dos dados — estação automática A001 (Brasília, DF)

Itens marcados com **[AUTORES]** precisam ser preenchidos ou confirmados antes da submissão.

| Item | Valor |
|---|---|
| Fonte | INMET, Banco de Dados Meteorológicos (BDMEP), https://bdmep.inmet.gov.br/ |
| Produto / consulta | Dados diários de estação automática **[AUTORES: nome exato do produto e parâmetros da consulta]** |
| Data de obtenção | **[AUTORES]** |
| Estação | A001, Brasília (DF), código OMM 86715; 15,79° S, 47,93° W; 1.161 m |
| Período do arquivo | 06/05/2000 a 25/04/2025; 9.121 dias de calendário, sem datas repetidas |
| Campos originais usados | **[AUTORES: nomes das colunas no arquivo do BDMEP]** → `data`, `precipitacao_mm`, `temperatura_c`, `umidade_relativa_pct`, `vento_ms` |
| Definição da média diária | Valor diário fornecido pelo INMET a partir dos registros horários; não recalculado pelos autores **[AUTORES: confirmar; informar horários e fuso (UTC)]** |
| Critério de completude diária | **[AUTORES: critério do INMET para gerar o valor diário, se documentado]** |
| Altura do anemômetro | 10 m **[AUTORES: confirmar na ficha da estação]** |
| Mudanças de sensor | Não documentadas no arquivo; não avaliadas |
| Passo de registro | 0,1 m/s (vento), 0,1 °C (temperatura) — passo do arquivo, não resolução metrológica |
| Falhas de vento | 281 dias vazios; 101 interrupções entre registros válidos, a maior de 29 dias |
| Transformações feitas pelos autores | Renomeação de colunas e conversão de datas; nenhuma interpolação ou preenchimento de falhas |
| Leitura | Células "Leitura e exame de qualidade dos dados" de `rbef_notebook.ipynb` |
