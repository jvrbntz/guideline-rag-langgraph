# CAP RAG Evaluation: Test Questions with Ground Truth

**Source:** ATS/IDSA 2019 Community-Acquired Pneumonia Clinical Practice Guideline  
**Purpose:** Evaluation dataset for clinical RAG system — drives chunking decisions and defines success criteria  
**Status:** V1 — covers core decision branches across outpatient, inpatient nonsevere, and inpatient severe settings

---

## Q1: Basic outpatient treatment, no comorbidities

**Question:** What is the recommended empiric antibiotic for an otherwise healthy adult with CAP managed in the outpatient setting with no comorbidities?

**Expected answer:**  
Amoxicillin 1g three times daily OR doxycycline 100mg twice daily. Azithromycin or clarithromycin are options only if local pneumococcal resistance is <25%. Macrolide monotherapy is no longer strongly recommended (departure from prior guidelines).

**Evidence strength:** Strong recommendation for amoxicillin (moderate quality); conditional for doxycycline (low quality); conditional for macrolides (low quality)

**Source location:** Question 8, Table 3

**What this tests:** Basic first-line retrieval. Also tests that the system captures the macrolide caveat — a meaningful change from 2007 guidelines that a naive retrieval might miss.

---

## Q2: Outpatient with comorbidities and recent macrolide use

**Question:** What antibiotic regimen is recommended for an outpatient with CAP who has COPD and was treated with azithromycin six weeks ago?

**Expected answer:**  
Patient has both comorbidities (COPD) and recent macrolide use. Because recent exposure to one antibiotic class warrants switching to a different class, macrolides are excluded here. Appropriate regimens are: (1) amoxicillin/clavulanate OR a cephalosporin PLUS doxycycline, or (2) respiratory fluoroquinolone monotherapy (levofloxacin 750mg daily, moxifloxacin 400mg daily, or gemifloxacin 320mg daily). Beta-lactam monotherapy alone is not recommended for patients with comorbidities.

**Evidence strength:** Strong recommendation (moderate quality) for combination therapy; strong for fluoroquinolone

**Source location:** Question 8, Table 3 footnotes, antibiotic class-switching convention

**What this tests:** Requires two-step reasoning — comorbidities change the regimen, AND recent antibiotic class exposure requires switching classes. Tests whether the system retrieves the class-switching convention alongside the comorbidity table.

---

## Q3: Nonsevere inpatient CAP, no resistant-organism risk factors

**Question:** For a hospitalized adult with nonsevere CAP and no risk factors for MRSA or Pseudomonas aeruginosa, what empiric antibiotic regimens are recommended?

**Expected answer:**  
Two options, in no order of preference: (1) beta-lactam plus macrolide — ampicillin-sulbactam, cefotaxime, ceftriaxone, or ceftaroline PLUS azithromycin or clarithromycin; or (2) respiratory fluoroquinolone monotherapy — levofloxacin 750mg daily or moxifloxacin 400mg daily. Beta-lactam monotherapy is not routinely recommended. A third option (beta-lactam plus doxycycline) exists for patients with contraindications to both macrolides and fluoroquinolones (conditional, low quality).

**Evidence strength:** Strong recommendation, high quality of evidence for both primary options

**Source location:** Recommendation 9.1, Table 4

**What this tests:** Standard inpatient retrieval. Tests correct evidence strength and whether the system correctly excludes beta-lactam monotherapy.

---

## Q4: Severe inpatient CAP, no resistant-organism risk factors

**Question:** For an adult admitted to the ICU with severe CAP and no MRSA or Pseudomonas risk factors, what are the recommended empiric regimens?

**Expected answer:**  
Beta-lactam PLUS macrolide (strong, moderate quality) OR beta-lactam PLUS respiratory fluoroquinolone (strong, low quality). Respiratory fluoroquinolone monotherapy is NOT recommended for severe CAP — this is a critical distinction from nonsevere inpatient treatment. Same beta-lactam options as nonsevere apply (ampicillin-sulbactam, cefotaxime, ceftriaxone, ceftaroline). Specific agents and doses are same as Recommendation 9.1.

**Evidence strength:** Strong for beta-lactam/macrolide (moderate quality); strong for beta-lactam/fluoroquinolone (low quality)

**Source location:** Recommendation 9.2, Table 4

**What this tests:** Tests the severe vs nonsevere distinction — specifically that fluoroquinolone monotherapy is NOT an option in severe CAP. A system that conflates the two categories will fail this question.

