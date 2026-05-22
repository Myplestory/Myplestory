

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
industry     swe                                  updated         2026-05-22
scope        cross-domain · grab-bag              duration        58m 4s
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  frontend           concurrent-rendering    ₂   1   ₁
q2  data-engineering   bloom-filter-pushdown   ₂   2   ₁
q3  ml-engineering     concept-drift-vs-data   ₂   2   ₂
q4  security           session-fixation        ₅   3   ₂
q5  ai-llm             reranker-cross-encoder  ₂   2   ₁

gaps         bi-encoder-vs-cross-encoder · bloom-filter-pushdown · concept-drift-vs-data-drift · concurrent-rendering

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · frontend · concurrent-rendering · pre 1 → post 1 · ceiling —</samp></summary>

<small>

 

**Scenario:** A SaaS analytics dashboard has a search input that filters a list of 8,000 rows rendered as a complex component tree (each row has charts and sparklines). Users complain that typing in the search box feels laggy — keystrokes visibly stutter. A junior engineer proposes wrapping the filter state update in React's useTransition. Explain the mechanism by which useTransition would improve keystroke responsiveness here: what specifically gets marked as a 'transition,' what does React do differently with that update versus an urgent one, and what visible behavior does the user get in exchange? Then identify one scenario where useDeferredValue would be the better choice instead, and explain why.

 

**Refinement:** You said 'it propogates the ui/ux reactive, meaning less latency than setting/propogating the state up the fabric tree'. Clarify: what does React do with the rendering work for the filtered list during the period between the keystroke and the transition completing?

 

**Assessment:** The question tested whether the answerer could name React 18's documented priority model for the keystroke-lag scenario — what gets marked as urgent vs as a transition, and what the concurrent renderer does with an in-progress lower-priority render when a new urgent update arrives. The response substituted invented vocabulary for the API across both turns, and the refinement probe — which targeted exactly the interruptibility behavior — produced a metaphor ('stacking dominos, then tip over') that inverts the documented model. The ownership-of-setter rule that selects useDeferredValue over useTransition was also miscast as a functional/UX distinction. The gap is in the canonical React 18 concurrent rendering model itself.

**Literature**

- [remediation] useTransition — React Reference — Entire page: Reference (signature, isPending, startTransition) + Usage §'Marking a state update as a non-blocking transition' and §'Updating the parent component in a transition' — ~25m
- [remediation] useDeferredValue — React Reference, §'useDeferredValue vs useTransition' — Entire page: Reference + Usage §'Deferring re-rendering for a part of the UI' + the explicit §'useDeferredValue vs useTransition' comparison — ~20m

</small>
</details>

