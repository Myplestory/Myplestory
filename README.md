

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
<summary><samp>fortifai · self-audit loop · streak 4d</samp></summary>

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
q5  systems-distributedfan-out-on-write-vs     ₄   3   ₃

gaps         deadlock-detection · feature-scaling · lock-ordering · regularization-sensitivity-to-scale

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · backend · deadlock-detection · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A payments service runs in PostgreSQL. Two endpoints each take a balance transfer: endpoint A locks account row X then Y (SELECT ... FOR UPDATE in that order), endpoint B locks Y then X. Under load, you see periodic transactions failing with 'deadlock detected' and being rolled back by Postgres after roughly 1 second. A junior engineer proposes increasing `deadlock_timeout` to 10s so 'the deadlocks have time to resolve themselves.' Explain (a) the mechanism by which Postgres detects this deadlock and what happens to the loser transaction, (b) why the junior's proposal does not eliminate deadlocks and what it actually changes, and (c) what structural fix removes the deadlock class entirely and why it works. Be concrete about what 'lock ordering' means at the row level when the two accounts are not known until query time.

 

**Assessment:** The answer correctly identified the failure domain (deadlock via cycle in a lock-dependency graph) and rightly dismissed the junior's timeout proposal as post-hoc rather than preventive. However, the structural fix proposed — CQRS/materialized views — addresses a read-path concern, while the question is about two concurrent writes contending for row-level locks on the same accounts in opposing orders. The refinement probe directly asked how materialization would prevent conflicting WRITE-lock acquisition, and the response did not recognize the category error: materialized views do not participate in the row-level write locks on base tables that produced the cycle. The gap is the specific primitive that makes a wait-for cycle structurally impossible on the write path when the two row identities are only known at query time.

**Literature**

- [remediation] PostgreSQL Documentation — Explicit Locking — §13.3 Explicit Locking, especially §13.3.3 Deadlocks — focused read on the canonical lock-ordering recommendation and the wait-for graph detection mechanism — ~25m
- [remediation] Designing Data-Intensive Applications — Ch. 7 §Preventing Lost Updates → Explicit locking (pp. 242–246) — focused chapter on when pessimistic row-level locking is the right primitive and the operational hazards (deadlock among them) it introduces — ~35m

</small>
</details>

<details>
<summary><samp>q2 · data-engineering · change-data-capture · pre 3 → post 3 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A retail company is replacing nightly batch dumps from their orders OLTP database into the warehouse with a continuous pipeline. They're choosing between (i) a periodic SELECT-based extract using `updated_at > last_high_watermark`, and (ii) log-based CDC reading the database's write-ahead log via Debezium. Explain the mechanism difference (what each approach reads and from where), and walk through three concrete failure modes the timestamp-watermark approach has that log-based CDC does not — at minimum cover: rows updated within the same second as the watermark cutoff, hard deletes, and transactions that commit out of order relative to their `updated_at` assignment. Then name what new operational concerns log-based CDC introduces in exchange.

 

**Assessment:** The answer correctly diagnosed all three timestamp-watermark failures by attributing them to a single underlying cause — timestamps are not an authoritative ordering primitive — and gestured at log-based replication as the resolution. The gap is at the canonical-primitive layer: which specific artifact in the write-ahead log carries the ordering guarantee, and what database-side construct keeps a consumer's position durable across failover. The refinement explicitly probed this and the answer remained at the analogy level ('WAL or something like that', 'similar to inbox/outbox', 'hashed keys I am assuming') rather than naming the primitive. Closing this gap means learning the named vocabulary (sequence-number-as-position, slot-as-durable-cursor, timeline-as-failover-discriminator) and the operational consequences each one introduces.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 11 §Change Data Capture, pp. 454–457 — covers log-based replication, commit-order vs assignment-order, and why CDC observes the database's authoritative ordering rather than a derived timestamp — ~45m
- [remediation] Debezium PostgreSQL Connector Documentation — §How the connector works → Replication Slots, §Snapshots, §Failure handling — the specific WAL artifact (LSN), the durability mechanism (replication slot), and timeline_id reconciliation on promotion — ~1h

</small>
</details>

