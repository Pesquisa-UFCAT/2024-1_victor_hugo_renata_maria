.. _`sec:roteiro`:

Sugestão de uso em sala
=======================

O material foi pensado para disciplinas de laboratório, de tratamento de dados ou de métodos computacionais dos anos finais da graduação em física e em engenharia, e pode ser usado também no início da pós-graduação. Supõe-se que o estudante conheça probabilidade básica (função distribuição acumulada, densidade, média e variância), cálculo de uma variável (derivada, integral e regra da cadeia) e o suficiente de Python para executar e modificar as células de um notebook. Uma sequência possível ocupa duas aulas de cerca de 100 minutos. Na primeira, trabalham-se as seções :ref:`2 <sec:gld>` e :ref:`3 <sec:dados>` com a Figura :ref:`1 <fig:parametros>` e o Código :ref:`1 <lst:quantil>`. Na segunda, o estudo do vento ou o da temperatura é refeito no notebook, e o outro fica como tarefa extraclasse. A duração é uma estimativa dos autores, ainda não verificada em turma.

A Tabela :ref:`9 <tab:roteiro>` liga cada objetivo da seção :ref:`1 <sec:introducao>` a uma atividade e ao que se espera que o estudante produza. Em todas as tarefas, recomenda-se pedir primeiro uma previsão por escrito e só depois a execução do código, para que a discussão parta da diferença entre o previsto e o obtido.

.. _tab:roteiro:

.. container::

   .. table:: Tabela 9. Objetivos, atividades e evidências esperadas na sequência proposta.

      +--------------------------------------------+------------------------------------------------------------------------------+---------------------------------------------------------------------------+
      | **Objetivo**                               | **Atividade**                                                                | **Evidência esperada**                                                    |
      +============================================+==============================================================================+===========================================================================+
      | Interpretar a função quantil               | Prever o efeito de dobrar :math:`\lambda_2` e conferir no notebook           | Explicação de que a dispersão cai à metade e a forma não muda             |
      +--------------------------------------------+------------------------------------------------------------------------------+---------------------------------------------------------------------------+
      | Compreender o ajuste por momentos          | Comparar os momentos e o suporte da GLD ajustada ao vento                    | Constatação de que momentos iguais não garantem suporte adequado          |
      +--------------------------------------------+------------------------------------------------------------------------------+---------------------------------------------------------------------------+
      | Avaliar criticamente um ajuste             | Comparar :math:`\Delta_p` da normal com a variabilidade dos quantis de julho | Justificativa escrita para manter, ou não, a normal                       |
      +--------------------------------------------+------------------------------------------------------------------------------+---------------------------------------------------------------------------+
      | Reconhecer limites da interpretação física | Discutir a potência eólica a partir de médias diárias                        | Argumento de que médias diárias não determinam :math:`\langle v^3\rangle` |
      +--------------------------------------------+------------------------------------------------------------------------------+---------------------------------------------------------------------------+

As quatro tarefas abaixo correspondem às linhas da tabela, com as respostas esperadas.

#. **Dobrar :math:`\lambda_2`.** Pela equação :ref:`(4) <eq:fkml>`, :math:`Q(u) - \lambda_1` é proporcional a :math:`1/\lambda_2`. Dobrar :math:`\lambda_2` divide por dois a distância de cada quantil a :math:`\lambda_1`, e portanto o desvio padrão e a distância interquartil, sem alterar a assimetria nem a curtose. O painel (b) da Figura :ref:`1 <fig:parametros>` permite conferir.

#. **Momentos e suporte.** Os momentos são integrais sobre toda a distribuição e podem coincidir com os da amostra mesmo que o limite inferior :math:`a = \lambda_1 - 1/(\lambda_2\lambda_3)` fique acima do menor valor observado. Espera-se que o estudante calcule :math:`a = 1,148\,\text{m/s}`, conte os 84 dias abaixo dele e explique por que a verossimilhança se anula.

#. **Manter a normal em julho?** Os desvios da normal (:math:`+0,16`, :math:`-0,09` e :math:`+0,12\,^\circ`\ C) são menores que os desvios padrão por reamostragem de anos (:math:`0,38`, :math:`0,10` e :math:`0,21\,^\circ`\ C). Uma resposta adequada mantém a normal para descrever as temperaturas típicas e reconhece que, se o interesse for a cauda fria, a assimetria capturada pela GLD pode importar.

#. **Médias diárias e potência eólica.** A densidade de potência depende de :math:`\langle v^3\rangle` calculado com velocidades em intervalos curtos. Como :math:`v^3` é convexa, a média de :math:`v^3` ao longo de um dia é maior ou igual ao cubo da média diária, de modo que usar médias diárias subestima a potência. A resposta esperada é que seriam necessários dados horários ou de dez minutos.
