Flexible distributions
======================

Study and reproduction materials for the paper on the generalized lambda distribution, with wind and temperature examples.

:doc:`Download data and notebooks <downloads>`

Abstract
--------

The normal distribution holds a central place in many introductory data-analysis courses, although many physical quantities are skewed or bounded. This paper presents a pedagogical approach to the probabilistic modeling of real physical data with the generalized lambda distribution (GLD), in the FKML parameterization, which is defined by an explicit quantile function. It explains the meaning of the four parameters, the conditions of validity and support, and the fit by the method of moments, implemented in the Python library ``pyglam``. The procedure is applied to two data sets from an automatic weather station of the Brazilian National Institute of Meteorology (INMET) in Brasília, namely the daily mean wind speed, compared with the Rayleigh and Weibull distributions, and the daily mean temperature in July, compared with the normal distribution. The assessment uses the Kolmogorov-Smirnov distance and quantile deviations in the units of the measured quantity, interpreted in light of the measurement resolution and the sampling uncertainty. For wind, the flexible distribution gives the smallest deviations at the quantiles examined, of the same order as the variability estimated by resampling, but its support excludes 0.95% of the days, precisely the calmest ones. For temperature, the deviations of the normal distribution are smaller than the sampling variability of the quantiles, and the two-parameter model remains a reasonable choice for this description. The examples show that a good fit requires examining the support and the goodness of fit, not only the moments, and that the choice of model depends on the physical question. All results are reproduced by a notebook provided with the paper, and a suggested classroom sequence, with tasks and expected answers, accompanies the text.

Authors
--------

Renata Maria Pensin · Wanderlei Malaquias Pereira Junior · Victor Hugo Moreira do Couto Souza · Marcos Luiz Henrique

Full text and materials
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
