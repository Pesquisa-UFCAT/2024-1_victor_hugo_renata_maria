ProbabilisticEngineeringMechanics19(2004)345–359
www.elsevier.com/locate/probengmech
|     |     | Two | probabilistic |               |                 | life-cycle | maintenance     |            |     | models |     |     |     |
| --- | --- | --- | ------------- | ------------- | --------------- | ---------- | --------------- | ---------- | --- | ------ | --- | --- | --- |
|     |     |     | for           | deteriorating |                 | civil      | infrastructures |            |     |        |     |     |     |
|     |     |     |               |               | Noortwijka,b,*, |            |                 | Frangopolc |     |        |     |     |     |
|     |     |     | Jan           | M.            | van             |            | Dan             | M.         |     |        |     |     |     |
aHKVConsultants,P.O.Box2120,NL-8203ACLelystad,TheNetherlands
bFacultyofElectricalEngineering,MathematicsandComputerScience,DelftUniversityofTechnology,
P.O.Box5031,NL-2600GADelft,TheNetherlands
cDepartmentofCivil,Environmental,andArchitecturalEngineering,UniversityofColorado,Boulder,CO80309-0428,USA
Received23June2003;revised4September2003;accepted18March2004
Abstract
Thepurposeofthispaperistodescribeandcomparetwomaintenancemodelsfordeterioratingcivilinfrastructuresthatcanbeusedto
insureanadequatelevelofreliabilityatminimallife-cyclecost.Thesemodels,referredtoRijkswaterstaat’smodelandFrangopol’smodel
havebeenindependentlydevelopedbytheauthorsofthispaperandtheirassociates.TheformermodelhasbeenappliedbytheNetherlands
Ministry of Transport, Public Works and Water Management (Rijkswaterstaat). It can be used for justification and optimisation of
maintenancemeasures.Thelattermodelcontributedtothefurtherdevelopmentofthebridgemanagementmethodologythathasbeensetup
bytheUKHighwaysAgency.
q2004ElsevierLtd.Allrightsreserved.
Keywords: Life-cycle costing; Deterioration; Maintenance optimisation; Lifetime extension; Bridge management; Renewal theory; Simulation; Gamma
process
1. Introduction an adequate level of reliability at minimal life-cycle cost.
Thesetwomodelshavebeenpresentedanddiscussedduring
Thepurposeofthispaperistodescribeandcomparetwo theworkshoponOptimalMaintenanceofStructures[11].
|             |        |     |               |       |                 |     | The         | outline of | this | paper     | is as     | follows. | The two     |
| ----------- | ------ | --- | ------------- | ----- | --------------- | --- | ----------- | ---------- | ---- | --------- | --------- | -------- | ----------- |
| maintenance | models | for | deteriorating | civil | infrastructures |     |             |            |      |           |           |          |             |
|             |        |     |               |       |                 |     | maintenance | models     | are  | described | inSection |          | 2.Theactual |
thatcanbeusedtobalancestructuralreliabilityandlife-cycle
|     |     |     |     |     |     |     | comparison | of the | condition-based |     | maintenance |     | model of |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------ | --------------- | --- | ----------- | --- | -------- |
cost.ThesetwomodelsaretheRijkswaterstaat’smodeland
|     |     |     |     |     |     |     | Rijkswaterstaat |     | and the | reliability-based |     |     | maintenance |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------- | ----------------- | --- | --- | ----------- |
Frangopol’smodel.Theformermodelhasbeenappliedfor
|                  |     |                                       |                |        |          |     | model of    | Frangopol | is          | presented | in  | Section | 3. Finally, |
| ---------------- | --- | ------------------------------------- | -------------- | ------ | -------- | --- | ----------- | --------- | ----------- | --------- | --- | ------- | ----------- |
| justification    | and | optimisation                          | of maintenance |        | measures | by  |             |           |             |           |     |         |             |
|                  |     |                                       |                |        |          |     | conclusions | are given | inSection4. |           |     |         |             |
| the Netherlands  |     | Ministry                              | of Transport,  | Public | Works    | and |             |           |             |           |     |         |             |
| Water Management |     | (Rijkswaterstaat);detailedinformation |                |        |          |     |             |           |             |           |     |         |             |
onthismodelcanbefoundinRefs.[1,2].Thelattermodel
|             |             |             |             |             |           |         | 2. Maintenancemodels |                |         |       |                   |         |            |
| ----------- | ----------- | ----------- | ----------- | ----------- | --------- | ------- | -------------------- | -------------- | ------- | ----- | ----------------- | ------- | ---------- |
| contributed | to          | the further | development |             | of the    | bridge  |                      |                |         |       |                   |         |            |
| management  | methodology |             | that has    | been        | set up by | the UK  |                      |                |         |       |                   |         |            |
|             |             |             |             |             |           |         | Civil                | infrastructure | systems |       | are deteriorating |         | with time. |
| Highways    | Agency      | [3–5];      | additional  | information |           | on this |                      |                |         |       |                   |         |            |
|             |             |             |             |             |           |         | Designing            | these systems  |         | for a | particular        | service | life and   |
modelcanbefoundinRefs.[6–10,35].Bothmodelscanbe
|     |     |     |     |     |     |     | maintaining | them | in a safe | condition |     | during | their entire |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ---- | --------- | --------- | --- | ------ | ------------ |
appliedtodeterminethebestmaintenancestrategytoinsure
|                 |     |                  |     |              |          |       | service    | life have | been recognised |      | as         | very | critical issues |
| --------------- | --- | ---------------- | --- | ------------ | -------- | ----- | ---------- | --------- | --------------- | ---- | ---------- | ---- | --------------- |
|                 |     |                  |     |              |          |       | worldwide. | According | to              | Ref. | [12] there | are  | two types of    |
| * Corresponding |     | author. Address: | HKV | Consultants, | P.O. Box | 2120, |            |           |                 |      |            |      |                 |
maintenancework:preventivemaintenancewhichifitisnot
NL-8203ACLelystad,TheNetherlands.Tel.:þ31-320-294203;fax:þ31-
doneitwillcostmoreatalaterstagetokeepthestructurein
320-253901.
E-mail addresses: j.m.van.noortwijk@hkv.nl (J.M. van Noortwijk), a safe condition, and essential maintenance which is
dan.frangopol@colorado.edu(D.M.Frangopol). required to keep the structure safe. Whilst it is easy to
0266-8920/$-seefrontmatterq2004ElsevierLtd.Allrightsreserved.
doi:10.1016/j.probengmech.2004.03.002

