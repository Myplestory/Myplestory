

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
<summary><samp>fortifai · self-audit loop</samp></summary>

<sub><samp><i>self-audit: scenario-based time-pressured recall, cross-domain breadth, b3-calibrated<br>
invariant: zero outside assistance. no docs, no ai, no peers. 10m/response, 5m/single refinement<br>
breadth: systems/distributed, backend, sre, ml, ai/llm, frontend, data, security<br>
bar: consistent ≥3 across all 8 swe fields</i></samp></sub>

```
industry     swe                                  updated         2026-05-13
scope        cross-domain · grab-bag              duration        1h 3m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  backend            deadlock-detection      ₂   2   ₁
q2  data-engineering   change-data-capture     ₄   3   ₂
q3  ml-engineering     feature-scaling         ₂   2   ₁
q4  frontend           useeffect-dependency    ₃   3   ₂
q5  systems-distributedfan-out-on-write-vs     ₅   4   ₃

strengths    celebrity-problem · fan-out-on-write-vs-read · write-amplification
gaps         deadlock-detection · feature-scaling · lock-ordering · regularization-sensitivity-to-scale

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · backend · deadlock-detection · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A payments service runs in PostgreSQL. Two endpoints each take a balance transfer: endpoint A locks account row X then Y (SELECT ... FOR UPDATE in that order), endpoint B locks Y then X. Under load, you see periodic transactions failing with 'deadlock detected' and being rolled back by Postgres after roughly 1 second. A junior engineer proposes increasing `deadlock_timeout` to 10s so 'the deadlocks have time to resolve themselves.' Explain (a) the mechanism by which Postgres detects this deadlock and what happens to the loser transaction, (b) why the junior's proposal does not eliminate deadlocks and what it actually changes, and (c) what structural fix removes the deadlock class entirely and why it works. Be concrete about what 'lock ordering' means at the row level when the two accounts are not known until query time.

 

**Assessment:** The answer identifies the deadlock domain and correctly rejects the junior's deadlock_timeout proposal as treating the symptom, but the structural-fix step targets the wrong layer: it proposes CQRS/materialized views, which are read-path patterns and do not participate in row-level write locks on the base accounts table that both transfer endpoints contend on. The refinement probe pointed directly at this contradiction — two concurrent writers acquiring locks on the same base rows in conflicting orders — and the response doubled down on read/write separation rather than pivoting to the canonical fix. The unaddressed gap is the primitive that actually closes the wait-for cycle at the row-lock level and the reason it is sufficient under concurrent retries.

**Literature**

- [remediation] PostgreSQL Documentation — Explicit Locking — §13.3 Explicit Locking — focus on §13.3.3 Deadlocks (the wait-for graph, victim selection, and the canonical-acquisition-order guidance) and skim §13.3.2 Row-Level Locks for FOR UPDATE semantics. — ~30m
- [remediation] Designing Data-Intensive Applications — Ch. 7 §Preventing Lost Updates, specifically the subsection on Explicit Locking (pp. 242–246) and the surrounding discussion of pessimistic vs. optimistic concurrency control. — ~45m

</small>
</details>

<details>
<summary><samp>q2 · data-engineering · change-data-capture · pre 3 → post 3 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A retail company is replacing nightly batch dumps from their orders OLTP database into the warehouse with a continuous pipeline. They're choosing between (i) a periodic SELECT-based extract using `updated_at > last_high_watermark`, and (ii) log-based CDC reading the database's write-ahead log via Debezium. Explain the mechanism difference (what each approach reads and from where), and walk through three concrete failure modes the timestamp-watermark approach has that log-based CDC does not — at minimum cover: rows updated within the same second as the watermark cutoff, hard deletes, and transactions that commit out of order relative to their `updated_at` assignment. Then name what new operational concerns log-based CDC introduces in exchange.

 

**Assessment:** The answer correctly diagnosed all three watermark failure modes and unified them under the right root cause — that wall-clock timestamps are not authoritative for commit-ordering — and the refinement reached for a substrate-level analogy (inbox/outbox, state transitions logged for failover) that points at the right idea. But when the refinement directly probed for the specific WAL artifact and its failover-survival mechanism, the answer stayed at analogy with explicit terminology hedging ('a WAL or something like that', 'hashed keys I am assuming') rather than committing canonical primitives. The gap is in the named ordering token within the WAL, the durable consumer-position artifact, the failover reconciliation handle, and the operational concerns the question explicitly requested — none of which were surfaced.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 11 §Change Data Capture, pp. 454–457 — covers CDC mechanism, log-as-source-of-truth, and commit-order vs row-state distinction — ~45m
- [remediation] Debezium PostgreSQL Connector Documentation — §How the connector works → Replication slots, and §Failover and replication slots — focused subsection on LSN persistence, slot retention, and timeline_id reconciliation — ~30m

</small>
</details>

<details>
<summary><samp>q3 · ml-engineering · feature-scaling · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A team is training two models on the same tabular dataset of customer features (age in years, account_balance in dollars ranging 0–10M, num_logins_last_week 0–500): a logistic regression with L2 regularization, and a gradient-boosted tree model (XGBoost). The data scientist applies StandardScaler to features before both. Explain (a) why feature scaling materially changes the logistic regression's behaviour — be specific about which part of the loss function or optimization is affected, (b) why the same scaling has essentially no effect on the XGBoost model's predictions, and (c) one case where scaling would still matter for a tree-based pipeline. Commit to whether you'd keep or remove the scaler from the XGBoost training script and justify.

 

**Assessment:** The answer correctly partitioned 'LR is affected, XGBoost is not' but substituted invented framing (float-precision, deterministic data structure, clamping into bucketed nodes) for the two gating mechanisms — the L2 penalty's uniform coupling to coefficient magnitudes for logistic regression, and the rank-ordering property of greedy split selection for tree models. The refinement probe pointed directly at the tree-split mechanism and the response moved further from it rather than toward it, introducing unrelated 'drift mitigation' language. The (c) exception cited latency, which is an operational rather than modeling concern; the canonical exception (distance-based features feeding into a tree, or linear leaves with regularization) was not surfaced, and the keep/remove commit was conditioned on the wrong axis.

**Literature**

- [remediation] An Introduction to Statistical Learning (with Applications in Python), 2nd ed. — Ch. 6 §6.2.1 'Ridge Regression' (pp. 237–242) and Ch. 8 §8.1 'The Basics of Decision Trees' (pp. 327–338) — focused chapter on the missing mechanisms — ~2h 15m
- [remediation] Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow, 3rd ed. — Ch. 2 §'Feature Scaling and Transformation' and Ch. 6 §'The CART Training Algorithm' — chapter coverage of when scaling matters in tree pipelines — ~1h 30m

</small>
</details>

<details>
<summary><samp>q4 · frontend · useeffect-dependency-array · pre 2 → post 3 · ceiling b1 · transitional b3</samp></summary>

<small>

 

**Scenario:** A React component fetches search results based on a `query` prop:

```
useEffect(() => {
  fetch(`/search?q=${query}`)
    .then(r => r.json())
    .then(data => setResults(data));
}, [query]);
```

Users report that when they type quickly, the displayed results sometimes don't match the current query — older results 'win' over newer ones. Explain (a) the mechanism by which this race occurs (be precise about what useEffect does on each `query` change and the ordering of fetch resolutions), (b) why simply debouncing the input reduces but does not eliminate the bug, and (c) commit to a fix using the effect cleanup function and explain what invariant your fix guarantees about which `setResults` call wins.

 

**Assessment:** The answer framed the race as generalized 'input-to-render latency' rather than the specific mechanism: out-of-order resolution of fetch promises launched by successive effect invocations. Under refinement, the answerer reached the correct primitive family (a flag determining whether the in-flight fetch is still intended) but misplaced it as a dependency-array entry rather than a closure variable flipped by the effect's cleanup return. The gap is in where the cancellation flag lives in the effect's lifecycle and what invariant the cleanup contract guarantees — and the related modern alternative that cancels the request itself rather than just ignoring its response.

**Literature**

- [remediation] Synchronizing with Effects — §Fetching data — the 'let ignore = false ... return () => { ignore = true; }' pattern and the surrounding 'Each effect synchronizes with one render' framing (focused chapter for B3) — ~25m
- [remediation] A Complete Guide to useEffect — Sections 'Each Render Has Its Own Effects' and 'Each Render Has Its Own… Everything' through 'So What About Cleanup?' (focused chapter for B3) — ~45m

</small>
</details>

<details>
<summary><samp>q5 · systems-distributed · fan-out-on-write-vs-read · pre 3 → post 4 · ceiling b3 · transitional b4</samp></summary>

<small>

 

**Scenario:** A social-media product is designing the timeline service. Two architectures are on the table: (1) fan-out-on-write — when a user posts, the post id is pushed into a precomputed timeline list for every follower; timeline reads are a single lookup. (2) fan-out-on-read — posts are stored once; a timeline read queries posts from all followed users and merges them. Explain the read-cost vs write-cost tradeoff each makes (be concrete about what 'write amplification' means in approach 1), why approach 1 collapses under a user with 50M followers (the 'celebrity problem'), and commit to a hybrid design that handles the celebrity case. Be specific about which users get which treatment and how the timeline read merges the two sources.

 

**Assessment:** Pre-refinement the answer identified the cost asymmetry and committed to a hybrid but did not specify how the two sources combine at read time — the central B3 mechanism gap. The refinement closed most of the gap: the answerer named ordering primitives (monotonics, hybrid clocks), described the merge shape, and layered a cache plus idempotent upsert pipeline. What remains missing is the canonical ordering primitive that turns the merge from an O(N) scan-and-insert into a bounded k-way merge over already-sorted streams, plus dismissal of alternatives on a tradeoff axis and operational-hazard framing (threshold oscillation, per-celebrity tail-latency contract).

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 1 §Describing Load — Twitter timeline case study (pp. 11–14) — ~30m
- [growth] Announcing Snowflake — k-sortable id design — Connection: the answer's 'attach monotonics/hybrid clocks and scan O(N) to insert' is the right instinct; Snowflake-style k-sortable ids ((timestamp, machine_id, seq)) make the cross-source merge a true k-way merge over already-sorted streams, eliminating the O(N) insertion-sort framing. — ~20m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
