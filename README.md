

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
industry     swe                                  updated         2026-05-29
scope        cross-domain · grab-bag              duration        50m 34s
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  security           jwt-algorithm           ₃   3   ₂
q2  sre                noisy-neighbor          ₂   2   ₂
q3  backend            api-rate-limiting       ₃   3   ₂
q4  systems-distributedtwo-phase-commit        ₃   3   ₂
q5  data-engineering   streaming-join-state    ₂   2   ₂

gaps         cgroup-resource-limits · cpu-throttling-vs-oom · noisy-neighbor-isolation · state-store-unbounded-growth

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · security · jwt-algorithm-confusion · pre 2 → post 3 · ceiling — · transitional b1–b3</samp></summary>

<small>

 

**Scenario:** A SaaS platform issues JWTs signed with RS256. The auth library on the resource server is configured to accept a list of allowed algorithms and uses the IdP's public key (fetched from a JWKS endpoint) for verification. A code review reveals that the allowed-algorithms list is `['RS256', 'HS256']`. Explain the specific attack this configuration enables, the mechanism by which the verifier is tricked into accepting an attacker-forged token, and the correct fix. Why is it insufficient to simply 'rotate the signing key' if this misconfiguration is discovered in production?

 

**Refinement:** You said 'the public key can somehow be cross referenced with the HS256 algorithm, and therefore tricked into accepting an attacker token'. Clarify: what specific bytes does the attacker use as the HS256 secret, and why does possessing those bytes let them produce a signature the verifier accepts?

 

**Assessment:** Post-refinement, the answer reaches the load-bearing fact — the attacker uses the RSA public key bytes as the HS256 secret — but the supporting explanation describes a broken model of asymmetric cryptography ('combined keys to decode', 'his own HS256 private key') and never names the canonical mechanism: the verifier selects its verification routine from the attacker-controlled `alg` header. The fix proposal correctly tightens the allowlist but bundles in unrelated session-hardening (short TTLs, session cookies on every endpoint) that conflates this JWT-specific vulnerability with general web-session hygiene. The rotation-is-insufficient argument is directionally right but unjustified: the answer says 'rotation won't save the attacker from spoofing' rather than explaining that the rotated public key is itself published on JWKS and immediately reusable as the HMAC secret.

**Literature**

- [remediation] Critical vulnerabilities in JSON Web Token libraries — Full post — 'Meet the alg header' through 'The Fix' (the canonical disclosure of RS256→HS256 algorithm confusion, including the exact attack: signing a forged token with the public key as HMAC secret) — ~20m
- [remediation] OWASP JSON Web Token for Java Cheat Sheet — §'None Hashing Algorithm' and §'Token Sidejacking' — the algorithm-selection family of attacks and the prescribed fix (pin the verifier to one algorithm, bind key to algorithm) — ~15m

</small>
</details>

<details>
<summary><samp>q2 · sre · noisy-neighbor-isolation · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A team runs ~40 microservices on a shared Kubernetes cluster. One service (a batch report generator) periodically consumes large amounts of CPU, and during those windows unrelated latency-sensitive services on the same nodes see p99 latency rise 3–5×. The team sets a CPU limit of 2 cores on the report generator. After the change, the report generator itself frequently fails its readiness probe and gets killed by the kubelet, while the latency-sensitive services still occasionally see degradation. Explain (a) the mechanism by which CPU limits cause the report generator's probe failures (vs how memory limits would behave), (b) why setting a CPU *limit* did not fully fix the noisy-neighbor problem, and (c) what combination of CPU requests, limits, and scheduling controls actually achieves the desired isolation.

 

**Refinement:** You said 'the cpu limit is a consumer fix'. Clarify: what is the specific kernel scheduling mechanism that causes the report generator's readiness probe to time out under a CPU limit, as opposed to the process being terminated by an OOM killer under a memory limit?

 

