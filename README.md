

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
industry     swe                                  updated         2026-05-17
scope        cross-domain · grab-bag              duration        48m 41s
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  ml-engineering     feature-importance      ₂   2   ₁
q2  ai-llm             function-calling-loop   ₃   3   ₂
q3  security           oauth-authorization     ₂   2   ₁
q4  data-engineering   data-skew-in-shuffle    ₂   2   ₂
q5  systems-distributedleader-election         ₃   3   ₂

gaps         authorization-code-interception · correlated-feature-importance-split · data-skew-in-shuffle · feature-importance-interpretation

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · ml-engineering · feature-importance-interpretation · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A data scientist at an insurance pricing startup trains an XGBoost model to predict claim severity. They report to the product team that the top three features by gain importance are policy_tenure_days, policy_tenure_months, and policy_tenure_years (all derived from the same policyholder start date). The product team wants to drop policy_tenure_months and policy_tenure_years to simplify the feature pipeline, citing that gain importance shows they're 'almost as predictive' as policy_tenure_days. Explain (a) what gain importance is actually measuring and why it produces this misleading picture when correlated/redundant features are present, (b) what would happen mechanically if you dropped two of the three features and retrained, and (c) what alternative importance method would give a more trustworthy answer to the product team's question, and what it measures differently.

 

**Assessment:** The answer recognized that correlation among the three tenure features is the source of the misleading gain picture, but did not state what gain actually counts (cumulative loss reduction at splits where the feature is chosen), did not predict the correct mechanical outcome of dropping two of three redundant features (performance is preserved; gain consolidates on the survivor), and named no concrete alternative importance method. The refinement probe pointed directly at the split-selection mechanism; the response surfaced the phrase 'split points' but did not connect it to per-node greedy choice across near-identical features, and the (b) prediction was not revised. The gap is in the gain-attribution mechanism and the catalog of held-out-evaluation-based alternatives.

**Literature**

- [remediation] Interpretable Machine Learning — Ch. 8.5 'Permutation Feature Importance' — full chapter, including the discussion of correlated features — ~45m
- [remediation] XGBoost Documentation — Python API — Booster.get_score importance_type parameter: 'gain', 'weight', 'cover', 'total_gain', 'total_cover' — ~15m

</small>
</details>

<details>
<summary><samp>q2 · ai-llm · function-calling-loop · pre 3 → post 3 · ceiling b1 · transitional b2</samp></summary>

<small>

 

**Scenario:** A SaaS support assistant is built as an LLM agent with three tools: search_kb(query), get_ticket(ticket_id), and create_ticket(payload). The current loop is: send prompt → if model returns a tool call, execute it → append tool result to messages → call model again → repeat until model returns a final text response. In production, two failure modes appear: (1) when a tool raises an exception, the agent often loops calling the same tool with the same arguments 5-10 times before giving up, and (2) occasionally the model emits a tool call with a malformed argument (e.g., ticket_id as a sentence rather than an id), the tool errors, and the model 'apologizes' to the user without retrying. Explain (a) why the current loop produces these behaviors — what the model is actually seeing in its context on each iteration, (b) two specific changes to how tool results (especially errors) are formatted and fed back that would change this behavior, and (c) what loop-level control you would add and why it is preferable to relying on the model to self-terminate.

 

**Assessment:** The proposed remediations — schema-bounded error contracts, retry budgets, and a deterministic outer controller with hash-based loop detection — are on-mechanism and would in fact constrain both failure modes. What is missing, and what the refinement specifically surfaced, is an accurate model of what the LLM actually sees on each iteration of an agent loop and why error formatting is itself a prompt-engineering decision. The refinement attributed the looping behavior to KV-cache token persistence influencing generation, which conflates an inference-layer prefill optimization with the conditioning mechanism that actually drives repeated tool calls. The gap is in naming the conditioning primitive — what is in the message array on turn N — and connecting tool-result shape to next-token distribution.

**Literature**

- [remediation] Building Effective Agents — §Tool design and §Agent control loops — full sections on how tool definitions, error messages, and orchestration shape model behavior — ~30m
- [remediation] vLLM: Easy, Fast, and Cheap LLM Serving with PagedAttention — §3 Background — KV cache, prefill, and prefix sharing (single section, ~3 pages) — ~30m

</small>
</details>

<details>
<summary><samp>q3 · security · oauth-authorization-code-flow · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A mobile app for a retail loyalty program uses OAuth 2.0 to authenticate users against the company's identity provider. The original implementation used the authorization code flow with a static client_secret embedded in the mobile binary. A security review flagged this and the team migrated to authorization code flow with PKCE, removing the client_secret entirely. A junior engineer asks: 'If we just removed the secret and added a code_verifier/code_challenge, what attack are we actually preventing? The authorization code is still in the redirect URL either way.' Explain (a) the specific attack PKCE prevents that the static-secret flow could not defend against on a mobile device, (b) the mechanism by which code_challenge (sent at /authorize) and code_verifier (sent at /token) bind the two requests together so an interceptor of the code cannot redeem it, and (c) why simply keeping the client_secret would not have closed this gap on a mobile client.

 

