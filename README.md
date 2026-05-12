

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
industry     swe                                  updated         2026-05-12
scope        cross-domain · grab-bag              duration        48m 2s
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  data-engineering   data-contract           ₃   2   ₂
q2  backend            bulkhead-pattern        ₄   3   ₃
q3  ai-llm             prompt-caching          ₂   2   ₂
q4  sre                pod-disruption-budget   ₂   2   ₂
q5  security           server-side-request     ₃   3   ₃

gaps         kv-cache-reuse · prefix-stability-requirement · voluntary-vs-involuntary-disruption · drain-vs-eviction-semantics

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · data-engineering · data-contract · pre 2 → post 2 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A logistics SaaS company runs a Kafka-based event pipeline. The `shipment_events` topic is produced by the Operations team's service and consumed by three downstream pipelines: a billing aggregator, a customer-facing tracking API, and an ML feature store. Last quarter, the Operations team renamed `status` to `shipment_status` and changed `estimated_delivery_ts` from a string to an epoch milliseconds long — both in the same release. All three consumers broke in production at different times over the following 48 hours. The team has now agreed to introduce a 'data contract' enforced via a schema registry (Avro or Protobuf). Explain the mechanism by which a schema registry with a compatibility policy (e.g., BACKWARD) would have prevented this specific incident at producer-publish time, what the two changes above each constitute under BACKWARD compatibility rules, and what the registry cannot protect against (i.e., what failure modes remain even with the contract in place). Be specific about which side of the producer-consumer boundary each check runs on.

 

**Assessment:** The answer treats the registry as a generic 'lookup/routing' abstraction rather than a publish-time compatibility validator, and does not classify the rename or the string→long change against the BACKWARD rule. The refinement correctly locates the check 'right before publish' but misattributes it to the broker rather than the producer-side serializer that calls the registry HTTP API. The gap is in naming what BACKWARD specifically rejects and why, and where in the publish flow that rejection physically occurs.

**Literature**

- [remediation] Confluent Schema Registry Documentation — Compatibility Types — §Schema Evolution and Compatibility — 'Compatibility Types' subsection (BACKWARD, FORWARD, FULL, NONE) and 'Order of upgrading clients' — ~25m
- [remediation] Confluent Schema Registry Documentation — Serializer & Formatter — §Serializer and Formatter — 'How the Serializer Works' subsection (producer-side schema registration and compatibility check before publish) — ~15m

</small>
</details>

<details>
<summary><samp>q2 · backend · bulkhead-pattern · pre 3 → post 3 · ceiling b3 · transitional b4</samp></summary>

<small>

 

**Scenario:** A B2B SaaS backend exposes a single REST API process (a Spring Boot service, but the question is framework-agnostic) that serves three categories of endpoints from a shared thread pool of 200 worker threads: (a) fast tenant-dashboard reads (~10ms p99), (b) report-generation endpoints that synchronously call a slow analytics database (~3-8s p99), and (c) webhook delivery endpoints that call out to third-party customer URLs (unbounded latency — some customers' endpoints take 30s before timing out). During incidents, a single customer with a slow webhook receiver causes the dashboard endpoints for *all* tenants to time out, even though the dashboard endpoints themselves have not changed. Explain the mechanism that causes this cross-endpoint degradation, then describe the bulkhead pattern as the remediation: what specifically gets partitioned, what each partition guards, and what the configuration tradeoff is (i.e., why you can't just make each pool 'large enough'). Finally, name one failure mode that bulkheading does NOT fix.

 

**Assessment:** The answer correctly identifies shared-pool saturation as the cross-endpoint coupling and arrives at the bulkhead partition by analogy, with a fair tradeoff statement and a residual-failure named. The refinement reaches for the right constraint (threads share finite compute) but doesn't derive the sizing relationship — why the sum of isolated pools is structurally capped by the same hardware budget, and how Little's Law would set each partition's size from its arrival rate and latency. The gap is in canonical sizing vocabulary and dismissal of structurally different alternatives.

**Literature**

- [remediation] Release It! Design and Deploy Production-Ready Software (2nd ed.) — Ch. 5 'Stability Patterns' §Bulkheads (pp. 95–106) — pool partitioning, sizing, and interaction with Timeouts and Circuit Breaker patterns — ~45m
- [remediation] Performance Modeling and Design of Computer Systems — Ch. 6 §Little's Law and applications (pool sizing from arrival rate × service time) — ~40m

</small>
</details>

<details>
<summary><samp>q3 · ai-llm · prompt-caching · pre 2 → post 2 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A customer-support AI assistant is built on a large LLM provider (Anthropic/OpenAI) and receives ~2M queries/day. Each query is structured as: [long system prompt with policies, ~4k tokens] + [retrieved knowledge base snippets, ~6k tokens, varies per query] + [user message, ~200 tokens]. The product team enables the provider's prompt caching feature hoping to cut both latency and cost, but observes only a ~5% cost reduction and no meaningful latency improvement. Explain the mechanism by which prompt caching saves work on the provider side (what specifically is being cached and reused at the model-inference layer), the structural property the prompt must have for the cache to hit, and why the current prompt layout above defeats the cache for most queries. Then describe the specific restructuring that would make caching effective, and the tradeoff that restructuring forces.

 