**Assessment:** The answer correctly framed the problem as noisy-neighbor contention and intuited that the CPU limit was the wrong primary lever, but the mechanism-level claims are inverted: part (a) attributes the probe failure to memory pressure and OOM under CPU cap, when the actual mechanism is the Linux CFS bandwidth controller throttling the cgroup at quota exhaustion within a 100ms period, descheduling the probe handler. The refinement directly asked for that kernel scheduling mechanism and the response substituted generic syscall/scheduler vocabulary (task scheduler queueing, mutex vs futex, pipe costs) rather than CFS quota/period throttling. Part (c) reached for application-protocol stability patterns (backoff, jitter, DLQ, circuit breaker, bulkhead) which do not apply to a single CPU-bound batch process being throttled by the kernel; the canonical answer involves CPU requests vs limits semantics, QoS classes, and node-level scheduling isolation (taints, affinity, dedicated pools). The gap is in the cgroup / CFS / Kubernetes-scheduler primitives layer.

**Literature**

- [remediation] Kubernetes Documentation — Resource Management for Pods and Containers — Full document, with focus on §How Pods with resource limits are run (CFS quota), §Requests and limits, and §Configure default CPU requests and limits for a namespace; plus the linked QoS classes page. — ~45m
- [remediation] Understanding Linux Container Scheduling (CFS Bandwidth Control and Kubernetes CPU Throttling) — Full article — covers cpu.cfs_quota_us / cfs_period_us mechanics, why throttling causes p99 latency spikes and probe failures, the kernel 5.4 fix, and the operational guidance on when to drop CPU limits entirely. — ~30m

</small>
</details>

<details>
<summary><samp>q3 · backend · api-rate-limiting-algorithm · pre 2 → post 3 · ceiling b1 · transitional b2–b3</samp></summary>

<small>

 

**Scenario:** A backend team is adding per-API-key rate limiting (e.g., 100 requests/minute per key) to a public REST API served by ~20 stateless application instances behind a load balancer. An engineer proposes a Redis-backed fixed-window counter: `INCR key:{api_key}:{minute}` with a 60-second TTL, reject if > 100. Explain (a) the specific 'burst at the window boundary' failure mode of this design and quantify the worst-case burst a client can achieve, (b) how a token bucket (or sliding-window log/counter) algorithm differs mechanically and why it eliminates that burst, and (c) the tradeoff that token bucket pays vs the fixed-window counter — what is more expensive about it in Redis terms?

 

**Refinement:** You said 'The worst case burst a client can achieve under this design is 100 + 99 + .... 1 throughout the 1 minute window (sliding)'. Clarify: what is the exact maximum number of requests a client can fire in a short time span at the boundary between two fixed windows, and what window-boundary timing produces that number?

 

**Assessment:** The answer recognizes the algorithm family (fixed window, token bucket, sliding window log/counter) but does not articulate the mechanism that produces the boundary burst. The initial response offered the wrong quantification (a triangular-sum series rather than the straddling-boundary 200) and inverted the Redis cost tradeoff, claiming fixed-window is more expensive than token bucket. The refinement recovered the correct burst quantification (200) and corrected the cost ordering, but attributed the burst cause to instance statelessness rather than to the atomic window reset at the boundary — a mechanical confusion about where the failure originates. The Redis cost analysis remains qualitative; nothing concrete about token-bucket Lua atomicity or sorted-set memory growth.

**Literature**

- [remediation] System Design Interview – An Insider's Guide, Volume 1 — Chapter 4: Design a Rate Limiter — covers fixed window, sliding window log, sliding window counter, token bucket, and leaky bucket with mechanism diagrams and Redis implementation sketches. — ~1h 30m
- [remediation] How we built rate limiting capable of scaling to millions of domains — Full post — covers the boundary-burst problem of fixed windows, the GCRA/token-bucket family, and the Redis state cost of each approach with concrete Lua sketches. — ~25m

</small>
</details>

<details>
<summary><samp>q4 · systems-distributed · two-phase-commit-blocking · pre 2 → post 3 · ceiling — · transitional b1–b3</samp></summary>

<small>

 

