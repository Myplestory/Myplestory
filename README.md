

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
industry     swe                                  updated         2026-06-10
scope        cross-domain · grab-bag              duration        1h 12m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  sre                dns-ttl-failover        ₃   3   ₂
q2  ai-llm             reranker-cross-encoder  ₃   3   ₂
q3  frontend           search-as-you-type      ₃   3   ₂
q4  backend            soft-delete-vs-hard     ₃   3   ₁
q5  data-engineering   medallion-architecture  ₅   3   ₃

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · sre · dns-ttl-failover-tradeoff · pre 2 → post 3 · ceiling b1 · transitional b2–b3</samp></summary>

<small>

 

**Scenario:** Company X runs a public API behind a single A-record (api.example.com) pointing at the active region's load balancer IP. During a regional outage their runbook is: update the DNS record to point at the standby region's IP with a 60-second TTL. In the post-incident review, a chunk of traffic kept hitting the dead IP for 20+ minutes despite the record having flipped. Explain the mechanism behind why a low TTL did not guarantee fast cutover — be specific about what TTL actually controls and which parties in the resolution path can ignore it. Then explain why a stable Anycast/VIP fronted by health-checked load balancers moves the failover decision to a different layer, and what that buys you over DNS-based failover. Name the tradeoff that approach introduces (it is not free).

 

**Refinement:** You said 'TTL bounds the time to live on that one load balancer nameserver/records, not access from consumer side'. Clarify: which specific actors in the resolution chain are permitted by protocol to serve a cached answer past TTL expiry, and what mechanism gives them that permission?

 

**Assessment:** The response correctly identifies that low TTL did not guarantee cutover because the record is cached below the authoritative server, and the refinement honestly retracts the original (wrong) claim that TTL is enforced 'at the load balancer nameserver.' However, it still misidentifies which actors in the resolution path are protocol-permitted to serve stale answers — conflating CDN/edge caches with recursive and stub/client resolvers — and the explanation of why Anycast/VIP moves failover to another layer invents a DNS-cache-invalidation flow rather than describing routing-layer (BGP/health-check) failover. The named tradeoff is also off-target. Read the cited DNS-TTL and Anycast sources to pin which caching parties ignore TTL and why the Anycast/VIP tradeoff is operational/routing complexity, not bandwidth.

**Literature**

- [remediation] Site Reliability Engineering — Ch. 19 'Load Balancing at the Frontend' §DNS, §Virtual IP Addresses, §Anycast — ~30m
- [remediation] RFC 1035 / RFC 8767 (Serve-Stale) — RFC 1035 §3.2.1 and §7 (TTL as caching maximum-hint); RFC 8767 (resolver serve-stale behavior) — ~25m

</small>
</details>

<details>
<summary><samp>q2 · ai-llm · reranker-cross-encoder · pre 3 → post 3 · ceiling b1 · transitional b2–b3</samp></summary>

<small>

 

**Scenario:** A SaaS support-assistant team has a RAG pipeline that does bi-encoder dense retrieval (cosine over precomputed embeddings) and feeds the top-50 chunks to the LLM. Answer quality is mediocre — relevant passages are in the top-50 but not the top-5 the model actually attends to. A teammate proposes adding a cross-encoder reranker as a second stage over the top-50. Explain the mechanism: how does a cross-encoder score a (query, passage) pair differently from the bi-encoder, and why does that produce better relevance ordering? Then explain WHY the cross-encoder cannot simply replace the bi-encoder as the first-stage retriever over the full corpus — what property of the bi-encoder makes first-stage retrieval over millions of chunks tractable that the cross-encoder lacks? Finally, name the ceiling this two-stage design cannot cross: if a relevant passage is absent from the top-50, what does reranking do for it, and why?

 

**Refinement:** You said 'the cross encoder comprehensively matches and ranks out of those candidates'. Clarify: what happens inside the cross-encoder's forward pass — specifically, what interaction between query tokens and passage tokens occurs that is absent when the bi-encoder encodes each independently — that makes the cross-encoder's relevance score higher fidelity?

 

