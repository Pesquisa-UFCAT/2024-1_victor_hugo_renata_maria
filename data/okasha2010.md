Novel Approach for Multicriteria Optimization
of Life-Cycle Preventive and Essential Maintenance
of Deteriorating Structures
Nader M. Okasha, S.M.ASCE1; and Dan M. Frangopol, Dist.M.ASCE2
Abstract:Inthispaper,theperformanceofstructuresismodeledusinglifetimefunctions.Specifically,theunavailabilityandredundancy
are used as performance indicators, based on which optimum maintenance strategies are sought. Models that reflect the separate or
combinedeffectsofessentialandpreventivemaintenanceontheunavailabilityarepresented.Anoveloptimizationapproachisproposed
inwhichtheproblemisformulatedtoprovideoptimummaintenancestrategieswitheitherorbothessentialandpreventivemaintenance
actions. Genetic algorithms are used to solve this problem. In this paper, multiple essential maintenance types and multiple preventive
maintenance types are considered, and regular or irregular preventive maintenance time-intervals are considered. Furthermore, essential
maintenanceistreatedasperformance-based,i.e.,essentialmaintenanceisonlyappliedwhenaperformancethresholdisreached,andan
algorithm is proposed for conducting the optimization under uncertainty. Although applicable to any type of structure, the proposed
approach is illustrated on a highway bridge example.
DOI: 10.1061/(cid:1)ASCE(cid:2)ST.1943-541X.0000198
CE Database subject headings: Structural systems; Life cycles; Optimization; Maintenance; Deterioration.
Author keywords: Structural systems; Lifetime functions; Redundancy; Availability; Lifetime performance; Maintenance; Multi-
objective optimization; GA.
Introduction mance measures. Examples of these measures and their applica-
tionsintheliteratureare:thepoint-in-timereliabilityindex(cid:1)Estes
Economic allocation of funds for maintaining deteriorating civil and Frangopol 1999; Akgül and Frangopol 2004(cid:2); the point-in-
time probability of system failure and redundancy (cid:1)Okasha and
infrastructure systems requires optimizing the maintenance plans
under uncertainty (cid:1)Frangopol 2010(cid:2). The key ingredients of the
Frangopol2010b(cid:2);thecumulativeprobabilityoffailure(cid:1)Moriand
maintenanceoptimizationprocessare(cid:1)1(cid:2)theperformanceindica- Ellingwood 1993, 1994a,b; Enright and Frangopol 1998; Ciam-
tors upon which maintenance decisions are made; (cid:1)2(cid:2) the list of poli and Ellingwood 2002(cid:2); the lifetime probability of failure or maintenance options to be optimized; (cid:1)3(cid:2) the problem formula- the unavailability (cid:1)Yang et al. 2006; Okasha and Frangopol
2010a(cid:2); and the condition and safety indexes (cid:1)Neves et al.
tion; and (cid:1)4(cid:2) the solution technique.
2006a,b; Liu and Frangopol 2004, 2005a,b; Frangopol and Liu
One of the roles that a performance indicator plays in the
2007(cid:2).
maintenance planning process is an alarm which is triggered
Maintenance interventions are scheduled to either delay the
when that performance indicator reaches a specified threshold. It
occurrenceofreachingaperformanceindicatortoitsthresholdor
isatoolbywhichthesafetyandintegrityofthestructuralsystem
improve the state of the performance indicator if its threshold is
is ensured by preventing the performance indicators from cross-
reached. Thus, maintenance types may be categorized into two
ingtheirthresholds.Needlesstosay,aperformanceindicatorused generalgroups:preventivemaintenance(cid:1)PM(cid:2)andessentialmain-
forthemaintenanceoptimizationprocessisrequiredtobeableto tenance(cid:1)EM(cid:2)(cid:1)KongandFrangopol2003(cid:2).PMsareusuallytime-
accuratelyrepresentaspecifictypeofperformanceandpredictits based, that is, they are applied at prespecified time instants over
future variations. Frangopol and Okasha (cid:1)2008(cid:2) have identified the life-cycle of the structure. In contrast, EMs are performance-
numerous commonly encountered and used life-cycle perfor- basedinthattheyareappliedwhensomeperformanceindicators
reach predefined target values (cid:1)Liu and Frangopol 2005a(cid:2).
1Graduate Research Assistant, Dept. of Civil and Environmental Ingeneral,theoptimizationofmaintenanceisacombinatorial
Engineering,ATLSS Center, Lehigh Univ., 117ATLSS Dr., Bethlehem, optimizationproblembecausethemaintenanceplaniscomprised
PA18015-4729.E-mail:nao204@lehigh.edu of various maintenance measures (cid:1)Miyamoto et al. 2000(cid:2). The
2Professor and the Fazlur R. Khan Endowed Chair of Structural En- optimizationofmaintenanceconsideringonlyperformance-based
gineering andArchitecture, Dept. of Civil and Environmental Engineer- EM reduces the problem to finding the optimum EM option to
ing,ATLSSCenter,LehighUniv.,117ATLSSDr.,Bethlehem,PA18015-
apply once a performance threshold is reached. Hence, the opti-
4729(cid:1)correspondingauthor(cid:2).E-mail:dan.frangopol@lehigh.edu
mization of continuous design variables is not required and
Note. This manuscript was submitted on November 11, 2008; ap-
a nonautomated solution of the problem is possible (cid:1)Estes and
provedonFebruary1,2010;publishedonlineonFebruary6,2010.Dis-
Frangopol1999;OkashaandFrangopol2010a;Yangetal.2006(cid:2).
cussionperiodopenuntilJanuary1,2011;separatediscussionsmustbe
submitted for individual papers. This paper is part of the Journal of However, including the PM in the optimization introduces the
StructuralEngineering,Vol.136,No.8,August1,2010.©ASCE,ISSN need for continuous design variables to represent the times of
0733-9445/2010/8-1009–1022/$25.00. application of these PMs into the problem. The solution of this
JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010/1009
J. Struct. Eng. 2010.136:1009-1022.
.devreser
sthgir
lla
;ylno
esu
lanosrep
roF
.ECSA
thgirypoC
.31/92/90
no
seirarbiL
adirolF
lartneC
fO
ytisrevinU
yb
gro.yrarbilecsa
morf
dedaolnwoD

type of problems requires using a robust optimization algorithm, Okasha 2008(cid:2). Closed-form solutions are not available for most
such as a genetic algorithm (cid:1)GA(cid:2) (cid:1)Goldberg 1989; Deb 2001(cid:2). life-cycle probabilistic performance indicators. Instead, simula-
Another issue with including PM in optimization is that the best tionoriterativemethodsarerequiredtoevaluatethisperformance
numberofPMapplicationsisnotknownandthusthenumberof indicator. In addition, life-cycle performance evaluation requires
time-of-application design variables to be used is unknown. By evaluating the performance indicator at many time increments
considering the uniform application of PM, the problem is sim- overthelifetimeofthestructure.Furthermore,theoptimizationof
plified. Neves et al. (cid:1)2006a,b(cid:2) used two design variables for PM: maintenanceisacombinatorialoptimizationthatrequiresiterative
one for the time of first application of PM and the other for solution techniques. Thus, for optimization of maintenance, the
thetime-intervalbetweensubsequentapplications.However,non- life-cycle performance needs to be evaluated many times.There-
uniformtime-intervalPMstrategieshavebeenshowntobemore fore, the optimization of maintenance based on probabilistic life-
economical than the uniform ones (cid:1)Frangopol et al. 1997(cid:2). At- cycle performance indicators is usually computationally very
tempting to address this issue, coded design variables in a form expensive.
of numerical strings were used. Liu and Frangopol (cid:1)2005a(cid:2) used Lifetimefunctions,however,offertheabilitytorapidlyevalu-
a real value string with a bit length equal to the designated life- ate the life-cycle performance through available closed-form
cycle in years. Each bit may take an integer value representing solutions.Hence,theuseoflifetimefunctionsinautomatedmain-
one of the identifiers (cid:1)ids(cid:2) given for the considered maintenance tenance optimization problems significantly reduces the compu-
options. In fact, the difference between PM and EM is removed; tational time required. In fact, the efficiency and convenience of
only the effects of each maintenance type on the performance using lifetime functions even in nonautomated maintenance opti-
are retained (cid:1)Liu and Frangopol 2005a(cid:2). In other words, the mization has already been demonstrated (cid:1)Yang et al. 2006;
time and choice of application of both PM and EM were deter- Okasha and Frangopol 2010a(cid:2).
mined by the optimum coded string found by the optimiza- Lifetime functions may be used to characterize the lifetime
tion problem, and with no regard to any performance threshold. reliability of existing structures. According to these functions,
Alternatively, Miyamoto et al. (cid:1)2000(cid:2) used binary strings for de- the time to failure of components or systems is treated as a ran-
scribing the ids of the maintenance options. The result was a dom variable. The time to failure is defined as the time elapsing
binary matrix in which each row represented the maintenance from the time the component is put into operation until it fails
actionatagivenyearandthebinarycodeinthatrowrepresented for the first time (cid:1)Hoyland and Rausand 1994(cid:2). An appropriate
one of the considered maintenance options. Other similar rep- distribution is assigned to the probability density function (cid:1)PDF(cid:2)
resentations were used (cid:1)Okasha and Frangopol 2009; Liu and of the time to failure by regression of statistical data of ages of
Frangopol 2004, 2005b; Liu et al. 1997; Furuta et al. 2004(cid:2). similar components or systems. The Weibull distribution is
However, treating EM as a time-based maintenance (cid:1)Okasha and usually the best fit distribution to ages of decaying components
Frangopol 2009; Liu and Frangopol 2004, 2005a,b; Miyamoto or systems. The PDF of the Weibull distribution is defined as
et al. 2000(cid:2) may result in obtaining uneconomical solutions, (cid:1)Leemis 1995(cid:2)
(cid:3) (cid:4)
whereEMisappliedsoonerthanthetimeofreachingthethresh-
old of a performance indicator. Neves et al. (cid:1)2006b(cid:2) combined (cid:1)(cid:2)(cid:1)(cid:2)t(cid:2)(cid:1)−1e−(cid:1)(cid:2)t(cid:2)(cid:1) for t(cid:3)0
EM with PM in the optimization and EM was treated indeed as
f(cid:1)t(cid:2)= (cid:1)1(cid:2)
0 otherwise
performance-based.However,onlyoneEMtypewasused.Thus,
theneedtooptimizetheEMwasabsent.TheconsideredEMtype where (cid:2)=scale parameter and (cid:1)=shape parameter. Based on the
was applied at the time the performance indicator reaches its time to failure PDF, several lifetime function representations can
threshold. be derived.Among these representations are the availability and
It follows from the above discussion that the need for an effi- redundancy (cid:1)Okasha and Frangopol 2010a(cid:2).
cient problem formulation for maintenance optimization is evi-
dent. To overcome the shortcomings of the aforementioned
Availability
approaches, this problem formulation is required to be able to:
(cid:1)1(cid:2) handle regular and irregular time-interval PM; (cid:1)2(cid:2) handle Acomponentisavailableattimetifitisfunctioningatthistime.
EM only, PM only, and both EM and PM combined; (cid:1)3(cid:2) handle The event that a component survives (cid:1)i.e., does not fail(cid:2) up to
multiple PM types and multiple EM types; and (cid:1)4(cid:2) treat EM as timet isinfactthesameeventthatthecomponentisavailableat
performance-based. It is the objective of this paper to pro- timet.Therefore,theprobabilityofsurvivalofacomponentfrom
pose such an approach. Performance indicators used are the un- the time it is put in service until time t is the same as the prob-
availability and redundancy and they are calculated based on ability that the component is available at time t. Availability is,
lifetime functions. Models that reflect the separate and combined therefore,analternativewaytoquantifyingthereliabilityofcom-
effects of EM and PM on these performance indicators are ponents and systems. In fact, the survivor function (cid:1)or reliability
presented. function(cid:2) of a nonrepairable component is a special case of its
availability.Theybothdifferonlywhenthecomponentisrepaired
orreplaced(cid:1)KlaassenandvanPeppen1989(cid:2).TheavailabilityA(cid:1)t(cid:2)
Performance Measures canbecalculatedbyintegrationofthePDFofthetimetofailure.
Theavailabilityofacomponentwithoutmaintenancecanbecal-
The performance of structures may be measured by various indi- culated by
cators. Crucial decisions are made based on the results provided (cid:5)
(cid:4)
by these indicators.Thus, the accurate representation and predic-
A(cid:1)t(cid:2)=P(cid:1)T(cid:3)t(cid:2)= f(cid:1)u(cid:2)du (cid:1)2(cid:2)
tion of the performance by its indicator is evidently essential.
t
However,uncertaintyinquantifyingthelifetimestructuralperfor-
mance is inevitably encountered. Probabilistic methods are used whereT=timetofailureand f(cid:1)t(cid:2)isitsPDF.Theunavailabilityof
to handle these uncertainties appropriately (cid:1)Frangopol and a component, An(cid:1)t(cid:2)=1−A(cid:1)t(cid:2), is the probability that it has failed
1010/JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010
J. Struct. Eng. 2010.136:1009-1022.
.devreser
sthgir
lla
;ylno
esu
lanosrep
roF
.ECSA
thgirypoC
.31/92/90
no
seirarbiL
adirolF
lartneC
fO
ytisrevinU
yb
gro.yrarbilecsa
morf
dedaolnwoD

