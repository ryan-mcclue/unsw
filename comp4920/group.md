<!-- SPDX-License-Identifier: zlib-acknowledgement -->

TODO: google kardiamobile mission values

kardiamobile is currently being used in england, with users

Released as heart health monitoring device as part of NDIS through NSW Health.
Type A conditions often suffer from cardiovascular illness.
- what issues might account based on what has happened in real world?
- how to handle them?

beneficience: enforce sustainable practices in manufacturing and disposal
              (made from recyclable materials)
non-malefience: provide confidence score
                keep an eye on bias
autonomy: opt-in/opt-out of user data
          make users are aware of AI use
justice: equitable access for non-technical users

transparency umbrella

explain
interpret


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

fairness (AI accuracy (bias and model limitation), phone requirement, subscription model)
  AI accuracy:
    apple smart watch
A study published in the New England Journal of Medicine found that of the Apple Watch users who received irregular pulse notifications, only 34% were confirmed to have atrial fibrillation on subsequent ECG patch readings [3].
[3] Perez, M. V., et al. (2019). "Large-Scale Assessment of a Smartwatch to Identify Atrial Fibrillation." New England Journal of Medicine.

  phone requirement:
The Apple Watch ECG feature requires pairing with an iPhone to function fully. As of 2021, iPhone users made up only about 47% of smartphone users in the US [2], potentially excluding a significant portion of the population from accessing this health feature.
[2] Statista. (2021). "Smartphone usage in the United States - Statistics & Facts."
    
  subscription model:
    apple smart watch models 
While the ECG feature itself doesn't require a subscription, it's only available on Apple Watch Series 4 and later. The pricing model, with new models released annually, creates a de facto subscription-like system where users need to upgrade devices to access the latest health features [3].

accountability (data sharing, xAI)
  data sharing:
In 2019, Apple faced scrutiny when it was revealed that some third-party apps could access and potentially share users' health data, including ECG readings, without clear disclosure [4]. Apple subsequently tightened its policies on health data sharing.

  xAI:
[5] U.S. Food and Drug Administration. (2018). "FDA Clears First Medical Device Accessory for Apple Watch."
The Apple Watch's ECG app received FDA clearance, but it's classified as a Class II device, which means it's not intended to replace traditional methods of diagnosis or treatment [5].

The Apple Watch ECG feature provides a classification of the heart rhythm (e.g., sinus rhythm, atrial fibrillation) but doesn't offer detailed explanations of how it reached this conclusion. This "black box" approach has been criticized by some medical professionals for potentially leading to unnecessary anxiety or false reassurance [5].


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