**Assessment:** The answer correctly partitions the two-stage design — cheap bi-encoder candidate generation, expensive cross-encoder rerank, and a recall ceiling — but mischaracterises the single mechanism the question turns on. It repeatedly attributes the cross-encoder's fidelity gain to scoring queries against each other, whereas the gain comes from query tokens and passage tokens attending to each other inside one joint forward pass. The 'cannot replace the bi-encoder' answer never names the load-bearing property (passage embeddings are precomputable for the bi-encoder but a cross-encoder score is irreducibly per-(query,passage)-pair, so first-stage use would require a full forward pass over every chunk). The refinement probe asked exactly for the token-interaction detail and the answerer self-reported that the primitive eluded them — the gap did not close.

**Literature**

- [remediation] Passage Re-ranking with BERT — §3 Method — the [CLS] query [SEP] passage [SEP] input construction and how the joint encoding yields the relevance score (one focused section) — ~20m
- [remediation] Retrieve & Re-Rank — The 'Bi-Encoder vs. Cross-Encoder' subsection plus the retrieve-then-rerank diagram — why no independent embeddings exist for cross-encoders and why that forbids first-stage use over large collections — ~15m

</small>
</details>

<details>
<summary><samp>q3 · frontend · search-as-you-type · pre 2 → post 3 · ceiling — · transitional b1–b3</samp></summary>

<small>

 

**Scenario:** A frontend team builds a search-as-you-type box that fires a request on each keystroke and renders whatever response arrives. Users report that after typing quickly, the results panel sometimes shows results for a partial query (e.g. 'reac') even though the box reads 'react hooks'. Decompose the problem into the three independent concerns at play. (1) For the keystroke cadence: contrast debounce vs throttle and state which one fits this workload and why. (2) For the in-flight requests: name the mechanism that cancels superseded requests so an older one cannot resolve into the UI, and where in the component lifecycle you wire it. (3) For the response-ordering failure itself: explain precisely why a trailing-edge debounce timer used ALONE does not fix it (give the request-A-then-request-B trace), and name the reconciliation primitive you'd use when request cancellation is unavailable. Also state why a backend circuit breaker / retry-with-backoff does NOT address this ordering bug.

 

**Refinement:** You said 'the timer does not take into account serverside processing delays/the visibility in the ordering the server sees, not the egress from clientside'. Clarify: walk through the specific request-A-then-request-B sequence that produces the stale render even when both requests are fired from a single debounced emission.

 

**Assessment:** The answer correctly chooses debounce for cadence and correctly argues that a backend circuit breaker / retry-with-backoff cannot fix a race determined on the client receive path, and the refinement does produce an ordered A-then-B trace plus a gesture at a monotonic ordering token. The gaps are (1) the in-flight cancellation mechanism is never named as the standard frontend primitive wired into the effect cleanup — it is replaced by an inbox/outbox server pattern; (2) the reconciliation is described as a CAP / two-systems consensus problem rather than the canonical single-client response-order race with its specific client-side reconciliation primitive; and (3) the A-then-B trace relies on network drop/retry rather than the simpler two-debounced-fires-resolving-out-of-order case the question asked for. Read the cancellation-in-cleanup and request-sequence-reconciliation references to see the named primitive and where it wires.

**Literature**

- [remediation] AbortController — Web APIs — AbortController — 'Examples' and 'signal' subsection (the abort()-on-fetch cancellation pattern) — ~15m
- [remediation] A Complete Guide to useEffect — race conditions in fetch — 'A Complete Guide to useEffect' — the data-fetching race-condition subsection (response order independent of request order; cancellation flag / AbortController in cleanup) — ~20m

</small>
</details>

<details>
<summary><samp>q4 · backend · soft-delete-vs-hard-delete · pre 2 → post 3 · ceiling — · transitional b1–b3</samp></summary>

<small>

 

**Scenario:** A backend team adds soft-delete (a deleted_at timestamp, NULL when active) to a users table that already has a UNIQUE constraint on email. After deploying, two problems surface: (a) a user who deletes their account can no longer re-register with the same email — the insert fails; (b) an admin 'active user count' report is now slightly inflated. Explain the mechanism behind each. For (a), say precisely why the existing unique constraint collides with the soft-deleted row, and give the exact index construct that enforces 'unique among active rows only' — state the predicate and why a NULL deleted_at row satisfies it. For (b), explain why the count went wrong and what invariant every read query now carries. Finally, name one cost soft-delete imposes that hard-delete does not, beyond these two bugs.

 

