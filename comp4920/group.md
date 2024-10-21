<!-- SPDX-License-Identifier: zlib-acknowledgement -->

## Value sensitive design
Consider human values throughout design process
1. Stakeholder identification 
2. Stakeholder values:
   - Conceptual investigation
     judgement call is this, so it lays out the 'human values' we are considering

   critical analysis of different technologies:
   - Empirical investigation
   User Acceptance: A study by Lowres et al. (2019) found high user acceptance of the KardiaMobile device among older adults for AF screening, with 98% finding it easy to use[1].
   Diagnostic Accuracy: Selder et al. (2019) reported that KardiaMobile showed high accuracy in detecting AF, with a sensitivity of 96.6% and specificity of 94.1%[2].
   Cost-Effectiveness: A study by Proietti et al. (2016) suggested that using KardiaMobile for AF screening could be cost-effective in certain populations[3].
   Patient Anxiety: Some studies have noted increased anxiety in some patients due to frequent self-monitoring, highlighting the need for proper education and support[4].
   - Technical investigation
   FDA-Cleared Algorithm: The AI algorithm for detecting atrial fibrillation has been cleared by the FDA, indicating a certain level of reliability and safety.
   Encryption: Data is encrypted during transmission and storage, supporting privacy and security.
   Cloud Storage: ECG recordings are stored in the cloud, allowing easy access for users and healthcare providers but raising potential security concerns.
   Integration: The system integrates with electronic health record systems, supporting comprehensive patient care but potentially raising privacy concerns.
   Algorithm Transparency: More research is needed on how the AI algorithm makes its decisions and how this is communicated to users and healthcare providers.
   Data Retention Policies: Investigation into how long data is stored and who has access to it over time.


