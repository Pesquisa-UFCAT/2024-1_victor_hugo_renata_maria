.. _`sec:introducao`:

Introdução
==========

Distribuições no ensino de física e engenharia
----------------------------------------------

A descrição matemática da variabilidade de medições e grandezas observáveis faz parte do ensino e da prática da física e da engenharia. Fatores estocásticos e incertezas estão presentes em todas as escalas da observação empírica. Frequentemente, a estatística introdutória ensinada nos cursos de graduação concentra-se em medidas de tendência central, como a média. Contudo, a média isolada é insuficiente para capturar a dispersão, a assimetria, os quantis de interesse para projetos ou a frequência de ocorrência de valores extremos.

Grandezas físicas reais apresentam comportamentos variados. Ao analisar a velocidade do vento em estudos de escoamento, as variações de temperatura em termodinâmica, o tempo de falha de componentes mecânicos ou a profundidade de carbonatação em estruturas de concreto, observa-se que a variabilidade não é uniforme. Nessas grandezas, a dispersão observada pode refletir a flutuação intrínseca do fenômeno, o erro instrumental associado aos equipamentos de medição ou a incerteza epistêmica sobre os parâmetros de um modelo. Muitas vezes, uma única distribuição ajustada a dados experimentais reflete a superposição dessas fontes de variabilidade.

Nos textos de tratamento de dados usados no ensino de física, a distribuição normal ocupa posição central, tanto na teoria de erros :ref:`[1] <ref-taylor1997>` quanto na avaliação de incertezas de medição :ref:`[2] <ref-gum2008>`. Porém os fenômenos físicos não se limitam a comportamentos gaussianos. A literatura estatística oferece uma variedade de distribuições de probabilidade, cada uma com características próprias, mas a escolha da distribuição adequada para modelar dados reais é um desafio que exige conhecimento do fenômeno, da matemática e da estatística.

Percurso histórico das distribuições particulares às famílias flexíveis
-----------------------------------------------------------------------

O esforço para representar dados não normais levou, ao longo de mais de um século, a diferentes famílias de distribuições. Pearson :ref:`[3] <ref-elderton1969>` propôs curvas contínuas definidas como soluções de uma equação diferencial, abrindo caminho para a modelagem sistemática da assimetria, e Johnson :ref:`[4] <ref-johnson1949>` construiu sistemas de distribuições por transformações não lineares da variável normal padrão. Outro caminho foi aberto pela família lambda :ref:`[5] <ref-hastings1947>`, difundida por Tukey :ref:`[6] <ref-tukey1960>` e definida pela função quantil, a inversa da função distribuição acumulada :ref:`[7] <ref-gilchrist2000>`, o que facilita o tratamento computacional dos dados e das caudas.

Ramberg e Schmeiser :ref:`[8] <ref-ramberg1974>` generalizaram a família lambda para gerar variáveis assimétricas em simulações de Monte Carlo, e Ramberg e colaboradores :ref:`[9] <ref-ramberg1979>` propuseram seu ajuste pelo método dos momentos. Esse refinamento culminou na formulação de Freimer, Kollia, Mudholkar e Lin :ref:`[10] <ref-freimer1988>`, adotada neste artigo e conhecida como GLD-FKML (Generalized Lambda Distribution, parametrização FKML). Uma exposição abrangente está em Karian e Dudewicz :ref:`[11] <ref-karian2011>`. A GLD representa diferentes formas, assimetrias e pesos de cauda com uma mesma expressão de função quantil.

Por que utilizar distribuições flexíveis?
-----------------------------------------

A vantagem de adotar distribuições flexíveis como a GLD está na capacidade de representar uma grande variedade de comportamentos sob um procedimento computacional comum, o que reduz a necessidade de testar muitas famílias distintas para encontrar um ajuste adequado.

Esse poder representativo, entretanto, tem um custo. Modelos com quatro parâmetros, como a GLD-FKML, exigem uma estimação mais delicada, são suscetíveis a instabilidades em amostras pequenas e exigem verificação cuidadosa para que o suporte matemático da distribuição não viole o suporte físico da grandeza (por exemplo, atribuindo probabilidade a valores negativos de variáveis estritamente positivas).