**Scenario:** A payments platform needs to debit a wallet (Service A, Postgres) and credit a merchant ledger (Service B, separate Postgres in a different bounded context) as part of a single business transaction. An architect proposes two-phase commit (2PC) across both databases via XA. A second architect proposes a saga: debit wallet → publish event → credit ledger, with a compensating 'refund wallet' action on credit failure. Explain (a) the specific failure mode of 2PC that makes it operationally fragile in this microservices setup (be precise about which phase and which participant state causes the problem), (b) why the saga gives up serializability and what business-visible anomaly the user can observe between the two steps, and (c) what mechanism the saga consumer must implement so that retries of the credit step do not double-credit the merchant.

 

**Refinement:** You said 'At most once semantics, at both user debitting time and merchant attempt'. Clarify: what property of an idempotency key prevents a retry of the credit step from being treated as a new, distinct transaction by the merchant ledger service?

 

**Assessment:** The answer recognizes the saga vs 2PC framing and, after refinement, correctly identifies that an idempotency key prevents double-credit via key collision at write time — satisfying the B3 mechanism floor for part (c). The unresolved gap is part (a): the precise reason 2PC is fragile in microservices is never named — specifically, the coordinator-failure-after-PREPARE scenario where participants are stuck in the 'in-doubt' / prepared state holding locks and cannot unilaterally commit or abort. The answer describes generic atomicity-failure-during-commit, which is the problem 2PC is designed to solve, not the failure mode of 2PC itself. Secondary gap: 'at-most-once' semantics is named for the credit step where the correct semantic is effectively-once (at-least-once delivery + idempotent dedup); this terminological misuse signals that the dedup mechanism is recognized but its delivery-semantics framing is not.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 9 §Atomic Commit and Two-Phase Commit, pp. 352–359 — focus on 'Coordinator failure' subsection and the 'in-doubt' participant state — ~1h 30m
- [remediation] Microservices Patterns — Ch. 4 'Managing transactions with sagas' §4.3 Countermeasures, plus §4.4 The order service saga — covers isolation anomalies (lost updates, dirty reads) and the role of idempotency keys at the consumer — ~45m

</small>
</details>

<details>
<summary><samp>q5 · data-engineering · streaming-join-state-management · pre 2 → post 2 · ceiling b1</samp></summary>

<small>

 

**Scenario:** A streaming pipeline (Kafka Streams or Flink) joins two event streams: `clicks` and `impressions`, keyed by `(user_id, ad_id)`, to compute click-through-rate features. The naive implementation does an inner join with no time bound. After two weeks in production, state-store size has grown to hundreds of GB and checkpoint times are dominating processing latency. Explain (a) the mechanism by which an unbounded stream-stream join causes state to grow without bound (be specific about what is being retained and why), (b) how a windowed/interval join bounds the state and what the window parameter physically controls in the state store, and (c) the correctness tradeoff introduced by the window — what kinds of legitimate joins will the windowed version miss, and how would you reason about choosing the window size from business semantics?

 

**Refinement:** You said 'the join occurs over all the data seen/recomputes joins already seen'. Clarify: what specific data structure the state store retains for each stream side, and why entries cannot be evicted until a match attempt is made.

 

**Assessment:** The answer identifies that windowing bounds state and that there is a correctness tradeoff, satisfying surface-level domain identification. However, the core mechanism — why state cannot be evicted (asymmetric future arrival on the opposite stream side could still produce a legitimate match, gated by event-time watermark advancement) — is not articulated. The refinement probe targeted precisely this gap, and the answer conflated eviction-blocking with in-memory residency, which is a primitive-level misunderstanding rather than an articulation gap. Vocabulary for keyed state stores, watermarks, and event-time retention horizons is absent throughout. The business-semantics reasoning for window sizing is gestured at but not connected to a named downstream consumer (attribution policy, CTR model freshness).

**Literature**

- [remediation] Streaming Systems — Ch. 3 'Watermarks' and Ch. 4 'Advanced Windowing' — focused chapters on event-time, watermark-driven retention, and how windows physically bound state in keyed state stores — ~2h 30m
- [remediation] Kafka Streams Developer Guide — Stream-Stream Joins — §Stream-Stream Joins and §State Stores — JoinWindows.of(Duration), windowed state store retention semantics, RocksDB-backed keyed buffers per side — ~45m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
