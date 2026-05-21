

<samp>hi, i'm charles</samp>  
  
<samp>always open to talk  ·  [discord](https://discord.com/users/myplestory)  ·  [twitter](https://x.com/tormentedos)  ·  [email](mailto:myplestorydev@gmail.com)  ·  [site](https://myplestory.dev)</samp>

 

<samp>infra oriented engineer across fintech, web3, and tooling  
building to solve. focused on correctness, auditability, automation, efficiency  
currently working on low latency infra, compliance systems, evaluation harnesses</samp>  

 

**<samp>[polyedge](https://github.com/PolyEdge-Trade)</samp>**  ·  <samp>fintech infrastructure</samp>  ·  <samp>prediction market platform</samp>  ·  *<samp>hardening paid tiers</samp>*  

`tokio-powered data plane` `axum + tower`  `parquet`  `react · vercel · cloudflare`

 

**<samp>[fortifai](https://github.com/Myplestory/FortifAIBot)</samp>**  ·  <samp>cognitive infrastructure</samp> · <samp>LLM-proctored harness</samp> · *<samp>hardening falsifiability</samp>*  

`discord interfaced` `sqlite` `claude` `prompt-cached streaming` `agnostic pipeline`

 

*<samp>___</samp>*

 
  
<img src="https://spotifynowlistening.vercel.app/api/spotify" width="100%" alt=""><br>

 

<details>
<summary><samp>fortifai · self-audit loop · streak 1d</samp></summary>

<sub><samp><i>self-audit: scenario-based time-pressured recall, cross-domain breadth, b3-calibrated<br>
invariant: zero outside assistance. no docs, no ai, no peers. 10m/response, 5m/single refinement<br>
breadth: systems/distributed, backend, sre, ml, ai/llm, frontend, data, security<br>
bar: consistent ≥3 across all 8 swe fields</i></samp></sub>

```
industry     swe                                  updated         2026-05-21
scope        cross-domain · grab-bag              duration        1h 0m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  frontend           error-boundary          ₂   2   ₁
q2  ml-engineering     probability             ₂   2   ₁
q3  sre                error-budget-policy     ₂   2   ₁
q4  security           idor                    ₃   3   ₂
q5  systems-distributeddual-region-active      ₂   2   ₁

gaps         component-failure-isolation · dual-region-active-active · error-boundary · error-budget-policy

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · frontend · error-boundary · pre 2 → post 2 · ceiling —</samp></summary>

<small>

 

**Scenario:** Team Y is building a dashboard SaaS where the main page composes ~12 independent widgets (charts, tables, KPI tiles) from different upstream services. Today, when one widget's render throws (e.g., it receives malformed data from a flaky service), the entire dashboard goes blank with a white screen and the user has to refresh. Product wants the failing widget to show an inline error state while the other 11 keep working. Explain the React mechanism you'd use to achieve this, why it works at the level of the component tree, and what classes of errors it does NOT catch — name at least two — so the team understands where complementary handling is still required.

 

**Refinement:** You said 'a global per page/app level context that passes that context down/propogates errors but stops before reachig the highest level of the heirarchy'. Clarify: what specific React mechanism enforces the boundary at which an error stops propagating up the tree, and how does it intercept a render-phase throw rather than relying on state updates?

 

**Assessment:** The question tested whether the answerer could name React's Error Boundary mechanism as the per-widget failure-isolation primitive, explain that it catches render-phase throws because React's reconciler walks up the fiber tree to the nearest ancestor boundary, and name at least two classes of errors it does not catch. The original response substituted virtualization and context-based state scoping for the actual mechanism, which addresses different problems (DOM node budget and prop-drilling) and does not intercept a render throw. The refinement probe was explicit about the gap, and the follow-up introduced a C++/Rust idiom ('implicit RAII', Ok/Err optionals) rather than naming React's lifecycle-based interception — confirming the canonical mechanism is not in the answerer's recall. The two classes of uncaught errors named in the original answer (duplicate renders, state reconciliation races) are also not the documented uncaught classes.

**Literature**

- [remediation] React Documentation — Catching rendering errors with an error boundary — Component reference §'Catching rendering errors with an error boundary' (~4 pages: the section itself plus the linked 'static getDerivedStateFromError' and 'componentDidCatch' API entries) — ~30m
- [remediation] react-error-boundary — README §'Usage', §'API', §'FAQ — Why won't my errors get caught?' — ~25m

</small>
</details>

<details>
<summary><samp>q2 · ml-engineering · probability-calibration · pre 1 → post 2 · ceiling —</samp></summary>

<small>

 

**Scenario:** A fraud-detection model at fintech Company X is a gradient-boosted classifier whose AUC is 0.94 on a held-out set. The risk team wants to use the model's predicted probability directly as an expected-loss input (e.g., 'block if predicted P(fraud) × transaction_amount > $X'). On inspection, the model's predicted probabilities are systematically too low in the 0.6–0.9 range — when the model says 0.8, the empirical fraud rate among those transactions is closer to 0.92. Explain (a) what 'calibration' means here and how it differs from discrimination/AUC, (b) the mechanism by which a strong-discriminator model can still be poorly calibrated, and (c) one post-hoc calibration technique you'd apply, what data you'd fit it on, and what it gives up.

 

**Refinement:** You said 'it reduces the gap between the trained accuracy/precision (golden set) and'. Clarify: what specific property of the model's output distribution is being corrected when calibration is applied, distinct from changing how the model separates fraud from non-fraud cases?

 

**Assessment:** The answer does not establish what calibration is as a property of the output distribution — it is conflated with threshold tuning, overfitting, and feature-level error analysis throughout. The refinement nudged the answer toward 'post-fit remap to empirical data', which is directionally correct, but the canonical methods, their data requirement, and what they trade off are never produced. The gap is at the level of the core vocabulary and standard toolkit, not at the level of nuance.

**Literature**

- [remediation] scikit-learn User Guide §1.16 Probability calibration — §1.16.1 Calibration curves, §1.16.2 Calibrating a classifier, §1.16.3 Usage (full chapter) — ~45m
- [remediation] Designing Machine Learning Systems — Ch. 6 §Evaluation Metrics — Calibration subsection (one focused subsection) — ~20m

</small>
</details>

<details>
<summary><samp>q3 · sre · error-budget-policy · pre 2 → post 2 · ceiling —</samp></summary>

<small>

 

**Scenario:** Service A has a 99.9% monthly availability SLO, giving roughly 43 minutes of allowed downtime per month. Three weeks into the month, an incident has already burned ~38 minutes of budget. The product team wants to ship a major feature next week. As the SRE on-call lead, walk through (a) how you'd compute the current error-budget state in concrete terms (what 'budget remaining' means numerically and how you'd track it through the rest of the month), (b) what policy this should trigger and why error-budget policies tie release decisions to budget state rather than to individual incident severity, and (c) the tradeoff against a 'fast burn' alert that fires within the same window — what does each signal tell you that the other doesn't?

 

**Refinement:** You said 'burn alert that fires in the same window, the signals get more urgency, but along certain axes'. Clarify: what distinct information does a fast-burn rate signal give you about current consumption velocity that the remaining-budget figure alone does not capture?

 

**Assessment:** The question asked for three specific things: concrete arithmetic on the remaining budget, the canonical policy mechanism that ties release decisions to budget state, and the stock-vs-flow distinction between remaining budget and fast-burn rate. The response substituted a generic multi-signal matrix for all three. The refinement probe specifically narrowed in on the stock/flow distinction; the answer collapsed the two signals into a single non-canonical formula and introduced inverted circuit-breaker state semantics. The gap is in the canonical SRE error-budget vocabulary and the multi-window multi-burn-rate alerting construction.

**Literature**

- [remediation] Site Reliability Workbook — Ch. 5 'Alerting on SLOs' — focused chapter on multi-window multi-burn-rate alerting; specifically the worked example computing budget consumed as (1 − SLO) × total_window, and the table mapping burn-rate × window pairs to paging vs. ticket alerts — ~1h 15m
- [remediation] Site Reliability Engineering — Ch. 3 'Embracing Risk' and Ch. 4 'Service Level Objectives' — focused chapters establishing the error-budget-as-contract concept: why ship/freeze decisions are tied to budget state and not incident severity, and how the budget depersonalizes the product-vs-SRE negotiation — ~1h 30m

</small>
</details>

<details>
<summary><samp>q4 · security · idor · pre 2 → post 3 · ceiling b1 · transitional b2–b3</samp></summary>

<small>

 

**Scenario:** An audit of a healthcare SaaS API turns up the following endpoint: GET /api/v2/patients/{patient_id}/records. The handler authenticates the caller via a session JWT (signature validated, not expired) and then loads and returns the records for the patient_id in the URL. Authenticated user Alice (patient_id=4471) can change the URL to /api/v2/patients/4472/records and receive Bob's records. Name the vulnerability class, explain the mechanism (why authentication passes but the attack still succeeds), and describe the structural fix — including where the check belongs in the request pipeline and why a single middleware that 'checks the JWT is valid' is not sufficient. Contrast briefly with how this differs from a missing-authentication bug.

 

**Refinement:** You said 'the DATA validity of the request needs to be handled by a gateway/check at the service ingest'. Clarify: what specific attribute of the authenticated session must be compared against what specific attribute of the requested resource at that check point, and where does that pairing come from?

 

**Assessment:** The answer recognizes that JWT validity is not authority and, under refinement, isolates the correct attribute pairing (authenticated subject identity against the resource's ownership identifier). What it does not produce — even when explicitly asked — is the canonical class name for this failure, the contrast with missing-authentication that the prompt requested, or a correct source-of-truth for the ownership lookup: the refinement proposes caching session-to-owner mappings as the authoritative comparator, which inverts the trust model (the resource's stored owner field is the authoritative side, not a session-derived cache). The vocabulary gap and the inverted-trust-source gap together cap the B3 score at the mechanism-precedence floor.

**Literature**

- [remediation] OWASP API Security Top 10 — API1:2023 Broken Object Level Authorization — Full page: Description, Example Attack Scenarios, How to Prevent — ~20m
- [remediation] OWASP Authorization Cheat Sheet — Chapter: 'Enforce Authorization Checks on Static and Dynamic Resources' and 'Verify the Source of a Website Redirect and Other Similar Transformations' — focus on object-level checks and authoritative ownership lookup — ~30m

</small>
</details>

<details>
<summary><samp>q5 · systems-distributed · dual-region-active-active · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A SaaS product runs in one region today and the team is planning an active-active two-region deployment (us-east, eu-west) for an inventory-management table where each row represents a SKU's available stock count, mutated by decrement-on-order and increment-on-restock operations. Each region accepts writes locally and replicates asynchronously to the other. Walk through (a) the concrete failure mode that can occur when the inter-region link partitions for several minutes while both regions accept writes against the same SKU, (b) why naive last-write-wins on a wall-clock timestamp is the wrong conflict-resolution primitive for this specific workload, and (c) one alternative resolution strategy and why it fits the operation semantics better — including what it still gives up compared to a single-region design.

 

**Refinement:** You said 'tracking the RECONCILIATION is the load bear, not the ORDERING OF THE DATA ITSELF'. Clarify: how does your snapshot/hybrid-clock approach handle two concurrent decrements against the same SKU stock count that together would drive inventory below zero, given that each region saw sufficient stock locally at write time?

 

**Assessment:** The answer recognized that asynchronous replication creates a window of concurrent independent writes, but reached for ordering/snapshot/vector-clock primitives when the question was about composing commutative operations. The refinement probe handed the answerer the exact diagnostic case — two decrements driving stock below zero — and the response chose a winner ('DB2 wins') rather than recognizing that both decrements must compose. The gap is the operation-semantics frame: this workload's writes are deltas, not absolute values, and the correct primitive class preserves the operation rather than picking a state. The standard remediation pointer is the CRDT family, specifically counter CRDTs, and the inventory-as-escrow alternative.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 5 §Handling Write Conflicts (pp. 171–177) and Ch. 5 §Conflict Resolution — 'Custom Conflict Resolution Logic' & 'Automatic Conflict Resolution' / 'CRDTs' (pp. 174–177) — ~1h 30m
- [remediation] A comprehensive study of Convergent and Commutative Replicated Data Types — §3 'State-based CRDTs' and §3.1 'Counter' (PN-Counter) — pp. 13–18 — ~50m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
