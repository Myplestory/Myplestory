

hi, i'm charles  
  
always open to talk  ·  [discord](https://discord.com/users/myplestory)  ·  [twitter](https://x.com/tormentedos)  ·  [email](mailto:myplestorydev@gmail.com)  ·  [site](https://myplestory.dev)

 

infra oriented engineer across fintech, web3, and tooling  
building to solve. focused on correctness, auditability, automation, efficiency  
currently working on low latency infra, compliance systems, evaluation harnesses  

 

**[polyedge](https://github.com/PolyEdge-Trade)**  ·  fintech infrastructure  ·  prediction market platform  ·  *hardening paid tiers*  

`tokio-powered data plane` `axum + tower`  `parquet`  `react · vercel · cloudflare`

 

**[fortifai](https://github.com/Myplestory/FortifAIBot)**  ·  cognitive infrastructure · LLM-proctored harness · *hardening falsifiability*  

`discord interfaced` `sqlite` `claude` `prompt-cached streaming` `agnostic pipeline`

 

*___*

 
  
<img src="https://spotifynowlistening.vercel.app/api/spotify" width="100%" alt=""><br>

 

<details>
<summary><samp>fortifai · self-audit loop · streak 2d</samp></summary>

<sub><samp><i>self-audit: scenario-based time-pressured recall, cross-domain breadth, b3-calibrated<br>
invariant: zero outside assistance. no docs, no ai, no peers. 10m/response, 5m/single refinement<br>
breadth: systems/distributed, backend, sre, ml, ai/llm, frontend, data, security<br>
bar: consistent ≥3 across all 8 swe fields</i></samp></sub>

```
industry     swe                                  updated         2026-05-11
scope        cross-domain · grab-bag              duration        1h 6m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  ml-engineering     class-imbalance         ₂   1   ₁
q2  frontend           hydration-cost          ₄   4   ₃
q3  sre                autoscaling-signal      ₄   4   ₃
q4  backend            api-pagination          ₂   1   ₁
q5  security           sql-injection-defense   ₃   3   ₂

strengths    autoscaling-signal-selection · scale-up-lag · cpu-vs-queue-depth-metric · hydration-cost
gaps         class-imbalance · resampling-strategy · calibration-loss · api-pagination-consistency

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · ml-engineering · class-imbalance · pre 1 → post 1 · ceiling b1 · transitional b2</samp></summary>

<small>

 

**Scenario:** A team is training a binary classifier to flag fraudulent transactions. The positive class is ~0.3% of the dataset. A junior engineer trains on the raw data and reports 99.7% accuracy. A senior suggests SMOTE oversampling on the training set; another suggests class weighting in the loss; a third suggests downsampling the majority class. Explain the mechanism by which each of these three approaches changes what the model learns, what each gives up (consider calibration of predicted probabilities and sample efficiency), and how you would decide between class-weighting and SMOTE for a downstream system that uses the predicted probability as a score (not just a hard label).

 

**Assessment:** The response correctly enumerates the three options and where each sits in the pipeline, but never engages with the concept the question is structured around — what each intervention does to the predicted-probability output as a number that a downstream system consumes as a score. The refinement explicitly named the calibration probe, and the answer doubled down on the position that class weighting leaves outputs essentially unaffected, which is the wrong direction. The gap is in connecting any of the three interventions to a specific, named distortion of the predicted-probability distribution relative to the empirical base rate.

**Literature**

- [remediation] Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (3e) — Ch. 3 'Classification' §Performance Measures and Ch. 4 'Training Models' §Logistic Regression — through end of Ch. 4 — ~5h
- [remediation] Properly Calibrated Probabilities under Class Imbalance — Entire 'Probability calibration' user-guide page (read fully) — ~1h

</small>
</details>

<details>
<summary><samp>q2 · frontend · hydration-cost · pre 3 → post 4 · ceiling b3 · transitional b4</samp></summary>

<small>

 

**Scenario:** A marketing-heavy e-commerce site is choosing between client-side rendering (CSR), server-side rendering (SSR), and static site generation (SSG) for product detail pages. The pages have personalized recommendations below the fold and a price/inventory widget that must reflect live values. Explain how each rendering strategy affects FCP and TTI, what hydration is and why it can make a 'fast-looking' SSR page feel unresponsive on mid-tier mobile, and recommend an approach for this page (commit to one). Identify which parts of the page would be problematic under your chosen strategy and how you'd mitigate them.

 

**Assessment:** The answer correctly partitioned the page (static shell via SSG, dynamic islands via CSR) and the refinement recovered the core hydration mechanism — that visual completion precedes interactivity because the runtime still has to walk the DOM and attach event handlers. The gap is that the response treats hydration cost as a reconciliation step rather than as main-thread JavaScript parse/execute time, which is what specifically explains the 'fast-looking but unresponsive' symptom on mid-tier mobile. The original commit was also not revisited once the hydration mechanism was made explicit.

**Literature**

- [remediation] web.dev — Core Web Vitals and Rendering Performance — 'Largest Contentful Paint (LCP)', 'Interaction to Next Paint (INP)', and 'Total Blocking Time' articles — read all three end-to-end — ~45m
- [growth] React Server Components and Selective Hydration — Connection: once initial hydration cost is understood, RSC + selective hydration is the next-step strategy that lets the SSG-shell-plus-CSR-islands intuition the answer reached be implemented as a single framework primitive. — ~1h

</small>
</details>

<details>
<summary><samp>q3 · sre · autoscaling-signal-selection · pre 4 → post 4 · ceiling b3 · transitional b4</samp></summary>

<small>

 

**Scenario:** A queue-backed worker fleet processes background jobs. The on-call engineer configures Kubernetes HPA to scale on CPU at 70% utilization. Under a burst of traffic, the queue depth grows to tens of thousands of messages before the fleet scales out, and even after scaling, the backlog takes 30 minutes to drain. Explain why CPU is the wrong scaling signal for this workload, what mechanism causes the lag between load arrival and effective capacity (consider pod startup time, image pull, warmup), and what scaling signal you would use instead. Articulate the tradeoff between scaling on a leading indicator (queue depth or arrival rate) vs. a lagging indicator (CPU) — what does each give up?

 

**Assessment:** The strongest answer in the run. The mechanism invariant for SRE B3 is fully satisfied: the failure mode is named, the lag contributors are enumerated correctly, a bounded mitigation is committed to (horizontal scale gated on queue depth, with CPU as a coupled secondary signal), and the refinement productively distinguishes the failure modes of using each signal alone. The remaining gap is contract-level: the answer reasons about signals and scaling actions but does not name an SLO or quantify the pod-budget cost of biasing toward the leading indicator, which is what would lift it into B4 territory.

**Literature**

- [remediation] Google SRE Book — Practical Alerting and Handling Overload — Ch. 6 'Monitoring Distributed Systems' (SLI/SLO/SLA section) and Ch. 21 'Handling Overload' — read both chapters — ~2h
- [growth] KEDA — Kubernetes Event-Driven Autoscaling — Connection: the answer independently reasoned to queue-depth-based horizontal scaling; KEDA is the productionised primitive that implements exactly that scaler taxonomy on top of HPA. — ~45m

</small>
</details>

<details>
<summary><samp>q4 · backend · api-pagination-consistency · pre 2 → post 1 · ceiling b1 · transitional b2</samp></summary>

<small>

 

**Scenario:** A REST API returns a list of orders sorted by created_at descending, paginated with `?page=N&size=50`. Users report that when they scroll quickly, they occasionally see the same order twice on consecutive pages, or skip orders entirely. Explain the mechanism that causes duplicates/skips under offset pagination when the underlying dataset is being mutated concurrently. Describe how keyset (cursor) pagination fixes this, what its implementation requires (consider the sort key and tiebreakers), and what it gives up compared to offset pagination. Commit to one approach for this orders endpoint and justify.

 

**Assessment:** The response located the cause of pagination duplicates and skips in client-side rendering desync rather than in concurrent server-side mutation of the underlying row-set between page requests. The refinement was a direct probe at the server-side mechanism — 'what happens on the server side to the ordered result set' — and the answer responded that the server is unaware and uninvolved, which inverts the actual cause. The gap is the offset-pagination mechanism itself: under concurrent inserts/deletes, the absolute position that page N+1's OFFSET resolves against is no longer the same row-set page N saw, which is precisely why keyset pagination (anchored on a stable sort-key + tiebreaker) fixes the problem.

**Literature**

- [remediation] Use the Index, Luke! — Paging Through Results — 'Paging Through Results' chapter — read the full chapter including 'The Trouble with OFFSET' and 'Seek Method' subsections — ~30m
- [remediation] Designing Data-Intensive Applications — Ch. 7 'Transactions' §Read Skew and Snapshot Isolation (pp. 233–242) and the consistency-anomaly discussion through 'Lost Updates' (pp. 246) — ~1h 15m

</small>
</details>

<details>
<summary><samp>q5 · security · sql-injection-defense-layers · pre 3 → post 3 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A code review surfaces a Python service that builds a SQL query by string-concatenating a user-supplied `sort_column` parameter into an `ORDER BY` clause: `f"SELECT * FROM orders WHERE customer_id = %s ORDER BY {sort_column}"`, with `customer_id` passed as a bound parameter. The author claims 'we're using parameterized queries, so we're safe from SQL injection.' Explain why this claim is wrong, the specific mechanism by which parameterized queries prevent injection (and why that mechanism doesn't extend to identifiers like column names), and the correct defense for the `sort_column` case. Then compare that defense to using an ORM's `order_by` API — what does each give up?

 

**Assessment:** The answer correctly identifies the attack surface as the concatenated identifier and commits to a defense-in-depth approach with an allowlist-from-discovery-endpoint as the structural fix — both genuine B3 instincts. The information-leakage observation about exposing column names to the user is a strong adjacent insight. The gap is in articulating *why* parameterized queries are safe in their domain: the database driver sends the query template and the bound values through separate protocol fields so the SQL parser produces a query plan once with parameter placeholders, and bound values can never be re-lexed as syntax. This is the structural property absent for identifiers, and the refinement probe asked for it directly without eliciting it. A secondary gap is residual-risk awareness on ORM order_by APIs and on keeping the allowlist in sync with schema changes.

**Literature**

- [remediation] OWASP SQL Injection Prevention Cheat Sheet — Defense Option 1 (Prepared Statements) and 'Defense Option 4: Allow-list Input Validation' — read both sections fully — ~30m
- [remediation] PostgreSQL Documentation — Prepared Statements and Protocol-Level Bind — 'PREPARE' SQL command page and the linked 'Extended Query' protocol-flow subsection in Ch. 55 Frontend/Backend Protocol — ~25m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
