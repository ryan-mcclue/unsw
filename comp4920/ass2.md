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
Make explicit reference to the 'assigned-reading.pdf' I have attached.
Also make references to these which are referenced in 'assigned-reading.pdf':
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
Also draw information from 'additional-reading.pdf' and 'additional-reading1.pdf' I have attached.

Note that the question wants you to discuss achieving FAT (fairness, accountability, transparency) in the context of an automated decision (specifically AI).
The next part of the question is asking for you to discuss the above focus from a casual explanation perspective and then compare and contrast this lens with 
least one other account of explanation (i.e. non-causal account of explanation). 
It is this casual vs other account of explanation where we want to see some back-and-forth analysis/discussion. 

The essay word length is 2000-2500words.
My plan is to discuss causal and correlational explanations. 
Specifically, that causal is more robust framework for achieving FAT in ADM systems compared to correlational explanations.
I will discuss technical and social aspects.
I will have 4 paragraphs:
  1. Technical Aspects - Causal Explanations (e.g. using algorithms like minimax over black-box neural networks)
  2. Technical Aspects - Correlational Explanations (e.g. model makes decisions on statistical fairness measures)
  3. Social Aspects - Causal Explanations (e.g. stakeholder engagement) 
  4. Social Aspects - Correlational Explanations (e.g. diversity initiatives)
I want to link these to a specific ADM system.
Write this essay and offer additional insight as to how to modify plan.


Define FAT in the context of AI-powered ADM systems
Introduce the concept of causal and correlational explanations
Thesis statement: Causal explanations provide a more robust framework for achieving FAT in ADM systems compared to correlational explanations, 
both in technical and social aspects

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


# ACTUAL START
This is introduction of essay. Want to have a paragraph each of causal and statistical for FAT.
Thesis is causal and statisical can get some way there, but as modelling human decision, an actual human is required.
So, I feel have to not mention human intervention in paragraphs.
Currently, can only think of explainable AI through non-machine learning AI, e.g. minimax for deep blue chess as a way to acheive FAT without human intervention.
Please give more examples for the paragraphs using causal and statiscal explanation for each.
What category would my deep blue example fit into?

TODO: citation in introduction good
Automated decision making (ADM) systems powered by artificial intelligence 
are becoming increasingly prevalent in society (1).
Considering causal and statistical models of explanation, there are
potential pathways for achieving fairness, accountability and transparency (FAT) in ADM systems
However, due to the nuanced nature of human cognition, these systems can only 
theoretically approximate the complexity of human decision making[6]. 
As a result, while technical approaches can make significant progress toward FAT principles, 
achieving them fully in practice requires human involvement.

Define FAT and causal and statistical.
(TODO: use tutorial slides)

F1

F2

A1

A2

TODO: flora lecture slides from week 7 for XAI
T1
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

In conclusion, by exploring causal and statistical accounts of explanation,
ADM systems powered by AI can work towards acheiving FAT.
However, computational models of human decision making will never be perfect due to the innate complexities
of human nature. As a result, to fully acheive FAT, human involvement is required.
# ACTUAL END





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
