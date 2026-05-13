

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
q2  data-engineering   change-data-capture     ₃   3   ₂
q3  ml-engineering     feature-scaling         ₂   2   ₁
q4  frontend           useeffect-dependency    ₃   3   ₂
q5  systems-distributedfan-out-on-write-vs     ₃   3   ₂

strengths    fan-out-on-write-vs-read · celebrity-problem · change-data-capture
gaps         feature-scaling · regularization-sensitivity-to-scale · tree-based-vs-linear-scaling · deadlock-detection

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · backend · deadlock-detection · pre 2 → post 2 · ceiling b1 · transitional b2</samp></summary>

<small>

 

**Scenario:** A payments service runs in PostgreSQL. Two endpoints each take a balance transfer: endpoint A locks account row X then Y (SELECT ... FOR UPDATE in that order), endpoint B locks Y then X. Under load, you see periodic transactions failing with 'deadlock detected' and being rolled back by Postgres after roughly 1 second. A junior engineer proposes increasing `deadlock_timeout` to 10s so 'the deadlocks have time to resolve themselves.' Explain (a) the mechanism by which Postgres detects this deadlock and what happens to the loser transaction, (b) why the junior's proposal does not eliminate deadlocks and what it actually changes, and (c) what structural fix removes the deadlock class entirely and why it works. Be concrete about what 'lock ordering' means at the row level when the two accounts are not known until query time.

 

**Assessment:** The response correctly identifies that the junior's proposal is post-hoc handling rather than a structural fix, but the proposed structural fix (CQRS / materialized read views) does not address the actual failure: two concurrent write transactions acquiring row-level locks on the same two rows in opposite orders. Materialized views decouple reads from writes; they do not change the order in which the write path acquires locks. The mechanism the question targets — acquiring locks in a deterministic canonical order (e.g., ORDER BY account_id FOR UPDATE so both endpoints lock min(X,Y) first then max(X,Y)) — is not produced. PostgreSQL's deadlock_timeout is also misframed: it is the interval at which Postgres polls for cycles in the wait-for graph, not a tolerance window.

**Literature**

- [remediation] PostgreSQL Documentation — Explicit Locking — Ch. 13.3 'Explicit Locking' — §13.3.3 Deadlocks (full chapter, ~15 pages) — ~1h 30m
- [remediation] Designing Data-Intensive Applications — Ch. 7 'Transactions' — §Preventing Lost Updates and §Serializability subsections on locking (pp. 242–258) — ~4h

</small>
</details>

<details>
<summary><samp>q2 · data-engineering · change-data-capture · pre 3 → post 3 · ceiling b1 · transitional b3</samp></summary>

<small>

 

**Scenario:** A retail company is replacing nightly batch dumps from their orders OLTP database into the warehouse with a continuous pipeline. They're choosing between (i) a periodic SELECT-based extract using `updated_at > last_high_watermark`, and (ii) log-based CDC reading the database's write-ahead log via Debezium. Explain the mechanism difference (what each approach reads and from where), and walk through three concrete failure modes the timestamp-watermark approach has that log-based CDC does not — at minimum cover: rows updated within the same second as the watermark cutoff, hard deletes, and transactions that commit out of order relative to their `updated_at` assignment. Then name what new operational concerns log-based CDC introduces in exchange.

 

**Assessment:** The three failure modes are correctly named in direction, and the intuition that something log-shaped with monotonic ordering is what CDC provides is correct. The gap is naming the specific artifact: the Log Sequence Number (LSN) is the monotonic, commit-ordered token in the WAL that gives CDC its ordering guarantee; replication slots persist a consumer's LSN position on the primary; after failover, the consumer reconciles position using the new primary's timeline_id and the durable LSN of the last applied change. The same-second cutoff, hard-delete, and out-of-order-commit failures all collapse to one underlying property: timestamps are wall-clock-assigned (and may be assigned before commit), whereas LSN is commit-order-assigned by the log writer.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 11 'Stream Processing' — §Change Data Capture, pp. 454–457; and Ch. 5 §Setting Up New Followers, pp. 155–158 (LSN and replication position) — ~2h
- [remediation] Debezium Documentation — PostgreSQL Connector Internals — §How the PostgreSQL connector works — §Snapshots, §Streaming changes, §Replication slots, and §Failover behaviour — ~1h 15m

</small>
</details>

<details>
<summary><samp>q3 · ml-engineering · feature-scaling · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A team is training two models on the same tabular dataset of customer features (age in years, account_balance in dollars ranging 0–10M, num_logins_last_week 0–500): a logistic regression with L2 regularization, and a gradient-boosted tree model (XGBoost). The data scientist applies StandardScaler to features before both. Explain (a) why feature scaling materially changes the logistic regression's behaviour — be specific about which part of the loss function or optimization is affected, (b) why the same scaling has essentially no effect on the XGBoost model's predictions, and (c) one case where scaling would still matter for a tree-based pipeline. Commit to whether you'd keep or remove the scaler from the XGBoost training script and justify.

 

