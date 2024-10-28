<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Readings Lecture 2 Week 4

causal explanation:
  - explains event by identifying cause that directly brought about event
    * Increasing an applicant's credit score from 650 to 700 causes a 15% increase in the probability of loan approval

non-causal:
  - based on fact
    * Applicants with higher credit scores are more likely to be approved for loans

Here is the essay question:
How might fairness, accountability, and transparency be achieved collectively by an auto-
mated decision - that is - by a decision outputted by an AI? In your answer, compare and
contrast a causal account of explanation with at least one other account of explanation.
Make explicit reference to the attached file.
Also make references to these which are referenced in the attached file.
- Solon Barocas, Andrew D Selbst, and Manish Raghavan. 2020. The hidden assumptions behind counterfactual explanations and principal reasons. In Proceedings of the 2020 conference on fairness, accountability, and transparency. 80–89. 
- Helen Beebee. 2016. Hume and the Problem of Causation. Oxford Handbooks. 
- John Brunero. 2013. Reasons as explanations. Philosophical Studies 165 (2013), 805–824. 
- Alexandra Chouldechova. 2017. Fair prediction with disparate impact: A study of bias in recidivism prediction instruments. Big data 5, 2 (2017), 153–163. 
- Julia Dressel and Hany Farid. 2018. The accuracy, fairness, and limits of predicting recidivism. Science advances 4, 1 (2018), eaao5580. 
- J Fodor, Replies In B Loewer, and G Rey. 1996. Folk Psychology from the Standpoint of Conceptual Analysis. The Philosophy of Psychology (1996), 264. 
- Carl Ginet. 2005. Reasons explanations of action: Causalist versus noncausalist accounts. (2005). 
- Carl G Hempel. 1962. Deductive-nomological vs. statistical explanation. (1962). 
- Terence Horgan and James Woodward. 2013. Folk psychology is here to stay. In Folk psychology and the philosophy of mind. Psychology Press, 144–166. 
- Stephen Kearns and Daniel Star. 2008. Reasons: Explanations or evidence? Ethics 119, 1 (2008), 31–56. 
- David K Lewis. 1986. Causation. (1986). Peter Lipton. 1990. Contrastive explanation. Royal Institute of Philosophy Supplements 27 (1990), 247–266. Ilkka Niiniluoto. 1981. Statistical explanation reconsidered. Synthese (1981), 437–472. 
- Cynthia Rudin, Caroline Wang, and Beau Coker. 2020. The age of secrecy and unfairness in recidivism prediction. Harvard Data Science Review 2, 1 (2020), 1. 
- Wesley C Salmon. 1971. Statistical explanation and statistical relevance. Vol. 69. University of Pittsburgh Pre. 
- Stephen Stich and Ian Ravenscroft. 1994. What is folk psychology? Cognition 50, 1-3 (1994), 447–468. 
- Ruixiang Tang, Yu-Neng Chuang, and Xia Hu. 2023. The science of detecting llm-generated texts. arXiv preprint arXiv:2303.07205 (2023). 
- Bas Van Fraassen. 1988. The pragmatic theory of explanation. Theories of explanation 8 (1988), 135–155. 
- Caroline Wang, Bin Han, Bhrij Patel, and Cynthia Rudin. 2023. In pursuit of interpretable, fair and accurate machine learning for criminal recidivism prediction. Journal of Quantitative Criminology 39, 2 (2023), 519–581. 

The essay word length is 2000-2500words.
My plan is to discuss causal and statistical models of explanations. 
It is this casual vs statistical account of explanation where we want to see some back-and-forth analysis/discussion. 

My current introduction is:
Automated decision making (ADM) systems powered by artificial intelligence 
are becoming increasingly prevalent in society.
Considering causal and statistical models of explanation, there are
potential pathways for achieving fairness, accountability and transparency (FAT) in ADM systems
However, due to the nuanced nature of human cognition, these systems can only 
theoretically approximate the complexity of human decision making. 
As a result, while technical approaches can make significant progress toward FAT principles, 
achieving them fully in practice requires human involvement.

