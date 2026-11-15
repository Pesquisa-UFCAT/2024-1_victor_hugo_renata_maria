.. _`sec:dados`:

Real physical data and modeling by distributions
================================================

What does it mean to say that a quantity follows a distribution?
----------------------------------------------------------------

In physics and engineering, stating that a quantity follows a given probability distribution means establishing a descriptive mathematical model for a set of empirical observations obtained under specified conditions. The distribution is not a property of the phenomenon itself, since it depends on how the variable of interest is defined and measured. For example, modeling the instantaneous wind speed in a gust requires a statistical treatment different from the one applied to the daily mean speed. Likewise, daily precipitation in a river basin behaves differently from the annual precipitation maxima used in dam design.

The observed shape of the distribution (such as its degree of skewness or the thickness of its tails) depends strongly on the physical conditions of the phenomenon, on the resolution of the measurement procedure, and on the scale of temporal or spatial aggregation. The visual similarity between a histogram and the curve of a theoretical model does not prove that a physical mechanism lies behind the data. A bimodal histogram of temperatures collected over a year, for example, does not reveal a new thermodynamic law, but frequently results from the combination of two distinct seasonal populations (summer and winter) with different means. Statistics describes the pattern, but justifying the model requires physical understanding.

Examples of relations between quantities and families of distributions
----------------------------------------------------------------------

Different physical mechanisms and probabilistic theorems give rise to classical families of distributions, each with its fundamental assumptions and limits of validity. Table :ref:`3 <tab:modelos_fisicos>` summarizes the theoretical motivations for adopting some usual reference models.

.. _tab:modelos_fisicos:

.. container::

   .. table:: Table 3. Relation between physical phenomena, statistical models, and their assumptions.

      +-------------------------------------------------+-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | **Quantity or situation**                       | **Model**               | **Assumptions or physical limits to be explained**                                                                                                               |
      +=================================================+=========================+==================================================================================================================================================================+
      | Sum of many independent contributions           | Normal (Gaussian)       | The central limit theorem requires conditions (finite variance, independence). It does not guarantee, for example, that every temperature time series is normal. |
      +-------------------------------------------------+-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | Magnitude of two orthogonal Gaussian components | Rayleigh                | Assumes independent components with zero mean and equal variance. Its application to real atmospheric wind requires verification.                                |
      +-------------------------------------------------+-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | Block maxima (annual floods, gusts)             | Gumbel (extreme values) | The limiting family depends on the shape of the parent distribution. Not every maximum converges to a Gumbel model.                                              |
      +-------------------------------------------------+-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | Material strength or time to failure            | Weibull                 | Suitability depends on the microstructure of the material, the mode of failure propagation, and the test conditions.                                             |
      +-------------------------------------------------+-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+

The Rayleigh distribution illustrates how a physical hypothesis about the velocity components generates a statistical model. Consider the horizontal wind velocity, with orthogonal components :math:`V_x` and :math:`V_y`, and assume that both are independent, normally distributed random variables with zero means and identical variances :math:`\sigma^2`. The joint density is the product of the marginal densities,

.. math::

   f_{V_x,V_y}(v_x, v_y) = \frac{1}{2\pi\sigma^2} \exp\left( -\frac{v_x^2 + v_y^2}{2\sigma^2} \right).

The physical quantity of interest is usually the speed, :math:`v = \sqrt{v_x^2 + v_y^2}`. Changing to polar coordinates, in which the area element :math:`dv_x\,dv_y` becomes :math:`v\,dv\,d\theta`, and integrating the angle :math:`\theta` from :math:`0` to :math:`2\pi`, one obtains the Rayleigh density,

.. _eq:rayleigh:

.. math::

   f_V(v) = \frac{v}{\sigma^2} \exp\left( -\frac{v^2}{2\sigma^2} \right), \qquad v \geq 0.
   \tag{12}

In this formulation, the scale parameter :math:`\sigma` has a direct interpretation, since, because :math:`E[V^2] = E[V_x^2] + E[V_y^2] = 2\sigma^2`, the quantity :math:`\sigma^2` is the mean kinetic energy per unit mass associated with the horizontal motion. In the real atmosphere, however, there are effects of terrain roughness and thermal gradients, so the assumptions of the derivation cannot be taken as valid for atmospheric wind without proper empirical verification. Moreover, the derivation refers to the velocity at an instant or over short intervals. Averages over long intervals, such as the daily mean, have a smaller relative dispersion, owing to the aggregation itself. In wind-energy practice, the Weibull distribution, which contains the Rayleigh as a particular case, is the usual reference for hourly or ten-minute speeds :ref:`[20] <ref-justus1978>`, :ref:`[21] <ref-carta2009>`.