|     |     |     |     |     |     |     |     |     |     |     | (cid:8) | (cid:10) |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | -------- | --- | --- | --- | --- |
beforetimet andthusitisunavailable(cid:1)notfunctioning(cid:2)attimet k
(cid:9)
(cid:1)Ang andTang 1984(cid:2). A(cid:1)(cid:1)t(cid:2)=A t− Pn Tem (cid:5)t(cid:6)Tem (cid:1)3(cid:2)
|     |     |     |     |     |     |     |     |     |     |     |     | i   | k   |     | k+1 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:1)or
As will be shown next, the choice of availability unavail- i=1
ability(cid:2)asaperformancemeasureoffersgreatflexibilityinincor-
A(cid:1)(cid:1)t(cid:2)=updated
|                                                            |             |     |          |                 |     |         |      | where  |     |       | availability | after   | the    | application | of   | mainte- |
| ---------------------------------------------------------- | ----------- | --- | -------- | --------------- | --- | ------- | ---- | ------ | --- | ----- | ------------ | ------- | ------ | ----------- | ---- | ------- |
| porating                                                   | the effects | of  | any type | of maintenance. |     | Whether | this |        |     |       |              |         |        |             |      |         |
|                                                            |             |     |          |                 |     |         |      | nance. | The | value | of Pn        | depends | on the | improvement | that | EM      |
| effectisimprovingthestateoftheavailabilityorslowingtherate |             |     |          |                 |     |         |      |        |     |       | i            |         |        |             |      |         |
actionibringstotheavailability.However,iftheEMapplications
by which it deteriorates, an appropriate model is presented. In requirereplacingthecomponent,itisrationaltorestoretheavail-
| general, | information | regarding | the | effects | of maintenance |     | on any |     |     |     |     |     |     |     |     |     |
| -------- | ----------- | --------- | --- | ------- | -------------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
abilitytoitsoriginalvalueatthetimeofeachEMapplicationand
performanceindicatorishardtoobtain.Onceobtained,thisinfor- (cid:1)Okasha 2010a(cid:2)
|            |           |      |        |              |     |         |             | can | thus be | calculated                            | by  |             | and Frangopol      |     |     |                 |
| ---------- | --------- | ---- | ------ | ------------ | --- | ------- | ----------- | --- | ------- | ------------------------------------- | --- | ----------- | ------------------ | --- | --- | --------------- |
| mation can | be easily | used | in the | availability |     | models. | Until then, |     |         |                                       |     |             |                    |     |     |                 |
|            |           |      |        |              |     |         |             |     |         | A(cid:1)(cid:1)t(cid:2)=A(cid:1)t−Tem |     | (cid:2) Tem | (cid:5)t(cid:6)Tem |     |     | (cid:1)4(cid:2) |
appropriate assumptions based on engineering judgment are re- k k k+1
.devreser sthgir lla ;ylno esu lanosrep roF .ECSA thgirypoC .31/92/90 no seirarbiL adirolF lartneC fO ytisrevinU yb gro.yrarbilecsa morf dedaolnwoD
sorted to.
|           |           |             |     |     |     |     |     | Effect | of Preventive |     | Maintenance  |     |            |               |     |        |
| --------- | --------- | ----------- | --- | --- | --- | --- | --- | ------ | ------------- | --- | ------------ | --- | ---------- | ------------- | --- | ------ |
| Effect of | Essential | Maintenance |     |     |     |     |     |        |               |     |              |     |            |               |     |        |
|           |           |             |     |     |     |     |     | The    | application   | of  | PM typically |     | results in | the reduction |     | of the |
The application of EM typically results in restoring the perfor- deterioration rate (cid:1)Neves et al. 2006b(cid:2). This effect is manifested
manceindicatortoitsvalueatsometimepriortotheapplication in the availability as follows. Let TPM=(cid:6)Tpm ,Tpm ,...,
|                        |     |     |     |     |         |     |     |     |         |     |     |     |     |     | 1   | 2   |
| ---------------------- | --- | --- | --- | --- | ------- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
| ofEM.LetTEM=(cid:6)Tem |     |     |     |     | (cid:7) |     |     |     | (cid:7) |     |     |     |     |     |     |     |
1 ,Tem 2 ,...,Tem n bethetimesatwhich Tpm be the times at which q PM actions are applied to a com-
q
n EM actions are applied to a component. Let also Tem =0 and ponent.LetalsoTpm =0 andTpm =(cid:4).ApplicationofPMac-
|     |     |     |     |     |     |     | 0   |     |     |     | 0   |     | q+1 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Tem =(cid:4).ApplicationofEMactionirestorestheavailabilityto tion j restorestherateofchangeintheavailabilitytoitsrateata
n+1
its value at a point in time Pn prior to the time Tem.The avail- point in time Rn prior to the time Tpm. The availability of a
|     |     |     | i   |     |     | i   |     |     |     | j   |     |     | j   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ability of a component can thus be calculated by component can thus be calculated by
|     |     |     |     |     | (cid:11)         |     |     |     |             |     |     | (cid:13) |     |     |     |     |
| --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | ----------- | --- | --- | -------- | --- | --- | --- | --- |
|     |     |     |     |     | A(cid:1)t(cid:2) |     |     | if  | t(cid:6)Tpm |     |     |          |     |     |     |     |
1
A(cid:1)(cid:1)t(cid:2)= i A(cid:1)Tpm (cid:2) (cid:1)5(cid:2)
|     |     |     |     |     |                     | (cid:12) | −F                    |        |                        |     |             |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------------------- | -------- | --------------------- | ------ | ---------------------- | --- | ----------- | --- | --- | --- | --- | --- |
|     |     |     |     |     | A(cid:1)t−F(cid:2)· |          | j                     | j−1 if | Tpm (cid:5)t(cid:6)Tpm |     | , i(cid:7)1 |     |     |     |     |     |
|     |     |     |     |     |                     | i        | A(cid:1)Tpm −F(cid:2) |        | i                      |     | i+1         |     |     |     |     |     |
|     |     |     |     |     |                     | j=1      | j                     | j      |                        |     |             |     |     |     |     |     |
jth
| where Tpm | j =time | of application |     | of the | PM, | and |          |          |              |          |     |     |     |     |     |                 |
| --------- | ------- | -------------- | --- | ------ | --- | --- | -------- | -------- | ------------ | -------- | --- | --- | --- | --- | --- | --------------- |
|           |         |                |     |        |     |     | (cid:11) |          |              | (cid:13) |     |     |     |     |     |                 |
|           |         |                |     |        |     |     | 0        |          | j=0          |          |     |     |     |     |     |                 |
|           |         |                |     |        |     |     | (cid:8)  | (cid:10) | if           |          |     |     |     |     |     |                 |
|           |         |                |     |        |     |     | j        |          |              |          |     |     |     |     |     | (cid:1)6(cid:2) |
|           |         |                |     |        |     | F = | (cid:9)  |          |              |          |     |     |     |     |     |                 |
|           |         |                |     |        |     | j   | min Rn   | ,Tpm     | if j(cid:3)0 |          |     |     |     |     |     |                 |
|           |         |                |     |        |     |     |          | x j      |              |          |     |     |     |     |     |                 |
x=1
Clearly, the effect of a given type of PM on the availability is determined by the value of Rn x . If the application of PM reduces the rate
of change in the availability to its original value, the availability of a component can be calculated by
|     |     |     |     | (cid:11) |                  |     |     |     |                |     |     | (cid:13) |     |     |     |     |
| --- | --- | --- | --- | -------- | ---------------- | --- | --- | --- | -------------- | --- | --- | -------- | --- | --- | --- | --- |
|     |     |     |     |          | A(cid:1)t(cid:2) |     |     |     | if t(cid:6)Tpm |     |     |          |     |     |     |     |
1
|     |     |     | A(cid:1)(cid:1)t(cid:2)= |     |     |     | i   |     |     |     |     |     |     |     |     | (cid:1)7(cid:2) |
| --- | --- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- |
(cid:12)
|     |     |     |     |     | A(cid:1)t−Tpm(cid:2)· |     | A(cid:1)Tpm −Tpm | (cid:2) | if Tpm | (cid:5)t(cid:6)Tpm |     | , i(cid:7)1 |     |     |     |     |
| --- | --- | --- | --- | --- | --------------------- | --- | ---------------- | ------- | ------ | ------------------ | --- | ----------- | --- | --- | --- | --- |
|     |     |     |     |     |                       | i   | j                | j−1     |        | i                  | i+1 |             |     |     |     |     |
j=1
Figs.1(cid:1)a(cid:2)and1(cid:1)b(cid:2)showtheeffectsofEMandPM,respectively, i
|                                                         |                |     |           |               |     |           |         |     |                                       |     |     |            | (cid:12) A(cid:1)Tpm | −F  | (cid:2) |     |
| ------------------------------------------------------- | -------------- | --- | --------- | ------------- | --- | --------- | ------- | --- | ------------------------------------- | --- | --- | ---------- | -------------------- | --- | ------- | --- |
|                                                         |                |     |           |               |     |           |         |     | A(cid:1)(cid:1)t(cid:2)=A(cid:1)t−Tem |     |     | −F(cid:2)· |                      | j   | j−1     |     |
| ontheunavailabilityofacomponentwithalifetimeWeibulldis- |                |     |           |               |     |           |         |     |                                       |     |     | k i        |                      |     |         |     |
|                                                         |                |     | (cid:1)=5 | (cid:2)=1/200 |     |           |         |     |                                       |     |     |            | A(cid:1)Tpm          | −F  | (cid:2) |     |
| tribution                                               | and parameters |     | and       |               |     | under two | mainte- |     |                                       |     |     |            | j=a                  | j   | j       |     |
nance applications over its lifetime. The first maintenance (cid:5)t(cid:6)Tpm (cid:6)Tpm
|     |     |     |     |     |     |     |     |     |     | if  | Tpm |     | ; Tem |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
applicationisattheyear20andthesecondisattheyear40.For i i+1 k a
|         |              |     | 1(cid:1)b(cid:2), |       |     |           |            |     |     | and | Tpm | (cid:3)Tpm |     |     |     | (cid:1)8(cid:2) |
| ------- | ------------ | --- | ----------------- | ----- | --- | --------- | ---------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --------------- |
| both PM | applications | in  | Fig.              | Rn=Rn |     | and it is | clear that |     |     |     |     | i          | a   |     |     |                 |
i
| increasing | Rn reduces | the | slope | of the | unavailability |     | curve. |          |            |       |         |          |           |         |              |     |
| ---------- | ---------- | --- | ----- | ------ | -------------- | --- | ------ | -------- | ---------- | ----- | ------- | -------- | --------- | ------- | ------------ | --- |
|            |            |     |       |        |                |     |        | if the   | PM actions |       | restore | the rate | of change | in the  | availability | to  |
|            |            |     |       |        |                |     |        | its rate | at a       | point | in time | Rn prior | to the    | time of | application  | of  |
x
| Effect of | Combined | Essential |     | and Preventive |     | Maintenance |     |      |           |     |        |          |                  |     |        |          |
| --------- | -------- | --------- | --- | -------------- | --- | ----------- | --- | ---- | --------- | --- | ------ | -------- | ---------------- | --- | ------ | -------- |
|           |          |           |     |                |     |             |     | each | PM action | x   | and EM | restores | the availability |     | to its | original |
CalculationofavailabilityconsideringtheapplicationofbothEM
value, or
| and PM                         | depends | on the | sequence | of application |                       | of these | mainte- |     |     |     |     |     |     |     |     |     |
| ------------------------------ | ------- | ------ | -------- | -------------- | --------------------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nancetypes.Attimet,ifEMactionk |         |        |          |                | wasthemostrecentmain- |          |         |     |     |     |     |     | i   |     |     |     |
(cid:12)
tenance type applied, Eq. (cid:1)3(cid:2) or Eq. (cid:1)4(cid:2) is used. However, if PM A(cid:1)(cid:1)t(cid:2)=A(cid:1)t−Tem −Tpm(cid:2)· A(cid:1)Tpm (cid:2)
|          |         |             |             |     |      |         |        |     |     |     | k   | i   |     | j −Tpm | j−1 |     |
| -------- | ------- | ----------- | ----------- | --- | ---- | ------- | ------ | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
| action i | was the | most recent | maintenance |     | type | applied | and EM |     |     |     |     |     |     |        |     |     |
j=a
actions were applied up to that time ending by EM action k, (cid:5)t(cid:6)Tpm (cid:6)Tpm
|     |     |     |     |     |     |     |     |     |     | if Tpm |     |     | ; Tem |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | ----- | --- | --- | --- |
where the PM action following EM action k is PM action a, the i i+1 k a
availability can be calculated by and Tpm (cid:3)Tpm (cid:1)9(cid:2)
|     |     |     |     |     |     |     |     |     |     |     | i   | a   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010/1011
J. Struct. Eng. 2010.136:1009-1022.