https://github.com/SanDiegoMachineLearning/talks
https://www.youtube.com/watch?app=desktop&v=DJBAzvZDEgs

Paragraph 0 (explain FAT, causal and statistical)
Paragraph 1 (fairness with causal, uc berkely admission, counterfactuals)
Paragraph 2 (fairness with statistical, flight finder, simpsons paradox)
Paragraph 3 (transparency with causal, deep blue, non-machine learning AI) -> how got decision
Paragraph 4 (transparency with statistical, NHS, xAI/LIME)
Paragraph 5 (accountability with causal and statistical, loans, LEWIS, probabilistic counterfactuals) -> (i.e. assign responsibilities, want algorithmic recourse)

Conclusion:
In conclusion, by exploring causal and statistical accounts of explanation,
ADM systems powered by AI can work towards acheiving FAT.
However, computational models of human decision making will never be perfect due to the innate complexities
of human nature. As a result, to fully acheive FAT, human involvement is required.

Write paragraphs for me.


Technical Aspects - Causal Explanations
Algorithmic fairness through causal modeling
Transparency via interpretable AI techniques
Accountability through causal audit trails

Technical Aspects - Correlational Explanations
Statistical fairness measures
Black-box model explanations
Performance monitoring based on correlations

Social Aspects - Causal Explanations
Stakeholder engagement in causal model design
Training on causal reasoning for ethical decision-making
Policy interventions based on causal impact assessments

Social Aspects - Correlational Explanations
Diversity initiatives based on representation statistics
Ethics guidelines derived from observed best practices
Public reporting of system performance correlations

(Sequoiah-Grayson, N/A). 


# ACTUAL START
TODO: citation in introduction good
Automated decision making (ADM) systems powered by artificial intelligence 
are becoming increasingly prevalent in society. Considering statistical and causal models of explanation, there are potential pathways for achieving fairness, accountability and transparency (FAT) in ADM systems. However, due to the nuanced nature of human cognition, these systems can only theoretically approximate the complexity of human decision making. As a result, while technical approaches can make progress toward FAT principles, achieving them fully in practice requires human involvement.

A statistical model of explanation focuses on probabilistic relationships within data. This approach assumes that statistical patterns can reveal associations that influence decisions. On the other hand, a causal model of explanation looks at direct cause-and-effect relationships. This approach naturally aligns with the human decision making process, where an individual's beliefs and desires influence their actions. These models offer different lenses to interpret the extent to which an ADM system is achieving FAT.

In the context of a statistical model of explanation, an ADM system is fair if the proportion of positive to negative decisions are the same for all demographics. This statistical correlation can reveal biases in the system that need to be rectified to promote fairness. Consider applying an ADM system to the University of California, Berkeley admissions study (Bickel et al., 1975). Initial statistical analysis showed that 44% of male applicants were accepted compared to only 35% of females, suggesting apparent gender discrimination. However, when examining acceptance rates by individual departments, females actually had higher acceptance rates than males. This phenomenon, known as Simpson's Paradox (Malinas and Bigelow, 2016), occurs when a statistical trend appears in grouped data but reverses when the data is subdivided. The paradox arose because females more frequently applied to departments with lower overall acceptance rates, skewing the aggregate statistics. This example highlights several limitations of statistical fairness measures. Firstly, there is no clear guidance on how to address identified biases. As explored by Dressel and Farid (2018), blindly pursuing statistical fairness can lead to unintended consequences and even exacerbate existing inequalities. Secondly, there is no programmatic way to cluster the data that reveals all possible biases. Thirdly, violations of demographic parity may not necessarily indicate unfairness given the context of the problem. This is explored by Wang et al. (2023), where differing base rates of recidivism leading to statistically unequal outcomes aren't necessarily discriminatory. Therefore, in line with Sequoiah-Grayson's (2022) arguments, while statistical approaches can work towards achieving fairness in an ADM system, they are not sufficient on their own. Human judgement is required to properly interpret the inherent complexities of fairness.
TODO: have to make explicit reference to Grayson (i.e. direct quotes)



