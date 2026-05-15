

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
industry     swe                                  updated         2026-05-15
scope        cross-domain · grab-bag              duration        1h 5m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  systems-distributed                        ₄   3   ₂
q2  backend                                    ₃   3   ₂
q3  security                                   ₂   2   ₂
q4  sre                                        ₄   3   ₃
q5  ai-llm                                     ₂   2   ₁

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · systems-distributed ·  · pre 2 → post 3 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A multi-tenant analytics SaaS shards customer event ingestion across 16 backend nodes using a simple `hash(tenant_id) % N` scheme. Operations wants to scale to 24 nodes next quarter, and the team has also noticed that two enterprise tenants account for ~40% of total event volume, causing those shards to run hot. A staff engineer proposes switching to consistent hashing with virtual nodes. Explain (a) the specific mechanism by which `hash % N` makes the 16→24 rescale operationally painful and how consistent hashing changes that picture, (b) why virtual nodes are needed on top of a basic consistent-hashing ring rather than just placing each physical node once, and (c) what consistent hashing does NOT solve in this scenario — be concrete about what the team still has to handle for the two heavy tenants.

 

**Assessment:** Part (a) of the answer arrived correctly after the refinement probe: the remapping fraction under modulo is large (the answerer arrived at 33–50% framing, with the actual figure closer to ~94% for 16→24), and consistent hashing produces a more bounded remapping profile. Part (b) is the load-bearing gap — virtual nodes are framed as a hardware-isolation / backpressure-safety construct, which is not their purpose. Their purpose is load smoothing on the hash ring (reducing arc-length variance) and parallelizing rebalancing across many source nodes. Part (c) reaches for generic tail-latency and SRE concerns rather than the concrete and decisive point that consistent hashing cannot subdivide a single key, and the two whale tenants are each a single key. The literature points at the canonical sources for each gap.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 6 §Partitioning, 'Partitioning by Hash of Key' and 'Rebalancing Partitions' (pp. 203–218) — ~3h 45m
- [remediation] Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web — §3 Consistent Hashing — properties of monotonicity, balance, and spread (focused read of §3 only) — ~45m

</small>
</details>