---

## Q5: MRSA risk factors and empiric coverage decision [FIXED — two-tier structure]

**Question:** What are the risk factors for MRSA that should guide empiric antibiotic decisions in hospitalized patients with CAP, and how does the tier of risk factor change management?

**Expected answer:**  
The guideline defines two tiers:

**Tier 1 — Prior respiratory isolation of MRSA (within prior year):** Warrants empiric MRSA coverage plus cultures/nasal PCR in both nonsevere and severe CAP. Strongest risk factor.

**Tier 2 — Recent hospitalization AND parenteral antibiotics in last 90 days (with locally validated risk factors):** Management differs by severity:
- Nonsevere CAP: Obtain cultures, but WITHHOLD empiric MRSA coverage unless cultures or nasal PCR are positive
- Severe CAP: Add empiric MRSA coverage AND obtain cultures/nasal PCR for deescalation

Note: No validated scoring system exists to identify MRSA risk with high positive predictive value. Local prevalence data should guide decisions.

**Evidence strength:** Strong recommendation (moderate quality) for abandoning broad MRSA coverage without specific risk factors

**Source location:** Recommendation 11, Table 4, rationale section

**What this tests:** This is the most important nuance in the guideline. The two-tier structure and the nonsevere/withhold recommendation are the exact clinical judgment points this system must capture correctly. A system that retrieves only "risk factors" without the severity-conditional action will fail this.

---

## Q6: Empiric MRSA drug selection and dosing

**Question:** What are the recommended empiric antibiotic options and doses for MRSA coverage in a hospitalized patient with CAP?

**Expected answer:**  
Vancomycin 15 mg/kg every 12 hours (adjust based on levels) OR linezolid 600mg every 12 hours. These are endorsed from the 2016 ATS/IDSA HAP/VAP guidelines. No preference order between the two.

**Evidence strength:** Strong recommendation (moderate quality)

**Source location:** Recommendation 11, Table 4 footnote x

**What this tests:** Specific drug and dose retrieval — tests whether the system correctly attributes these to the HAP/VAP guideline cross-reference, not original evidence in this document.

---

## Q7: Aspiration pneumonia — anaerobic coverage

**Question:** Should patients hospitalized with suspected aspiration pneumonia receive routine empiric anaerobic antibiotic coverage in addition to standard CAP treatment?

**Expected answer:**  
No — not routinely. The guideline recommends against routine anaerobic coverage for suspected aspiration. Anaerobic coverage should be added only if lung abscess or empyema is suspected. More recent studies show anaerobes are uncommon in hospitalized aspiration cases, and increasing C. difficile rates make unnecessary clindamycin use risky. Standard CAP regimens provide adequate coverage for the most likely pathogens.

**Evidence strength:** Conditional recommendation (very low quality of evidence)

**Source location:** Question 10

**What this tests:** Counterintuitive recommendation that departs from traditional teaching. Tests whether the system retrieves the correct nuance (not "never" — only if abscess/empyema) rather than a binary yes/no.

---

## Q8: Complex scenario — severe CAP with prior MRSA isolation

**Question:** A patient arrives to the ED with severe CAP meeting ICU criteria. Chart review shows a sputum culture positive for MRSA from a hospitalization 8 months ago. What empiric antibiotic regimen should be initiated?

**Expected answer:**  
This patient has prior respiratory isolation of MRSA within the prior year — the strongest tier-1 risk factor. For severe CAP, the regimen is: (1) standard severe CAP backbone (beta-lactam PLUS macrolide OR beta-lactam PLUS respiratory fluoroquinolone) PLUS (2) empiric MRSA coverage (vancomycin 15mg/kg q12h or linezolid 600mg q12h). Blood and sputum cultures should be obtained promptly to allow deescalation at 48 hours if MRSA is not confirmed. Fluoroquinolone monotherapy is not appropriate for severe CAP.

**Evidence strength:** Strong recommendation

**Source location:** Recommendation 9.2 + Recommendation 11 + Table 4 (severe + prior respiratory MRSA isolation column)

**What this tests:** Multi-step reasoning: severity classification → backbone selection (with correct exclusion of FQ monotherapy) → MRSA risk tier → add coverage → cultures for deescalation. This is the most complex reasoning chain in the test set.

---

## Q9: HCAP classification