<details>
<summary><samp>q3 · ml-engineering · feature-scaling · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A team is training two models on the same tabular dataset of customer features (age in years, account_balance in dollars ranging 0–10M, num_logins_last_week 0–500): a logistic regression with L2 regularization, and a gradient-boosted tree model (XGBoost). The data scientist applies StandardScaler to features before both. Explain (a) why feature scaling materially changes the logistic regression's behaviour — be specific about which part of the loss function or optimization is affected, (b) why the same scaling has essentially no effect on the XGBoost model's predictions, and (c) one case where scaling would still matter for a tree-based pipeline. Commit to whether you'd keep or remove the scaler from the XGBoost training script and justify.

 

**Assessment:** The question tests two named mechanisms: how L2 regularization couples to feature scale in logistic regression, and which property of tree split selection makes magnitude irrelevant in XGBoost. The original response substituted 'floating-point precision and determinism' for both mechanisms — a domain misidentification. The refinement narrowed in on the tree-split property specifically, and the follow-up answered with 'bucketed nodes and clamping', which describes that trees produce discrete partitions but does not identify the property under test. The gap is at the level of the underlying primitives, not articulation: the canonical body-of-knowledge concepts for both halves of the question were never produced.

**Literature**

- [remediation] An Introduction to Statistical Learning (2nd ed.) — Ch. 6 §6.2 'Shrinkage Methods' (esp. §6.2.1 Ridge Regression — note on standardizing predictors) and Ch. 8 §8.1 'The Basics of Decision Trees' (split selection) — ~1h 30m
- [remediation] Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (3rd ed.) — Ch. 2 §'Feature Scaling and Transformation' and Ch. 6 §'Decision Trees' — together cover when scaling is required vs. a no-op, and the canonical exception (distance-based features feeding into a tree pipeline) — ~1h

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

 

**Assessment:** The response framed the race as cumulative input-to-render latency rather than as out-of-order resolution of overlapping in-flight fetches, so part (a) missed the ordering mechanism. Part (b) asserted that debouncing 'bounds but doesn't solve' without articulating the resumed-typing case that re-opens the window. The refinement nudged the answerer toward a staleness flag, but the flag was placed in the dependency array rather than as a closure variable flipped by the effect's cleanup return, and the invariant about which setResults call wins was never stated. The gap is in how React's per-render effect identity and cleanup-before-next-effect ordering combine to neutralize stale closures.

**Literature**

- [remediation] Synchronizing with Effects — §'Fetching data' — the verbatim `let ignore = false ... return () => { ignore = true; }` cancellation pattern, plus the surrounding §'How to handle the Effect firing twice in development' and §'Each render has its own Effects' subsections to ground the closure-per-render mental model — ~25m
- [remediation] A Complete Guide to useEffect — §'Each Render Has Its Own Effects' and §'Each Render Has Its Own… Everything' — establishes that the effect body, its variables, and its cleanup all close over a specific render's `query`, which is the invariant the cancellation flag relies on — ~35m

</small>
</details>

<details>
<summary><samp>q5 · systems-distributed · fan-out-on-write-vs-read · pre 3 → post 3 · ceiling b2 · transitional b4</samp></summary>

<small>

 

**Scenario:** A social-media product is designing the timeline service. Two architectures are on the table: (1) fan-out-on-write — when a user posts, the post id is pushed into a precomputed timeline list for every follower; timeline reads are a single lookup. (2) fan-out-on-read — posts are stored once; a timeline read queries posts from all followed users and merges them. Explain the read-cost vs write-cost tradeoff each makes (be concrete about what 'write amplification' means in approach 1), why approach 1 collapses under a user with 50M followers (the 'celebrity problem'), and commit to a hybrid design that handles the celebrity case. Be specific about which users get which treatment and how the timeline read merges the two sources.

 

**Assessment:** The answer correctly identifies write amplification, the celebrity collapse, and commits to a follower-count-threshold hybrid. The refinement supplies the right shape of read-time stitch — fetch precomputed timeline, merge in celebrity posts using an ordering primitive, with a cache + idempotent upsert pipeline behind it. The gap is at the canonical primitive: the response names 'monotonics, hybrid clocks, etc' as a family rather than committing to the specific k-sortable id scheme (snowflake, or composite (timestamp, post_id)) that makes the cross-source merge a true k-way merge without coordination. Operational hazards a proficient practitioner would surface — threshold oscillation, tail-latency SLI under celebrity read amplification — are not named.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 1 §Describing Load — Twitter timeline case study (pp. 11–14); Ch. 9 §Ordering Guarantees — Lamport Timestamps and k-sortable ids (pp. 339–352) — ~1h 30m
- [remediation] Announcing Snowflake — Full post — Snowflake id structure (timestamp-prefixed 64-bit ids) and the k-sortable property — ~15m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
