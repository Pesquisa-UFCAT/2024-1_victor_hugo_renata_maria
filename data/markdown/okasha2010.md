<!--
Fonte: okasha2010.pdf (14 páginas)
Okasha & Frangopol (2010). Novel Approach for Multicriteria Optimization of Life-Cycle Preventive and Essential Maintenance of Deteriorating Structures. Journal of Structural Engineering 136(8), 1009-1022. doi:10.1061/(asce)st.1943-541x.0000198
Extração: texto do PDF (pymupdf4llm) corrigido página a página a partir da imagem da página por um modelo de linguagem
(símbolos, equações em LaTeX, tabelas). Figuras: só a legenda. Conferir equações e números contra o PDF antes de citar.
-->

<!-- página 1 -->

# **Novel Approach for Multicriteria Optimization of Life-Cycle Preventive and Essential Maintenance of Deteriorating Structures**

Nader M. Okasha, S.M.ASCE<sup>1</sup>; and Dan M. Frangopol, Dist.M.ASCE<sup>2</sup>

**Abstract:** In this paper, the performance of structures is modeled using lifetime functions. Specifically, the unavailability and redundancy are used as performance indicators, based on which optimum maintenance strategies are sought. Models that reflect the separate or combined effects of essential and preventive maintenance on the unavailability are presented. A novel optimization approach is proposed in which the problem is formulated to provide optimum maintenance strategies with either or both essential and preventive maintenance actions. Genetic algorithms are used to solve this problem. In this paper, multiple essential maintenance types and multiple preventive maintenance types are considered, and regular or irregular preventive maintenance time-intervals are considered. Furthermore, essential maintenance is treated as performance-based, i.e., essential maintenance is only applied when a performance threshold is reached, and an algorithm is proposed for conducting the optimization under uncertainty. Although applicable to any type of structure, the proposed approach is illustrated on a highway bridge example.

**DOI:** 10.1061/(ASCE)ST.1943-541X.0000198

**CE Database subject headings:** Structural systems; Life cycles; Optimization; Maintenance; Deterioration.

**Author keywords:** Structural systems; Lifetime functions; Redundancy; Availability; Lifetime performance; Maintenance; Multiobjective optimization; GA.

## **Introduction**

Economic allocation of funds for maintaining deteriorating civil infrastructure systems requires optimizing the maintenance plans under uncertainty (Frangopol 2010). The key ingredients of the maintenance optimization process are (1) the performance indicators upon which maintenance decisions are made; (2) the list of maintenance options to be optimized; (3) the problem formulation; and (4) the solution technique.

One of the roles that a performance indicator plays in the maintenance planning process is an alarm which is triggered when that performance indicator reaches a specified threshold. It is a tool by which the safety and integrity of the structural system is ensured by preventing the performance indicators from crossing their thresholds. Needless to say, a performance indicator used for the maintenance optimization process is required to be able to accurately represent a specific type of performance and predict its future variations. Frangopol and Okasha (2008) have identified numerous commonly encountered and used life-cycle perfor-

<sup>1</sup>Graduate Research Assistant, Dept. of Civil and Environmental Engineering, ATLSS Center, Lehigh Univ., 117 ATLSS Dr., Bethlehem, PA 18015-4729. E-mail: nao204@lehigh.edu

<sup>2</sup>Professor and the Fazlur R. Khan Endowed Chair of Structural Engineering and Architecture, Dept. of Civil and Environmental Engineering, ATLSS Center, Lehigh Univ., 117 ATLSS Dr., Bethlehem, PA 18015-4729 (corresponding author). E-mail: dan.frangopol@lehigh.edu

Note. This manuscript was submitted on November 11, 2008; approved on February 1, 2010; published online on February 6, 2010. Discussion period open until January 1, 2011; separate discussions must be submitted for individual papers. This paper is part of the *Journal of Structural Engineering*, Vol. 136, No. 8, August 1, 2010. ©ASCE, ISSN 0733-9445/2010/8-1009–1022/$25.00.

mance measures. Examples of these measures and their applications in the literature are: the point-in-time reliability index (Estes and Frangopol 1999; Akgül and Frangopol 2004); the point-in-time probability of system failure and redundancy (Okasha and Frangopol 2010b); the cumulative probability of failure (Mori and Ellingwood 1993, 1994a,b; Enright and Frangopol 1998; Ciampoli and Ellingwood 2002); the lifetime probability of failure or the unavailability (Yang et al. 2006; Okasha and Frangopol 2010a); and the condition and safety indexes (Neves et al. 2006a,b; Liu and Frangopol 2004, 2005a,b; Frangopol and Liu 2007).

Maintenance interventions are scheduled to either delay the occurrence of reaching a performance indicator to its threshold or improve the state of the performance indicator if its threshold is reached. Thus, maintenance types may be categorized into two general groups: preventive maintenance (PM) and essential maintenance (EM) (Kong and Frangopol 2003). PMs are usually time-based, that is, they are applied at prespecified time instants over the life-cycle of the structure. In contrast, EMs are performance-based in that they are applied when some performance indicators reach predefined target values (Liu and Frangopol 2005a).

In general, the optimization of maintenance is a combinatorial optimization problem because the maintenance plan is comprised of various maintenance measures (Miyamoto et al. 2000). The optimization of maintenance considering only performance-based EM reduces the problem to finding the optimum EM option to apply once a performance threshold is reached. Hence, the optimization of continuous design variables is not required and a nonautomated solution of the problem is possible (Estes and Frangopol 1999; Okasha and Frangopol 2010a; Yang et al. 2006). However, including the PM in the optimization introduces the need for continuous design variables to represent the times of application of these PMs into the problem. The solution of this

JOURNAL OF STRUCTURAL ENGINEERING © ASCE / AUGUST 2010 / **1009**

J. Struct. Eng. 2010.136:1009-1022.

<!-- página 2 -->

type of problems requires using a robust optimization algorithm, such as a genetic algorithm (GA) (Goldberg 1989; Deb 2001). Another issue with including PM in optimization is that the best number of PM applications is not known and thus the number of time-of-application design variables to be used is unknown. By considering the uniform application of PM, the problem is simplified. Neves et al. (2006a,b) used two design variables for PM: one for the time of first application of PM and the other for the time-interval between subsequent applications. However, non-uniform time-interval PM strategies have been shown to be more economical than the uniform ones (Frangopol et al. 1997). Attempting to address this issue, coded design variables in a form of numerical strings were used. Liu and Frangopol (2005a) used a real value string with a bit length equal to the designated life-cycle in years. Each bit may take an integer value representing one of the identifiers (ids) given for the considered maintenance options. In fact, the difference between PM and EM is removed; only the effects of each maintenance type on the performance are retained (Liu and Frangopol 2005a). In other words, the time and choice of application of both PM and EM were determined by the optimum coded string found by the optimization problem, and with no regard to any performance threshold. Alternatively, Miyamoto et al. (2000) used binary strings for describing the ids of the maintenance options. The result was a binary matrix in which each row represented the maintenance action at a given year and the binary code in that row represented one of the considered maintenance options. Other similar representations were used (Okasha and Frangopol 2009; Liu and Frangopol 2004, 2005b; Liu et al. 1997; Furuta et al. 2004). However, treating EM as a time-based maintenance (Okasha and Frangopol 2009; Liu and Frangopol 2004, 2005a,b; Miyamoto et al. 2000) may result in obtaining uneconomical solutions, where EM is applied sooner than the time of reaching the threshold of a performance indicator. Neves et al. (2006b) combined EM with PM in the optimization and EM was treated indeed as performance-based. However, only one EM type was used. Thus, the need to optimize the EM was absent. The considered EM type was applied at the time the performance indicator reaches its threshold.

