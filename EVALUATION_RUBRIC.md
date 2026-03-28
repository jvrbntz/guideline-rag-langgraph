# Evaluation Rubric

## Overview

This rubric scores pipeline outputs against the ATS/IDSA 2019 CAP guideline across three dimensions: faithfulness to retrieved context, relevance to the query, and whether the answer cites its source. The driving concern in a clinical setting is the confident wrong answer — not a gap, which is visible and prompts verification, but a plausible-sounding claim that goes beyond or contradicts the guideline without signaling that it has. That's the failure mode this rubric is designed to catch.

This rubric has not been clinically validated. Clinical judgment remains with the treating clinician.

---

## Metrics

### Faithfulness

Does the answer stay within what the retrieved chunks actually say? Hallucinated or extrapolated claims score lower — even if they happen to be clinically accurate.

| Score | Description |
| ------- | ------------- |
| 3 | Fully grounded. No claims go beyond the retrieved context. |
| 2 | Partially grounded. Some claims are supported; others introduce information absent from the retrieved chunks. |
| 1 | Contradicts the retrieved context, or makes claims entirely absent from it. |

---

### Answer Relevance

Answer Relevance measures the semantic alignment between a generated answer and the expected answer. A high cosine similarity score means the two are closely related in embedding space. It does not measure whether the answer completely addresses the clinical query.

| Score | Description |
| ------- | ------------- |
| 3 | cosine sim ≥ 0.75 — high semantic overlap with reference answer |
| 2 | cosine sim 0.50–0.74 — moderate overlap |
| 1 | cosine sim < 0.50 — low overlap |  

Thresholds were set empirically based on V1 eval results and general cosine similarity conventions. They have not been statistically validated and should be recalibrated with a larger eval set in V2.

---

### Citation Present

Is the source document and page referenced in the answer? Without attribution, the clinician has no path to verify the response.

| Score | Description |
| ------- | ------------- |
| Pass | Source document and page number are present in the response. |
| Fail | Answer is provided without attribution. |

---

## Limitations

- Faithfulness and Answer Relevance are scored by an LLM judge with no clinical training. Human review is required for any safety-critical use case.
- An answer can score 3 on all three metrics and still be clinically wrong. This rubric measures output quality against the retrieved context, not clinical correctness.
- Retrieval quality is not measured here — chunk-level recall and context relevance require ground truth labels that aren't available in V1. Deferred to V2.
- Citation Present checks for existence only. It does not validate whether the cited source actually supports the answer. Citation correctness is deferred to V2.
