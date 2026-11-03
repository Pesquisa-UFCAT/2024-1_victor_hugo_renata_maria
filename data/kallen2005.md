ReliabilityEngineeringandSystemSafety90(2005)177–185
www.elsevier.com/locate/ress
|     | Optimal | maintenance |              | decisions |      | under        | imperfect |     | inspection |     |     |
| --- | ------- | ----------- | ------------ | --------- | ---- | ------------ | --------- | --- | ---------- | --- | --- |
|     |         |             | Kallena,b,*, |           |      | Noortwijka,b |           |     |            |     |     |
|     |         |             | M.J.         |           | J.M. | van          |           |     |            |     |     |
aHKVConsultants,P.O.Box2120,NL-8203ACLelystad,TheNetherlands
bDelftInstituteofAppliedMathematics,FacultyofElectricalEngineering,MathematicsandComputerScience,
DelftUniversityofTechnology,P.O.Box5301,NL-2600GADelft,TheNetherlands
Availableonline8December2004
Abstract
The process industry is increasingly making use of Risk Based Inspection (RBI) techniques to develop cost and/or safety optimal
inspection plans. This paper proposes an adaptive Bayesian decision model to determine these optimal inspection plans under uncertain
deterioration.ItusesthegammastochasticprocesstomodelthecorrosiondamagemechanismandBayes’theoremtoupdatepriorknowledge
overthecorrosionratewithimperfectwallthicknessmeasurements.Thisisveryimportantintheprocessindustryascurrentnon-destructive
inspectiontechniquesarenotcapableofmeasuringtheexactmaterialthickness,norcantheseinspectionscoverthetotalsurfaceareaofthe
component.Thedecisionmodelfindsaperiodicinspectionandreplacementpolicy,whichminimizestheexpectedaveragecostsperyear.
The failure condition is assumed to be random and depends on uncertain operation conditions and material properties. The combined
deteriorationanddecisionmodelisillustratedbyanexampleusingactualplantdataofapressurizedsteelvessel.
q2004ElsevierLtd.Allrightsreserved.
Keywords:Maintenance;Riskbasedinspection;Gammaprocess;Adaptivebayesianupdating;Measurementerror;Renewalmodel
1. Introduction will degrade the quality of the construction material of the
|     |     |     |     |     |     | components. | Among the | most | common degradation |     | mech- |
| --- | --- | --- | --- | --- | --- | ----------- | --------- | ---- | ------------------ | --- | ----- |
In order to illustrate the requirements, which are anisms are internal and external thinning (e.g. due to
necessary for the development of a suitable model, we corrosion), stress corrosion cracking, brittle fracture and
| start with | a general | introduction | on current practices |     | inthe | fatigue. |     |     |     |     |     |
| ---------- | --------- | ------------ | -------------------- | --- | ----- | -------- | --- | --- | --- | --- | --- |
process industry concerning the use ofdecision models for The highest uncertainties in the decision model are
inspectionplanning. associated with the rate at which these mechanisms reduce
|     |     |     |     |     |     | the resistance | of the construction |     | material. | Inspections | are |
| --- | --- | --- | --- | --- | --- | -------------- | ------------------- | --- | --------- | ----------- | --- |
1.1. Risk based inspection used to reduce this uncertainty, but since current wall
|     |     |     |     |     |     | thickness | or crack length | measurement | techniques |     | are not |
| --- | --- | --- | --- | --- | --- | --------- | --------------- | ----------- | ---------- | --- | ------- |
Since the late 1980s, numerous companies and organiz- perfect, the measurements contain (small) errors. Some
ations have developed several qualitative and quantitative inspectiontechniques,e.g.ultrasonicwallthicknessmeasure-
|        |        |                 |                         |     |     | ments, are | highly accurate, | but | there is always | the | spatial |
| ------ | ------ | --------------- | ----------------------- | --- | --- | ---------- | ---------------- | --- | --------------- | --- | ------- |
| models | to aid | plant engineers | with the prioritization |     | of  |            |                  |     |                 |     |         |
componentinspections.Theaveragechemicalprocessplant variabilityinthemeasurements.Thismeansthatthequalityof
or refining installation will have thousands of components the material is not uniform for the whole component.
likepipelines,columns,heatexchangers,steamvessels,etc., Inspectionshavetobecarriedoutsuchthatthemostcritical
which operate under significant pressure. This pressure, spots are covered and suchthatthe average measurement is
representativeforthecompleteitem.Decisionmodelsshould
combinedwiththecorrosivenatureofthechemicalsinside
thesystemsandtheexposuretotheweatherontheoutside, takethesemeasurementerrorsintoaccount.
|     |     |     |     |     |     | 1.2. Current | methodologies |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------ | ------------- | --- | --- | --- | --- |
*Correspondingauthor.Address:HKVConsultants,P.O.Box2120,NL-
8203ACLelystad,TheNetherlands.Tel.:C31320294256;fax:C31320
Acommonapproachintacklingtheinspectionproblem,
253901.
E-mailaddress:m.j.kallen@hkv.nl(M.J.Kallen). is to start with a prioritization. This means that usually a
0951-8320/$-seefrontmatterq2004ElsevierLtd.Allrightsreserved.
doi:10.1016/j.ress.2004.10.004

