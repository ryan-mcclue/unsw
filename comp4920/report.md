<!-- SPDX-License-Identifier: zlib-acknowledgement -->

Take feedback from presentation into report
# AI Heart Monitoring - KardiaMobile 6L

## Introduction
Introduction and background of tech: A clear focus, and a comprehensive explanation of the
AI/ADM technology. States the case study, and provides a clear context for the investigation
and the broad stakeholders and users.

KardiaMobile 6L is a personal ECG/EKG (Electrocardiogram) device that leverages AI.
An ECG is a test that measures the electrical pulses that trigger a heartbeat.
The 6 leads in the KardiaMobile refers to 6 pulses, e.g from arm-to-arm, arm-to-leg etc.
TODO: clarify trad. ecg vs kardia
In a traditional ECG, the lead count corresponds to the number of contact points.
However, in KardiaMobile the number of contact points is half the lead count.

In its current state, the purpose of the KardiaMobile 6L is to 
facilitate the early detection of heart rhythm abnormalities to reduce the negative
impact of heart disease in the community (AliveCor, n.d).
Our proposed adoption of KardiaMobile would see this purpose amended to 
provide accessible and accurate heart monitoring for NDIS (National Disability
Insurance Scheme) clients situated in NSW, Australia. The goal of this would be 
to promote heart health for high needs individuals.
The NDIS is an Australian Government initiative that provides funding to people with
a disability to improve their quality of life (NDIS, 2024).

The objectives of the KardiaMobile 6L are:
  - Comprehensive: Capture a more detailed view compared to traditional ECG wearables.
  - Accurate: Perform AI ECG analysis to detect up to 6 types of arrhythmias.
  - Adaptable: Perform AI trend analysis to identify trigger points specific to an individual's heart rhythm changes.
  - Accessible: Easy to use and interpret by a non-technical user.

In its current deployment, the time frame of KardiaMobile is 
to provide a detailed ECG analysis in a 30 second window. In addition,
previous ECG reports can be saved for cumulative analysis to support routine monitoring.
Our suggested use of KardiaMobile has time frames in line with 
regular reporting periods matching individual NDIS health plans.
In addition, this would include scheduled monitoring aligned with NDIS carer visits.

Currently, KardiaMobile is primarily used in North America and Western Europe 
in a relaxed home setting. However, the portable design allows for use in other locations
such as a hospital or health clinic. This also gives the potential for 
integration in telemedicine and remote patient monitoring programs.
In our proposed plan, KardiaMobile would be used in NSW, Australia.
This would include NDIS approved accommodation settings such as a
communal living arrangements or NDIS day programs with support workers.


TODO: be more clear that smartphones are required
KardiaMobile requires a smartphone to record and view its data.

Currently, KardiaMobile is mainly used to perform regular heart monitoring at home
for individuals with known heart conditions.  In addition, it also enables
the sharing of ECG data with healthcare providers to allow for more informed
decision making. In our use case, KardiaMobile would provide an easy-to-use heart
monitoring system for NDIS participants. Furthermore, it would 
integrate ECG sharing between NDIS support teams and healthcare providers.

The primary motivation for our proposed adoption of KardiaMobile is 
to tackle cardiovascular disease.  In 2023, this was the leading cause
of death in Australia (). 
https://www.abs.gov.au/statistics/health/causes-death/causes-death-australia/2022

People with disability have cardiovascular disease more often and earlier than the general
population (). 
https://www.ndiscommission.gov.au/sites/default/files/2022-06/Practice%20Alert%20-%20Cardiovascular%20disease%20in%20people%20who%20have%20a%20disability.pdf

The main benefits of rolling out the KardiaMobile for NDIS participants are:
Early detection of atrial fibrillation (AF), the most common type of heart arrhythmia, which can lower quality of life and increase the risk of stroke or heart failure. The KardiaMobile provides a non-invasive way to monitor heart health and detect potential issues.
Overcoming fears associated with traditional ECGs, as the KardiaMobile is less invasive and may help alleviate anxiety for people with disabilities who have concerns about standard ECG procedures.
Easier to disinfect compared to a standard 12-lead ECG, which is particularly important for people with disabilities who may have compromised immune systems.
Minimal training required for use, making it easy for support workers and carers to utilize the device effectively, thus increasing access to heart monitoring for people with disabilities.
Immediate results on six types of arrhythmias, combined with its portability, allows patients experiencing symptomatic palpitations to obtain an ECG reading at the onset of symptoms, leading to more timely diagnosis and treatment.
Potential for use in telemedicine, reducing the need for patients to travel to healthcare facilities, which can be particularly burdensome for people with disabilities. This also lowers the risk of infection for high-risk individuals by enabling remote appointments.
Expanded use in treating patients with infectious diseases, as the self-administered ECG reduces the risk of infection for healthcare practitioners.
Increased accessibility of ECG monitoring in primary care facilities and low-resource healthcare regions due to the relatively low cost and minimal training required to use the KardiaMobile effectively.

TODO: economic benefit of reduced hospital visitation
what economic benefits can we flag, high level societal benefits - 
e.g benefits from not transporting to hospital and ed visits.

Healthcare Practitioners:
Jake Miller is a 37-year-old nurse working in the infectious disease unit at Royal North Shore Hospital in Hornsby. 
He regularly administers ECGs to patients and needs a device that reduces transmission risk while maintaining accuracy comparable to standard 12-lead ECGs. 
As hospitals are short-staffed, he's particularly concerned about avoiding infection and subsequent time off work.