|     |     |     |     |     |     |     |     | Colorado       | Bridge | E-17-AH  |             |     |              |     |          |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | ------ | -------- | ----------- | --- | ------------ | --- | -------- | --- |
|     |     |     |     |     |     |     |     | In this study, | the    | proposed | maintenance |     | optimization |     | approach | is  |
appliedtothesuperstructureoftheColoradoBridgeE-17-AH.A
|     |     |     |     |     |     |     |     | detailed | description | of  | this bridge | can | be  | found in | Estes | (cid:1)1997(cid:2). |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | --- | ----------- | --- | --- | -------- | ----- | ------------------- |
Thebridgehasthreesimplespansofequallength.Thereinforced
|     |     |     |     |     |     |     |     | concrete     | slab is | supported | by           | nine         | standard-rolled, |     | compact, | and |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ------- | --------- | ------------ | ------------ | ---------------- | --- | -------- | --- |
|     |     |     |     |     |     |     |     |              |         |           | (cid:1)Estes | 1997(cid:2). |                  |     |          |     |
|     |     |     |     |     |     |     |     | noncomposite | steel   | girders   |              |              |                  |     |          |     |
Weibulldistributionsareadoptedtomodelthelifetimesofthe
|     |     |     |     |     |     |     |     | components | of  | this bridge. | The | parameters |     | of these | distributions |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ------------ | --- | ---------- | --- | -------- | ------------- | --- |
arebasedonthebestfitofthedatasummarizedin(cid:1)MaunsellLtd.
.devreser sthgir lla ;ylno esu lanosrep roF .ECSA thgirypoC .31/92/90 no seirarbiL adirolF lartneC fO ytisrevinU yb gro.yrarbilecsa morf dedaolnwoD 1999(cid:2).Theshapeandscaleparameters,(cid:1) and(cid:2),respectively,are
|     |     |     |     |     |     |     |     | (cid:1)=2.37              | and (cid:2)=0.0077 |             | for the | deck,        | and     | (cid:1)=2.86 | and (cid:2)=0.0106 |        |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------- | ------------------ | ----------- | ------- | ------------ | ------- | ------------ | ------------------ | ------ |
|     |     |     |     |     |     |     |     | for the girders.          |                    | This bridge |         | was examined |         | in Okasha    | and                | Fran-  |
|     |     |     |     |     |     |     |     | gopol (cid:1)2010a(cid:2) |                    | for EM      | only.   | However,     | herein, | both         | EM                 | and PM |
|     |     |     |     |     |     |     |     | are considered,           |                    | separately  | and     | combined     | for     | this bridge. |                    |        |
Multigirderbridgesaremodeledinsystemreliabilityanalyses
|     |     |     |     |     |     |     |     | as combinations |     | of series | and | parallel | components |     | (cid:1)Akgül | and |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --------- | --- | -------- | ---------- | --- | ------------ | --- |
Frangopol2004;EstesandFrangopol1999(cid:2).Forthebridgebeing
analyzed,thesystemfailureisassumedtooccurbythefailureof
anythreeadjacentgirdersorthedeck.Itwasfoundthatincluding
|     |     |     |     |     |     |     |     | the deck       | in the | redundancy |        | calculations | completely |          | undermines |        |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | ------ | ---------- | ------ | ------------ | ---------- | -------- | ---------- | ------ |
|     |     |     |     |     |     |     |     | the redundancy |        | offered    | to the | system       | by the     | girders. | This       | is be- |
Fig.1.Effectoftwoactions(cid:1)a(cid:2)EM;(cid:1)b(cid:2)PMattheyears20and40
|                       |     |      |           |      |            |         |         | cause the | deck | is connected |     | to the | rest of | the components |     | in the |
| --------------------- | --- | ---- | --------- | ---- | ---------- | ------- | ------- | --------- | ---- | ------------ | --- | ------ | ------- | -------------- | --- | ------ |
| on the unavailability |     | of a | component | with | a lifetime | Weibull | distri- |           |      |              |     |        |         |                |     |        |
assumedsystemmodelinseriesandhenceitsfailuretriggersthe
| butionandparameters(cid:1)=5 |     |     | and(cid:2)=1/200 |     |     |     |     |            |            |     |                  |     |        |              |            |     |
| ---------------------------- | --- | --- | ---------------- | --- | --- | --- | --- | ---------- | ---------- | --- | ---------------- | --- | ------ | ------------ | ---------- | --- |
|                              |     |     |                  |     |     |     |     | failure of | the system |     | (cid:1)Frangopol | and | Okasha | 2009(cid:2). | Therefore, |     |
thedeckwasexcludedfromthesystemmodelintheredundancy
|                    |     |       |         |          |           |     |            | calculations. | However,      |     | it was | part | of the | system | model | for the |
| ------------------ | --- | ----- | ------- | -------- | --------- | --- | ---------- | ------------- | ------------- | --- | ------ | ---- | ------ | ------ | ----- | ------- |
| if the application |     | of PM | reduces | the rate | of change | in  | the avail- |               |               |     |        |      |        |        |       |         |
|                    |     |       |         |          |           |     |            | availability  | calculations. |     |        |      |        |        |       |         |
abilitytoitsoriginalvalue.IfEMactionkrestorestheavailability
FourEMoptionsareconsideredandtheyandtheirassociated
| toitsvalueatapriorpointintimePn |     |     |     |     | priortothetimeTem |     | ,the |     |     |     |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | ----------------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
k k costs are (cid:1)Estes and Frangopol 1999(cid:2): (cid:1)1(cid:2) replace superstructure
|     | isreplacedwith(cid:9)k |     |     | inEqs.(cid:1)8(cid:2)and(cid:1)9(cid:2).Itisalso |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ---------------------- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
termTem k Pn y (cid:1)$487,100(cid:2); (cid:1)2(cid:2) replace exterior girders and deck (cid:1)$341,800(cid:2); (cid:1)3(cid:2)
|     |     | (cid:1)8(cid:2) | (cid:1)9(cid:2) y=1 |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --------------- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
noted that Eqs. and assume that PM application i is fol- (cid:1)$229,200(cid:2); (cid:1)4(cid:2)
|                |      |                                                  |     |     |       |             |              | replace                 | exterior | girders    |           |     | and           |     | replace       | deck |
| -------------- | ---- | ------------------------------------------------ | --- | --- | ----- | ----------- | ------------ | ----------------------- | -------- | ---------- | --------- | --- | ------------- | --- | ------------- | ---- |
| lowed by       | a PM | application                                      | and | not | an EM | application | (cid:1)i.e., |                         |          |            |           |     |               |     |               |      |
|                |      |                                                  |     |     |       |             |              | (cid:1)$225,600(cid:2). | For      | PM, silane | treatment |     | is considered |     | for maintain- |      |
| Tpm (cid:6)Tem |      | (cid:2).However,ifapplicationiisratherfollowedby |     |     |       |             |              |                         |          |            |           |     |               |     |               |      |
i+1 k+1 ing the deck and repainting is considered for maintaining the
an EM application, the equations are only modified by replacing girders. The effect of both these PM types is assumed to restore
(cid:6)Tem
| Tpm |     | in the inequality |     | conditions. |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ----------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
i+1 k+1 the rate of change in the unavailability to its original value. The
costofsilanetreatmentfortheentiredeckisassumedas$50,000
Redundancy and the cost of repainting all girders is assumed as $100,000.
Redundancyisanadditionaltypeofstructuralperformancethatis
| defined   | as a measure   | of  | the warning        |        | available | prior       | to system  |              |     |                |     |     |             |     |     |      |
| --------- | -------------- | --- | ------------------ | ------ | --------- | ----------- | ---------- | ------------ | --- | -------------- | --- | --- | ----------- | --- | --- | ---- |
|           |                |     |                    |        |           |             |            | Optimization |     | of Maintenance |     |     | Considering |     | EM  | Only |
| collapse. | The redundancy |     | of a               | system | can be    | directly    | calculated |              |     |                |     |     |             |     |     |      |
| from its  | unavailability | and | the unavailability |        | of        | its weakest | com-       |              |     |                |     |     |             |     |     |      |
(cid:1)Okasha 2010a(cid:2) EM usually has a significant effect on the bridge performance,
| ponent as |     | and Frangopol |     |     |     |     |     |          |           |            |     |         |     |        |           |       |
| --------- | --- | ------------- | --- | --- | --- | --- | --- | -------- | --------- | ---------- | --- | ------- | --- | ------ | --------- | ----- |
|           |     |               |     |     |     |     |     | although | extremely | expensive, |     | in part | due | to the | high user | costs |
(cid:1) (cid:1)t(cid:2)−An (cid:1)(cid:1)t(cid:2) associated with bridge partial or total closure during application
|     |     | RI(cid:1)= | An wc |     | s   |     |                  |                                                                     |     |     |     |     |     |     |     |     |
| --- | --- | ---------- | ----- | --- | --- | --- | ---------------- | ------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |            |       |     |     |     | (cid:1)10(cid:2) | ofthistypeofmaintenance(cid:1)Nevesetal.2006b(cid:2).PMisassociated |     |     |     |     |     |     |     |     |
An (cid:1)(cid:1)t(cid:2)
s
withsmallerimpactsonperformance,butclosureofthebridgeis
| whereAn(cid:1)(cid:1)t(cid:2)andAn(cid:1) |     | (cid:1)t(cid:2)=unavailabilityofthesystemandweak- |     |     |     |     |     |             |            |     |        |            |     |          |      |          |
| ----------------------------------------- | --- | ------------------------------------------------- | --- | --- | --- | --- | --- | ----------- | ---------- | --- | ------ | ---------- | --- | -------- | ---- | -------- |
|                                           |     |                                                   |     |     |     |     |     | not usually | necessary, |     | or can | be limited |     | to short | time | periods, |
|                                           | s   | wc                                                |     |     |     |     |     |             |            |     |        |            |     |          |      |          |
est component, respectively. resulting in lower user costs (cid:1)Neves et al. 2006b(cid:2). Ideally, the
For the purpose of reliability analysis, complex systems are downtimeofthebridgeduetoEMandtheusercostsarisingdue
usually decomposed into functional entities made of components to this downtime should be estimated and accounted for in the
or subsystems. By combining the appropriate series and parallel optimization process. In fact, their effect on the results can be
branches (cid:1)subsystems(cid:2) of a model systematically, the entire sys- significant (cid:1)Frangopol et al. 2001; Liu and Frangopol 2005b(cid:2). In
tem can be reduced to one single equivalent component. The re- this paper, these issues are not considered. However, having the
liability of this equivalent component is the reliability of the meansandappropriatedatatoquantifythem,theycanbestraight-
system. Such a procedure is known as the network reduction forwardly introduced into the approach presented herein.
method(cid:1)Ramakumar1993(cid:2).Infact,thismethodhassuccessfully The general goal in performance-based EM optimization is
been applied by Yang et al. (cid:1)2006(cid:2) in analyzing structures using finding the appropriate EM option to apply once a performance
lifetime functions. The minimal cut set method is also useful for threshold is reached. Considering one EM option transforms the
systemreliabilitycalculations(cid:1)HoylandandRausand1994(cid:2).This (cid:1)i.e.,
|     |     |     |     |     |     |     |     | optimization | problem |     | to a straightforward |     |     | analysis | problem |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ------- | --- | -------------------- | --- | --- | -------- | ------- | --- |
method has also been applied by Okasha and Frangopol (cid:1)2010a(cid:2) there is no need to search for an optimum solution(cid:2). However,
and it is used in this study. consideringmultipleEMoptionscreatesadiscretecombinatorial
1012/JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010
J. Struct. Eng. 2010.136:1009-1022.