It follows from the above discussion that the need for an efficient problem formulation for maintenance optimization is evident. To overcome the shortcomings of the aforementioned approaches, this problem formulation is required to be able to: (1) handle regular and irregular time-interval PM; (2) handle EM only, PM only, and both EM and PM combined; (3) handle multiple PM types and multiple EM types; and (4) treat EM as performance-based. It is the objective of this paper to propose such an approach. Performance indicators used are the unavailability and redundancy and they are calculated based on lifetime functions. Models that reflect the separate and combined effects of EM and PM on these performance indicators are presented.

## Performance Measures

The performance of structures may be measured by various indicators. Crucial decisions are made based on the results provided by these indicators. Thus, the accurate representation and prediction of the performance by its indicator is evidently essential. However, uncertainty in quantifying the lifetime structural performance is inevitably encountered. Probabilistic methods are used to handle these uncertainties appropriately (Frangopol and Okasha 2008). Closed-form solutions are not available for most life-cycle probabilistic performance indicators. Instead, simulation or iterative methods are required to evaluate this performance indicator. In addition, life-cycle performance evaluation requires evaluating the performance indicator at many time increments over the lifetime of the structure. Furthermore, the optimization of maintenance is a combinatorial optimization that requires iterative solution techniques. Thus, for optimization of maintenance, the life-cycle performance needs to be evaluated many times. Therefore, the optimization of maintenance based on probabilistic life-cycle performance indicators is usually computationally very expensive.

Lifetime functions, however, offer the ability to rapidly evaluate the life-cycle performance through available closed-form solutions. Hence, the use of lifetime functions in automated maintenance optimization problems significantly reduces the computational time required. In fact, the efficiency and convenience of using lifetime functions even in nonautomated maintenance optimization has already been demonstrated (Yang et al. 2006; Okasha and Frangopol 2010a).

Lifetime functions may be used to characterize the lifetime reliability of existing structures. According to these functions, the time to failure of components or systems is treated as a random variable. The time to failure is defined as the time elapsing from the time the component is put into operation until it fails for the first time (Hoyland and Rausand 1994). An appropriate distribution is assigned to the probability density function (PDF) of the time to failure by regression of statistical data of ages of similar components or systems. The Weibull distribution is usually the best fit distribution to ages of decaying components or systems. The PDF of the Weibull distribution is defined as (Leemis 1995)

$$f(t) = \begin{cases} \kappa\lambda(\lambda t)^{\kappa-1}e^{-(\lambda t)^{\kappa}} & \text{for } t > 0 \\ 0 & \text{otherwise} \end{cases} \tag{1}$$

where λ=scale parameter and κ=shape parameter. Based on the time to failure PDF, several lifetime function representations can be derived. Among these representations are the availability and redundancy (Okasha and Frangopol 2010a).

### Availability

A component is available at time $t$ if it is functioning at this time. The event that a component survives (i.e., does not fail) up to time $t$ is in fact the same event that the component is available at time $t$. Therefore, the probability of survival of a component from the time it is put in service until time $t$ is the same as the probability that the component is available at time $t$. Availability is, therefore, an alternative way to quantifying the reliability of components and systems. In fact, the survivor function (or reliability function) of a nonrepairable component is a special case of its availability. They both differ only when the component is repaired or replaced (Klaassen and van Peppen 1989). The availability $A(t)$ can be calculated by integration of the PDF of the time to failure. The availability of a component without maintenance can be calculated by

$$A(t) = P(T > t) = \int_{t}^{\infty} f(u)du \tag{2}$$

where $T$=time to failure and $f(t)$ is its PDF. The unavailability of a component, $An(t)=1-A(t)$, is the probability that it has failed

<!-- página 3 -->

# Effect of Essential Maintenance

before time $t$ and thus it is unavailable (not functioning) at time $t$ (Ang and Tang 1984).

As will be shown next, the choice of availability (or unavailability) as a performance measure offers great flexibility in incorporating the effects of any type of maintenance. Whether this effect is improving the state of the availability or slowing the rate by which it deteriorates, an appropriate model is presented. In general, information regarding the effects of maintenance on any performance indicator is hard to obtain. Once obtained, this information can be easily used in the availability models. Until then, appropriate assumptions based on engineering judgment are resorted to.

The application of EM typically results in restoring the performance indicator to its value at some time prior to the application of EM. Let TEM={Tem$_1$,Tem$_2$,...,Tem$_n$} be the times at which $n$ EM actions are applied to a component. Let also Tem$_0$=0 and Tem$_{n+1}$=∞. Application of EM action $i$ restores the availability to its value at a point in time $Pn_i$ prior to the time Tem$_i$. The availability of a component can thus be calculated by

$$A^*(t) = A\left(t - \sum_{i=1}^{k} Pn_i\right) \quad \text{Tem}_k \leq t < \text{Tem}_{k+1} \tag{3}$$

where $A^*(t)$=updated availability after the application of maintenance. The value of $Pn_i$ depends on the improvement that EM action $i$ brings to the availability. However, if the EM applications require replacing the component, it is rational to restore the availability to its original value at the time of each EM application and can thus be calculated by (Okasha and Frangopol 2010a)

$$A^*(t) = A(t - \text{Tem}_k) \quad \text{Tem}_k \leq t < \text{Tem}_{k+1} \tag{4}$$

# Effect of Preventive Maintenance

The application of PM typically results in the reduction of the deterioration rate (Neves et al. 2006b). This effect is manifested in the availability as follows. Let TPM={Tpm$_1$,Tpm$_2$,...,Tpm$_q$} be the times at which $q$ PM actions are applied to a component. Let also Tpm$_0$=0 and Tpm$_{q+1}$=∞. Application of PM action $j$ restores the rate of change in the availability to its rate at a point in time $Rn_j$ prior to the time Tpm$_j$. The availability of a component can thus be calculated by

$$A^*(t) = \begin{cases} A(t) & \text{if } t < \text{Tpm}_1 \\ A(t - F_i) \cdot \prod_{j=1}^{i} \dfrac{A(\text{Tpm}_j - F_{j-1})}{A(\text{Tpm}_j - F_j)} & \text{if } \text{Tpm}_i \leq t < \text{Tpm}_{i+1}, \ i \geq 1 \end{cases} \tag{5}$$

where Tpm$_j$=time of application of the $j$th PM, and

$$F_j = \begin{cases} 0 & \text{if } j = 0 \\ \min\left(\sum_{x=1}^{j} Rn_x, \text{Tpm}_j\right) & \text{if } j > 0 \end{cases} \tag{6}$$

Clearly, the effect of a given type of PM on the availability is determined by the value of $Rn_x$. If the application of PM reduces the rate of change in the availability to its original value, the availability of a component can be calculated by

$$A^*(t) = \begin{cases} A(t) & \text{if } t < \text{Tpm}_1 \\ A(t - \text{Tpm}_i) \cdot \prod_{j=1}^{i} A(\text{Tpm}_j - \text{Tpm}_{j-1}) & \text{if } \text{Tpm}_i \leq t < \text{Tpm}_{i+1}, \ i \geq 1 \end{cases} \tag{7}$$