A causal model of explanation considers fairness to be if a decision 
applies equally across different demographics.
Beyond just identifying a correlation as a statistical model enables, 
causality provides a means to articulate the reasons for these relationships.
By understanding the causal mechanisms at play, targeted interventions can be developed to 
promote fairness.
A causal query can be encoded as a counterfactual, i.e. a hypothetical.
In the context of the UNSW admissions example, 
counterfactuals would be of the form 
"what would the admission rate be if all people were male" (and likewise all female).
If these are different, have shown that manipulating gender affects decision 
and therefore established discrimination casually.
However, don't have control over causal relationships, like gender influences hobbies which influences if admitted or not,
i.e. doesn't take into account proxy variables.
There is no magic formula to say what variables along this chain are permissible causal influences, e.g. ok if department affects, but not hobbies
These choices are determined by cultural, social and ethical considerations. 
So, need human to be able to justify these variables as admissable. 
---
Causal models offer a more nuanced and actionable approach to achieving fairness in ADM systems.


Utilising a statistical model of explanation, transparency is the ability to understand which input features
most influenced the decision that was made.
Modern explainable AI techniques like LIME (Local Interpretable Model-agnostic Explanations) achieve this by approximating complex models with simpler, interpretable ones in the local region around a specific decision. 
Rather than providing a complete decision trace, these methods offer simplified explanations of what features were most important for a particular output. 
For instance, in an image classification task, LIME might highlight which regions of an image most strongly influenced the model's decision. 
This approach acknowledges that while the full computational process may be too complex to fully comprehend, we can still gain meaningful insights into what the system considers important for its decisions

Posthoc Model agnostic xAI, make no assumptions about internal of model, just input and output.
Quantify input of features, e.g. name, age, credit history and rank based on importance.
SHAP is popular method assess importance of an input feature.
LIME (decision trees etc.) on the other hand approximates non-linear models based off some locality/data-point you want to explain
using a surrogate function, i.e. a linear model. Then rank features based on outputs.
All these are wrong as only focus on input and output of algorithm.
Humans explain phenomena constrastively, e.g. why this and not that.
---


Considering a causal model of explanation, an ADM system is transparent if it's possible to trace the logical steps that were
made in order to reach a decision.
Non-machine learning AI systems like IBM's Deep Blue exemplify this approach, 
where each move is determined by explicit rules and game-tree search algorithms. 
The system's decisions can be audited by examining the specific rules triggered, positions evaluated, 
and paths explored in the game tree. 
This deterministic nature means that given the same input state, the system will always produce identical outputs 
through the same logical pathway. 
Such transparency enables complete verification of the system's reasoning process, 
as each decision point can be mapped to specific programmed rules and evaluation criteria.
---

A universal view of accountability is if an ADM system can assign responsibility to a decision.
Specifically, this means the system makes it clear as to what actions can be taken
to change the decision that was made.
Combining both causal and statistical methods, probabilistic counterfactuals offer a powerful framework for accountability.
These models analyze not just what would change if a single factor were different, but also quantify the likelihood of different outcomes under various scenarios. For instance, in a loan approval system, rather than simply stating that income was too low, the system can specify that increasing income by $10,000 would raise approval probability by 40%, while improving credit score by 50 points would raise it by 60%. This probabilistic approach acknowledges the inherent uncertainty in real-world decisions while still providing actionable insights for accountability. By merging causal reasoning about "what-if" scenarios with statistical measures of uncertainty, the system can provide more nuanced and practical guidance for appealing or improving future outcomes.
This analysis identifies both sufficient and necessary conditions for changing the decision - whether changing an attribute like income would be enough to alter the outcome, and whether it is required for approval.
However, while algorithms can compute these probabilistic relationships, only human judgment can determine what constitutes truly sufficient causation in complex real-world scenarios.
The system can suggest that a $10,000 income increase would likely lead to approval, but a human must evaluate if this represents a reasonable and achievable path forward for the applicant.
Probabilistic counterfactual, e.g. for individual with ..., for whom algorithm made decision ..., 
the decision would have been ... with probability ..., had the attribute been ...
So, to what extent would changing name, be sufficent in changing outcome of algorithm.
Also want to know if attribute is necessary.
Only human knows what sufficent causation is.
---