M.J.Kallen,J.M.vanNoortwijk/ReliabilityEngineeringandSystemSafety90(2005)177–185
178
morequalitativemodelisusedtodeterminethecomponents 2.1.Corrosion state function
| which constitute |     | the highest | risk. | The | assumption |     | is that |     |     |     |     |     |     |     |
| ---------------- | --- | ----------- | ----- | --- | ---------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
80%oftheriskisgeneratedbyonly20%ofthecomponents. Thestatefunctionforthinningdueto(internal)corrosion
This prioritization is then followed by a detailed quantitat- is taken from[1] and is defined as:
iveanalysisofthesehigh-riskitems,inwhichtheremaining
|     |     |     |     |     |     |     |     |     | (cid:1) | (cid:2) |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     |         | Ct      | Pd  |     |     |     |
lifetimesareestimatedandtheconsequencesoffailuresare gðtÞZS 1K K ; (2)
|           |              |     |           |     |           |       |     |     |     | r   | 2r  |     |     |     |
| --------- | ------------ | --- | --------- | --- | --------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
| modelled. | The American |     | Petroleum |     | Institute | (API) | has |     |     | 0   | 0   |     |     |     |
published a large document [1], which describes the |fflfflfflfflfflfflfflffl{zfflfflfflfflfflfflfflffl} |{z}
|             |           |     |                |     |      |     |          |     | Resistance |     | Load |     |     |     |
| ----------- | --------- | --- | -------------- | --- | ---- | --- | -------- | --- | ---------- | --- | ---- | --- | --- | --- |
| methodology | developed |     | in cooperation |     | with | an  | industry |     |            |     |      |     |     |     |
sponsor group. This document has become a methodology whereS(MPaZ10bar),C(mm/yr)andP(bar)arerandom
initselfandisusedbymanycompaniesasabasisforfurther variables representing the material strength, corrosion rate
development. and operating pressure, respectively. This model assumes
Typically, structural reliability methods are used to thatthinningwillcauseafailureduetoductileoverload,i.e.
estimate the failure probabilities of the components. The thematerialbecomesdistortedandisnolongerabletocarry
conditionoftheconstructionmaterialisdescribedbyastate the stresses and loads which are present. The component
function g, which is represented by a resistance (R) minus diameterd(mm) andthe initialmaterialthicknessr (mm)
0
stress orload (L)model: areassumedtobeknown.Theamountofwalllossattimet
C!t
|        |     |     |     |     |     |     |     | is given | by  |          | (mm).      | Eq. (2) is a | stress–strength | model   |
| ------ | --- | --- | --- | --- | --- | --- | --- | -------- | --- | -------- | ---------- | ------------ | --------------- | ------- |
|        |     |     |     |     |     |     |     | where    | the | strength | is reduced | as the       | steel wall      | becomes |
| gZRKL: |     |     |     |     |     |     | (1) |          |     |          |            |              |                 |         |
thinner.Theequivalentstatefunctionintermsofwalllossis
|     |     |     |     |     |     |     |     | given | by  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
The uncertain variables in this model usually have normal (cid:1) (cid:2)
Pd
|             |           |      |          |            |     |          |     | gðtÞZ | r   | K   | KCt: |     |     | (3) |
| ----------- | --------- | ---- | -------- | ---------- | --- | -------- | --- | ----- | --- | --- | ---- | --- | --- | --- |
| probability | densities | with | suitable | parameters |     | assigned | to  |       | 0   |     |      |     |     |     |
2S
| them. The | failure | probability |     | is then | approximated |     | at the |     |     |     |     |     |     |     |
| --------- | ------- | ----------- | --- | ------- | ------------ | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
limitstategZ0orRZLbyusingareliabilityindexmethod The component is assumed to fail when the limit state is
reached,i.e.wheng(t)Z0.FromEq.(3)wecandeducethe
| (e.g. FORM: | First | Order | Reliability | Method). |     | Many | of the |     |     |     |     |     |     |     |
| ----------- | ----- | ----- | ----------- | -------- | --- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- |
methodscurrentlyappliedintheprocessindustry,alsomake critical safety margin m:
| useofasimplediscreteversionofBayes’theoremtoupdate |     |     |     |     |     |     |     |     | Pd  |     |     |     |     |     |
| -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|                                                    |     |     |     |     |     |     |     | mZr |     | :   |     |     |     |     |
prior knowledgeon the rate ofdegradation with inspection K (4)
|          |                |     |           |         |     |            |     |     | 0 2S |     |     |     |     |     |
| -------- | -------------- | --- | --------- | ------- | --- | ---------- | --- | --- | ---- | --- | --- | --- | --- | --- |
| results. | The likelihood |     | in Bayes’ | formula |     | represents | the |     |      |     |     |     |     |     |
Thismarginrepresentsarandomfailureconditionduetothe
| likelihood  | of an      | inspection | result | correctly | identifying |     | the |                 |     |     |       |     |     |     |
| ----------- | ---------- | ---------- | ------ | --------- | ----------- | --- | --- | --------------- | --- | --- | ----- | --- | --- | --- |
| state ofthe | component. |            |        |           |             |     |     | randomvariables |     |     | P and | S.  |     |     |
In the following sections a different approach to this Eachcomponentwillusuallyhaveacorrosionallowance
assignedtoit.Thisisavaluegivenbythemanufacturerof
| problem | is taken. | The gamma |     | stochastic | process | is  | used to |     |     |     |     |     |     |     |
| ------- | --------- | --------- | --- | ---------- | ------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
modelthedegradationandtheparametersofthisprocessare thecomponentandrepresentstheamountofwalllossupto
|         |                  |     |       |      |             |     |        | which | the component |     | is  | supposed to | function | safely under |
| ------- | ---------------- | --- | ----- | ---- | ----------- | --- | ------ | ----- | ------------- | --- | --- | ----------- | -------- | ------------ |
| updated | using inspection |     | data. | This | is inspired |     | by the |       |               |     |     |             |          |              |
successful application of this stochastic process to the normal operating conditions. In general, this corrosion
problem of optimally inspecting large civil structures like allowance is fairly conservative, therefore it should be less
|             |          |     |           |      |             |     |         | than | the failure | condition |     | m. This means | that | we can write |
| ----------- | -------- | --- | --------- | ---- | ----------- | --- | ------- | ---- | ----------- | --------- | --- | ------------- | ---- | ------------ |
| storm–surge | barriers | [2] | and dikes | [3]. | The purpose |     | of this |      |             |           |     |               |      |              |
paperistoillustratetheversatilityofthegammaprocessand thecorrosionallowanceasapercentageofthecriticalsafety
|     |     |     |     |     |     |     |     | margin: | rm  | with | 0%r%1. | We will | use this | value as the |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ---- | ------ | ------- | -------- | ------------ |
toshowthatthereisgreatpotentialforitsuseintheprocess
industry. Characteristically, in the development of most replacement level, i.e. we will preventively replace the
current models, many assumptions and simplifications are component if the wall loss is more than the corrosion
allowance.
appliedinordertokeepthemodelseasytouse.Wewilluse
| the same | assumptions |     | in order | to avoid | large | amounts | of  |           |     |                      |     |     |     |     |
| -------- | ----------- | --- | -------- | -------- | ----- | ------- | --- | --------- | --- | -------------------- | --- | --- | --- | --- |
|          |             |     |          |          |       |         |     | 2.2.Gamma |     | deteriorationprocess |     |     |     |     |
inputandtokeepthenecessaryinputassimpleaspossible.
|     |     |     |     |     |     |     |     | Instead |     | of using | a reliability | index | method, | we will |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | -------- | ------------- | ----- | ------- | ------- |
modelthecumulativewalllosswithagammaprocess.We
2. Modelling the deterioration willusethefollowingdefinitionforthegammadensitywith
|         |       |         |      |          |             |     |        | shape | parameter | aO0 | and | scale parameter | bO0 |     |
| ------- | ----- | ------- | ---- | -------- | ----------- | --- | ------ | ----- | --------- | --- | --- | --------------- | --- | --- |
| In this | paper | we will | only | consider | degradation |     | due to |       |           | ba  |     |                 |     |     |
corrosion,buttheapplicationofthismodelisnotrestricted Gaðxja;bÞZ xaK1expfKbxgI ðxÞ; (5)
|                |            |     |     |      |         |         |       |     |     | GðaÞ |     | ð0;NÞ |     |     |
| -------------- | ---------- | --- | --- | ---- | ------- | ------- | ----- | --- | --- | ---- | --- | ----- | --- | --- |
| to this damage | mechanism. |     | For | this | purpose | we will | first |     |     |      |     |       |     |     |
GðaÞZÐN
define the corrosion state function, after which the gamma where taK1eKtdt is the gamma function and the
tZ0
processwith suitableparameters is introduced. indicator function is defined as: I (x)Z1 for x2(0,N)
(0,N)

