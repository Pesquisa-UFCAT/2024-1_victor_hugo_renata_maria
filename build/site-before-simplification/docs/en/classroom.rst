.. _`sec:roteiro`:

Suggested classroom use
=======================

The material was designed for laboratory, data-analysis, or computational-methods courses in the final years of undergraduate physics and engineering programs, and it may also be used in early graduate study. Students are assumed to know basic probability (cumulative distribution function, density, mean, and variance), single-variable calculus (derivative, integral, and chain rule), and enough Python to run and modify the cells of a notebook. A possible sequence takes two classes of about 100 minutes. In the first, Sections :ref:`2 <sec:gld>` and :ref:`3 <sec:dados>` are covered with Figure :ref:`1 <fig:parametros>` and Code :ref:`1 <lst:quantil>`. In the second, the wind study or the temperature study is redone in the notebook, and the other is left as homework. The duration is an estimate by the authors and has not yet been verified in a classroom.

Table :ref:`9 <tab:roteiro>` links each objective of Section :ref:`1 <sec:introducao>` to an activity and to what the student is expected to produce. In all tasks, it is recommended to ask first for a written prediction and only then for the execution of the code, so that the discussion starts from the difference between what was predicted and what was obtained.

.. _tab:roteiro:

.. container::

   .. table:: Table 9. Objectives, activities, and expected evidence in the proposed sequence.

      +-------------------------------------------------+---------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
      | **Objective**                                   | **Activity**                                                                          | **Expected evidence**                                                   |
      +=================================================+=======================================================================================+=========================================================================+
      | Interpret the quantile function                 | Predict the effect of doubling :math:`\lambda_2` and check it in the notebook         | Explanation that the dispersion is halved and the shape does not change |
      +-------------------------------------------------+---------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
      | Understand the fit by moments                   | Compare the moments and the support of the GLD fitted to the wind data                | Recognition that equal moments do not guarantee an adequate support     |
      +-------------------------------------------------+---------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
      | Critically evaluate a fit                       | Compare the :math:`\Delta_p` of the normal with the variability of the July quantiles | Written justification for keeping, or not, the normal                   |
      +-------------------------------------------------+---------------------------------------------------------------------------------------+-------------------------------------------------------------------------+
      | Recognize the limits of physical interpretation | Discuss wind power from daily means                                                   | Argument that daily means do not determine :math:`\langle v^3\rangle`   |
      +-------------------------------------------------+---------------------------------------------------------------------------------------+-------------------------------------------------------------------------+

The four tasks below correspond to the rows of the table, with the expected answers.

#. **Doubling :math:`\lambda_2`.** By Eq. :ref:`(4) <eq:fkml>`, :math:`Q(u) - \lambda_1` is proportional to :math:`1/\lambda_2`. Doubling :math:`\lambda_2` halves the distance of each quantile to :math:`\lambda_1`, and therefore the standard deviation and the interquartile range, without changing the skewness or the kurtosis. Panel (b) of Figure :ref:`1 <fig:parametros>` allows this to be checked.

#. **Moments and support.** The moments are integrals over the whole distribution and may coincide with those of the sample even if the lower limit :math:`a = \lambda_1 - 1/(\lambda_2\lambda_3)` lies above the smallest observed value. The student is expected to compute :math:`a = 1.148\,\text{m/s}`, count the 84 days below it, and explain why the likelihood vanishes.

#. **Keep the normal in July?** The deviations of the normal (:math:`+0.16`, :math:`-0.09`, and :math:`+0.12\,^\circ`\ C) are smaller than the standard deviations obtained by resampling years (:math:`0.38`, :math:`0.10`, and :math:`0.21\,^\circ`\ C). An adequate answer keeps the normal to describe typical temperatures and recognizes that, if the interest is the cold tail, the skewness captured by the GLD may matter.

#. **Daily means and wind power.** The power density depends on :math:`\langle v^3\rangle` computed from speeds over short intervals. Since :math:`v^3` is convex, the mean of :math:`v^3` over a day is greater than or equal to the cube of the daily mean, so using daily means underestimates the power. The expected answer is that hourly or ten-minute data would be needed.
