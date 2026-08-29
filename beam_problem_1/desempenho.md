# Otimização computacional do emulador de profundidade de carbonatação: vetorização e paralelização

## 1. Contexto

A função `emulator_function_time_durability` (módulo `functions_final.py`) constrói, para cada
ponto de projeto (realização de `f_ck`, `RH` e cobrimento), uma amostra de `n_latent_samples`
cenários de incerteza latente, avalia um modelo substituto de profundidade de carbonatação
(rede neural MLP, scikit-learn) e ajusta uma distribuição GLAM-FKML aos valores da função de
estado limite resultante. O conjunto de saídas alimenta o treinamento do metamodelo PCE usado na
análise de confiabilidade dependente do tempo do elemento estrutural.

Na implementação original, o modelo substituto era avaliado uma vez por amostra latente (laço
Python duplo: pontos de projeto × amostras latentes), o que se tornou o fator limitante de
desempenho à medida que o número de amostras de projeto (500–1000) e de amostras latentes
(~5000) aumentou. Este relatório documenta o ganho de desempenho obtido em duas etapas de
otimização: (i) vetorização com avaliação em lote do modelo substituto e (ii) paralelização do
laço externo (pontos de projeto) entre múltiplos processos.

## 2. Ambiente computacional

| Item | Especificação |
|---|---|
| CPU | AMD Ryzen 5 3600 (6 núcleos físicos / 12 threads lógicas) |
| Memória RAM | 34 GB |
| Sistema operacional | Windows 10 Pro (64 bits) |
| Python | 3.11.0 |
| Bibliotecas | numpy 1.26.4, pandas 3.0.3, scikit-learn 1.4.2, scipy 1.17.1 |
| Modelo substituto | `MLPRegressor` (camadas ocultas 100-50) dentro de um `Pipeline` com `StandardScaler` |

## 3. Configuração do benchmark

Configuração fixa em todas as medições: `n_latent_samples = 5000`, `time_step = 10` anos,
`installation_year = 1990`, `cement_type = 3`, `exposure_conditions = 2`, com `x` amostrado de
`Normal(30, 5)`, `Normal(70, 5)` e `Normal(30, 3)` para `f_ck`, `RH` e cobrimento,
respectivamente (`numpy.random.seed(0)`).

Três implementações foram comparadas:

1. **Original** — laço Python duplo; o modelo substituto é chamado uma vez por amostra latente
   (lotes de 16 linhas).
2. **Vetorizada** — variáveis latentes vetorizadas com numpy; o modelo substituto é chamado uma
   única vez por ponto de projeto, em um lote único de `n_latent_samples × n_grid` linhas.
3. **Vetorizada + paralela** — idêntica à anterior, mas o laço externo (pontos de projeto) é
   distribuído entre processos com `multiprocessing.Pool` (12 processos, 1 thread de BLAS por
   processo).

Como a implementação original demandaria ≈2h por execução completa (`n_samples = 1000`), seu
tempo na escala plena foi obtido por extrapolação linear a partir de três medições controladas
em escala reduzida (20.000–40.000 avaliações combinadas projeto × latente). A taxa observada foi
de 156,6 ± 0,8 s por 10⁵ avaliações (três medições: 156,07; 156,39; 157,48 s/10⁵), consistente
com escalonamento linear no produto `n_samples × n_latent_samples`. As versões vetorizada e
vetorizada+paralela foram medidas diretamente na escala plena (`n_samples = 1000`).

## 4. Resultados

| Versão | Estratégia | Tempo — 1000×5000 avaliações | Speedup vs. original | Speedup incremental |
|---|---|---|---|---|
| Original | `predict()` chamado 1×/amostra latente (lotes de 16 linhas) | ≈ 130,5 min (extrapolado)¹ | 1× (referência) | — |
| Vetorizada | `predict()` em lote único por ponto de projeto | 21,8 s (média de 4 execuções; 20,5–23,2 s) | ≈ 360× | ≈ 360× |
| Vetorizada + paralela | + `multiprocessing` no laço de pontos de projeto | 19,5 s (média de 3 execuções; 19,3–19,7 s) | ≈ 402× | ≈ 1,12× |

¹ Extrapolação linear a partir de medições em escala reduzida (ver Seção 3).

A correção numérica de cada etapa foi verificada comparando, com a mesma semente aleatória,
a saída completa (profundidade de carbonatação, valores de `g` e parâmetros λ da GLAM) entre a
versão original e a vetorizada, obtendo diferenças de ordem 10⁻⁹–10⁻¹⁵ (ruído numérico do
solver de mínimos quadrados). A versão paralela, por usar geradores aleatórios independentes em
cada processo, foi validada por equivalência estatística (médias e desvios-padrão das mesmas
grandezas, em vez de igualdade ponto a ponto).

## 5. Discussão

A vetorização foi responsável por praticamente todo o ganho de desempenho. Antes dela, o tempo
de execução era dominado pelo número de chamadas ao modelo substituto (até 5×10⁶ chamadas para
lotes de apenas 16 linhas cada), cujo custo fixo por chamada (validação de entrada do
scikit-learn, criação de objetos) dominava sobre o cálculo em si. Ao consolidar todas as
amostras latentes de um mesmo ponto de projeto em uma única chamada, esse número caiu para 1000
chamadas, e o custo computacional passou a ser limitado pela multiplicação de matrizes da rede
neural — já eficiente o suficiente para não se beneficiar de mais lotes maiores.

A paralelização adicional trouxe um ganho bem mais modesto do que o esperado a priori (~4–8×,
estimado por perfilamento prévio do código sequencial). Os fatores identificados foram: (i) a
biblioteca BLAS já utiliza múltiplas threads internamente por processo, e a execução simultânea
de 12 processos com essa configuração padrão causou saturação dos núcleos (observada como falhas
espúrias de alocação de memória), exigindo limitar cada processo a 1 thread de BLAS; (ii) cada
processo worker precisa reimportar todo o conjunto de bibliotecas científicas usadas pelo módulo
(~4,7 s medidos), custo fixo pago a cada chamada da função; (iii) o gargalo remanescente após a
vetorização já é limitado por computação (multiplicação de matrizes), não por overhead de
chamada, reduzindo a margem de ganho disponível para distribuição entre processos nessa escala
de problema.

## 6. Conclusão

A reestruturação do emulador de profundidade de carbonatação — substituindo o laço de amostras
latentes por operações vetorizadas e uma única chamada em lote ao modelo substituto por ponto de
projeto — reduziu o tempo de geração do conjunto de treinamento do metamodelo PCE em um passo de
tempo de aproximadamente 2h10min para menos de 22 segundos (≈360×), sem alteração dos resultados
numéricos. A paralelização do laço de pontos de projeto entre processos contribuiu com um ganho
incremental de ≈12% (≈402× em relação à versão original), inferior ao esperado devido a custos
fixos de inicialização de processos e de importação de bibliotecas, que passam a dominar uma vez
que o principal gargalo computacional já foi eliminado pela vetorização.
