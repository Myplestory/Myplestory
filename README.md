

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
q2  ai-llm             function-calling-loop   ₄   3   ₂
q3  security           oauth-authorization     ₂   2   ₁
q4  data-engineering   data-skew-in-shuffle    ₂   2   ₁
q5  systems-distributedleader-election         ₄   3   ₂

gaps         authorization-code-interception · correlated-feature-importance-split · data-skew-in-shuffle · feature-importance-interpretation

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · ml-engineering · feature-importance-interpretation · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A data scientist at an insurance pricing startup trains an XGBoost model to predict claim severity. They report to the product team that the top three features by gain importance are policy_tenure_days, policy_tenure_months, and policy_tenure_years (all derived from the same policyholder start date). The product team wants to drop policy_tenure_months and policy_tenure_years to simplify the feature pipeline, citing that gain importance shows they're 'almost as predictive' as policy_tenure_days. Explain (a) what gain importance is actually measuring and why it produces this misleading picture when correlated/redundant features are present, (b) what would happen mechanically if you dropped two of the three features and retrained, and (c) what alternative importance method would give a more trustworthy answer to the product team's question, and what it measures differently.

 

**Assessment:** The answer recognized that correlation among the three tenure features distorts the importance picture but did not produce the mechanism: what gain is actually summing, what tree-building decision causes the fragmentation, what would mechanically happen to performance after dropping the redundant columns, and which named alternative method gives a more trustworthy answer. The refinement probe pointed directly at the split-selection step and surfaced the phrase 'split points', but did not connect it to per-node greedy candidate evaluation across near-identical features. The gap is in the formal definition of gain attribution and the canonical alternative-method literature.

**Literature**

- [remediation] Introduction to Boosted Trees (XGBoost documentation) — §The Structure Score and §Learn the tree structure — definition of gain as G²/(H+λ) and how it is accumulated per feature across splits; plus Python API Booster.get_score importance_type='gain' / 'total_gain' — ~45m
- [remediation] Interpretable Machine Learning — Ch. 8.5 Permutation Feature Importance — definition, correlated-feature failure mode, and the hierarchical-clustering remedy; cross-read with the scikit-learn example 'Permutation Importance with Multicollinear or Correlated Features' — ~50m

</small>
</details>

<details>
<summary><samp>q2 · ai-llm · function-calling-loop · pre 3 → post 3 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A SaaS support assistant is built as an LLM agent with three tools: search_kb(query), get_ticket(ticket_id), and create_ticket(payload). The current loop is: send prompt → if model returns a tool call, execute it → append tool result to messages → call model again → repeat until model returns a final text response. In production, two failure modes appear: (1) when a tool raises an exception, the agent often loops calling the same tool with the same arguments 5-10 times before giving up, and (2) occasionally the model emits a tool call with a malformed argument (e.g., ticket_id as a sentence rather than an id), the tool errors, and the model 'apologizes' to the user without retrying. Explain (a) why the current loop produces these behaviors — what the model is actually seeing in its context on each iteration, (b) two specific changes to how tool results (especially errors) are formatted and fed back that would change this behavior, and (c) what loop-level control you would add and why it is preferable to relying on the model to self-terminate.

 

**Assessment:** The answer correctly proposes the right family of remediations — structured error envelopes, bounded retries, and a deterministic outer controller with argument-hash dedup — and frames the orchestration boundary correctly as 'move control off the non-deterministic model.' The refinement targeted the underlying primitive (what is the model actually seeing on iteration N+1?) and the answer attributed the repeated-call behavior to LLM-side token caching rather than to the cumulative message history conditioning the next-turn distribution. The gap is in the conditioning-vs-caching distinction: understanding that the tool result message is appended to history and re-fed on every call, and that this history (not any cache) is what shapes the next token choice.

**Literature**

- [remediation] Building Effective Agents — §Tool use and §Agents — specifically the description of how tool results are appended to the message array and re-fed as input on each iteration of the agent loop — ~20m
- [remediation] vLLM: Efficient Memory Management for Large Language Model Serving with PagedAttention — §3 Background — KV cache and prefix sharing (~3 pages) — ~30m

</small>
</details>

<details>
<summary><samp>q3 · security · oauth-authorization-code-flow · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A mobile app for a retail loyalty program uses OAuth 2.0 to authenticate users against the company's identity provider. The original implementation used the authorization code flow with a static client_secret embedded in the mobile binary. A security review flagged this and the team migrated to authorization code flow with PKCE, removing the client_secret entirely. A junior engineer asks: 'If we just removed the secret and added a code_verifier/code_challenge, what attack are we actually preventing? The authorization code is still in the redirect URL either way.' Explain (a) the specific attack PKCE prevents that the static-secret flow could not defend against on a mobile device, (b) the mechanism by which code_challenge (sent at /authorize) and code_verifier (sent at /token) bind the two requests together so an interceptor of the code cannot redeem it, and (c) why simply keeping the client_secret would not have closed this gap on a mobile client.

 

