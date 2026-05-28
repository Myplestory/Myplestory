

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
industry     swe                                  updated         2026-05-28
scope        cross-domain · grab-bag              duration        53m 54s
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  data-engineering   medallion-architecture  ₄   3   ₃
q2  sre                runbook-automation      ₅   4   ₃
q3  systems-distributedread-after-write        ₂   2   ₂
q4  ml-engineering     batch-normalization     ₂   2   ₁
q5  frontend           css-stacking-context    ₂   2   ₁

strengths    incident-postmortem-loop · runbook-automation · toil-reduction
gaps         batch-normalization-train-eval-divergence · batchnorm-inference-mode · css-stacking-context · dynamo-style-r-w-n

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · data-engineering · medallion-architecture · pre 3 → post 3 · ceiling b2 · transitional b3–b4</samp></summary>

<small>

 

**Scenario:** Company X is building a lakehouse on Delta Lake to land clickstream events from a mobile app. The platform team proposes a three-zone layout: bronze (raw events, schema-on-read), silver (cleaned, deduplicated, conformed types), and gold (business-aggregated marts). A new engineer asks: 'Why not just write directly into the silver layer? Bronze looks like duplicated storage cost for no benefit.' Explain the mechanism each zone provides — what bronze gives you that silver alone cannot, what silver gives you that gold alone cannot — and identify the tradeoff each layer makes (what it costs to maintain it). Be concrete about at least one failure scenario where collapsing bronze into silver would be unrecoverable.

 

**Refinement:** You said 'lulls in data collection/ingestion cannot be surfaced because they are identical under the idempotent/deduplicated model'. Clarify: what specific property of the bronze layer's storage format or write semantics makes that distinction recoverable there but not in silver?

 

**Assessment:** The answer correctly identifies medallion layering as a derivability/fidelity contract and, after refinement, names the right mechanism — bronze's lossless raw persistence vs silver's lossy conformance — which satisfies the B3 invariant. The gap is in the worked failure example: the question asked for a concrete unrecoverable scenario, and the chosen example (data-collection lulls) is one that silver could actually surface from its timestamps. The canonical bronze-only recovery cases — reprocessing after a silver dedup/cleaning bug, schema evolution that needs historical raw fields, and audit/regulatory replay — are not surfaced, and the contract framing (what each layer promises to its downstream consumer) is implicit rather than explicit.

**Literature**

- [remediation] Delta Lake: The Definitive Guide — Ch. 9 'Architecting Your Lakehouse' — §Medallion Architecture: bronze replayability, silver conformance contract, and the canonical 'reprocess after silver-logic bug' failure mode. — ~45m
- [remediation] Designing Data-Intensive Applications — Ch. 11 'Stream Processing' §The Unbundled Database / Event Sourcing, pp. 457–465 — raw event log as the source-of-truth substrate from which all derived views can be rebuilt. — ~30m

</small>
</details>

<details>
<summary><samp>q2 · sre · runbook-automation · pre 4 → post 4 · ceiling b3 · transitional b4</samp></summary>

<small>

 

**Scenario:** Service A at Company X pages its on-call rotation roughly 12 times per week for the same class of incident: a downstream partner API returns intermittent 5xxs, the on-call engineer SSHes into a worker pod, restarts the consumer, and clears a backed-up queue. The runbook for this is six steps long and has been followed correctly every time. Leadership asks the on-call team to 'reduce alert volume'. The team proposes silencing the alert during low-traffic hours. Explain why this is the wrong remediation in SRE terms, what category of work this incident pattern represents, and what the mechanism-level fix looks like. Identify what tradeoff the right fix imposes that silencing does not.

 

**Refinement:** You said 'automate or mitigate the backed up queue via multi layer defenses'. Clarify: what property of the current six-step human runbook, when encoded into automation, determines whether the automated fix eliminates the underlying failure class or simply reproduces the same manual loop faster?

 