optimization problem.The optimization aims to select one of the Table1.ResultsoftheEMO2MethodExamplefortheColoradoBridge
| availableEMoptionswhenaperformancethresholdisreached.If |     |     |     |     |     |     |     | E-17-AH |     |     |     |     |     |     |     |     |
| ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
multiple performance indicators, each with a threshold, are used Timeof
in the optimization process, the optimum selection of EM takes Maintenance EM application LCC
placeeachtimeanythresholdisreached.Performancethresholds scenario options (cid:1)years(cid:2) (cid:1)$(cid:2)
| that are            | reached     | and not     | reached | during    | the     | service      | life in the |     |     |                  |     |                        |     |     |         |     |
| ------------------- | ----------- | ----------- | ------- | --------- | ------- | ------------ | ----------- | --- | --- | ---------------- | --- | ---------------------- | --- | --- | ------- | --- |
|                     |             |             |         |           |         |              |             | 1   |     | (cid:3)11(cid:4) |     | (cid:3)18.637.3(cid:4) |     |     | 569,740 |     |
| optimum             | maintenance | plan        | are     | called    | active  | and inactive | thresh-     |     |     |                  |     |                        |     |     |         |     |
|                     |             |             |         |           |         |              |             |     |     | (cid:3)12(cid:4) |     | (cid:3)18.637.3(cid:4) |     |     |         |     |
|                     |             |             |         |           |         |              |             | 2   |     |                  |     |                        |     |     | 500,320 |     |
| olds, respectively. |             | An inactive |         | threshold | implies | that         | the worst   |     |     |                  |     |                        |     |     |         |     |
|                     |             |             |         |           |         |              |             | 3   |     | (cid:3)14(cid:4) |     | (cid:3)18.637.3(cid:4) |     |     | 444,800 |     |
valueitsperformanceindicatorreachedisbetterthanthevalueof
|     |     |     |     |     |     |     |     | 4   |     | (cid:3)21(cid:4) |     | (cid:3)18.636.1(cid:4) |     |     | 474,800 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ---------------------- | --- | --- | ------- | --- |
thisthreshold.Aperformancethresholdbecomesinactiveeitherif
|     |     |     |     |     |     |     |     |     |     | (cid:3)221(cid:4) |     | (cid:3)18.636.145.5(cid:4) |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | -------------------------- | --- | --- | --- | --- |
none of the performance thresholds considered in the optimiza- 5 601,550
.devreser sthgir lla ;ylno esu lanosrep roF .ECSA thgirypoC .31/92/90 no seirarbiL adirolF lartneC fO ytisrevinU yb gro.yrarbilecsa morf dedaolnwoD 6 (cid:3)222(cid:4) (cid:3)18.636.145.5(cid:4) 542,540
tionarereachedoriftheotherperformancethresholdsarealways
|         |        |               |            |     |     |     |     |     |     | (cid:3)224(cid:4) |     | (cid:3)18.636.145.5(cid:4) |     |     |         |     |
| ------- | ------ | ------------- | ---------- | --- | --- | --- | --- | --- | --- | ----------------- | --- | -------------------------- | --- | --- | ------- | --- |
| reached | before | this inactive | threshold. |     |     |     |     | 7   |     |                   |     |                            |     |     | 495,340 |     |
A commonly used EM optimization method states that the 8 (cid:3)241(cid:4) (cid:3)18.636.145.1(cid:4) 546,280
optimumEMoptiontoapplyatatimeaperformancethresholdis 9 (cid:3)242(cid:4) (cid:3)18.636.145.1(cid:4) 486,790
10a
reached is the one providing the lowest present cost per year of [41] [18.635.9] 395,350
increase in service life. This method was proposed by Estes and 11 (cid:3)421(cid:4) (cid:3)18.635.945.4(cid:4) 522,210
Frangopol (cid:1)1999(cid:2), used in Yang et al. (cid:1)2006(cid:2) and extended for 12 (cid:3)422(cid:4) (cid:3)18.635.945.4(cid:4) 463,080
multiple performance measures in Okasha and Frangopol (cid:3)424(cid:4) (cid:3)18.635.945.4(cid:4)
|     |     |     |     |     |     |     |     | 13  |     |     |     |     |     |     | 415,790 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- |
(cid:1)2010a(cid:2),
where a detailed algorithm is presented. In this study, 14 (cid:3)441(cid:4) (cid:3)18.635.944.0(cid:4) 470,710
this method is denoted by EMO1. (cid:3)442(cid:4) (cid:3)18.635.944.0(cid:4)
|        |      |        |        |          |     |            |          | 15  |     |     |     |     |     |     | 409,910 |     |
| ------ | ---- | ------ | ------ | -------- | --- | ---------- | -------- | --- | --- | --- | --- | --- | --- | --- | ------- | --- |
| Method | EMO1 | relies | on the | embedded |     | assumption | that the |     |     |     |     |     |     |     |         |     |
aOptimumsolution.
servicelifeextensionofferedbyanEMoptionisthesameregard-
| less of    | when it   | is applied. | For       | example,       | if  | an EM   | option that  |     |     |     |     |     |     |     |     |     |
| ---------- | --------- | ----------- | --------- | -------------- | --- | ------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| requires   | replacing | a given     | part      | of a structure |     | extends | the service  |     |     |     |     |     |     |     |     |     |
| life for a | given     | number      | of years, | the method     |     | assumes | that if this |     |     |     |     |     |     |     |     |     |
EMoptionisappliedagainaftertheendoftheeffectperiodofthe point ensures that the service life extension provided by the ap-
first application it will provide the same service life extension as plication of any given EM application is larger than a minimum
|     |     |     |     |     |     |     |     | toleranceTOL.The |     | steps | of the | algorithm | are | the following: |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ----- | ------ | --------- | --- | -------------- | --- | --- |
thefirstapplication.However,thisassumptionmaynotalwaysbe
|          |           |          |     |       |       |        |               | 1. INITIALIZE: |     | sort the | EM  | options | in the | order | of increasing |     |
| -------- | --------- | -------- | --- | ----- | ----- | ------ | ------------- | -------------- | --- | -------- | --- | ------- | ------ | ----- | ------------- | --- |
| true. In | the given | example, | the | other | parts | of the | structure are |                |     |          |     |         |        |       |               |     |
naturally deteriorating perhaps at a time-varying rate. cost,andassignthemarankingnumberraccordingly,where
An alternative method compares the total cost of all EM sce- r=1,2,...,n,andn=numberofconsideredEMoptions.Set
|     |     |     |     |     |     |     |     | i=1, | j=0, | k=1, T(cid:1)1,0(cid:2)=0, |     | LCC(cid:1)1,0(cid:2)=0, |     | t=0. | Assign | a   |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- | -------------------------- | --- | ----------------------- | --- | ---- | ------ | --- |
nariosrequiredtoprovideaprespecifiedservicelifefromstartto
end by an event-tree analysis. The resulting large number of “very large” value to LCC opt .
branches (cid:1)i.e., EM scenarios(cid:2) to analyze can become a computa- 2. INCREMENT t and analyze the performance at this incre-
| tional burden     | for | solving    | the problem |                | even for | a limited   | number | ment. |               |           |     |             |     |         |     |     |
| ----------------- | --- | ---------- | ----------- | -------------- | -------- | ----------- | ------ | ----- | ------------- | --------- | --- | ----------- | --- | ------- | --- | --- |
|                   |     |            |             |                |          |             |        | 3. If | a performance | threshold |     | is reached, | go  | to Step | 5.  |     |
| of EM options.The |     | difficulty |             | in programming |          | this method | stems  |       |               |           |     |             |     |         |     |     |
t(cid:7)specified
fromthefactthatneitherthenumberofbranchesnorthelengthof 4. If service life, go to Step 11; otherwise go to
| each branch | is  | known before |     | the end | of the | analysis. | Therefore, | Step | 2.  |     |     |     |     |     |     |     |
| ----------- | --- | ------------ | --- | ------- | ------ | --------- | ---------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
thefollowingalgorithmisproposedforefficientlyperformingthe 5. j=j+1. k=1, M(cid:1)i,j(cid:2)=k. T(cid:1)i,j(cid:2)=t.
event-tree analysis for EM optimization and is denoted herein as CHECKPOINT T(cid:1)i,j(cid:2)−T(cid:1)i,j−1(cid:2)(cid:7)TOL
|       |     |     |     |     |     |     |     | 6.     |     | 1:         | if  |     |     | continue; |     | oth- |
| ----- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | ---------- | --- | --- | --- | --------- | --- | ---- |
| EMO2. |     |     |     |     |     |     |     | erwise | go  | to Step 9. |     |     |     |           |     |      |
The goal of the EMO2 algorithm is to identify the ids and 7. CHECKPOINT 2: calculate LCC(cid:1)i,j(cid:2). If LCC(cid:1)i,j(cid:2)(cid:3)LCC
opt
times of applications of the EM options in all scenarios M(cid:1)i,j(cid:2) gotoStep12;otherwiseapplyEMoptionwithr=kattimet;
| and T(cid:1)i,j(cid:2), | respectively, |     | where | M(cid:1)i,j(cid:2) | represents | the | id of the |      |     |            |     |     |     |     |     |     |
| ----------------------- | ------------- | --- | ----- | ------------------ | ---------- | --- | --------- | ---- | --- | ---------- | --- | --- | --- | --- | --- | --- |
|                         |               |     |       |                    |            |     |           | then | go  | to Step 2. |     |     |     |     |     |     |
t=T(cid:1)i,j(cid:2);
maintenance option to use at the jth application in the ith main- 8. If k=n continue; otherwise k=k+1, then go to
T(cid:1)i,j(cid:2)
| tenance   | scenario    | and         | represents |          | its time | of application. | In          | Step | 7.     |     |     |     |     |     |     |     |
| --------- | ----------- | ----------- | ---------- | -------- | -------- | --------------- | ----------- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- |
| addition, | the optimum | maintenance |            | scenario |          | M and           | its associ- | 9.   | j=j−1. |     |     |     |     |     |     |     |
opt
ated optimum life-cycle maintenance cost LCC are identified. k=M(cid:1)i,j(cid:2);
|     |     |     |     |     |     | opt |     | 10. If | j=0 STOP;                      | otherwise |     |     | then                   | go to Step | 8.  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ------------------------------ | --------- | --- | --- | ---------------------- | ---------- | --- | --- |
|     |     |     |     |     |     |     |     |        | LCC(cid:1)i,j(cid:2)(cid:6)LCC |           |     |     | =LCC(cid:1)i,j(cid:2), |            |     |     |
Themethodissupportedwithcheckpointsthatpredictandtermi- 11. If ; then LCC M =i.
|     |     |     |     |     |     |     |     |     |     |     | opt | opt |     |     | opt |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
natethecontinuationofnonoptimumbranchesandpreventcreat- 12. If j=0 STOP; otherwise k=M(cid:1)i,j(cid:2), i=i+1, M(cid:1)i,z(cid:2)=M(cid:1)i
ing new branches known a priori to be nonoptimum. The first −1,z(cid:2), T(cid:1)i,z(cid:2)=T(cid:1)i−1,z(cid:2), where z=1,2,...j; then go to
| checkpoint | compares | the | partial | life-cycle | cost | (cid:1)LCC(cid:2) | up to the |     |     |     |     |     |     |     |     |     |
| ---------- | -------- | --- | ------- | ---------- | ---- | ----------------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Step 8.
| jth |     | ith |     |     |     | LCC(cid:1)i,j(cid:2), |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
application of the maintenance scenario, with This algorithm is illustrated in the following example. An
theminimum(cid:1)optimum(cid:2)LCCvaluefounduptothatpointinthe
|     |     |     |     |     |     |     |     | unavailability |     | threshold | is specified |     | as 10−2 | for the | Colorado |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --------- | ------------ | --- | ------- | ------- | -------- | --- |
optimization process, LCC . LCC(cid:1)i,j(cid:2) is calculated as BridgeE-17-AHandtheservicelifeisspecifiedas50years.The
opt
|     |     |     |     |     |     |     |     | algorithm | of  | EMO2 is | implemented | and | the | results | are shown | in           |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------- | ----------- | --- | --- | ------- | --------- | ------------ |
|     |     |     |     | j   |     |     |     |           |     |         |             |     |     |         |           | (cid:1)i.e., |
(cid:9) C(cid:14)M(cid:1)i,y(cid:2)(cid:15) Table 1. It is noted that the application of EM option 3
|     |     | LCC(cid:1)i,j(cid:2)= |     |     |     |     | (cid:1)11(cid:2) |     |     |     |     |     |     |     |     |     |
| --- | --- | --------------------- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:1)1+(cid:8)(cid:2)T(cid:1)i,y(cid:2) replace the exterior girders(cid:2) extends the service life for a very
y=1 short amount of time and therefore it always fails at CHECK-
C(cid:14)M(cid:1)i,y(cid:2)(cid:15)=cost (cid:1)where considered(cid:2).
where of the yth maintenance application of POINT 1 TOL=2years is Scenario 10 pro-
the ith EM scenario; T(cid:1)i,y(cid:2) is its time of application; and vides the solution with the lowest total LCC and thus it is the
(cid:8)=discount rate of money (cid:1)2% in this study(cid:2).The second check- optimum maintenance strategy.
JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010/1013
J. Struct. Eng. 2010.136:1009-1022.

.devreser sthgir lla ;ylno esu lanosrep roF .ECSA thgirypoC .31/92/90 no seirarbiL adirolF lartneC fO ytisrevinU yb gro.yrarbilecsa morf dedaolnwoD
|     |     |     |     | Fig. | 3. (cid:1)a(cid:2) | Schedules | of  | maintenance |     | application; | (cid:1)b(cid:2) history | pro- |
| --- | --- | --- | --- | ---- | ------------------ | --------- | --- | ----------- | --- | ------------ | ----------------------- | ---- |
filesforthecumulativemaintenancecostfortheselectedsolutionsof
EM
|     |     |     |     | However, |     | “all feasible | solutions |     | are nondominated |     | and | the only |
| --- | --- | --- | --- | -------- | --- | ------------- | --------- | --- | ---------------- | --- | --- | -------- |
roleplayedbyGAisfindingasetofsolutionsaswelldistributed
|     |     |     |     | (cid:1)i.e., | a set       | of evenly    | distributed |               | solutions  | in the            | objective   | space(cid:2) |
| --- | --- | --- | --- | ------------ | ----------- | ------------ | ----------- | ------------- | ---------- | ----------------- | ----------- | ------------ |
|     |     |     |     | as           | possible”   | (cid:1)Neves | et al.      | 2006a(cid:2). | In         | this example,     | the         | effect of    |
|     |     |     |     | the          | performance | thresholds   |             | on            | the LCC    | is analyzed       | by enumara- |              |
|     |     |     |     | tively       | varying     | the          | values      | of the        | thresholds | of unavailability |             | and          |
redundancy,andperformingtheEMoptimizationtofindthecor-
Fig.2.Effectoftheunavailabilityandredundancythresholdsonthe responding LCC associated with the optimum maintenance solu-
life-cyclecostforoptimumEMusing(cid:1)a(cid:2)methodEMO1;(cid:1)b(cid:2)method tion. Both EM optimization methods EMO1 and EMO2 are used
| EMO2 |     |     |     | separately.Theservicelifeofthebridgeisnowconsideredas75 |     |     |     |     |     |     |     |     |
| ---- | --- | --- | --- | ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
years.
|     |     |     |     |     | Figs. | 2(cid:1)a(cid:2) and | 2(cid:1)b(cid:2) | show | the results | obtained | by  | methods |
| --- | --- | --- | --- | --- | ----- | -------------------- | ---------------- | ---- | ----------- | -------- | --- | ------- |
Needlesstosay,oneofthedecidingfactorsindeterminingthe EMO1 and EMO2, respectively. Fig. 2(cid:1)b(cid:2) shows the consistency
optimumstrategyisthevaluesoftheperformancethresholds.For in method EMO2 in that by improving the unavailability and/or
anysetofperformancethresholds,anoptimummaintenancestrat- the redundancy threshold the associated LCC either increases or
egy exists. Standard or codified performance thresholds do not remains the same. The increase in LCC with improving both the
exist thus far. Therefore, it may be desired to understand the in- unavailability and redundancy implies that both their thresholds
teraction among the performance thresholds and the LCC re- are active. Improving either threshold with same LCC indicates
quiredforamaintenancestrategythatmaintainsthesethresholds. that the improved threshold is inactive. However, numerous
Nevesetal.(cid:1)2006a(cid:2)treatedtheperformancethresholdasadesign spikesandregionsinFig.2(cid:1)a(cid:2)withhigherLCCthantheircorre-
variable in a multiobjective optimization problem solved by GA. sponding regions in Fig. 2(cid:1)b(cid:2) show that method EMO1 can yield
Table2.RepresentativeEMSolutionsUsingEMO2fortheColoradoBridgeE-17-AH
|     | Unavailability |           | Redundancy |     | Maximum        |     |     |     | Minimum    |     |     |     |
| --- | -------------- | --------- | ---------- | --- | -------------- | --- | --- | --- | ---------- | --- | --- | --- |
|     |                | threshold | threshold  |     | unavailability |     |     |     | redundancy |     |     | LCC |
(cid:1)An (cid:2) (cid:1)RI (cid:2) (cid:1)An (cid:2) (cid:1)RI (cid:2) (cid:1)$(cid:2)
| Solution |     | th      | th     |     |         | max |     |     | min    |     |           |         |
| -------- | --- | ------- | ------ | --- | ------- | --- | --- | --- | ------ | --- | --------- | ------- |
|          |     | 10−1.00 | 101.00 |     | 10−1.06 |     |     |     | 101.00 |     |           |         |
| A1       |     |         |        |     |         |     |     |     |        |     |           | 199,410 |
| B1       |     | 10−2.00 | 102.00 |     | 10−2.00 |     |     |     | 102.00 |     |           | 657,880 |
| C1       |     | 10−3.00 | 104.00 |     | 10−3.00 |     |     |     | 104.01 |     | 1,830,100 |         |
1014/JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010
J. Struct. Eng. 2010.136:1009-1022.

