

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
industry     swe                                  updated         2026-05-18
scope        cross-domain · grab-bag              duration        1h 7m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  frontend           focus-management        ₃   2   ₂
q2  security           timing-attack           ₃   2   ₁
q3  backend            select-for-update-skip  ₃   3   ₂
q4  sre                log-cardinality         ₂   2   ₂
q5  systems-distributedread-replica-lag        ₃   3   ₂

gaps         constant-time-comparison · focus-management · keyboard-trap · log-cardinality-explosion

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · frontend · focus-management · pre 1 → post 2 · ceiling — · transitional b1–b2</samp></summary>

<small>

 

**Scenario:** A SaaS dashboard product has a custom React modal component used across the app for confirmation dialogs and forms. QA reports three issues from an accessibility audit: (1) when the modal opens, keyboard users tab through the underlying page elements behind the modal rather than only the modal's controls; (2) when the modal closes, focus lands at the top of the page rather than returning to the button that opened it; (3) screen reader users sometimes hear content from the page beneath the modal. Explain the mechanism behind each of these three failures (what the browser is actually doing in each case), then describe what a correct implementation must do for each. Be specific about which DOM/ARIA primitives are involved and why a CSS-only fix (e.g., z-index, pointer-events) cannot solve any of them.

 

**Refinement:** You said 'the modal is not treated as a leaf of the render tree'. Clarify: what specific browser behavior governs which elements are reachable via Tab key, and why tree position alone does not determine that behavior?

 

**Assessment:** The response correctly senses that the three failures are about something other than visual layering, and the refinement moves from a 'render tree leaf' model toward 'Tab iterates focusable elements via an attribute, not via tree position' — directionally right. However, none of the actual governing primitives are named: the attribute that controls tab reachability, the mechanism that hides a subtree from assistive technology, the API used to capture and restore focus across an open/close lifecycle, and the established UI pattern that bundles these as a single component contract. The CSS-only dismissal is asserted as 'attribute vs structural' without grounding it in why focus order and the accessibility tree are independent of paint and hit-testing. The gap is the WAI-ARIA dialog pattern and its three implementation primitives.

**Literature**

- [remediation] ARIA Authoring Practices Guide — Dialog (Modal) Pattern — Full pattern page: Keyboard Interaction, WAI-ARIA Roles/States/Properties, and the linked 'Modal Dialog Example' implementation notes — covers focus trap, role=dialog, aria-modal=true, focus restoration on close — ~45m
- [remediation] The inert attribute — MDN Web Docs — Full page: definition, effect on focus order, effect on the accessibility tree, and the 'Use cases — modal dialogs' subsection — ~20m

</small>
</details>

<details>
<summary><samp>q2 · security · timing-attack · pre 2 → post 2 · ceiling b1 · transitional b2</samp></summary>

<small>

 

**Scenario:** A company exposes a webhook receiver that authenticates incoming requests by checking an HMAC signature in the X-Signature header against an HMAC the server computes over the request body using a shared secret. The current implementation does the comparison with a standard string equality operator (`if computed_sig == header_sig`). A security researcher claims this is exploitable via a timing side channel even though the secret is never reflected in any response. Explain the mechanism: how can an attacker who only sees response latency learn information about the correct signature, and what is the attacker actually recovering (the secret? the expected signature? something else)? Then state the correct primitive to use and why it eliminates the leak. Finally, name one additional class of secret comparison in a typical web stack that has the same hazard.

 

**Refinement:** You said 'latency itself between the incoming request and the server compare check is a vector of which the attacker can get information about the HMAC sig details'. Clarify: what specific property of the byte-by-byte comparison loop causes response latency to vary with the attacker's input, and what does each measurement reveal about the target value?

 

**Assessment:** The response identified that a timing side channel was claimed and, after refinement, located the issue at the byte-by-byte comparison loop — a correct boundary observation. However, the underlying mechanism by which loop duration leaks information was not articulated; the answer attributed the latency variation to TOCTOU semantics and to cache hot/cold effects rather than to the behavior of the standard equality operator on mismatching bytes. The mitigation was likewise misidentified as 'a different signature/hash' rather than as a comparison-time primitive. The gap is in the operational behavior of standard string/byte equality and in the family of cryptographic-comparison primitives that exists specifically to neutralize it. The additional-example part of the question also requires naming a peer secret-comparison surface in the same hazard class.