**Assessment:** The response correctly rejects silencing on mechanism grounds — it identifies that muting hides real backpressure and degrades 'what changed' debugging — and reaches for the right family of fixes (bounded retries, automated drain, multi-layer queue defenses). The refinement sharpens this with the critical distinction between automation that replays the runbook faster vs. automation that prevents step 1 from being needed. The gap is at the vocabulary and framing layer: the work category the question explicitly asks to name is never named in canonical terms, and the right-fix tradeoff is not connected to the partner-team signal or on-call/error-budget consequence that distinguishes a B4 design commitment from a B3 mechanism explanation.

**Literature**

- [remediation] Site Reliability Engineering: How Google Runs Production Systems — Ch. 5 'Eliminating Toil' — the full chapter (toil definition, the toil-to-engineering ratio, and the case that automating a runbook step-for-step without removing the failure class is faster toil, not engineering) — ~45m
- [growth] Release It! Design and Deploy Production-Ready Software, 2e — Connects the answer's instinct toward 'multi-layer defenses' to the named stability-pattern catalog (Circuit Breaker, Bulkhead, Timeout, Steady State) so the next-step fix to a flaky partner API can be committed to by name rather than enumerated as options. — ~6h

</small>
</details>

<details>
<summary><samp>q3 · systems-distributed · read-after-write-quorum · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A distributed key-value store is configured with N=5 replicas per key. Team Y is deciding between (W=3, R=3), (W=4, R=2), and (W=2, R=4) for a workload that is 90% reads, 10% writes, and requires read-your-writes consistency for a single client session in the steady state (no failures). Explain the mechanism that makes R+W>N sufficient for read-your-writes in this model, then commit to one of the three configurations for this workload and justify the choice. For the two you dismiss, name the specific axis on which they lose (latency, availability under one replica down, write throughput, etc.). Finally, identify one failure scenario where R+W>N still produces a stale read despite the inequality holding.

 

**Refinement:** You said 'The mechanism that makes R+W>N sufficient is the fact the read-your-writes is named as a consistent invariant'. Clarify: what specific property of the intersection between the write quorum set and the read quorum set guarantees that at least one node in any read quorum has seen the most recent write?

 

**Assessment:** The response identifies the right domain (Dynamo-style quorum, read-your-writes) and commits to a configuration, but substitutes a sticky-session routing model for the actual quorum-intersection mechanism — the property that any write set of size W and read set of size R on N replicas must share at least one replica when W+R>N. The refinement probe pointed directly at 'the intersection between the write quorum set and the read quorum set,' and the response answered with superset/subset and session-routing language rather than the intersection property. The dismissals of the other two configurations rest on a fabricated connection-hold argument rather than the real tradeoff axes (read latency on the 90% path, write availability under one replica down). The stale-read failure example ('routing to a non-propagated node') is directionally aware but does not name a specific mechanism such as sloppy quorum / hinted handoff or in-flight unacknowledged writes.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 5 §Quorums for reading and writing, pp. 179–182 — the pigeonhole intersection argument and the diagram showing W+R>N as set overlap, plus §Limitations of Quorum Consistency, pp. 181–184 (sloppy quorum, concurrent writes, in-flight writes) — ~1h 30m
- [remediation] Dynamo: Amazon's Highly Available Key-value Store — §4.5 'Data Versioning' and §4.6 'Execution of get () and put () operations' — how the coordinator assembles W and R sets from the preference list and how version metadata (vector clocks) lets the client reconcile, and §4.6 sloppy-quorum mechanics that produce stale reads even when R+W>N — ~1h

</small>
</details>

<details>
<summary><samp>q4 · ml-engineering · batch-normalization-train-eval-divergence · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** An engineer at Company X trains an image classifier with BatchNorm layers. Training accuracy is 94% and validation accuracy (computed during training with the model in train mode) is 91%. After saving the model and loading it into a production inference service that processes requests one image at a time, accuracy drops to 62%. The model weights are identical to what was validated. Explain the mechanism that produces this gap. What does BatchNorm compute differently in train mode vs eval mode, and why does the difference manifest specifically at batch size 1 in production? Name the fix and identify one tradeoff the fix imposes (i.e., what you give up by switching modes correctly).

 