.devreser sthgir lla ;ylno esu lanosrep roF .ECSA thgirypoC .31/92/90 no seirarbiL adirolF lartneC fO ytisrevinU yb gro.yrarbilecsa morf dedaolnwoD
Fig.5.HistoryprofilesofredundancyforselectedEMsolutions:(cid:1)a(cid:2)
| Fig. 4. History | profiles | of  | unavailability | for | selected | EM solutions: |     |     |     |     |     |     |     |     |
| --------------- | -------- | --- | -------------- | --- | -------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
SolutionA1;(cid:1)b(cid:2)SolutionB1;and(cid:1)c(cid:2)SolutionC1
(cid:1)a(cid:2)SolutionA1;(cid:1)b(cid:2)SolutionB1;and(cid:1)c(cid:2)SolutionC1
|           |              |         |          |               |     |             | Multiobjective |     | Optimization |     | of Maintenance |     |     |     |
| --------- | ------------ | ------- | -------- | ------------- | --- | ----------- | -------------- | --- | ------------ | --- | -------------- | --- | --- | --- |
|           |              |         |          |               |     |             | Considering    | PM  | Only         |     |                |     |     |     |
| solutions | that are not | in fact | optimum. | Nevertheless, |     | most of the |                |     |              |     |                |     |     |     |
surfaceinFig.2(cid:1)a(cid:2)foundbyEMO1appearstobethesameasthe By aiming to find an optimum maintenance solution considering
corresponding parts of the surface in Fig. 2(cid:1)b(cid:2) found by EMO2. onlyPMactions,twoquestionsareposed:whataretheoptimum
Therefore,methodEMO1hastheabilitytoprovideoptimumso- times of application of each PM type and what is the optimum
lutions in most cases. However, EMO2 is always more accurate number of PM applications of each type? Treating the times of
and will be used for the rest of this study. application of PM as design variables answers the first question,
|       |             |            |     |         |         |             | but the second | question |     | is posed | again as: | what | is the | number of |
| ----- | ----------- | ---------- | --- | ------- | ------- | ----------- | -------------- | -------- | --- | -------- | --------- | ---- | ------ | --------- |
| Three | maintenance | solutions, |     | A1, B1, | and C1, | obtained by |                |          |     |          |           |      |        |           |
method EMO2 are examined. Table 2 shows the unavailability designvariablestousefortheoptimumtimesofPMapplication?
Inthisstudy,thisquestionisansweredbyusinganintegerdesign
| An th andredundancyRI |     | th  | thresholdsforthesesolutionsalongwith |     |     |     |     |     |     |     |     |     |     |     |
| --------------------- | --- | --- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
variablethatrepresentstheoptimumnumberofPMapplications.
| the maximum | unavailability |     | An  | and | minimum | redundancy |     |     |     |     |     |     |     |     |
| ----------- | -------------- | --- | --- | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
max This integer design variable takes values from 0 to n , where
RI achieved throughout the 75 years of service life and the p
min
|     |     |     |     |     |     |     | n p =number | of time-of-application |     |     | design | variables | for | the given |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ---------------------- | --- | --- | ------ | --------- | --- | --------- |
associatedLCC.Itcanbeobservedinthevaluesofthistablethat
|                 |                |                |             |                  |                  |          | PM type        | considered     | in the       | problem,     | which     | should     | be   | the maxi-  |
| --------------- | -------------- | -------------- | ----------- | ---------------- | ---------------- | -------- | -------------- | -------------- | ------------ | ------------ | --------- | ---------- | ---- | ---------- |
| the performance | threshold      |                | may not     | be reached       | (cid:1)inactive  | thresh-  |                |                |              |              |           |            |      |            |
|                 |                |                |             |                  |                  |          | mum desired    | number         | of           | applications |           | for this   | PM   | type. This |
| old(cid:2) and  | the worst      | value          | for the     | performance      | indicator        | in such  |                |                |              |              |           |            |      |            |
|                 |                |                |             |                  |                  |          | implies that   | at             | each design  | point,       | a         | number     | of   | the time-  |
|                 |                |                |             | 3(cid:1)a(cid:2) | 3(cid:1)b(cid:2) |          |                |                |              |              |           |            |      |            |
| case is         | better than    | its threshold. |             | Figs.            | and              | show the |                |                |              |              |           |            |      |            |
|                 |                |                |             |                  |                  |          | of-application | design         | variables    | are          | inactive, | i.e.,      | have | no contri- |
| schedules       | of maintenance |                | application | and history      | profiles         | for the  |                |                |              |              |           |            |      |            |
|                 |                |                |             |                  |                  |          | bution to      | the evaluation |              | of the       | objective | functions. |      | Instead of |
| cumulative      | maintenance    |                | cost for    | the selected     | solutions,       | respec-  |                |                |              |              |           |            |      |            |
|                 |                |                |             |                  |                  |          | performing     | the            | optimization | multiple     | times,    | where      | each | time a     |
(cid:1)i.e.,
tively. It can be seen that EM option 3 replace the exterior different number of time-of-application design variables is used,
girders(cid:2) is not used in the three solutions since this EM option and at the end the optimum solution is found, the combinatorial
| does not | extend the | service | life for | a significant | amount | of time. |         |              |     |            |     |        |                 |     |
| -------- | ---------- | ------- | -------- | ------------- | ------ | -------- | ------- | ------------ | --- | ---------- | --- | ------ | --------------- | --- |
|          |            |         |          |               |        |          | problem | is performed | at  | once using | the | number | of applications |     |
Figs. 4 and 5 show the history profiles of the selected EM solu- integer design variable.To the best of our knowledge, this is the
tions for the unavailability and redundancy, respectively. first time an optimization problem is solved by activation and
JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010/1015
J. Struct. Eng. 2010.136:1009-1022.

.devreser sthgir lla ;ylno esu lanosrep roF .ECSA thgirypoC .31/92/90 no seirarbiL adirolF lartneC fO ytisrevinU yb gro.yrarbilecsa morf dedaolnwoD
Fig.6.(cid:1)a(cid:2)Three-dimensionalPareto-optimalsetofPM;(cid:3)(cid:1)b(cid:2)–(cid:1)d(cid:2)(cid:4)itsprojectionsinthebidimensionalspace
deactivation of design variables based on the values of other de- between any two consecutive maintenance applications of the
signvariables.TherobustnessofGAsprovidesauniqueabilityto same type is required.Accordingly, the formulation of the prob-
solve such a cumbersome optimization problem. lem is stated as follows.
The PM optimization is based on two structural performance Find: Td, Nd, Tg, Ng.
i j
|                                                          |              |                   |            |             |                  |          | To achieve | the following three | objectives |     |                   |
| -------------------------------------------------------- | ------------ | ----------------- | ---------- | ----------- | ---------------- | -------- | ---------- | ------------------- | ---------- | --- | ----------------- |
| indicators,                                              | the lifetime | unavailability    | and        | lifetime    | redundancy.      |          |            |                     |            |     |                   |
| These performance                                        | indicators   | are               | introduced | in          | the optimization |          |            |                     |            |     |                   |
|                                                          |              |                   |            |             |                  |          |            | MinimizeAn          |            |     | (cid:1)12a(cid:2) |
| processascriteria.Thegoaloftheoptimizationistoimprovethe |              |                   |            |             |                  |          |            |                     |            | max |                   |
| worst values                                             | reached for  | these performance |            | indicators. |                  | In other |            |                     |            |     |                   |
(cid:1)12b(cid:2)
words, one objective is to minimize the maximum (cid:1)worst(cid:2) value MaximizeRI
min
| reached | for the unavailability | throughout |     | the service |     | life An |     |     |     |     |                   |
| ------- | ---------------------- | ---------- | --- | ----------- | --- | ------- | --- | --- | --- | --- | ----------------- |
|         |                        |            |     |             |     | m a x   |     |     |     |     | (cid:1)12c(cid:2) |
andtheotherobjectiveistomaximizetheminimum(cid:1)worst(cid:2)val u e MinimizeLCC
| reachedfortheredundancythroughouttheservicelifeRI |                |     |              |     |          | .The    |            |                 |           |     |                   |
| ------------------------------------------------- | -------------- | --- | ------------ | --- | -------- | ------- | ---------- | --------------- | --------- | --- | ----------------- |
|                                                   |                |     |              |     |          | min     | Subject to | the constraints |           |     |                   |
| third objective                                   | is to minimize | the | LCC required |     | to apply | mainte- |            |                 |           |     |                   |
|                                                   |                |     |              |     |          |         |            | 2(cid:5)Td      | (cid:5)73 |     | (cid:1)12d(cid:2) |
nance activities resulting in achieving these values of An max and i
| RI .The | service life of | the structure | is  | considered | as  | 75 years. |     |     |     |     |     |
| ------- | --------------- | ------------- | --- | ---------- | --- | --------- | --- | --- | --- | --- | --- |
min
Two PM types are considered in this study: silane treatment 2(cid:5)Tg (cid:5)73 (cid:1)12e(cid:2)
j
andgirderrepainting.Amaximumof10applicationsofeachPM
typeisallowed.Therefore,20continuoustime-of-applicationde- Td −Td (cid:7)2 (cid:1)12f(cid:2)
|                |                                         |           |     |          |           |         |     | i   | i−1 |     |     |
| -------------- | --------------------------------------- | --------- | --- | -------- | --------- | ------- | --- | --- | --- | --- | --- |
| sign variables | are used,                               | namely 10 | for | the time | of silane | treat-  |     |     |     |     |     |
| ments of       | the deck Td (cid:1)i=1,2,...,10(cid:2), |           |     | and 10   | for the   | time of |     |     |     |     |     |
i
girder repaintings Tg (cid:1)j=1,2,...,10(cid:2). In addition, two number- Table 3. Selected Representative PM Pareto-Optimal Solutions for the
j
ColoradoBridgeE-17-AH
of-applicationsintegerdesignvariablesareused;oneforthenum-
berofapplicationsofthesilanetreatmentforthedeckNd(cid:1)where
|     |     |     |     |     |     |     |     | Maximum |     | Minimum |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------- | --- |
Nd=0,1,2,...,10(cid:2),andoneforthenumberofapplicationsofthe
|     |     |     |     |     |     |     |     | unavailability |     | redundancy | LCC |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ---------- | --- |
girder repaintings Ng (cid:1)where Ng=0,1,2,...,10(cid:2). (cid:1)An (cid:2) (cid:1)RI (cid:2) (cid:1)$(cid:2)
|               |                |             |                 |         |        |          | Solution | max     |     | min    |         |
| ------------- | -------------- | ----------- | --------------- | ------- | ------ | -------- | -------- | ------- | --- | ------ | ------- |
| It is desired | not to apply   | maintenance |                 | anytime | in the | first or |          |         |     |        |         |
|               |                |             |                 |         |        |          |          | 10−1.00 |     | 100.67 |         |
|               |                |             |                 |         |        |          | A2       |         |     |        | 76,720  |
| last 2 years  | of the service | life of the | structure.Thus, |         | the    | applica- |          |         |     |        |         |
|               |                |             |                 |         |        |          | B2       | 10−1.22 |     | 103.60 | 561,913 |
tiontimedesignvariablesareonlyallowedtovaryfromtheyear
|          |                       |           |     |      |         |         | C2  | 10−1.99 |     | 103.40 | 734,588 |
| -------- | --------------------- | --------- | --- | ---- | ------- | ------- | --- | ------- | --- | ------ | ------- |
| 2 to the | year 73. In addition, | a minimum |     | time | span of | 2 years |     |         |     |        |         |
1016/JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010
J. Struct. Eng. 2010.136:1009-1022.

