

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
industry     swe                                  updated         2026-06-04
scope        cross-domain · grab-bag              duration        1h 8m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  ai-llm             semantic-cache-key      ₄   3   ₂
q2  backend            optimistic-vs           ₃   3   ₂
q3  security           session-fixation        ₃   2   ₂
q4  ml-engineering     auc-vs-pr-curve-under   ₃   3   ₂
q5  systems-distributedidempotency-key-design  ₅   4   ₃

strengths    at-least-once-plus-idempotent · effectively-once-vs-at-most-once · idempotency-key-design
gaps         csrf-vs-fixation-distinction · session-fixation · session-id-rotation-on-privilege-change

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · ai-llm · semantic-cache-key-design · pre 3 → post 3 · ceiling b1–b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A SaaS support-assistant team fronts their LLM with a semantic cache: incoming user questions are embedded, and if cosine similarity to a cached question exceeds a threshold T, the cached answer is returned instead of calling the model. They report two problems in production: (a) some users get answers to subtly different questions ('How do I cancel my subscription?' returns the answer for 'How do I pause my subscription?'), and (b) after they raised T to fix that, the cache hit rate collapsed and costs went back up. Walk through the mechanism: why does a similarity threshold trade false-hit risk against hit rate, and what is the cache actually keyed on? Then explain what they give up versus an exact-string cache, and name one thing besides the question text that should be part of the cache key for this to be safe.

 

**Refinement:** You said 'The main mechanism the similarity threshold operates in is retrieval/top~k simil...'. What breaks if that assumption is wrong?

 

**Assessment:** The answer correctly identifies that the cache is keyed on embeddings rather than intent and that an exact-string cache trades recall for the precision that would have separated 'cancel' from 'pause', and the refinement usefully isolates the scalar threshold as the load-bearing element. The gap is the mechanism the question explicitly asked for: why a single scalar similarity radius simultaneously trades false-hit risk against hit rate across the whole embedding space, and what context discriminator (besides question text) must enter the key. The 'additional key' answer loops back into lexical matching and vague 'fusion metadata' instead of naming a dimension that changes the correct answer for identical text — read the cache-key-metadata and bi-encoder material to close it. Terminology ('identity hashing', embeddings as token comparison) should be corrected against how learned embeddings differ from hashes.

**Literature**

- [remediation] Sentence-Transformers: Semantic Search & Bi-Encoder vs Cross-Encoder — Chapter: 'Bi-Encoder vs. Cross-Encoder' plus the Semantic Search guide — focused chapter on why an embedding is a learned semantic vector (not a hash or token comparison) and why a cross-encoder confirmation gate fixes the cancel↔pause false hit — ~20m
- [remediation] LlamaIndex Vector Stores — embedding metadata & cache-key best practices — One focused chapter: storing model_name/model_version and context discriminators alongside each vector — directly supplies the 'what besides question text belongs in the key' answer (tenant/KB-version/model-version) the response left as vague 'fusion metadata' — ~15m

</small>
</details>

<details>
<summary><samp>q2 · backend · optimistic-vs-pessimistic-locking · pre 2 → post 3 · ceiling — · transitional b1–b3</samp></summary>

<small>

 

**Scenario:** A backend team has an inventory service where multiple workers can decrement the stock count for the same SKU concurrently. They currently do `SELECT quantity ... ; quantity = quantity - 1; UPDATE ...` in application code and are seeing oversell (stock going negative). An engineer proposes optimistic locking with a version column; another proposes `SELECT ... FOR UPDATE`. Explain the mechanism of each: how does the version-column compare-and-swap detect a conflict, and how does `FOR UPDATE` prevent one? State what each approach gives up — specifically, under what contention profile would you reach for one over the other, and what happens to a transaction that loses the optimistic race?

 

**Refinement:** You said 'The transaction that loses the optimistic race means they get either overwritten or blocked?'. Clarify: what concrete action does the application layer take when the version column check fails at UPDATE time — and how does that differ from what the database itself enforces?

 

**Assessment:** The answer correctly locates the high-level distinction — optimistic locking pushes conflict enforcement into the application layer while FOR UPDATE delegates arbitration to the database — and the refinement strengthened that enforcement-boundary framing. But the two mechanisms are inverted throughout (compare-and-swap is attributed to FOR UPDATE and MVCC to the version column), the actual conflict-detection predicate and its signal are never stated, and the contention recommendation runs opposite to the standard mapping. The gap is in the concrete row-level mechanics of each primitive and what the losing writer concretely does; the reading below leads to both.

**Literature**

- [remediation] Designing Data-Intensive Applications — DDIA Ch. 7 §Preventing Lost Updates — 'Atomic write operations', 'Explicit locking' (SELECT ... FOR UPDATE), and 'Compare-and-set' (pp. 242–246) — ~1h 15m
- [remediation] PostgreSQL Documentation §13.3 Explicit Locking — §13.3 Explicit Locking — FOR UPDATE row-lock blocking semantics (the locked rows block other UPDATE/DELETE/FOR UPDATE until the current transaction ends) — ~20m

</small>
</details>

<details>
<summary><samp>q3 · security · session-fixation · pre 2 → post 2 · ceiling — · transitional b1–b2</samp></summary>

<small>

 

**Scenario:** An e-commerce app issues a session cookie to every anonymous visitor so they can build a cart before logging in. After a user authenticates, the app keeps the same session ID and just flips an `is_authenticated` flag on the server-side session record. A pentester flags this. Name the vulnerability class and describe the attack: how does an attacker exploit the fact that the session identifier spans the unauthenticated→authenticated boundary? Then state the structural fix and explain why it works. Finally, explain why adding a CSRF token does NOT close this particular hole.

 

