Distribuições flexíveis
=======================

Material de estudo e reprodução do artigo sobre a distribuição lambda generalizada, com exemplos de vento e temperatura.

:doc:`Baixar dados e notebooks <downloads>`

Resumo
--------

A distribuição normal ocupa posição central em muitos cursos introdutórios de tratamento de dados, embora muitas delas sejam assimétricas ou limitadas. Este artigo apresenta uma abordagem didática para a modelagem probabilística de dados físicos reais com a distribuição lambda generalizada, na parametrização FKML, definida por uma função quantil explícita. Explica-se o significado dos quatro parâmetros, as condições de validade e de suporte e o ajuste pelo método dos momentos, implementado na biblioteca Python ``pyglam``. O procedimento é aplicado a dois conjuntos de dados de uma estação meteorológica automática do INMET em Brasília, que são a velocidade média diária do vento, comparada às distribuições de Rayleigh e de Weibull, e a temperatura média diária de julho, comparada à distribuição normal. A avaliação usa a distância de Kolmogorov-Smirnov e os desvios de quantis nas unidades da grandeza, interpretados à luz da resolução das medições e da incerteza amostral. No vento, a distribuição flexível tem os menores desvios nos quantis examinados, da mesma ordem da variabilidade estimada por reamostragem, mas seu suporte exclui 0,95% dos dias, justamente os de vento mais fraco. Na temperatura, as discrepâncias da normal são menores que a variabilidade amostral dos quantis, e o modelo de dois parâmetros continua sendo uma escolha razoável para essa descrição. Os exemplos mostram que um bom ajuste exige examinar o suporte e a aderência, e não apenas os momentos, e que a escolha do modelo depende da pergunta física. Todos os resultados são reproduzidos por um notebook disponibilizado com o artigo, e uma sugestão de roteiro para uso em sala, com tarefas e respostas esperadas, acompanha o texto.

Autoria
--------

Renata Maria Pensin · Wanderlei Malaquias Pereira Junior · Victor Hugo Moreira do Couto Souza · Marcos Luiz Henrique

Texto completo e materiais
---------------------------

.. toctree::
   :maxdepth: 2

   introduction
   distribution
   data
   wind
   temperature
   classroom
   conclusions
   downloads
   data-notes
   references
