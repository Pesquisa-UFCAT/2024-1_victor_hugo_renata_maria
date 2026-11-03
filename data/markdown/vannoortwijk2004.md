<!--
Fonte: vannoortwijk2004.pdf (15 páginas)
van Noortwijk & Frangopol (2004). Two probabilistic life-cycle maintenance models for deteriorating civil infrastructures. Probabilistic Engineering Mechanics 19(4), 345-359. doi:10.1016/j.probengmech.2004.03.002
Extração: texto do PDF (pymupdf4llm) corrigido página a página a partir da imagem da página por um modelo de linguagem
(símbolos, equações em LaTeX, tabelas). Figuras: só a legenda. Conferir equações e números contra o PDF antes de citar.
-->

<!-- página 1 -->

# Two probabilistic life-cycle maintenance models for deteriorating civil infrastructures

Jan M. van Noortwijk<sup>a,b,*</sup>, Dan M. Frangopol<sup>c</sup>

> <sup>a</sup>HKV Consultants, P.O. Box 2120, NL-8203 AC Lelystad, The Netherlands
>
> <sup>b</sup>Faculty of Electrical Engineering, Mathematics and Computer Science, Delft University of Technology, P.O. Box 5031, NL-2600 GA Delft, The Netherlands
>
> <sup>c</sup>Department of Civil, Environmental, and Architectural Engineering, University of Colorado, Boulder, CO 80309-0428, USA

Received 23 June 2003; revised 4 September 2003; accepted 18 March 2004

### Abstract

The purpose of this paper is to describe and compare two maintenance models for deteriorating civil infrastructures that can be used to insure an adequate level of reliability at minimal life-cycle cost. These models, referred to Rijkswaterstaat's model and Frangopol's model have been independently developed by the authors of this paper and their associates. The former model has been applied by the Netherlands Ministry of Transport, Public Works and Water Management (Rijkswaterstaat). It can be used for justification and optimisation of maintenance measures. The latter model contributed to the further development of the bridge management methodology that has been set up by the UK Highways Agency.

© 2004 Elsevier Ltd. All rights reserved.

*Keywords:* Life-cycle costing; Deterioration; Maintenance optimisation; Lifetime extension; Bridge management; Renewal theory; Simulation; Gamma process

## 1. Introduction

The purpose of this paper is to describe and compare two maintenance models for deteriorating civil infrastructures that can be used to balance structural reliability and life-cycle cost. These two models are the Rijkswaterstaat's model and Frangopol's model. The former model has been applied for justification and optimisation of maintenance measures by the Netherlands Ministry of Transport, Public Works and Water Management (Rijkswaterstaat); detailed information on this model can be found in Refs. [1,2]. The latter model contributed to the further development of the bridge management methodology that has been set up by the UK Highways Agency [3–5]; additional information on this model can be found in Refs. [6–10,35]. Both models can be applied to determine the best maintenance strategy to insure

---

\* Corresponding author. Address: HKV Consultants, P.O. Box 2120, NL-8203 AC Lelystad, The Netherlands. Tel.: +31-320-294203; fax: +31-320-253901.

*E-mail addresses:* j.m.vannoortwijk@hkv.nl (J.M. van Noortwijk), dan.frangopol@colorado.edu (D.M. Frangopol).

an adequate level of reliability at minimal life-cycle cost. These two models have been presented and discussed during the workshop on Optimal Maintenance of Structures [11].

The outline of this paper is as follows. The two maintenance models are described in Section 2. The actual comparison of the condition-based maintenance model of Rijkswaterstaat and the reliability-based maintenance model of Frangopol is presented in Section 3. Finally, conclusions are given in Section 4.

## 2. Maintenance models

Civil infrastructure systems are deteriorating with time. Designing these systems for a particular service life and maintaining them in a safe condition during their entire service life have been recognised as very critical issues worldwide. According to Ref. [12] there are two types of maintenance work: preventive maintenance which if it is not done it will cost more at a later stage to keep the structure in a safe condition, and essential maintenance which is required to keep the structure safe. Whilst it is easy to

---

0266-8920/$ - see front matter © 2004 Elsevier Ltd. All rights reserved.
doi:10.1016/j.probengmech.2004.03.002

<!-- página 2 -->

défend essential maintenance work on safety grounds, since failure consequences are in general extremely large, preventive treatments are more difficult to justify. Engineering judgment or best practice is usually put forward as reasons for undertaking such work. Some have questioned as whether some types of preventive work, including both proactive preventive maintenance (i.e. applied before any indication of deterioration is apparent) and reactive preventive maintenance (i.e. applied only after some deterioration is evidenced) are necessary at all. There is an urgent need, therefore, to justify preventive work in a rational manner [4]. For highway bridges, some of the preventive maintenances currently in practice include cathodic protection, silane treatment, painting of steelwork, and concrete patch repairs. Many engineers believe that these preventive measures are worthwhile in the long term, but cannot defend this viewpoint on a reliability basis. This is simply because this basis does not exist. For this reason, a reliability-based approach has to be developed and used to identify optimal preventive maintenance strategies based on lifetime reliability and life-cycle costs for different civil infrastructure systems. The use of condition-based and reliability-based maintenance optimisation models is therefore of considerable interest for optimum life-cycle maintenance of deteriorating civil infrastructures.

## 2.1. Condition-based maintenance model

### 2.1.1. Maintenance

The area of optimising maintenance through mathematical models was founded in the early sixties. This pioneering work is summarised in Refs. [13,14]. The interest in maintenance optimisation had been brought about by the high cost of military-industrial equipment such as jet airliners, electronic computers, and ballistic missiles, among others. A well-known model of this period is the age replacement model. The age replacement strategy involves replacement upon failure or upon reaching a predetermined age, whichever occurs first. The predetermined age in an age replacement strategy is called the age replacement interval. According to Refs. [15,16], the age replacement model is one of the maintenance optimisation models that has been applied most.