**Refinement:** You said 'the pure unique constraint scopes the access to only readtime, and the row is declared as alive by postgres therefore the insert fails'. Clarify: what property of the UNIQUE index — separate from any locking — causes the second INSERT to be rejected even when the first row has a non-NULL deleted_at value?

 

**Assessment:** Across both turns the answer correctly reaches for the partial unique index as the remediation but never satisfies the B3 mechanism gate: it never states the index predicate, never explains why a NULL deleted_at row is included in (and a non-NULL row excluded from) the index, and instead constructs an invented lock taxonomy ('shared exclusive', 'read-only exclusive', 'ON CONFLICT lever'). The refinement probe specifically asked for the index property separate from locking, and the answer doubled down on locking rather than identifying that the plain UNIQUE index covers all rows including the soft-deleted one. The (b) count explanation also misses that no implicit filtering occurs and the per-query WHERE deleted_at IS NULL invariant, and the named extra cost (write ordering/versioning serialization) is not the retention/filter-obligation cost soft-delete actually imposes. The gap is in why index coverage — not locking — produces the collision.

**Literature**

- [remediation] PostgreSQL Documentation — Partial Indexes — §11.8 Partial Indexes — the example building a UNIQUE partial index with a WHERE predicate, and §11.5 Unique Indexes for why a plain unique index covers all rows — ~30m
- [remediation] Patterns of Enterprise Application Architecture / Time Narrative — Soft Delete tradeoffs — The section on retaining historical rows and the obligation it imposes on every read query — ~15m

</small>
</details>

<details>
<summary><samp>q5 · data-engineering · medallion-architecture · pre 3 → post 3 · ceiling b1–b2 · transitional b3–b5</samp></summary>

<small>

 

**Scenario:** A data team is designing a lakehouse and standardizes on a bronze/silver/gold (medallion) layering. A reviewer pushes back: 'Why not just land cleaned, conformed data directly into silver and skip bronze — bronze is duplicated storage of raw data we already have upstream.' Defend the layering by articulating the distinct PURPOSE of each layer and the mechanism each enables. Specifically: (1) what does keeping raw, append-only bronze give you that a silver-only design loses — frame this in terms of replay/reprocessing when a transformation bug or a schema-evolution requirement is discovered downstream. (2) What does silver cost you that bronze does not — name the lossy operations (dedup, conformance, type coercion) and why they are irreversible once you discard the raw rows. (3) What rigidity does a gold aggregate introduce that silver avoids, and what happens when the required aggregation grain changes? Commit to whether the reviewer's shortcut is acceptable and on what axis you'd reject it.

 

**Refinement:** You said 'roll backs are cheap on corrupted upstream normalization/dedupe at silver and gold tiers'. Clarify: what property of append-only bronze makes replay produce a deterministically identical result when the transformation logic itself has changed, rather than just restoring a prior snapshot?

 

**Assessment:** The response correctly identifies the purpose of each medallion layer, names the lossy silver operations (dedup, coercion, conformance), articulates the gold grain-change blast radius, and commits firmly that the reviewer's shortcut is unacceptable. The targeted probe asked for the specific property of append-only bronze that makes replay deterministically reproduce a result when the transformation LOGIC has changed (as opposed to restoring a prior output snapshot). The refinement answers with ingest-time causal ordering (watermarks, hybrid clocks) rather than the load-bearing point that bronze is the immutable INPUT and replay means recomputing from raw with the new code — the distinction between regenerating a derived view and restoring a checkpoint is the gap. Read the cited replay/event-sourcing material to see why the immutable-input framing, not ordering, is what makes replay reproduce changed logic.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 11 §Event Sourcing and §The Unbundled Database, pp. 457–465 — raw-log replay as the substrate for deriving all downstream views — ~2h 30m
- [remediation] Delta Lake: The Definitive Guide — Ch. 9 §Medallion Architecture — the reprocessing contract bronze provides and the silver conformance/loss tradeoff — ~45m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