**Question:** Should the Healthcare-Associated Pneumonia (HCAP) classification be used to guide empiric antibiotic selection for patients with CAP?

**Expected answer:**  
No — the guideline strongly recommends abandoning the HCAP categorization. Studies showed HCAP risk factors (nursing home residence, recent hospitalization, home infusion therapy, dialysis, etc.) do not reliably predict antibiotic-resistant pathogens in most settings, but led to significant overuse of vancomycin and antipseudomonal beta-lactams without improving outcomes. Instead, clinicians should use locally validated risk factors specific to MRSA or P. aeruginosa at their institution.

**Evidence strength:** Strong recommendation (moderate quality)

**Source location:** Recommendation 11

**What this tests:** Important conceptual shift from prior guidelines. Tests whether the system retrieves the "why" (overuse without outcome benefit) not just the "what."

---

## Q10: Duration of therapy

**Question:** How long should antibiotics be continued for a hospitalized patient with CAP who is clinically improving?

**Expected answer:**  
Antibiotic duration should be guided by a validated measure of clinical stability — resolution of vital sign abnormalities (heart rate, respiratory rate, blood pressure, oxygen saturation, temperature), ability to eat, and normal mentation. Therapy should continue until stability is achieved AND for no less than 5 days total, even if stability occurs before day 5. Most patients reach stability within 48–72 hours, making 5 days appropriate for most. For suspected or confirmed MRSA or P. aeruginosa, 7 days is recommended. Failure to achieve stability by day 5 should prompt reassessment for resistant pathogens, complications (empyema, lung abscess), or alternative diagnoses.

**Evidence strength:** Strong recommendation (moderate quality)

**Source location:** Question 15

**What this tests:** Discrete clinical question distinct from antibiotic selection. Tests whether the system retrieves the stability criteria (specific vital sign parameters) rather than just "5 days," and whether it catches the MRSA/Pseudomonas 7-day extension.

---

## Q11: Nonsevere inpatient + recent hospitalization/parenteral antibiotics

**Question:** A patient is admitted with nonsevere CAP. She was hospitalized for a UTI 6 weeks ago and received IV piperacillin-tazobactam during that admission. No prior MRSA or Pseudomonas cultures are on record. What is the recommended approach?

**Expected answer:**  
This patient has tier-2 MRSA/Pseudomonas risk (recent hospitalization + parenteral antibiotics in last 90 days) but NO prior respiratory isolation of either organism. For nonsevere CAP with tier-2 risk: obtain blood and sputum cultures, but DO NOT add empiric MRSA coverage. Initiate standard nonsevere CAP regimen (beta-lactam + macrolide OR respiratory fluoroquinolone). Withhold extended-spectrum empiric therapy unless cultures return positive — or if rapid nasal MRSA PCR is available and positive. This is the key distinction from tier-1 risk or severe CAP, where empiric extended coverage IS recommended.

**Evidence strength:** Strong recommendation (moderate quality) for the withhold strategy in nonsevere CAP

**Source location:** Recommendation 11, Table 4 (nonsevere + recent hospitalization/parenteral antibiotics column)

**What this tests:** The hardest and most practically important recommendation in the guideline. Directly tests the severity-conditional branching in the two-tier risk framework. A system that retrieves "get cultures + withhold coverage" vs "get cultures + add coverage" has actually understood the guideline structure.

---

## Q12: Procalcitonin and antibiotic initiation

**Question:** Can a low serum procalcitonin level be used to withhold empiric antibiotics in a patient with radiographically confirmed CAP?

**Expected answer:**  
No. The guideline recommends initiating empiric antibiotic therapy in all adults with clinically suspected and radiographically confirmed CAP regardless of procalcitonin level. Although low procalcitonin decreases the likelihood of bacterial infection, it cannot rule out bacterial pneumonia with sufficient accuracy to justify withholding antibiotics — particularly in severe CAP. Exception: in patients with positive influenza test, no evidence of bacterial pathogen, and early clinical stability, consideration may be given to discontinuing antibiotics earlier (48–72 hours), but this is not routine practice.

**Evidence strength:** Strong recommendation (moderate quality) against using procalcitonin to withhold antibiotic initiation

**Source location:** Question 5

**What this tests:** Common clinical question with a clear guideline answer that runs counter to procalcitonin's use in other respiratory contexts (e.g., bronchitis). Tests whether the system retrieves the correct CAP-specific recommendation and the influenza exception.

---