346 J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359
defendessentialmaintenanceworkonsafetygrounds,since chapter 3), whereby the renewals are the maintenance
failure consequences are in general extremely large, actions that bring a component back into its original
preventive treatments are more difficult to justify. conditionor‘asgoodasnewstate’.Aftereach renewal we
Engineeringjudgmentorbestpracticeisusuallyputforward start, in statistical sense, all over again. A discrete renewal
as reasons for undertaking such work. Some have process {NðnÞ;n¼1;2;3;…} is a non-negative integer-
questioned as whether some types of preventive work, valued stochastic process that registers the successive
ð0;n(cid:5):
including both proactive preventive maintenance renewals in the time interval Let the renewal times
(i.e. applied before any indication of deterioration is T ; T ;…; be non-negative, independent, identically
1 2
apparent)andreactivepreventivemaintenance(i.e.applied distributed, random quantities having the discrete prob-
onlyaftersomedeteriorationisevidenced)arenecessaryat ability function Pr{T ¼i}¼p; i¼1;2;3;…; where p
|     |     |     |     |     |     |     |     |     | k   | i   |     |     | i   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
all. There is an urgent need, therefore, to justify represents the probability of a renewal in unit time i: We
preventive work in a rational manner [4]. For highway denote the cost associated with a renewal in unit time i by
bridges, some of the preventive maintenances currently in c; i¼1;2;3;… In mathematical terms, the (present)
i
practice include cathodic protection, silane treatment, discounted value of the cost c i in unit time i is defined to
painting of steelwork, and concrete patch repairs. Many be aic with a¼½1þðr=100Þ(cid:5)21 the discount factor
i
engineers believe that these preventive measures are per unit time and r the discount rate per unit time,
.0:
| worthwhile | in  | the long | term, | but | cannot | defend this | where r |     |     |     |     |     |     |
| ---------- | --- | -------- | ----- | --- | ------ | ----------- | ------- | --- | --- | --- | --- | --- | --- |
viewpoint on a reliability basis. This is simply because The expected discounted cost over a bounded time
thisbasisdoesnotexist.Forthisreason,areliability-based horizoncanbeobtainedwitharecursiveformula.Toobtain
approach has to be developed and used to identify optimal thisequation,weconditiononthevaluesofthefirstrenewal
preventive maintenance strategies based on lifetime time T and apply the law of total probability. The cost
1
reliability and life-cycle costs for different civil infrastruc- associatedwithoccurrenceoftheeventT ¼iisc plusthe
1 i
ture systems. The use of condition-based and reliability- additional expected discounted cost during the interval
based maintenance optimisation models is therefore of ði;n(cid:5);i¼1;…;n:Hence,theexpecteddiscountedcostover
|     |     |     |     |     |     |     |     |     | ð0;n(cid:5); |     | EðKðn;aÞÞ; |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ---------- | --- | --- |
considerableinterestforoptimumlife-cyclemaintenanceof the bounded horizon denoted by can be
| deteriorating | civil | infrastructures. |     |     |     |     | written as |     |     |     |     |     |     |
| ------------- | ----- | ---------------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
n
| 2.1. Condition-basedmaintenance |     |     |     | model |     |     |            | X   |                            |     |     |     |     |
| ------------------------------- | --- | --- | --- | ----- | --- | --- | ---------- | --- | -------------------------- | --- | --- | --- | --- |
|                                 |     |     |     |       |     |     | EðKðn;aÞÞ¼ |     | aip½c þEðKðn2i;aÞÞ(cid:5); |     |     |     |     |
i i
ð1Þ
i¼1
2.1.1. Maintenance
The area of optimising maintenance through mathe- n¼1;2;3;…; Kð0;aÞ;0:
| matical | models | was | founded | in the | early | sixties. This |     |     |     |     |     |     |     |
| ------- | ------ | --- | ------- | ------ | ----- | ------------- | --- | --- | --- | --- | --- | --- | --- |
pioneering work is summarised in Refs. [13,14]. The By using discrete-time renewal theory ([18], chapter 13),
interest in maintenance optimisation had been brought the expected discounted cost over an unbounded horizon
aboutbythehighcostofmilitary-industrialequipmentsuch can be written as[20]
asjetairliners,electroniccomputers,andballisticmissiles,
|     |     |     |     |     |     |     |     |     | X1  | aicp |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
amongothers.Awell-knownmodelofthisperiodistheage
|                                                    |        |     |                 |     |          |          | lim EðKðn;aÞÞ¼ |     | i¼1 | i i : |     |     | ð2Þ |
| -------------------------------------------------- | ------ | --- | --------------- | --- | -------- | -------- | -------------- | --- | --- | ----- | --- | --- | --- |
| replacement                                        | model. | The | age replacement |     | strategy | involves |                |     | X1  |       |     |     |     |
|                                                    |        |     |                 |     |          |          | n!1            |     | 12  | aip   |     |     |     |
| replacementuponfailureoruponreachingapredetermined |        |     |                 |     |          |          |                |     |     | i¼1 i |     |     |     |
age,whicheveroccursfirst.Thepredeterminedageinanage
|     |     |     |     |     |     |     | Forcost-optimalinvestmentdecisions,we |     |     |     | areinterestedin |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --------------- | --- | --- |
replacementstrategyiscalledtheagereplacementinterval.
|            |             |          |              |     |             |               | finding an         | optimum | balance    | between              | the | initial      | cost of |
| ---------- | ----------- | -------- | ------------ | --- | ----------- | ------------- | ------------------ | ------- | ---------- | -------------------- | --- | ------------ | ------- |
| According  | to Refs.    | [15,16], | the          | age | replacement | model is      |                    |         |            |                      |     |              |         |
|            |             |          |              |     |             |               | investment         | and     | the future | cost of maintenance, |     | being        | the     |
| one of the | maintenance |          | optimisation |     | models      | that has been |                    |         |            |                      |     |              |         |
|            |             |          |              |     |             |               | area of life-cycle |         | costing.   | In this situation,   |     | the monetary |         |
applied most.
lossesoveranunboundedhorizonarethesumoftheinitial
| As a                                                 | basis for | optimising |     | maintenance, | Rijkswaterstaat |     |                    |          |           |              |            |          |        |
| ---------------------------------------------------- | --------- | ---------- | --- | ------------ | --------------- | --- | ------------------ | -------- | --------- | ------------ | ---------- | -------- | ------ |
|                                                      |           |            |     |              |                 |     | cost of investment |          | c and     | the expected | discounted |          | future |
| implementedtheagereplacementmodelwithdiscountedcost. |           |            |     |              |                 |     |                    |          | 0         |              |            |          |        |
|                                                      |           |            |     |              |                 |     | cost in            | Eq. (2). | A similar | result       | can be     | obtained | for    |
Thecriterionofexpecteddiscountedcost(netpresentvalue)
|         |           |         |     |          |           |          | continuous-time |     | renewalprocesses |     | [21]. |     |     |
| ------- | --------- | ------- | --- | -------- | --------- | -------- | --------------- | --- | ---------------- | --- | ----- | --- | --- |
| over an | unbounded | horizon | is  | used for | comparing | mainten- |                 |     |                  |     |       |     |     |
ancedecisions(forargumentsonwhethertouseaboundedor
unboundedhorizon,seeSection3.4).Byusingthiscriterion, 2.1.2.Deterioration
thecostofpreventivemaintenancecanbebalancedagainstthe In the condition-based maintenance model of Rijkswa-
costofcorrective(alsocalledessentialinFrangopol’smodel) terstaat, ageing has been modelled in three ways with
maintenance. For a discussion about which cost-based increasing complexity:
criterioncanbestbeused,werefertoRef.[17].
The maintenance of structurescan often be modelled as 1. Lifetime model on the basis of the probability
a (discrete) renewal process ([18], chapters 12–13; [19], distributionof the lifetime ortime offailure.

J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359 347
2. Deteriorationmodelonthebasisofthestochasticprocess {XðtÞ;t$0}isthencalledagammaprocess.Theparameter
of deterioration, where failure is defined as the event in urepresentstheuncertaintyinthedeteriorationprocess;the
which—due to deterioration—the condition (resistance) largeru;the moreuncertain the deterioration process [22].
dropsbelowthefailurelevel(load).Itisassumedthatthe A component is said to fail when its deterioration
expecteddeteriorationattimetcanbedescribedusinga exceeds a certain level y; where y is defined as the initial
power law; that is, the expected deterioration at time t resistancer minusthefailurelevels:Letthetimeatwhich
0
can be writtenas atb for a;b.0: the failure level is crossed be denoted by the lifetime T
3. Deterioration and lifetime-extension model on the basis (in years). Due to the gamma distributed deterioration (4),
ofthestochasticprocessofdeteriorationcombinedwith the lifetimedistributioncan then bewritten as:
lifetimeextension,wherefailureisdefinedastheeventin
ð1
which the condition drops below the failure level. FðtÞ¼Pr{T #t}¼Pr{XðtÞ$y}¼ f ðxÞdx
XðtÞ
The deterioration process with lifetime extension has x¼y
been approximated by a deterioration process without Gð½atb(cid:5)=u;y=uÞ
lifetime extension. The approximate expected ¼ ; ð5Þ
Gð½atb(cid:5)=uÞ
deterioration is a least squares power law fit to the
lower envelope function of the exact deterioration where Gðv;xÞ¼ Ð1 tv21exp{2t}dt is the incomplete
t¼x
process with lifetime extension. The coefficient of gamma function for x$0 and a.0: The probability of
variation of the deterioration at the time at which the failureper year follows immediatelyfrom Eq. (5):
expected deterioration equals the failure level is
unchanged. q ¼FðiÞ2Fði21Þ; i¼1;2;3;… ð6Þ
i
Forallthreemodels,theoptimalpreventivereplacement
intervalfollowsfromanagereplacementmodelbasedona 2.1.3. Age replacement
lifetime distribution. For the deterioration models, the Underanagereplacementpolicy([14],chapters3–4),a
probabilityoffailureperyear(discretelifetimedistribution) replacementiscarriedoutatagek(preventivereplacement)
is defined asthe probability thatthe condition drops below or at failure (corrective replacement), whichever occurs
the failure level per year. first,wherek¼1;2;3;…Apreventive replacement entails
Sincedeteriorationisuncertain,itcanbestberegardedas acostc P ;whereasacorrectivereplacemententailsacostc F ;
a stochastic process. At first glance, it seems possible to where 0,c P #c F : According to Eq. (2), the expected
represent the uncertainty in a deterioration process by the discounted cost of age replacement over an unbounded
normal distribution. This probability distribution has been horizonis
used for modelling the exchange-value of shares and the ! !
k k
movement of small particles in fluids and air. A character- X aiq c þak 12 X q c
i F i P
istic feature of this model—also denoted by the Brownian limEðKðn;aÞÞ¼ i¼1 i¼1 ; ð7Þ
s m tr o u t c io tu n re w ’s it r h es d is r t i a ft nc ( e se a e lte e r . n g a . te [ l 1 y 9] i , nc c r h e a a p se te s r a 7 n ) d — d i e s cr t e h a a s t es a , n!1 12 " X k aiq i ! þak 12 X k q i !#
like the exchange-value of a share. For this reason, the i¼1 i¼1
Brownian motion is inadequate in modelling deterioration, where k is the age replacement interval. The optimal age
whichproceedsinonedirection.Inorderforthestochastic replacementintervalkp isanintervalforwhichtheexpected
deterioration process to proceed in one direction, we discounted cost over an unbounded horizon is minimal.
consideritasaso-called‘gammaprocess’.Inmathematical Note that the replacement model can also be applied for
terms, a gamma process is a stochastic process with determining the optimal initial resistance of a structure,
independent non-negative increments having a gamma which balances the initial cost of investment c optimally
P
distribution. against the future cost of maintenance in Eq. (7) (see also
ArandomquantityX .0hasagammadistributionwith [23]). The expected discounted cost can also be calculated
shape parameter v.0 and scale parameter u.0 if its over a bounded horizon using Eq. (1). In situations with a
probability density function (PDF) is given by: boundedtimehorizonlargerthan50years,thecostoveran
Gaðxlv;uÞ¼½uv=GðvÞ(cid:5)xv21exp{2ux} ð3Þ unboundedhorizon(2)mayserveasagoodapproximation.
Asasimplifiedexample,westudythemaintenanceofa
where GðvÞ¼ Ð1 t¼0 tv21exp{2t}dt is the gamma function cylinderonanexistingswingbridge(adaptedfromRef.[1]).
for v.0: Let XðtÞ denote the amount of deterioration at Preventive maintenance of a cylinder mainly consists of
time t; t$0; and letthe PDFof XðtÞbe given by replacing the guide bushes and plunger, and replacing the
packing of the piston rod. In the event of corrective
f ðxÞ¼Gaðxl½atb(cid:5)=u;1=uÞ ð4Þ
XðtÞ maintenance, the cylinder has to be replaced completely
for u.0 with mean and variance EðXðtÞÞ¼atb and because too much damage has occurred. The cost of
VarðXðtÞÞ¼uatb; respectively. The stochastic process preventive maintenance is c ¼30;000 Dutch guilders,
P

348 J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359
Fig.1.Maintainingacylinderonanexistingswingbridge.Theexpecteddiscountedcostoveranunboundedhorizonasafunctionoftheagereplacement
interval.
whereasthecostofcorrectivemaintenanceisc ¼100;000 the functioning state and the failed state. For example, a
F
Dutchguilders.Bothmaintenanceactionsbringthecylinder motororswitchiseitherworkingornot.Astructure,onthe
backintoits‘goodasnewstate’.Theexpecteddeterioration other hand, can be in a range of states depending on its
is assumed to degrade linearly in time from the initial degrading condition.
conditionof100%downtothefailurelevelof0%.Thetime In situations where the cost of structural failure is very
atwhichtheexpectedconditionequalsthefailurelevelis15 high, failure norms can only be optimised in the design
years. For an annual discount rate of 5%, the expected phase. Because the bulk of the maintenance programme is
discountedcostofpreventiveandcorrectivemaintenanceis devoted to existing structures, failure norms should
displayed in Fig. 1, where the vertical axis shows the net generallybetreatedasconstraints.Giventheseconstraints,
present value in 1000 Dutch guilders (i.e. KFL). a maintenance manager can optimise the preventive
The expected discounted cost over an unbounded horizon maintenance level. A cost-optimal preventive maintenance
isminimalforapreventivereplacementintervalof13years. leveloptimallybalancesthecostofpreventivemaintenance
On the basis of the expected deterioration, this and the cost of corrective maintenance. The cost of
preventive replacement interval can approximately be corrective maintenance may include cost of traffic-jam,
transformed into the optimum preventive maintenance detour, vehicle-weight restriction, closure, etc. The load is
(condition) level of 13%. generally be taken into account in the design phase by
incorporating it into the functional requirements and thus
2.1.4. Failure intothe failurenorm.
In structural engineering, we can roughly identify two
types of failure: structural failure and condition failure. 2.1.5.Lifetime extension
Structural failure can be a collapse, whereas condition The deterioration model has been extended for the
failure means that a certain predetermined norm level has possibility of lifetime-extending maintenance. With this
been exceeded. Condition failure is defined as the event at model both the interval of preventive replacement and
which a structure fails to meet its main functional lifetime extension can be optimised. Through replacement,
requirements. It can be used to prevent structures from the condition of a component is restored to its original
being unsafe by the safety requirement (often expressed in condition.Throughlifetimeextension,thedeteriorationcan
terms of the reliability index; see Section 3.3). bedelayedsothatfailureispostponedandthelifetimeofa
Therefore, structures usually do not fail due to physical component is extended (e.g. a coating protecting steel).
failure, but due to condition failure. Inspections must be Possibleeffectsoflifetime-extendingmeasuresaretheinitia-
carriedouttoinsurethatconditionfailurewillbedetected. tionperiod(timeintervalinwhichnodeteriorationoccurs)
Physical failure is more common in mechanical and and the condition improvement. In addition, the rate of
electrical engineering. In these fields, one often considers deteriorationafterlifetimeextensioncanbe‘repeating’(after
equipment, which can assume at most two states: everylifetimeextensiontherateofdeteriorationisthesame

J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359 349
Fig.2.Expectedconditionofthesteelwith‘repeating’lifetimeextensionintermsofgritblasting.
w;2w;3w;…;bði21Þ=wcw;
andequalstherateofdeteriorationattheinitialcondition;see extended at the units of time
Fig.2)and‘non-repeating’(aftereverylifetimeextensionthe wherebxcisthelargestintegerlessthanorequaltox:Using
rate of deterioration is different and equals the rate of the geometric series, the discounted cost of a lifetime
deteriorationatthecorrespondingcondition;seeFig.3). extension at unit time ican bewritten as
| Let the | rate of deterioration | now be | based on periodic |     |     |     |     |
| ------- | --------------------- | ------ | ----------------- | --- | --- | --- | --- |
lifetime-extendingmaintenanceatafrequencyofonceinw a1wc þa2wc þ…þabði21Þ=wcwc
years. The cost of lifetime-extending maintenance is c : L L L
L aw2aðbi21Þ=wcþ1Þw
| Suppose either                                       | a preventive | replacement | or a correctiv | e   |        |             |     |
| ---------------------------------------------------- | ------------ | ----------- | -------------- | --- | ------ | ----------- | --- |
|                                                      |              |             |                | ¼   | c ¼x c | ; w¼1;2;3;… | ð8Þ |
| replacementiscarriedoutatunittimei;thenthelifetimeis |              |             |                |     | L iw L |             |     |
12aw
Fig.3.Expected(hypothetical)conditionofthesteelwith‘non-repeating’lifetimeextensionintermsofconditionimprovement.

350 J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359
Then, it follows from Eq. (2) that the expected discounted 2.2.Reliability-based maintenance model
| cost | of lifetime |     | extension | and | age replacement |     | over | an  |     |     |     |     |     |     |
| ---- | ----------- | --- | --------- | --- | --------------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
unbounded horizon is 2.2.1.Condition and reliability deterioration
limEðKðn;aÞÞ Currently available structure management systems,
| n!1 |     |     |     |     |     |     |     |     | including | PONTIS | [27]      | and BRIDGIT | [28],     | are directly |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | ------ | --------- | ----------- | --------- | ------------ |
|     |     |     |     |     |     |     | !   |     | related   | to the | condition | states      | of bridge | elements.    |
|     | k   |     |     |     |     |     | k   |     |           |        |           |             |           |              |
X ½x þaic (cid:5)q þ½x þakc (cid:5) X The number of condition states is limited (e.g. five) for
|     | iw  | c L | F;i i | kw c L | P;k | 12  | q i |     |     |     |     |     |     |     |
| --- | --- | --- | ----- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
eachbridgeelement.Eachconditiondescribesthetypeand
| ¼i¼1 |     |     |     |     |     |     | i¼1 | ; ð9Þ |     |     |     |     |     |     |
| ---- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
|      |     | "   |     | !   |     | !#  |     |       |     |     |     |     |     |     |
k k severity of element deterioration in visual terms. PONTIS
|     |     |     | X aiq |     | X   |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
12 þak 12 q and BRIDGIT assume that the condition states incorporate
|     |     |     |     | i   |     | i   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | i¼1 |     | i¼1 |     |     |     |     |     |     |     |     |     |
alltheinformationnecessarytopredictfuturedeterioration
where c P;k is the time-dependent cost of preventive and use a Markovian deterioration model to predict the
replacement at age replacement interval k and c is the annual probability of transitions among condition states.
F;i
time-dependentcostofcorrectivereplacementatunittimei:
AsindicatedinRefs.[7,9],theMarkovianapproachused
The probability of failure q now depends on the lifetime in currently available bridge management systems has
i
extension strategy. several important limitations, such as: (a) severity of
Thelifetime-extendingmaintenancemodelcanbeusedto element deterioration is described in visual terms only;
optimise maintenance in both the design phase and the (b)elementconditiondeteriorationisassumedtobeasingle
application phase. In the design phase, the initial cost of stepfunction;(c)transitionratesamongconditionstatesofa
investmentcanbeoptimallybalancedagainstthefuturecost bridge element are not time dependent; and (d) bridge
of maintenance. In the application phase, the cost of system condition deterioration is not explicitly considered.
preventive maintenance (lifetime extension and preventive Experience gained in different countries shows that the
replacement) can beoptimally balanced against the cost of major part of the work on existing bridges depends on
corrective maintenance (corrective replacement and the load carrying capacity (or structural reliability) of the
failure) The lifetime-extension model enables optimal bridgesystem ratherthan theconditionstates ofthe bridge
maintenancedecisionstobedeterminedonthebasisofthe elements alone [7]. Consequently, bridge management
uncertainties in the deterioration (e.g. the loss of steel systems have to consider bridge reliabilitydeterioration.
thicknessduetocorrosion).Themodelhasbeensuccessfully Fig. 4 shows simplified (i.e. linear) condition index and
appliedinRef.[2]tooptimisetheapplicationofaprotective
|     |     |     |     |     |     |     |     |     | reliability | index | deterioration | models | (also called | profiles). |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ----- | ------------- | ------ | ------------ | ---------- |
steelcoating.Twoexamplesofacost-optimalfrequencyof These profiles are each defined by three variables:
| lifetime-extending |     |     | maintenance |     | are shown | in  | Figs. 2 | and 3 |     |     |     |     |     |     |
| ------------------ | --- | --- | ----------- | --- | --------- | --- | ------- | ----- | --- | --- | --- | --- | --- | --- |
withrepeatingandnon-repeatinglifetimeextension,respect-
| ively.   | In the | first   | example, | the lifetime |       | of the | steel   | can be |     |     |     |     |     |     |
| -------- | ------ | ------- | -------- | ------------ | ----- | ------ | ------- | ------ | --- | --- | --- | --- | --- | --- |
| extended |        | by grit | blasting | (with        | 0.1mm |        | loss of | steel  |     |     |     |     |     |     |
thickness),aswellasplacingthenewcoating.Theexpected
conditionwithoutlifetimeextensioninFig.2representsthe
corrosionprocessgiveninitiationattimezero.
2.1.6. Inspection
Strictlyspeaking,maintenanceonthebasisofpreventive
| maintenance |     | levels | depends | on  | two | decision | variables: |     |     |     |     |     |     |     |
| ----------- | --- | ------ | ------- | --- | --- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
(i)therateofinspection(dependingonbothfrequencyand
| accuracy)     |     | and         | (ii) the | preventive      |     | maintenance |          | level. |     |     |     |     |     |     |
| ------------- | --- | ----------- | -------- | --------------- | --- | ----------- | -------- | ------ | --- | --- | --- | --- | --- | --- |
| These         | two | variables   | are      | interdependent: |     | with        | a high   | rate   |     |     |     |     |     |     |
| of inspection |     | it suffices |          | to choose       | the | preventive  | mainten- |        |     |     |     |     |     |     |
anceleveltobeclosetothefailurelevel,whereaswithalow
| rate        | of inspection |               | the preventive |               | maintenance |         | level       | should |     |     |     |     |     |     |
| ----------- | ------------- | ------------- | -------------- | ------------- | ----------- | ------- | ----------- | ------ | --- | --- | --- | --- | --- | --- |
| be          | larger        | than          | the failure    | level.        | Therefore,  |         | preventive  |        |     |     |     |     |     |     |
| maintenance |               | levels        | determined     |               | with        | an age  | replacement |        |     |     |     |     |     |     |
| model       | are           | approximately |                | cost-optimal. |             | If      | the cost    | of     |     |     |     |     |     |     |
| inspection  |               | is taken      | into           | account,      | a more      | complex | model       | of     |     |     |     |     |     |     |
condition-basedpreventivemaintenanceshouldbeused[see
| [24,25]].      | Other     | tailor-made |                 | examples |          | include     | determining  |     |     |                                              |     |     |     |     |
| -------------- | --------- | ----------- | --------------- | -------- | -------- | ----------- | ------------ | --- | --- | -------------------------------------------- | --- | --- | --- | --- |
| cost-optimal   |           | rates       | of inspection   |          | for berm | breakwaters |              | and |     |                                              |     |     |     |     |
| the            | blockmats | ofthe       | Eastern–Scheldt |          |          | barrier     | [see[26,22], |     |     |                                              |     |     |     |     |
| respectively]. |           |             |                 |          |          |             |              |     |     | Fig.4.(a)Conditionand(b)reliabilityprofiles. |     |     |     |     |

J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359 351
| (a) the | condition profile                            | is  | defined | by the | initial | condition |     |     |     |     |     |     |     |
| ------- | -------------------------------------------- | --- | ------- | ------ | ------- | --------- | --- | --- | --- | --- | --- | --- | --- |
|         | ;thetimeofconditiondeteriorationinitiation,t |     |         |        |         | ;         |     |     |     |     |     |     |     |
index,C
|         | 0                       |     |       |     |         | iC          |     |     |     |     |     |     |     |
| ------- | ----------------------- | --- | ----- | --- | ------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
| and the | condition deterioration |     | rate, | a ; | (b) the | reliability |     |     |     |     |     |     |     |
C
indexprofile(alsocalledreliabilityprofile)isdefinedbythe
| initial reliability | index, | b;  | the time | of  | reliability | index |     |     |     |     |     |     |     |
| ------------------- | ------ | --- | -------- | --- | ----------- | ----- | --- | --- | --- | --- | --- | --- | --- |
0
| deterioration | initiation, | t; and | the reliability |     | index | deterio- |     |     |     |     |     |     |     |
| ------------- | ----------- | ------ | --------------- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
i
a:
| ration | rate, As | indicated | in  | Ref. | [29] | there are |     |     |     |     |     |     |     |
| ------ | -------- | --------- | --- | ---- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
fundamentaldifferencesbetweentheconditiondeterioration
| profile | (Fig. 4(a)) and | the | reliability | deterioration |     | profile |     |     |     |     |     |     |     |
| ------- | --------------- | --- | ----------- | ------------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
(Fig.4(b)).
| First,        | the condition | deterioration |         | profile     |               | refers to  |     |     |     |     |     |     |     |
| ------------- | ------------- | ------------- | ------- | ----------- | ------------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
| deterioration | in visual     | terms.        | The     | reliability | deterioration |            |     |     |     |     |     |     |     |
| profile       | refers to the | deterioration | of      | a proper    |               | measure of |     |     |     |     |     |     |     |
| structural    | performance   | defined       | by      | the         | reliability   | index.     |     |     |     |     |     |     |     |
| For example,  | considering   | the           | element | 107         | from          | PONTIS     |     |     |     |     |     |     |     |
[27]representingpaintedsteelopengirders,Fig.5(a)shows
| the gradual | transition | among | five | condition |     | states: no |     |     |     |     |     |     |     |
| ----------- | ---------- | ----- | ---- | --------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
corrosion(paintsystemsoundandfunctioningasintended),
¼t
| t#t ic | C1 ; paint | distress, | t C1 ,t#t  | C2  | ; rust  | formation, |     |     |     |     |     |     |     |
| ------ | ---------- | --------- | ---------- | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
| t ,t#t | ; active   | corrosion | (corrosion |     | present | but any    |     |     |     |     |     |     |     |
C2 C3 Fig. 6. (a) Condition and (b) reliability profiles: condition-based
| section | loss resulting | from | active | corrosion | does | not yet |     |     |     |     |     |     |     |
| ------- | -------------- | ---- | ------ | --------- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- |
maintenance;improvementinconditionwithouteffectonreliability.
| warrantstructuralanalysis),t |            |         | #t#t |            | ;andsectionloss |            |     |     |     |     |     |     |     |
| ---------------------------- | ---------- | ------- | ---- | ---------- | --------------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
|                              |            |         | C3   | C4         |                 |            |     |     |     |     |     |     |     |
| (i.e. corrosion              | has caused | section | loss | sufficient |                 | to warrant |     |     |     |     |     |     |     |
structural analysis to ascertain the effect of damage), to the same element. In fact, an element may failsuddenly
:
t.t In contrast to the visual conditions indicated in (i.e.brittlefailure)even ifitsvisualcondition immediately
C4
Fig. 5(a), the reliability index deterioration profile in beforefailureisperfect,ormaybeextremelysafeevenifits
|           |           |             |             |     |               |     | visual condition |     | is extremely | poor. |     |     |     |
| --------- | --------- | ----------- | ----------- | --- | ------------- | --- | ---------------- | --- | ------------ | ----- | --- | --- | --- |
| Fig. 5(b) | refers to | the element | performance |     | deterioration |     |                  |     |              |       |     |     |     |
measured in terms of reliability index. The reliability Third, a maintenance action due to loss in condition
deterioration states (e.g. those indicated in Fig. 5(b)) are index(i.e.condition-basedmaintenance)canhavenoeffect
differentfromtheconditiondeteriorationstatesinFig.5(a). onreliabilityindex(seeFig.6)or,viceversa,amaintenance
Second, the condition and reliability deterioration action due to loss in reliability (i.e. reliability-based
|          |                 |       |             |     |         |            | maintenance) | can | have | no effect | on  | the | condition index |
| -------- | --------------- | ----- | ----------- | --- | ------- | ---------- | ------------ | --- | ---- | --------- | --- | --- | --------------- |
| profiles | may have little | or no | correlation |     | even if | they refer |              |     |      |           |     |     |                 |
(see Fig. 7).
Finally,systemeffects(e.g.combinedeffectsofdifferent
|     |     |     |     |     |     |     | failure modes | associated |       | with         | a bridge | element, | combined     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | ---------- | ----- | ------------ | -------- | -------- | ------------ |
|     |     |     |     |     |     |     | effects of    | failure    | modes | of different |          | members  | in a bridge, |
combinedeffectsofserviceabilityandultimatelimitstates)
canonlybecapturedbyreliabilitydeteriorationprofiles[9].
|     |     |     |     |     |     |     | 2.2.2. Reliability |     | index   | profileand | reliabilitystates |     |                  |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | ------- | ---------- | ----------------- | --- | ---------------- |
|     |     |     |     |     |     |     | The reliability    |     | profile | is defined | as                | the | variation of the |
reliabilityindexwithtimebðtÞ:AsdemonstratedinRef.[7],
|     |     |     |     |     |     |     | similar bridges |            | designed | and       | constructed |                | to the same    |
| --- | --- | --- | --- | --- | --- | --- | --------------- | ---------- | -------- | --------- | ----------- | -------------- | -------------- |
|     |     |     |     |     |     |     | requirements,   | for        | various  | reasons,  |             | end up         | with different |
|     |     |     |     |     |     |     | reliability     | levels.    | This     | variation |             | of reliability | index          |
|     |     |     |     |     |     |     | influenced      | by various |          | factors   | can         | be captured    | by using       |
randomvariables.
|     |     |     |     |     |     |     | The reliability                                 |            | profile    | bðtÞ          | is difficult |                | to predict for |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------------------------- | ---------- | ---------- | ------------- | ------------ | -------------- | -------------- |
|     |     |     |     |     |     |     | bridges under                                   |            | various    | maintenance   |              | interventions. | Fig. 8         |
|     |     |     |     |     |     |     | (adapted                                        | from       | Ref. [30]) | shows         | examples     |                | of reliability |
|     |     |     |     |     |     |     | profilesofdeterioratingstructuresassociatedwith |            |            |               |              |                | different      |
|     |     |     |     |     |     |     | maintenance                                     | scenarios. |            | E0 represents |              | the            | no maintenance |
|     |     |     |     |     |     |     | scenario,                                       | and E1     | represents | a             | maintenance  |                | scenario with  |
oneessentialmaintenance.E0;PandE1;Prepresentcyclic
|     |     |     |     |     |     |     | preventive | maintenance |     | scenarios | without |     | and with one |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ----------- | --- | --------- | ------- | --- | ------------ |
Fig.5.(a)Conditionand(b)reliabilitystates. essential maintenance, respectively.

352 J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359
Ingeneral,theservicelifeofdeterioratingstructuresisa
|     |     |     | progression | of          | reliability | states.        |     | In Ref.   | [9] five | reliability |
| --- | --- | --- | ----------- | ----------- | ----------- | -------------- | --- | --------- | -------- | ----------- |
|     |     |     | states      | are defined | for         | steel/concrete |     | composite |          | bridges as  |
follows:excellent(i.e.State5:b^9:0),verygood(i.e.State
|     |     |     | 4: 9:0.b^8:0), |     | good | (i.e. | State | 3: 8:0.b^6:0), |     | fair |
| --- | --- | --- | -------------- | --- | ---- | ----- | ----- | -------------- | --- | ---- |
(i.e.State2:6:0.b^4:6),andunacceptable(i.e.State1:
|     |     |     | b,4:6). | Notice | that | a new | (i.e. | as constructed) |     | bridge |
| --- | --- | --- | ------- | ------ | ---- | ----- | ----- | --------------- | --- | ------ |
belongingtoagroupofsimilarbridgesisnotnecessarilyin
State5,sincetheinitialreliabilityindexofthebridgegroupis
notcompletelyknown.
|     |     |     | 2.2.3.Theeightrandom |         |        | variablesmaintenance |     |               |     | model     |
| --- | --- | --- | -------------------- | ------- | ------ | -------------------- | --- | ------------- | --- | --------- |
|     |     |     | The                  | eight   | random | variables            |     | affecting     | the | lifetime  |
|     |     |     | reliability          | profile | of     | an individual        |     | deteriorating |     | structure |
oragroupofdeterioratingstructuresundermaintenanceare
|     |     |     | shown     | in Fig. | 9 (adapted  |             | from | Ref. [9]). | These   | random  |
| --- | --- | --- | --------- | ------- | ----------- | ----------- | ---- | ---------- | ------- | ------- |
|     |     |     | variables | are:    | the initial | reliability |      | index      | B ; the | time of |
0
;thereliabilityindexdeteriorationrate
|     |     |     | damageinitiationT                                 |               | I     |             |                   |             |               |        |
| --- | --- | --- | ------------------------------------------------- | ------------- | ----- | ----------- | ----------------- | ----------- | ------------- | ------ |
|     |     |     | A; the                                            | time of       | first | application | of                | preventive  | maintenance   |        |
|     |     |     | T ;thetimeofreapplicationofpreventivemaintenanceT |               |       |             |                   |             |               | ;      |
|     |     |     | PI                                                |               |       |             |                   |             |               | P      |
|     |     |     | the durationofpreventive                          |               |       |             | maintenanceeffect |             | onreliability |        |
|     |     |     | T ; the                                           | deterioration |       | rate        | of                | reliability | index         | during |
PD
Q;
|                       |                     |                             | preventive | maintenance |     | effect |     | and the | improvement | in  |
| --------------------- | ------------------- | --------------------------- | ---------- | ----------- | --- | ------ | --- | ------- | ----------- | --- |
| Fig. 7. (a) Condition | and (b) reliability | profiles: reliability-based |            |             |     |        |     |         |             |     |
reliabilityindex(ifany)immediatelyaftertheapplicationof
maintenance;improvementinreliabilitywithouteffectoncondition.
|     |     |     |            | maintenanceG: |     |     |          |     | B ; T ; | A; T ; T ; |
| --- | --- | --- | ---------- | ------------- | --- | --- | -------- | --- | ------- | ---------- |
|     |     |     | preventive |               |     |     | The PDFs | of  | 0 I     | PI P       |
Fig.8.Reliabilityprofilesassociatedwithdifferentmaintenancescenarios.

J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359 353
Fig.9.Reliabilityprofilesandassociatedrandomvariablesfortheoptionswithorwithoutpreventivemaintenance.
| ; Q; | G;  |     |     |     |     | t¼0). |     |     |     |     |     |     |
| ---- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
T PD and and their main descriptors for a group of time (say, at The reliability states are those defined
steel/concrete composite bridges are indicated in Ref. [9]. previously and the eight random variables of the mainten-
|     |     |     |     |     | ance model | in  | Fig. | 8 are defined | in  | Ref. [9]. | The | time |
| --- | --- | --- | --- | --- | ---------- | --- | ---- | ------------- | --- | --------- | --- | ---- |
variationofthenumberofbridgesineachreliabilitystateis
| 2.2.4. Monte                                | Carlo simulation                       |                |             |            |              |            |            |                |             |            |             |        |
| ------------------------------------------- | -------------------------------------- | -------------- | ----------- | ---------- | ------------ | ---------- | ---------- | -------------- | ----------- | ---------- | ----------- | ------ |
|                                             |                                        |                |             |            | indicated    | in Fig.    | 11         | [10] for the   | options     | with       | and without |        |
| Monte                                       | Carlo simulation                       | is used to     | generate    | the random |              |            |            |                |             |            |             |        |
|                                             |                                        |                |             |            | maintenance. | The        | beneficial | effect         | of          | preventive | mainten-    |        |
| numbersforthePDFsoftheeightrandomvariablesB |                                        |                |             | ;T ;       |              |            |            |                |             |            |             |        |
|                                             |                                        |                |             | 0 I        | ance is      | clearly    | indicated  | by the         | substantial | decrease   |             | in the |
| A;T ;T                                      | ;T ;Q;andGandtocapturethepropagationof |                |             |            |              |            |            |                |             |            |             |        |
| PI                                          | P PD                                   |                |             |            | number       | of bridges | in         | criticalStates | 1           | and 2.     |             |        |
| uncertainties                               | during the                             | entire service | of existing | deterior-  |              |            |            |                |             |            |             |        |
atingstructures.Asaqualitativeexample,Fig.10showsthe
2.2.5.Probabilityandcostprofilesfordifferentbridgetypes
| time variation | of the mean | and standard | deviation | of the |     |     |     |     |     |     |     |     |
| -------------- | ----------- | ------------ | --------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
reliability index of a bridge group for the options with and In order to choose the optimal maintenance strategy for
|     |     |     |     |     | each bridge | type, | the | present value | of  | the expected |     | cost of |
| --- | --- | --- | --- | --- | ----------- | ----- | --- | ------------- | --- | ------------ | --- | ------- |
withoutpreventivemaintenance.
ThesimulationprocessisalsocomputingthePDFofthe rehabilitation with and without preventive maintenance
|           |                 |                      |     |          | interventions | has | to  | be computed. | As  | a first | step | in this |
| --------- | --------------- | -------------------- | --- | -------- | ------------- | --- | --- | ------------ | --- | ------- | ---- | ------- |
| time when | the reliability | profile down-crosses |     | a target |               |     |     |              |     |         |      |         |
reliability level (also called rehabilitation time). As an complex computation, the probability of rehabilitation has
example,agroupof100steel/concretecompositebridgesis tobeobtained[31].Figs.12and13(adaptedfromRef.[31])
studiedassumingthatallbridgesareconstructedatthesame show the probability of rehabilitation for four bridge types
assumingthatnopreventivemaintenancehasbeendoneand
|     |     |     |     |     | preventive | maintenance |     | has | been | done, | respectively. |     |
| --- | --- | --- | --- | --- | ---------- | ----------- | --- | --- | ---- | ----- | ------------- | --- |
Thecomputationoftheseprobabilitiesisbasedontriangular
Fig.10.Timevariationofthemeanandstandarddeviationofthereliability
index of a bridge group for the options with and without preventive Fig.11.Expectednumberofbridgesineachreliabilitystatefromagroupof
maintenance. 100bridgesfortheoptionswithorwithoutpreventivemaintenance.

354 J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359
| Fig. 12. Probability |     | of rehabilitation |     | of four | bridge | types assuming | no  |                  |       |             |     |            |                  |     |         |
| -------------------- | --- | ----------------- | --- | ------- | ------ | -------------- | --- | ---------------- | ----- | ----------- | --- | ---------- | ---------------- | --- | ------- |
|                      |     |                   |     |         |        |                |     | Fig. 14. Present | value | of expected |     | cumulative | unit maintenance |     | cost of |
preventivemaintenancehasbeendone.
|     |     |     |     |     |     |     |     | steel/concrete | composite | bridges | [GBP/m2] | with | and | without preventive |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --------- | ------- | -------- | ---- | --- | ------------------ | --- |
distributionsofrehabilitationratespredictedbyexperts[31] maintenanceassuming6%discountrateforcost.
| for two | different | situations: |     | (a) rehabilitation |     | assuming | no  |                     |     |           |     |                |     |             |     |
| ------- | --------- | ----------- | --- | ------------------ | --- | -------- | --- | ------------------- | --- | --------- | --- | -------------- | --- | ----------- | --- |
|         |           |             |     |                    |     |          |     | a reliability-based |     | framework |     | for life-cycle |     | maintenance |     |
preventivemaintenancehasbeendoneand(b)rehabilitation
|          |            |     |             |     |      |       |          | analysis | and optimisation |       | of      | deteriorating | structures |            | based |
| -------- | ---------- | --- | ----------- | --- | ---- | ----- | -------- | -------- | ---------------- | ----- | ------- | ------------- | ---------- | ---------- | ----- |
| assuming | preventive |     | maintenance | has | been | done. | For each |          |                  |       |         |               |            |            |       |
|          |            |     |             |     |      |       |          | on the   | model            | shown | in Fig. | 10.           | Most       | input data | are   |
bridgetype,computationswereperformedaccordingtothe
|           |             |     |           |     |      |               |     | represented | by  | random | variables. |     | In this | manner, | the |
| --------- | ----------- | --- | --------- | --- | ---- | ------------- | --- | ----------- | --- | ------ | ---------- | --- | ------- | ------- | --- |
| following | assumptions |     | (Maunsell |     | Ltd. | and Transport |     |             |     |        |            |     |         |         |     |
uncertaintiesassociatedwithvariousmaintenanceinterven-
ResearchLaboratory,[32]):(a)thepreventivemaintenance
|              |     |         |              |     |                 |     |        | tions, reliability |              | index | profiles, | and        | costs are | all taken | into |
| ------------ | --- | ------- | ------------ | --- | --------------- | --- | ------ | ------------------ | ------------ | ----- | --------- | ---------- | --------- | --------- | ---- |
| intervention | is  | defined | by repeating |     | the application |     | of the |                    |              |       |           |            |           |           |      |
|              |     |         |              |     |                 |     |        | account.           | Optimisation |       | and       | parametric | analyses  | modules   |      |
triangular distribution [10,20,25], where 10, 20, and 25 helptheidentificationofthemaintenancestrategythatbest
indicatetheminimum,mode,andthemaximumnumberof
|                      |     |                |         |       |            |             |         | balance    | the present | value       | of  | the expected  | cumulative |                 | cost |
| -------------------- | --- | -------------- | ------- | ----- | ---------- | ----------- | ------- | ---------- | ----------- | ----------- | --- | ------------- | ---------- | --------------- | ---- |
| years, respectively; |     |                | and (b) | the   | triangular | probability |         |            |             |             |     |               |            |                 |      |
|                      |     |                |         |       |            |             |         | associated | with        | maintenance |     | interventions |            | and reliability |      |
| distributions        | of  | rehabilitation |         | rates | with       | and         | without |            |             |             |     |               |            |                 |      |
indexprofilesoveraspecifiedtimehorizonusuallyassumed
| preventive | maintenance |     | and | the unit | maintenance |     | costs |       |         |     |        |        |      |             |     |
| ---------- | ----------- | --- | --- | -------- | ----------- | --- | ----- | ----- | ------- | --- | ------ | ------ | ---- | ----------- | --- |
|            |             |     |     |          |             |     |       | to be | between | 30  | and 50 | years. | This | maintenance |     |
arethoseindicatedinMaunsellLtd.andTransportResearch optimisation can be performed for both an individual
| Laboratory  | [32]. |                 |     |                    |     |           |     |                 |     |         |                        |             |               |             |      |
| ----------- | ----- | --------------- | --- | ------------------ | --- | --------- | --- | --------------- | --- | ------- | ---------------------- | ----------- | ------------- | ----------- | ---- |
|             |       |                 |     |                    |     |           |     | structure       | and | a group | of                     | structures. | Additionally, |             | both |
| The results |       | are illustrated |     | for steel/concrete |     | composite |     |                 |     |         |                        |             |               |             |      |
|             |       |                 |     |                    |     |           |     | time-controlled |     | and/or  | reliability-controlled |             |               | maintenance |      |
bridges in Fig. 14 (adapted from Ref. [31]), where the scenarios can be considered. Numerical examples of cost
| expected | cumulative |     | costs are | discounted |     | topresent | values |              |        |     |               |     |               |          |     |
| -------- | ---------- | --- | --------- | ---------- | --- | --------- | ------ | ------------ | ------ | --- | ------------- | --- | ------------- | -------- | --- |
|          |            |     |           |            |     |           |        | optimisation | oftime | of  | interventions |     | for different | mainten- |     |
usinganetdiscountrateforcostof6%.Fromthisfigureitis ancescenariosofdeterioratingbridgesaregiveninRef.[30]
clearthatafterabout30yearsthestrategyusingpreventive
|             |     |                     |     |     |     |     |     | considering | a   | discount | rate | of 6%, | a time | horizon | of 50 |
| ----------- | --- | ------------------- | --- | --- | --- | --- | --- | ----------- | --- | -------- | ---- | ------ | ------ | ------- | ----- |
| maintenance | is  | the mosteconomical. |     |     |     |     |     |             |     |          |      |        |        |         |       |
years,agroupof713bridgesbuiltindifferenttimeperiods,
|     |     |     |     |     |     |     |     | and six | different | maintenance |     | scenarios | including | essential |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --------- | ----------- | --- | --------- | --------- | --------- | --- |
2.2.6. Optimisation maintenanceonly,preventivemaintenanceonly,andmixed
Recently, Kong and Frangopol [30] developed a preventive andessential maintenances.
| computer         | program | for         | life-cycle | analysis |         | and optimisation |          |         |            |     |     |     |     |     |     |
| ---------------- | ------- | ----------- | ---------- | -------- | ------- | ---------------- | -------- | ------- | ---------- | --- | --- | --- | --- | --- | --- |
| of deteriorating |         | structures. |            | This     | program |                  | provides |         |            |     |     |     |     |     |     |
|                  |         |             |            |          |         |                  |          | 3.Model | comparison |     |     |     |     |     |     |
3.1.Terminology
|     |     |     |     |     |     |     |     | Before          | explaining |                 | the                   | differences | and  | similarities |        |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | ---------- | --------------- | --------------------- | ----------- | ---- | ------------ | ------ |
|     |     |     |     |     |     |     |     | between         | the        | condition-based |                       | maintenance |      | model        | of     |
|     |     |     |     |     |     |     |     | Rijkswaterstaat |            | and             | the reliability-based |             |      | maintenance  |        |
|     |     |     |     |     |     |     |     | model of        | Frangopol, |                 | it should             | be noted    | that | both         | models |
useaslightlydifferentterminology.Forsakeofclarity,both
|     |     |     |     |     |     |     |     | terminologiesare |     | compared |     | inTable | 1.  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | -------- | --- | ------- | --- | --- | --- |
UnlikeRijkswaterstaat’smodel,preventivemaintenance
intermsofpreventivereplacementisnotexplicitlyincluded
|     |     |     |     |     |     |     |     | in Frangopol’s |     | model. | Replacement |     | is  | defined | as a |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ------ | ----------- | --- | --- | ------- | ---- |
Fig. 13. Probability of rehabilitation of four bridge types assuming combination of actions carried out to restore a component
preventivemaintenancehasbeendone. or structure, or to ‘renew’ it, to the initial condition.

J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359 355
|     |     |     |     |     |     |     | 8. performance/condition |     |     |     | improvement |     | at  | lifetime |
| --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | --- | ----------- | --- | --- | -------- |
Table1
| Comparisonofterminologyusedinthetwomaintenancemodels |     |     |                              |     |     |     | extension, |                |     |             |     |              |     |         |
| ---------------------------------------------------- | --- | --- | ---------------------------- | --- | --- | --- | ---------- | -------------- | --- | ----------- | --- | ------------ | --- | ------- |
|                                                      |     |     |                              |     |     |     | 9. cost    | of maintenance |     | (preventive |     | replacement, |     | correc- |
| Condition-basedmaintenance                           |     |     | Reliability-basedmaintenance |     |     |     |            |                |     |             |     |              |     |         |
model(Section2.1) model(Section2.2) tive replacement, lifetime extension),
10. time horizon,
11. discountrate.
| Condition        |     |     | Performance(e.g.reliabilityindex) |     |     |     |             |       |     |          |       |        |           |     |
| ---------------- | --- | --- | --------------------------------- | --- | --- | --- | ----------- | ----- | --- | -------- | ----- | ------ | --------- | --- |
| Initialcondition |     |     | Initialperformance                |     |     |     |             |       |     |          |       |        |           |     |
|                  |     |     |                                   |     |     |     | Frangopol’s | model |     | includes | eight | random | variables |     |
Preventivemaintenance Notexplicitlyincluded (i.e. uncertainties 1–8 above), whereas Rijkswaterstaat’s
level
|     |     |     |     |     |     |     | model includes | only | the | third | random | variable. | The | latter |
| --- | --- | --- | --- | --- | --- | --- | -------------- | ---- | --- | ----- | ------ | --------- | --- | ------ |
Failurelevel Targetlevel model assumes the other uncertainties to be deterministic
Replacement(renewal) Replacement and to be approximately incorporated in the uncertainty of
|     |     |     |     |     |     |     | the deterioration. |     | The former |     | model is | hence | more | flexible |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | ---------- | --- | -------- | ----- | ---- | -------- |
Preventivereplacement Notexplicitlyincluded thanthelatter.Forexample,inFrangopol’smodel,thetime
Correctivereplacement Essentialmaintenance of damage initiation can be different from the duration of
(replacement) effectoflifetimeextension,andthetimeoffirstapplication
Lifetimeextension Preventivemaintenance of lifetime extension can be different from the time of
(lifeextension) reapplication of lifetime extension. In Rijkswaterstaat’s
model,onlyonetimeofdamageinitiationandonlyonetime
| Initiationperiod(timeinterval |     |     | Damageinitiationtime |     |     |     |     |     |     |     |     |     |     |     |
| ----------------------------- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
inwhichnodeteriorationoccurs) of application of lifetime extension can be specified.
| Conditionimprovementat |     |     | Performanceimprovement     |     |     |     |                  |     |             |     |        |              |     |     |
| ---------------------- | --- | --- | -------------------------- | --- | --- | --- | ---------------- | --- | ----------- | --- | ------ | ------------ | --- | --- |
| lifetimeextension      |     |     | afterpreventivemaintenance |     |     |     | 3.3. Differences |     |             |     |        |              |     |     |
| Lifetime               |     |     | Rehabilitationtime         |     |     |     |                  |     |             |     |        |              |     |     |
|                        |     |     |                            |     |     |     | Although         | the | maintenance |     | models | of Frangopol |     | and |
Timehorizon Lifespan(servicelife) Rijkswaterstaat are quite similar, the following five
|          |        |         |            |           |     |            | differences         | can be | recognised:   |     |      |     |              |     |
| -------- | ------ | ------- | ---------- | --------- | --- | ---------- | ------------------- | ------ | ------------- | --- | ---- | --- | ------------ | --- |
|          |        |         |            |           |     |            | 1. multi-component, |        | multi-failure |     | mode | and | multi-uncer- |     |
| The main | reason | for not | explicitly | including |     | preventive |                     |        |               |     |      |     |              |     |
replacement is that bridge management mainly deals with tainty(Frangopol) vs.one component,one failure mode
|              |         |           |                 |       |         |             | and oneuncertainty |          |     | (Rijkswaterstaat), |        |            |            |     |
| ------------ | ------- | --------- | --------------- | ----- | ------- | ----------- | ------------------ | -------- | --- | ------------------ | ------ | ---------- | ---------- | --- |
| condition    | failure | rather    | than structural |       | failure | (collapse). |                    |          |     |                    |        |            |            |     |
|              |         |           |                 |       |         |             | 2. maintenance     | strategy |     | for                | groups | of similar | structures |     |
| In the event | of      | condition | failure,        | there | are     | no severe   |                    |          |     |                    |        |            |            |     |
consequences to failure and preventive replacement is not (Frangopol) vs. maintenance strategy for groups of
|               |     |           |       |            |             |     | similar(critical) |     | components(Rijkswaterstaat), |     |     |     |     |     |
| ------------- | --- | --------- | ----- | ---------- | ----------- | --- | ----------------- | --- | ---------------------------- | --- | --- | --- | --- | --- |
| cost-optimal. | On  | the other | hand, | preventive | replacement | is  |                   |     |                              |     |     |     |     |     |
implicitly included in Frangopol’s model in terms of 3. reliability-based(Frangopol)vs.condition-based(Rijks-
waterstaat),
| lifetime | extension.    | Lifetime-extending |             |     | maintenance | is         |               |             |     |     |              |     |              |     |
| -------- | ------------- | ------------------ | ----------- | --- | ----------- | ---------- | ------------- | ----------- | --- | --- | ------------ | --- | ------------ | --- |
|          |               |                    |             |     |             |            | 4. evaluation | (Frangopol) |     | vs. | optimisation |     | (Rijkswater- |     |
| defined  | as activities | that               | are carried |     | out to      | extend the |               |             |     |     |              |     |              |     |
staat),
| lifetime of | (a component |     | of) a structure. |     | Depending | on the |     |     |     |     |     |     |     |     |
| ----------- | ------------ | --- | ---------------- | --- | --------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
5. modelbasedonMonteCarlosimulation(Frangopol)vs.
| systemlevel,areplacement |     |     | ononelevelcan |     | bealifetime- |     |     |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | ------------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
extending maintenance action on another level. For analyticalmodel(Rijkswaterstaat).
| example,     | renewing | a           | coating | can | be regarded | as a       |                |           |             |                |         |                   |             |      |
| ------------ | -------- | ----------- | ------- | --- | ----------- | ---------- | -------------- | --------- | ----------- | -------------- | ------- | ----------------- | ----------- | ---- |
|              |          |             |         |     |             |            | The main       | objective |             | for developing |         | Rijkswaterstaat’s |             |      |
| replacement  | of       | the coating | itself  | as  | well as     | a lifetime |                |           |             |                |         |                   |             |      |
|              |          |             |         |     |             |            | model was      | to offer  | the         | maintenance    | manager |                   | a simple    | tool |
| extensionofa | steel    | plate.      |         |     |             |            |                |           |             |                |         |                   |             |      |
|              |          |             |         |     |             |            | for optimising | the       | maintenance |                | of      | critical          | components. |      |
|              |          |             |         |     |             |            | Therefore,     | the model | focuses     |                | only on | one component,    |             | one  |
3.2. Uncertainties
|     |     |     |     |     |     |     | failure mode | and | one | uncertainty. | In  | order | to keep | the |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | ------------ | --- | ----- | ------- | --- |
mathematicstractable,onlythemostimportantuncertainty–
For modelling deterioration and maintenance, the the uncertainty in the deterioration–has been considered.
following uncertainties can be identified: Theuncertaintiesintheinitialconditionandthefailurelevel
|     |     |     |     |     |     |     | can be approximately |     |     | included | in the | uncertainty |     | in the |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | -------- | ------ | ----------- | --- | ------ |
1. initial performance/condition, deterioration. The maintenance model is based on an age
2. time ofdamage initiation, replacement strategy combined with the possibility of
3. deterioration rate withoutlifetime extension, lifetime extension. The ageing mechanism is described by
4. deterioration rate withlifetime extension, the gamma process. When the age replacement strategy is
5. time offirst application oflifetime extension, combined with a gamma-distributed deterioration, the
6. time ofreapplication oflifetime extension, expecteddiscountedcostcanbeexpressedinexplicitform.
7. durationof effect oflifetime extension, BecauseRijkswaterstaat’smodelisanalytic,thecombination

356 J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359
oftheintervalofagereplacementandtheintervaloflifetime The advantage of reliability-based maintenance is that the
extensionforwhichtheexpecteddiscountedcostisminimal reliability is explicitly taken into account. In condition-
canbedetermined.Inessence,Rijkswaterstaat’smodelisan based maintenance, the reliability only follows implicitly
optimisation model. Although Rijkswaterstaat’s model has aftertransformingconditiontoreliability.Theadvantageof
primarily been developed for specifying cost-optimal condition-based maintenance is that conditions can be
maintenance strategies for groups of similar components measured or inspected, whereas reliabilities must
[33], it can also be applied for determining maintenance be computed from conditions. Especially the effects of
strategiesforgroupsofsimilarstructures. lifetime extension on the reliability index are difficult to
The advantage of Frangopol’s model over Rijkswater- estimate.Becauseastructure’sreliabilitymustbecalculated
staat’s model is that more than one component, more than on the basis of a probabilistic analysis, Frangopol’s model
one failure mode and more than one uncertainty can be canbestberunbystructuralengineershavingknowledgeof
incorporated. In order to take account of all these probability.Rijkswaterstaat’smodel,ontheotherhand,can
components,failuremodes,anduncertainties,theexpected also be used by maintenance managers without much
cost cannot be calculated in explicit form. Instead, the knowledgeofprobability.Duetothedifferencebetweenthe
Monte Carlo simulation is used to compute the expected condition-based and reliability-based concepts, the
cumulativediscountedcost.Frangopol’smodelisalsomore management decisions associated with each of these
flexible in analysing all kinds of combinations of lifetime- concepts will ingeneral be different [29].
extending measures, such as time of first application of A detailed comparison of Frangopol’s model and
lifetime extension, time of reapplication of lifetime Rijkswaterstaat’s modelcan be found inTable 2.
extension, duration of effect of lifetime extension, and
performance improvement at lifetime extension. Because 3.4.Discountrate
the expected cumulative discounted cost cannot be
determined in explicit form, Frangopol’s model is an BothFrangopol’smodelandRijkswaterstaat’smodelare
evaluation model rather than an optimisation model. based on the notion of discounted cost. This cost is
However,veryrecentlyKongandFrangopol[30]extended determined by summing the (present) discounted values of
the capability of the original evaluation-based model to an the cost over a bounded or an unbounded time horizon,
optimisationmaintenancemodel.Maintenanceoptimisation under the assumption that the value of money decreases
can be performed by repeatedly evaluating different with time. The criterion of discounted cost is especially
maintenance strategies. Frangopol’s model has primarily usefulforbalancingtheinitialcostofinvestmentagainstthe
been developed for specifying a cost-optimal maintenance futurecostofmaintenance.Afterchoosingthediscountrate,
strategy for groups of similar structures on the basis of different investment decisions can be compared and the
ageing components. Groups of similar bridges are formed decision with minimal expected discounted cost is often
byclassifyingbridgesonthebasisofthebridgetypeandthe preferred. The choice of the discount rate is mainly a
construction period. The parameters of the maintenance political decision; it serves as an agreement on comparing
modelare assessed using expertjudgement. investments.IntheUnitedStatesandtheUnitedKingdom,a
The main conceptual difference between Frangopol’s discountrateofabout4and6%,respectively,hasbeenused;
modelandRijkswaterstaat’smodelisthattheformermodel intheNetherlands,adiscountrateof4%isusuallychosen.
is reliability-based and the latter model is condition-based. A characteristic feature of the discount rate is the later
Reliability-based means that the performance is quantified futurecostisincurred,thelessitspresentvalueandtheless
intermsofthereliabilityindexorbetaindexb¼2F21ðpÞ; weightitcarriesinacost-basedcomparison.Forcalculating
where p is the failure probability. Condition-based means the expected discounted cost, [4,7,12] use a bounded
thattheperformanceisquantifiedintermsofthecondition, horizon, whereas Rijkswaterstaat uses an unbounded
such as the surplus of average steel thickness, the overall horizon. It is interesting to note that the same argument
functional quality, etc. Note that this condition does not leads to either of the two choices. For high discount rates
have to coincide with the visual condition. When both (largerthan6%),futurecostincurred50yearsfromnowis
models are used to model the deterioration of the same small in comparison with the non-discounted cost. On the
component, the target performance level should be the otherhand,Rijkswaterstaatarguesthat‘insituationswitha
same; that is, the target reliability index in Frangopol’s boundedtimehorizonlargerthan50years,thecostoveran
model (so-called ‘target level’) and the target condition in unbounded horizon may serve as a good approximation’.
Rijkswaterstaat’s model (so-called ‘failure level’) should The advantage of the latter approach is that the renewal
represent the same target failure probability. As soon as theory offers us a simple analytical formula for computing
the reliability index drops below the target level or, the expected discounted cost over an unbounded horizon
equivalently, the condition drops below the failure level, [20,21]. As opposed to Frangopol’s model, Rijkswater-
corrective/essentialmaintenance shouldbe carried out. staat’s model can be used to calculate the expected
Reliability-based management represents the future discounted cost over both a bounded and an unbounded
generation of bridge management systems [9,34]. horizon.

J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359 357
Table2
Comparisonofthetwomaintenancemodels
Maintenancemodel Condition-basedmaintenancemodel(Section2.1) Reliability-basedmaintenancemodel(Section2.2)
| State         |     | Condition-based  | Reliability-based(betaindex) |
| ------------- | --- | ---------------- | ---------------------------- |
| Uncertainties |     | (i)Deterioration | (i)Initialperformance,       |
(ii)Damageinitiationtime
(iii)Deteriorationratewithlifetimeextension
(iv)Deteriorationratewithoutlifetimeextension
(v)Timeoffirstapplicationoflifetimeextension
(vi)Timeofreapplicationoflifetimeextension
(vii)Durationofeffectoflifetimeextension
(viii)Performanceimprovementatlifetimeextension
Deterioration Deteriorationaccordingtogammaprocess Uniformly-distributeddeteriorationrateassumed,
withindependentincrements butanytypeofdistributioncanbeused
| Complexity    |     | Low          | High       |
| ------------- | --- | ------------ | ---------- |
| Decisionbasis |     | Optimisation | Evaluation |
Decisionvariables (i)Uniformintervalsoflifetime (i)Uniformandnon-uniformintervalsoflifetimeextension
extensionandpreventivereplacement
(ii)Non-uniformintervalsof (ii)Non-uniformintervalsofessentialmaintenance
correctivereplacement
Systemlevelconsidered Groupsofsimilarcomponentsor Groupsofsimilarstructuresorindividualstructures
individual(critical)components
| Numberofcomponents   |     | One | Morethanone |
| -------------------- | --- | --- | ----------- |
| Numberoffailuremodes |     | One | Morethanone |
Possiblemaintenanceactionsandtheir (i)Lifetimeextension (i)Lifetimeextension
cost
(ii)Preventivereplacement (ii)Essentialmaintenance
(iii)Correctivereplacement
| Implementation      |         | Analyticalmodel     | MonteCarlosimulation     |
| ------------------- | ------- | ------------------- | ------------------------ |
| Computerenvironment |         | Personalcomputer    | Workstation              |
| Timehorizon         |         | Boundedandunbounded | Bounded                  |
| Discountrate        |         | Greaterthanzero     | Greaterthanorequaltozero |
| 3.5. Deterioration  | process |                     | 4. Conclusions           |
The two maintenance models represent the uncertainty This paper described and compared two maintenance
in the deterioration in a different manner. In Frangopol’s models that are currently being used to optimally balance
model, the expected deterioration is described by a model structuralreliabilityandlife-cyclecostofdeterioratingcivil
being linear or quadratic in time; the coefficients of these infrastructure.Frangopol’smodelcontributedtothefurther
models are assumed to be random variables. In Rijkswa- development of the bridge maintenance methodology that
terstaat’s model, the expected deterioration is described by has been set up by the UK Highways Agency, whereas
a power law in time; the deterioration process is assumed Rijkswaterstaat’s model has been applied in the
to be a stochastic process (gamma process) with Netherlands. Although the two maintenance models are
independent increments. Although the former approach quite similar, the following differences can be identified.
may serve as a good approximation, the latter approach is The former model is reliability-based and treats the multi-
more realistic. However, the former approach is more component, multi-failure mode and multi-uncertainty case.
flexible in accommodating real data. Another difference is The latter model is condition-based and treats only one
that Frangopol’s model includes reliability deterioration component,onefailuremodeandoneuncertainty.Another
and Rijkswaterstaat’s model includes condition difference is that Frangopol’s model uses Monte Carlo
deterioration. simulation, whereas Rijkswaterstaat’s model is analytic.

358 J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359
| Furthermore,the |     | maintenancemodels |     |     | differ | in the | way the |               |            |     |               |        |     |         |         |
| --------------- | --- | ----------------- | --- | --- | ------ | ------ | ------- | ------------- | ---------- | --- | ------------- | ------ | --- | ------- | ------- |
|                 |     |                   |     |     |        |        |         | international | conference |     | on structural | faults | and | repair, | London, |
uncertainty in the deterioration is modelled; that is, United Kingdom, 1999. Edinburgh: Engineering Technics Press;
| uncertain     | parameters        |     | as opposed     | to        | stochastic | processes,     |     | 1999.         |                |                 |             |       |                    |       |        |
| ------------- | ----------------- | --- | -------------- | --------- | ---------- | -------------- | --- | ------------- | -------------- | --------------- | ----------- | ----- | ------------------ | ----- | ------ |
|               |                   |     |                |           |            |                |     | [3] Frangopol | DM.            | A probabilistic |             | model | based on           | eight | random |
| respectively. | Due               | to  | the difference |           | between    | the condition- |     |               |                |                 |             |       |                    |       |        |
|               |                   |     |                |           |            |                |     | variables     | for preventive |                 | maintenance | of    | bridges. Presented |       | at the |
| based and     | reliability-based |     |                | concepts, | the        | management     |     |               |                |                 |             |       |                    |       |        |
progressmeetingoptimummaintenancestrategiesfordifferentbridge
| decisions | associated |     | with each | of  | these concepts |     | will in |     |     |     |     |     |     |     |     |
| --------- | ---------- | --- | --------- | --- | -------------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
types,London:HighwaysAgency;1998.
general bedifferent. [4] FrangopolDM.(2000).Optimummaintenancestrategiesfordifferent
The authors believe that the two models could benefit bridgetypes:projectdescriptionandsteel/concretecompositebridges,
vol.1,FinalreporttotheHighwaysAgency,London,UK.
from one another. For example, Frangopol’s multi-com- [5] Frangopol DM. (2003). Preventative Maintenance Strategies for
ponent, multi-failure mode and multi-uncertainty model Bridge Groups-Analysis, Volume 1, Final Report to the Highways
Agency,London,U.K.
| could benefit |     | from | the analytic |     | formulas | for both | the |     |     |     |     |     |     |     |     |
| ------------- | --- | ---- | ------------ | --- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
[6] FrangopolDM.Life-cyclecostanalysisforbridges.Bridgesafetyand
| expected | discounted |     | cost over | an unbounded |     | time | horizon |     |     |     |     |     |     |     |     |
| -------- | ---------- | --- | --------- | ------------ | --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
reliability.Reston,Virginia:ASCE;1999.p.210–36.
| and the | stochastic | deterioration |     | process | of  | the Rijkswater- |     |     |     |     |     |     |     |     |     |
| ------- | ---------- | ------------- | --- | ------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
[7] FrangopolDM,DasPC.Managementofbridgestocksbasedonfuture
staatmodel.TheMonteCarlosimulationcanthenbeusedin reliabilityandmaintenancecosts.BridgeDesign,Construction,and
both models to determine the probabilistic characteristics Maintenance. Thomas Telford, London: The Institution of Civil
Engineers;1999.p.45–58.
| per renewal | cycle, | which | can | subsequently |     | be up scaled | to  |               |     |           |     |      |            |     |         |
| ----------- | ------ | ----- | --- | ------------ | --- | ------------ | --- | ------------- | --- | --------- | --- | ---- | ---------- | --- | ------- |
|             |        |       |     |              |     |              |     | [8] Frangopol | DM, | Gharaibeh | ES, | Kong | JS, Miyake | M.  | (2000). |
anunboundedhorizonusingrenewaltheory.Theauthorsare
|             |     |               |     |          |     |           |     | Optimal | network-level |       | bridge      | maintenance | planning   | based          | on  |
| ----------- | --- | ------------- | --- | -------- | --- | --------- | --- | ------- | ------------- | ----- | ----------- | ----------- | ---------- | -------------- | --- |
| considering | a   | comprehensive |     | analysis | to  | determine | the |         |               |       |             |             |            |                |     |
|             |     |               |     |          |     |           |     | minimum | expected      | cost. | J Transport |             | Res Board, | Transportation |     |
most sensitive parameters of their maintenance models in Research Record, No. 1696, vol. 2, National Academy Press,
| future studies. |     |     |     |     |     |     |     | p. 26–33. |     |     |     |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
[9] FrangopolDM,KongJS,GharaibehES.Reliability-basedlife-cycle
managementofhighwaybridges.JComputCivilEngngASCE2001;
15(1):27–34.
|     |     |     |     |     |     |     |     | [10] KongJS,FrangopolDM,GharaibehES.Lifepredictionofhighway |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
Acknowledgements
bridgeswithorwithoutpreventivemaintenance.Proceedingsofthe
|     |     |     |     |     |     |     |     | 8th ASCE | special | conference |     | on probabilistic |     | mechanics | and |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------- | ---------- | --- | ---------------- | --- | --------- | --- |
The work reported by the first author was supported by structural reliability, Notre Dame, Indiana: University of Notre
theCivilEngineeringDivisionoftheNetherlandsMinistry Dame;2000.July24–26,6pagesonCD-ROM.
|               |        |        |        |           |             |        |     | [11] Rijkswaterstaat. |      | Workshop     | on  | optimal      | maintenance | of structures, |     |
| ------------- | ------ | ------ | ------ | --------- | ----------- | ------ | --- | --------------------- | ---- | ------------ | --- | ------------ | ----------- | -------------- | --- |
| of Transport, |        | Public | Works, | and Water | Management. |        | The |                       |      |              |     |              |             |                |     |
|               |        |        |        |           |             |        |     | October               | 4–6, | 2000, Delft, | The | Netherlands. | Utrecht:    | Ministry       | of  |
| first author  | thanks | Mr     | Leo    | Klatter,  | Mr Jaap     | Bakker | and |                       |      |              |     |              |             |                |     |
Transport,PublicWorksandWaterManagement,CivilEngineering
| Mr Harry | van | der Graaf | for | their | helpful | discussions | and |     |     |     |     |     |     |     |     |
| -------- | --- | --------- | --- | ----- | ------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Division;2000.
comments in developing the Rijkswaterstaat model. The [12] Das PC. Prioritization of bridge maintenance needs. In: Frangopol
second author thanks Prof. Palle Thoft-Christensen, DM,editor.Casestudiesinoptimaldesignandmaintenanceplanning
|            |     |          |          |     |        |       |         | of civil | infrastructure |     | systems. | Reston, | Virginia: | ASCE; | 1999. |
| ---------- | --- | -------- | -------- | --- | ------ | ----- | ------- | -------- | -------------- | --- | -------- | ------- | --------- | ----- | ----- |
| University | of  | Aalborg, | Denmark, |     | and Dr | Parag | Das and |          |                |     |          |         |           |       |       |
p.26–44.
| Dr Victoria   | Hogg, | from        | the | Highways   | Agency, |             | UK, for |                                                                     |     |     |     |     |     |     |     |
| ------------- | ----- | ----------- | --- | ---------- | ------- | ----------- | ------- | ------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|               |       |             |     |            |         |             |         | [13] McCallJJ.Maintenancepoliciesforstochasticallyfailingequipment: |     |     |     |     |     |     |     |
| their helpful |       | discussions | in  | developing | the     | maintenance |         |                                                                     |     |     |     |     |     |     |     |
asurvey.ManageSci1965;11:493–524.
model. He also thanks his former and current Ph.D. [14] Barlow RE, Proschan F. Mathematical theory of reliability. New
students Dr Jung S. Kong, who played a key role in York:Wiley;1965.
|              |     |        |             |          |                  |            |     | [15] Dekker | R. Applications |     | of maintenance |       | optimization | models:      | a   |
| ------------ | --- | ------ | ----------- | -------- | ---------------- | ---------- | --- | ----------- | --------------- | --- | -------------- | ----- | ------------ | ------------ | --- |
| implementing |     | the    | maintenance |          | model,           | Dr Emhaidy |     |             |                 |     |                |       |              |              |     |
|              |     |        |             |          |                  |            |     | review      | and analysis.   |     | Reliability    | Engng | Syst         | Saf 1996;51: |     |
| S. Gharaibeh |     | and Mr | Luis        | C. Neves | for cooperation. |            | The |             |                 |     |                |       |              |              |     |
229–40.
| partial | financial | support |     | of the | US National |     | Science |             |          |     |        |        |                 |        |     |
| ------- | --------- | ------- | --- | ------ | ----------- | --- | ------- | ----------- | -------- | --- | ------ | ------ | --------------- | ------ | --- |
|         |           |         |     |        |             |     |         | [16] Dekker | R, Scarf | PA. | On the | impact | of optimisation | models | in  |
Foundation through grants CMS-9506435, CMS-9912525, maintenancedecisionmaking:thestateoftheart.ReliabilityEngng
CMS-0217290 and of the UK Highways Agency is SystSaf1998;60:111–9.
|            |               |       |           |          |             |             |        | [17] van    | Noortwijk  | JM, | Peerbolte  |      | EB. Optimal |       | sand  |
| ---------- | ------------- | ----- | --------- | -------- | ----------- | ----------- | ------ | ----------- | ---------- | --- | ---------- | ---- | ----------- | ----- | ----- |
| gratefully | acknowledged. |       | The       | opinions | and         | conclusions |        |             |            |     |            |      |             |       |       |
|            |               |       |           |          |             |             |        | nourishment | decisions. |     | J Waterway | Port | Coastal     | Ocean | Engng |
| presented  | in this       | paper | are those | of       | the authors | and         | do not |             |            |     |            |      |             |       |       |
2000;126(1):30–8.
| necessarily    |     | reflect | the | views | of the | sponsoring |     |                                                                   |     |     |     |     |     |     |     |
| -------------- | --- | ------- | --- | ----- | ------ | ---------- | --- | ----------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|                |     |         |     |       |        |            |     | [18] FellerW,Anintroductiontoprobabilitytheoryanditsapplications, |     |     |     |     |     |     |     |
| organizations. |     |         |     |       |        |            |     | vol.1.NewYork:Wiley;1950.                                         |     |     |     |     |     |     |     |
|                |     |         |     |       |        |            |     | [19] KarlinS,TaylorHM.Afirstcourseinstochasticprocesses,2nded.    |     |     |     |     |     |     |     |
SanDiego:AcademicPress;1975.
|     |     |     |     |     |     |     |     | [20] vanNoortwijkJM.Explicitformulasforthevarianceofdiscounted |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
References
life-cyclecost.ReliabilityEngngSystSaf2003;80(2):185–95.
|     |     |     |     |     |     |     |     | [21] Rackwitz | R.  | Optimizing | systematically |     | renewed | structures. |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ---------- | -------------- | --- | ------- | ----------- | --- |
[1] van Noortwijk JM. Optimal replacement decisions for structures ReliabilityEngngSystSaf2001;73(3):269–79.
understochasticdeterioration.In:NowakAS,editor.Proceedingsof [22] vanNoortwijkJM,KlatterHE.Optimalinspectiondecisionsforthe
the eighth IFIP WG 7.5 working conference on reliability and blockmatsoftheEastern-Scheldtbarrier.ReliabilityEngngSystSaf
| optimizationofstructuralsystems,Krako´w,Poland,1998.AnnArbor: |     |     |     |     |     |     |     | 1999;65(3):203–11. |     |     |     |     |     |     |     |
| ------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- |
UniversityofMichigan;1998.p.273–80. [23] van Noortwijk JM. Optimal maintenance decisions on the basis of
[2] BakkerJD,vanderGraafHJ,vanNoortwijkJM.Modeloflifetime- uncertainfailureprobabilities.JQualMaintenanceEngng2000;6(2):
| extendingmaintenance.In:FordeMC,editor.Proceedingsofthe8th |     |     |     |     |     |     |     | 113–22. |     |     |     |     |     |     |     |
| ---------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |

J.M.vanNoortwijk,D.M.Frangopol/ProbabilisticEngineeringMechanics19(2004)345–359 359
[24] van Noortwijk JM, Cooke RM, Kok M. A Bayesian failure model [31] FrangopolDM,GharaibehES,KongJS,MiyakeM.(2000).Optimal
based on isotropic deterioration. Eur J Operation Res 1995;82(2): network-level bridge maintenance planning based on minimum
270–82. expected cost, J Transport Res Board, Transportation Research
[25] van Noortwijk JM, Kok M, Cooke RM. Optimal maintenance Record1696,vol.2,NationalAcademyPress,p.26–33.
decisions for the sea-bed protection of the Eastern-Scheldt barrier. [32] MaunsellLtd.andTransportResearchLaboratory(1998).Strategic
In:CookeR,MendelM,VrijlingH,editors.Engineeringprobabilistic reviewofbridgemaintenancecosts:Reporton1997/98Review,Draft
design and maintenance for flood protection. Dordrecht: Kluwer Report,TheHighwaysAgency,London.
AcademicPublishers;1997.p.25–56. [33] Klatter HE, van Noortwijk JM, Vrisou van Eck N. Bridge
[26] van Noortwijk JM, van Gelder PHAJM. Optimal maintenance management in the Netherlands; prioritisation based on network
decisionsforbermbreakwaters.StructSaf1996;18(4):293–309. performance.In:CasasJR,FrangopolDM,NowakAS,editors.First
[27] ThompsonPD,SmallEP,JohnsonM,MarshallAR.ThePontisbridge internationalconferenceonbridgemaintenance,safetyandmanage-
managementsystem.StructEngngInt,IABSE1998;8(4):303–8. ment (IABMAS), Barcelona, Spain, 14–17 July 2002. Barcelona:
[28] HawkH,SmallEP.TheBRIDGITbridgemanagementsystem.Struct International Center for Numerical Methods in Engineering
EngngInt,IABSE1998;8(4):309–14. (CIMNE);2002.
[29] Frangopol DM. Reliability deterioration and lifetime maintenance [34] Frangopol DM, Kong JS. Bridge management based on reliability
cost optimization. Keynote lecture in proceedings of the first statesandwholelifecost:fromtheorytoimplementation.In:Chang
international ASRANet colloquium on integrating structural F-K,editor.Structuralhealthmonitoring-thedemandsandchallenges.
reliability analysis with advanced structural analysis, July 8–10, BocaRaton:CRCPress;2001.p.403–19.
2002,Glasgow,Scotland;2002. [35] FrangopolDM,KongJS,GharaibehES.Bridgemanagementbased
[30] Kong JS, Frangopol DM. Life-cycle reliability-based maintenance onlifetimereliabilityandwholelifecosting:thenextgeneration.In:
costoptimizationofdeterioratingstructureswithemphasisonbridges. RyallMJ,ParkeGAR,HardingJE,editors.Bridgemanagementfour.
JStructEngng2003;129(6):818–28. London:ThomasTelford;2000.p.392–9.