As a basis for optimising maintenance, Rijkswaterstaat implemented the age replacement model with discounted cost. The criterion of expected discounted cost (net present value) over an unbounded horizon is used for comparing maintenance decisions (for arguments on whether to use a bounded or unbounded horizon, see Section 3.4). By using this criterion, the cost of preventive maintenance can be balanced against the cost of corrective (also called essential in Frangopol's model) maintenance. For a discussion about which cost-based criterion can best be used, we refer to Ref. [17].

The maintenance of structures can often be modelled as a (discrete) renewal process ([18], chapters 12–13; [19],

chapter 3), whereby the renewals are the maintenance actions that bring a component back into its original condition or 'as good as new state'. After each renewal we start, in statistical sense, all over again. A discrete renewal process $\{N(n), n = 1, 2, 3, \ldots\}$ is a non-negative integer-valued stochastic process that registers the successive renewals in the time interval $(0, n]$. Let the renewal times $T_1, T_2, \ldots$, be non-negative, independent, identically distributed, random quantities having the discrete probability function $\Pr\{T_k = i\} = p_i$, $i = 1, 2, 3, \ldots$, where $p_i$ represents the probability of a renewal in unit time $i$. We denote the cost associated with a renewal in unit time $i$ by $c_i$, $i = 1, 2, 3, \ldots$ In mathematical terms, the (present) discounted value of the cost $c_i$ in unit time $i$ is defined to be $\alpha^i c_i$ with $\alpha = [1 + (r/100)]^{-1}$ the discount factor per unit time and $r$ the discount rate per unit time, where $r > 0$.

The expected discounted cost over a bounded time horizon can be obtained with a recursive formula. To obtain this equation, we condition on the values of the first renewal time $T_1$ and apply the law of total probability. The cost associated with occurrence of the event $T_1 = i$ is $c_i$ plus the additional expected discounted cost during the interval $(i, n]$, $i = 1, \ldots, n$. Hence, the expected discounted cost over the bounded horizon $(0, n]$, denoted by $E(K(n, \alpha))$, can be written as

$$E(K(n, \alpha)) = \sum_{i=1}^{n} \alpha^i p_i [c_i + E(K(n-i, \alpha))], \tag{1}$$

$$n = 1, 2, 3, \ldots, \quad K(0, \alpha) \equiv 0.$$

By using discrete-time renewal theory ([18], chapter 13), the expected discounted cost over an unbounded horizon can be written as [20]

$$\lim_{n \to \infty} E(K(n, \alpha)) = \frac{\sum_{i=1}^{\infty} \alpha^i c_i p_i}{1 - \sum_{i=1}^{\infty} \alpha^i p_i}. \tag{2}$$

For cost-optimal investment decisions, we are interested in finding an optimum balance between the initial cost of investment and the future cost of maintenance, being the area of life-cycle costing. In this situation, the monetary losses over an unbounded horizon are the sum of the initial cost of investment $c_0$ and the expected discounted future cost in Eq. (2). A similar result can be obtained for continuous-time renewal processes [21].

### 2.1.2. Deterioration

In the condition-based maintenance model of Rijkswaterstaat, ageing has been modelled in three ways with increasing complexity:

1. Lifetime model on the basis of the probability distribution of the lifetime or time of failure.

<!-- página 3 -->

2. Deterioration model on the basis of the stochastic process of deterioration, where failure is defined as the event in which—due to deterioration—the condition (resistance) drops below the failure level (load). It is assumed that the expected deterioration at time $t$ can be described using a power law; that is, the expected deterioration at time $t$ can be written as $at^b$ for $a, b > 0$.

3. Deterioration and lifetime-extension model on the basis of the stochastic process of deterioration combined with lifetime extension, where failure is defined as the event in which the condition drops below the failure level. The deterioration process with lifetime extension has been approximated by a deterioration process without lifetime extension. The approximate expected deterioration is a least squares power law fit to the lower envelope function of the exact deterioration process with lifetime extension. The coefficient of variation of the deterioration at the time at which the expected deterioration equals the failure level is unchanged.

For all three models, the optimal preventive replacement interval follows from an age replacement model based on a lifetime distribution. For the deterioration models, the probability of failure per year (discrete lifetime distribution) is defined as the probability that the condition drops below the failure level per year.

Since deterioration is uncertain, it can best be regarded as a stochastic process. At first glance, it seems possible to represent the uncertainty in a deterioration process by the normal distribution. This probability distribution has been used for modelling the exchange-value of shares and the movement of small particles in fluids and air. A characteristic feature of this model—also denoted by the Brownian motion with drift (see e.g. [19], chapter 7)—is that a structure's resistance alternately increases and decreases, like the exchange-value of a share. For this reason, the Brownian motion is inadequate in modelling deterioration, which proceeds in one direction. In order for the stochastic deterioration process to proceed in one direction, we consider it as a so-called 'gamma process'. In mathematical terms, a gamma process is a stochastic process with independent non-negative increments having a gamma distribution.

A random quantity $X > 0$ has a gamma distribution with shape parameter $v > 0$ and scale parameter $u > 0$ if its probability density function (PDF) is given by:

$$\text{Ga}(x|v, u) = [u^v/\Gamma(v)]x^{v-1}\exp\{-ux\} \tag{3}$$

where $\Gamma(v) = \int_{t=0}^{\infty} t^{v-1}\exp\{-t\}dt$ is the gamma function for $v > 0$. Let $X(t)$ denote the amount of deterioration at time $t$, $t \geq 0$, and let the PDF of $X(t)$ be given by

$$f_{X(t)}(x) = \text{Ga}(x|[at^b]/\theta, 1/\theta) \tag{4}$$

for $\theta > 0$ with mean and variance $E(X(t)) = at^b$ and $\text{Var}(X(t)) = \theta a t^b$, respectively. The stochastic process

{$X(t), t \geq 0$} is then called a gamma process. The parameter $\theta$ represents the uncertainty in the deterioration process; the larger $\theta$, the more uncertain the deterioration process [22].

A component is said to fail when its deterioration exceeds a certain level $y$, where $y$ is defined as the initial resistance $r_0$ minus the failure level $s$. Let the time at which the failure level is crossed be denoted by the lifetime $T$ (in years). Due to the gamma distributed deterioration (4), the lifetime distribution can then be written as:

$$F(t) = \Pr\{T \leq t\} = \Pr\{X(t) \geq y\} = \int_{x=y}^{\infty} f_{X(t)}(x)dx$$

$$= \frac{\Gamma([at^b]/\theta, y/\theta)}{\Gamma([at^b]/\theta)}, \tag{5}$$

where $\Gamma(v, x) = \int_{t=x}^{\infty} t^{v-1}\exp\{-t\}dt$ is the incomplete gamma function for $x \geq 0$ and $a > 0$. The probability of failure per year follows immediately from Eq. (5):

$$q_i = F(i) - F(i-1), \quad i = 1, 2, 3, \ldots \tag{6}$$

### 2.1.3. Age replacement

Under an age replacement policy ([14], chapters 3–4), a replacement is carried out at age $k$ (preventive replacement) or at failure (corrective replacement), whichever occurs first, where $k = 1, 2, 3, \ldots$ A preventive replacement entails a cost $c_P$, whereas a corrective replacement entails a cost $c_F$, where $0 < c_P \leq c_F$. According to Eq. (2), the expected discounted cost of age replacement over an unbounded horizon is

$$\lim_{n\to\infty} E(K(n,\alpha)) = \frac{\left(\sum_{i=1}^{k}\alpha^i q_i\right)c_F + \alpha^k\left(1 - \sum_{i=1}^{k}q_i\right)c_P}{1 - \left[\left(\sum_{i=1}^{k}\alpha^i q_i\right) + \alpha^k\left(1 - \sum_{i=1}^{k}q_i\right)\right]}, \tag{7}$$

where $k$ is the age replacement interval. The optimal age replacement interval $k^*$ is an interval for which the expected discounted cost over an unbounded horizon is minimal. Note that the replacement model can also be applied for determining the optimal initial resistance of a structure, which balances the initial cost of investment $c_P$ optimally against the future cost of maintenance in Eq. (7) (see also [23]). The expected discounted cost can also be calculated over a bounded horizon using Eq. (1). In situations with a bounded time horizon larger than 50 years, the cost over an unbounded horizon (2) may serve as a good approximation.

As a simplified example, we study the maintenance of a cylinder on an existing swing bridge (adapted from Ref. [1]). Preventive maintenance of a cylinder mainly consists of replacing the guide bushes and plunger, and replacing the packing of the piston rod. In the event of corrective maintenance, the cylinder has to be replaced completely because too much damage has occurred. The cost of preventive maintenance is $c_P = 30,000$ Dutch guilders,

<!-- página 4 -->

> **Fig. 1.** Maintaining a cylinder on an existing swing bridge. The expected discounted cost over an unbounded horizon as a function of the age replacement interval.

whereas the cost of corrective maintenance is $c_F = 100,000$ Dutch guilders. Both maintenance actions bring the cylinder back into its 'good as new state'. The expected deterioration is assumed to degrade linearly in time from the initial condition of 100% down to the failure level of 0%. The time at which the expected condition equals the failure level is 15 years. For an annual discount rate of 5%, the expected discounted cost of preventive and corrective maintenance is displayed in Fig. 1, where the vertical axis shows the net present value in 1000 Dutch guilders (i.e. KFL). The expected discounted cost over an unbounded horizon is minimal for a preventive replacement interval of 13 years. On the basis of the expected deterioration, this preventive replacement interval can approximately be transformed into the optimum preventive maintenance (condition) level of 13%.

### 2.1.4. Failure

In structural engineering, we can roughly identify two types of failure: structural failure and condition failure. Structural failure can be a collapse, whereas condition failure means that a certain predetermined norm level has been exceeded. Condition failure is defined as the event at which a structure fails to meet its main functional requirements. It can be used to prevent structures from being unsafe by the safety requirement (often expressed in terms of the reliability index; see Section 3.3). Therefore, structures usually do not fail due to physical failure, but due to condition failure. Inspections must be carried out to insure that condition failure will be detected. Physical failure is more common in mechanical and electrical engineering. In these fields, one often considers equipment, which can assume at most two states: the functioning state and the failed state. For example, a motor or switch is either working or not. A structure, on the other hand, can be in a range of states depending on its degrading condition.

In situations where the cost of structural failure is very high, failure norms can only be optimised in the design phase. Because the bulk of the maintenance programme is devoted to existing structures, failure norms should generally be treated as constraints. Given these constraints, a maintenance manager can optimise the preventive maintenance level. A cost-optimal preventive maintenance level optimally balances the cost of preventive maintenance and the cost of corrective maintenance. The cost of corrective maintenance may include cost of traffic-jam, detour, vehicle-weight restriction, closure, etc. The load is generally be taken into account in the design phase by incorporating it into the functional requirements and thus into the failure norm.

### 2.1.5. Lifetime extension

The deterioration model has been extended for the possibility of lifetime-extending maintenance. With this model both the interval of preventive replacement and lifetime extension can be optimised. Through replacement, the condition of a component is restored to its original condition. Through lifetime extension, the deterioration can be delayed so that failure is postponed and the lifetime of a component is extended (e.g. a coating protecting steel). Possible effects of lifetime-extending measures are the initiation period (time interval in which no deterioration occurs) and the condition improvement. In addition, the rate of deterioration after lifetime extension can be 'repeating' (after every lifetime extension the rate of deterioration is the same

<!-- página 5 -->

# Expected condition with lifetime-extending maintenance without replacement

> **Fig. 2.** Expected condition of the steel with 'repeating' lifetime extension in terms of grit blasting.

and equals the rate of deterioration at the initial condition; see Fig. 2) and 'non-repeating' (after every lifetime extension the rate of deterioration is different and equals the rate of deterioration at the corresponding condition; see Fig. 3).

Let the rate of deterioration now be based on periodic lifetime-extending maintenance at a frequency of once in $w$ years. The cost of lifetime-extending maintenance is $c_L$. Suppose either a preventive replacement or a corrective replacement is carried out at unit time $i$, then the lifetime is

extended at the units of time $w, 2w, 3w, \ldots, \lfloor (i-1)/w \rfloor w$, where $\lfloor x \rfloor$ is the largest integer less than or equal to $x$. Using the geometric series, the discounted cost of a lifetime extension at unit time $i$ can be written as

$$\alpha^{1w} c_L + \alpha^{2w} c_L + \ldots + \alpha^{\lfloor (i-1)/w \rfloor w} c_L$$

$$= \frac{\alpha^w - \alpha^{(\lfloor (i-1)/w \rfloor + 1)w}}{1 - \alpha^w} c_L = \chi_{iw} c_L, \quad w = 1, 2, 3, \ldots \tag{8}$$

# Expected condition with lifetime-extending maintenance without replacement

> **Fig. 3.** Expected (hypothetical) condition of the steel with 'non-repeating' lifetime extension in terms of condition improvement.

<!-- página 6 -->

# 350

J.M. van Noortwijk, D.M. Frangopol / Probabilistic Engineering Mechanics 19 (2004) 345–359

Then, it follows from Eq. (2) that the expected discounted cost of lifetime extension and age replacement over an unbounded horizon is

$$\lim_{n\to\infty} E(K(n,\alpha)) = \frac{\sum_{i=1}^{k}[\chi_{iw}c_L+\alpha^i c_{F,i}]q_i+[\chi_{kw}c_L+\alpha^k c_{P,k}]\left(1-\displaystyle\sum_{i=1}^{k}q_i\right)}{1-\left[\left(\displaystyle\sum_{i=1}^{k}\alpha^i q_i\right)+\alpha^k\left(1-\displaystyle\sum_{i=1}^{k}q_i\right)\right]}, \tag{9}$$

where $c_{P,k}$ is the time-dependent cost of preventive replacement at age replacement interval $k$ and $c_{F,i}$ is the time-dependent cost of corrective replacement at unit time $i$. The probability of failure $q_i$ now depends on the lifetime extension strategy.

The lifetime-extending maintenance model can be used to optimise maintenance in both the design phase and the application phase. In the design phase, the initial cost of investment can be optimally balanced against the future cost of maintenance. In the application phase, the cost of preventive maintenance (lifetime extension and preventive replacement) can be optimally balanced against the cost of corrective maintenance (corrective replacement and failure) The lifetime-extension model enables optimal maintenance decisions to be determined on the basis of the uncertainties in the deterioration (e.g. the loss of steel thickness due to corrosion). The model has been successfully applied in Ref. [2] to optimise the application of a protective steel coating. Two examples of a cost-optimal frequency of lifetime-extending maintenance are shown in Figs. 2 and 3 with repeating and non-repeating lifetime extension, respectively. In the first example, the lifetime of the steel can be extended by grit blasting (with 0.1 mm loss of steel thickness), as well as placing the new coating. The expected condition without lifetime extension in Fig. 2 represents the corrosion process given initiation at time zero.

## 2.1.6. Inspection

Strictly speaking, maintenance on the basis of preventive maintenance levels depends on two decision variables: (i) the rate of inspection (depending on both frequency and accuracy) and (ii) the preventive maintenance level. These two variables are interdependent: with a high rate of inspection it suffices to choose the preventive maintenance level to be close to the failure level, whereas with a low rate of inspection the preventive maintenance level should be larger than the failure level. Therefore, preventive maintenance levels determined with an age replacement model are approximately cost-optimal. If the cost of inspection is taken into account, a more complex model of condition-based preventive maintenance should be used [see [24,25]]. Other tailor-made examples include determining cost-optimal rates of inspection for berm breakwaters and the block mats of the Eastern–Scheldt barrier [see [26,22], respectively].

## 2.2. Reliability-based maintenance model

### 2.2.1. Condition and reliability deterioration

Currently available structure management systems, including PONTIS [27] and BRIDGIT [28], are directly related to the condition states of bridge elements. The number of condition states is limited (e.g. five) for each bridge element. Each condition describes the type and severity of element deterioration in visual terms. PONTIS and BRIDGIT assume that the condition states incorporate all the information necessary to predict future deterioration and use a Markovian deterioration model to predict the annual probability of transitions among condition states.

As indicated in Refs. [7,9], the Markovian approach used in currently available bridge management systems has several important limitations, such as: (a) severity of element deterioration is described in visual terms only; (b) element condition deterioration is assumed to be a single step function; (c) transition rates among condition states of a bridge element are not time dependent; and (d) bridge system condition deterioration is not explicitly considered. Experience gained in different countries shows that the major part of the work on existing bridges depends on the load carrying capacity (or structural reliability) of the bridge system rather than the condition states of the bridge elements alone [7]. Consequently, bridge management systems have to consider bridge reliability deterioration.

Fig. 4 shows simplified (i.e. linear) condition index and reliability index deterioration models (also called profiles). These profiles are each defined by three variables:

> **Fig. 4.** (a) Condition and (b) reliability profiles.

<!-- página 7 -->

(a) the condition profile is defined by the initial condition index, $C_0$, the time of condition deterioration initiation, $t_{iC}$, and the condition deterioration rate, $\alpha_C$; (b) the reliability index profile (also called reliability profile) is defined by the initial reliability index, $\beta_0$, the time of reliability index deterioration initiation, $t_i$, and the reliability index deterioration rate, $\alpha$. As indicated in Ref. [29] there are fundamental differences between the condition deterioration profile (Fig. 4(a)) and the reliability deterioration profile (Fig. 4(b)).

First, the condition deterioration profile refers to deterioration in visual terms. The reliability deterioration profile refers to the deterioration of a proper measure of structural performance defined by the reliability index. For example, considering the element 107 from PONTIS [27] representing painted steel open girders, Fig. 5(a) shows the gradual transition among five condition states: no corrosion (paint system sound and functioning as intended), $t \leq t_{ic} = t_{C1}$; paint distress, $t_{C1} < t \leq t_{C2}$; rust formation, $t_{C2} < t \leq t_{C3}$; active corrosion (corrosion present but any section loss resulting from active corrosion does not yet warrant structural analysis), $t_{C3} \leq t \leq t_{C4}$; and section loss (i.e. corrosion has caused section loss sufficient to warrant structural analysis to ascertain the effect of damage), $t > t_{C4}$. In contrast to the visual conditions indicated in Fig. 5(a), the reliability index deterioration profile in Fig. 5(b) refers to the element performance deterioration measured in terms of reliability index. The reliability deterioration states (e.g. those indicated in Fig. 5(b)) are different from the condition deterioration states in Fig. 5(a).

Second, the condition and reliability deterioration profiles may have little or no correlation even if they refer

> **Fig. 5.** (a) Condition and (b) reliability states.

to the same element. In fact, an element may fail suddenly (i.e. brittle failure) even if its visual condition immediately before failure is perfect, or may be extremely safe even if its visual condition is extremely poor.

Third, a maintenance action due to loss in condition index (i.e. condition-based maintenance) can have no effect on reliability index (see Fig. 6) or, vice versa, a maintenance action due to loss in reliability (i.e. reliability-based maintenance) can have no effect on the condition index (see Fig. 7).

Finally, system effects (e.g. combined effects of different failure modes associated with a bridge element, combined effects of failure modes of different members in a bridge, combined effects of serviceability and ultimate limit states) can only be captured by reliability deterioration profiles [9].

### 2.2.2. Reliability index profile and reliability states

The reliability profile is defined as the variation of the reliability index with time $\beta(t)$. As demonstrated in Ref. [7], similar bridges designed and constructed to the same requirements, for various reasons, end up with different reliability levels. This variation of reliability index influenced by various factors can be captured by using random variables.

The reliability profile $\beta(t)$ is difficult to predict for bridges under various maintenance interventions. Fig. 8 (adapted from Ref. [30]) shows examples of reliability profiles of deteriorating structures associated with different maintenance scenarios. $E0$ represents the no maintenance scenario, and $E1$ represents a maintenance scenario with one essential maintenance. $E0, P$ and $E1, P$ represent cyclic preventive maintenance scenarios without and with one essential maintenance, respectively.

> **Fig. 6.** (a) Condition and (b) reliability profiles: condition-based maintenance; improvement in condition without effect on reliability.

<!-- página 8 -->

# Condition and Reliability Profiles

> **Fig. 7.** (a) Condition and (b) reliability profiles: reliability-based maintenance; improvement in reliability without effect on condition.

In general, the service life of deteriorating structures is a progression of reliability states. In Ref. [9] five reliability states are defined for steel/concrete composite bridges as follows: excellent (i.e. State 5: β ≧ 9.0), very good (i.e. State 4: 9.0 > β ≧ 8.0), good (i.e. State 3: 8.0 > β ≧ 6.0), fair (i.e. State 2: 6.0 > β ≧ 4.6), and unacceptable (i.e. State 1: β < 4.6). Notice that a new (i.e. as constructed) bridge belonging to a group of similar bridges is not necessarily in State 5, since the initial reliability index of the bridge group is not completely known.

### 2.2.3. The eight random variables maintenance model

The eight random variables affecting the lifetime reliability profile of an individual deteriorating structure or a group of deteriorating structures under maintenance are shown in Fig. 9 (adapted from Ref. [9]). These random variables are: the initial reliability index $B_0$, the time of damage initiation $T_I$, the reliability index deterioration rate $A$, the time of first application of preventive maintenance $T_{PI}$, the time of reapplication of preventive maintenance $T_P$, the duration of preventive maintenance effect on reliability $T_{PD}$, the deterioration rate of reliability index during preventive maintenance effect $\Theta$, and the improvement in reliability index (if any) immediately after the application of preventive maintenance $\Gamma$. The PDFs of $B_0$, $T_I$, $A$, $T_{PI}$, $T_P$,

> **Fig. 8.** Reliability profiles associated with different maintenance scenarios.

<!-- página 9 -->

> **Fig. 9.** Reliability profiles and associated random variables for the options with or without preventive maintenance.

$T_{PD}$, $\Theta$, and $\Gamma$, and their main descriptors for a group of steel/concrete composite bridges are indicated in Ref. [9].

### 2.2.4. Monte Carlo simulation

Monte Carlo simulation is used to generate the random numbers for the PDFs of the eight random variables $B_0$, $T_I$, $A$, $T_{PI}$, $T_P$, $T_{PD}$, $\Theta$, and $\Gamma$ and to capture the propagation of uncertainties during the entire service of existing deteriorating structures. As a qualitative example, Fig. 10 shows the time variation of the mean and standard deviation of the reliability index of a bridge group for the options with and without preventive maintenance.

The simulation process is also computing the PDF of the time when the reliability profile down-crosses a target reliability level (also called rehabilitation time). As an example, a group of 100 steel/concrete composite bridges is studied assuming that all bridges are constructed at the same time (say, at $t = 0$). The reliability states are those defined previously and the eight random variables of the maintenance model in Fig. 8 are defined in Ref. [9]. The time variation of the number of bridges in each reliability state is indicated in Fig. 11 [10] for the options with and without maintenance. The beneficial effect of preventive maintenance is clearly indicated by the substantial decrease in the number of bridges in critical States 1 and 2.

### 2.2.5. Probability and cost profiles for different bridge types

In order to choose the optimal maintenance strategy for each bridge type, the present value of the expected cost of rehabilitation with and without preventive maintenance interventions has to be computed. As a first step in this complex computation, the probability of rehabilitation has to be obtained [31]. Figs. 12 and 13 (adapted from Ref. [31]) show the probability of rehabilitation for four bridge types assuming that no preventive maintenance has been done and preventive maintenance has been done, respectively. The computation of these probabilities is based on triangular

> **Fig. 10.** Time variation of the mean and standard deviation of the reliability index of a bridge group for the options with and without preventive maintenance.

> **Fig. 11.** Expected number of bridges in each reliability state from a group of 100 bridges for the options with or without preventive maintenance.

<!-- página 10 -->

> **Fig. 12.** Probability of rehabilitation of four bridge types assuming no preventive maintenance has been done.

distributions of rehabilitation rates predicted by experts [31] for two different situations: (a) rehabilitation assuming no preventive maintenance has been done and (b) rehabilitation assuming preventive maintenance has been done. For each bridge type, computations were performed according to the following assumptions (Maunsell Ltd. and Transport Research Laboratory, [32]): (a) the preventive maintenance intervention is defined by repeating the application of the triangular distribution [10,20,25], where 10, 20, and 25 indicate the minimum, mode, and the maximum number of years, respectively; and (b) the triangular probability distributions of rehabilitation rates with and without preventive maintenance and the unit maintenance costs are those indicated in Maunsell Ltd. and Transport Research Laboratory [32].

The results are illustrated for steel/concrete composite bridges in Fig. 14 (adapted from Ref. [31]), where the expected cumulative costs are discounted to present values using a net discount rate for cost of 6%. From this figure it is clear that after about 30 years the strategy using preventive maintenance is the most economical.

### 2.2.6. Optimisation

Recently, Kong and Frangopol [30] developed a computer program for life-cycle analysis and optimisation of deteriorating structures. This program provides

> **Fig. 13.** Probability of rehabilitation of four bridge types assuming preventive maintenance has been done.

> **Fig. 14.** Present value of expected cumulative unit maintenance cost of steel/concrete composite bridges [GBP/m²] with and without preventive maintenance assuming 6% discount rate for cost.

a reliability-based framework for life-cycle maintenance analysis and optimisation of deteriorating structures based on the model shown in Fig. 10. Most input data are represented by random variables. In this manner, the uncertainties associated with various maintenance interventions, reliability index profiles, and costs are all taken into account. Optimisation and parametric analyses modules help the identification of the maintenance strategy that best balance the present value of the expected cumulative cost associated with maintenance interventions and reliability index profiles over a specified time horizon usually assumed to be between 30 and 50 years. This maintenance optimisation can be performed for both an individual structure and a group of structures. Additionally, both time-controlled and/or reliability-controlled maintenance scenarios can be considered. Numerical examples of cost optimisation of time of interventions for different maintenance scenarios of deteriorating bridges are given in Ref. [30] considering a discount rate of 6%, a time horizon of 50 years, a group of 713 bridges built in different time periods, and six different maintenance scenarios including essential maintenance only, preventive maintenance only, and mixed preventive and essential maintenances.

## 3. Model comparison

### 3.1. Terminology

Before explaining the differences and similarities between the condition-based maintenance model of Rijkswaterstaat and the reliability-based maintenance model of Frangopol, it should be noted that both models use a slightly different terminology. For sake of clarity, both terminologies are compared in Table 1.

Unlike Rijkswaterstaat's model, preventive maintenance in terms of preventive replacement is not explicitly included in Frangopol's model. Replacement is defined as a combination of actions carried out to restore a component or structure, or to 'renew' it, to the initial condition.

<!-- página 11 -->

# Table 1
Comparison of terminology used in the two maintenance models

| Condition-based maintenance model (Section 2.1) | Reliability-based maintenance model (Section 2.2) |
|---|---|
| Condition | Performance (e.g. reliability index) |
| Initial condition | Initial performance |
| Preventive maintenance level | Not explicitly included |
| Failure level | Target level |
| Replacement (renewal) | Replacement |
| Preventive replacement | Not explicitly included |
| Corrective replacement | Essential maintenance (replacement) |
| Lifetime extension | Preventive maintenance (life extension) |
| Initiation period (time interval in which no deterioration occurs) | Damage initiation time |
| Condition improvement at lifetime extension | Performance improvement after preventive maintenance |
| Lifetime | Rehabilitation time |
| Time horizon | Life span (service life) |

The main reason for not explicitly including preventive replacement is that bridge management mainly deals with condition failure rather than structural failure (collapse). In the event of condition failure, there are no severe consequences to failure and preventive replacement is not cost-optimal. On the other hand, preventive replacement is implicitly included in Frangopol's model in terms of lifetime extension. Lifetime-extending maintenance is defined as activities that are carried out to extend the lifetime of (a component of) a structure. Depending on the system level, a replacement on one level can be a lifetime-extending maintenance action on another level. For example, renewing a coating can be regarded as a replacement of the coating itself as well as a lifetime extension of a steel plate.

## 3.2. Uncertainties

For modelling deterioration and maintenance, the following uncertainties can be identified:

1. initial performance/condition,
2. time of damage initiation,
3. deterioration rate without lifetime extension,
4. deterioration rate with lifetime extension,
5. time of first application of lifetime extension,
6. time of reapplication of lifetime extension,
7. duration of effect of lifetime extension,
8. performance/condition improvement at lifetime extension,
9. cost of maintenance (preventive replacement, corrective replacement, lifetime extension),
10. time horizon,
11. discount rate.

Frangopol's model includes eight random variables (i.e. uncertainties 1–8 above), whereas Rijkswaterstaat's model includes only the third random variable. The latter model assumes the other uncertainties to be deterministic and to be approximately incorporated in the uncertainty of the deterioration. The former model is hence more flexible than the latter. For example, in Frangopol's model, the time of damage initiation can be different from the duration of effect of lifetime extension, and the time of first application of lifetime extension can be different from the time of reapplication of lifetime extension. In Rijkswaterstaat's model, only one time of damage initiation and only one time of application of lifetime extension can be specified.

## 3.3. Differences

Although the maintenance models of Frangopol and Rijkswaterstaat are quite similar, the following five differences can be recognised:

1. multi-component, multi-failure mode and multi-uncertainty (Frangopol) vs. one component, one failure mode and one uncertainty (Rijkswaterstaat),
2. maintenance strategy for groups of similar structures (Frangopol) vs. maintenance strategy for groups of similar (critical) components (Rijkswaterstaat),
3. reliability-based (Frangopol) vs. condition-based (Rijkswaterstaat),
4. evaluation (Frangopol) vs. optimisation (Rijkswaterstaat),
5. model based on Monte Carlo simulation (Frangopol) vs. analytical model (Rijkswaterstaat).

The main objective for developing Rijkswaterstaat's model was to offer the maintenance manager a simple tool for optimising the maintenance of critical components. Therefore, the model focuses only on one component, one failure mode and one uncertainty. In order to keep the mathematics tractable, only the most important uncertainty–the uncertainty in the deterioration–has been considered. The uncertainties in the initial condition and the failure level can be approximately included in the uncertainty in the deterioration. The maintenance model is based on an age replacement strategy combined with the possibility of lifetime extension. The ageing mechanism is described by the gamma process. When the age replacement strategy is combined with a gamma-distributed deterioration, the expected discounted cost can be expressed in explicit form. Because Rijkswaterstaat's model is analytic, the combination

<!-- página 12 -->

of the interval of age replacement and the interval of lifetime extension for which the expected discounted cost is minimal can be determined. In essence, Rijkswaterstaat's model is an optimisation model. Although Rijkswaterstaat's model has primarily been developed for specifying cost-optimal maintenance strategies for groups of similar components [33], it can also be applied for determining maintenance strategies for groups of similar structures.

The advantage of Frangopol's model over Rijkswaterstaat's model is that more than one component, more than one failure mode and more than one uncertainty can be incorporated. In order to take account of all these components, failure modes, and uncertainties, the expected cost cannot be calculated in explicit form. Instead, the Monte Carlo simulation is used to compute the expected cumulative discounted cost. Frangopol's model is also more flexible in analysing all kinds of combinations of lifetime-extending measures, such as time of first application of lifetime extension, time of reapplication of lifetime extension, duration of effect of lifetime extension, and performance improvement at lifetime extension. Because the expected cumulative discounted cost cannot be determined in explicit form, Frangopol's model is an evaluation model rather than an optimisation model. However, very recently Kong and Frangopol [30] extended the capability of the original evaluation-based model to an optimisation maintenance model. Maintenance optimisation can be performed by repeatedly evaluating different maintenance strategies. Frangopol's model has primarily been developed for specifying a cost-optimal maintenance strategy for groups of similar structures on the basis of ageing components. Groups of similar bridges are formed by classifying bridges on the basis of the bridge type and the construction period. The parameters of the maintenance model are assessed using expert judgement.

The main conceptual difference between Frangopol's model and Rijkswaterstaat's model is that the former model is reliability-based and the latter model is condition-based. Reliability-based means that the performance is quantified in terms of the reliability index or beta index $\beta = -\Phi^{-1}(p)$, where $p$ is the failure probability. Condition-based means that the performance is quantified in terms of the condition, such as the surplus of average steel thickness, the overall functional quality, etc. Note that this condition does not have to coincide with the visual condition. When both models are used to model the deterioration of the same component, the target performance level should be the same; that is, the target reliability index in Frangopol's model (so-called 'target level') and the target condition in Rijkswaterstaat's model (so-called 'failure level') should represent the same target failure probability. As soon as the reliability index drops below the target level or, equivalently, the condition drops below the failure level, corrective/essential maintenance should be carried out.

Reliability-based management represents the future generation of bridge management systems [9,34].

The advantage of reliability-based maintenance is that the reliability is explicitly taken into account. In condition-based maintenance, the reliability only follows implicitly after transforming condition to reliability. The advantage of condition-based maintenance is that conditions can be measured or inspected, whereas reliabilities must be computed from conditions. Especially the effects of lifetime extension on the reliability index are difficult to estimate. Because a structure's reliability must be calculated on the basis of a probabilistic analysis, Frangopol's model can best be run by structural engineers having knowledge of probability. Rijkswaterstaat's model, on the other hand, can also be used by maintenance managers without much knowledge of probability. Due to the difference between the condition-based and reliability-based concepts, the management decisions associated with each of these concepts will in general be different [29].

A detailed comparison of Frangopol's model and Rijkswaterstaat's model can be found in Table 2.

### 3.4. Discount rate

Both Frangopol's model and Rijkswaterstaat's model are based on the notion of discounted cost. This cost is determined by summing the (present) discounted values of the cost over a bounded or an unbounded time horizon, under the assumption that the value of money decreases with time. The criterion of discounted cost is especially useful for balancing the initial cost of investment against the future cost of maintenance. After choosing the discount rate, different investment decisions can be compared and the decision with minimal expected discounted cost is often preferred. The choice of the discount rate is mainly a political decision; it serves as an agreement on comparing investments. In the United States and the United Kingdom, a discount rate of about 4 and 6%, respectively, has been used; in the Netherlands, a discount rate of 4% is usually chosen.

A characteristic feature of the discount rate is the later future cost is incurred, the less its present value and the less weight it carries in a cost-based comparison. For calculating the expected discounted cost, [4,7,12] use a bounded horizon, whereas Rijkswaterstaat uses an unbounded horizon. It is interesting to note that the same argument leads to either of the two choices. For high discount rates (larger than 6%), future cost incurred 50 years from now is small in comparison with the non-discounted cost. On the other hand, Rijkswaterstaat argues that 'in situations with a bounded time horizon larger than 50 years, the cost over an unbounded horizon may serve as a good approximation'. The advantage of the latter approach is that the renewal theory offers us a simple analytical formula for computing the expected discounted cost over an unbounded horizon [20,21]. As opposed to Frangopol's model, Rijkswaterstaat's model can be used to calculate the expected discounted cost over both a bounded and an unbounded horizon.

<!-- página 13 -->

Table 2
Comparison of the two maintenance models

| Maintenance model | Condition-based maintenance model (Section 2.1) | Reliability-based maintenance model (Section 2.2) |
|---|---|---|
| State | Condition-based | Reliability-based (beta index) |
| Uncertainties | (i) Deterioration | (i) Initial performance,<br>(ii) Damage initiation time<br>(iii) Deterioration rate with lifetime extension<br>(iv) Deterioration rate without lifetime extension<br>(v) Time of first application of lifetime extension<br>(vi) Time of reapplication of lifetime extension<br>(vii) Duration of effect of lifetime extension<br>(viii) Performance improvement at lifetime extension |
| Deterioration | Deterioration according to gamma process with independent increments | Uniformly-distributed deterioration rate assumed, but any type of distribution can be used |
| Complexity | Low | High |
| Decision basis | Optimisation | Evaluation |
| Decision variables | (i) Uniform intervals of lifetime extension and preventive replacement<br>(ii) Non-uniform intervals of corrective replacement | (i) Uniform and non-uniform intervals of lifetime extension<br>(ii) Non-uniform intervals of essential maintenance |
| System level considered | Groups of similar components or individual (critical) components | Groups of similar structures or individual structures |
| Number of components | One | More than one |
| Number of failure modes | One | More than one |
| Possible maintenance actions and their cost | (i) Lifetime extension<br>(ii) Preventive replacement<br>(iii) Corrective replacement | (i) Lifetime extension<br>(ii) Essential maintenance |
| Implementation | Analytical model | Monte Carlo simulation |
| Computer environment | Personal computer | Work station |
| Time horizon | Bounded and unbounded | Bounded |
| Discount rate | Greater than zero | Greater than or equal to zero |

## 3.5. Deterioration process

The two maintenance models represent the uncertainty in the deterioration in a different manner. In Frangopol's model, the expected deterioration is described by a model being linear or quadratic in time; the coefficients of these models are assumed to be random variables. In Rijkswaterstaat's model, the expected deterioration is described by a power law in time; the deterioration process is assumed to be a stochastic process (gamma process) with independent increments. Although the former approach may serve as a good approximation, the latter approach is more realistic. However, the former approach is more flexible in accommodating real data. Another difference is that Frangopol's model includes reliability deterioration and Rijkswaterstaat's model includes condition deterioration.

## 4. Conclusions

This paper described and compared two maintenance models that are currently being used to optimally balance structural reliability and life-cycle cost of deteriorating civil infrastructure. Frangopol's model contributed to the further development of the bridge maintenance methodology that has been set up by the UK Highways Agency, whereas Rijkswaterstaat's model has been applied in the Netherlands. Although the two maintenance models are quite similar, the following differences can be identified. The former model is reliability-based and treats the multicomponent, multi-failure mode and multi-uncertainty case. The latter model is condition-based and treats only one component, one failure mode and one uncertainty. Another difference is that Frangopol's model uses Monte Carlo simulation, whereas Rijkswaterstaat's model is analytic.

<!-- página 14 -->

Furthermore, the maintenance models differ in the way the uncertainty in the deterioration is modelled; that is, uncertain parameters as opposed to stochastic processes, respectively. Due to the difference between the condition-based and reliability-based concepts, the management decisions associated with each of these concepts will in general be different.

The authors believe that the two models could benefit from one another. For example, Frangopol's multi-component, multi-failure mode and multi-uncertainty model could benefit from the analytic formulas for both the expected discounted cost over an unbounded time horizon and the stochastic deterioration process of the Rijkswaterstaat model. The Monte Carlo simulation can then be used in both models to determine the probabilistic characteristics per renewal cycle, which can subsequently be up scaled to an unbounded horizon using renewal theory. The authors are considering a comprehensive analysis to determine the most sensitive parameters of their maintenance models in future studies.

## Acknowledgements

The work reported by the first author was supported by the Civil Engineering Division of the Netherlands Ministry of Transport, Public Works, and Water Management. The first author thanks Mr Leo Klatter, Mr Jaap Bakker and Mr Harry van der Graaf for their helpful discussions and comments in developing the Rijkswaterstaat model. The second author thanks Prof. Palle Thoft-Christensen, University of Aalborg, Denmark, and Dr Parag Das and Dr Victoria Hogg, from the Highways Agency, UK, for their helpful discussions in developing the maintenance model. He also thanks his former and current Ph.D. students Dr Jung S. Kong, who played a key role in implementing the maintenance model, Dr Emhaidy S. Gharaibeh and Mr Luis C. Neves for cooperation. The partial financial support of the US National Science Foundation through grants CMS-9506435, CMS-9912525, CMS-0217290 and of the UK Highways Agency is gratefully acknowledged. The opinions and conclusions presented in this paper are those of the authors and do not necessarily reflect the views of the sponsoring organizations.

## References

[1] van Noortwijk JM. Optimal replacement decisions for structures under stochastic deterioration. In: Nowak AS, editor. Proceedings of the eighth IFIP WG 7.5 working conference on reliability and optimization of structural systems, Kraków, Poland, 1998. Ann Arbor: University of Michigan; 1998. p. 273–80.

[2] Bakker JD, van der Graaf HJ, van Noortwijk JM. Model of lifetime-extending maintenance. In: Forde MC, editor. Proceedings of the 8th international conference on structural faults and repair, London, United Kingdom, 1999. Edinburgh: Engineering Technics Press; 1999.

[3] Frangopol DM. A probabilistic model based on eight random variables for preventive maintenance of bridges. Presented at the progress meeting optimum maintenance strategies for different bridge types, London: Highways Agency; 1998.

[4] Frangopol DM. (2000). Optimum maintenance strategies for different bridge types: project description and steel/concrete composite bridges, vol. 1, Final report to the Highways Agency, London, UK.

[5] Frangopol DM. (2003). Preventative Maintenance Strategies for Bridge Groups-Analysis, Volume 1, Final Report to the Highways Agency, London, U.K.

[6] Frangopol DM. Life-cycle cost analysis for bridges. Bridge safety and reliability. Reston, Virginia: ASCE; 1999. p. 210–36.

[7] Frangopol DM, Das PC. Management of bridge stocks based on future reliability and maintenance costs. Bridge Design, Construction, and Maintenance. Thomas Telford, London: The Institution of Civil Engineers; 1999. p. 45–58.

[8] Frangopol DM, Gharaibeh ES, Kong JS, Miyake M. (2000). Optimal network-level bridge maintenance planning based on minimum expected cost. J Transport Res Board, Transportation Research Record, No. 1696, vol. 2, National Academy Press, p. 26–33.

[9] Frangopol DM, Kong JS, Gharaibeh ES. Reliability-based life-cycle management of highway bridges. J Comput Civil Engng ASCE 2001; 15(1):27–34.

[10] Kong JS, Frangopol DM, Gharaibeh ES. Life prediction of highway bridges with or without preventive maintenance. Proceedings of the 8th ASCE special conference on probabilistic mechanics and structural reliability, Notre Dame, Indiana: University of Notre Dame; 2000. July 24–26, 6 pages on CD-ROM.

[11] Rijkswaterstaat. Workshop on optimal maintenance of structures, October 4–6, 2000, Delft, The Netherlands. Utrecht: Ministry of Transport, Public Works and Water Management, Civil Engineering Division; 2000.

[12] Das PC. Prioritization of bridge maintenance needs. In: Frangopol DM, editor. Case studies in optimal design and maintenance planning of civil infrastructure systems. Reston, Virginia: ASCE; 1999. p. 26–44.

[13] McCall JJ. Maintenance policies for stochastically failing equipment: a survey. Manage Sci 1965;11:493–524.

[14] Barlow RE, Proschan F. Mathematical theory of reliability. New York: Wiley; 1965.

[15] Dekker R. Applications of maintenance optimization models: a review and analysis. Reliability Engng Syst Saf 1996;51: 229–40.

[16] Dekker R, Scarf PA. On the impact of optimisation models in maintenance decision making: the state of the art. Reliability Engng Syst Saf 1998;60:111–9.

[17] van Noortwijk JM, Peerbolte EB. Optimal sand nourishment decisions. J Waterway Port Coastal Ocean Engng 2000;126(1):30–8.

[18] Feller W, An introduction to probability theory and its applications, vol. 1. New York: Wiley; 1950.

[19] Karlin S, Taylor HM. A first course in stochastic processes, 2nd ed. San Diego: Academic Press; 1975.

[20] van Noortwijk JM. Explicit formulas for the variance of discounted life-cycle cost. Reliability Engng Syst Saf 2003;80(2):185–95.

[21] Rackwitz R. Optimizing systematically renewed structures. Reliability Engng Syst Saf 2001;73(3):269–79.

[22] van Noortwijk JM, Klatter HE. Optimal inspection decisions for the block mats of the Eastern-Scheldt barrier. Reliability Engng Syst Saf 1999;65(3):203–11.

[23] van Noortwijk JM. Optimal maintenance decisions on the basis of uncertain failure probabilities. J Qual Maintenance Engng 2000;6(2): 113–22.

<!-- página 15 -->

[24] van Noortwijk JM, Cooke RM, Kok M. A Bayesian failure model based on isotropic deterioration. Eur J Operation Res 1995;82(2):270–82.

[25] van Noortwijk JM, Kok M, Cooke RM. Optimal maintenance decisions for the sea-bed protection of the Eastern-Scheldt barrier. In: Cooke R, Mendel M, Vrijling H, editors. Engineering probabilistic design and maintenance for flood protection. Dordrecht: Kluwer Academic Publishers; 1997. p. 25–56.

[26] van Noortwijk JM, van Gelder PHAJM. Optimal maintenance decisions for berm breakwaters. Struct Saf 1996;18(4):293–309.

[27] Thompson PD, Small EP, Johnson M, Marshall AR. The Pontis bridge management system. Struct Engng Int, IABSE 1998;8(4):303–8.

[28] Hawk H, Small EP. The BRIDGIT bridge management system. Struct Engng Int, IABSE 1998;8(4):309–14.

[29] Frangopol DM. Reliability deterioration and lifetime maintenance cost optimization. Keynote lecture in proceedings of the first international ASRANet colloquium on integrating structural reliability analysis with advanced structural analysis, July 8–10, 2002, Glasgow, Scotland; 2002.

[30] Kong JS, Frangopol DM. Life-cycle reliability-based maintenance cost optimization of deteriorating structures with emphasis on bridges. J Struct Engng 2003;129(6):818–28.

[31] Frangopol DM, Gharaibeh ES, Kong JS, Miyake M. (2000). Optimal network-level bridge maintenance planning based on minimum expected cost, J Transport Res Board, Transportation Research Record 1696, vol. 2, National Academy Press, p. 26–33.

[32] Maunsell Ltd. and Transport Research Laboratory (1998). Strategic review of bridge maintenance costs: Report on 1997/98 Review, Draft Report, The Highways Agency, London.

[33] Klatter HE, van Noortwijk JM, Vrisou van Eck N. Bridge management in the Netherlands; prioritisation based on network performance. In: Casas JR, Frangopol DM, Nowak AS, editors. First international conference on bridge maintenance, safety and management (IABMAS), Barcelona, Spain, 14–17 July 2002. Barcelona: International Center for Numerical Methods in Engineering (CIMNE); 2002.

[34] Frangopol DM, Kong JS. Bridge management based on reliability states and whole life cost: from theory to implementation. In: Chang F-K, editor. Structural health monitoring-the demands and challenges. Boca Raton: CRC Press; 2001. p. 403–19.

[35] Frangopol DM, Kong JS, Gharaibeh ES. Bridge management based on lifetime reliability and whole life costing: the next generation. In: Ryall MJ, Parke GAR, Harding JE, editors. Bridge management four. London: Thomas Telford; 2000. p. 392–9.