In conclusion, by exploring causal and statistical accounts of explanation,
ADM systems powered by AI can work towards acheiving FAT.
However, computational models of human decision making will never be perfect due to the innate complexities
of human nature. As a result, to fully acheive FAT, human involvement is required.
# ACTUAL END





What to extract data and turn it into actionable insight to make decisions to improve areas in life.


TODO: Use this flow as first paragraph
Data flow pipeline involves 
  1. raw data (algorithmic fairness) 
  2. preprocessing (responsible data management; clean data?)
  3. analysis (user asks queries are inherently bias; i.e. asks false queries get false answers?)
  4. decision (explanations)

Things can go wrong in pipeline, resulting in discriminatory decision.
Issues with raw data contributing to fairness.


causal inference from complex relational data can form foundation for 
    F: algorithmic fairness, 
    A: responsible data management, avoiding false conclusions, 
    T: generating explanation

(TODO: use tutorial slides for definitions)

F1 (statistical, airline selection, simpsons paradox)
Fairness includes the correctness of a decision and the equitable treatment across different demographics.

Whilst algorithms are in some way objective creatures, and don't possess capability to be racist or sexist.
The input data to the pipeline is being collected from societies that are polluted with layers of institutionalised racism, discrimanation etc.
Therefore, algorithms will pick up these discriminations and result in discriminatory outputs.
e.g. Amazon AI recruiting tool showing bias against women (due to bias in training data)

Choose best airline; so look at that with least delays. 
Results differ if only looking at one airport, as oppose to many.
Also, say one airline disproportionately flies at an airport with many weather events, so it's results are affected by this.
So, results not because of performance, just has to do with location.
So, cannot rely on SQL queries etc. as they may lead to false conclusions.


F2 (causal, UC Berkely, counterfactuals) 
Fairness in a statistical context, is when 'positive' outputs have same porportion for protected and priveleged groups.
i.e. statistical correlation. 
This is inconsistent (unable to satisfy all the time) 
and counterintuitive (cannot capture the social idea behind fairness)
e.g. UC Berkely violated statistical parity of men and women acceptance rates, 
i.e. there was a correlation to gender and admittance (want them to be independent)
Big disparity against women.
however if look other graph of department, shows disparity against men.
Simpson's paradox.
Shows impossible to capture the intuition behind fairness using a statistical model.
Furthermore, even if demographic parity is violated, this does not indicate unfair, just might be nature.
Only discriminatory, if direct link can be shown.


Once found out about correlation, must ask why is there this correlation (statisical cannot).
Causal can answer why are gender and admittance correlated.
Causal encodes significant variables, e.g. gender, admittance
and encodes edge if related, i.e. have causal relationship.
So, must assume gender is connected to choice of department. 
However, due to human nature, there are way more factors affecting this.

Fairness is fundamentally causal.
Causality allows to answer what would be outcome if change some variable, i.e. answer a hypothetical/counterfactual.
(causal queries are counterfactuals)
e.g. what would be admission rates if all people were female?
e.g. what would be admission rates if all people were male?
if these are different, can establish discrimination causally.
however, we don't have all this data, so causual inference is a missing data problem.
can only emulate data with randomised experiment, yet still an estimate, so carries assumptions.


