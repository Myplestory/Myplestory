

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
scope        cross-domain · grab-bag              duration        1h 3m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  ml-engineering     learning-curve          ₂   2   ₁
q2  backend            read-replica-routing    ₄   3   ₂
q3  data-engineering   merge-vs-append         ₂   2   ₁
q4  sre                alert-on-symptoms       ₃   2   ₂
q5  frontend           optimistic-ui-update    ₃   3   ₂

gaps         actionable-alert-design · alert-on-symptoms · bias-variance-tradeoff · cause-vs-symptom-alerting

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · ml-engineering · learning-curve-diagnosis · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A data scientist at a marketing analytics firm trains a gradient-boosted classifier to predict email-campaign click-through. After training, they observe: training AUC = 0.94, validation AUC = 0.71, with a wide and persistent gap that does not close as more training data is added (they tried doubling the training set). The team's instinct is to add more features. Walk through what the learning-curve shape (high training score, much lower validation score, gap not closing with more data) is telling you about the model, why adding more raw features is likely the wrong move, and what two interventions you would try first. Explain the mechanism behind each intervention — why it would narrow the gap.

 

**Refinement:** You said 'the model itself'. Clarify: what is the mechanism by which tree depth specifically causes the training-validation gap to persist even as more training data is added?

 

**Assessment:** Both turns missed the canonical reading of the learning-curve shape (high train, much lower val, gap not closing with more data) as a high-variance / overfitting signature, and instead pursued a training-vs-validation environment-mismatch story that the 'gap persists when data is doubled' clue actually rules out. The refinement handed over 'tree depth' as the lever; the reply did not produce the depth→leaf-sample-count→noise-memorization mechanism, and instead recast depth as a downstream symptom of sampling bias, which inverts how the hyperparameter actually works. The gap is in the bias-variance framework itself and in the GBDT-specific regularization knobs (max_depth, min_child_weight, reg_lambda, gamma, subsample, colsample_bytree, early_stopping_rounds) that operationalize it.

**Literature**

- [remediation] Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow (3rd ed.) — Ch. 4 §Learning Curves and Ch. 7 §Gradient Boosting — read the learning-curve diagnosis (high training score / low validation score / gap that does not close with more data → high variance, not high bias) and then the GBDT regularization knobs that act on it. — ~1h 15m
- [remediation] XGBoost Documentation — Notes on Parameter Tuning & Introduction to Boosted Trees — 'Notes on Parameter Tuning' §Control Overfitting and §Handle Imbalanced Dataset, plus 'Introduction to Boosted Trees' §Model Complexity and Regularization. — ~30m

</small>
</details>