The accuracy of the underlying AI system is crucial to successfully detect heart abnormalities.
To acheive AI accuracy, KardiaMobile:
  - Incorporates machine learning algorithms trained on large datasets of ECG readings [4].
  - Continuous refinement of algorithms based on new data and user feedback [5].
  - Integration of multiple data points (e.g., KardiaMobile's six-lead ECG provides more comprehensive data than single-lead devices) [6].
Fairness:
  High accuracy promotes equal access to reliable heart monitoring for general users.
  However, if the AI performs differently across demographic groups due to training data biases, it could lead to health disparities [7].
  For insurance companies high accuracy might result in discrimination if used to determine insurance premiums.
Transparency:
  The "black box" nature of AI algorithms may make it difficult for general users to understand how diagnoses are made.
  Similary, may make it challenging for healthcare providers to explain results to patients.
Responsibility: 
  General users might over-rely on AI interpretations, potentially delaying seeking professional medical care.
  Healthcare providers might become overly reliant on AI interpretations.
  --> apple smart watch 
  The Apple Watch uses a single-lead ECG and has similarly shown high accuracy in detecting AF, with a 97.5% sensitivity and 99.3% specificity in one study [14]. 
  However, its accuracy has been questioned for other heart rhythm disorders, highlighting the need for transparency about the device's limitations [15].
Ethical Risks:
  The push for more accuracy, requires more data, which might lead to privacy concerns as more detailed health data is collected and analysed.

KardiaMobile uses a subscription model to provide a steady revunue stream and to support ongoing costs of data storage to ensure business is profitable.
KardiaMobile 6L's subscription model typically includes:
  A basic free tier with limited ECG readings and AI interpretations.
  Premium tiers offering unlimited ECG storage, detailed reports, and additional AI-detected conditions 
Fairness:
  Creates a two-tiered system where comprehensive health insights are only available to those who can afford the subscription.
  Patients with premium subscriptions might receive more detailed insights, potentially leading to disparities in care
Responsibility: 
  The division between free and paid features may not be clear to all general users.
  The subscription model might prioritise profitable features over those with the greatest public health impact.
  Could exacerbate existing health disparities as advanced features may be inaccessible to lower-income populations.
  --> apple smart watch
  No subscription model, All health features available so fairness.
  However, high upfront cost may exclude may users.
  Initial (more flexible to users with changing fiancial situations) vs Upfront costs (reduce stress of ongoing purchases).



Issue 1 - Accuracy:
AI accuracy:
  - why is AI accuracy needed?
  - how is AI accuracy attained?
  - what affects does attaining this AI accuracy have on fairness, transparency, explainability, and/or responsibility issues, ethical and/or discrimination risks with relation to direct users, healthcare providers and stakeholders?
  - provide examples from apple smart watch

Issue 2 - Profitability:
Subscription Model:
  - why is subscription model used?
  - how is subscription model implemented?
  - what affects does this subscription model have on fairness, transparency, explainability, and/or responsibility issues, ethical and/or discrimination risks with relation to direct users, healthcare providers and stakeholders?
  - provide examples from apple smart watch


  high accuracy:
    KardiaMobile 6L has demonstrated high accuracy in detecting atrial fibrillation (AF), 
    with studies showing sensitivity of 96.6% and specificity of 94.1% [1].
    High accuracy promotes trust and reliability for general users.


  direct users, healthcare providers, stakeholders

  critical analysis on ethical impacts on users/stakeholders (with references)
    general-user-group1-kardia: the kardia has high accuaracy. this promotes ... for general user.
    general-user-group1-apple: this is also the case for general users of apple, who say they wanted ... for ... 



IMPORTANT:
technology: AI ECG
application: use in smarthome

TODO: self-administiring for reducing infection using 12Lead

desktop word: tab references

issues:
fairness, transparency, explainability, and/or responsibility issues, ethical and/or discrimination risks
  - Accuracy (false-positives): 
**AI:**
The use of AI, particularly neural networks, introduces complexities in terms of explainability and potential biases.

explainability:
The "black box" nature of neural networks makes it difficult to explain how decisions are made, 
potentially eroding trust in the technology.

responsibility:
Trust issues: Frequent false-positives might lead to users ignoring genuine warnings, potentially missing real cardiac events. 
Patient anxiety: False-positives can cause unnecessary stress and worry for users.
Healthcare system burden: Increased visits to healthcare providers for false alarms can strain medical resources.

  - Profitibility:
**Subscription:**
It creates a two-tiered system where access to potentially life-saving information is determined by a user's ability to pay.
User trust: Lack of transparency about what data is withheld might erode user confidence.
Health inequity: Those who can't afford subscriptions may receive inferior health monitoring.
Data ownership issues: Raises questions about who owns the health data generated by users.






Indeed automated decision making in health sciences poses many more risks

cost of training excludes others from doing so
access to training data excludes others

HEALTHCARE:

IMPORTANT: in effect AI predictors; try to catch things missed by traditional healthcare process
1. detecting heart arrhythmiams (AliveCor KardiaMobile analyser)
2. monitor patient vitals to detect sepsis (hcahealthcare sepsis prediction)
3. siezure detection (embrace2 bracelet)
4. skin checking (apps)
5. stroke detection (lov app)
6. breast cancer detection

Perhaps best to combine deep learning predictions with clinicians diagnosis improve patient outcome

- AI-powered diagnosis

Natural Language Processing for electronic health records
- AI-assisted robotic surgery
Predictive analytics for patient outcomes
- AI-driven drug discovery
- Virtual nursing assistants
AI for personalized treatment plans


AI technology:
  Description:
    - PURPOSE:
     * Overarching Purpose
     * Goals
     record electrical signals in the heart (electrocardiogram ECG)
     accuracy: the analysis of an ecg is an inexact science, with personal interpretations
     comprehensive: analyse more up to 6 types of arryhtmias
     adaptability: trends in data and identify potential trigger points 
     quickness: cardiologist can get data more quickly through app
     simplicity: no messy gels or sticky wires
    - Goals
     reduce heart disease
     healthcare more accesible

    - Scope (context, time, location, use case), 
     person with previous heart condition or family history etc.
     24hour usage
     person at home 

     person experiencing heart palpatations and wants to verify  



    - Needs (motivation, reasons for creation), 
    - Benefits (health/economic/societal)

  Users:
    - attributes (age group, gender etc.)
    - needs (when iteracting with tech.)
    - skills

  Stakeholders (somone who is positively/negatively impacted by tech):
    - attributes (age group, gender etc.)
    - needs (when iteracting with tech.)
    - skills

1.
Of 3 users/stakeholders, discuss tech impact on their ethical principles/concerns:
ethical principles of fairness, privacy and security, reliability and safety, trans-
parency, inclusion, and accountability
learn about existing efforts to mitigate these issues.
TODO: backup stakeholder discussion with research?
TODO: discuss frictions across different stakeholders
TODO: summarise findings in chart? 
(radar chart for overlap and grouped bar chart for the degree to which affect them)

2.
Of a similar technology, discuss impact on two previously discussed ethical issues.
TODO: use table/chart again
(stacked bar chart to show how much ethical principles of each compare)

TODO: describe what possible impacts this tech might have based on previous tech
discuss possible mitigation techniques backed by data

5.
Compare/summarise findings of 1. with that of 2.
what do they agree on? etc.

6.
Provide recommendation to adopt technology and possible changes to it.
