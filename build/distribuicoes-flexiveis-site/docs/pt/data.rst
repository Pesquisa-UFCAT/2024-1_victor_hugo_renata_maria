.. _`sec:dados`:

Dados de grandezas físicas reais e modelagem por distribuições
==============================================================

O que significa dizer que uma grandeza segue uma distribuição?
--------------------------------------------------------------

Na física e na engenharia, afirmar que uma grandeza segue uma determinada distribuição de probabilidade significa estabelecer um modelo matemático descritivo para um conjunto de observações empíricas obtidas sob condições especificadas. A distribuição não é uma propriedade do fenômeno em si, pois depende de como a variável de interesse é definida e medida. Por exemplo, modelar a velocidade instantânea do vento em uma rajada exige um tratamento estatístico diferente daquele aplicado à velocidade média diária. Da mesma forma, as precipitações diárias em uma bacia hidrográfica apresentam um comportamento distinto dos máximos anuais de precipitação utilizados em projetos de barragens.

A forma observada da distribuição (como seu grau de assimetria ou espessura das caudas) depende fortemente das condições físicas do fenômeno, da resolução do procedimento de medição e da escala de agregação temporal ou espacial. A semelhança visual entre um histograma e a curva de um modelo teórico não prova que exista um mecanismo físico por trás dos dados. Um histograma bimodal de temperaturas coletadas ao longo de um ano, por exemplo, não revela uma nova lei termodinâmica, mas frequentemente resulta da combinação de duas populações sazonais distintas (verão e inverno) com médias diferentes. A estatística descreve o padrão, mas a justificativa do modelo exige compreensão física.

Exemplos de relações entre grandezas e famílias de distribuições
----------------------------------------------------------------

Diferentes mecanismos físicos e teoremas probabilísticos dão origem a famílias clássicas de distribuições, cada qual com suas hipóteses fundamentais e limites de validade. A Tabela :ref:`3 <tab:modelos_fisicos>` resume as motivações teóricas para a adoção de alguns modelos de referência habituais.

.. _tab:modelos_fisicos:

.. container::

   .. table:: Tabela 3. Relação entre fenômenos físicos, modelos estatísticos e suas premissas.

      +--------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | **Grandeza ou situação**                         | **Modelo**                | **Hipóteses ou limites físicos a explicar**                                                                                                                  |
      +==================================================+===========================+==============================================================================================================================================================+
      | Soma de múltiplas contribuições independentes    | Normal (gaussiana)        | O teorema central do limite exige condições (variância finita, independência). Não garante, por exemplo, que toda série temporal de temperatura seja normal. |
      +--------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | Módulo de duas componentes ortogonais gaussianas | Rayleigh                  | Assume componentes independentes, de média nula e mesma variância. Sua aplicação ao vento atmosférico real requer verificação.                               |
      +--------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | Máximos por blocos (cheias anuais, rajadas)      | Gumbel (valores extremos) | A família limite depende da forma da distribuição de origem. Nem todo valor máximo converge para um modelo de Gumbel.                                        |
      +--------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | Resistência de materiais ou tempo até a falha    | Weibull                   | A adequação depende da microestrutura do material, do modo de propagação da falha e das condições do ensaio.                                                 |
      +--------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+

A distribuição de Rayleigh ilustra como uma hipótese física sobre as componentes da velocidade gera um modelo estatístico. Considere-se a velocidade horizontal do vento, com componentes ortogonais :math:`V_x` e :math:`V_y`, e assuma-se que ambas são variáveis aleatórias independentes e normalmente distribuídas, com médias nulas e variâncias idênticas :math:`\sigma^2`. A densidade conjunta é o produto das densidades marginais,

.. math::

   f_{V_x,V_y}(v_x, v_y) = \frac{1}{2\pi\sigma^2} \exp\left( -\frac{v_x^2 + v_y^2}{2\sigma^2} \right).

A grandeza física de interesse usualmente é o módulo da velocidade, :math:`v = \sqrt{v_x^2 + v_y^2}`. Transformando para coordenadas polares, em que o elemento de área :math:`dv_x\,dv_y` se torna :math:`v\,dv\,d\theta`, e integrando o ângulo :math:`\theta` de :math:`0` a :math:`2\pi`, obtém-se a densidade da distribuição de Rayleigh,

.. _eq:rayleigh:

.. math::

   f_V(v) = \frac{v}{\sigma^2} \exp\left( -\frac{v^2}{2\sigma^2} \right), \qquad v \geq 0.
   \tag{12}

Nesta formulação, o parâmetro de escala :math:`\sigma` tem interpretação direta, pois, como :math:`E[V^2] = E[V_x^2] + E[V_y^2] = 2\sigma^2`, a quantidade :math:`\sigma^2` é a energia cinética média por unidade de massa associada ao movimento horizontal. Na atmosfera real, porém, há efeitos de rugosidade do terreno e gradientes térmicos, de modo que as hipóteses da dedução não devem ser tomadas como válidas para o vento atmosférico sem a devida verificação empírica. Além disso, a dedução refere-se à velocidade em um instante ou em intervalos curtos. Médias sobre intervalos longos, como a média diária, têm dispersão relativa menor, por efeito da própria agregação. Na prática da energia eólica, a distribuição de Weibull, que contém a de Rayleigh como caso particular, é a referência usual para velocidades horárias ou de dez minutos :ref:`[20] <ref-justus1978>`, :ref:`[21] <ref-carta2009>`.