The same reasoning, applied to the three Cartesian components of the velocity of a molecule of an ideal gas, leads to the Maxwell-Boltzmann distribution, familiar to students of thermodynamics and kinetic theory. The example shows how a probability distribution can follow from explicit physical hypotheses, and not only from an empirical fit.

Why does this matter for the reliability of materials?
------------------------------------------------------

The shape of the distribution matters also outside curve fitting, because it underlies the theory of structural and materials reliability. Suppose that a structure, such as a reinforced-concrete beam, has a mechanical strength of random behavior, modeled by the variable :math:`R`. If this structure is subjected to a fixed, known load :math:`s`, failure will occur whenever the strength is lower than the load.

In this simplified scenario, the failure probability :math:`P_f` is exactly the value of the cumulative distribution function (CDF) of :math:`R` evaluated at the point :math:`s`,

.. math::

   P_f = P(R < s) = F_R(s).

This simple balance shows why knowing only the mean strength of a material is insufficient for engineering. The safety of the structure is governed by the behavior of the *lower tail* of the distribution (the lowest and rarest strength values), and a model whose lower tail does not match that of the data may underestimate the failure probability. In real designs, both :math:`R` and :math:`s` are random quantities, which requires evaluating the probabilistic interference between them and highlights the need to choose distributions that reflect the physics of failure, as discussed in reference guidelines on failure data :ref:`[12] <ref-nist2012>`.

.. _`subsec:protocolo`:

Protocol common to the case studies
-----------------------------------

So that the analyses can be reproduced and compared, the case studies developed in Sections :ref:`4 <sec:vento>` and :ref:`5 <sec:temperatura>` follow a protocol divided into the seven sequential steps described below.

#. **Data documentation and physical context:** identification of the primary source (institution, monitoring station, coordinates, and altitude), observation period, measured physical quantity, time resolution of the readings (for example, daily means or instantaneous values), and associated instrumentation.

#. **Quality and physical-consistency check:** survey of missing data, identification of possible spurious readings, and evaluation of support constraints (for example, the nonnegativity of wind speed or the limits of relative humidity). The criteria for discarding or handling gaps are made explicit and justified.

#. **Definition of the sampling window:** prior and justified establishment of homogeneous temporal or spatial windows (such as restricting the data to a specific month to attenuate seasonal nonstationarity), avoiding *a posteriori* selections aimed at favoring a predetermined model. When no stratification is made, the target is stated. For wind, for example, the target is the aggregate historical distribution over the whole period, which mixes the seasons of the year.

#. **Exploratory statistical description:** characterization of the sample by measures of location, dispersion, skewness (:math:`\widehat\gamma_1`), and kurtosis (:math:`\widehat\beta_2`), together with reference empirical quantiles (:math:`Q_{0.05}`, :math:`Q_{0.50}`, :math:`Q_{0.95}`) and plots of the time series and the histogram.

#. **Parameter estimation and fitting of the families:** fitting of the reference models, estimated by maximum likelihood with the physical support constraints (such as the origin fixed at zero), and of the GLD-FKML, estimated by the method of moments with multiple starting points. The validity of the parameters and the resulting support are checked.

#. **Goodness-of-fit diagnostics and quantile comparison:** comparative evaluation by metrics in the units of the quantity. The Kolmogorov-Smirnov distance, :math:`D_n = \sup_x |F_n(x) - \widehat{F}(x)|`, is used to measure the largest cumulative discrepancy, together with the quantile deviations

   .. _eq:delta:

.. math::

   \Delta_p = Q_{\text{model}}(p) - Q_{\text{empirical}}(p), \quad p \in \{0.05,\, 0.50,\, 0.95\},
   \tag{14}

   whose sign indicates underestimation (negative) or overestimation (positive). The fits are compared visually in panels with overlaid densities, cumulative distribution functions, and quantile-quantile (Q-Q) plots.

#. **Interpretation in the units of the phenomenon and limits of validity:** physical translation of the discrepancies into the context of the application, comparing them with the measurement resolution and with the sampling uncertainty of the empirical quantiles themselves, and discussing the principle of parsimony against the cost of additional parameters.

The distance :math:`D_n` is used here as a descriptive measure. The usual :math:`p`-values of the Kolmogorov-Smirnov test do not apply directly, because the parameters are estimated from the same data :ref:`[22] <ref-lilliefors1967>`, the daily observations are dependent on one another, and the recorded values are rounded. To give a scale to the discrepancies, the notebook that accompanies the paper estimates the sampling variability of the empirical quantiles by block *bootstrap* resampling of consecutive days :ref:`[23] <ref-kunsch1989>`, which preserves the dependence between nearby days by drawing only blocks without recording gaps, and quantifies by simulation the effect of rounding on :math:`D_n`. These scales serve to compare orders of magnitude. None of them is used as a hypothesis test.