<details>
<summary><samp>q2 · data-engineering · bloom-filter-pushdown · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A data team stores 5 years of clickstream events in Parquet files on object storage, partitioned by event_date. Analysts increasingly run queries like 'find all events for user_id = X across the entire history' — these scan terabytes because user_id is uncorrelated with partition date. The team is considering two interventions: (a) Z-order clustering by user_id within each partition, or (b) writing a Bloom filter index per file on user_id. Explain the mechanism each one uses to reduce I/O for a point-lookup-by-user_id query, what each gives up (write-side cost, query patterns they don't help, false-positive behavior), and which you'd commit to first for this access pattern. Why?

 

**Refinement:** You said 'Bloom filter index is a query time optimization. It allows efficient access of matching through composite data points/keys and set/subset theory to index and make the access less costly (exact method slipped my mind)'. Clarify: what property of the Bloom filter data structure lets it rule out an entire file without reading its row groups, and at what stage of query execution does that file elimination happen?

 

**Assessment:** The response treats Bloom filters as 'set/subset theory' pre-refinement and then commits confidently to 'prefix matching with fail-fast on incorrect prefixes' under refinement — both are the wrong data structure for the Parquet Bloom filter index. Z-order is described as deferring query-time work to write time via 'locality of data', missing the actual two-part mechanism (Morton-curve clustering enabling per-file min/max data-skipping at scan planning). The commit ordering for an equality point-lookup over 5 years of immutable Parquet is inverted relative to the write-amplification cost calculus. The gap is in the names of the two pruning data structures, where they live in the Parquet footer, and at what query-execution stage they prune.

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 3 §SSTables and LSM-Trees, 'Performance optimizations' subsection (pp. 80–84) — Bloom filter as probabilistic set membership with k hash functions and no false negatives — ~30m
- [remediation] Delta Lake Documentation — Data Skipping and Z-Ordering — §Data Skipping and §OPTIMIZE ZORDER BY — per-file min/max statistics in the transaction log, Morton-curve clustering, write amplification of OPTIMIZE — ~30m

</small>
</details>

<details>
<summary><samp>q3 · ml-engineering · concept-drift-vs-data-drift · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A fraud-detection model deployed for 8 months has shown a slow, steady decline in precision (from 0.91 to 0.78) while recall has remained roughly constant. The ML platform team monitors input feature distributions using Population Stability Index (PSI) per feature, and none of the per-feature PSI values have crossed the alerting threshold. Explain the distinction between data drift and concept drift, identify which is most consistent with the observed symptom pattern, and explain why per-feature PSI monitoring failed to detect it. What additional monitoring signal would catch this class of drift, and what does that signal require that per-feature PSI does not?

 

**Refinement:** You said 'drift is the blending of the features cause stable psi to manifest in a different manner'. Clarify: what is it about the relationship between features and the target label that per-feature PSI structurally cannot observe, even when every individual feature distribution is stable?

 

**Assessment:** The answer identified concept drift as the correct domain but never produced the operative framing — that concept drift is a change in P(y|X) and that per-feature PSI is structurally blind to it because labels are not an input to the statistic. The refinement probe directly named "the relationship between features and the target label" and the response pivoted to multivariate feature interaction and cardinality, not to labels. The monitoring signal that catches this class of drift, and the label-availability dependency it introduces relative to PSI, were never named.

**Literature**

- [remediation] Designing Machine Learning Systems — Ch. 8 §Types of Data Distribution Shifts and §Monitoring ML Systems (covariate shift, label shift, concept drift; feature-monitor blindness; label-aware monitoring) — ~1h 30m
- [remediation] A Survey on Concept Drift Adaptation — §2 Concept Drift Formalization (P(X,y) = P(X)·P(y|X) decomposition; labeled vs unlabeled drift detectors) — ~45m

</small>
</details>

<details>
<summary><samp>q4 · security · session-fixation · pre 3 → post 3 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A web application issues an anonymous session cookie when a visitor lands on the site (used to track cart contents pre-login). When the user logs in, the application validates credentials and then attaches the user identity to that existing session — same session ID, now authenticated. A penetration tester flags this as a session fixation vulnerability. Explain the attack mechanism: how does an attacker exploit the fact that the session ID does not change at the authentication boundary? What is the structural fix, and why is rotating the session ID at the privilege-elevation moment (rather than, e.g., adding a CSRF token or shortening session TTL) the correct mitigation?

 

**Refinement:** You said 'csrf can be'. Clarify: what specific property of session ID rotation at the privilege boundary makes it effective against the fixation attack vector that neither CSRF tokens nor TTL reduction can address?

 

**Assessment:** The response correctly localizes the defect at the unauthenticated → authenticated boundary and commits to the right structural fix (rotate the session identifier at privilege elevation), which satisfies the structural-commit half of the B3 invariant. It does not name the vulnerability class, does not describe how an attacker comes to possess the pre-auth identifier in the first place, and does not give a causal argument for why the two named alternatives are categorically inappropriate rather than merely weaker. The refinement asked precisely for that causal argument and instead substituted implementation properties (server-side ownership, atomicity, constant-time comparison) drawn from adjacent threat models. The gap is in threat-model vocabulary and in articulating what each mitigation assumes about the attacker's knowledge of the session ID.

**Literature**

- [remediation] OWASP Session Management Cheat Sheet — §Renew the Session ID After Any Privilege Level Change, and §Session Fixation — ~20m
- [remediation] Session Fixation Vulnerability in Web-based Applications — §3 Attack Variants and §4 Countermeasures — ~30m

</small>
</details>

<details>
<summary><samp>q5 · ai-llm · reranker-cross-encoder · pre 2 → post 2 · ceiling —</samp></summary>

<small>

 

**Scenario:** A RAG system over a 2M-document corpus uses a bi-encoder (e.g., a sentence-transformer) to embed documents and queries, then retrieves the top-50 by cosine similarity. Faithfulness evaluations show the retrieved set often contains the right document but ranked at position 20-40, so the top-5 passed into the LLM context misses it. A teammate proposes adding a cross-encoder reranker over the top-50 before truncating to top-5. Explain the architectural distinction between a bi-encoder and a cross-encoder, why a cross-encoder produces better relevance ranking at the cost that prevents you from using it as the first-stage retriever, and what the two-stage retrieve-then-rerank pattern gives up in exchange for the improved top-k quality.

 

**Refinement:** You said 'the cross encoder does it both ways (two pass, forward back)'. Clarify: what is the actual input construction difference between a bi-encoder and a cross-encoder at inference time, and why does that difference prevent precomputing and caching document representations?

 

**Assessment:** The answer correctly identified that two-stage retrieve-then-rerank trades latency and throughput for improved top-k quality, which is one part of the B3 articulation. However, the load-bearing architectural distinction — that a cross-encoder jointly encodes the concatenated query and document so self-attention runs across both, making the document representation query-dependent and therefore impossible to precompute — was not stated, and was instead replaced by a 'forward vs forward-and-backward pass' and set-theoretic frame that do not correspond to the actual mechanism. The refinement probed exactly this gap and the response introduced additional unfounded vocabulary (hashes of canonicalized tokens, clustering-altered embeddings) rather than producing the canonical input-construction fact. The recall-ceiling giveup of the two-stage pattern was also not surfaced.

**Literature**

- [remediation] Sentence-Transformers — Cross-Encoders — 'Bi-Encoder vs. Cross-Encoder' section — the diagram and the two paragraphs immediately following it (the canonical one-page explainer for this exact distinction) — ~10m
- [remediation] Sentence-Transformers — Retrieve & Re-Rank — The 'Retrieve & Re-Rank Pipeline' diagram and the paragraph stating cross-encoders are not used for retrieval over large collections plus the recall-ceiling note — ~10m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