Figs. 1(a) and 1(b) show the effects of EM and PM, respectively, on the unavailability of a component with a lifetime Weibull distribution and parameters κ=5 and λ=1/200 under two maintenance applications over its lifetime. The first maintenance application is at the year 20 and the second is at the year 40. For both PM applications in Fig. 1(b), $Rn_i$=$Rn$ and it is clear that increasing $Rn$ reduces the slope of the unavailability curve.

# Effect of Combined Essential and Preventive Maintenance

Calculation of availability considering the application of both EM and PM depends on the sequence of application of these maintenance types. At time $t$, if EM action $k$ was the most recent maintenance type applied, Eq. (3) or Eq. (4) is used. However, if PM action $i$ was the most recent maintenance type applied and EM actions were applied up to that time ending by EM action $k$, where the PM action following EM action $k$ is PM action $a$, the availability can be calculated by

$$A^*(t) = A(t - \text{Tem}_k - F_i) \cdot \prod_{j=a}^{i} \dfrac{A(\text{Tpm}_j - F_{j-1})}{A(\text{Tpm}_j - F_j)}$$

$$\text{if } \text{Tpm}_i \leq t < \text{Tpm}_{i+1}; \ \text{Tem}_k < \text{Tpm}_a$$

$$\text{and } \text{Tpm}_i > \text{Tpm}_a \tag{8}$$

if the PM actions restore the rate of change in the availability to its rate at a point in time $Rn_x$ prior to the time of application of each PM action $x$ and EM restores the availability to its original value, or

$$A^*(t) = A(t - \text{Tem}_k - \text{Tpm}_i) \cdot \prod_{j=a}^{i} A(\text{Tpm}_j - \text{Tpm}_{j-1})$$

$$\text{if } \text{Tpm}_i \leq t < \text{Tpm}_{i+1}; \ \text{Tem}_k < \text{Tpm}_a$$

$$\text{and } \text{Tpm}_i > \text{Tpm}_a \tag{9}$$

<!-- página 4 -->

> **Fig. 1.** Effect of two actions (a) EM; (b) PM at the years 20 and 40 on the unavailability of a component with a lifetime Weibull distribution and parameters κ=5 and λ=1/200

if the application of PM reduces the rate of change in the availability to its original value. If EM action $k$ restores the availability to its value at a prior point in time $Pn_k$ prior to the time Tem$_k$, the term Tem$_k$ is replaced with $\Sigma_{y=1}^{k}Pn_y$ in Eqs. (8) and (9). It is also noted that Eqs. (8) and (9) assume that PM application $i$ is followed by a PM application and not an EM application (i.e., Tpm$_{i+1}$<Tem$_{k+1}$). However, if application $i$ is rather followed by an EM application, the equations are only modified by replacing Tpm$_{i+1}$<Tem$_{k+1}$ in the inequality conditions.

### Redundancy

Redundancy is an additional type of structural performance that is defined as a measure of the warning available prior to system collapse. The redundancy of a system can be directly calculated from its unavailability and the unavailability of its weakest component as (Okasha and Frangopol 2010a)

$$RI^* = \frac{An_{wc}^*(t) - An_s^*(t)}{An_s^*(t)} \tag{10}$$

where $An_s^*(t)$ and $An_{wc}^*(t)$=unavailability of the system and weakest component, respectively.

For the purpose of reliability analysis, complex systems are usually decomposed into functional entities made of components or subsystems. By combining the appropriate series and parallel branches (subsystems) of a model systematically, the entire system can be reduced to one single equivalent component. The reliability of this equivalent component is the reliability of the system. Such a procedure is known as the network reduction method (Ramakumar 1993). In fact, this method has successfully been applied by Yang et al. (2006) in analyzing structures using lifetime functions. The minimal cut set method is also useful for system reliability calculations (Hoyland and Rausand 1994). This method has also been applied by Okasha and Frangopol (2010a) and it is used in this study.

## Colorado Bridge E-17-AH

In this study, the proposed maintenance optimization approach is applied to the superstructure of the Colorado Bridge E-17-AH. A detailed description of this bridge can be found in Estes (1997). The bridge has three simple spans of equal length. The reinforced concrete slab is supported by nine standard-rolled, compact, and noncomposite steel girders (Estes 1997).

Weibull distributions are adopted to model the lifetimes of the components of this bridge. The parameters of these distributions are based on the best fit of the data summarized in (Maunsell Ltd. 1999). The shape and scale parameters, κ and λ, respectively, are κ=2.37 and λ=0.0077 for the deck, and κ=2.86 and λ=0.0106 for the girders. This bridge was examined in Okasha and Frangopol (2010a) for EM only. However, herein, both EM and PM are considered, separately and combined for this bridge.

Multigirder bridges are modeled in system reliability analyses as combinations of series and parallel components (Akgül and Frangopol 2004; Estes and Frangopol 1999). For the bridge being analyzed, the system failure is assumed to occur by the failure of any three adjacent girders or the deck. It was found that including the deck in the redundancy calculations completely undermines the redundancy offered to the system by the girders. This is because the deck is connected to the rest of the components in the assumed system model in series and hence its failure triggers the failure of the system (Frangopol and Okasha 2009). Therefore, the deck was excluded from the system model in the redundancy calculations. However, it was part of the system model for the availability calculations.

Four EM options are considered and they and their associated costs are (Estes and Frangopol 1999): (1) replace superstructure ($487,100); (2) replace exterior girders and deck ($341,800); (3) replace exterior girders ($229,200); and (4) replace deck ($225,600). For PM, silane treatment is considered for maintaining the deck and repainting is considered for maintaining the girders. The effect of both these PM types is assumed to restore the rate of change in the unavailability to its original value. The cost of silane treatment for the entire deck is assumed as $50,000 and the cost of repainting all girders is assumed as $100,000.

## Optimization of Maintenance Considering EM Only

EM usually has a significant effect on the bridge performance, although extremely expensive, in part due to the high user costs associated with bridge partial or total closure during application of this type of maintenance (Neves et al. 2006b). PM is associated with smaller impacts on performance, but closure of the bridge is not usually necessary, or can be limited to short time periods, resulting in lower user costs (Neves et al. 2006b). Ideally, the downtime of the bridge due to EM and the user costs arising due to this downtime should be estimated and accounted for in the optimization process. In fact, their effect on the results can be significant (Frangopol et al. 2001; Liu and Frangopol 2005b). In this paper, these issues are not considered. However, having the means and appropriate data to quantify them, they can be straightforwardly introduced into the approach presented herein.

The general goal in performance-based EM optimization is finding the appropriate EM option to apply once a performance threshold is reached. Considering one EM option transforms the optimization problem to a straightforward analysis problem (i.e., there is no need to search for an optimum solution). However, considering multiple EM options creates a discrete combinatorial

<!-- página 5 -->

# Alternative method for evaluating EM optimization: EMO2 algorithm

optimization problem. The optimization aims to select one of the available EM options when a performance threshold is reached. If multiple performance indicators, each with a threshold, are used in the optimization process, the optimum selection of EM takes place each time any threshold is reached. Performance thresholds that are reached and not reached during the service life in the optimum maintenance plan are called active and inactive thresholds, respectively. An inactive threshold implies that the worst value its performance indicator reached is better than the value of this threshold. A performance threshold becomes inactive either if none of the performance thresholds considered in the optimization are reached or if the other performance thresholds are always reached before this inactive threshold.

