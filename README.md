

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
<summary><samp>fortifai · self-audit loop · streak 2d</samp></summary>

<sub><samp><i>self-audit: scenario-based time-pressured recall, cross-domain breadth, b3-calibrated<br>
invariant: zero outside assistance. no docs, no ai, no peers. 10m/response, 5m/single refinement<br>
breadth: systems/distributed, backend, sre, ml, ai/llm, frontend, data, security<br>
bar: consistent ≥3 across all 8 swe fields</i></samp></sub>

```
industry     swe                                  updated         2026-05-16
scope        cross-domain · grab-bag              duration        1h 0m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  frontend           virtualized-list        ₃   3   ₂
q2  backend            unique-constraint-race  ₂   2   ₁
q3  data-engineering   small-files-problem     ₃   2   ₂
q4  sre                graceful-shutdown       ₃   3   ₂
q5  ml-engineering     one-hot-vs-target       ₂   2   ₁

gaps         compaction-strategy · high-cardinality-categorical · insert-on-conflict · object-store-listing-cost

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · frontend · virtualized-list · pre 2 → post 3 · ceiling b1 · transitional b2</samp></summary>

<small>

 

**Scenario:** A team is building a customer support dashboard that displays an activity feed of up to 50,000 events for a single account. The current implementation renders all rows into the DOM at mount time inside a scrollable container. Initial render takes 4 seconds on a mid-range laptop, scrolling is janky, and memory usage spikes. A junior engineer proposes 'just use a virtualized list library like react-window or TanStack Virtual'. Explain the mechanism by which list virtualization fixes the performance problem (what changes about what the browser is doing). Then describe two concrete tradeoffs or correctness hazards virtualization introduces that the engineer must handle — be specific about what breaks and why.

 

**Assessment:** The original response framed virtualization as 'lazy loading vs eager loading' and as decoupling DOM mount from event rendering, which is not the operative mechanism — the browser's cost scales with DOM node count, and virtualization works by keeping only a viewport-sized window of real row nodes in the DOM at any moment. Under refinement the answerer reached DOM node count as the lever but landed on an incorrect model in which the virtualized region is treated as a single leaf node and rendering is 'deferred' outside the DOM, rather than understanding that a small set (~tens) of recycled row nodes is actually mounted and absolutely positioned within a spacer of full scroll height. The two tradeoffs offered — in-use sync/reconciliation latency and aggregation-correctness from data not being eagerly loaded — are not virtualization hazards (data still lives in JS state; only DOM nodes are windowed), and the canonical hazards in this space (variable row height measurement, accessibility and find-in-page semantics, focus loss on unmount) are absent. The gap is in the precise node-budget primitive and in the user-observable consequences that distinguish a windowed list from the alternatives.

**Literature**

- [remediation] react-window — Official Documentation and How It Works — 'How does it work?' overview + FixedSizeList API page — focused chapter on the windowing primitive: itemCount, itemSize, overscanCount, and the inner/outer container structure (~1 chapter equivalent) — ~45m
- [remediation] Rendering large lists with react-virtuoso / Inclusive Components: Tooltips & Toggletips and 'A Todo List' patterns for a11y in virtualized contexts — Virtuoso 'Troubleshooting & Common Pitfalls' + the 'Variable Sized Items' guide — the specific subsection on measurement, scroll-jump, and accessibility caveats with virtualized lists — ~30m

</small>
</details>

<details>
<summary><samp>q2 · backend · unique-constraint-race · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A signup endpoint creates a User row with a unique email constraint. Under load testing, the team observes occasional 500 errors with a Postgres unique_violation (SQLSTATE 23505) instead of the expected 'email already taken' 409 response. The current code does: `SELECT WHERE email = $1` — if empty, `INSERT`. Explain why this pattern produces the unique_violation under concurrency even though the SELECT returned nothing. Then commit to a fix that is correct under concurrency, name the Postgres primitive that makes it correct, and articulate why your fix preserves the invariant that two concurrent signups for the same email cannot both succeed.

 

**Assessment:** The answer reached for the right surface recipe (INSERT ... ON CONFLICT) but the refinement probe revealed that the recipe was not anchored to the mechanism that makes it correct. The pivot to inbox/outbox and to ACID-acronym framing under pressure indicates pattern-matching against memorized labels rather than reasoning about what Postgres actually does between the read and write phases of two concurrent transactions. The gap is in the storage-engine primitive that serializes concurrent inserts on the same key value, and in how Read Committed isolation treats non-existent rows.

**Literature**

- [remediation] PostgreSQL Documentation — INSERT ... ON CONFLICT — §ON CONFLICT Clause — specifically the paragraphs on atomicity guarantees, the role of the unique or exclusion index, and the use of RETURNING to distinguish inserted vs conflicting rows — ~20m
- [remediation] Designing Data-Intensive Applications — Ch. 7 §Preventing Lost Updates and §Write Skew and Phantoms (pp. 242–251) — covers compare-and-set, atomic write operations, materializing conflicts via unique constraints, and why SERIALIZABLE is the heavier alternative — ~1h 0m

</small>
</details>

<details>
<summary><samp>q3 · data-engineering · small-files-problem · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A streaming pipeline writes records to a partitioned table on S3 (Parquet, partitioned by event_date) every 60 seconds. After 6 months, downstream Spark queries that used to take 30 seconds now take 12 minutes, even though total data volume has only doubled. Investigation shows each daily partition contains ~1,440 small Parquet files averaging 2 MB each. Explain the mechanism by which small files degrade query performance on object-stored partitioned tables — be specific about what costs scale with file count rather than data volume. Then describe a compaction strategy that addresses this, and articulate the tradeoff you accept by running it (what gets worse, or what new failure mode you introduce).

 

**Assessment:** The answer recognized the small-files problem and proposed compaction in the right direction, but when the refinement probe asked the load-bearing B3 question — which specific object-store operations scale with file count and why — the response retreated to an abstract 'object metadata vs file hierarchy' analogy rather than naming the concrete per-file costs that distinguish S3 from a local filesystem. The compaction description also conflated batch compaction with at-ingest consolidation, and the tradeoff analysis enumerated generic pipeline risks rather than the specific tradeoffs the question asked for. The gap is in the canonical primitives of object-store access cost and the operational shape of a compaction job.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 3 §Column-Oriented Storage (pp. 95–101) and Ch. 10 §Distributed Filesystems vs Object Stores — ~1h 30m
- [remediation] Apache Iceberg Documentation — Maintenance — §Compacting Data Files (rewrite_data_files) and §Expire Snapshots — ~25m

</small>
</details>

<details>
<summary><samp>q4 · sre · graceful-shutdown · pre 2 → post 3 · ceiling b1 · transitional b2</samp></summary>

<small>

 

**Scenario:** A stateless HTTP service running in Kubernetes shows a spike in 502s from the ingress every time a deployment rolls out, even when the new version is healthy. The team has readiness probes configured correctly. Explain the lifecycle mechanism that causes the 502s during pod termination — what specifically happens between the moment Kubernetes decides to terminate a pod and the moment the kube-proxy/endpoints controller stops sending it traffic, and why in-flight or newly-arriving connections fail. Then describe the canonical fix (name the specific signals and hooks involved) and articulate the tradeoff: what does your fix cost, and what bounds it?

 

**Assessment:** The original response identified the rollout lifecycle as the failure domain and intuited that there is a gap between the terminate decision and traffic cessation, but invented a multi-step lifecycle in place of the actual Kubernetes primitives and proposed a custom 'termination signal status' rather than recognizing the existing mechanism. The refinement probe pulled out SIGTERM correctly and the right shape of fix (delay before the signal), but the specific pod-spec hook and — more importantly — the propagation race between Endpoints/EndpointSlice updates and SIGTERM delivery were never named. The gap is in the two-flow concurrency model that makes the canonical fix bounded by endpoint propagation latency on one side and terminationGracePeriodSeconds on the other.

**Literature**

- [remediation] Kubernetes Documentation — Pod Lifecycle: Termination of Pods — §Pod termination and §Container hooks (preStop) — the two-flow diagram: API-server marks pod Terminating → Endpoints controller removes pod → kube-proxy on every node reprograms iptables, IN PARALLEL with kubelet running preStop then sending SIGTERM to PID 1, then SIGKILL after terminationGracePeriodSeconds — ~25m
- [remediation] Graceful shutdown and zero downtime deployments in Kubernetes — Full article — walks through why pods receive traffic after SIGTERM, the preStop sleep pattern, terminationGracePeriodSeconds tuning, and the SIGTERM handler the app itself must implement — ~30m

</small>
</details>

<details>
<summary><samp>q5 · ml-engineering · one-hot-vs-target-encoding · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A team is training a gradient-boosted tree model (LightGBM) to predict 30-day customer churn. One of the features is `zip_code` with ~30,000 distinct values. A teammate proposes target encoding (replace each zip with the mean churn rate of training rows in that zip) to avoid the dimensionality blow-up of one-hot encoding. Explain why one-hot encoding is a poor fit for this feature in a tree model — be specific about what tree-split mechanics do with one-hot columns at this cardinality. Then explain the specific leakage hazard target encoding introduces if implemented naively, and name the concrete technique that prevents that leakage while preserving the encoding's signal.

 

**Assessment:** The answer correctly senses that encoding can leak information and that one-hot interacts badly with tree split mechanics, but the specific primitives are not held: the per-column gain-ranking behavior of LightGBM's split search at high cardinality is not named, the leakage family is misidentified (described as 'look-ahead bias,' which is temporal leakage, not target leakage), and the canonical mitigation — out-of-fold / K-fold target encoding — is replaced with a general 'scope the information, process sequentially' framing. The refinement probe pointed directly at split-candidate selection across columns and the response did not narrow toward the mechanism. The gap is in the concrete vocabulary of categorical handling in GBDTs and in the standard leakage-mitigation pattern for mean-target encoding.

**Literature**

- [remediation] LightGBM Documentation — Advanced Topics: Optimal Split for Categorical Features — Advanced Topics §Categorical Feature Support and §Optimal Split for Categorical Features — the one focused section explaining why one-hot is inferior at high cardinality and how LightGBM's native handling (Fisher 1958 partition over category statistics) replaces it. — ~20m
- [remediation] Feature Engineering for Machine Learning — Chapter 5 §Categorical Variables — specifically the subsection on target/mean encoding and out-of-fold computation, plus the smoothed (Bayesian) variant for low-count categories. — ~45m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