Patients:
Emily Thompson is a 16-year-old student from Randwick with a pacemaker due to a congenital heart defect. 
She requires regular cardiac monitoring but wants to minimize disruption to her studies and social life. 
Her needs focus on portability and quick setup. 

John Moorebank is a 64-year-old retiree from Lithgow who values simplicity and independence. 
Following a stroke that affected his dexterity, and with a family history of heart disease, he needs an easy-to-use monitoring system that doesn't require fine motor skills.

Caretakers:
Margaret "Marg" Brown is a 68-year-old retired caretaker from Ryde who looks after her husband Frank, who has moderate dementia. 
Following a car accident that left Frank with a fractured sternum and possible heart trauma, they need a home-based monitoring solution that's easy to use given their low dexterity and limited familiarity with smartphones.

Healthcare Industry Stakeholders:
John is a 42-year-old NDIS Support Coordinator based in Western Sydney. 
John manages a caseload of 45 participants, many with complex health needs 
requiring regular cardiac monitoring. 
John is responsible for ensuring that funding requests for assistive technology 
are both clinically appropriate and cost-effective. 
His priorities include finding sustainable, long-term health monitoring solutions that provide value for participants' funding packages while ensuring they maintain choice and control over their healthcare decisions.

Dr. Joanne Chia, 51, serves as the Director of Cardiology at Prince of Wales Hospital and must ensure the accuracy and efficiency of cardiac monitoring solutions. Suresh Akash, 40, is an investment director at CardieX limited who needs detailed performance data to make investment decisions.

Government Stakeholders:
Aryan McClure, 36, serves as the Minister of Health for New South Wales and is responsible for overseeing the deployment of new medical devices in health facilities. His role requires evaluating both the technical capabilities and broader implications of implementing the KardiaMobile system across the state's healthcare facilities.



## VSD Users/Stakeholders
Conceptual investigation of the chosen stakeholders: the stakeholders are well-described, with
the values and the frictions across the chosen principles to be well discussed and elaborated
across each stakeholder. A clear summary is provided at the end of the detailed descriptions.

TODO: what does ndis expect of us. contextualised framing, ndis is important stakeholder

TODO: 
opportunity for drs and health team members to help train NDIS participant 
dr will have interest in results and can provide training on the device as well. 
usage in hospitals is an opportunity for being part of the training.

TODO:
jake - if its a device to be used at home, clarification of why is it 
being deployed in a hospital 

(many NDIS participants with history of hospital visitations)



## Critical Analysis
Research, analysis, and comparison: a sophisticated critical analysis of the possible positive
and negative impact of the studied AI/ADM technology, based on similar technology in the
literature or commercial systems that are already deployed. Discuss the possible mitigation
techniques or approaches to deal with the potential risks and ethical concerns of the studied AI
system. Well-justified usage and selection of the used data sources, figures, and/or references.

TODO:
explainability and transparency. 
what are the rules and regulations in nsw around ai and healthcare

This should follow along with the Explainability and Transparency guidelines
mentioned in Australia's AI Ethics Principles.
(https://www.industry.gov.au/publications/australias-artificial-intelligence-ethics-principles/australias-ai-ethics-principles)
This means KardiaMobile must clearly disclose the AI's presence to users, 
provide understandable explanations for their decisions, 
and ensure this information is readily accessible, documented, and regularly reviewed.


## Recommendations
Overall creative and critical thinking: Thinks out of the box, creates or extends to a novel
or unique investigation, incorporating feedback from the presentation session, a well-rounded
discussion and recommendation.

TODO:
where would user data be stored? how can doctors access the pt data? add to recommendations
Implement secure cloud storage using either Microsoft Azure or Google Cloud with healthcare-specific compliance features (e.g., Azure Health Data Services)
Encrypt all data both in transit and at rest using industry-standard encryption protocols

TODO:
rolling it out in hospitals in additional to ndis


TODO:
add a comment on earliest rollout and what it would look like in nsw (following NDIS taskforce results) 
what does ndis expect of us. 

NDIS Provider and Worker Registration Taskforce
The NDIS Provider and Worker Registration Taskforce (the Taskforce) was established to provide advice on the design and implementation of the new graduated risk-proportionate regulatory model proposed in Recommendation 17 of the NDIS Review Final Report(link is external) (NDIS Review) in consultation with the disability community.
Following an extensive period of consultation with the disability community, the Taskforce advice was provided to the Minister and released on 2 August 2024.
The advice sets out a number of recommendations on:
    The design and implementation of the graduated risk-proportionate regulatory model;
    A Provider Risk Framework; and
    Arrangements for platform providers and circumstances where participants directly employ their workers.
The Government is carefully considering each of the recommendations contained in the final advice and will commence consultation on the design elements of a new model from October 2024.
(https://www.dss.gov.au/disability-and-carers-standards-and-quality-assurance/ndis-provider-and-worker-registration-taskforce)


TODO:
clarify this basic tablet smartphone - add in ui design for pt

TODO:
what is the medical device software standard in NSW?

https://www.cec.health.nsw.gov.au/__data/assets/pdf_file/0010/952966/Factsheet-Software-based-medical-devices-including-software-as-a-medical-device.pdf
Therapeutic Goods Administration
Clinical and technical evidence will need to demonstrate the safety and performance of the product
inline with TGA requirements concerning AI based medical software

kardiamobile considered medium risk
https://www.tga.gov.au/resources/guidance/understanding-regulation-software-based-medical-devices#artificial-intelligence-chat-text-and-language







