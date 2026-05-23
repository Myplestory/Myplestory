

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
q2  ai-llm             embedding-cache         ₃   2   ₂
q3  frontend           browser-event-loop      ₂   2   ₁
q4  ml-engineering     auc-vs-pr-curve-under   ₁   1   ₁
q5  backend            postgres-mvcc-bloat     ₂   2   ₂

gaps         auc-vs-pr-curve-under-imbalance · browser-event-loop-microtask-macrotask · embedding-cache-invalidation · fencing-token-monotonicity

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · systems-distributed · leader-lease-expiry · pre 2 → post 2 · ceiling — · transitional b1–b2</samp></summary>

<small>

 

**Scenario:** A coordination service issues 30-second leases to designate one node as the 'primary writer' for a shared key-value store. The shared store accepts any write that arrives with a current lease ID. During an incident, the primary writer experienced a 45-second stop-the-world GC pause, then resumed and immediately wrote to the store using what it believed was its valid lease — but by then the coordination service had granted the lease to a new primary, and the new primary had already written. Both writes were accepted; the second writer's data was silently overwritten by the first. Explain the mechanism that caused this failure. Then describe what the shared store would need to do (and what the lease service would need to issue) to make this class of bug impossible. Be specific about why simply shortening the lease TTL to 5 seconds does not fix it.

 

**Refinement:** You said 'shared state as i already explained needs the metadata'. Clarify: what specific property of that metadata forces the store to reject a write from a node whose lease epoch is lower than the last accepted write's epoch, even if the writing node believes its lease is current?

 

**Assessment:** The question targeted recognition of the canonical fencing-token pattern: a monotonic epoch issued with each lease, enforced storage-side atomically with the write. The response identified the right problem family (stale-write after pause) and the right failure surface (the store accepted a write it should have rejected), but reached for an event-sourcing/reconciliation primitive instead of the storage-side monotonic-token primitive. The refinement probe explicitly asked what property of the metadata forces the store to reject a lower-epoch write; the answer responded with provenance, election-membership, and Byzantine fault tolerance — escalating to a heavier primitive class rather than naming monotonicity and storage-side enforcement. The gap is in recognizing that the store, not the client, must be the enforcement point, and that the enforcement is a single atomic compare-and-write on a token, not a reconciliation protocol.

**Literature**

- [remediation] How to do distributed locking — Sections 'Is Redlock safe?' through 'Making the lock safe with fencing' — the diagram showing client 1 pausing, lease expiring, client 2 acquiring, and the store rejecting client 1's late write because its fencing token is lower than client 2's — ~25m
- [remediation] Designing Data-Intensive Applications — Ch. 8 §Process Pauses (pp. 295–299) and §The Truth Is Defined by the Majority — 'Fencing tokens' (pp. 301–304) — ~1h 15m

</small>
</details>

<details>
<summary><samp>q2 · ai-llm · embedding-cache-invalidation · pre 2 → post 2 · ceiling b1 · transitional b2</samp></summary>

<small>

 

**Scenario:** A documentation-search RAG system caches embeddings for ~2 million corpus chunks in a vector store. The team upgrades from embedding model v1 (768-dim) to embedding model v2 (1536-dim, different training corpus, better recall on technical queries). They want to deploy v2 without a 12-hour full-corpus re-embedding job blocking the rollout. A junior engineer proposes: 'Just re-embed lazily — when a chunk is retrieved by v1 and ranked low, re-embed it with v2 and overwrite the entry.' Explain why this proposal is broken at the retrieval level (not just operationally). Then commit to a deployment strategy that handles the transition correctly, and name what the cache key for an embedding entry must include to prevent this entire class of bug from recurring on future model upgrades.

 

**Refinement:** You said 'The ideal balance for this task would be (if allowed) to 1) slowly embed away from the original db'. Clarify: how does query routing work during the transition period when v1 and v2 indexes coexist — specifically, what property of a query result from each index makes them incomparable, and how does your strategy avoid returning a mixed ranking to the user?

 