**Assessment:** The answer identified the security domain and the platform constraint (mobile binary inspectability) but misidentified the cryptographic primitive twice — first as temporal binding plus MFA provenance, then under direct refinement as an asymmetric public/private keypair scheme. The B3 security mechanism invariant requires naming the mechanism and why it is sufficient against the specific threat; the response named neither the threat correctly (authorization code interception via OS redirect handling on native clients) nor the mechanism (SHA-256 preimage resistance binding /authorize to /token). The gap is in the specific RFC 7636 construction and the public-client credential-confidentiality impossibility from RFC 6749 §2.1.

**Literature**

- [remediation] RFC 7636: Proof Key for Code Exchange by OAuth Public Clients — §1 (Authorization Code Interception Attack), §4.1 code_verifier, §4.2 code_challenge, §4.6 Server Verifies code_verifier — ~45m
- [remediation] OAuth 2.0 in Action — Ch. 7 §Public clients and Ch. 10 §Native applications and PKCE — ~2h

</small>
</details>

<details>
<summary><samp>q4 · data-engineering · data-skew-in-shuffle · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A daily Spark job joins a clickstream fact table (~2B rows/day) against a customer dimension (~50M rows) on customer_id, then aggregates clicks-per-customer-per-day. The job runs for 45 minutes total, but the Spark UI shows 199 of 200 shuffle tasks finishing within 3 minutes while one task runs for 42 minutes processing ~30% of the data. Investigation shows that customer_id = 0 is used as a sentinel for unauthenticated/anonymous traffic and accounts for roughly 600M rows/day. Explain (a) the precise mechanism by which a single skewed key produces this one-task-dominates pattern in a shuffle-based hash join, (b) the 'salting' technique for mitigating this — what you change on each side of the join and why it redistributes the work — and (c) one tradeoff or correctness concern the salting approach introduces that did not exist in the naive join.

 

**Assessment:** The answer identified shuffle skew and named salting at vocabulary level but mis-attributed the mechanism to hash-function entropy rather than to the co-location-by-contract requirement that every hash join imposes — equal keys MUST land on one reducer for the join to be correct, and entropy in the hash would break that. The proposed prefix-deterministic salting variant would not redistribute work because a partitioner keying on the prefix would still route all sentinel rows to one task; the dimension-side replication step and the post-join rollup are both absent. The refinement probe gave a chance to interrogate the 'naive hashing' framing, but the answerer pivoted to an upstream schema suggestion (add a label column) rather than repairing the partitioner-contract understanding. The gap is in the join-internals primitive, not in awareness of the symptom.

**Literature**

- [remediation] High Performance Spark — Ch. 4 §Skewed Data — salting with paired fact-side key augmentation, dim-side row replication, and post-aggregation rollup — ~45m
- [remediation] Spark: The Definitive Guide — Ch. 19 §How Spark Performs Joins — hash partitioning and the co-location contract for equal keys — ~35m

</small>
</details>

<details>
<summary><samp>q5 · systems-distributed · leader-election-fencing-token · pre 3 → post 3 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A distributed job scheduler uses a coordination service (e.g., ZooKeeper/etcd) to elect a single leader that holds an exclusive lease on writing to a shared object store. Leases expire after 30 seconds and are renewed every 10 seconds. An on-call engineer reports a corruption incident: leader A experienced a 45-second GC pause, leader B was elected and started writing during the pause, then leader A woke up, still believed it held the lease (its in-process clock said only a moment had passed), and wrote stale data over B's writes. Explain (a) why a lease-and-clock-only design is insufficient to prevent this class of bug regardless of how short you make the lease, (b) what a fencing token is, the monotonicity property it must have, and how the object store must use it to make A's late write a no-op, and (c) what specifically must change on the storage side — not just the client — for fencing to actually work.

 

**Assessment:** The answer correctly locates the enforcement boundary — storage-side, at the ingest layer, before request acceptance — and recognizes that monotonicity, durability, and serialization must hold there. Two load-bearing articulation gaps remain after refinement: first, the lease+clock failure is attributed to TOCTOU and polling delay rather than to the lease holder's local clock being non-authoritative during an unbounded process pause; second, the storage-side comparison is described as a bitwise/divergence-index operation rather than as a monotonic greater-than check against a durable high-water mark with atomic accept-or-reject. The mechanism is named in the right neighborhood but the operator and the underlying invariant are not committed.

**Literature**

- [remediation] How to do distributed locking — §'Making the lock safe with fencing' — the fencing-token diagram and the storage-server rule: 'the storage server remembers that it has already processed a write with a higher token number, and so it rejects the request with token 33' — ~20m
- [remediation] Designing Data-Intensive Applications — Ch. 8 §'The Truth Is Defined by the Majority' — 'Fencing tokens' (pp. 301–304), and §'Process Pauses' (pp. 295–299) — ~45m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