Berkely admission algorithm.
Focus on pre-existing/historical bias; many other biases like process for training label selection, selection, measurement bias etc. (link to lecture slides)
Want to remove these upstream biases with a sort of data cleaning process to remove discrimination signal from it.
For causal fairness, don't want gender (sensitive attribute) to influence admission.
Expressed as counterfactual, manipulating gender does not change algorithm outcome.
However, don't have control over causal relationships, like gender influences hobbies which influences if admitted or not,
i.e. doesn't take into account proxy variables.
There is no magic formula to say what variables along this chain are permissible causal influences, e.g. ok if department affects, but not hobbies
These choices are determined by cultural, social and ethical considerations. 
So, need human to be able to justify these variables as admissable. 

(ACCOUNTABILITY)


A1


A2


Assumes homogenous data, i.e. can't be both student and teacher



TODO: flora lecture slides from week 7 for XAI
T1
AI increasingly being used to make consequential decisions.
Models high accuracy results in high complexity and opacity.
Often not intuitive, hard to interpret.
To be adopted, ADM must build trust in stakeholders.
Decisions need to be justifiable and provide actionable recourse.
Developers want to perform root cause analysis, users want to do why this outcome, business address discriminatory outputs etc.
Consider bank loan system that considers credibility of customers to pay off debts.
Want to provide reason for decision and set of recommended actions so they can change result for future.

Indeed compliance is legislated, european union (gdpr.eu) states that "right to not be subject to decision based solely on automated processing"

Posthoc Model agnostic xAI, make no assumptions about internal of model, just input and output.
Quantify input of features, e.g. name, age, credit history and rank based on importance.
SHAP is popular method assess importance of an input feature.
LIME (decision trees etc.) on the other hand approximates non-linear models based off some locality/data-point you want to explain
using a surrogate function, i.e. a linear model. Then rank features based on outputs.

Counterfactual explanations will somehow perturb input, e.g. name, so that the outcome of perturbed input changes.
i.e. perform some minimal change to name to see how changes

All these are wrong as only focus on input and output of algorithm.

Humans explain phenomena constrastively, e.g. why this and not that.
e.g. why got rejected and not accepted.

Probabilistic counterfactual, e.g. for individual with ..., for whom algorithm made decision ..., 
the decision would have been ... with probability ..., had the attribute been ...
So, to what extent would changing name, be sufficent in changing outcome of algorithm.
Also want to know if attribute is necessary.

Only human knows what sufficent causation is.







(transparency is broken into explainability (understood by non-technical) and interpretability (computer science understanding))
interpetability: saliency maps (heatmaps; no actionable insights to guide decision making), statisical regression, etc.