A commonly used EM optimization method states that the optimum EM option to apply at a time a performance threshold is reached is the one providing the lowest present cost per year of increase in service life. This method was proposed by Estes and Frangopol (1999), used in Yang et al. (2006) and extended for multiple performance measures in Okasha and Frangopol (2010a), where a detailed algorithm is presented. In this study, this method is denoted by EMO1.

Method EMO1 relies on the embedded assumption that the service life extension offered by an EM option is the same regardless of when it is applied. For example, if an EM option that requires replacing a given part of a structure extends the service life for a given number of years, the method assumes that if this EM option is applied again after the end of the effect period of the first application it will provide the same service life extension as the first application. However, this assumption may not always be true. In the given example, the other parts of the structure are naturally deteriorating perhaps at a time-varying rate.

An alternative method compares the total cost of all EM scenarios required to provide a prespecified service life from start to end by an event-tree analysis. The resulting large number of branches (i.e., EM scenarios) to analyze can become a computational burden for solving the problem even for a limited number of EM options. The difficulty in programming this method stems from the fact that neither the number of branches nor the length of each branch is known before the end of the analysis. Therefore, the following algorithm is proposed for efficiently performing the event-tree analysis for EM optimization and is denoted herein as EMO2.

The goal of the EMO2 algorithm is to identify the ids and times of applications of the EM options in all scenarios $M(i,j)$ and $T(i,j)$, respectively, where $M(i,j)$ represents the id of the maintenance option to use at the $j$th application in the $i$th maintenance scenario and $T(i,j)$ represents its time of application. In addition, the optimum maintenance scenario $M_{opt}$ and its associated optimum life-cycle maintenance cost LCC$_{opt}$ are identified. The method is supported with checkpoints that predict and terminate the continuation of nonoptimum branches and prevent creating new branches known a priori to be nonoptimum. The first checkpoint compares the partial life-cycle cost (LCC) up to the $j$th application of the $i$th maintenance scenario, LCC($i,j$), with the minimum (optimum) LCC value found up to that point in the optimization process, LCC$_{opt}$. LCC($i,j$) is calculated as

$$\text{LCC}(i,j) = \sum_{y=1}^{j} \frac{C[M(i,y)]}{(1+\nu)^{T(i,y)}} \tag{11}$$

where $C[M(i,y)]$=cost of the $y$th maintenance application of the $i$th EM scenario; $T(i,y)$ is its time of application; and $\nu$=discount rate of money (2% in this study). The second check-

**Table 1.** Results of the EMO2 Method Example for the Colorado Bridge E-17-AH

| Maintenance scenario | EM options | Time of application (years) | LCC ($) |
|---|---|---|---|
| 1 | [1 1] | [18.6 37.3] | 569,740 |
| 2 | [1 2] | [18.6 37.3] | 500,320 |
| 3 | [1 4] | [18.6 37.3] | 444,800 |
| 4 | [2 1] | [18.6 36.1] | 474,800 |
| 5 | [2 2 1] | [18.6 36.1 45.5] | 601,550 |
| 6 | [2 2 2] | [18.6 36.1 45.5] | 542,540 |
| 7 | [2 2 4] | [18.6 36.1 45.5] | 495,340 |
| 8 | [2 4 1] | [18.6 36.1 45.1] | 546,280 |
| 9 | [2 4 2] | [18.6 36.1 45.1] | 486,790 |
| **10ᵃ** | **[4 1]** | **[18.6 35.9]** | **395,350** |
| 11 | [4 2 1] | [18.6 35.9 45.4] | 522,210 |
| 12 | [4 2 2] | [18.6 35.9 45.4] | 463,080 |
| 13 | [4 2 4] | [18.6 35.9 45.4] | 415,790 |
| 14 | [4 4 1] | [18.6 35.9 44.0] | 470,710 |
| 15 | [4 4 2] | [18.6 35.9 44.0] | 409,910 |

ᵃOptimum solution.

point ensures that the service life extension provided by the application of any given EM application is larger than a minimum tolerance TOL. The steps of the algorithm are the following:

1. *INITIALIZE:* sort the EM options in the order of increasing cost, and assign them a ranking number $r$ accordingly, where $r=1,2,\ldots,n$, and $n$=number of considered EM options. Set $i=1$, $j=0$, $k=1$, $T(1,0)=0$, LCC$(1,0)=0$, $t=0$. Assign a "very large" value to LCC$_{opt}$.

2. *INCREMENT* $t$ and analyze the performance at this increment.

3. If a performance threshold is reached, go to Step 5.

4. If $t\geq$ specified service life, go to Step 11; otherwise go to Step 2.

5. $j=j+1$. $k=1$, $M(i,j)=k$. $T(i,j)=t$.

6. *CHECKPOINT* 1: if $T(i,j)-T(i,j-1)\geq$ TOL continue; otherwise go to Step 9.

7. *CHECKPOINT* 2: calculate LCC($i,j$). If LCC($i,j$) > LCC$_{opt}$ go to Step 12; otherwise apply EM option with $r=k$ at time $t$; then go to Step 2.

8. If $k=n$ continue; otherwise $k=k+1$, $t=T(i,j)$; then go to Step 7.

9. $j=j-1$.

10. If $j=0$ STOP; otherwise $k=M(i,j)$; then go to Step 8.

11. If LCC($i,j$)<LCC$_{opt}$; then LCC$_{opt}$=LCC($i,j$), $M_{opt}=i$.

12. If $j=0$ STOP; otherwise $k=M(i,j)$, $i=i+1$, $M(i,z)=M(i-1,z)$, $T(i,z)=T(i-1,z)$, where $z=1,2,\ldots j$; then go to Step 8.

This algorithm is illustrated in the following example. An unavailability threshold is specified as $10^{-2}$ for the Colorado Bridge E-17-AH and the service life is specified as 50 years. The algorithm of EMO2 is implemented and the results are shown in Table 1. It is noted that the application of EM option 3 (i.e., replace the exterior girders) extends the service life for a very short amount of time and therefore it always fails at CHECKPOINT 1 (where TOL=2 years is considered). Scenario 10 provides the solution with the lowest total LCC and thus it is the optimum maintenance strategy.

<!-- página 6 -->

> **Fig. 2.** Effect of the unavailability and redundancy thresholds on the life-cycle cost for optimum EM using (a) method EMO1; (b) method EMO2

Needless to say, one of the deciding factors in determining the optimum strategy is the values of the performance thresholds. For any set of performance thresholds, an optimum maintenance strategy exists. Standard or codified performance thresholds do not exist thus far. Therefore, it may be desired to understand the interaction among the performance thresholds and the LCC required for a maintenance strategy that maintains these thresholds. Neves et al. (2006a) treated the performance threshold as a design variable in a multiobjective optimization problem solved by GA.

> **Fig. 3.** (a) Schedules of maintenance application; (b) history profiles for the cumulative maintenance cost for the selected solutions of EM

