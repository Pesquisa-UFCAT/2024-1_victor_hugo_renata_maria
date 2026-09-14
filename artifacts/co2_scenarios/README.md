# Figuras do paper

Gerar com `.venv/bin/python scripts/plot_co2_scenarios.py` na raiz do projeto.

- `texto/artigo/z_co2_scenarios_pt.{png,pdf,svg}`: CO₂ atmosférico, 1980–2100.
- `texto/artigo/z_co2_scenarios_en.{png,pdf,svg}`: mesma figura em inglês.
- `texto/artigo/z_carbonation_fck_{pt,en}.{png,pdf,svg}` e
  `z_carbonation_rh_{pt,en}.{png,pdf,svg}`: perfis paramétricos atualizados.
- `co2_1980_2100.csv`: valores anuais das três curvas em ppm.
- `carbonation_reference_2000_2100.csv`: dados dos perfis de referência.

O estilo segue as figuras científicas do projeto: fontes serifadas, matemática
Computer Modern, eixos com moldura, grade discreta, legendas internas, sem título
ou referências dentro da imagem. A atribuição das fontes está na legenda LaTeX.

Os perfis de carbonatação são ilustrações determinísticas calculadas diretamente
pela função de Possan existente, sob SSP2-4.5, construção em 2000 e 100 anos de
exposição. Não são novos resultados probabilísticos de confiabilidade ou RUL.
Usam a avaliação instantânea com máximo acumulado; não implementam uma nova
integração do histórico de exposição.

As figuras de comparação com a antiga curva polinomial foram substituídas.
A fonte dos dados e as instruções de extração estão em `data/co2/README.md`.