**Assessment:** The response substitutes 'float precision' and 'reproducibility' for the actual mechanism. For logistic regression with L2, the relevant facts are: (1) without scaling, gradient descent on the loss takes longer to converge because the loss surface is elongated along the large-magnitude feature axis; (2) L2 penalizes ||w||² uniformly, so a feature measured in dollars (0–10M) receives a vastly smaller coefficient than a feature in 0–500, distorting the regularization's intent. For trees, the property is rank/order invariance: split search evaluates candidate thresholds by their effect on a node-purity criterion, and any strictly monotonic transform preserves the rank ordering and therefore the same splits. The answer's 'bucketed nodes' framing in refinement is not this mechanism. The case-(c) commit (drop the scaler from the XGBoost script; the canonical exception is when distance-based features or a regularized linear leaf model is part of the same pipeline) was not produced.

**Literature**

- [remediation] An Introduction to Statistical Learning — Ch. 6 §6.2 Shrinkage Methods (ridge/lasso and scale dependence) and Ch. 8 §8.1 Decision Trees (split selection) — ~3h
- [remediation] Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow (3e) — Ch. 2 §Feature Scaling and Transformation, Ch. 4 §Regularized Linear Models, Ch. 6 §Decision Trees — ~4h

</small>
</details>

<details>
<summary><samp>q4 · frontend · useeffect-dependency-array · pre 2 → post 3 · ceiling b2 · transitional b3</samp></summary>

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

 

**Assessment:** The race is between async resolution ordering, not network latency translated into render lag: when the user types 'a' then 'ab', both fetches are in flight, and the slower one — whichever it is — wins by virtue of being the last to call setResults. Debouncing reduces the *probability* of overlap but does not eliminate it because the next-typed query can still arrive before the in-flight fetch resolves. The canonical fix lives inside the effect closure: declare `let cancelled = false`, gate setResults on `!cancelled`, and return a cleanup that sets `cancelled = true`. React invokes that cleanup before running the next effect, neutralizing the stale fetch. The invariant the fix guarantees is: only the setResults call from the effect tied to the currently committed `query` value can win. The refinement got close — a stale flag — but did not locate it inside the cleanup closure.

**Literature**

- [remediation] React Documentation — Synchronizing with Effects & You Might Not Need an Effect — Full pages: 'Synchronizing with Effects' (§Fetching data) and 'You Might Not Need an Effect' (§Fetching data) — also 'Lifecycle of Reactive Effects' §Each render has its own effects — ~1h 30m
- [remediation] A Complete Guide to useEffect — Full essay — §What does useEffect Do?, §Each Render Has Its Own Props and State, §So What About Cleanup?, §Speaking the Same Language as React — ~1h

</small>
</details>

<details>
<summary><samp>q5 · systems-distributed · fan-out-on-write-vs-read · pre 3 → post 3 · ceiling b1 · transitional b3</samp></summary>

<small>

 

**Scenario:** A social-media product is designing the timeline service. Two architectures are on the table: (1) fan-out-on-write — when a user posts, the post id is pushed into a precomputed timeline list for every follower; timeline reads are a single lookup. (2) fan-out-on-read — posts are stored once; a timeline read queries posts from all followed users and merges them. Explain the read-cost vs write-cost tradeoff each makes (be concrete about what 'write amplification' means in approach 1), why approach 1 collapses under a user with 50M followers (the 'celebrity problem'), and commit to a hybrid design that handles the celebrity case. Be specific about which users get which treatment and how the timeline read merges the two sources.

 

**Assessment:** The hybrid commit is in the right shape: pull celebrities out of the fan-out-on-write path, store their posts once, and merge at read time. The refinement correctly described the read path as 'fetch the precomputed timeline, scan and insert celebrity posts by ordering primitive.' The gap is in the ordering primitive itself: k-sortable ids (Twitter's snowflake, Instagram's id scheme, or a (timestamp, post_id) composite key) are what make the merge a true k-way merge rather than an O(N) insertion sort. The cache-and-upsert addition is a thoughtful elaboration but introduces a concurrency hazard (two read paths writing the same precomputed timeline) the response does not address. Tradeoff dismissals at the B4 level — what happens when a user oscillates around the celebrity threshold, how the system bounds fanout tail latency, what SLI signals which branch is degraded — were not produced.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 1 §Describing Load (Twitter timelines case study, pp. 11–14) — fan-out-on-write vs fan-out-on-read, the celebrity hybrid — ~45m
- [remediation] System Design Interview Vol. 1 — Design a News Feed System — Ch. 11 'Design a News Feed System' — full chapter (fan-out service, read path merge, cache layers, snowflake-style ordering ids) — ~50m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
