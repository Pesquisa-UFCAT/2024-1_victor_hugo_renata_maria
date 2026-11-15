Distribuições flexíveis
========================

Uma breve introdução à distribuição lambda generalizada e materiais para explorar
dados de vento e temperatura com Python e ``pyGLAM``.

:doc:`Baixar dados e notebooks <downloads>`

A FKML em poucas palavras
----------------------------

A distribuição lambda generalizada, na parametrização FKML, permite representar
formas simétricas ou assimétricas, com caudas limitadas ou não. Ela é definida pela
função quantil: para uma probabilidade :math:`u`, :math:`Q(u)` fornece o valor abaixo
do qual está essa fração da distribuição. Por exemplo, :math:`Q(0{,}5)` é a mediana.

.. math::

   Q(u)=\lambda_1+\frac{1}{\lambda_2}
   \left[\frac{u^{\lambda_3}-1}{\lambda_3}
   -\frac{(1-u)^{\lambda_4}-1}{\lambda_4}\right],
   \qquad 0<u<1,\quad\lambda_2>0.

* :math:`\lambda_1` desloca a distribuição.
* :math:`\lambda_2` controla a escala inversamente: aumentá-lo reduz a dispersão.
* :math:`\lambda_3` e :math:`\lambda_4` controlam a forma, principalmente nos lados
  esquerdo e direito, respectivamente.

Quando um parâmetro de forma é zero, a fração correspondente é substituída pelo
limite logarítmico. O ajuste pode ser feito pelo método dos momentos, como nos
notebooks. Além da concordância com os dados, é necessário verificar se o suporte
do modelo é adequado à grandeza física e às observações.

Artigo
--------

O artigo será disponibilizado aqui após a publicação.

.. TODO: adicionar a referência e o link do artigo somente após a publicação.

.. toctree::
   :hidden:

   downloads