**Refinement:** You said 'BatchNorm computes the normalize aggregate between the batch'. Clarify: what specific numerical values does BatchNorm use to normalize inputs at inference time when no batch statistics are available, and where do those values come from?

 

**Assessment:** The response correctly localized the failure to BatchNorm and to the batch-size mismatch between training/validation and one-at-a-time production inference, but missed the actual mechanism: the model was never switched to evaluation mode, so BN continued to normalize against batch statistics where 'the batch' is a single sample. The refinement probed exactly the missing primitive — what stored values BN uses at inference — and the answerer surfaced guesses ('median/mean?', 'deviation or variance?', 'default is 0') rather than recall, confirming the gap is in the running-statistics / EMA primitive and the eval-mode toggle, not in deployment batching strategy. The proposed fix (batch the production traffic) addresses a symptom under the wrong model and would not resolve the gap; the canonical one-line fix (model.eval()) and its tradeoff (frozen statistics that cannot adapt to covariate shift) are absent.

**Literature**

- [remediation] Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift — §3 'Normalization via Mini-Batch Statistics' and §3.1 'Training and Inference with Batch-Normalized Networks' — specifically the inference-time use of population (running) statistics rather than mini-batch statistics — ~45m
- [remediation] PyTorch Documentation — BatchNorm2d and Module.eval() — BatchNorm2d 'track_running_stats' and 'momentum' parameter descriptions, plus the Module.eval() page explaining the train/eval mode switch and which layers it affects (BatchNorm, Dropout) — ~20m

</small>
</details>

<details>
<summary><samp>q5 · frontend · css-stacking-context · pre 2 → post 2 · ceiling —</samp></summary>

<small>

 

**Scenario:** A frontend engineer on Team Y reports that their modal dialog (z-index: 9999) is being rendered behind a sidebar (z-index: 10) on one page but not on others. Inspecting the DOM, they discover that the sidebar's parent has `transform: translateZ(0)` applied for GPU compositing. Explain the mechanism: why does a transform on an ancestor cause a high z-index descendant to lose to a low z-index sibling tree? Name the CSS concept involved and identify at least two other properties that trigger the same effect. Commit to a remediation strategy and explain what tradeoff it imposes vs. the 'just raise z-index higher' approach a junior engineer might reach for.

 

**Refinement:** You said 'the dom fundamentally changes (the render tree is altered/the transform shifts the nodes, and overrides the z index values)'. Clarify: what is the specific boundary that a transform creates, and why does that boundary prevent z-index comparisons from crossing it regardless of how high the z-index value is?

 

**Assessment:** The answer identifies that the transform is causally responsible for the modal's z-index losing to a lower-z-index sibling tree but cannot name the CSS concept that gates the comparison or state the rule that governs z-index across that boundary. The refinement probe directly invited naming the boundary; the response offered three guesses ('a styling? subtree? root render state?') without converging. The 'other two properties' answer named one transform sub-case and one unrelated ARIA attribute, indicating the peer-property family was not recalled. The remediation reached for a React lifecycle metaphor ('re-render', 'use effect') for what is purely a CSS painting-model issue, suggesting the gap is conceptual rather than articulation. The reading should establish what the boundary is named, the rule that operates across it, and what design pattern bypasses it without raising z-index.

**Literature**

- [remediation] MDN — Stacking context — Full article: 'Stacking context' — definition, the list of stacking-context-creating properties (transform, opacity, filter, will-change, isolation, position: fixed/sticky, contain, mix-blend-mode), and the z-index-within-context rule — ~25m
- [remediation] CSS Transforms Module Level 1 — The Transform Rendering Model — Full section §6 'The Transform Rendering Model' — verbatim: 'For elements whose layout is governed by the CSS box model, any value other than none for the transform property results in the creation of a stacking context.' — ~15m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
