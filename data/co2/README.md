# Concentração atmosférica de CO₂ — CMIP6 / SSP

`co2_concentrations_1900_2100.csv` contém médias globais anuais em **ppm**.
São concentrações atmosféricas, não emissões, consumo de carbono ou CO₂ equivalente.

- 1900–2014: histórico comum aos três cenários, Meinshausen et al. (2017),
  https://doi.org/10.5194/gmd-10-2057-2017.
- 2015–2100: SSP1-2.6, SSP2-4.5 e SSP5-8.5, Meinshausen et al. (2020),
  https://doi.org/10.5194/gmd-13-3571-2020.
- Origem: suplemento de 2020, abas T2, T4, T5 e T11; coluna B: CO2 / ppm / World.
  As abas SSP descrevem 2015–2016 como baseados em observações. Os demais anos
  seguem as trajetórias publicadas, sem atualização com observações recentes.
- A extração não ajusta regressões, não corrige os cenários e não extrapola.
  Os números são gravados com nove casas decimais em ppm para preservar a fonte;
  isso não representa precisão observacional de nove casas.
- `sources.json` registra URL, DOI, licença e SHA-256 do ZIP e do CSV.
  Dados distribuídos sob CC BY-SA 4.0, conforme a seção Data availability da fonte.

## Uso

```python
from functions import co2_percentage_year

co2_percentage_year(2050, "SSP2-4.5")  # aproximadamente 0.0506875 (%)
co2_percentage_year(2100, "SSP5-8.5")  # aproximadamente 0.1135210 (%)
co2_percentage_year(1980, "SSP1-2.6")  # histórico, igual nos três cenários
```

A função converte ppm para % dividindo por 10.000. Aceita anos fracionários por
interpolação linear e rejeita anos fora de [1900, 2100]. O padrão é SSP2-4.5;
`ssp126`, `ssp245` e `ssp585` são abreviações aceitas.

O ano é de calendário: para uma estrutura de 2000 com idade 100, consultar 2100.
O intervalo de CO₂ não determina o domínio de validade do modelo de carbonatação.

## Reprodução

Baixar o ZIP indicado em `sources.json` e executar, na raiz do projeto:

```bash
.venv/bin/python scripts/extract_co2_scenarios.py /caminho/supplement.zip
.venv/bin/python scripts/plot_co2_scenarios.py
```

O uso da função e a geração das figuras não precisam de rede. Os arquivos PNG,
PDF e SVG em português e inglês são escritos em `texto/artigo/`.

Os arquivos de simulação novos incluem `_co2_SSP2-4.5` (ou o cenário escolhido)
no nome. As tabelas geradas também registram o cenário e a fonte nos atributos.
Resultados anteriores da curva polinomial precisam ser recalculados: não devem
ser renomeados como se tivessem sido obtidos com os cenários publicados.