However, "all feasible solutions are nondominated and the only role played by GA is finding a set of solutions as well distributed (i.e., a set of evenly distributed solutions in the objective space) as possible" (Neves et al. 2006a). In this example, the effect of the performance thresholds on the LCC is analyzed by enumaratively varying the values of the thresholds of unavailability and redundancy, and performing the EM optimization to find the corresponding LCC associated with the optimum maintenance solution. Both EM optimization methods EMO1 and EMO2 are used separately. The service life of the bridge is now considered as 75 years.

Figs. 2(a) and 2(b) show the results obtained by methods EMO1 and EMO2, respectively. Fig. 2(b) shows the consistency in method EMO2 in that by improving the unavailability and/or the redundancy threshold the associated LCC either increases or remains the same. The increase in LCC with improving both the unavailability and redundancy implies that both their thresholds are active. Improving either threshold with same LCC indicates that the improved threshold is inactive. However, numerous spikes and regions in Fig. 2(a) with higher LCC than their corresponding regions in Fig. 2(b) show that method EMO1 can yield

**Table 2.** Representative EM Solutions Using EMO2 for the Colorado Bridge E-17-AH

| Solution | Unavailability threshold ($An_{th}$) | Redundancy threshold ($RI_{th}$) | Maximum unavailability ($An_{max}$) | Minimum redundancy ($RI_{min}$) | LCC ($) |
|---|---|---|---|---|---|
| A1 | $10^{-1.00}$ | $10^{1.00}$ | $10^{-1.06}$ | $10^{1.00}$ | 199,410 |
| B1 | $10^{-2.00}$ | $10^{2.00}$ | $10^{-2.00}$ | $10^{2.00}$ | 657,880 |
| C1 | $10^{-3.00}$ | $10^{4.00}$ | $10^{-3.00}$ | $10^{4.01}$ | 1,830,100 |

<!-- página 7 -->

**Fig. 4.** History profiles of unavailability for selected EM solutions: (a) Solution A1; (b) Solution B1; and (c) Solution C1

**Fig. 5.** History profiles of redundancy for selected EM solutions: (a) Solution A1; (b) Solution B1; and (c) Solution C1

## Multiobjective Optimization of Maintenance Considering PM Only

solutions that are not in fact optimum. Nevertheless, most of the surface in Fig. 2(a) found by EMO1 appears to be the same as the corresponding parts of the surface in Fig. 2(b) found by EMO2. Therefore, method EMO1 has the ability to provide optimum solutions in most cases. However, EMO2 is always more accurate and will be used for the rest of this study.

Three maintenance solutions, A1, B1, and C1, obtained by method EMO2 are examined. Table 2 shows the unavailability $An_{th}$ and redundancy $RI_{th}$ thresholds for these solutions along with the maximum unavailability $An_{max}$ and minimum redundancy $RI_{min}$ achieved throughout the 75 years of service life and the associated LCC. It can be observed in the values of this table that the performance threshold may not be reached (inactive threshold) and the worst value for the performance indicator in such case is better than its threshold. Figs. 3(a) and 3(b) show the schedules of maintenance application and history profiles for the cumulative maintenance cost for the selected solutions, respectively. It can be seen that EM option 3 (i.e., replace the exterior girders) is not used in the three solutions since this EM option does not extend the service life for a significant amount of time. Figs. 4 and 5 show the history profiles of the selected EM solutions for the unavailability and redundancy, respectively.

By aiming to find an optimum maintenance solution considering only PM actions, two questions are posed: what are the optimum times of application of each PM type and what is the optimum number of PM applications of each type? Treating the times of application of PM as design variables answers the first question, but the second question is posed again as: what is the number of design variables to use for the optimum times of PM application? In this study, this question is answered by using an integer design variable that represents the optimum number of PM applications. This integer design variable takes values from 0 to $n_p$, where $n_p$=number of time-of-application design variables for the given PM type considered in the problem, which should be the maximum desired number of applications for this PM type. This implies that at each design point, a number of the time-of-application design variables are inactive, i.e., have no contribution to the evaluation of the objective functions. Instead of performing the optimization multiple times, where each time a different number of time-of-application design variables is used, and at the end the optimum solution is found, the combinatorial problem is performed at once using the number of applications integer design variable. To the best of our knowledge, this is the first time an optimization problem is solved by activation and

<!-- página 8 -->

> **Fig. 6.** (a) Three-dimensional Pareto-optimal set of PM; [(b)–(d)] its projections in the bidimensional space

deactivation of design variables based on the values of other design variables. The robustness of GAs provides a unique ability to solve such a cumbersome optimization problem.

The PM optimization is based on two structural performance indicators, the lifetime unavailability and lifetime redundancy. These performance indicators are introduced in the optimization process as criteria. The goal of the optimization is to improve the worst values reached for these performance indicators. In other words, one objective is to minimize the maximum (worst) value reached for the unavailability throughout the service life $An_{max}$ and the other objective is to maximize the minimum (worst) value reached for the redundancy throughout the service life $RI_{min}$. The third objective is to minimize the LCC required to apply maintenance activities resulting in achieving these values of $An_{max}$ and $RI_{min}$. The service life of the structure is considered as 75 years.

Two PM types are considered in this study: silane treatment and girder repainting. A maximum of 10 applications of each PM type is allowed. Therefore, 20 continuous time-of-application design variables are used, namely 10 for the time of silane treatments of the deck $Td_i$ ($i$=1,2, ... ,10), and 10 for the time of girder repaintings $Tg_j$ ($j$=1,2, ... ,10). In addition, two number-of-applications integer design variables are used; one for the number of applications of the silane treatment for the deck $Nd$ (where $Nd$=0,1,2, ... ,10), and one for the number of applications of the girder repaintings $Ng$ (where $Ng$=0,1,2, ... ,10).

It is desired not to apply maintenance anytime in the first or last 2 years of the service life of the structure. Thus, the application time design variables are only allowed to vary from the year 2 to the year 73. In addition, a minimum time span of 2 years

between any two consecutive maintenance applications of the same type is required. Accordingly, the formulation of the problem is stated as follows.

*Find: $Td_i$, $Nd$, $Tg_j$, $Ng$.*

*To achieve the following three objectives*

$$\text{Minimize } An_{max} \tag{12a}$$

$$\text{Maximize } RI_{min} \tag{12b}$$

$$\text{Minimize LCC} \tag{12c}$$

*Subject to the constraints*

$$2 \leq Td_i \leq 73 \tag{12d}$$

$$2 \leq Tg_j \leq 73 \tag{12e}$$

$$Td_i - Td_{i-1} \geq 2 \tag{12f}$$

**Table 3.** Selected Representative PM Pareto-Optimal Solutions for the Colorado Bridge E-17-AH

| Solution | Maximum unavailability ($An_{max}$) | Minimum redundancy ($RI_{min}$) | LCC ($) |
|---|---|---|---|
| A2 | $10^{-1.00}$ | $10^{0.67}$ | 76,720 |
| B2 | $10^{-1.22}$ | $10^{3.60}$ | 561,913 |
| C2 | $10^{-1.99}$ | $10^{3.40}$ | 734,588 |

<!-- página 9 -->

> **Fig. 7.** (a) Schedules of maintenance application; (b) history profiles for the cumulative maintenance cost for the selected solutions of PM

> **Fig. 8.** History profiles of unavailability for selected PM solutions: (a) Solution A2; (b) Solution B2; and (c) Solution C2