**Refinement:** You said 'leveraging the unauthenticated sessions to match the session id to authenticated boundaries'. Clarify: what concrete action does the attacker take before the victim logs in, and what does the attacker gain control of as a result?

 

**Assessment:** The answer never names the vulnerability class (Session Fixation) and, critically, mischaracterizes the attack: the refinement probe specifically asked what concrete action the attacker takes before the victim logs in, and the response substituted an XSS/JS-injection 'browser-state persists across the boundary' model in place of the actual fixation mechanism — planting a session identifier the victim then authenticates on, which the attacker subsequently reuses as a bearer credential. The structural fix (don't carry the ID, spawn a fresh authenticated session and copy cart state) is directionally correct but justified by abstract 'boundary enforcement' language rather than by why credential invalidation defeats the threat. The CSRF reasoning reaches the right same-origin conclusion via the wrong rationale (it being 'intra-site') rather than the load-bearing point: the attacker already holds the session directly, so there is no forged cross-origin request to block. Read the named sources to recover the precise pre-auth-plant attack sequence and the credential-invalidation rationale.

**Literature**

- [remediation] OWASP Session Management Cheat Sheet — §Session Fixation and §Renew the Session ID After Any Privilege Level Change — ~15m
- [remediation] Session Fixation Vulnerability in Web-based Applications — §3 Attack Variants and §4 Countermeasures — ~40m

</small>
</details>

<details>
<summary><samp>q4 · ml-engineering · auc-vs-pr-curve-under-imbalance · pre 2 → post 3 · ceiling b1 · transitional b2–b3</samp></summary>

<small>

 

**Scenario:** An ML team builds a fraud classifier where ~0.5% of transactions are fraudulent. They report a held-out ROC-AUC of 0.97 and are ready to ship, but a reviewer pushes back and says the model may still be operationally useless. Explain the mechanism: why can ROC-AUC look excellent on a heavily imbalanced positive class while the model is poor at the thing the business cares about? Walk through what happens to the false-positive rate's denominator when negatives dominate. Then state which metric/curve you would report instead and why it gives up the misleading optimism that ROC-AUC retains here.

 

**Refinement:** You said 'The false-positive rate's denominator decreases when negatives dominates because of the diminishing nature of the ratio'. Clarify: what specific quantity sits in that denominator, and why its size relative to true positives makes FPR appear low even when the model misclassifies many fraudulent transactions?

 

**Assessment:** The answer identifies that imbalance makes ROC-AUC misleading and, after the probe, correctly names the FPR denominator as the total negatives (TN+FP) and recognizes that its size makes the false-positive rate appear small. The gap is the other half of the mechanism: it never states why precision (TP/(TP+FP)) — the metric that puts false positives against the rare positive class — is the quantity the business feels, and it substitutes an invented 'residual quality metric' framing for the actual ranking-vs-operating-point distinction. The PR-curve answer is reached only by guesswork ('pr-AUC or something'). The reading pointer should close the precision-denominator side of the contrast and ground why the PR curve drops the optimism ROC retains.

**Literature**

- [remediation] The Relationship Between Precision-Recall and ROC Curves — §3–4 — why ROC underweights false positives when the negative class dominates, and how PR space exposes it — ~40m
- [remediation] Hands-On Machine Learning, 3rd ed. — Ch. 3 'Classification' §The ROC Curve and §Precision/Recall Trade-off — ~45m

</small>
</details>

<details>
<summary><samp>q5 · systems-distributed · idempotency-key-design · pre 3 → post 4 · ceiling b3 · transitional b4–b5</samp></summary>

<small>

 

**Scenario:** A payments service consumes a message queue that delivers each 'credit merchant wallet' event at-least-once, so duplicates are possible (network retries, consumer redelivery after a crash before ack). A junior engineer suggests switching the queue to at-most-once delivery to avoid double-crediting. Explain why at-most-once is the wrong move for a value-bearing operation, and describe the mechanism that actually gives you effectively-once: what does the idempotency/dedup key look like, and crucially, why must the dedup check and the credit write happen atomically in the same transaction? Walk through what breaks if they are two separate steps and a duplicate arrives concurrently.

 

**Refinement:** You said 'the dedupe check and atomic write must happen in the same transaction'. Clarify: what specific database or storage property makes a combined check-and-write prevent a duplicate from succeeding when two concurrent consumers reach that step at the same moment?

 

**Assessment:** Pre-refinement, the answer correctly located the problem in the idempotency/dedup domain and asserted that the dedup check and credit write must share one transaction, but it never named the storage property that wins the concurrent race and it mislabeled the target semantics ('exactly once'/'at most once') rather than at-least-once delivery plus idempotent processing yielding effectively-once. The refinement probe closed the central gap: the answerer reached for an atomic compare-and-write (ON CONFLICT) and serialized access as the reason a second concurrent duplicate cannot also commit. Remaining gaps are vocabulary precision (constraint-conflict-at-commit vs. 'read lock') and the uncorrected effectively-once labeling; the design-review layer (alternative dedup strategies, downstream ledger/audit consequences) is absent. Read the pointed material to firm up the exact enforcement primitive and the correct delivery-semantics vocabulary.

**Literature**

- [remediation] Implementing Stripe-like Idempotency Keys in Postgres — §'Idempotency and concurrency' and §'Recovery points' — the unique-constraint-on-idempotency-key-written-atomically-with-the-side-effect-row subsection — ~25m
- [growth] Designing Data-Intensive Applications, Ch. 12 §The End-to-End Argument for Databases — Connects this question's atomic-dedup mechanism to the broader principle that effectively-once requires an end-to-end idempotency identifier threaded from producer through to the final write — the next conceptual layer above the single-transaction race the answer solved. — ~30m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