<details>
<summary><samp>q2 · backend ·  · pre 2 → post 3 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A B2B order-management backend on PostgreSQL needs to publish an `OrderPlaced` event to Kafka every time an order row is inserted. The current code does `INSERT INTO orders ...; producer.send('orders', event); COMMIT;` inside a service method. The team has observed two intermittent bugs: (1) some orders exist in the database but no event was ever consumed downstream, and (2) some downstream consumers process an event whose corresponding order row cannot be found. Explain the underlying mechanism that causes both bugs (be specific about what is and isn't atomic across the two systems), then describe the outbox pattern as a remediation: what table you add, what the write path looks like inside the transaction, and what separate component is responsible for getting rows from that table to Kafka. Finally, identify one tradeoff or operational concern the outbox pattern introduces that the original code did not have.

 

**Assessment:** The answer recognizes that the INSERT, the send, and the COMMIT are sequenced incorrectly and, after the refinement, pairs each independent outcome to one of the two observed bugs — which is the right diagnostic shape. The gap is in naming the actual primitive: that Postgres and Kafka are two separate systems with no shared transaction coordinator, so 'atomicity' in the ACID sense was never on offer for the publish step. The outbox sketch reaches for 'LSN or WAL' and a 'materializer', conflating Postgres-internal write-ahead logging with an application-level outbox table written in the same transaction and drained by a relay; the at-least-once nature of that relay, and the corresponding consumer-side idempotency contract, are not surfaced as the substantive tradeoff.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 11 §Keeping Systems in Sync — Dual Writes (pp. 452–457) and §Total Order Broadcast / Idempotent Consumers — ~1h 30m
- [remediation] Pattern: Transactional Outbox — Full pattern page: 'Problem', 'Solution', 'Example', 'Resulting context' — including the relay variants (polling publisher vs. transaction-log tailing) and the at-least-once delivery consequence — ~25m

</small>
</details>

<details>
<summary><samp>q3 · security ·  · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A customer-support web app renders ticket comments authored by end users. The team currently sanitizes input on the way in by stripping `<script>` tags with a regex before storing the comment in the database. A penetration test report flags a stored XSS vulnerability: the tester managed to execute JavaScript by submitting a comment containing `<img src=x onerror=alert(1)>`. Explain (a) why input-time tag stripping is the wrong layer to defend against this and what the correct defense layer is — name the specific mechanism, (b) how the choice of *where the untrusted string is rendered* (HTML body text vs. an HTML attribute vs. inside a `<script>` block vs. a URL) changes what counts as 'correct' encoding, and (c) what a Content Security Policy contributes here that output encoding alone does not, and what CSP does NOT protect against in this scenario.

 

**Assessment:** The response correctly diagnoses that <script>-tag stripping is insufficient, but inverts the canonical defense layer: it identifies input-time validation/encoding as the fix, where the canonical answer is context-aware output encoding applied by the template engine at render time. The per-context sub-question (b) — which encoder applies to HTML body vs. attribute vs. <script> vs. URL — is answered in terms of DOM render order rather than in terms of distinct encoder functions per sink, indicating the underlying model is missing. The refinement softens the wrong-layer claim and adds defense-in-depth language but does not surface output encoding as the gating primitive, and CSP's specific limitations in this scenario (DOM-based XSS, allowlisted-origin exfiltration, non-script injection) are not named — only an irrelevant SSRF exclusion is offered.

**Literature**

- [remediation] OWASP Cross-Site Scripting Prevention Cheat Sheet — §'Output Encoding' and Rules #1–#5 (HTML body, attribute, JavaScript, CSS, URL contexts) — ~30m
- [remediation] OWASP Content Security Policy Cheat Sheet — §'What CSP is not' and §'Strict CSP' (nonces/hashes, blocking 'unsafe-inline') — ~25m

</small>
</details>

<details>
<summary><samp>q4 · sre ·  · pre 3 → post 3 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A payment service calls a downstream fraud-scoring API. Both services run behind autoscaled fleets. During a brief 90-second incident in which the fraud API returned 503s on ~30% of requests, the payment service's monitoring showed that even *after* the fraud API fully recovered, payment latency stayed elevated for another ~6 minutes and several payment pods OOMed. The payment client currently retries failed calls up to 3 times with a fixed 200ms delay between attempts. Explain (a) the specific mechanism by which the existing retry policy turned a partial-failure incident into a longer self-inflicted incident — be concrete about what is being amplified and where, (b) what exponential backoff with jitter changes about that mechanism and why jitter (not just exponential growth) is the load-bearing part, and (c) one additional control beyond retry tuning that the payment service should add so a future fraud-API brownout doesn't propagate the same way, and what it gives up.

 

**Assessment:** The response correctly identifies retry amplification and synchronized cadence as the mechanism, and the refinement gives a defensible reason why randomness (not deterministic spread) is required — coordination-free local decisions can only produce global spread via entropy. Two gaps remain that bound this to B3 score 3. First, the question explicitly asked where the amplification lands; the payment-pod OOM is the load-bearing 'where' (in-flight request state — threads, connection-pool slots, request buffers — held for the full retry duration on the caller side, not just the callee), and this is never named. Second, the requested 'additional control beyond retry tuning' is answered with retry bounding, which is still retry tuning; the canonical beyond-retry controls (circuit breaker, retry budget / token bucket, load shedding with deadline propagation) and their specific tradeoffs are missing.

**Literature**

- [remediation] Exponential Backoff and Jitter — Full article (full jitter vs equal jitter vs decorrelated jitter; the simulation showing why exponential growth alone still produces herds) — ~15m
- [remediation] Site Reliability Engineering — Ch. 22 'Addressing Cascading Failures' §Preventing Server Overload and §Client-Side Throttling; Ch. 21 'Handling Overload' §Retry Budgets — ~45m

</small>
</details>

<details>
<summary><samp>q5 · ai-llm ·  · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A team is building a customer-facing LLM feature with two modes: a 'rewrite this email more politely' mode and a 'brainstorm 5 marketing taglines' mode. They're using the same model and currently call it with `temperature=0.7, top_p=1.0` for both. The rewrite mode occasionally produces outputs that change the user's intended meaning; the brainstorm mode occasionally produces five taglines that all sound nearly identical. Explain (a) what temperature actually does to the next-token probability distribution at the decode step, and what top_p (nucleus sampling) does that is distinct from temperature — they are not redundant, (b) which mode wants which settings and why, given the symptoms described, and (c) why setting `temperature=0` does NOT make outputs fully reproducible across runs in a production API setting — name at least one concrete source of remaining non-determinism.

 

**Assessment:** The answer treats decode-time sampling as a transformer-internal phenomenon (gradients, matmul, activation) rather than as a post-logit reshape-and-truncate pipeline applied at the sampling step. The mode-to-setting recommendation is inverted relative to the symptoms, and the temperature=0 sub-question is answered with a categorical misconception (that it disables the model) rather than an analysis of why greedy decoding still varies in a real API. The refinement probe narrowed in on exactly the right gap — the operation temperature performs on the logit vector — and the answer did not converge.

**Literature**

- [remediation] The Curious Case of Neural Text Degeneration — §3 'Nucleus Sampling' and §2 'Background: Decoding from Language Models' — focused chapter covering temperature scaling of logits, top-k, and the nucleus (top-p) truncation procedure end-to-end — ~45m
- [remediation] Defeating Nondeterminism in LLM Inference — Full post — sections 'The Hypothesis' through 'Batch Invariance' — covers why greedy/temp=0 is not bitwise reproducible (batch-dependent floating-point reductions, kernel non-associativity) — ~30m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