**Assessment:** The answer correctly diagnoses that variable retrieval content defeats caching and that restructuring should move variability to the end, but the inference-layer mechanism is misnamed: the refinement attributes reuse to 'embeddings' and 'clustering drift,' conflating retrieval-side embedding similarity with the attention-layer KV-cache. The gap is in the canonical mechanism — the KV-cache stores the keys and values produced by self-attention over prefix tokens, the provider reuses them only when the prefix is byte-identical, and reuse skips the prefill forward pass.

**Literature**

- [remediation] Anthropic Documentation — Prompt Caching — §How prompt caching works and §Structuring your prompt — cache breakpoints and prefix-exact-match requirement — ~20m
- [remediation] Efficient Memory Management for Large Language Model Serving with PagedAttention (vLLM) — §3 Background — KV cache in autoregressive inference (prefill vs decode, what is stored, why prefix sharing yields savings) — ~30m

</small>
</details>

<details>
<summary><samp>q4 · sre · pod-disruption-budget · pre 2 → post 2 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A Kubernetes-hosted payment-processing service runs 6 replicas behind a service. The team configures a HorizontalPodAutoscaler (min=6, max=20) and adds a PodDisruptionBudget with `minAvailable: 5`. Two production incidents follow: (1) during a routine cluster upgrade where nodes are cordoned and drained one at a time, the upgrade stalls for 40 minutes; (2) a separate incident where a node hardware-fails and 3 pods of the service simultaneously go unhealthy, taking the service below `minAvailable: 5` — the PDB does not 'protect' against this. Explain why the PDB blocked the cluster upgrade in case (1) (what specific action did it veto, and why), and explain the mechanism that makes the PDB structurally unable to prevent case (2). Commit to what `minAvailable` should be set to given replicas=6 and a desire to survive single-node hardware failure without service degradation, and justify with a brief calculation.

 

**Assessment:** The answer treats the PDB as an HPA-coupled scaling gate rather than as an admission check on the Eviction API, and never names the voluntary-vs-involuntary disruption distinction that the question's case (2) is specifically testing. The refinement persists in framing drain as 'readiness probe cycling' rather than as a sequence of Eviction API calls that the PDB-aware admission controller can refuse. The minAvailable=7 commit for replicas=6 is structurally impossible. The gap is in the Eviction API mechanism and the disruption taxonomy.

**Literature**

- [remediation] Kubernetes Documentation — Specifying a Disruption Budget for your Application & API-initiated Eviction — Full page: §Voluntary and involuntary disruptions, §Pod disruption budgets, §How disruption budgets work, plus linked §API-initiated Eviction — ~40m
- [remediation] Kubernetes Documentation — Safely Drain a Node — Full page: §The eviction API, §kubectl drain behavior — eviction loop and retry-on-PDB-block — ~20m

</small>
</details>

<details>
<summary><samp>q5 · security · server-side-request-forgery · pre 3 → post 3 · ceiling b3 · transitional b4</samp></summary>

<small>

 

**Scenario:** An internal corporate tool lets authenticated employees enter a URL and receive a rendered preview of the page (the server fetches the URL, screenshots it, returns the image). A security review flags this as an SSRF vector. The current mitigation proposal is: 'block any URL whose hostname resolves to a private IP range (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8) before fetching.' Explain the specific attack class this mitigation is trying to prevent in a cloud-hosted (AWS/GCP/Azure) deployment — name the concrete asset most commonly targeted and what an attacker gains by reaching it. Then identify the mechanism by which the proposed mitigation can still be bypassed (be specific about what happens between hostname validation and the actual HTTP fetch). Finally, commit to a more robust defense and explain why it closes the gap.

 

**Assessment:** The answer correctly identifies the TOCTOU shape between hostname validation and HTTP-client DNS resolution — the canonical DNS-rebinding bypass — and the refinement makes that gap explicit. The gap is in naming the concrete cloud asset (IMDS at 169.254.169.254 serving instance-role credentials), the IMDSv2 hardening, and the canonical structural fix (resolve once at validation time and pass the resolved IP to the HTTP client, or route all egress through an enforcing proxy) rather than 'defense-in-depth' as a general principle.

**Literature**

- [remediation] OWASP Server-Side Request Forgery Prevention Cheat Sheet — Full cheat sheet: §Case 1 / Case 2 application-layer defenses, §DNS pinning / resolve-once recommendation, §Cloud metadata service callout — ~30m
- [remediation] AWS Documentation — Use IMDSv2 — §How Instance Metadata Service Version 2 works — session-token PUT/GET protocol and the SSRF-mitigation properties (no GET on /latest/api/token, no preflight, Origin/Host header requirements) — ~20m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