**Assessment:** The question's mechanism gate is naming why v1 and v2 embeddings are incomparable at the retrieval level — specifically the dimensionality mismatch (768 vs 1536 cannot share an ANN index) and the vector-space non-alignment between independently trained bi-encoders, so similarity scores across the two are not on the same scale. The response identifies that mixing is bad and reaches for 'contamination' as a metaphor, but never names the geometric property, never commits to a concrete deployment shape, and never enumerates what the cache key must contain. The refinement probe targeted exactly the missing primitive ('what property makes the results incomparable') and the answer remained at the metaphor level while deferring the deployment commitment to 'operators'. The gap is in the bi-encoder retrieval contract and the model-version cache-key invariant.

**Literature**

- [remediation] Sentence-Transformers: Semantic Search & Bi-Encoder Retrieval — Semantic Search §'Background' and §'Symmetric vs. Asymmetric Semantic Search' — the bi-encoder contract: query and corpus embeddings must come from the same model to be comparable in the shared vector space — ~25m
- [remediation] Designing Data-Intensive Applications — Ch. 4 §'Schema Evolution' and Ch. 11 §'Reprocessing Data for Application Evolution', pp. 111–128 and pp. 461–467 — dual-write / dual-read patterns and the derived-data reprocessing playbook that maps directly onto v1/v2 index cutover — ~1h 15m

</small>
</details>

<details>
<summary><samp>q3 · frontend · browser-event-loop-microtask-macrotask · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A dashboard renders 200 widgets on mount. Each widget calls `fetch('/api/widget/' + id)` in a `useEffect`, and on resolution calls `setState` to update that widget's data. Users report that during the initial load, clicking buttons or scrolling feels frozen for 2-3 seconds even though the network tab shows responses arriving spread out over time. The team's first instinct is 'we need to debounce setState' — explain why that diagnosis misidentifies the mechanism. Then explain what is actually consuming the main thread in that window, distinguishing between microtasks and macrotasks in the browser event loop, and describe what concretely changes about scheduling if the team wraps each `setState` call in `startTransition` versus if they batch the fetches into chunks of 20 with a `setTimeout(0)` between chunks. Which actually restores input responsiveness and why?

 

**Refinement:** You said 'the main loop is blocked, hence the 2-3 sec when microtasks are not partitioned/designed thoughtfully and result is propogation of execution pressure through blocks'. Clarify: what specifically in the browser event loop's ordering rules causes a flood of resolved Promise callbacks to prevent input events from being processed, and how does that differ from a macrotask blocking the same loop?

 

**Assessment:** The diagnosis hinges on a specific event-loop ordering rule that the answer never names, despite the refinement probe targeting it directly. The response uses microtask/macrotask vocabulary but inverts the roles — describing the main loop as a macrotask that delegates work via microtasks, and the refinement compounds this by claiming event-loop slots are 'allocated at compile'. The two mitigation mechanisms (startTransition vs setTimeout(0) chunking) are both endorsed without committing to which actually breaks the flood and why, leaving the central B3 'why is this mechanism sufficient' question unanswered. The gap is in the HTML spec event-loop algorithm and how React 18's concurrent renderer interacts with it.

**Literature**

