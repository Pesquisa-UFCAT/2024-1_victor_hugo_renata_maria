Flexible distributions
========================

A brief introduction to the generalized lambda distribution and materials for
exploring wind and temperature data with Python and ``pyGLAM``.

:doc:`Download data and notebooks <downloads>`

FKML in a nutshell
---------------------

The generalized lambda distribution, in the FKML parameterization, can represent
symmetric or asymmetric shapes with bounded or unbounded tails. It is defined by
its quantile function: for a probability :math:`u`, :math:`Q(u)` gives the value
below which that fraction of the distribution lies. For example, :math:`Q(0.5)` is
the median.

.. math::

   Q(u)=\lambda_1+\frac{1}{\lambda_2}
   \left[\frac{u^{\lambda_3}-1}{\lambda_3}
   -\frac{(1-u)^{\lambda_4}-1}{\lambda_4}\right],
   \qquad 0<u<1,\quad\lambda_2>0.

* :math:`\lambda_1` shifts the distribution.
* :math:`\lambda_2` inversely controls scale: increasing it reduces dispersion.
* :math:`\lambda_3` and :math:`\lambda_4` control shape, mainly on the left and
  right sides, respectively.

When a shape parameter is zero, the corresponding fraction is replaced by its
logarithmic limit. Parameters can be fitted by the method of moments, as in the
notebooks. Besides agreement with the data, the model's support must be checked
against the physical quantity and the observations.

Paper
--------

The paper will be made available here after publication.

.. TODO: add the paper citation and link only after publication.

.. toctree::
   :hidden:

   downloads