.devreser sthgir lla ;ylno esu lanosrep roF .ECSA thgirypoC .31/92/90 no seirarbiL adirolF lartneC fO ytisrevinU yb gro.yrarbilecsa morf dedaolnwoD
Fig.7.(cid:1)a(cid:2)Schedulesofmaintenanceapplication;(cid:1)b(cid:2)historyprofiles
forthecumulativemaintenancecostfortheselectedsolutionsofPM
Fig.9.HistoryprofilesofredundancyforselectedPMsolutions:(cid:1)a(cid:2)
SolutionA2;(cid:1)b(cid:2)SolutionB2;and(cid:1)c(cid:2)SolutionC2
|     |     |     |     |     |     |     | Tg −Tg                        | (cid:7)2 |     |     | (cid:1)12g(cid:2) |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------- | -------- | --- | --- | ----------------- |
|     |     |     |     |     |     |     | j                             | j−1      |     |     |                   |
|     |     |     |     |     |     |     | Nd=(cid:6)0,1,2,...,10(cid:7) |          |     |     | (cid:1)12h(cid:2) |
|     |     |     |     |     |     |     | Ng=(cid:6)0,1,2,...,10(cid:7) |          |     |     | (cid:1)12i(cid:2) |
where i,j=1,2,...,10.
|     |     |     |     | An advanced       |     | GA called | nondominated |        | sorting | GA         | with con- |
| --- | --- | --- | --- | ----------------- | --- | --------- | ------------ | ------ | ------- | ---------- | --------- |
|     |     |     |     | trolled elitisms, |     | NSGA-II,  | has          | gained | much    | popularity | since its |
appearance(cid:1)Debetal.2002;Deb2001(cid:2).TheNSGA-IIalgorithm
|     |     |     |     | for multiobjective |           | optimization      |     | is used | to solve       | the above | prob-  |
| --- | --- | --- | --- | ------------------ | --------- | ----------------- | --- | ------- | -------------- | --------- | ------ |
|     |     |     |     | lem. The           | resulting | three-dimensional |     |         | Pareto-optimal | set       | of the |
optimizationproblemisshowninFig.6(cid:1)a(cid:2).Projectionsofthisset
6(cid:1)b–d(cid:2).
|     |     |     |     | in the bidimensional |     |     | space are | also | presented | in Figs. |     |
| --- | --- | --- | --- | -------------------- | --- | --- | --------- | ---- | --------- | -------- | --- |
Threerepresentativesolutions(cid:1)A2,B2,andC2(cid:2)selectedfromthe
|     |     |     |     | Pareto-optimal |       | set are  | also shown | on   | the figure. | The interaction |           |
| --- | --- | --- | --- | -------------- | ----- | -------- | ---------- | ---- | ----------- | --------------- | --------- |
|     |     |     |     | among the      | three | criteria | indicates  | that | improving   | either          | An max or |
RI usingPMdoesnotalwaysimprovetheother.Ingeneral,the
min
|     |     |     |     | increase | in LCC | is relatively |     | higher with | improving | An  | than |
| --- | --- | --- | --- | -------- | ------ | ------------- | --- | ----------- | --------- | --- | ---- |
max
|     |     |     |     | with improving |     | RI  | (cid:1)i.e., it | is less expensive |     | to improve | RI  |
| --- | --- | --- | --- | -------------- | --- | --- | --------------- | ----------------- | --- | ---------- | --- |
|     |     |     |     |                |     | min |                 |                   |     |            | min |
An (cid:2).
|     |     |     |     | than to improve          |     | max | Solutions | between                     | A2  | and B2 | improve |
| --- | --- | --- | --- | ------------------------ | --- | --- | --------- | --------------------------- | --- | ------ | ------- |
|     |     |     |     | immenselywithrespecttoRI |     |     |           | withlittleornoimprovementin |     |        |         |
min
|     |     |     |     | An . On | the other | hand, | solutions | between |     | B2 and C2 | improve |
| --- | --- | --- | --- | ------- | --------- | ----- | --------- | ------- | --- | --------- | ------- |
max
|                 |                            |              |               | greatly in   | An          | with little | or       | no improvement |          | in RI .This | can    |
| --------------- | -------------------------- | ------------ | ------------- | ------------ | ----------- | ----------- | -------- | -------------- | -------- | ----------- | ------ |
|                 |                            |              |               |              | max         |             |          |                |          | min         |        |
|                 |                            |              |               | be justified | as follows. |             |          |                |          |             |        |
|                 |                            |              |               | On one       | hand,       | the         | deck has | more           | relative | importance  | to the |
| Fig. 8. History | profiles of unavailability | for selected | PM solutions: |              |             |             |          |                |          |             |        |
systemunavailabilitymodelthanthegirderssinceitisconnected
(cid:1)a(cid:2)SolutionA2;(cid:1)b(cid:2)SolutionB2;and(cid:1)c(cid:2)SolutionC2
|     |     |     |     | separately | to the | system | in series.Therefore, |     |     | improving | the gird- |
| --- | --- | --- | --- | ---------- | ------ | ------ | -------------------- | --- | --- | --------- | --------- |
JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010/1017
J. Struct. Eng. 2010.136:1009-1022.

.devreser sthgir lla ;ylno esu lanosrep roF .ECSA thgirypoC .31/92/90 no seirarbiL adirolF lartneC fO ytisrevinU yb gro.yrarbilecsa morf dedaolnwoD
Fig.10.(cid:1)a(cid:2)Three-dimensionalPareto-optimalsetofcombinedEMandPM;(cid:3)(cid:1)b(cid:2)–(cid:1)d(cid:2)(cid:4)itsprojectionsinthebidimensionalspace
ersbyrepaintingthemprovideslittleimprovementtoAn max while quent PM applications associated with a higher LCC. Although,
improving the deck by the silane treatment greatly improves the cost of girder repainting is twice the cost of silane treatment,
An . On the other hand, the deck is removed from the redun- Solution B2 has used the 10 allowed girder repaintings while
max
dancy system model. Thus, repainting the girders greatly im- using only two silane treatments. Solution C2 applies also 10
proves RI , while silane treatment does not affect RI . girderrepaintings,inadditionto10silanetreatments.Sincesilane
min min
Accordingly, by moving from SolutionA2 to Solution B2, more treatmentdoesnotimproveRI andthetimesofgirderrepaint-
min
girder repaintings are applied and thus RI is relatively im- ingsaredifferentinSolutionB2fromC2,RI inSolutionC2is
|     | min |     |     | min |     |
| --- | --- | --- | --- | --- | --- |
provedmuchmorerapidlythanAn is.Furthermore,bymoving lower than in Solution B2. However, An is better.
max max
from Solution B2 to Solution C2, more silane treatments are ap- Figs. 8 and 9 show the history profiles of the selected PM
pliedandthusAn isrelativelyimprovedrapidlywhileRI is solutionsfortheunavailabilityandredundancy,respectively.Itis
| max |     | min |     |     |     |
| --- | --- | --- | --- | --- | --- |
not improved. clear in the figures how the application of silane treatment
Table 3 shows the values of the obtained objective functions changestheslope(cid:1)rateofchange(cid:2)oftheunavailabilitycurvesand
for the selected solutions A2, B2, and C2. Clearly, Solution B2 how the girder repaintings change the slope of the redundancy
has better RI min than Solution C2 but worse An max . Both solu- curves. For instance, SolutionA2 shows that the change in slope
tionsB2andC2arebetterthanA2inavailabilityandredundancy. ofitsredundancycurveduetothesilanetreatmentisinsignificant
Figs.7(cid:1)a(cid:2)and7(cid:1)b(cid:2)showtheschedulesofmaintenanceapplication (cid:3)see the effects of the first PM application on the redundancy in
and history profiles for the cumulative maintenance cost for the Fig. 9(cid:1)a(cid:2)(cid:4). The change in slope of its unavailability curve, how-
(cid:3)see 8(cid:1)a(cid:2)(cid:4).
selected solutions of PM, respectively. In general, it is evident in ever, is evident Fig. On the other hand, Solution B2
thefigurethatimprovingAn requiresadditionalandmorefre- shows that the change in slope of its unavailability curve due to
max
Table4.SelectedRepresentativeCombinedPMandEMPareto-OptimalSolutionsfortheColoradoBridgeE-17-AH
|     | Unavailability | Redundancy | Maximum        | Minimum    |     |
| --- | -------------- | ---------- | -------------- | ---------- | --- |
|     | threshold      | threshold  | unavailability | redundancy | LCC |
Solution (cid:1)An (cid:2) (cid:1)RI (cid:2) (cid:1)An (cid:2) (cid:1)RI (cid:2) (cid:1)$(cid:2)
|     | th      | th     | max     | min    |           |
| --- | ------- | ------ | ------- | ------ | --------- |
| A3  | 10−1.00 | 101.00 | 10−1.00 | 101.01 | 106,764   |
|     | 10−1.39 | 103.53 | 10−1.82 | 103.53 |           |
| B3  |         |        |         |        | 761,464   |
| C3  | 10−2.64 | 104.00 | 10−2.64 | 104.73 | 1,533,273 |
| D3  | 10−3.00 | 104.00 | 10−3.00 | 104.00 | 1,863,516 |
1018/JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010
J. Struct. Eng. 2010.136:1009-1022.

|     |     |     |     |     |     |     | using EMO2      | for      | each   | design | point       | (cid:1)i.e., | nesting      | EMO2 | into    |
| --- | --- | --- | --- | --- | --- | --- | --------------- | -------- | ------ | ------ | ----------- | ------------ | ------------ | ---- | ------- |
|     |     |     |     |     |     |     | NSGA-II(cid:2). | In other | words, | the    | maintenance |              | optimization |      | is per- |
formedontwolevels:global(cid:1)NSGA-II(cid:2)andlocal(cid:1)EMO2(cid:2).Each
timetheglobaldesignvariablesareprovided,alocaloptimization
|     |     |     |     |     |     |     | (cid:1)EMO2(cid:2) | takes place | to        | find the     | optimum      | set | of EM     | applications, |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | ----------- | --------- | ------------ | ------------ | --- | --------- | ------------- | --- |
|     |     |     |     |     |     |     | given the          | presence    | of        | the PM       | applications |     | and       | satisfying    | the |
|     |     |     |     |     |     |     | given thresholds.  |             | The local | optimization |              | is  | performed | during        | the |
objectivefunctionsevaluationofeachglobaloptimizationdesign
solution.Basedontheresultsofthelocaloptimization,theworst
valuesoftheperformanceindicatorsthroughouttheservicelifeof
thestructureandtheLCCarereturnedtotheglobaloptimization
.devreser sthgir lla ;ylno esu lanosrep roF .ECSA thgirypoC .31/92/90 no seirarbiL adirolF lartneC fO ytisrevinU yb gro.yrarbilecsa morf dedaolnwoD
|     |     |     |     |     |     |     | as values    | of the      | considered | objective     |                | functions.   | The           | global       | opti-   |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ----------- | ---------- | ------------- | -------------- | ------------ | ------------- | ------------ | ------- |
|     |     |     |     |     |     |     | mization     | is thus     | able to    | find          | the best       | set of       | PM            | applications | to      |
|     |     |     |     |     |     |     | fulfill the  | thresholds, | provided   |               | that EM        | applications |               | may          | also be |
|     |     |     |     |     |     |     | applied      | and their   | set is     | determined    | by             | the local    | optimization. |              |         |
|     |     |     |     |     |     |     | As mentioned |             | above,     | a set         | of performance |              | thresholds    |              | is re-  |
|     |     |     |     |     |     |     | quired as    | an input    | to         | this process. |                | With         | the lack      | of standard  |         |
|     |     |     |     |     |     |     | thresholds,  | the         | effects    | of the        | unavailability |              | and           | redundancy   |         |
thresholdsonthevaluesoftheobjectivefunctionsisdesiredtobe
examined.Thiscanberealizedinacombinatorialmanneraspre-
viouslyachievedwiththeEMoptimizationwhereforeachsetof
|     |     |     |     |     |     |     | performance  | thresholds     |            | the GAoptimization |               |            | is performed. |             | How-   |
| --- | --- | --- | --- | --- | --- | --- | ------------ | -------------- | ---------- | ------------------ | ------------- | ---------- | ------------- | ----------- | ------ |
|     |     |     |     |     |     |     | ever, the    | computational  |            | cost required      |               | is clearly | very          | high.Alter- |        |
|     |     |     |     |     |     |     | natively,    | these          | thresholds |                    | are treated   | as         | design        | variables.  |        |
|     |     |     |     |     |     |     | Although     | each threshold |            | set                | is associated | with       | an            | optimal     | solu-  |
|     |     |     |     |     |     |     | tion, the    | goal of        | treating   | them               | as            | design     | variables     | in          | the GA |
|     |     |     |     |     |     |     | optimization | is             | to find    | a well             | distributed   | set        | of optimal    | solutions   |        |
(cid:1)Nevesetal.2006a(cid:2).Therefore,twomorecontinuousdesignvari-
|     |     |     |     |     |     |     | ablesareusedfortheunavailabilitythresholdAn |     |     |     |     |     |     | andtheredun- |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- | ------------ | --- |
th
|     |     |     |     |     |     |     | dancy threshold |     | RI . |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ---- | --- | --- | --- | --- | --- | --- |
th
|     |                 |     |     |     |                 |     | The        | threshold | for the  | unavailability |           | is  | desired        | to range | be-    |
| --- | --------------- | --- | --- | --- | --------------- | --- | ---------- | --------- | -------- | -------------- | --------- | --- | -------------- | -------- | ------ |
|     |                 |     |     |     |                 |     | tween 10−1 | and       | 10−3 and | the            | threshold | for | the redundancy |          | is de- |
|     | (cid:1)a(cid:2) |     |     |     | (cid:1)b(cid:2) |     |            |           |          |                |           |     |                |          |        |
Fig. 11. Schedules of maintenance application; history pro- 101 104.
|     |     |     |     |     |     |     | sired to | range between |     | and |     | However, | in order | to  | reduce |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------- | --- | --- | --- | -------- | -------- | --- | ------ |
filesforthecumulativemaintenancecostfortheselectedsolutionsof
|                 |     |     |     |     |     |     | thesearchspace,theredundancythresholdRI |        |           |        |          |     | designvariableis |       |        |
| --------------- | --- | --- | --- | --- | --- | --- | --------------------------------------- | ------ | --------- | ------ | -------- | --- | ---------------- | ----- | ------ |
| combinedEMandPM |     |     |     |     |     |     |                                         |        |           |        |          |     | th               |       |        |
|                 |     |     |     |     |     |     | replaced                                | by the | auxiliary | design | variable | x   | which            | takes | values |
r
|                                                                                  |                |        |          |          |            |                               | from 0.1    | to 0.4. | The redundancy |     | threshold      |         | is related | to the | vari-            |
| -------------------------------------------------------------------------------- | -------------- | ------ | -------- | -------- | ---------- | ----------------------------- | ----------- | ------- | -------------- | --- | -------------- | ------- | ---------- | ------ | ---------------- |
| thegirderrepaintingsisverysmall(cid:3)seeFig.8(cid:1)b(cid:2)(cid:4).Thechangein |                |        |          |          |            |                               | able x r by |         |                |     |                |         |            |        |                  |
| slope of                                                                         | its redundancy | curve, | however, | is clear | (cid:3)see | Fig. 9(cid:1)b(cid:2)(cid:4). |             |         |                |     |                |         |            |        |                  |
|                                                                                  |                |        |          |          |            |                               |             |         |                | RI  | =10(cid:1)10xr | (cid:2) |            |        | (cid:1)13(cid:2) |
th
|     |     |     |     |     |     |     | In addition, | a minimum |     | time | span | of 2 years | between | any | two |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --------- | --- | ---- | ---- | ---------- | ------- | --- | --- |
Multiobjective Optimization of Maintenance consecutivemaintenanceapplicationsappliedtothesamecompo-
Considering Combined EM and PM nentisrequired.ThisincludesEMand/orPMtypes.Forinstance,
thetimespanbetweenadeckreplacementandasubsequentdeck
The 22 design variables used in the PM optimization above are replacement or silane treatment should not be less than 2 years.
usedinthisproblemformulation.ThustheGAsearchisdirected Accordingly, the formulation of the problem is stated as follows.
to find optimal values for the PM. It is desired to keep the treat- Find: An , x, Td, Nd, Tg, Ng.
|     |     |     |     |     |     |     |     | th  | r i |     | j   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ment of EM as performance-based (cid:1)i.e., only apply EM when a To achieve the following three objectives
reached(cid:2).
| performance | threshold | is  |     | In this case, | it is | difficult to |     |     |     |            |     |     |     |     |                   |
| ----------- | --------- | --- | --- | ------------- | ----- | ------------ | --- | --- | --- | ---------- | --- | --- | --- | --- | ----------------- |
|             |           |     |     |               |       |              |     |     |     | MinimizeAn |     |     |     |     | (cid:1)14a(cid:2) |
use a GA search to obtain the optimum EM solution since the max
numberoftimesathresholdwillbereacheddependsonthecho-
senEMoptionsthroughouttheservicelife.Infact,aGAsearchis MaximizeRI (cid:1)14b(cid:2)
min
notneededforEMoptimization.EithermethodEMO1orEMO2
can be used. Both methods can easily incorporate the effects of MinimizeLCC (cid:1)14c(cid:2)
applyingagivensetofPMoptions.Whileevaluatingtheservice
|                |        |       |             |       |        |             | Subject | to the | constraints |     |     |     |     |     |     |
| -------------- | ------ | ----- | ----------- | ----- | ------ | ----------- | ------- | ------ | ----------- | --- | --- | --- | --- | --- | --- |
| life extension | due to | an EM | application | using | either | method, the |         |        |             |     |     |     |     |     |     |
further extension provided by additional PM applied during that 10−1(cid:5)An (cid:5)10−3 (cid:1)14d(cid:2)
th
| extension | period is | taken | into account. | Method | EMO2 | is used |     |     |     |     |     |     |     |     |     |
| --------- | --------- | ----- | ------------- | ------ | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
here.
|                                                       |     |     |     |     |     |     |     |     |     | 0.1(cid:5)x | (cid:5)0.4 |     |     |     | (cid:1)14e(cid:2) |
| ----------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ---------- | --- | --- | --- | ----------------- |
| Accordingly,foragivensetofperformancethresholdsandset |     |     |     |     |     |     |     |     |     |             | r          |     |     |     |                   |
ofPMapplications,anoptimumEMsolutioncanbefoundusing
EMO2.Thus,combinedmaintenance(cid:1)CM(cid:2)consideringbothEM 2(cid:5)Tm (cid:5)73 (cid:1)14f(cid:2)
i
| and PM | can be optimized |     | with NSGA-II | by  | using the | aforemen- |     |     |     |     |     |     |     |     |     |
| ------ | ---------------- | --- | ------------ | --- | --------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tioned design variables and finding the optimum EM options Tm −Tm (cid:7)2 (cid:1)14g(cid:2)
|     |     |     |     |     |     |     |     |     |     | i   | i−1 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010/1019
J. Struct. Eng. 2010.136:1009-1022.