overcome cognitive biases (AI is looking at patterns that humans can't comphrehend)
TODO: discuss limitations in current XAI
T2

Echoes Principlism's aspirations for benefience and justice.
Fairness
Incremental ethical specification.

our normative goals sit on sliding scale between what is acheivebale and what is aspirational.
(have a human can enhance reflective equilibrium)

But must contextualise them for real-world use.
Benefit of abstraction allows for broad agreement.






ADM systems are attempting to emulate human decision making and humans are fundamentally inexact while with enough computing resources is theoretically possible

demonstrate that fully achieving FAT in ADM systems may only be realizable in principle, as effective implementation will likely always require some degree of human intervention. 
However, significant practical challenges remain and is something only realisable in principle as will always require human intervention.

(e.g. utilitarian cumbersome method incapable of expressing in code).

Looking at causal and statistical models of explanation, can see that acheiving FAT in ADM system requires a multifaceted approach. 

Want to say causal, statistical models help acheive it, only realisable in principle not in reality.



Achieving FAT in ADM systems requires a multifaceted approach. 
By combining causal and social explanations, we can create more robust, fair, and accountable systems. 

Causal explanations provide the technical rigor necessary for understanding and improving algorithms, 
while social explanations ensure that human judgment, ethics, and societal values remain central to the decision-making process. 
As ADM systems continue to evolve, integrating these complementary approaches will be essential for building trust and ensuring responsible AI deployment.

Where you take that discussion is up to you, but certainly you can think about both whether it is currently possible, currently not possible, 
possible in principle or unrealisable in principle.

1. Technical Causal 
   Using algorithms like minimax over black-box neural networks
   F: allows for causal modelling/intervention which can give adjusted predictions?
   A: explainable AI
   T: audit trail can step through source code
2. Technical - Statistical 
   F: statistical fairness can mask underlying biases as correlation not imply causation, e.g. poverty to crime
   A: Correlational approaches often employ complex, opaque models like neural networks, making it difficult to understand the reasoning behind individual predictions. While post-hoc explanations for black-box models exist, they often rely on simplified approximations of the model's behavior and lack the transparency of causally interpretable models.
   T: If the underlying data or societal factors contributing to these correlations are biased, even a well-performing model can perpetuate unfair outcomes
3. Social - Causal
   F: Having the ability to explainthe causal pathways behind decisions, stakeholders (e.g. formerly incarcerated individuals) can engage in informed discussions about the ethical implications of the system and advocate for changes to promote fairness.
   A: Educating developers, policymakers, and users on causal reasoning and its implications for ethical decision
   T: if a causal analysis reveals that lack of access to employment opportunities causally increases re-offending rates, this can inform policy interventions focused on providing job training and employment support to formerly incarcerated individuals
4. Social - Correlational


The increasing reliance on automated decision making (ADM) systems, particularly those powered by artificial intelligence (AI), raises critical questions about fairness, accountability, and transparency (FAT). Achieving FAT in ADM systems is not merely a technical challenge but a deeply social and ethical one. A central question revolves around how to explain the decisions made by these often complex and opaque systems. This essay argues that causal explanations offer a more robust framework for achieving FAT in ADM systems compared to correlational explanations, exploring both technical and social aspects through the lens of recidivism prediction tools.

Technical Aspects: Causal Explanations for Actionable Insight

Causal explanations, rooted in the counterfactual model of causation (Lewis, 1986), aim to identify the specific factors that directly lead to a particular outcome. This approach goes beyond merely observing statistical associations and seeks to uncover the underlying mechanisms driving decisions. In ADM systems like COMPAS, which predicts recidivism risk, a causal approach would strive to pinpoint the features or factors that causally contribute to an individual's predicted risk score. This focus on causality unlocks several pathways towards achieving FAT:

Technical Aspects: The Limitations of Correlational Explanations

In contrast, correlational explanations merely identify statistical associations between variables without establishing causal relationships. This reliance on correlation can lead to several limitations in achieving FAT:

    Statistical fairness measures: Focusing solely on achieving statistical fairness (e.g., ensuring similar recidivism prediction rates across racial groups) can mask underlying biases and perpetuate unfair outcomes (Barocas et al., 2020). This is because correlation does not imply causation; a model trained on biased data might learn to associate poverty with recidivism, even if poverty is merely correlated with, but not causally related to, re-offending.

    Black-box model explanations: Correlational approaches often employ complex, opaque models like neural networks, making it difficult to understand the reasoning behind individual predictions. While post-hoc explanations for black-box models exist, they often rely on simplified approximations of the model's behavior and lack the transparency of causally interpretable models.

    Performance monitoring based on correlations: Monitoring system performance based solely on correlations (e.g., tracking recidivism rates by demographic group) can be misleading. If the underlying data or societal factors contributing to these correlations are biased, even a well-performing model can perpetuate unfair outcomes. This highlights the need for causal analysis to understand the factors driving system performance and identify potential sources of bias.

Social Aspects: The Importance of Causal Reasoning in Participatory Design

Beyond technical considerations, achieving FAT in ADM requires engaging with the social context of decision-making. Causal explanations play a crucial role in facilitating meaningful stakeholder engagement and informing policy interventions:

    Stakeholder engagement in causal model design: Involving diverse stakeholders, including those most impacted by the system (e.g., formerly incarcerated individuals), in the design and evaluation of recidivism prediction tools can help uncover hidden biases and identify relevant social factors that might be overlooked by solely technical approaches (Friedman & Nissenbaum, 1996). By explaining the causal pathways behind decisions, stakeholders can engage in informed discussions about the ethical implications of the system and advocate for changes to promote fairness.

    Training on causal reasoning for ethical decision-making: Educating developers, policymakers, and users on causal reasoning and its implications for ethical decision-making is crucial. This includes understanding the limitations of correlational thinking and recognizing the importance of considering the causal impacts of decisions on different communities.

    Policy interventions based on causal impact assessments: Causal impact assessments, which go beyond merely observing correlations to estimate the causal effect of interventions, can inform policy decisions aimed at addressing the root causes of recidivism. For example, if a causal analysis reveals that lack of access to employment opportunities causally increases re-offending rates, this can inform policy interventions focused on providing job training and employment support to formerly incarcerated individuals.

Social Aspects: Correlational Explanations and the Risk of Superficial Solutions

Relying on correlational explanations in the social realm can lead to superficial solutions that fail to address systemic issues and hinder meaningful social change:

    Diversity initiatives based on representation statistics: While increasing diversity in the development teams building ADM systems is important, focusing solely on representation statistics without addressing the underlying biases in the data, algorithms, and development processes can result in symbolic change without substantive progress towards fairness.

    Ethics guidelines derived from observed best practices: Developing ethics guidelines based on observed best practices, without a thorough causal analysis of the ethical implications of ADM systems, can lead to a narrow focus on avoiding past mistakes rather than proactively anticipating and mitigating potential harms. This reactive approach risks overlooking novel ethical challenges posed by the rapidly evolving capabilities of AI systems.

    Public reporting of system performance correlations: While transparency in reporting system performance is essential, focusing solely on correlations (e.g., reporting recidivism rates by demographic group) can be misleading. This is because correlations can be influenced by numerous factors, including societal biases and historical injustices. This highlights the need for reporting that includes causal analysis to provide a more nuanced and accurate understanding of system performance and its implications for fairness.

Conclusion: Towards a Causally Informed Approach to FAT in ADM

Achieving FAT in ADM requires moving beyond opaque statistical associations and embracing a causally informed approach that prioritizes transparency, accountability, and social justice. This involves employing techniques that reveal the causal pathways within ADM systems, engaging in meaningful dialogue with stakeholders, and informing policy decisions based on causal impact assessments. By prioritizing causal explanations, we can move towards a future where these systems are not simply tools of prediction but instruments for positive social change.




## Technical 
Diverse and representative data:
Ensure training data is diverse and representative of all groups the system will affect.
Regularly update and refine the dataset to reflect changing demographics or conditions.

Explainable AI (XAI) techniques:
Use interpretable machine learning models like decision trees, linear regression, or rule-based systems instead of complex neural networks when possible.


## Social (human involvement)
Appeals process:
Implement a clear and accessible process for individuals to appeal decisions made by the system.
Ensure human oversight in the appeals process.

System-Logging/Transparency reports:
Regularly publish transparency reports detailing system performance, impact assessments, and improvement efforts.

Counterfactual explanations:
Provide explanations that show how input changes would affect the decision, helping users understand what factors influence outcomes.


## References from reading
[lipton1990contrastive] - https://www.cambridge.org/core/services/aop-cambridge-core/content/view/EB3C55BBB37E6D0B2A88705EBD1F3BA5/S1358246100005130a.pdf/contrastive-explanation.pdf

[lewis1986causation] - https://academic-oup-com.wwwproxy1.library.unsw.edu.au/book/44820/chapter/383578449

[hempel1962deductive] - https://conservancy.umn.edu/items/b8ce3527-af35-44a0-be95-013a66d7af79

[stich1994folk] - https://www-sciencedirect-com.wwwproxy1.library.unsw.edu.au/science/article/pii/001002779490040X

[fodor1996folk] - can't find

[horgan2013folk] - can't find

[barocas2020hidden] - https://dl.acm.org/doi/abs/10.1145/3351095.3372830

[wang2023pursuit] - can't find

[chouldechova2017fair] - https://arxiv.org/abs/1703.00056

[brunero2013reasons] - https://link.springer.com/article/10.1007/s11098-012-9982-8