**Literature**

- [remediation] Coda Hale, 'A Lesson In Timing Attacks (or, Don't use MessageDigest.isEquals)' — Full post — the canonical walkthrough of how standard byte-array comparison leaks through early-exit and how a constant-time XOR-OR loop fixes it; includes the byte-by-byte recovery attack and the corrected primitive in one short read. — ~15m
- [remediation] Python stdlib docs — hmac.compare_digest — hmac.compare_digest entry and the cross-referenced secrets.compare_digest — the API note explicitly states the function 'uses an approach designed to prevent timing analysis by avoiding content-based short circuit behaviour,' and lists the comparison surfaces it is meant for (HMACs, tokens, secrets). — ~10m

</small>
</details>

<details>
<summary><samp>q3 · backend · select-for-update-skip-locked · pre 2 → post 3 · ceiling b1 · transitional b2–b3</samp></summary>

<small>

 

**Scenario:** A team is building a background job worker pool in Python against Postgres. Jobs live in a `jobs` table with columns `(id, status, run_at, payload)`. Workers poll for ready jobs with `SELECT id FROM jobs WHERE status = 'ready' AND run_at <= now() ORDER BY run_at LIMIT 10` and then update the rows to `'running'`. With 20 workers polling every second they observe: most workers pick up the same rows and only one wins the update, the other 19 do wasted work; under load some workers block for seconds on the SELECT. The senior on the team suggests changing the query to `SELECT id FROM jobs WHERE status = 'ready' AND run_at <= now() ORDER BY run_at LIMIT 10 FOR UPDATE SKIP LOCKED` and doing the status update in the same transaction. Explain what `FOR UPDATE SKIP LOCKED` does at the row-lock level, why it fixes both the duplicate-work problem and the blocking problem, and what tradeoff it introduces that plain `FOR UPDATE` does not have. Dismiss the alternative of using application-level distributed locks (e.g., a Redis lock per job id) on a specific tradeoff axis.

 

**Refinement:** You said 'the ready probe is fail closed, because the job is run on that row and returns not ready due to access being gated'. Clarify: what specifically happens at the row-lock level that causes a competing worker's SELECT to skip the locked row rather than block on it, and how that differs from the behavior of plain FOR UPDATE.

 

**Assessment:** The original answer recognized the row-level locking pattern and the directional fix, but the mechanism by which SKIP LOCKED differs from plain FOR UPDATE was substituted with invented vocabulary ('fail closed on the ready probe'). The refinement narrowed the gap — the enqueue-vs-skip contrast is correct in shape — but the answer remains hedged, speculates that indexing is the arbitration site (it is not), and never names the actual tradeoff that the question explicitly asks for. The dismissal of Redis distributed locks lands on an off-axis distinction rather than the concrete property the question is probing.

**Literature**

- [remediation] PostgreSQL Documentation — The Locking Clause (SELECT ... FOR UPDATE / SKIP LOCKED) — §SELECT — The Locking Clause: subsections on FOR UPDATE and on NOWAIT / SKIP LOCKED behavior, including the explicit note that SKIP LOCKED returns an inconsistent view of the data. — ~20m
- [remediation] What's the Difference Between FOR UPDATE and FOR UPDATE SKIP LOCKED? — Full post — a focused walkthrough of the job-queue use case showing concurrent transactions, how plain FOR UPDATE blocks and serializes workers, and how SKIP LOCKED produces disjoint batches. — ~15m

</small>
</details>

<details>
<summary><samp>q4 · sre · log-cardinality-explosion · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** An on-call engineer at a mid-sized SaaS company is investigating why their logging bill from a managed log provider has tripled in three months while traffic only grew 20%. They discover that ingest volume is dominated by a handful of services that recently adopted structured logging. On inspection, log lines from these services include fields like `request_id`, `user_id`, `trace_id`, and a free-form `error_message` that includes stack traces with memory addresses. Their alerting backend (a metrics system) is also slow when querying by service. Explain why high-cardinality fields are expensive in two distinct ways depending on whether they land in a log indexing system or a metrics system — what data structure each system maintains and how cardinality affects it. Then describe the discipline a team should adopt to keep observability useful: which fields belong in logs vs. metrics vs. traces, and why `user_id` is fine in one of those three places but ruinous in another.

 