> **Fig. 9.** History profiles of redundancy for selected PM solutions: (a) Solution A2; (b) Solution B2; and (c) Solution C2

$$Tg_j - Tg_{j-1} \geq 2 \tag{12g}$$

$$Nd = \{0,1,2,\ldots,10\} \tag{12h}$$

$$Ng = \{0,1,2,\ldots,10\} \tag{12i}$$

where $i,j=1,2,\ldots,10$.

An advanced GA called nondominated sorting GA with controlled elitisms, NSGA-II, has gained much popularity since its appearance (Deb et al. 2002; Deb 2001). The NSGA-II algorithm for multiobjective optimization is used to solve the above problem. The resulting three-dimensional Pareto-optimal set of the optimization problem is shown in Fig. 6(a). Projections of this set in the bidimensional space are also presented in Figs. 6(b–d). Three representative solutions (A2, B2, and C2) selected from the Pareto-optimal set are also shown on the figure. The interaction among the three criteria indicates that improving either $An_{\max}$ or $RI_{\min}$ using PM does not always improve the other. In general, the increase in LCC is relatively higher with improving $An_{\max}$ than with improving $RI_{\min}$ (i.e., it is less expensive to improve $RI_{\min}$ than to improve $An_{\max}$). Solutions between A2 and B2 improve immensely with respect to $RI_{\min}$ with little or no improvement in $An_{\max}$. On the other hand, solutions between B2 and C2 improve greatly in $An_{\max}$ with little or no improvement in $RI_{\min}$. This can be justified as follows.

On one hand, the deck has more relative importance to the system unavailability model than the girders since it is connected separately to the system in series. Therefore, improving the gird-

<!-- página 10 -->

> **Fig. 10.** (a) Three-dimensional Pareto-optimal set of combined EM and PM; [(b)–(d)] its projections in the bidimensional space

ers by repainting them provides little improvement to $An_{\max}$ while improving the deck by the silane treatment greatly improves $An_{\max}$. On the other hand, the deck is removed from the redundancy system model. Thus, repainting the girders greatly improves $RI_{\min}$, while silane treatment does not affect $RI_{\min}$. Accordingly, by moving from Solution A2 to Solution B2, more girder repaintings are applied and thus $RI_{\min}$ is relatively improved much more rapidly than $An_{\max}$ is. Furthermore, by moving from Solution B2 to Solution C2, more silane treatments are applied and thus $An_{\max}$ is relatively improved rapidly while $RI_{\min}$ is not improved.

Table 3 shows the values of the obtained objective functions for the selected solutions A2, B2, and C2. Clearly, Solution B2 has better $RI_{\min}$ than Solution C2 but worse $An_{\max}$. Both solutions B2 and C2 are better than A2 in availability and redundancy. Figs. 7(a) and 7(b) show the schedules of maintenance application and history profiles for the cumulative maintenance cost for the selected solutions of PM, respectively. In general, it is evident in the figure that improving $An_{\max}$ requires additional and more frequent PM applications associated with a higher LCC. Although, the cost of girder repainting is twice the cost of silane treatment, Solution B2 has used the 10 allowed girder repaintings while using only two silane treatments. Solution C2 applies also 10 girder repaintings, in addition to 10 silane treatments. Since silane treatment does not improve $RI_{\min}$ and the times of girder repaintings are different in Solution B2 from C2, $RI_{\min}$ in Solution C2 is lower than in Solution B2. However, $An_{\max}$ is better.

Figs. 8 and 9 show the history profiles of the selected PM solutions for the unavailability and redundancy, respectively. It is clear in the figures how the application of silane treatment changes the slope (rate of change) of the unavailability curves and how the girder repaintings change the slope of the redundancy curves. For instance, Solution A2 shows that the change in slope of its redundancy curve due to the silane treatment is insignificant [see the effects of the first PM application on the redundancy in Fig. 9(a)]. The change in slope of its unavailability curve, however, is evident [see Fig. 8(a)]. On the other hand, Solution B2 shows that the change in slope of its unavailability curve due to

**Table 4.** Selected Representative Combined PM and EM Pareto-Optimal Solutions for the Colorado Bridge E-17-AH

| Solution | Unavailability threshold ($An_{th}$) | Redundancy threshold ($RI_{th}$) | Maximum unavailability ($An_{\max}$) | Minimum redundancy ($RI_{\min}$) | LCC ($) |
|---|---|---|---|---|---|
| A3 | $10^{-1.00}$ | $10^{1.00}$ | $10^{-1.00}$ | $10^{1.01}$ | 106,764 |
| B3 | $10^{-1.39}$ | $10^{3.53}$ | $10^{-1.82}$ | $10^{3.53}$ | 761,464 |
| C3 | $10^{-2.64}$ | $10^{4.00}$ | $10^{-2.64}$ | $10^{4.73}$ | 1,533,273 |
| D3 | $10^{-3.00}$ | $10^{4.00}$ | $10^{-3.00}$ | $10^{4.00}$ | 1,863,516 |

<!-- página 11 -->

> **Fig. 11.** (a) Schedules of maintenance application; (b) history profiles for the cumulative maintenance cost for the selected solutions of combined EM and PM

the girder repaintings is very small [see Fig. 8(b)]. The change in slope of its redundancy curve, however, is clear [see Fig. 9(b)].

## Multiobjective Optimization of Maintenance Considering Combined EM and PM

The 22 design variables used in the PM optimization above are used in this problem formulation. Thus the GA search is directed to find optimal values for the PM. It is desired to keep the treatment of EM as performance-based (i.e., only apply EM when a performance threshold is reached). In this case, it is difficult to use a GA search to obtain the optimum EM solution since the number of times a threshold will be reached depends on the chosen EM options throughout the service life. In fact, a GA search is not needed for EM optimization. Either method EMO1 or EMO2 can be used. Both methods can easily incorporate the effects of applying a given set of PM options. While evaluating the service life extension due to an EM application using either method, the further extension provided by additional PM applied during that extension period is taken into account. Method EMO2 is used here.

Accordingly, for a given set of performance thresholds and set of PM applications, an optimum EM solution can be found using EMO2. Thus, combined maintenance (CM) considering both EM and PM can be optimized with NSGA-II by using the aforementioned design variables and finding the optimum EM options using EMO2 for each design point (i.e., nesting EMO2 into NSGA-II). In other words, the maintenance optimization is performed on two levels: global (NSGA-II) and local (EMO2). Each time the global design variables are provided, a local optimization (EMO2) takes place to find the optimum set of EM applications, given the presence of the PM applications and satisfying the given thresholds. The local optimization is performed during the objective functions evaluation of each global optimization design solution. Based on the results of the local optimization, the worst values of the performance indicators throughout the service life of the structure and the LCC are returned to the global optimization as values of the considered objective functions. The global optimization is thus able to find the best set of PM applications to fulfill the thresholds, provided that EM applications may also be applied and their set is determined by the local optimization.

As mentioned above, a set of performance thresholds is required as an input to this process. With the lack of standard thresholds, the effects of the unavailability and redundancy thresholds on the values of the objective functions is desired to be examined. This can be realized in a combinatorial manner as previously achieved with the EM optimization where for each set of performance thresholds the GA optimization is performed. However, the computational cost required is clearly very high. Alternatively, these thresholds are treated as design variables. Although each threshold set is associated with an optimal solution, the goal of treating them as design variables in the GA optimization is to find a well distributed set of optimal solutions (Neves et al. 2006a). Therefore, two more continuous design variables are used for the unavailability threshold $An_{\text{th}}$ and the redundancy threshold $RI_{\text{th}}$.