Ao longo dos exemplos deste artigo, três questões guiarão a avaliação das distribuições: a proximidade dos dados (quão bem o modelo se ajusta às observações), a simplicidade do modelo (o princípio da parcimônia) e a plausibilidade física (se as caudas e os limites do modelo fazem sentido para o fenômeno). Nenhuma delas é resolvida apenas pela contagem de parâmetros, tampouco pela simples inspeção visual de um histograma :ref:`[12] <ref-nist2012>`.

Aplicações contemporâneas e ferramentas computacionais
------------------------------------------------------

Se no passado o uso da GLD era limitado pelo custo da estimação de parâmetros, hoje essas distribuições encontram aplicações na engenharia e nas ciências computacionais, como a representação das saídas de simuladores estocásticos e a quantificação de incertezas. Zhu e Sudret :ref:`[13] <ref-zhu2021>`, por exemplo, empregam modelos baseados na GLD como metamodelos de simuladores estocásticos, e o modelo MF-GLaM :ref:`[14] <ref-giannoukou2026>` estende essa ideia à combinação de simulações com diferentes níveis de fidelidade.

Para levar esses conceitos à sala de aula, há hoje ferramentas computacionais acessíveis. A Tabela :ref:`1 <tab:ferramentas>` resume as principais ferramentas disponíveis para o trabalho com a GLD.

.. _tab:ferramentas:

.. container::

   .. table:: Tabela 1. Ferramentas computacionais para ajuste e análise de distribuições flexíveis.

      +--------------+-----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | **Ambiente** | **Ferramenta**                                                        | **Papel e aplicabilidade**                                                                                                                                                                |
      +==============+=======================================================================+===========================================================================================================================================================================================+
      | Python       | ``pyglam`` :ref:`[15] <ref-pyglam>`                                   | Biblioteca que implementa a GLD-FKML, utilizada na execução dos exemplos deste artigo.                                                                                                    |
      +--------------+-----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | Python       | ``scipy.stats`` :ref:`[16] <ref-scipy2020>`                           | Contém distribuições e funções estatísticas clássicas. A distribuição ``tukeylambda`` abrange apenas a família original simétrica, não substituindo a FKML completa de quatro parâmetros. |
      +--------------+-----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | R            | ``gld`` :ref:`[17] <ref-KingGld>`, ``GLDEX`` :ref:`[18] <ref-su2007>` | Pacotes que implementam diversas parametrizações da família lambda generalizada e vários métodos de ajuste, incluindo máxima verossimilhança.                                             |
      +--------------+-----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | MATLAB       | ``fitdist`` :ref:`[19] <ref-matlabfitdist>`                           | Ferramenta de ajuste de distribuições do software. A GLD-FKML não consta entre as distribuições disponíveis, e seu uso requer rotinas próprias.                                           |
      +--------------+-----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Objetivo, contribuição didática e organização
---------------------------------------------

O objetivo deste artigo é apresentar uma via didática para o ensino de distribuições de probabilidade flexíveis, estruturada sobre a análise de dados físicos reais.

A contribuição do trabalho é oferecer a estudantes e professores um percurso que vai além da aplicação de fórmulas. Ao final do percurso proposto, o leitor deverá ser capaz de interpretar a matemática de uma função quantil, compreender os mecanismos e as sensibilidades do ajuste por momentos, avaliar criticamente as distribuições ajustadas, comparando as discrepâncias com a resolução das medições e com a incerteza amostral, e reconhecer os limites da interpretação física das caudas dessas distribuições. O público, os pré-requisitos e as tarefas com que o estudante pode demonstrar essas capacidades estão na seção :ref:`6 <sec:roteiro>`.

O artigo está organizado da seguinte forma. A seção :ref:`2 <sec:gld>` apresenta a função quantil, a parametrização FKML e o ajuste pelo método dos momentos. A seção :ref:`3 <sec:dados>` discute o que significa modelar uma grandeza física por uma distribuição e estabelece o protocolo comum aos estudos de caso, desenvolvidos para a velocidade do vento na seção :ref:`4 <sec:vento>` e para a temperatura na seção :ref:`5 <sec:temperatura>`. A seção :ref:`6 <sec:roteiro>` propõe um roteiro de uso em sala, e a seção :ref:`7 <sec:consideracoes>` reúne as considerações finais e indica os materiais computacionais que acompanham o artigo.