M.J.Kallen,J.M.vanNoortwijk/ReliabilityEngineeringandSystemSafety90(2005)177–185
179
and zero otherwise. The stationary gamma process with Nowonlytheuncertainvariablemfortheaveragecorrosion
shape function at O0 and scale parameter bO0 is a rate is left to be assessed. In Section 4, a suitable prior
tR0}
continuous-time process {X(t): with the following density for this variable is defined and the consequence of
| properties: |     |     |     |     |     |     | fixings | relative to | mis discussed. |     |     |     |
| ----------- | --- | --- | --- | --- | --- | --- | ------- | ----------- | -------------- | --- | --- | --- |
X(0)Z0
| (1) | with | probability | one, |     |     |     |     |     |     |     |     |     |
| --- | ---- | ----------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(2) XðtÞKXðtÞwGaðaðtKtÞ;bÞfor tOtR0, 3. Review of inspection modelsbased on
| (3) X(t)has | independentincrements. |     |     |     |     |     | the gamma | process |     |     |     |     |
| ----------- | ---------------------- | --- | --- | --- | --- | --- | --------- | ------- | --- | --- | --- | --- |
AsfirstproposedbyAbdel-Hameed[4],lettheamountof Inspection models based on the gamma process for
deteriorationattimetbedenotedbyX(t)andtheprobability
deteriorationarenotnew.Hereweprovideashortoverview
density function ofX(t)be given by of the application of the models in the past. None of the
ðxÞZGaðxjat;bÞ: followingreferencesdealwithimperfectinspections,which
| f XðtÞ |     |     |     |     |     | (6) |                |            |     |     |     |     |
| ------ | --- | --- | --- | --- | --- | --- | -------------- | ---------- | --- | --- | --- | --- |
|        |     |     |     |     |     |     | is the topicof | thispaper. |     |     |     |     |
TheamountofwalllossCtinthestatefunctiongivenbyEq. Abdel-Hameed[5,6]studiedanoptimalperiodicinspec-
(3)isthereforerepresentedbytheprocessX(t).Therearea tionpolicymodelbasedontheclassofincreasingpurejump
number of advantages to using the gamma process. Most Markovprocesses.Heprovidesahypotheticalexampleusing
interestingly, the increments are always positive, therefore thegammaprocess,whichisamemberofthisclass.Inhis
increasesinwallthicknessarenotallowedfor.Thefactthat model, failure can only be detected by inspection. Other
incrementsareindependentandthereforeexchangeablefits characteristicsofthemodelaretheuseofarandomfailure
well with the physics of corrosion and deterioration in levelandwear-dependentcosts.Park[7]consideredthesame
general. As opposed to the reliability-index method, the model as Abdel-Hameed, but failure is assumed to be
gammaprocessproperlymodelsthetemporalvariabilityof discoveredimmediatelywithouttheneedforaninspection.
the deterioration. Also,Parkconsideredafixedfailurelevelandthemodelwas
Usingmomentgeneratingfunctions,itcanbeproventhat latergeneralizedbyKongandPark[8]byincludingarandom
the expectation and the variance of the process X(t) are failurelevel.AnadaptiveBayesianversionofPark’smodel
given by: is presented by van Noortwijk et al. [9,10] in which the
|          |     |            |     |     |     |     | average | rate of deterioration |     | is uncertain. |     | This model also |
| -------- | --- | ---------- | --- | --- | --- | --- | ------- | --------------------- | --- | ------------- | --- | --------------- |
|          | a   |            |     | a   |     |     |         |                       |     |               |     |                 |
| EðXðtÞÞZ |     | VarðXðtÞÞZ |     | t:  |     |     |         |                       |     |               |     |                 |
t and (7) includes the first application of discounted costs. Jia and
|     | b   |     |     | b2  |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Christer[11]provideessentiallythesamemodelasPark[7],
| Assuming | that | the expectation |     | and variance |     | are linear in |     |     |     |     |     |     |
| -------- | ---- | --------------- | --- | ------------ | --- | ------------- | --- | --- | --- | --- | --- | --- |
buttheyincludeonemoredecisionvariable:theoptimaltime
time, i.e. ofthefirstinspection.Theoptimaltimeintervalforperiodic
|            |     |                |     |     |     |     | inspectionsthenstartsfromthetimeofthe |     |     |     |     | firstinspection. |
| ---------- | --- | -------------- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | ---------------- |
| EðXðtÞÞZmt |     | VarðXðtÞÞZs2t; |     |     |     |     |                                       |     |     |     |     |                  |
and
|     |     |     |     |     |     |     | More recently, | Dieulle | et  | al. [12] | and Grall | et al. [13,14] |
| --- | --- | --- | --- | --- | --- | --- | -------------- | ------- | --- | -------- | --------- | -------------- |
we find that the parameters of the process X(t) are defined treatedamoreextensiveinspection model basedonthatof
| as:     |     |         |     |     |     |     | Park[7].Itincludesanoptimizationforaperiodicinspections |               |     |       |      |                 |
| ------- | --- | ------- | --- | --- | --- | --- | ------------------------------------------------------- | ------------- | --- | ----- | ---- | --------------- |
|         |     |         |     |     |     |     | which                                                   | are scheduled | by  | means | of a | function of the |
| aZm2=s2 |     | bZm=s2; |     |     |     |     |                                                         |               |     |       |      |                 |
and (8) deterioration state. Failure is detected only by inspection
where m is the average deterioration rate and s2 is the and a cost of unavailability of the system per unit time is
includedtoaccountforrepairtimes.
varianceoftheprocess.Thesetwoparametersareuncertain
andassessingbothvariablesforeachindividualcomponent
| is very cumbersome. |        |     | In order  | to keep   | the method | practical    |               |          |     |     |     |     |
| ------------------- | ------ | --- | --------- | --------- | ---------- | ------------ | ------------- | -------- | --- | --- | --- | --- |
|                     |        |     |           |           |            |              | 4. Inspection | updating |     |     |     |     |
| and easy            | to use | for | the plant | engineer, | we         | will fix the |               |          |     |     |     |     |
standarddeviationsrelativetothemeanmthroughtheuse
Duetothefactthatmostcomponentsareusuallyatmost
| of a coefficient |     | of variation |     | y (this | coefficient | is often |     |     |     |     |     |     |
| ---------------- | --- | ------------ | --- | ------- | ----------- | -------- | --- | --- | --- | --- | --- | --- |
referred toas the COV): inspectedevery2years,withtheaverageinspectioninterval
beingabout6–8years,thereisnotenoughdataavailablefor
| sZnm0nZs=m: |     |     |     |     |     | (9) |               |           |       |          |           |        |
| ----------- | --- | --- | --- | --- | --- | --- | ------------- | --------- | ----- | -------- | --------- | ------ |
|             |     |     |     |     |     |     | a statistical | analysis. | Using | Bayesian | updating, | we can |
Thisapproachisusedinmanyoftoday’sRBImodelsforthe efficientlyincorporatetheinspectionmeasurementsandthe
|                  |           |          |               |            |           |          | engineer’s    | prior knowledge |     | or estimate |     | of the average |
| ---------------- | --------- | -------- | ------------- | ---------- | --------- | -------- | ------------- | --------------- | --- | ----------- | --- | -------------- |
| process          | industry: | the      | coefficients  | of         | variation | for the  |               |                 |     |             |     |                |
|                  |           |          |               |            |           |          | deterioration | rate m.         |     |             |     |                |
| uncertain        | variables | are      | predetermined |            | by expert | judgment |               |                 |     |             |     |                |
| and subsequently |           | fixed    | in            | the model. | Using     | (9), the |               |                 |     |             |     |                |
|                  |           |          |               |            |           |          | 4.1. Choosing | the prior       |     |             |     |                |
| probability      | density   | function | for           | X(t) in(6) | reduces   | to       |               |                 |     |             |     |                |
(cid:9)
|     | (cid:1) | t 1 | (cid:2) |     |     |     |     |     |     |     |     |     |
| --- | ------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ðxÞZGa (cid:9) ; : D u e t o th e la r g e n um b er o f c o m p o n e n ts a n d t h e u s u a l l y
| f XðtÞ | x   | (cid:9) |     |     |     | (10) |     |     |     |     |     |     |
| ------ | --- | ------- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
(cid:9)n 2 m n2 lim ite d e xp e rie n c e o f th e p la n t e n g in e e r w i th p r ob a b i l i t y

M.J.Kallen,J.M.vanNoortwijk/ReliabilityEngineeringandSystemSafety90(2005)177–185
180
betweentheengineer’sassessmentand2–3timesthisvalue.
|     |     |     |     |     |     |     | The | prior | density | in  | Fig. 1 | is arbitrarily |     | chosen | for the |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------- | --- | ------ | -------------- | --- | ------ | ------- |
purposeofdemonstration.Inpractice,theparametersofthis
densityshouldbedeterminedusingexpertjudgment.Asin
thediscretecase,onecouldalsodefineanumberofdifferent
defaultpriorsfromwhichthepractitionercanselecttheone
whichbestrepresentshisownconfidence/uncertaintyinthe
|     |     |     |     |     |     |     | degradation |                                              | rate. |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | -------------------------------------------- | ----- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |             | InthefollowingsectionswewilluseBayes’theorem |       |     |     |     |     |     | to  |
updatethepriordensitywithaninspectionmeasurementto
obtainaposteriordensity.ThecontinuousversionofBayes’
|     |     |     |     |     |     |     | theorem |     | is given | by  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | -------- | --- | --- | --- | --- | --- | --- |
lðxjmÞpðmÞ
|     |     |     |     |     |     |     | pðmjxÞZ |     |     |     |     | ;   |     |     | (12) |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | ---- |
ÐN
mZ0 lðxjmÞpðmÞdm
l(xjm)
|     |     |     |     |     |     |     | where             | p(m) | is  | the prior | density, |        | the             | likelihood | of       |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | ---- | --- | --------- | -------- | ------ | --------------- | ---------- | -------- |
|     |     |     |     |     |     |     | measurementxgiven |      |     |           | mand     | p(mjx) | isthe posterior |            | density. |
Fig.1.TheAPIdiscretepriorandtherelated(continuous)invertedgamma
density.
|            |         |           |        |               |           |             | 4.2.Case1: |            | perfect | inspections |          |       |       |         |       |
| ---------- | ------- | --------- | ------ | ------------- | --------- | ----------- | ---------- | ---------- | ------- | ----------- | -------- | ----- | ----- | ------- | ----- |
| theory, it | is not  | feasible  | to ask | this engineer |           | to assess a |            |            |         |             |          |       |       |         |       |
|            |         |           |        |               |           |             |            | The choice |         | for the     | inverted | gamma | prior | becomes | clear |
| suitable   | density | for m. In | line   | with current  | practices | in the      |            |            |         |             |          |       |       |         |       |
whenweonlyconsiderperfectinspections.Inotherwords,
processindustry,wewillonlyaskforanaveragecorrosion
|     |     |     |     |     |     |     | we  | first | assume | that | we  | can measure |     | the exact | wall |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------ | ---- | --- | ----------- | --- | --------- | ---- |
rateoverwhichadefaultdensitywillbeplaced.TheAPI[1]
|     |     |     |     |     |     |     | thickness. |     | We  | can then | precisely |     | determine | the | amount |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | -------- | --------- | --- | --------- | --- | ------ |
suggeststheuseofasimplediscretepriordensity,whichis
ofwalllossxattimetanditcanbeproventhattheposterior
| shown in | Fig. 1. | The idea | behind | this | density | is that the |        |     |       |     |     |     |     |     |     |
| -------- | ------- | -------- | ------ | ---- | ------- | ----------- | ------ | --- | ----- | --- | --- | --- | --- | --- | --- |
|          |         |          |        |      |         |             | p(mjx) | is  | given | by  |     |     |     |     |     |
modelhas50%confidenceinacorrosionratewhichisless
|     |     |     |     |     |     |     |     |     | (cid:13) | (cid:9) t |     | x(cid:12) |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --------- | --- | --------- | --- | --- | --- |
thanorequaltotherateassessedbytheplantengineer.The pðmjxÞZIg ;bC ;
|     |     |     |     |     |     |     |     |     | m   | (cid:9)aC |     |     |     |     | (13) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | ---- |
other 50% is divided into 30% between 1 and 2 times the (cid:9) n2 n2
assessedrateand20%between2and4timestheengineer’s whereaandbaretheparametersfromthepriordensity.In
| estimate. | These | probabilities |     | are suggested |     | when the |          |     |             |     |        |     |          |       |         |
| --------- | ----- | ------------- | --- | ------------- | --- | -------- | -------- | --- | ----------- | --- | ------ | --- | -------- | ----- | ------- |
|           |       |               |     |               |     |          | Bayesian |     | statistics, | the | family | of  | inverted | gamma | distri- |
confidenceinthedataorestimateislow.Theyaregenerally
butionsissaidtobeaconjugatefamilyforsamplesfroma
| obtained   | from    | published | data, | corrosion  | rate     | tables or |       |         |              |        |              |     |                  |     |      |
| ---------- | ------- | --------- | ----- | ---------- | -------- | --------- | ----- | ------- | ------------ | ------ | ------------ | --- | ---------------- | --- | ---- |
|            |         |           |       |            |          |           | gamma |         | distribution |        | with unknown |     | scale parameter. |     | This |
| predefined | default | values    | [1].  | The expert | judgment | or the    |       |         |              |        |              |     |                  |     |      |
|            |         |           |       |            |          |           | fact  | is also | used         | in[9]. |              |     |                  |     |      |
genericdeteriorationdataisnotexplicitlyassumedtobean Theequivalent of (13) for nR1 inspections is
| underestimation.      |     | We believe |           | that engineers |           | do not by    |       |      |         |     |     |     |     |     |     |
| --------------------- | --- | ---------- | --------- | -------------- | --------- | ------------ | ----- | ---- | ------- | --- | --- | --- | --- | --- | --- |
| default underestimate |     | the        | corrosion | rate,          | but       | prefer to be | pðmjx | ;.;x | Þ       |     |     |     |     |     |     |
|                       |     |            |           |                |           |              |       | 1    | n       |     |     |     |     |     |     |
| conservative          | and | use a      | higher    | expected       | corrosion | rate in      |       |      |         |     |     |     |     |     |     |
|                       |     |            |           |                |           |              |       |      | (cid:9) |     |     |     |     | !   |     |
case of uncertainty. Our experience with practices in the (cid:9) X n t Kt X n x Kx
|     |     |     |     |     |     |     |     | ZIg | m (cid:9)aC | i   | iK1;bC |     | i   | iK1 : |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------ | --- | --- | ----- | --- |
(cid:9)
processindustryhasshownthatplantengineersprefertobe (cid:9) n2 n2
|         |             |     |        |     |      |            |     |     |     | iZ1 |     |     | iZ1 |     |     |
| ------- | ----------- | --- | ------ | --- | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ‘on the | safe side’. | For | medium | and | high | confidence |     |     |     |     |     |     |     |     |     |
estimates, the distribution of densities for the three state whichreducesto
categories is {70%, 20%, 10%} and {80%, 15%, 5%}, (cid:13) (cid:9) t x (cid:12)
|               |       |         |       |     |      |              | pðmjx | ÞZIg | m(cid:9)aC |         | n ;bC                     | n ; |     |     | (14) |
| ------------- | ----- | ------- | ----- | --- | ---- | ------------ | ----- | ---- | ---------- | ------- | ------------------------- | --- | --- | --- | ---- |
| respectively. |       |         |       |     |      |              |       | n    |            | (cid:9) |                           |     |     |     |      |
|               |       |         |       |     |      |              |       |      |            |         | n2                        | n2  |     |     |      |
| For our       | gamma | process | model | we  | will | not use this |       |      |            |         |                           |     |     |     |      |
|               |       |         |       |     |      |              |       |      |            | Z0att   | Z0.Inotherwords,becausewe |     |     |     |      |
ifweassumethatx
| discrete       | prior, but | a continuous |     | inverted | gamma | density. |       |      |            | 0         | 0      |            |           |      |           |
| -------------- | ---------- | ------------ | --- | -------- | ----- | -------- | ----- | ---- | ---------- | --------- | ------ | ---------- | --------- | ---- | --------- |
|                |            |              |     |          |       |          | fixed | the  | standard   | deviation |        | s relative | to the    | mean | m, only   |
| The definition | ofthis     | density      | is  | given by |       |          |       |      |            |           |        |            |           |      |           |
|                |            |              |     |          |       |          | the   | last | inspection | is        | needed | to         | calculate | the  | posterior |
(cid:1) (cid:2)aC1 (cid:10) b(cid:11) density when using perfect measurements. This is not
ba 1
Igðxja;bÞZ exp K I ðxÞ: (11) surprising, as the last measurement supplies all the
|        | GðaÞ   |        |          |      | ð0;NÞ    |       |           |     |             |     |        |             |          |     |     |
| ------ | ------ | ------ | -------- | ---- | -------- | ----- | --------- | --- | ----------- | --- | ------ | ----------- | -------- | --- | --- |
|        |        | x      |          | x    |          |       |           |     |             |     |        |             |          |     |     |
|        |        |        |          |      |          |       | necessary |     | information |     | on the | degradation | process. |     |     |
| Notice | that a | random | variable | X is | inverted | gamma |           |     |             |     |        |             |          |     |     |
distributed if YZXK1wGaðxja;bÞ with shape parameter 4.3.Case2: imperfectinspections
| aO0 |       |           | bO0. |      |          |             |     |     |     |     |     |     |     |     |     |
| --- | ----- | --------- | ---- | ---- | -------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| and | scale | parameter |      | With | suitable | choices for |     |     |     |     |     |     |     |     |     |
the parameters, we can again define a default prior density Similar to Newby and Dagg [15], we consider a new
for m as is shown in Fig. 1. Most confidence is placed process Y(t), which includes the original process X(t)

M.J.Kallen,J.M.vanNoortwijk/ReliabilityEngineeringandSystemSafety90(2005)177–185 181
togetherwith anormallydistributed measurement error e: substitutedinBayes’formula(12),whichcanthenbesolved
by numerical integration to obtain the posterior
YðtÞZXðtÞCe; ewNð0;s Þ: (15)
e pðmjy ;.;y Þ.
1 n
ThesameapproachisalsousedbyWhitmore[16]toinclude Usingsimulationtodeterminethelikelihood(19)greatly
measurement error in a degradation model based on the reduces the efficiency of the model, but the choice for the
Wiener diffusion process. In Eq. (15), we assume the error priordistributionisthennolongerrestrictedtotheinverted
has a normal distribution with mean 0 and a standard gamma density. Other types of distributions can be used.
deviations.Takingameandifferentfromzerowouldmean This feature, together with the simplified implementation,
e
thattheinspectiontendstooverorunderestimatetheactual makessimulationmoreattractivecomparedtotheanalytical
wall loss. The likelihood of the measurement y given the approach. Also, to assess the effect of inspection depen-
corrosionratem is now determined bythe convolution dence,itiseasytointroducecorrelatedmeasurementerrors
ðN (e
k
) by sampling from a multivariate normal distribution.
lðyjmÞZf YðtÞ ðyÞZ f XðtÞ ðyKeÞf e ðeÞde; (16) Duetotheabsenceoftherequireddata,thisisnotincluded
KN
here.
where f ðyKeÞZGaðyKejat;bÞ is the likelihood of the
XðtÞ
gamma increment X(t) as given by (10). Similarly, the
likelihood for more than one inspection is given by
Y n 5. Decisioncriterion
lðyjmÞZ l ðy Ky jmÞ; nR1; (17)
Yðtk ÞKYðtkK1 Þ k kK1
kZ1
Theposteriorprobabilitydensityfunctionfortheaverage
whereyZ{y 1 ,.,y n }arethewalllossmeasurements.InEq. corrosion rate incorporates the plant engineer’s prior
(17), we have used the fact that the increments are knowledge and all the available inspection data. Using
independent. Introducing some notation: the increment of this density and the probability densities for the uncertain
X(t) between two inspections is defined as D k ZX(t k )K variables S (material strength) and P (operating pressure),
X(t ), the difference between two measurements is d Z
kK1 k theprobabilityoffailureorapreventivereplacementofthe
y Ky , where k Z1,2,.,n. Using this notation and the
k kK1 component can be calculated asa function of time.
integral convolution as in Eq. (16), the likelihood (17) can
Inspections in a process plant are very expensive due to
be rewritten as
the fact that the process often has to be stopped during the
ðN ðN n inspection.Also,becausemanycomponentscontainhighly
Y
lðyjmÞZ / f ðd Kd Þfðd ;.;d Þdd /dd ;
KN KN kZ1 D k k k 1 n 1 n c
a
o
n
r
d
ro
c
s
le
iv
a
e
ne
a
d
nd
b
/
e
o
f
r
or
t
e
ox
a
i
n
c
in
ch
te
e
r
m
na
ic
l
a
i
l
n
s
s
,
p
t
e
h
c
e
t
y
ion
ha
c
v
a
e
n
t
b
o
e
b
d
e
on
fl
e
u
.
s
T
he
h
d
e
(18)
waste resulting from this rinsing needs to be recycled or
where d Ze Ke . Clearly the d’s are not independent treatedbeforerelease,whichbringsaddedcoststothewhole
k k kK1
since every d depends on d . There are two options: procedure.Therefore,theplantengineerwouldliketomake
k kK1
calculate the covariances between the d’s and analytically acostoptimaldecisiononwhentoinspectthecomponents.
solvethelikelihoodusingthejointdistributionofthed’sor This means that he wants to maximize the time interval
simulate the e ’s and approximate the likelihood. Since betweentwosubsequentinspections.Ontheotherhand,he
k
the first option will complicate matters considerably, has to ensure that the component operates safely and
the simulation approach is used. The likelihood (18) can therefore inspections should not be executed at too large
be formulated as an expectation, which in turn can be time intervals. For this purpose a cost based criterion is
approximated by the average of the product used,calledtheexpectedaveragecostpertimeunit;seee.g.
( ) ( ) Ross [17]. This cost criterion is derived using renewal
lðyjmÞZE Y n f ðd Kd Þ z 1 X N Y n f ðd KdðjÞÞ theoryandusestheconceptofthecomponentlifecycle.The
Dk k k N Dk k k
kZ1 jZ1 kZ1 lengthofthiscycleisthetimefromtheservicestartuntila
(19) renewal, which is either a preventive replacement or a
corrective replacement due tofailure.
as N/N. Here the law of large numbers is applied to
Theexpectedaveragecostspertimeunitaregivenbythe
performaMonteCarlointegration.Foreachinspectionkwe
ratiooftheexpectedcostspercycleovertheexpectedcycle
(1) sample eðjÞ for jZ1,2,.,N and length: Cðr;m;DkÞZEðC I Þ=EðIÞ, where Dk is the periodic
(2) calculate k dðjÞZeðjÞKeðjÞ , then finally inspection interval (i.e. the time between successive in-
k k kK1 service inspections). The expected costs per cycle are
(3) calculate (19).
determined by the expected number of inspections during
(cid:13) (cid:12)
Note that f d KdðjÞ Z0 when dðjÞRd due to the thecycleandtheexpectedcostsduetoeitherapreventiveor
definitionofth D e k gam k ma k densityin(5).E k q.(19 k )cannowbe a corrective replacement

M.J.Kallen,J.M.vanNoortwijk/ReliabilityEngineeringandSystemSafety90(2005)177–185
182
|       |     | N   |                    |     |     |     |     |     | Table1 |     |     |     |     |     |     |
| ----- | --- | --- | ------------------ | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
| EðCÞZ | X   |     | ÞPrfXððjK1ÞDkÞ%rm; |     |     |     |     |     |        |     |     |     |     |     |     |
ðjc Cc Operational,materialandinspectiondataforahydrogendryer
|     | I   | I   | P   |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
jZ1
Componentandoperationaldata
|     | rm!XðjDkÞ%mgC½ðjK1Þc |     |     |     |     | Cc (cid:7) |     |     | Componenttype |     |     |     | Verticaldrum |     |     |
| --- | -------------------- | --- | --- | --- | --- | ---------- | --- | --- | ------------- | --- | --- | --- | ------------ | --- | --- |
I F
|     | !PrfXððjK1ÞDkÞ%rm;XðjDkÞOmg; |     |     |     |     |     |     |     | Materialtype |     |     |     | Carbonsteel |     |     |
| --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | ----------- | --- | --- |
ð20Þ
|                                                     |     |       |       |           |       |        |             |     | Servicestart             |     |     |     | 1977      |     |     |
| --------------------------------------------------- | --- | ----- | ----- | --------- | ----- | ------ | ----------- | --- | ------------------------ | --- | --- | --- | --------- | --- | --- |
|                                                     |     |       |       |           |       |        |             |     | Tensilestrength(s        |     | ):  |     | 413.69MPa |     |     |
| where                                               | c,  | c and | c are | resp. the | costs | for an | inspection, | a   |                          | T   |     |     |           |     |     |
|                                                     | I   | P     | F     |           |       |        |             |     | Yieldstrength(s          | )   |     |     | 206.84MPa |     |     |
| preventivereplacementandacorrectivereplacementdueto |     |       |       |           |       |        |             |     |                          | Y   |     |     |           |     |     |
|                                                     |     |       |       |           |       |        |             |     | Meanoperatingpressure(P) |     |     |     | 32bar(g)  |     |     |
failure.Theexpectedcyclelengthisgivenbytheexpected Drumdiameter(d) 1180mm
time of either a preventive replacement or failure: Initialmaterialthickness(r): 16.8mm
0
|     |     |     |     |     |     |     |     |     | Estimatedcorrosionrate(m) |     |     |     | 0.1mm/yr |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | -------- | --- | --- |
N
|       | X   |                                   |     |     |     |     |     |     | Corrosionallowance(rm) |     |     |     | 4.5mm |     |     |
| ----- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | ----- | --- | --- |
| EðIÞZ |     | jDkPrfXððjK1ÞDkÞ%rm;rm!XðjDkÞ%mgC |     |     |     |     |     |     |                        |     |     |     |       |     |     |
Ultrasonicwallthicknessmeasurements
|     | jZ1 |     |     |     |     |     |     |     | 1986 |     |     |     | 15.6mm |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | ------ | --- | --- |
|     |     | jDk |     |     |     |     |     |     | 1990 |     |     |     | 14.6mm |     |     |
X
|     |     |     | nPrfXððjK1ÞDkÞ%rm; |     |     |     |     |     | 1994 |     |     |     | 14.2mm |     |     |
| --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | ---- | --- | --- | --- | ------ | --- | --- |
|     |     |     |                    |     |     |     |     |     | 1998 |     |     |     | 13.8mm |     |     |
nZðjK1ÞDkC1
Costsfordifferentactions
|     | XðnK1Þ%m;XðnÞOmg: |     |     |     |     |     |     | ð21Þ |               |     |     |     |         |     |     |
| --- | ----------------- | --- | --- | --- | --- | --- | --- | ---- | ------------- | --- | --- | --- | ------- | --- | --- |
|     |                   |     |     |     |     |     |     |      | Inspection(c) |     |     |     | 10,000$ |     |     |
I
|      |      |          |      |           |      |     |           |     | Preventivereplacement(c |     | )   |     | 50,000$    |     |     |
| ---- | ---- | -------- | ---- | --------- | ---- | --- | --------- | --- | ----------------------- | --- | --- | --- | ---------- | --- | --- |
| Eqs. | (20) | and (21) | have | also been | used | by  | Park [7], | van |                         |     | P   |     |            |     |     |
|      |      |          |      |           |      |     |           |     | FailureCreplacement(c   |     | )   |     | 1,000,000$ |     |     |
F
| Noortwijk   |     | et al. | [10]       | and Jia | and         | Christer | [11].  | An   |     |     |     |     |     |     |     |
| ----------- | --- | ------ | ---------- | ------- | ----------- | -------- | ------ | ---- | --- | --- | --- | --- | --- | --- | --- |
| application |     | to the | inspection | and     | maintenance |          | of the | rock |     |     |     |     |     |     |     |
whenitisprocessedbythemanufacturerofthecomponent,
| dumpingof |                    | astorm–surgebarrieris |     |             | givenby[10]. |                   |     |     |           |            |        |                 |     |     |     |
| --------- | ------------------ | --------------------- | --- | ----------- | ------------ | ----------------- | --- | --- | --------- | ---------- | ------ | --------------- | --- | --- | --- |
|           |                    |                       |     |             |              |                   |     |     | therefore | it couldbe | weaker | than indicated. |     |     |     |
|           | Theexpectedaverage |                       |     | costpertime |              | unitisafunctionof |     |     |           |            |        |                 |     |     |     |
IntheNetherlands,theinspectionofpressurizedvessels
| the | replacement | percentage |     | r, the | failure | level | m and | the |     |     |     |     |     |     |     |
| --- | ----------- | ---------- | --- | ------ | ------- | ----- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
isregulatedbytheDutchrulesforpressurevessels[20].All
| periodic   |     | inspection | interval | Dk.        | The | failure      | level | is     |          |            |     |             |      |                 |     |
| ---------- | --- | ---------- | -------- | ---------- | --- | ------------ | ----- | ------ | -------- | ---------- | --- | ----------- | ---- | --------------- | --- |
|            |     |            |          |            |     |              |       |        | types of | components | are | categorized | and, | until recently, |     |
| determined |     | by Eq.     | (4) and  | is assumed |     | to be random |       | due to |          |            |     |             |      |                 |     |
the random variables for the operating pressure P and the thereexistedafixedmandatoryinspectionintervalforeach
|          |          |     |             |     |         |       |               |     | category. | The fixed | interval | for the | hydrogen | dryer | in this |
| -------- | -------- | --- | ----------- | --- | ------- | ----- | ------------- | --- | --------- | --------- | -------- | ------- | -------- | ----- | ------- |
| material | strength |     | S. In order | to  | include | these | uncertainties |     |           |           |          |         |          |       |         |
andtheuncertaintyinthedeteriorationratemfortheprocess example is 4 years, which can be clearly observed in the
measurementdates.Nowadays,aplantengineercanextend
| X(t), | the | same technique |     | is applied |     | as in | Eq. (19). | We  |     |     |     |     |     |     |     |
| ----- | --- | -------------- | --- | ---------- | --- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
thefixedintervalbasedontheresultsofaRBIanalysis.This
| sample | a   | large number |     | N of sets | for | the three | uncertain |     |     |     |     |     |     |     |     |
| ------ | --- | ------------ | --- | --------- | --- | --------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
variables:{s(j),p(j),m(j)},forjZ1,2,.,NandaMonteCarlo is done by submitting an application to the proper
authoritiesforacceptance.Therulesrequireallcomponents
| integration |     | is performed |     | to calculate |     | C(r,m,Dk) | given | the |     |     |     |     |     |     |     |
| ----------- | --- | ------------ | --- | ------------ | --- | --------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
valuesofthesevariables.Thecorrosionratecanbesampled tohavehadatleastoneregularinspection,accordingtothe
fromtheposteriorp(mjy ,.,y fixed intervals, before this application can be made. For
|     |     |     |     | 1 n ),whichhasbeendetermined |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
inSection 4. itemswith afixedintervalof2years,thisminimumis two
|     |     |     |     |     |     |     |     |     | inspections.    | There        | will      | thus always | be at | least one     | set of |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | ------------ | --------- | ----------- | ----- | ------------- | ------ |
|     |     |     |     |     |     |     |     |     | measurementdata |              | available | for the     | model | tobe applied. |        |
|     |     |     |     |     |     |     |     |     | Using           | the Bayesian | updating  | model,      | which | is discussed  |        |
inSection4,theposteriordensitycanbecalculatedforthe
| 6.  | Case study: | inspecting |     | a pressurevessel |     |     |     |     |     |     |     |     |     |     |     |
| --- | ----------- | ---------- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
corrosionrategiventhemeasurementdatainTable1.Inthis
The gamma process decision model is illustrated with a examplesZ0.304isusedforallfourmeasurements,which
e
case study on a hydrogen dryer, which is a cylindrical correspondstoa90%probabilityoftheerrorbeingnomore
pressure vessel constructed from carbon steel. Table 1 thanG0.5mm.Thisisarelativelylargeerrortoaccountfor
summarizestheoperationalandmeasurementdata,whichis the inaccuracy of older measurements and the fact that
takenfromanundisclosedplantintheNetherlands.Thecost inspections are performed in-service and not under
numbers are fictive. The mean material strength is controlled laboratory conditions. The results are shown in
determined using the tensile (s ) and yield (s ) strengths Fig.2.Theposteriordensity,whichwouldbeobtainedifit
|     |     |     |     | T   |     |     | Y   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
with the equation: were assumed that the measurements were exact, is also
includedforcomparisonpurposes.Inthiscaseonlythelast
| SZminf1:1ðs |     | Cs  | Þ=2;s | g:  |     |     |     | (22) |                                                    |     |     |     |     |     |     |
| ----------- | --- | --- | ----- | --- | --- | --- | --- | ---- | -------------------------------------------------- | --- | --- | --- | --- | --- | --- |
|             |     | T   | Y     | T   |     |     |     |      | measurementisofimportance,asisdeterminedbyEq.(14). |     |     |     |     |     |     |
The values for these strengths can be looked up in [18] or The difference between the perfect and imperfect inspec-
[19]. The uncertainty in S comes from the fact that these tions is significant. The assumption of perfect inspections
values represent the minimum requirements for this increases the confidence in the estimated corrosion rate
particular material type and therefore the material could considerably compared to the assumption of imperfect
be stronger. On the other hand, the material loses strength inspections.Also,theexpectationfortheperfectinspection

M.J.Kallen,J.M.vanNoortwijk/ReliabilityEngineeringandSystemSafety90(2005)177–185
183
Fig.3.Expectedaveragecostsperyearforthehydrogendryer.
| Fig. 2. Posterior |     | densities | for 1 | perfect | and 4 imperfect | inspections |     |              |          |               |     |          |               |
| ----------------- | --- | --------- | ----- | ------- | --------------- | ----------- | --- | ------------ | -------- | ------------- | --- | -------- | ------------- |
|                   |     |           |       |         |                 |             |     | The expected | time for | the corrosion |     | to reach | the corrosion |
comparedtothepriordensity.
|     |     |     |     |     |     |     |     | allowance | is about 37 | years. | The vessel |     | will therefore be |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ----------- | ------ | ---------- | --- | ----------------- |
posteriordensityishighercomparedtothatoftheimperfect replaced at the inspection in 2037, when it has reached an
| inspection | posterior. |     | This is | due | to the | fact that the | last |     |     |     |     |     |     |
| ---------- | ---------- | --- | ------- | --- | ------ | ------------- | ---- | --- | --- | --- | --- | --- | --- |
ageof60years.Thisreplacementwillbedonewellbefore
measurement does not include the information of previous the expected time of critical failure at 93 years. A risk-
| inspection | measurements, |     | which | indicate |     | a slightly | slower |                 |       |     |        |     |                 |
| ---------- | ------------- | --- | ----- | -------- | --- | ---------- | ------ | --------------- | ----- | --- | ------ | --- | --------------- |
|            |               |     |       |          |     |            |        | averse decision | maker | can | decide | to  | adopt a shorter |
rate ofdeterioration. inspection interval based on the result in Fig. 3. The
Thecoefficientofvariationnforthedeteriorationprocess
|     |     |     |     |     |     |     |     | expected | annual costs | for | inspection |     | interval lengths |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------------ | --- | ---------- | --- | ---------------- |
is set to 1 in this example. The relationship between this rangingfrom16to44yearsdonotexceed$2000.Choosing
| coefficient | of  | variation | and | the | one | for the random |     |            |            |            |       | DkZ16 |            |
| ----------- | --- | --------- | --- | --- | --- | -------------- | --- | ---------- | ---------- | ---------- | ----- | ----- | ---------- |
|             |     |           |     |     |     |                |     | to perform | a periodic | inspection | every |       | years will |
deterioration rate in classical time-dependent reliability represent a more conservative policy without a significant
models, e.g. the random deterioration coefficient C in increase in the expected costs per year. This policy would
Eq. (3), is givenby [21]. result in a preventive replacement of the hydrogen dryer
Next,theexpectedaveragecostsperyeararecalculated after 48yearsof service.
usingEqs.(20)and(21).Thecorrosionrateissampledfrom
Finally,theresultinFig.3fortheexpectedaveragecosts
theposteriordensitybasedonthefourimperfectinspection per year, obtained using the prior density for the average
| measurements. |     | The operating |     | pressure | P   | and the material |     |     |     |     |     |     |     |
| ------------- | --- | ------------- | --- | -------- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
corrosionratem,showsthatthedecisionmodelisalsouseful
strengthSaresampledfromnormaldistributions.Themean
| operating | pressure | is  | given | in Table | 1   | and the standard |     |     |     |     |     |     |     |
| --------- | -------- | --- | ----- | -------- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
deviationisdeterminedbyacoefficientofvariationof0.05.
| For the  | material                   | strength, | the | mean | is determined |     | by Eq. |     |     |     |     |     |     |
| -------- | -------------------------- | --------- | --- | ---- | ------------- | --- | ------ | --- | --- | --- | --- | --- | --- |
| (22) and | the coefficientofvariation |           |     |      | is 0.20.      |     |        |     |     |     |     |     |     |
Fig.3showsthattheexpectedaveragecostsperyearwill
| be high     | when    | inspections | are        | performed |        | too often.   | The    |     |     |     |     |     |     |
| ----------- | ------- | ----------- | ---------- | --------- | ------ | ------------ | ------ | --- | --- | --- | --- | --- | --- |
| expected    | annual  | costs       | also       | rise when | the    | time between |        |     |     |     |     |     |     |
| inspections | becomes |             | too large. | The       | result | based        | on the |     |     |     |     |     |     |
posteriordensityfortheoptimalinspectionintervallengthis
| DkZ30     | years.      | Since      | the vessel | was      | taken          | into service   | in      |     |     |     |     |     |     |
| --------- | ----------- | ---------- | ---------- | -------- | -------------- | -------------- | ------- | --- | --- | --- | --- | --- | --- |
| 1977, the | component’s |            | age of     | 27 years | has            | to be deducted |         |     |     |     |     |     |     |
| from this | result.     | Therefore, |            | the next | inspection     | should         | be      |     |     |     |     |     |     |
| performed | in 3        | years      | from       | the time | of evaluation, |                | i.e. in |     |     |     |     |     |     |
2007.Ifthisinspectiondoesnotalterourassessmentofthe
| deterioration, |     | then the | following |     | inspection | should | be  |     |     |     |     |     |     |
| -------------- | --- | -------- | --------- | --- | ---------- | ------ | --- | --- | --- | --- | --- | --- | --- |
performed30yearslaterin2037.Usingthemeancorrosion
EðmÞZ0:1212
| rate     |              | from               | the           | imperfect | inspection | posterior       |     |                     |         |            |        |     |                   |
| -------- | ------------ | ------------------ | ------------- | --------- | ---------- | --------------- | --- | ------------------- | ------- | ---------- | ------ | --- | ----------------- |
| shown in | Fig.         | 2, the expectation |               | of        | the gamma  | process         | is  |                     |         |            |        |     |                   |
|          |              |                    |               |           |            |                 |     | Fig. 4. Expectation | and 90% | confidence | bounds | for | the gamma process |
| plotted  | togetherwith | the                | 90%confidence |           |            | bounds inFig.4. |     |                     |         |            |        |     |                   |
usingtheposteriorexpectationoftheaveragecorrosionratem.

M.J.Kallen,J.M.vanNoortwijk/ReliabilityEngineeringandSystemSafety90(2005)177–185
184
when little or no data is available. If no inspection the presentation of a single optimal value often leaves
measurements are available to the decision maker, the practitioners and regulators with more questions than they
priordensityisusedtocalculatetheexpectedaveragecosts started outwith.
peryear.Thisresultsinamuchmoreconservativeoptimal Thecasestudyonahydrogendryershowedencouraging
periodic inspection interval of 10 years for the example of resultsofthewholemodel.Weconcludethattheuseofthe
the hydrogen dryer. Due to the higher uncertainty, the gamma stochastic process with an adaptive Bayesian
expected costs for this policy are about $3380 per year, approach to incorporating the uncertain degradation, is a
which is more than the expected $1760 per year for the 30 viablealternativetothestructuralreliabilitymethodswhich
year policy based on the posterior density. The plant are commonly used in the process industry. Currently,
manager can therefore update his information after research is being done to compare the gamma process
each inspection. This approach is referred to as an deterioration model with the classical structural analysis
adaptive Bayesian updating model; see e.g. Mazzuchi and modelsbasedonrandomvariablesdescribingtheuncertain
Soyer [22,23]. growth in deterioration [21]. The example application has
Future development of this model will include the alsoshownthattheeffectofimperfectinspectionmeasure-
calculation of the standard deviation of the expected costs mentsontheoutcomeisconsiderable.Thepresentedmodel
per year. Interested readers are referred to van Noortwijk takes these measurement errors into account and only
[24], who presents the required equations for this purpose requiresthedecisionmakertosupplythestandarddeviation
when costs are discounted in order to account for the time ofthe measurement.
valueof money.
| 7. Conclusions |     |     |     |     |     |     |     | Acknowledgements |     |            |     |        |           |     |        |
| -------------- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ---------- | --- | ------ | --------- | --- | ------ |
|                |     |     |     |     |     |     |     | The research     | in  | this paper | was | partly | performed |     | by the |
Thereareanumberofconclusionstobedrawnfromthis
research.First,wehaveobservedthatthegammaprocessis firstauthorduringaninternshipatDetNorskeVeritasBV.
|            |            |     |         |          |     |               |     | in Rotterdam, | the | Netherlands. |     | We would | like | to  | thank |
| ---------- | ---------- | --- | ------- | -------- | --- | ------------- | --- | ------------- | --- | ------------ | --- | -------- | ---- | --- | ----- |
| a suitable | stochastic |     | process | to model |     | the uncertain |     |               |     |              |     |          |      |     |       |
reduction of wall thickness due to corrosion. In line with Chris van den Berg and his colleagues at DNV for their
supportandfortheplantdatawhichisusedintheexample.
| what is | currently | done | in the | process | industry, | we  | have |     |     |     |     |     |     |     |     |
| ------- | --------- | ---- | ------ | ------- | --------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
simplifiedtheparametersofthisprocessbyfixingtheratio
| of the standard |      | deviation | and        | the mean | ofthe   | deterioration |     |     |     |     |     |     |     |     |     |
| --------------- | ---- | --------- | ---------- | -------- | ------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rate. Together  | with | the       | assumption | of       | a fixed | prior density |     |     |     |     |     |     |     |     |     |
References
| for the average |       | corrosion     | rate,   | this results | in        | a model        | with  |                 |           |            |           |             |                 |            |     |
| --------------- | ----- | ------------- | ------- | ------------ | --------- | -------------- | ----- | --------------- | --------- | ---------- | --------- | ----------- | --------------- | ---------- | --- |
| minimum         | input | requirements. |         | This         | is a      | very desirable |       |                 |           |            |           |             |                 |            |     |
|                 |       |               |         |              |           |                |       | [1] American    | Petroleum | Institute. |           | Publication | API581:         | risk-based |     |
| feature,        | as we | are typically | dealing | with         | hundreds, |                | maybe |                 |           |            |           |             |                 |            |     |
|                 |       |               |         |              |           |                |       | inspection—base |           | resource   | document, | 1st         | ed. Washington, |            | DC: |
| even thousands, |       | ofcomponents  |         | inthe        | average   | plant.         |       |                 |           |            |           |             |                 |            |     |
AmericanPetroleumInstitute;May2000.
Next,wehavecreatedasimpleextensiontotheBayesian [2] VanNoortwijkJM,KlatterHE.Optimalinspectiondecisionsforthe
updating model, such that the model can incorporate the block mats of the Eastern-Scheldt barrier. Reliab Eng Syst Safety
resultsfrominaccuratemeasurements.Inthisstepwehave 1999;65(3):203–11.
|     |     |     |     |     |     |     |     | [3] Speijker | LJP, Van | Noortwijk | JM, | Kok M, | Cooke | RM. | Optimal |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | -------- | --------- | --- | ------ | ----- | --- | ------- |
lostsomeefficiency,aswehavetakenthepathofsimulation
maintenancedecisionsfordikes.ProbabEngInformSci2000;14(1):
| to solve | the resulting | equations. |     | However, |     | the simulation |     |     |     |     |     |     |     |     |     |
| -------- | ------------- | ---------- | --- | -------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
101–21.
approach allows greater flexibility in the choice of [4] Abdel-Hameed M. A gamma wear process. IEEE Transact Reliab
probability distributions for the variables which determine 1975;24(2):152–3.
theuncertainfailurelevel.Althoughthecalculationsforthe [5] Abdel-Hameed M. Inspection and maintenance policies of devices
subjecttodeterioration.AdvApplProbab1987;19:917–31.
| example | in this | paper | can be | performed |     | in a matter | of  |                  |     |            |     |             |     |             |     |
| ------- | ------- | ----- | ------ | --------- | --- | ----------- | --- | ---------------- | --- | ---------- | --- | ----------- | --- | ----------- | --- |
|         |         |       |        |           |     |             |     | [6] Abdel-Hameed | M.  | Correction | to: | ‘Inspection | and | maintenance |     |
minutesanapersonalcomputer,moreeffortscouldbemade
policiesofdevicessubjecttodeterioration’.AdvApplProbab1995;
| in order | to effect | a decrease | in  | computation |     | time such | that | 27:584. |     |     |     |     |     |     |     |
| -------- | --------- | ---------- | --- | ----------- | --- | --------- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- |
multipleitemscanbeassessedatonce.Theseimprovements [7] ParkKS.Optimalcontinuous-wearlimitreplacementunderperiodic
can mostly be attained in the area of dedicated computer inspections.IEEETransactReliab1988;37(1):97–102.
|                  |         |           |      |             |             |                 |     | [8] Kong   | MB, Park | KS. Optimal | replacement |              | of an | item subject | to  |
| ---------------- | ------- | --------- | ---- | ----------- | ----------- | --------------- | --- | ---------- | -------- | ----------- | ----------- | ------------ | ----- | ------------ | --- |
| code andimproved |         | numerical |      | integration | procedures. |                 |     |            |          |             |             |              |       |              |     |
|                  |         |           |      |             |             |                 |     | cumulative | damage   | under       | periodic    | inspections. |       | Microelectr  |     |
| In order         | to make | both      | cost | optimal     | and         | safe inspection |     |            |          |             |             |              |       |              |     |
Reliability1997;37(3):467–72.
| decisions, | the cost | criterion | of  | the expected |     | average | costs |                   |                |     |     |      |                      |     |     |
| ---------- | -------- | --------- | --- | ------------ | --- | ------- | ----- | ----------------- | -------------- | --- | --- | ---- | -------------------- | --- | --- |
|            |          |           |     |              |     |         |       | [9] Van Noortwijk | JM,CookeRM,Kok |     |     | M. A | Bayesianfailuremodel |     |     |
peryearhasbeenused.Notonlydoesthiscriterionfitwell basedonisotropicdeterioration.EurJOperRes1995;82(2):270–82.
withtherequirements,italsoresultsinagraphwhichiseasy [10] Van Noortwijk JM, Kok M, Cooke RM. Optimal maintenance
decisionsforthesea-bedprotectionoftheEastern-Scheldtbarrier.In:
tointerpretbytheplantengineers.Thiswillensurethatthe
|            |      |                   |     |     |         |         |      | Cooke | R, Mendel | M, Vrijling | H,  | editors. | Engineering | probabilistic |     |
| ---------- | ---- | ----------------- | --- | --- | ------- | ------- | ---- | ----- | --------- | ----------- | --- | -------- | ----------- | ------------- | --- |
| model will | have | some transparency |     | and | it will | be less | of a |       |           |             |     |          |             |               |     |
designandmaintenanceforfloodprotection.Dordrecht,Netherlands:
| black box | to  | the practitioners. |     | Experience |     | shows | that |     |     |     |     |     |     |     |     |
| --------- | --- | ------------------ | --- | ---------- | --- | ----- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
KluwerAcademicPublishers;1997.p.25–56.

M.J.Kallen,J.M.vanNoortwijk/ReliabilityEngineeringandSystemSafety90(2005)177–185
185
[11] Jia X, Christer AH. A prototype cost model of functional check [19] American Society of Mechanical Engineers. Boiler and pressure
decisons in reliability-centred maintenance. J Oper Res Soc 2002; vessel code—Section II: materials. New York, USA: American
| 53(12):1380–4. |     |     |     |     | SocietyofMechanicalEngineers(ASME);2001. |     |     |     |     |     |
| -------------- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- |
[12] DieulleL,Be´renguerC,GrallA,RoussignolM.Sequentialcondition- [20] TechnicalCommitteeonPressureVessels.Rulesforpressurevessels,
basedmaintenanceschedulingforadeterioratingsystem.EurJOper Vols1–3.TheHague,theNetherlands:SduPublishers;1997.Dutch
| Res2003;150(2):451–61. |     |     |     |     | title:Regelstoestellenonderdruk. |     |     |     |     |     |
| ---------------------- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | --- |
[13] Grall A, Dieulle L, Be´renguer C, Roussignol M. Continuous-time [21] Pandey, MD, Van Noortwijk JM. Gamma process model for time-
predictive-maintenanceschedulingforadeterioratingsystem.IEEE dependentstructuralreliabilityanalysis.In:WatanabeE,Frangopol
TransactReliab2002;51(2):141–50. DM, Utsonomiya T, editors. Bridge Maintenance, Safety, Manage-
[14] Grall A, Be´renguer C, Dieulle L. A condition-based maintenance mentandCost.ProceedingsoftheSecondInternationalConference
policyforstochasticallydeterioratingsystems.ReliabEngSystSafety
|     |     |     |     |     | on Bridge | Maintenance, |     | Safety | and Management | (IABMAS), |
| --- | --- | --- | --- | --- | --------- | ------------ | --- | ------ | -------------- | --------- |
2002;76(2):167–80.
|             |             |                    |                          |      | Kyoto,                                                       | Japan, 18–22 | October | 2004. | London: Taylor | and Francis |
| ----------- | ----------- | ------------------ | ------------------------ | ---- | ------------------------------------------------------------ | ------------ | ------- | ----- | -------------- | ----------- |
| [15] Newby  | M, Dagg R.  | Optimal inspection | policies in the presence | of   |                                                              |              |         |       |                |             |
|             |             |                    |                          |      | Group,                                                       | 2004.        |         |       |                |             |
| covariates. | Proceedings | of the European    | safety and reliability   | con- |                                                              |              |         |       |                |             |
|             |             |                    |                          |      | [22] MazzuchiTA,SoyerR.ABayesianperspectiveonsomereplacement |              |         |       |                |             |
ference—ESREL’02,Lyon,France,19–21March,20022002p.131–8.
strategies.ReliabEngSystSafety1996;51:295–303.
[16] WhitmoreGA.EstimatingdegradationbyaWienerdiffusionprocess
|     |     |     |     |     | [23] Mazzuchi | TA, | Soyer R. | Adaptive | Bayesian replacement | strat- |
| --- | --- | --- | --- | --- | ------------- | --- | -------- | -------- | -------------------- | ------ |
subjecttomeasurementerror.LifetimeDataAnal1995;1:307–19.
|     |     |     |     |     | egies. | In: Bernardo | JM, | Berger | JO, Dawid AP, | Smith AFM, |
| --- | --- | --- | --- | --- | ------ | ------------ | --- | ------ | ------------- | ---------- |
[17] RossSM.Appliedprobabilitymodelswithoptimizationapplications.
|     |     |     |     |     | editors. | Bayesian | statistics | 5. Oxford: | Oxford | University Press; |
| --- | --- | --- | --- | --- | -------- | -------- | ---------- | ---------- | ------ | ----------------- |
SanFrancisco:Holden-DayInc;1970.
|     |     |     |     |     | 1996. | p. 667–74. |     |     |     |     |
| --- | --- | --- | --- | --- | ----- | ---------- | --- | --- | --- | --- |
[18] ASTMInternational.AnnualbookofASTMstandards—Section1:
|          |                 |                    |               |      | [24] VanNoortwijkJM.Explicitformulasforthevarianceofdiscounted |     |     |     |     |     |
| -------- | --------------- | ------------------ | ------------- | ---- | -------------------------------------------------------------- | --- | --- | --- | --- | --- |
| iron and | steel products. | West Conshohocken, | Philadelphia: | ASTM |                                                                |     |     |     |     |     |
life-cyclecost.ReliabEngSystSafety2003;80(2):185–95.
International;2003.