<details>
<summary><samp>q2 · backend · read-replica-routing · pre 2 → post 3 · ceiling b1–b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A SaaS team running PostgreSQL with one primary and two asynchronous read replicas wants to route read-only API endpoints to the replicas to offload the primary. A junior engineer proposes a simple rule: any HTTP GET goes to a replica, any POST/PUT/DELETE goes to the primary. Explain two concrete user-visible failure modes this naive rule will produce in a typical web app (one of which must involve a user's own recent write), name the mechanism behind each (i.e., what specifically goes wrong at the database/replication layer), and describe a routing refinement that preserves the offload benefit while closing one of those failure modes. Be explicit about what the refinement gives up.

 

**Refinement:** You said 'use the session token to bypass that route and get from the just updated row/table with a ttl as the replica is still updating'. Clarify: what specific condition or event ends the TTL window and allows subsequent GETs to return to replica routing without risking another stale read?

 

**Assessment:** The answer correctly named replica lag as the mechanism behind the read-your-writes failure mode and, under refinement, sketched the right shape of the LSN-driven terminating condition for session-scoped primary pinning. Two gaps remain: the original 'second failure mode' answer diverted into primary HA / consensus territory (Raft, Paxos, Byzantine, Sybil), which is a different layer of the system than the question asked about; and the refinement never names what the proposed mitigation gives up. The result is a partial answer to a two-part question, with one strong half and one off-target half.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 5 §Problems with Replication Lag — Reading Your Own Writes, Monotonic Reads, Consistent Prefix Reads (pp. 161–168) — ~1h 45m
- [remediation] PostgreSQL Documentation — Hot Standby and Replication Monitoring — §27.4 Hot Standby + §27.2.5.2 Monitoring (pg_current_wal_lsn, pg_last_wal_replay_lsn) — the LSN-comparison primitive for session-bound replica routing — ~45m

</small>
</details>

<details>
<summary><samp>q3 · data-engineering · merge-vs-append-semantics · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A data engineer ingests a daily extract of an `orders` table from an OLTP source into a Snowflake (or equivalent warehouse) `orders_raw` table using an APPEND-only load. After three months, downstream analysts complain that `SELECT COUNT(*) FROM orders_raw WHERE status='SHIPPED'` returns far more rows than the source system reports, and per-order revenue rollups are inflated. The engineer's first reaction is 'dedupe with `SELECT DISTINCT`'. Explain (a) what the append-only ingest is actually capturing about the source table given that orders get updated over their lifecycle, (b) why `SELECT DISTINCT` will not fix the rollup, and (c) what the correct load pattern is — name it, describe the mechanism (what gets compared against what, on what key, with what tiebreaker), and explain the tradeoff it makes versus the original append-only approach.

 

**Refinement:** You said 'Compare on wall clock/post to warehouse(inventory housekeeping date) and update with relevant state'. Clarify: what specific column or columns from the source extract serve as the tiebreaker key, and how does the merge operation use that value to decide which row wins when multiple extracts contain the same order ID?

 

**Assessment:** The answer correctly senses that append-only loses lifecycle state and that a write-path fix is needed, but never names the warehouse primitive the question is about, and gives a wrong reason for the DISTINCT failure (treats it as query-time rather than as 'the rows are not actually duplicates — they differ in the mutated columns'). The refinement asked precisely which source column serves as the tiebreaker; the response answered with vector clocks and per-service bitmaps instrumented on the OLTP source, indicating a category error about where the ordering token comes from in a warehouse load. The gap is the canonical name of the pattern and the source-side column that the warehouse compares on.

**Literature**

- [remediation] The Data Warehouse Toolkit, 3rd Edition — Ch. 5 §Slowly Changing Dimension Basics (Type 1 overwrite vs Type 2 history-preserving) and Ch. 20 §Big Data Architectures — partition-replacement vs. merge patterns — ~2h 30m
- [remediation] Snowflake MERGE Statement Documentation — Full page: MERGE syntax, ON-clause semantics, WHEN MATCHED / WHEN NOT MATCHED branches, and the QUALIFY ROW_NUMBER() pattern for collapsing multi-row source extracts to one row per key before merging — ~45m

</small>
</details>

<details>
<summary><samp>q4 · sre · alert-on-symptoms · pre 2 → post 2 · ceiling b1 · transitional b2</samp></summary>

<small>

 

**Scenario:** A platform team's on-call rotation is drowning in pages. Looking at the alert list, you see: 'CPU > 80% on api-server-3', 'Memory > 75% on api-server-7', 'Disk I/O sustained > 5000 IOPS on db-replica-2', 'JVM heap > 70% on worker-pool'. The team's SLO is p99 checkout latency < 800ms and checkout success rate > 99.5%, both of which are currently being met. Explain the diagnostic problem with this alert set in terms of the cause-vs-symptom distinction, why an alert firing while the SLO is met is a specific kind of broken alert (name the failure mode), and what two alerts you would replace the existing set with. For each replacement alert, state what user-visible signal it tracks and why it is actionable in a way the originals are not.

 

**Refinement:** You said 'lack of legible observability, or whatever the canonical name for it is/symptom vs cause/upstream vs downstream distinction'. Clarify: what is the specific named failure mode for an alert that fires while no user-visible harm exists, and what property of that alert makes it categorically different from an alert that is merely noisy?

 

**Assessment:** The response correctly diagnosed the cause-vs-symptom mismatch and that the alerts do not track the SLO, but the refinement probe — which asked for the canonical name of an alert that fires without user-visible harm and the property that makes it categorically different from a noisy alert — was answered with a different failure family ('silent errors,' which is the inverse: harm without an alert) and a five-part taxonomy rather than the specific term. The two requested replacement alerts, each tied to one of the named SLIs with a stated triggering mechanism, were not produced; the answer described an instrumentation approach instead. The gap is in the vocabulary and paging-policy mechanism that converts an SLO into actionable alerts.

**Literature**

- [remediation] Site Reliability Engineering: How Google Runs Production Systems — Ch. 6 'Monitoring Distributed Systems' — focus on §'Symptoms Versus Causes' and §'Four Golden Signals' — ~45m
- [remediation] The Site Reliability Workbook — Ch. 5 'Alerting on SLOs' — the section on multi-window, multi-burn-rate alerts — ~1h

</small>
</details>

<details>
<summary><samp>q5 · frontend · optimistic-ui-update · pre 2 → post 3 · ceiling — · transitional b1–b3</samp></summary>

<small>

 

**Scenario:** A product team wants the 'like' button on a social feed to feel instant — the heart should fill in and the count increment before the server responds. The engineer implements this by updating local component state immediately on click, then firing the POST /likes request in the background. In code review, you flag three concrete correctness issues this naive optimistic-update has under realistic conditions: (a) the server request fails, (b) the user clicks like/unlike rapidly five times in two seconds while on slow network, and (c) the server's authoritative count differs from the client's optimistic count when the response arrives. For each, name the failure (what the user sees go wrong), name the mechanism that produces it (what concretely happens in the request/response sequence), and describe the minimum control that fixes it without losing the 'instant' feel.

 

**Refinement:** You said 'On a slow network, how you handle reqs matter here'. Clarify: what specific property of the request sequencing — ordering, deduplication, or cancellation — causes the local state to diverge from the server's final state after five rapid clicks?

 

**Assessment:** The answer recognizes the problem domain (optimistic update, rollback, reconciliation) but does not produce the concrete mechanism for any of the three sub-failures: no snapshot/restore tied to the request promise for (a), no AbortController or sequence-id or debounce for (b), and no replace-don't-delta reconciliation for (c). The refinement correctly identifies 'cancellation' as the property under test for the click-race, which is a real recovery, but stops short of naming the API or pattern that implements it and pivots into a multi-client ingest-ordering framing that is a different problem. The closing 'depends on UX' enumeration defers the design commitment a B4 reviewer would expect. The literature points at the request-sequencing primitive and the canonical optimistic-update lifecycle so the reader can name what the mechanism actually is.

**Literature**

- [remediation] TanStack Query (React Query) — Optimistic Updates — Optimistic Updates §'Updating a list of todos when adding a new todo' and §'If the mutation fails' — the onMutate/onError/onSettled lifecycle: snapshot previous state, apply optimistic update, restore snapshot on error, refetch/reconcile on settle — ~20m
- [remediation] MDN — AbortController and request cancellation — AbortController page + 'Using AbortController with fetch' example, plus the React docs 'Synchronizing with Effects §Fetching data' cancellation pattern — ~15m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