**Assessment:** The answer correctly identifies that mobile binaries cannot hold a meaningful secret, but misidentifies what PKCE actually does. The mechanism is not temporal binding, not MFA-based provenance, and not a public/private keypair exchange — it is a one-way hash binding between two values, one sent on the front channel and one on the back channel. The refinement probe targeted the cryptographic property directly and the response committed to the wrong cryptographic family, which is the diagnostic gap. The threat being prevented is also specific to the mobile platform's redirect-handling model and is not captured by general 'attack surface reduction' language.

**Literature**

- [remediation] RFC 7636: Proof Key for Code Exchange by OAuth Public Clients — §1 Introduction, §1.1 Protocol Flow, §4.1–§4.6 (code_verifier construction, code_challenge derivation, S256 method, server-side verification) — ~45m
- [remediation] OAuth 2.0 for Native Apps (BCP 212 / RFC 8252) — §8.1 Protecting the Authorization Code, §7 Receiving the Authorization Response (custom URI schemes, claimed https schemes, loopback interface) — ~30m

</small>
</details>

<details>
<summary><samp>q4 · data-engineering · data-skew-in-shuffle · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A daily Spark job joins a clickstream fact table (~2B rows/day) against a customer dimension (~50M rows) on customer_id, then aggregates clicks-per-customer-per-day. The job runs for 45 minutes total, but the Spark UI shows 199 of 200 shuffle tasks finishing within 3 minutes while one task runs for 42 minutes processing ~30% of the data. Investigation shows that customer_id = 0 is used as a sentinel for unauthenticated/anonymous traffic and accounts for roughly 600M rows/day. Explain (a) the precise mechanism by which a single skewed key produces this one-task-dominates pattern in a shuffle-based hash join, (b) the 'salting' technique for mitigating this — what you change on each side of the join and why it redistributes the work — and (c) one tradeoff or correctness concern the salting approach introduces that did not exist in the naive join.

 

**Assessment:** The answer recognised shuffle skew and named salting as the mitigation, but mis-attributed the mechanism to a defect in the hash function rather than to the deliberate co-location property that every hash join depends on. The proposed salting variant — hashing only the suffix of customer_id while keeping a deterministic prefix — would route all sentinel rows to the same reducer and not relieve the skew, indicating the redistribution logic was not internalised. The refinement directly probed this assumption; the response acknowledged the assumption could be wrong but pivoted to an upstream schema suggestion rather than correcting the join-time mechanism, and never described the paired fact-side key augmentation with dim-side row replication that makes salting work. The gap is in the partitioner's contract and how a composite key changes its input distribution.

**Literature**

- [remediation] High Performance Spark — Ch. 4 §Joins (SQL & Core) — 'Speeding Up Joins by Assigning a Known Sort Order' and 'Skewed Data' subsections (the canonical chapter on hash-join mechanics and the salting pattern with both fact-side key augmentation and dim-side replication worked through end-to-end) — ~1h 15m
- [remediation] Apache Spark Documentation — Adaptive Query Execution — §Optimizing Skew Join — spark.sql.adaptive.skewJoin.enabled and the partition-splitting mechanism AQE applies automatically when one shuffle partition is N× larger than the median — ~20m

</small>
</details>

<details>
<summary><samp>q5 · systems-distributed · leader-election-fencing-token · pre 2 → post 3 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A distributed job scheduler uses a coordination service (e.g., ZooKeeper/etcd) to elect a single leader that holds an exclusive lease on writing to a shared object store. Leases expire after 30 seconds and are renewed every 10 seconds. An on-call engineer reports a corruption incident: leader A experienced a 45-second GC pause, leader B was elected and started writing during the pause, then leader A woke up, still believed it held the lease (its in-process clock said only a moment had passed), and wrote stale data over B's writes. Explain (a) why a lease-and-clock-only design is insufficient to prevent this class of bug regardless of how short you make the lease, (b) what a fencing token is, the monotonicity property it must have, and how the object store must use it to make A's late write a no-op, and (c) what specifically must change on the storage side — not just the client — for fencing to actually work.

 

**Assessment:** The answer identifies the right problem family (stale-writer corruption, token-gated writes, storage-side enforcement at the ingest boundary) but the core comparison mechanism is mis-specified: the refinement proposes a bitwise-xor or diverging-character index, where the fencing protocol requires a monotonic greater-than check against a durably-held high-water mark. The reason a lease-and-clock-only design fails is also mis-rooted in a TOCTOU/polling argument rather than in the non-authoritativeness of the deposed leader's local clock-belief after an unbounded pause. The 'A wakes up, sees its writes are late, and drops itself' framing inverts the design — A does not need to discover anything; the storage rejects A's write unconditionally based on token order. The storage-side requirements (durable max-token, atomic compare-and-write, behavior across restart) are gestured at but not derived.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 8 §The Truth Is Defined by the Majority — 'Fencing tokens', pp. 301–304 — ~45m
- [remediation] How to do distributed locking — Section 'Making the lock safe with fencing' — ~25m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