The threshold for the unavailability is desired to range between $10^{-1}$ and $10^{-3}$ and the threshold for the redundancy is desired to range between $10^1$ and $10^4$. However, in order to reduce the search space, the redundancy threshold $RI_{\text{th}}$ design variable is replaced by the auxiliary design variable $x_r$ which takes values from 0.1 to 0.4. The redundancy threshold is related to the variable $x_r$ by

$$RI_{\text{th}} = 10^{(10x_r)} \tag{13}$$

In addition, a minimum time span of 2 years between any two consecutive maintenance applications applied to the same component is required. This includes EM and/or PM types. For instance, the time span between a deck replacement and a subsequent deck replacement or silane treatment should not be less than 2 years. Accordingly, the formulation of the problem is stated as follows.

*Find*: $An_{\text{th}}$, $x_r$, $Td_i$, $Nd$, $Tg_j$, $Ng$.

*To achieve the following three objectives*

$$\text{Minimize } An_{\max} \tag{14a}$$

$$\text{Maximize } RI_{\min} \tag{14b}$$

$$\text{Minimize LCC} \tag{14c}$$

*Subject to the constraints*

$$10^{-1} \leq An_{\text{th}} \leq 10^{-3} \tag{14d}$$

$$0.1 \leq x_r \leq 0.4 \tag{14e}$$

$$2 \leq Tm_i \leq 73 \tag{14f}$$

$$Tm_i - Tm_{i-1} \geq 2 \tag{14g}$$

<!-- página 12 -->

> **Fig. 12.** History profiles of unavailability for the selected combined EM and PM (CM) solutions: (a) Solution A3; (b) Solution B3; (c) Solution C3; and (d) Solution D3

$$Nd = \{0,1,2,\ldots,10\} \tag{14h}$$

$$Ng = \{0,1,2,\ldots,10\} \tag{14i}$$

where $Tm_i$ =time of application of the $i$th maintenance action applied to a given component and $i,j=1,2,\ldots,10$.

The resulting three-dimensional Pareto-optimal set is shown in Fig. 10(a). Projections of this set in the bidimensional space are also presented in Figs. 10(b–d). Four representative solutions (A3, B3, C3, and D3) selected from the Pareto-optimal set are also shown on the figure. The figure shows that solutions between Solutions A3 and C3 almost always improve in both $An_{\max}$ and $RI_{\min}$ with increasing the LCC. However, Solution D3 provides better $An_{\max}$ than Solution C3 with a higher cost but the $RI_{\min}$ it provides is worse than that of Solution C3. These observations can also be seen in Table 4, which shows the details of these representative solutions. This situation occurs due to the fact that improving $An_{\max}$ beyond what is offered by Solution C3 requires additional maintenance actions aimed at improving the deck, which is not part of the redundancy system model. This is shown in Figs. 11(a) and 11(b), which present the schedules of maintenance application and history profiles for the cumulative maintenance cost for the selected solutions, respectively. It is also observed in Fig. 11(a) that Solution A3 requires no EM applications. Figs. 12 and 13 show the history profiles of the selected CM solutions for the unavailability and redundancy, respectively. It can be observed in Figs. 11–13 how the three PM applications in Solution B3 were able to delay the first reaching of the unavail-

ability and redundancy to their thresholds. Once the unavailability threshold was reached, the superstructure is replaced. It would have been expected that the three PM applications were applied again. However, at that time and due to the effect of the discount rate, the optimization algorithm determined that it is more economical and effective to apply EM. The frequent application of EM associated with Solution D3 as shown in Figs. 11–13 indicates that it may not be practical to target an unavailability threshold as low as $10^{-3}$ and a redundancy threshold as high as $10^4$.

## Conclusions

This paper presented an approach for an automated multiobjective optimization of maintenance strategies considering the unavailability, redundancy, and the LCC as criteria. The unavailability and redundancy were calculated based on lifetime functions. Models that reflect the effects of separate and/or combined EM and PM on the lifetime functions were presented. An algorithm for the optimization of EM was proposed and its advantage over another algorithm was investigated. The effects of the performance thresholds on the LCC due to EM were investigated. A novel approach for regular and irregular time-interval PM optimization was proposed. Both EM and PM were considered in a novel proposed multiobjective maintenance optimization approach. In this approach, multiple EM types and multiple PM types were considered, and regular or irregular time-interval PM

<!-- página 13 -->

> **Fig. 13.** History profiles of redundancy for the selected combined EM and PM (CM) solutions: (a) Solution A3; (a) Solution B3; (c) Solution C3; and (d) Solution D3

were considered. Furthermore, EM was treated as performance-based, i.e., EM is only applied when a performance threshold is reached, and thus solutions that are more economical than time-based solutions were obtained. GAs were used to solve the optimization problem. The optimization approach was applied to a bridge located in Colorado, United States.

The following conclusions can be made:

1. Using the unavailability of structures as a performance indicator provides great flexibility in incorporating the effects of maintenance on the performance and high speed in the maintenance optimization solution;

2. It was observed that the EM optimization using the proposed algorithm EMO2 can always provide the optimum solutions while the traditional method EMO1 may, in some cases, fail to find these optimum solutions;

3. It was observed that the proposed single and combined optimization approaches were able to provide sets of optimum maintenance strategies among which trade-offs exist and can be identified;

4. It was shown that the interaction between the unavailability, redundancy, and LCC was found to be nontrivial and understanding it requires the inclusion of these three aspects in a proper maintenance optimization problem formulation; and

5. The interactions, trade-offs, and compromises among the optimum solution found using the proposed approach provide valuable insight for decision makers to make sound and informed decisions with respect to the selection of the maintenance strategy.

The great potential offered by lifetime functions including the availability and redundancy for use in maintenance optimization should draw attention to these tool. Thus far, the basis of deriving the lifetime functions is the use of statistical observations that are generally hard to obtain for structures. Therefore, the resulting uncertainties may be high. Further research is clearly required to develop more accurate methods for deriving lifetime functions for structures potentially by incorporating information obtained by structural health monitoring into these functions. This is a research subject currently underway by the writers. Additionally, experimental research is needed to capture the true effects of maintenance on the lifetime functions. Combined with the maintenance optimization approach proposed herein, a complete framework for the management of infrastructure is achievable.

## Acknowledgments

The support from (1) the National Science Foundation through Grant Nos. CMS-0638728 and CMS-0639428; (2) the Commonwealth of Pennsylvania, Department of Community and Economic Development, through the Pennsylvania Infrastructure Technology Alliance (PITA); (3) the U.S. Federal Highway Ad-

<!-- página 14 -->

ministration Cooperative Agreement Award No. DTFH61-07-H-00040; and (4) the U.S. Office of Naval Research Contract No. N00014-08–1-0188 is gratefully acknowledged. The opinions and conclusions presented in this paper are those of the writers and do not necessarily reflect the views of the sponsoring organizations.

## References

Akgül, F., and Frangopol, D. M. (2004). "Computational platform for predicting lifetime system reliability profiles for different structure types in a network." *J. Comput. Civ. Eng.*, 18(2), 92–104.