.devreser sthgir lla ;ylno esu lanosrep roF .ECSA thgirypoC .31/92/90 no seirarbiL adirolF lartneC fO ytisrevinU yb gro.yrarbilecsa morf dedaolnwoD
Fig.12.HistoryprofilesofunavailabilityfortheselectedcombinedEMandPM(cid:1)CM(cid:2)solutions:(cid:1)a(cid:2)SolutionA3;(cid:1)b(cid:2)SolutionB3;(cid:1)c(cid:2)Solution
C3;and(cid:1)d(cid:2)SolutionD3
Nd=(cid:6)0,1,2,...,10(cid:7) (cid:1)14h(cid:2) abilityandredundancytotheirthresholds.Oncetheunavailability
|     |     |     |     |     |     |     |     | threshold | was reached, |     | the superstructure |     | is  | replaced. | It would |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ------------ | --- | ------------------ | --- | --- | --------- | -------- |
Ng=(cid:6)0,1,2,...,10(cid:7) (cid:1)14i(cid:2) have been expected that the three PM applications were applied
again.However,atthattimeandduetotheeffectofthediscount
whereTm=timeofapplicationoftheithmaintenanceactionap- rate, the optimization algorithm determined that it is more eco-
i
| plied to | a given component |     | and | i,j=1,2,...,10. |     |     |     |         |               |     |       |         |          |             |     |
| -------- | ----------------- | --- | --- | --------------- | --- | --- | --- | ------- | ------------- | --- | ----- | ------- | -------- | ----------- | --- |
|          |                   |     |     |                 |     |     |     | nomical | and effective | to  | apply | EM. The | frequent | application | of  |
Theresultingthree-dimensionalPareto-optimalsetisshownin
|                         |             |     |          |        |               |       |     | EM associated |     | with Solution |     | D3 as shown | in  | Figs. 11–13 | indi- |
| ----------------------- | ----------- | --- | -------- | ------ | ------------- | ----- | --- | ------------- | --- | ------------- | --- | ----------- | --- | ----------- | ----- |
| Fig. 10(cid:1)a(cid:2). | Projections | of  | this set | in the | bidimensional | space | are |               |     |               |     |             |     |             |       |
catesthatitmaynotbepracticaltotargetanunavailabilitythresh-
alsopresentedinFigs.10(cid:1)b–d(cid:2).Fourrepresentativesolutions(cid:1)A3,
|           |               |           |        |                    |                |         |          |            | 10−3 |     |              |           |     |         | 104. |
| --------- | ------------- | --------- | ------ | ------------------ | -------------- | ------- | -------- | ---------- | ---- | --- | ------------ | --------- | --- | ------- | ---- |
|           |               |           |        |                    |                |         |          | old as low | as   | and | a redundancy | threshold |     | as high | as   |
| B3, C3,   | and D3(cid:2) | selected  | from   | the Pareto-optimal |                | set     | are also |            |      |     |              |           |     |         |      |
| shown on  | the figure.   | The       | figure | shows              | that solutions |         | between  |            |      |     |              |           |     |         |      |
| Solutions | A3 and        | C3 almost | always | improve            | in             | both An | and      |            |      |     |              |           |     |         |      |
max
Conclusions
| RI min with | increasing | the      | LCC.    | However, | Solution | D3      | provides |     |     |     |     |     |     |     |     |
| ----------- | ---------- | -------- | ------- | -------- | -------- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
| better An   | than       | Solution | C3 with | a higher | cost     | but the | RI it    |     |     |     |     |     |     |     |     |
|             | max        |          |         |          |          |         | min      |     |     |     |     |     |     |     |     |
provides is worse than that of Solution C3. These observations Thispaperpresentedanapproachforanautomatedmultiobjective
can also be seen in Table 4, which shows the details of these optimization of maintenance strategies considering the unavail-
|     |     |     |     |     |     |     |     | ability, redundancy, |     | and | the LCC | as criteria. |     | The unavailability |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | ------- | ------------ | --- | ------------------ | --- |
representativesolutions.Thissituationoccursduetothefactthat
improvingAn beyondwhatisofferedbySolutionC3requires and redundancy were calculated based on lifetime functions.
max
additional maintenance actions aimed at improving the deck, Models that reflect the effects of separate and/or combined EM
whichisnotpartoftheredundancysystemmodel.Thisisshown and PM on the lifetime functions were presented. An algorithm
11(cid:1)a(cid:2) 11(cid:1)b(cid:2), for the optimization of EM was proposed and its advantage over
| in Figs. | and |     | which | present | the schedules | of  | mainte- |     |     |     |     |     |     |     |     |
| -------- | --- | --- | ----- | ------- | ------------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
nance application and history profiles for the cumulative mainte- another algorithm was investigated. The effects of the perfor-
nance cost for the selected solutions, respectively. It is also mance thresholds on the LCC due to EM were investigated. A
observed in Fig. 11(cid:1)a(cid:2) that SolutionA3 requires no EM applica- novelapproachforregularandirregulartime-intervalPMoptimi-
tions. Figs. 12 and 13 show the history profiles of the selected zation was proposed. Both EM and PM were considered in a
CMsolutionsfortheunavailabilityandredundancy,respectively. novel proposed multiobjective maintenance optimization ap-
It can be observed in Figs. 11–13 how the three PM applications proach. In this approach, multiple EM types and multiple PM
inSolutionB3wereabletodelaythefirstreachingoftheunavail- types were considered, and regular or irregular time-interval PM
1020/JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010
J. Struct. Eng. 2010.136:1009-1022.

Fig.13.HistoryprofilesofredundancyfortheselectedcombinedEMandPM(cid:1)CM(cid:2)solutions:(cid:1)a(cid:2)SolutionA3;(cid:1)a(cid:2)SolutionB3;(cid:1)c(cid:2)SolutionC3;
and(cid:1)d(cid:2)SolutionD3
were considered. Furthermore, EM was treated as performance- formeddecisionswithrespecttotheselectionofthemainte-
based, i.e., EM is only applied when a performance threshold is nance strategy.
reached, and thus solutions that are more economical than time- Thegreatpotentialofferedbylifetimefunctionsincludingthe
based solutions were obtained. GAs were used to solve the opti- availability and redundancy for use in maintenance optimization
mization problem. The optimization approach was applied to a shoulddrawattentiontothesetool.Thusfar,thebasisofderiving
bridge located in Colorado, United States. thelifetimefunctionsistheuseofstatisticalobservationsthatare
The following conclusions can be made: generally hard to obtain for structures. Therefore, the resulting
1. Using the unavailability of structures as a performance indi- uncertainties may be high. Further research is clearly required to
catorprovidesgreatflexibilityinincorporatingtheeffectsof developmoreaccuratemethodsforderivinglifetimefunctionsfor
maintenanceontheperformanceandhighspeedinthemain- structures potentially by incorporating information obtained by
tenance optimization solution; structural health monitoring into these functions. This is a re-
2. ItwasobservedthattheEMoptimizationusingtheproposed search subject currently underway by the writers. Additionally,
algorithm EMO2 can always provide the optimum solutions experimental research is needed to capture the true effects of
while the traditional method EMO1 may, in some cases, fail maintenance on the lifetime functions. Combined with the main-
to find these optimum solutions; tenance optimization approach proposed herein, a complete
3. Itwasobservedthattheproposedsingleandcombinedopti- framework for the management of infrastructure is achievable.
mization approaches were able to provide sets of optimum
maintenancestrategiesamongwhichtrade-offsexistandcan
be identified;
4. It was shown that the interaction between the unavailability, Acknowledgments
redundancy, and LCC was found to be nontrivial and under-
standing it requires the inclusion of these three aspects in a The support from (cid:1)1(cid:2) the National Science Foundation through
proper maintenance optimization problem formulation; and Grant Nos. CMS-0638728 and CMS-0639428; (cid:1)2(cid:2) the Common-
5. Theinteractions,trade-offs,andcompromisesamongtheop- wealth of Pennsylvania, Department of Community and Eco-
timum solution found using the proposed approach provide nomic Development, through the Pennsylvania Infrastructure
valuable insight for decision makers to make sound and in- Technology Alliance (cid:1)PITA(cid:2); (cid:1)3(cid:2) the U.S. Federal Highway Ad-
JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010/1021
J. Struct. Eng. 2010.136:1009-1022.
.devreser
sthgir
lla
;ylno
esu
lanosrep
roF
.ECSA
thgirypoC
.31/92/90
no
seirarbiL
adirolF
lartneC
fO
ytisrevinU
yb
gro.yrarbilecsa
morf
dedaolnwoD

