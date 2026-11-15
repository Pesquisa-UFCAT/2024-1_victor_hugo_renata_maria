.. _`sec:introducao`:

Introduction
============

Distributions in physics and engineering education
--------------------------------------------------

The mathematical description of the variability of measurements and observable quantities is part of the teaching and practice of physics and engineering. Stochastic factors and uncertainties are present at every scale of empirical observation. Introductory statistics, as taught in undergraduate courses, often concentrates on measures of central tendency, such as the mean. However, the mean alone is insufficient to capture dispersion, skewness, the quantiles that matter for design, or the frequency of extreme values.

Real physical quantities show varied behaviors. When analyzing wind speed in flow studies, temperature variations in thermodynamics, the failure time of mechanical components, or the carbonation depth in concrete structures, one observes that the variability is not uniform. For these quantities, the observed dispersion may reflect the intrinsic fluctuation of the phenomenon, the instrumental error of the measuring equipment, or the epistemic uncertainty about the parameters of a model. A single distribution fitted to experimental data often reflects the superposition of these sources of variability.

In the data-analysis texts used in physics teaching, the normal distribution occupies a central position, both in the theory of errors :ref:`[1] <ref-taylor1997>` and in the evaluation of measurement uncertainty :ref:`[2] <ref-gum2008>`. Physical phenomena, however, are not restricted to Gaussian behavior. The statistical literature offers a variety of probability distributions, each with its own characteristics, but choosing the appropriate distribution to model real data is a challenge that requires knowledge of the phenomenon, of mathematics, and of statistics.

Historical path from particular distributions to flexible families
------------------------------------------------------------------

The effort to represent non-normal data has led, over more than a century, to different families of distributions. Pearson :ref:`[3] <ref-elderton1969>` proposed continuous curves defined as solutions of a differential equation, paving the way for the systematic modeling of skewness, and Johnson :ref:`[4] <ref-johnson1949>` built systems of distributions by nonlinear transformations of the standard normal variable. Another path was opened by the lambda family :ref:`[5] <ref-hastings1947>`, popularized by Tukey :ref:`[6] <ref-tukey1960>` and defined by the quantile function, the inverse of the cumulative distribution function :ref:`[7] <ref-gilchrist2000>`, which facilitates the computational treatment of data and tails.

Ramberg and Schmeiser :ref:`[8] <ref-ramberg1974>` generalized the lambda family to generate skewed variables in Monte Carlo simulations, and Ramberg and coworkers :ref:`[9] <ref-ramberg1979>` proposed fitting it by the method of moments. This refinement culminated in the formulation of Freimer, Kollia, Mudholkar, and Lin :ref:`[10] <ref-freimer1988>`, adopted in this paper and known as GLD-FKML (generalized lambda distribution, FKML parameterization). A comprehensive treatment is given by Karian and Dudewicz :ref:`[11] <ref-karian2011>`. The GLD represents different shapes, skewness values, and tail weights with a single quantile-function expression.

Why use flexible distributions?
-------------------------------

The advantage of flexible distributions such as the GLD lies in their ability to represent a wide variety of behaviors under a common computational procedure, which reduces the need to test many distinct families to find an adequate fit.

This representational power, however, has a cost. Four-parameter models such as the GLD-FKML require more delicate estimation, are prone to instabilities in small samples, and require careful checking so that the mathematical support of the distribution does not violate the physical support of the quantity (for example, by assigning probability to negative values of strictly positive variables).

Throughout the examples in this paper, three questions guide the evaluation of the distributions: closeness to the data (how well the model fits the observations), simplicity of the model (the principle of parsimony), and physical plausibility (whether the tails and limits of the model make sense for the phenomenon). None of them is settled by counting parameters alone, nor by simply inspecting a histogram :ref:`[12] <ref-nist2012>`.

Contemporary applications and computational tools
-------------------------------------------------

While the use of the GLD was once limited by the cost of parameter estimation, these distributions now find applications in engineering and computational science, such as the representation of the outputs of stochastic simulators and uncertainty quantification. Zhu and Sudret :ref:`[13] <ref-zhu2021>`, for example, use GLD-based models as surrogates of stochastic simulators, and the MF-GLaM model :ref:`[14] <ref-giannoukou2026>` extends this idea to the combination of simulations of different fidelity levels.

To bring these concepts into the classroom, accessible computational tools are now available. Table :ref:`1 <tab:ferramentas>` summarizes the main tools for working with the GLD.

.. _tab:ferramentas:

.. container::

   .. table:: Table 1. Computational tools for fitting and analyzing flexible distributions.

      +-----------------+-----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | **Environment** | **Tool**                                                              | **Role and applicability**                                                                                                                                                                |
      +=================+=======================================================================+===========================================================================================================================================================================================+
      | Python          | ``pyglam`` :ref:`[15] <ref-pyglam>`                                   | Library that implements the GLD-FKML, used to run the examples in this paper.                                                                                                             |
      +-----------------+-----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | Python          | ``scipy.stats`` :ref:`[16] <ref-scipy2020>`                           | Contains classical distributions and statistical functions. The ``tukeylambda`` distribution covers only the original symmetric family and does not replace the full four-parameter FKML. |
      +-----------------+-----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | R               | ``gld`` :ref:`[17] <ref-KingGld>`, ``GLDEX`` :ref:`[18] <ref-su2007>` | Packages that implement several parameterizations of the generalized lambda family and several fitting methods, including maximum likelihood.                                             |
      +-----------------+-----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | MATLAB          | ``fitdist`` :ref:`[19] <ref-matlabfitdist>`                           | The software’s distribution-fitting tool. The GLD-FKML is not among the available distributions, and its use requires custom routines.                                                    |
      +-----------------+-----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Objective, pedagogical contribution, and organization
-----------------------------------------------------

The objective of this paper is to present a pedagogical route for teaching flexible probability distributions, structured around the analysis of real physical data.

The contribution of this work is to offer students and instructors a path that goes beyond the application of formulas. By the end of the proposed path, the reader should be able to interpret the mathematics of a quantile function, understand the mechanisms and sensitivities of the fit by moments, critically evaluate fitted distributions by comparing the discrepancies with the measurement resolution and with the sampling uncertainty, and recognize the limits of the physical interpretation of the tails of these distributions. The audience, the prerequisites, and the tasks with which students can demonstrate these abilities are given in Section :ref:`6 <sec:roteiro>`.

The paper is organized as follows. Section :ref:`2 <sec:gld>` presents the quantile function, the FKML parameterization, and the fit by the method of moments. Section :ref:`3 <sec:dados>` discusses what it means to model a physical quantity by a distribution and establishes the protocol common to the case studies, which are developed for wind speed in Section :ref:`4 <sec:vento>` and for temperature in Section :ref:`5 <sec:temperatura>`. Section :ref:`6 <sec:roteiro>` proposes a classroom sequence, and Section :ref:`7 <sec:consideracoes>` gathers the concluding remarks and indicates the computational materials that accompany the paper.