O mesmo raciocínio, aplicado às três componentes cartesianas da velocidade de uma molécula de um gás ideal, leva à distribuição de Maxwell-Boltzmann, familiar aos estudantes da termodinâmica e da teoria cinética. O exemplo mostra como uma distribuição de probabilidade pode decorrer de hipóteses físicas explícitas, e não apenas de um ajuste empírico.

Por que isso importa na confiabilidade de materiais?
----------------------------------------------------

A forma da distribuição importa também fora do ajuste de curvas, porque está na base da teoria de confiabilidade estrutural e de materiais. Suponha-se que uma estrutura, como uma viga de concreto armado, possua uma resistência mecânica de comportamento aleatório, modelada pela variável :math:`R`. Se esta estrutura é submetida a uma solicitação (carga) fixa conhecida :math:`s`, a falha ocorrerá sempre que a resistência for inferior à solicitação.

Neste cenário simplificado, a probabilidade de falha :math:`P_f` é exatamente o valor da função distribuição acumulada (FDA) de :math:`R` avaliada no ponto :math:`s`,

.. math::

   P_f = P(R < s) = F_R(s).

Esse simples balanço mostra por que conhecer apenas a resistência média de um material é insuficiente para a engenharia. A segurança da estrutura é governada pelo comportamento da *cauda inferior* da distribuição (os valores mais baixos e raros de resistência), e um modelo cuja cauda inferior não corresponda à dos dados pode subestimar a probabilidade de falha. Em projetos reais, tanto :math:`R` quanto :math:`s` são grandezas aleatórias, exigindo a avaliação da interferência probabilística entre ambas e evidenciando a necessidade de escolhas de distribuições que reflitam a física da falha, conforme discutido em diretrizes de referência sobre dados de falha :ref:`[12] <ref-nist2012>`.

.. _`subsec:protocolo`:

Protocolo comum aos estudos de caso
-----------------------------------

Para que as análises possam ser reproduzidas e comparadas, os estudos de caso desenvolvidos nas seções :ref:`4 <sec:vento>` e :ref:`5 <sec:temperatura>` seguem um protocolo dividido nas sete etapas sequenciais descritas a seguir.

#. **Documentação dos dados e contextualização física:** identificação da fonte primária (instituição, estação de monitoramento, coordenadas e altitude), período de observação, grandeza física medida, resolução temporal das leituras (por exemplo, médias diárias ou valores instantâneos) e instrumental associado.

#. **Exame de qualidade e consistência física:** levantamento de dados ausentes, identificação de eventuais leituras espúrias e avaliação de restrições de suporte (por exemplo, a não negatividade da velocidade do vento ou os limites da umidade relativa). Os critérios de descarte ou tratamento de falhas são explicitados e fundamentados.

#. **Definição do recorte amostral:** estabelecimento prévio e justificado de janelas temporais ou espaciais homogêneas (como o recorte de um mês específico para atenuar a não estacionariedade sazonal), evitando seleções *a posteriori* direcionadas a favorecer um modelo pré-determinado. Quando não se estratifica, declara-se o alvo. No vento, por exemplo, o alvo é a distribuição histórica agregada de todo o período, que mistura as estações do ano.

#. **Descrição estatística exploratória:** caracterização da amostra por medidas de posição, dispersão, assimetria (:math:`\widehat\gamma_1`) e curtose (:math:`\widehat\beta_2`), acompanhadas de quantis empíricos de referência (:math:`Q_{0,05}`, :math:`Q_{0,50}`, :math:`Q_{0,95}`) e de gráficos da série temporal e do histograma.

#. **Estimação de parâmetros e ajuste das famílias:** ajuste dos modelos de referência, estimados por máxima verossimilhança com as restrições físicas de suporte (como a origem fixada em zero), e da GLD-FKML, estimada pelo método dos momentos com múltiplos pontos iniciais. A validade dos parâmetros e o suporte resultante são verificados.

#. **Diagnóstico de aderência e comparação quantílica:** avaliação comparativa por métricas nas unidades da grandeza. Utiliza-se a distância de Kolmogorov-Smirnov, :math:`D_n = \sup_x |F_n(x) - \widehat{F}(x)|`, para medir a maior discrepância acumulada, e os desvios quantílicos

   .. _eq:delta:

.. math::

   \Delta_p = Q_{\text{modelo}}(p) - Q_{\text{empírico}}(p), \quad p \in \{0,05;\, 0,50;\, 0,95\},
   \tag{14}

   cujo sinal indica subestimação (negativo) ou superestimação (positivo). Os ajustes são comparados visualmente em painéis com densidades sobrepostas, funções acumuladas e gráficos quantil-quantil (Q-Q).

#. **Interpretação nas unidades do fenômeno e limites de validade:** tradução física das discrepâncias para o contexto da aplicação, comparando-as com a resolução das medições e com a incerteza amostral dos próprios quantis empíricos, e discutindo o princípio da parcimônia frente ao custo de parâmetros adicionais.

A distância :math:`D_n` é usada aqui como medida descritiva. Os p-valores usuais do teste de Kolmogorov-Smirnov não se aplicam diretamente, porque os parâmetros são estimados com os mesmos dados :ref:`[22] <ref-lilliefors1967>`, as observações diárias são dependentes entre si e os valores registrados são arredondados. Para dar uma escala às discrepâncias, o notebook que acompanha o artigo estima a variabilidade amostral dos quantis empíricos por reamostragem *bootstrap* em blocos de dias consecutivos :ref:`[23] <ref-kunsch1989>`, que preserva a dependência entre dias próximos, sorteando apenas blocos sem falhas de registro, e quantifica por simulação o efeito do arredondamento sobre :math:`D_n`. Essas escalas servem para comparar ordens de grandeza. Nenhuma delas é usada como teste de hipótese.