ministration Cooperative Agreement Award No. DTFH61-07-H- Brühwiler,M.H.Faber,andB.Adey,eds.,ASCE,Reston,Va.,19–
| 00040; and | (cid:1)4(cid:2) the | U.S. | Office of | Naval | Research | Contract | No. | 25.       |       |                     |         |            |            |              |     |
| ---------- | ------------------- | ---- | --------- | ----- | -------- | -------- | --- | --------- | ----- | ------------------- | ------- | ---------- | ---------- | ------------ | --- |
|            |                     |      |           |       |          |          |     | Goldberg, | D. E. | (cid:1)1989(cid:2). | Genetic | algorithms | in search, | optimization | and |
N00014-08–1-0188isgratefullyacknowledged.Theopinionsand
machinelearning,Addison-Wesley,Reading,Mass.
conclusionspresentedinthispaperarethoseofthewritersanddo
Hoyland,A.,andRausand,M.(cid:1)1994(cid:2).Systemreliabilitytheory:Models
| not necessarily | reflect | the | views | of the sponsoring |     | organizations. |     |     |     |     |     |     |     |     |     |
| --------------- | ------- | --- | ----- | ----------------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
andstatisticalmethods,Wiley-Interscience,NewYork.
|     |     |     |     |     |     |     |     | Klaassen, | K. B., | and van | Peppen, | J. C. | L. (cid:1)1989(cid:2). | System | reliability: |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ------ | ------- | ------- | ----- | ---------------------- | ------ | ------------ |
Conceptsandapplications,EdwardArnold,NewYork.
| References |     |     |     |     |     |     |     |          |         |            |     | (cid:1)2003(cid:2). |             |     |                   |
| ---------- | --- | --- | --- | --- | --- | --- | --- | -------- | ------- | ---------- | --- | ------------------- | ----------- | --- | ----------------- |
|            |     |     |     |     |     |     |     | Kong, J. | S., and | Frangopol, | D.  | M.                  | “Life-cycle |     | reliability based |
maintenancecostoptimizationofdeterioratingstructureswithempha-
129(cid:1)6(cid:2),818–828.
Akgül, F., and Frangopol, D. M. (cid:1)2004(cid:2). “Computational platform for sisonbridges.”J.Struct.Eng.,
(cid:1)1995(cid:2).
predicting lifetime system reliability profiles for different structure Leemis, L. M. Reliability, probabilistic models and statistical
.devreser sthgir lla ;ylno esu lanosrep roF .ECSA thgirypoC .31/92/90 no seirarbiL adirolF lartneC fO ytisrevinU yb gro.yrarbilecsa morf dedaolnwoD
typesinanetwork.”J.Comput.Civ.Eng., 18(cid:1)2(cid:2),92–104. methods,Prentice-Hall,EnglewoodCliffs,N.J.
Ang,A.H.-S.,andTang,W.H.(cid:1)1984(cid:2).Probabilityconceptsinengineer- Liu, C., Hammad, A., and Itoh, Y. (cid:1)1997(cid:2). “Multiobjective optimization
|     |     |     |     |     |     |     |     | of bridge | deck | rehabilitation |     | using | a genetic | algorithm.” | Comput. |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ---- | -------------- | --- | ----- | --------- | ----------- | ------- |
ingplanninganddesign:Decision,riskandreliability,Vol.II,Wiley,
|     |     |     |     |     |     |     |     | AidedCiv.Infrastruct.Eng., |     |     |     | 12(cid:1)6(cid:2),431–443. |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | --- | -------------------------- | --- | --- | --- |
NewYork.
Liu,M.,andFrangopol,D.M.(cid:1)2004(cid:2).“Probabilisticmaintenancepriori-
Ciampoli,M.,andEllingwood,B.R.(cid:1)2002(cid:2).“Probabilisticmethodsfor
tizationfordeterioratingbridgesusingamultiobjectivegeneticalgo-
| assessing                          | current | and future | performance |                         | of concrete | structures | in  |         |        |         |           |       |                  |     |           |
| ---------------------------------- | ------- | ---------- | ----------- | ----------------------- | ----------- | ---------- | --- | ------- | ------ | ------- | --------- | ----- | ---------------- | --- | --------- |
|                                    |         |            |             |                         |             |            |     | rithm.” | Proc., | 9thASCE | Specialty | Conf. | on Probabilistic |     | Mechanics |
| nuclearpowerplants.”Mater.Struct., |         |            |             | 35(cid:1)1(cid:2),3–14. |             |            |     |         |        |         |           |       |                  |     |           |
Deb, K. (cid:1)2001(cid:2). Multi-objective optimization using evolutionary algo- andStructuralReliability,ASCE,Reston,Va.
(cid:1)2005a(cid:2).
|     |     |     |     |     |     |     |     | Liu, M., | and Frangopol, |     | D. M. |     | “Bridge | annual | maintenance |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | -------------- | --- | ----- | --- | ------- | ------ | ----------- |
rithms,Wiley,NewYork.
Deb,K.,Pratap,A.,Agrawal,S.,andMeyarivan,T.(cid:1)2002(cid:2).“Afastand prioritizationunderuncertaintybymultiobjectivecombinatorialopti-
20(cid:1)5(cid:2),343–353.
mization.”Comput.AidedCiv.Infrastruct.Eng.,
elitistmultiobjectivegeneticalgorithm:NSGA-II.”IEEETrans.Evol. (cid:1)2005b(cid:2).
6(cid:1)2(cid:2),182–197. Liu, M., and Frangopol, D. M. “Multiobjective maintenance
Comput.,
Enright,M.P.,andFrangopol,D.M.(cid:1)1998(cid:2).“Failuretimepredictionof planningoptimizationfordeterioratingbridgesconsideringcondition,
|               |           |              |     |            |       |                      |       | safety,andlife-cyclecost.”J.Struct.Eng., |                          |              |     |         | 131(cid:1)5(cid:2),833–842. |            |           |
| ------------- | --------- | ------------ | --- | ---------- | ----- | -------------------- | ----- | ---------------------------------------- | ------------------------ | ------------ | --- | ------- | --------------------------- | ---------- | --------- |
| deteriorating | fail-safe | structures.” |     | J. Struct. | Eng., | 124(cid:1)12(cid:2), | 1448– |                                          |                          |              |     |         |                             |            |           |
|               |           |              |     |            |       |                      |       | Maunsell                                 | Ltd. (cid:1)1999(cid:2). | “Serviceable |     | life of | highway                     | structures | and their |
1457.
components.”FinalRep.,BirminghamHighwaysAgency,London.
| Estes, A. | C. (cid:1)1997(cid:2). | “Asystem       | reliability      | approach   |           | to the lifetime | opti-   |                                   |               |     |             |              |                          |                     |              |
| --------- | ---------------------- | -------------- | ---------------- | ---------- | --------- | --------------- | ------- | --------------------------------- | ------------- | --- | ----------- | ------------ | ------------------------ | ------------------- | ------------ |
|           |                        |                |                  |            |           |                 |         | Miyamoto,                         | A., Kawamura, |     | K., and     | Nakamura,    | H.                       | (cid:1)2000(cid:2). | “Bridge man- |
| mization  | of inspection          | and            | repair           | of highway | bridges.” | Ph.D.           | thesis, |                                   |               |     |             |              |                          |                     |              |
|           |                        |                |                  |            |           |                 |         | agement                           | system        | and | maintenance | optimization |                          | for existing        | bridges.”    |
| Dept.     | of Civil,              | Environmental, | andArchitectural |            |           | Engineering,    | Univ.   |                                   |               |     |             |              |                          |                     |              |
|           |                        |                |                  |            |           |                 |         | Comput.AidedCiv.Infrastruct.Eng., |               |     |             |              | 15(cid:1)1(cid:2),45–55. |                     |              |
ofColoradoatBoulder,Boulder,Colo.
|     |     |     |     |     |     |     |     | Mori, Y., | and Ellingwood, |     | B. R. | (cid:1)1993(cid:2). | “Reliability-based |     | service life |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --------------- | --- | ----- | ------------------- | ------------------ | --- | ------------ |
Estes,A.C.,andFrangopol,D.M.(cid:1)1999(cid:2).“Repairoptimizationofhigh-
|             |       |        |             |            |     |            |       | assessment | of  | aging | concrete | structures.” | J.  | Struct. | Eng., 119(cid:1)5(cid:2), |
| ----------- | ----- | ------ | ----------- | ---------- | --- | ---------- | ----- | ---------- | --- | ----- | -------- | ------------ | --- | ------- | ------------------------- |
| way bridges | using | system | reliability | approach.” |     | J. Struct. | Eng., |            |     |       |          |              |     |         |                           |
1600–1621.
125(cid:1)7(cid:2),766–775.
Mori,Y.,andEllingwood,B.R.(cid:1)1994a(cid:2).“Maintainingreliabilityofcon-
Frangopol,D.M.(cid:1)2010(cid:2).“Life-cycleperformance,management,andop-
|            |               |     |               |                             |     |     |     | cretestructures.I:Roleofinspection/repair.”J.Struct.Eng., |     |     |     |     |     |     | 120(cid:1)3(cid:2), |
| ---------- | ------------- | --- | ------------- | --------------------------- | --- | --- | --- | --------------------------------------------------------- | --- | --- | --- | --- | --- | --- | ------------------- |
| timization | of structural |     | systems under | uncertainty:Accomplishments |     |     |     |                                                           |     |     |     |     |     |     |                     |
824–845.
andchallenges.”Struct.Infrastruct.Eng.,postedonlineaheadofprint Mori,Y.,andEllingwood,B.R.(cid:1)1994b(cid:2).“Maintainingreliabilityofcon-
May11,2010.DOI:10.1080/15732471003594427. crete structures. II: Optimum inspection/repair.” J. Struct. Eng.,
Frangopol,D.M.,Kong,J.S.,andGharaibeh,E.S.(cid:1)2001(cid:2).“Reliability-
120(cid:1)3(cid:2),846–862.
based life-cycle management of highway bridges.” J. Comput. Civ. Neves, L. C., Frangopol, D. M., and Cruz, P. J. (cid:1)2006a(cid:2). “Probabilistic
15(cid:1)1(cid:2),27–34.
Eng., lifetime-oriented multiobjective optimization of bridge maintenance:
(cid:1)1997(cid:2).
Frangopol, D. M., Lin, K.-Y., and Estes, A. C. “Life-cycle cost Singlemaintenancetype.”J.Struct.Eng., 132(cid:1)6(cid:2),991–1005.
123(cid:1)10(cid:2),
design of deteriorating structures.” J. Struct. Eng., 1390– Neves,L.C.,Frangopol,D.M.,andPetcherdchoo,A.(cid:1)2006b(cid:2).“Proba-
1401.
Frangopol,D.M.,andLiu,M.(cid:1)2007(cid:2).“Maintenanceandmanagementof bilistic lifetime-oriented multiobjective optimization of bridge main-
|     |     |     |     |     |     |     |     | tenance: | Combination |     | of  | maintenance | types.” | J.  | Struct. Eng., |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | --- | --- | ----------- | ------- | --- | ------------- |
civil infrastructure based on condition, safety, optimization and life- 132(cid:1)11(cid:2),1821–1834.
cyclecost.”Struct.Infrastruct.Eng., 3(cid:1)1(cid:2),29–41. (cid:1)2009(cid:2).
|            |        |             |       |                     |             |             |     | Okasha,   | N. M.,       | and Frangopol, |               | D. M.       | “Lifetime-oriented |             | multi- |
| ---------- | ------ | ----------- | ----- | ------------------- | ----------- | ----------- | --- | --------- | ------------ | -------------- | ------------- | ----------- | ------------------ | ----------- | ------ |
| Frangopol, | D. M., | and Okasha, | N. M. | (cid:1)2008(cid:2). | “Life-cycle | performance |     |           |              |                |               |             |                    |             |        |
|            |        |             |       |                     |             |             |     | objective | optimization |                | of structural | maintenance |                    | considering | system |
andredundancyofstructures.”Proc.,6thInt.ProbabilisticWorkshop,
|                                                            |     |     |     |     |     |     |     | reliability,               | redundancy |     | and life-cycle |     | cost using | GA.” | Struct. Safety, |
| ---------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | ---------- | --- | -------------- | --- | ---------- | ---- | --------------- |
| C.-A.Graubner,H.Schmidt,andD.Proske,eds.,TechnischeUniver- |     |     |     |     |     |     |     | 31(cid:1)6(cid:2),460–474. |            |     |                |     |            |      |                 |
sitätDarmstadt,Germany,1–14. Okasha,N.M.,andFrangopol,D.M.(cid:1)2010a(cid:2).“Redundancyofstructural
Frangopol,D.M.,andOkasha,N.M.(cid:1)2009(cid:2).“Redundancyofstructural
|     |     |     |     |     |     |     |     | systems | with | and without | maintenance: |     | An  | approach | based on life- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ---- | ----------- | ------------ | --- | --- | -------- | -------------- |
systems based on survivor functions.” Proc., 2009 Structures Con- timefunctions.”Reliab.Eng.Syst.Saf., 95(cid:1)5(cid:2),520–533.
gress: Don’t Mess with Structural Engineers SEI-ASCE (cid:1)CD-ROM(cid:2), Okasha,N.M.,andFrangopol,D.M.(cid:1)2010b(cid:2).“Time-variantredundancy
L.Griffiths,T.Helwig,M.Waggoner,andM.Hoit,eds.,ASCE,Re- ofstructuralsystems.”Struct.Infrastruct.Eng., 6(cid:1)1–2(cid:2),279–301.
ston,Va.,1781–1790. Ramakumar,R.(cid:1)1993(cid:2).Engineeringreliability:Fundamentalsandappli-
Furuta,H.,Kameda,T.,Fukuda,Y.,andFrangopol,D.M.(cid:1)2004(cid:2).“Life- cations,1stEd.,Prentice-Hall,EnglewoodCliffs,N.J.
cycle cost analysis for infrastructure systems: Life-cycle cost vs. Yang,S.-I.,Frangopol,D.M.,andNeves,L.C.(cid:1)2006(cid:2).“Optimummain-
safetylevelvs.servicelife.”Life-cycleperformanceofdeteriorating
|     |     |     |     |     |     |     |     | tenance | strategy | for | deteriorating | structures |     | based on | lifetime func- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | -------- | --- | ------------- | ---------- | --- | -------- | -------------- |
28(cid:1)2(cid:2),196–206.
structures:Assessment,designandmanagement,D.M.Frangopol,E. tions.”Eng.Struct.,
1022/JOURNALOFSTRUCTURALENGINEERING©ASCE/AUGUST2010
J. Struct. Eng. 2010.136:1009-1022.