Ang, A. H.-S., and Tang, W. H. (1984). *Probability concepts in engineering planning and design: Decision, risk and reliability*, Vol. II, Wiley, New York.

Ciampoli, M., and Ellingwood, B. R. (2002). "Probabilistic methods for assessing current and future performance of concrete structures in nuclear power plants." *Mater. Struct.*, 35(1), 3–14.

Deb, K. (2001). *Multi-objective optimization using evolutionary algorithms*, Wiley, New York.

Deb, K., Pratap, A., Agrawal, S., and Meyarivan, T. (2002). "A fast and elitist multiobjective genetic algorithm: NSGA-II." *IEEE Trans. Evol. Comput.*, 6(2), 182–197.

Enright, M. P., and Frangopol, D. M. (1998). "Failure time prediction of deteriorating fail-safe structures." *J. Struct. Eng.*, 124(12), 1448–1457.

Estes, A. C. (1997). "A system reliability approach to the lifetime optimization of inspection and repair of highway bridges." Ph.D. thesis, Dept. of Civil, Environmental, and Architectural Engineering, Univ. of Colorado at Boulder, Boulder, Colo.

Estes, A. C., and Frangopol, D. M. (1999). "Repair optimization of highway bridges using system reliability approach." *J. Struct. Eng.*, 125(7), 766–775.

Frangopol, D. M. (2010). "Life-cycle performance, management, and optimization of structural systems under uncertainty: Accomplishments and challenges." *Struct. Infrastruct. Eng.*, posted online ahead of print May 11, 2010. DOI: 10.1080/15732471003594427.

Frangopol, D. M., Kong, J. S., and Gharaibeh, E. S. (2001). "Reliability-based life-cycle management of highway bridges." *J. Comput. Civ. Eng.*, 15(1), 27–34.

Frangopol, D. M., Lin, K.-Y., and Estes, A. C. (1997). "Life-cycle cost design of deteriorating structures." *J. Struct. Eng.*, 123(10), 1390–1401.

Frangopol, D. M., and Liu, M. (2007). "Maintenance and management of civil infrastructure based on condition, safety, optimization and life-cycle cost." *Struct. Infrastruct. Eng.*, 3(1), 29–41.

Frangopol, D. M., and Okasha, N. M. (2008). "Life-cycle performance and redundancy of structures." *Proc., 6th Int. Probabilistic Workshop*, C.-A. Graubner, H. Schmidt, and D. Proske, eds., Technische Universität Darmstadt, Germany, 1–14.

Frangopol, D. M., and Okasha, N. M. (2009). "Redundancy of structural systems based on survivor functions." *Proc., 2009 Structures Congress: Don't Mess with Structural Engineers SEI-ASCE* (CD-ROM), L. Griffiths, T. Helwig, M. Waggoner, and M. Hoit, eds., ASCE, Reston, Va., 1781–1790.

Furuta, H., Kameda, T., Fukuda, Y., and Frangopol, D. M. (2004). "Life-cycle cost analysis for infrastructure systems: Life-cycle cost vs. safety level vs. service life." *Life-cycle performance of deteriorating structures: Assessment, design and management*, D. M. Frangopol, E. Brühwiler, M. H. Faber, and B. Adey, eds., ASCE, Reston, Va., 19–25.

Goldberg, D. E. (1989). *Genetic algorithms in search, optimization and machine learning*, Addison-Wesley, Reading, Mass.

Hoyland, A., and Rausand, M. (1994). *System reliability theory: Models and statistical methods*, Wiley-Interscience, New York.

Klaassen, K. B., and van Peppen, J. C. L. (1989). *System reliability: Concepts and applications*, Edward Arnold, New York.

Kong, J. S., and Frangopol, D. M. (2003). "Life-cycle reliability based maintenance cost optimization of deteriorating structures with emphasis on bridges." *J. Struct. Eng.*, 129(6), 818–828.

Leemis, L. M. (1995). *Reliability, probabilistic models and statistical methods*, Prentice-Hall, Englewood Cliffs, N.J.

Liu, C., Hammad, A., and Itoh, Y. (1997). "Multiobjective optimization of bridge deck rehabilitation using a genetic algorithm." *Comput. Aided Civ. Infrastruct. Eng.*, 12(6), 431–443.

Liu, M., and Frangopol, D. M. (2004). "Probabilistic maintenance prioritization for deteriorating bridges using a multiobjective genetic algorithm." *Proc., 9th ASCE Specialty Conf. on Probabilistic Mechanics and Structural Reliability*, ASCE, Reston, Va.

Liu, M., and Frangopol, D. M. (2005a). "Bridge annual maintenance prioritization under uncertainty by multiobjective combinatorial optimization." *Comput. Aided Civ. Infrastruct. Eng.*, 20(5), 343–353.

Liu, M., and Frangopol, D. M. (2005b). "Multiobjective maintenance planning optimization for deteriorating bridges considering condition, safety, and life-cycle cost." *J. Struct. Eng.*, 131(5), 833–842.

Maunsell Ltd. (1999). "Serviceable life of highway structures and their components." *Final Rep.*, Birmingham Highways Agency, London.

Miyamoto, A., Kawamura, K., and Nakamura, H. (2000). "Bridge management system and maintenance optimization for existing bridges." *Comput. Aided Civ. Infrastruct. Eng.*, 15(1), 45–55.

Mori, Y., and Ellingwood, B. R. (1993). "Reliability-based service life assessment of aging concrete structures." *J. Struct. Eng.*, 119(5), 1600–1621.

Mori, Y., and Ellingwood, B. R. (1994a). "Maintaining reliability of concrete structures. I: Role of inspection/repair." *J. Struct. Eng.*, 120(3), 824–845.

Mori, Y., and Ellingwood, B. R. (1994b). "Maintaining reliability of concrete structures. II: Optimum inspection/repair." *J. Struct. Eng.*, 120(3), 846–862.

Neves, L. C., Frangopol, D. M., and Cruz, P. J. (2006a). "Probabilistic lifetime-oriented multiobjective optimization of bridge maintenance: Single maintenance type." *J. Struct. Eng.*, 132(6), 991–1005.

Neves, L. C., Frangopol, D. M., and Petcherdchoo, A. (2006b). "Probabilistic lifetime-oriented multiobjective optimization of bridge maintenance: Combination of maintenance types." *J. Struct. Eng.*, 132(11), 1821–1834.

Okasha, N. M., and Frangopol, D. M. (2009). "Lifetime-oriented multiobjective optimization of structural maintenance considering system reliability, redundancy and life-cycle cost using GA." *Struct. Safety*, 31(6), 460–474.

Okasha, N. M., and Frangopol, D. M. (2010a). "Redundancy of structural systems with and without maintenance: An approach based on lifetime functions." *Reliab. Eng. Syst. Saf.*, 95(5), 520–533.

Okasha, N. M., and Frangopol, D. M. (2010b). "Time-variant redundancy of structural systems." *Struct. Infrastruct. Eng.*, 6(1–2), 279–301.

Ramakumar, R. (1993). *Engineering reliability: Fundamentals and applications*, 1st Ed., Prentice-Hall, Englewood Cliffs, N.J.

Yang, S.-I., Frangopol, D. M., and Neves, L. C. (2006). "Optimum maintenance strategy for deteriorating structures based on lifetime functions." *Eng. Struct.*, 28(2), 196–206.
