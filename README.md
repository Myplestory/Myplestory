

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
<summary><samp>fortifai · self-audit loop · streak 3d</samp></summary>

<sub><samp><i>self-audit: scenario-based time-pressured recall, cross-domain breadth, b3-calibrated<br>
invariant: zero outside assistance. no docs, no ai, no peers. 10m/response, 5m/single refinement<br>
breadth: systems/distributed, backend, sre, ml, ai/llm, frontend, data, security<br>
bar: consistent ≥3 across all 8 swe fields</i></samp></sub>

```
industry     swe                                  updated         2026-05-23
scope        cross-domain · grab-bag              duration        1h 6m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  systems-distributedleader-lease-expiry     ₃   2   ₂
q2  ai-llm             embedding-cache         ₃   2   ₁
q3  frontend           browser-event-loop      ₂   1   ₁
q4  ml-engineering     auc-vs-pr-curve-under   ₁   1   ₁
q5  backend            postgres-mvcc-bloat     ₂   1   ₁

gaps         auc-vs-pr-curve-under-imbalance · browser-event-loop-microtask-macrotask · embedding-cache-invalidation · fencing-token-monotonicity

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · systems-distributed · leader-lease-expiry · pre 2 → post 2 · ceiling — · transitional b1–b2</samp></summary>

<small>

 

**Scenario:** A coordination service issues 30-second leases to designate one node as the 'primary writer' for a shared key-value store. The shared store accepts any write that arrives with a current lease ID. During an incident, the primary writer experienced a 45-second stop-the-world GC pause, then resumed and immediately wrote to the store using what it believed was its valid lease — but by then the coordination service had granted the lease to a new primary, and the new primary had already written. Both writes were accepted; the second writer's data was silently overwritten by the first. Explain the mechanism that caused this failure. Then describe what the shared store would need to do (and what the lease service would need to issue) to make this class of bug impossible. Be specific about why simply shortening the lease TTL to 5 seconds does not fix it.

 

**Refinement:** You said 'shared state as i already explained needs the metadata'. Clarify: what specific property of that metadata forces the store to reject a write from a node whose lease epoch is lower than the last accepted write's epoch, even if the writing node believes its lease is current?

 

**Assessment:** The response identifies the failure domain (stale-leader writes under self-undetectable pause) but commits to the wrong primitive when directly probed: client-side reconciliation with provenance/chain-of-custody metadata, rather than storage-side monotonic enforcement atomic with the write. The refinement narrowed the question to exactly the property that must hold at the store, and the answer escalated into Byzantine-fault-tolerance territory — a category error, since the scenario is crash-stop with a paused node that cannot detect its own suspension. The gap is in recognizing that the load-bearing change is store-side, not client-side: the paused node, by definition, cannot reconcile before writing because it does not know it was paused. The TTL-magnitude argument is also imprecise — the reason short TTL does not fix the class is that pause duration is unbounded in principle, not that TTL introduces a cache-coherency surface.

**Literature**

- [remediation] How to do distributed locking — §'Making the lock safe with fencing' — the GC-pause diagram and the storage-side reject-if-token-less-than-max rule — ~25m
- [remediation] Designing Data-Intensive Applications — Ch. 8 §'Process Pauses' (pp. 295–299) and §'The Truth Is Defined by the Majority — Fencing tokens' (pp. 301–304) — ~2h

</small>
</details>

<details>
<summary><samp>q2 · ai-llm · embedding-cache-invalidation · pre 2 → post 2 · ceiling — · transitional b1–b2</samp></summary>

<small>

 

**Scenario:** A documentation-search RAG system caches embeddings for ~2 million corpus chunks in a vector store. The team upgrades from embedding model v1 (768-dim) to embedding model v2 (1536-dim, different training corpus, better recall on technical queries). They want to deploy v2 without a 12-hour full-corpus re-embedding job blocking the rollout. A junior engineer proposes: 'Just re-embed lazily — when a chunk is retrieved by v1 and ranked low, re-embed it with v2 and overwrite the entry.' Explain why this proposal is broken at the retrieval level (not just operationally). Then commit to a deployment strategy that handles the transition correctly, and name what the cache key for an embedding entry must include to prevent this entire class of bug from recurring on future model upgrades.

 

**Refinement:** You said 'The ideal balance for this task would be (if allowed) to 1) slowly embed away from the original db'. Clarify: how does query routing work during the transition period when v1 and v2 indexes coexist — specifically, what property of a query result from each index makes them incomparable, and how does your strategy avoid returning a mixed ranking to the user?

 

**Assessment:** The response correctly senses that v1 and v2 embeddings cannot coexist in one index and that lazy overwrite corrupts retrieval, but never names the property that makes them incomparable — the dimensionality mismatch is the most concrete signal in the scenario (768 vs 1536) and is not mentioned, and the more general bi-encoder vector-space property is described only by metaphor. The refinement probe asked for that property directly and was answered with the same metaphor. The deployment strategy is enumerated as axes to weigh rather than committed to a shape, and the cache-key answer — the part the question explicitly required — is deferred to operator judgement rather than specified as a composite of identifiers. The gap is in naming the retrieval-layer mechanism and committing to the cache-key composition that prevents recurrence.

**Literature**

- [remediation] Semantic Search with Sentence-Transformers — Semantic Search §'Symmetric vs. Asymmetric Semantic Search' and §'Manual Implementation' — the requirement that query and corpus be encoded by the same model for cosine/dot-product scores to be meaningful, plus the dimensionality contract of the index — ~25m
- [remediation] Designing Data-Intensive Applications — Ch. 11 §'Reprocessing Data for Application Evolution', pp. 461–467 — the derived-data reprocessing pattern: build new derived dataset alongside old, validate, atomically cut over — ~1h 30m

</small>
</details>

<details>
<summary><samp>q3 · frontend · browser-event-loop-microtask-macrotask · pre 2 → post 1 · ceiling —</samp></summary>

<small>

 

**Scenario:** A dashboard renders 200 widgets on mount. Each widget calls `fetch('/api/widget/' + id)` in a `useEffect`, and on resolution calls `setState` to update that widget's data. Users report that during the initial load, clicking buttons or scrolling feels frozen for 2-3 seconds even though the network tab shows responses arriving spread out over time. The team's first instinct is 'we need to debounce setState' — explain why that diagnosis misidentifies the mechanism. Then explain what is actually consuming the main thread in that window, distinguishing between microtasks and macrotasks in the browser event loop, and describe what concretely changes about scheduling if the team wraps each `setState` call in `startTransition` versus if they batch the fetches into chunks of 20 with a `setTimeout(0)` between chunks. Which actually restores input responsiveness and why?

 

**Refinement:** You said 'the main loop is blocked, hence the 2-3 sec when microtasks are not partitioned/designed thoughtfully and result is propogation of execution pressure through blocks'. Clarify: what specifically in the browser event loop's ordering rules causes a flood of resolved Promise callbacks to prevent input events from being processed, and how does that differ from a macrotask blocking the same loop?

 

**Assessment:** The answer identifies the symptom surface (main thread, microtasks, render blocking) but does not engage with the actual event-loop ordering rule that the scenario hinges on, and the refinement made this worse by introducing a fabricated 'compile-time slot allocation' model that has no basis in the HTML spec or any browser implementation. The recommendation prioritizes the wrong primitive between the two offered fixes and declines to dismiss either, which would mislead a team about which lever actually moves input responsiveness. The gap is in the precise spec-level rule governing when microtask queues are drained relative to input event dispatch and rendering, and how fetch-initiation cadence drives resolution cadence which drives that drain.

**Literature**

- [remediation] Tasks, microtasks, queues and schedules — Full article — read end-to-end. The canonical, illustrated reference for the exact rule the refinement probe targeted: promise callbacks queue as microtasks, the microtask queue drains to empty before the next macrotask, and macrotasks (including input/scroll dispatch and rendering opportunities) cannot interleave with a long microtask drain. Includes the worked example of a setTimeout vs Promise.resolve ordering test that disambiguates the two queues. — ~30m
- [remediation] HTML Living Standard §8.1.6.3 — Event loop processing model — §8.1.6.3 'Processing model' — read steps 1 (run oldest task), 6 (microtask checkpoint), and 11 (rendering opportunity). The normative source for why a flood of resolved promises starves both input dispatch and paint: rendering is step 11, after the microtask checkpoint at step 6 has drained the queue to empty. — ~20m

</small>
</details>

<details>
<summary><samp>q4 · ml-engineering · auc-vs-pr-curve-under-imbalance · pre 1 → post 1 · ceiling —</samp></summary>

<small>

 

**Scenario:** A team is building a binary classifier for detecting fraudulent insurance claims. Base rate is 0.3% positive. Their first model achieves AUC-ROC of 0.94 on a held-out set, which the PM calls 'excellent.' The deployed model, used at a fixed decision threshold of 0.5, flags only 8% of true fraud cases (recall = 0.08) while producing a precision of 62%. The PM is confused: 'how can AUC be 0.94 if we're catching almost no fraud?' Explain to the PM what AUC-ROC actually measures, why it can look strong on heavily imbalanced data while the deployed model performs poorly, and what specific metric and visualization you would use instead to (a) compare models during development and (b) choose the operating threshold given a business constraint of 'we can manually review at most 500 flagged claims per day out of ~40,000 daily claims.'

 

**Refinement:** You said 'AUC-ROC measures convergence on a designated metric, not a overall'. Clarify: what two axes are being integrated over to produce the AUC-ROC score, and why those axes make the metric insensitive to class imbalance?

 

**Assessment:** The answer did not identify the scenario as a metric-selection and operating-point problem: AUC-ROC was not defined, the role of the negative-class denominator under a 0.3% base rate was not articulated, and no alternative development-time curve or capacity-derived threshold was proposed. The refinement probe asked directly for the two axes of AUC-ROC and the answerer acknowledged not knowing them, then substituted a non-standard 'convergence/coherence' framing. The business constraint (500 reviews out of 40,000 daily claims) was rejected rather than translated into an operating-point derivation, and the proposed remediation (multi-threshold ensembling with deterministic fusion) misroutes the problem from threshold selection to model architecture.

**Literature**

- [remediation] Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow (3rd ed.) — Ch. 3 'Classification' — full chapter: confusion matrix, precision/recall, the precision/recall trade-off, the ROC curve, and the ROC vs PR curve guidance for imbalanced data — ~2h 30m
- [remediation] The Relationship Between Precision-Recall and ROC Curves — §3–4 — the proof that a curve dominates in ROC iff it dominates in PR space, and the explicit account of why ROC underweights false positives when negatives dominate; ~10 pages — ~3h

</small>
</details>

<details>
<summary><samp>q5 · backend · postgres-mvcc-bloat · pre 2 → post 1 · ceiling —</samp></summary>

<small>

 

**Scenario:** A Postgres-backed service has a nightly analytics job that opens a single transaction, runs a series of large read-only `SELECT` queries against several core tables (`orders`, `users`, `events`), and commits about 90 minutes later. Over the past two months, performance on those same tables during the day has degraded: query latency has roughly doubled, and `pg_stat_user_tables` shows `n_dead_tup` climbing into the tens of millions on `orders` even though `autovacuum` is running on schedule and completing without errors. Explain the mechanism connecting the nightly read-only transaction to the daytime degradation. Why doesn't autovacuum reclaim the dead tuples it visits? What concretely would you change about the analytics job to fix this, and what tradeoff does that change impose on the analytics workload itself?

 

**Refinement:** You said 'the autovaccum cant reclaim the dead tuples, how can it when the query latency is just cascading and causes incoherence'. Clarify: what specific internal Postgres bookkeeping value does the long-running transaction hold in place, and how does that value determine which dead tuples autovacuum is permitted to remove?

 

**Assessment:** The response correctly identified the nightly transaction as the trigger and proposed shortening or isolating it, but mis-located the mechanism in row-level locking and 'cascading lock contention,' which the SELECT's lock mode actually precludes. The refinement probe was precise — it asked for the specific internal bookkeeping value the long-running transaction holds — and the answer did not converge on the relevant Postgres concept, instead generating invented details about driver structs, futures, and cache-line memory layout. The gap is in the visibility/reclamation model that governs when vacuum is permitted to remove a dead tuple, and in the lock-mode semantics that rule out the contention hypothesis.

**Literature**

- [remediation] PostgreSQL Documentation — Concurrency Control — Chapter 13: Concurrency Control — §13.1 Introduction to MVCC, §13.2 Transaction Isolation, §13.3 Explicit Locking (focus on §13.3.1 Table-level Locks for AccessShareLock semantics) — ~1h 30m
- [remediation] PostgreSQL Documentation — Routine Vacuuming — Chapter 25 §25.1 Routine Vacuuming — especially §25.1.5 Preventing Transaction ID Wraparound Failures (OldestXmin cutoff) and §25.1.6 The Autovacuum Daemon; cross-reference pg_stat_activity.backend_xmin in the Monitoring chapter — ~45m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