- [remediation] In The Loop (JSConf.Asia) — Full talk (~35 min) — the canonical visual explanation of how the HTML spec event loop runs one task, drains all microtasks to empty, then renders/handles input, and exactly how promise floods starve input. — ~35m
- [remediation] React Docs — useTransition & Concurrent Rendering — useTransition reference page + linked 'React 18 release notes — Concurrent Rendering' section on interruptibility (https://react.dev/blog/2022/03/29/react-v18). Read together as one focused chapter on why startTransition makes renders yield to input. — ~45m

</small>
</details>

<details>
<summary><samp>q4 · ml-engineering · auc-vs-pr-curve-under-imbalance · pre 1 → post 1 · ceiling —</samp></summary>

<small>

 

**Scenario:** A team is building a binary classifier for detecting fraudulent insurance claims. Base rate is 0.3% positive. Their first model achieves AUC-ROC of 0.94 on a held-out set, which the PM calls 'excellent.' The deployed model, used at a fixed decision threshold of 0.5, flags only 8% of true fraud cases (recall = 0.08) while producing a precision of 62%. The PM is confused: 'how can AUC be 0.94 if we're catching almost no fraud?' Explain to the PM what AUC-ROC actually measures, why it can look strong on heavily imbalanced data while the deployed model performs poorly, and what specific metric and visualization you would use instead to (a) compare models during development and (b) choose the operating threshold given a business constraint of 'we can manually review at most 500 flagged claims per day out of ~40,000 daily claims.'

 

**Refinement:** You said 'AUC-ROC measures convergence on a designated metric, not a overall'. Clarify: what two axes are being integrated over to produce the AUC-ROC score, and why those axes make the metric insensitive to class imbalance?

 

**Assessment:** The answer does not satisfy the B3 mechanism invariant for ml-engineering: it never identifies the production-ML concern (a ranking metric being misread as an operating-point metric) and never names the standard primitives — TPR/FPR as the AUC-ROC axes, the FPR-denominator argument for why low base rate inflates AUC, the PR curve / average precision for development comparison, or precision@k for the capacity-constrained threshold. The refinement probe directly named 'the two axes' and asked for the imbalance-insensitivity mechanism; the response explicitly declined the axes and substituted invented vocabulary. The gap is at the level of standard vocabulary and the canonical decomposition of a ranking-vs-operating-point question.

**Literature**

- [remediation] Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (3rd ed.) — Chapters 2–4 (end-to-end ML project; classification — precision, recall, F1, ROC curve, ROC AUC; training models — learning curves). Read these three chapters together; the gap is foundational vocabulary for classification metrics and threshold selection. — ~25h
- [remediation] The Relationship Between Precision-Recall and ROC Curves — §3 'ROC and PR' and §4 'Theorem 3.2' — the formal demonstration that PR curves give a more informative picture than ROC curves when the negative class is large, which is the exact 0.3%-base-rate scenario in the question. — ~1h

</small>
</details>

<details>
<summary><samp>q5 · backend · postgres-mvcc-bloat · pre 2 → post 2 · ceiling —</samp></summary>

<small>

 

**Scenario:** A Postgres-backed service has a nightly analytics job that opens a single transaction, runs a series of large read-only `SELECT` queries against several core tables (`orders`, `users`, `events`), and commits about 90 minutes later. Over the past two months, performance on those same tables during the day has degraded: query latency has roughly doubled, and `pg_stat_user_tables` shows `n_dead_tup` climbing into the tens of millions on `orders` even though `autovacuum` is running on schedule and completing without errors. Explain the mechanism connecting the nightly read-only transaction to the daytime degradation. Why doesn't autovacuum reclaim the dead tuples it visits? What concretely would you change about the analytics job to fix this, and what tradeoff does that change impose on the analytics workload itself?

 

**Refinement:** You said 'the autovaccum cant reclaim the dead tuples, how can it when the query latency is just cascading and causes incoherence'. Clarify: what specific internal Postgres bookkeeping value does the long-running transaction hold in place, and how does that value determine which dead tuples autovacuum is permitted to remove?

 

**Assessment:** The answer correctly identifies that the nightly transaction is the cause and that autovacuum is somehow prevented from doing its job, but mis-locates the mechanism in row-level locking rather than in MVCC snapshot visibility. The refinement probe pointed directly at the relevant internal bookkeeping value, and the response moved further from the Postgres model — into driver-level locks, futures, and cache-line concerns — rather than naming the snapshot/xmin horizon. The fix proposal (snapshot the data, isolate phases) has the right shape directionally but is not grounded in what actually pins the horizon, and the named tradeoff (atomicity, fail-closed) is not the tradeoff this fix imposes (loss of cross-query point-in-time consistency).

**Literature**

- [remediation] PostgreSQL Documentation — Chapter 13: Concurrency Control — Ch. 13 §13.1 Introduction and §13.2 Transaction Isolation — read in full to establish that Postgres uses MVCC (not lock-based concurrency for reads), that each transaction sees a snapshot fixed at a defined point, and that readers do not block writers. — ~45m
- [remediation] PostgreSQL Documentation — Routine Vacuuming — Ch. 25 §25.1 Routine Vacuuming — specifically §25.1.5 'Preventing Transaction ID Wraparound Failures' and the surrounding discussion of OldestXmin / removable cutoff; pair with §13.3 to see how a running transaction's xmin holds the horizon. — ~30m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