**Refinement:** You said 'metrics system which uses numeric data/aggregated data by types'. Clarify: what specific data structure a metrics system maintains per label combination, and how adding a high-cardinality label like `user_id` causes that structure to grow in a way that differs from adding more time-series data points.

 

**Assessment:** The answer identified that cardinality drives observability cost but misnamed the underlying data structures in both systems — log indexing was described as a B-tree rather than an inverted index, and the metrics-system unit was described as 'the numeric data itself' rather than the per-label-combination time series. The refinement probe specifically asked for the structure metrics systems maintain per label combination and how it grows differently from data-point appends; the response reframed the question as character-base entropy (base-10 vs base-36) instead of naming the active-series multiplication. The discipline guidance was also inverted: the response placed user_id and request_id into logs as a way to make indexing 'load bearing,' but did not state the rule that high-cardinality identifiers must be kept out of metric labels and belong in logs/traces for a structural reason. The gap is in the canonical telemetry-system data structures and the cardinality-vs-samples distinction.

**Literature**

- [remediation] Observability Engineering — Ch. 1 'What Is Observability?' and Ch. 2 'How Debugging Practices Differ Between Observability and Monitoring' — the cardinality distinction between metrics and event-based telemetry, and why high-cardinality fields are the unit of value in logs/traces but the unit of cost in metrics — ~1h 30m
- [remediation] Prometheus Documentation — Naming and Labels — Practices §Labels and Practices §Instrumentation §Things to watch out for — 'CAUTION: Remember that every unique combination of key-value label pairs represents a new time series, which can dramatically increase the amount of data stored.' — ~15m

</small>
</details>

<details>
<summary><samp>q5 · systems-distributed · read-replica-lag-routing · pre 2 → post 3 · ceiling b1 · transitional b2–b3</samp></summary>

<small>

 

**Scenario:** An e-commerce platform routes reads to a pool of asynchronous Postgres read replicas and writes to the primary. Customers report a recurring bug: after submitting a product review (write to primary), the next page load shows the product page without their review, but a refresh 2-3 seconds later shows it. The team's first instinct is to route all reads to the primary for 5 seconds after any write from that user. Explain why this 'sticky-to-primary window' approach is a fragile fix — what specifically goes wrong under (a) load balancer rotation across multiple app servers, (b) the customer opening the page on a second device, and (c) a replica that happens to be 8 seconds behind. Then describe the correct mechanism that gives this customer read-your-writes consistency without sending all their reads to the primary. Name the specific primitive the application has to track and how the replica routing decision is made from it.

 

**Refinement:** You said 'the replica routing does this through fencing tokens and access to the LSN of the replicas and dbs, and routes accordingly as the write is propogated throughout the system'. Clarify: what specific value does the application capture at write time, where does it store that value between requests, and what comparison against replica state causes the router to accept or reject a given replica for the next read?

 

**Assessment:** The answer correctly rejects sticky-to-primary and identifies that read-your-writes requires a per-write ordering token compared against per-replica applied state. The post-refinement turn produces a worked example of the comparison shape (replica applied-state ≥ user's write-state ⇒ route). Two gaps remain: the primitive is misnamed as a fencing token (which is a lock-safety primitive, a different concern), and the token's storage location is placed at the load balancer rather than in per-user session state — a placement that fails exactly the second-device case the question probed. The fix is to read the canonical session-consistency-via-LSN pattern and the fencing-token chapter back-to-back so the two primitives become disambiguated.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 5 §Problems with Replication Lag — 'Reading Your Own Writes' and 'Monotonic Reads', pp. 161–168 — ~2h
- [remediation] Designing Data-Intensive Applications — Ch. 8 §The Truth Is Defined by the Majority — 'Fencing tokens', pp. 301–304 — ~45m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
