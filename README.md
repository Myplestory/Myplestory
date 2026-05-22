

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
q3  ml-engineering     concept-drift-vs-data   ₂   2   ₁
q4  security           session-fixation        ₄   3   ₂
q5  ai-llm             reranker-cross-encoder  ₂   2   ₂

gaps         bi-encoder-vs-cross-encoder · bloom-filter-pushdown · concept-drift-vs-data-drift · concurrent-rendering

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · frontend · concurrent-rendering · pre 1 → post 1 · ceiling —</samp></summary>

<small>

 

**Scenario:** A SaaS analytics dashboard has a search input that filters a list of 8,000 rows rendered as a complex component tree (each row has charts and sparklines). Users complain that typing in the search box feels laggy — keystrokes visibly stutter. A junior engineer proposes wrapping the filter state update in React's useTransition. Explain the mechanism by which useTransition would improve keystroke responsiveness here: what specifically gets marked as a 'transition,' what does React do differently with that update versus an urgent one, and what visible behavior does the user get in exchange? Then identify one scenario where useDeferredValue would be the better choice instead, and explain why.

 

**Refinement:** You said 'it propogates the ui/ux reactive, meaning less latency than setting/propogating the state up the fabric tree'. Clarify: what does React do with the rendering work for the filtered list during the period between the keystroke and the transition completing?

 

**Assessment:** The answer never anchors to React's documented priority model — that the controlled input's setState is processed as an urgent update while the filter setState wrapped in startTransition is deferred and rendered in an interruptible concurrent pass that newer keystrokes can abandon. The refinement probe gave a direct opening to name interruptibility and instead received a 'stacking dominos' metaphor that does not correspond to how the scheduler behaves. The useDeferredValue scenario also misses the actual differentiator, which is ownership of the setter (values arriving via props or external hooks that cannot be wrapped in startTransition). A secondary gap: neither hook reduces render cost for 8,000 complex rows, so a proficient answer would also flag that virtualization or per-row memoization is the real lever and useTransition is complementary, not a substitute.

**Literature**

- [remediation] useTransition — React Reference — 'useTransition' reference page in full — Reference, Usage ('Marking a state update as a non-blocking transition', 'Updating the parent component in a transition', 'Displaying a pending visual state during the transition'), and Troubleshooting — ~30m
- [remediation] useDeferredValue — React Reference — 'useDeferredValue' reference page in full — Usage ('Showing stale content while fresh content is loading', 'Indicating that the content is stale', 'Deferring re-rendering for a part of the UI') and 'useDeferredValue vs useTransition' comparison — ~25m

</small>
</details>

<details>
<summary><samp>q2 · data-engineering · bloom-filter-pushdown · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A data team stores 5 years of clickstream events in Parquet files on object storage, partitioned by event_date. Analysts increasingly run queries like 'find all events for user_id = X across the entire history' — these scan terabytes because user_id is uncorrelated with partition date. The team is considering two interventions: (a) Z-order clustering by user_id within each partition, or (b) writing a Bloom filter index per file on user_id. Explain the mechanism each one uses to reduce I/O for a point-lookup-by-user_id query, what each gives up (write-side cost, query patterns they don't help, false-positive behavior), and which you'd commit to first for this access pattern. Why?

 

**Refinement:** You said 'Bloom filter index is a query time optimization. It allows efficient access of matching through composite data points/keys and set/subset theory to index and make the access less costly (exact method slipped my mind)'. Clarify: what property of the Bloom filter data structure lets it rule out an entire file without reading its row groups, and at what stage of query execution does that file elimination happen?

 

**Assessment:** The candidate recognises the two techniques as named categories but cannot describe the mechanism by which either reduces I/O. The refinement targeted the single most important Bloom property — what lets a file be eliminated without opening its row groups — and the answer returned a description of prefix matching, which is a different data structure. The commit recommendation also inverts the expected direction for an equality point-lookup access pattern over multi-terabyte historical data. The gap is at the data-structure layer (how Bloom hashes set bits, how Z-order interacts with footer min/max statistics) and at the cost-model layer (rewrite-all-history vs append-time footer addition).

**Literature**

- [remediation] Designing Data-Intensive Applications — Ch. 3 §Storage and Retrieval — SSTables, LSM-trees and Bloom filters (pp. 78–84); plus Ch. 3 §Column-Oriented Storage — column compression, sort orders, and writing to column-oriented storage (pp. 95–101) — ~3h 30m
- [remediation] Delta Lake: The Definitive Guide — Ch. 5 'Performance Tuning' §Data Skipping and Z-Ordering — how OPTIMIZE ZORDER BY rewrites files and how the engine uses per-file min/max stats stored in the transaction log to skip files at scan-planning time — ~45m

</small>
</details>

<details>
<summary><samp>q3 · ml-engineering · concept-drift-vs-data-drift · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A fraud-detection model deployed for 8 months has shown a slow, steady decline in precision (from 0.91 to 0.78) while recall has remained roughly constant. The ML platform team monitors input feature distributions using Population Stability Index (PSI) per feature, and none of the per-feature PSI values have crossed the alerting threshold. Explain the distinction between data drift and concept drift, identify which is most consistent with the observed symptom pattern, and explain why per-feature PSI monitoring failed to detect it. What additional monitoring signal would catch this class of drift, and what does that signal require that per-feature PSI does not?

 

**Refinement:** You said 'drift is the blending of the features cause stable psi to manifest in a different manner'. Clarify: what is it about the relationship between features and the target label that per-feature PSI structurally cannot observe, even when every individual feature distribution is stable?

 

**Assessment:** The answer correctly identified the symptom as concept drift but never produced the controlling distinction — that data drift concerns P(X) while concept drift concerns the conditional P(y|X), the relationship between features and the label. The refinement probe explicitly named that relationship and the response still pivoted to multivariate feature interactions (which describe joint data drift) rather than to the label-vs-feature axis. The gap is twofold: the structural reason per-feature PSI fails (it inspects marginals of X only, never y) and the required signal (label-aware performance monitoring, with the operational implication that production labels must be available, despite the fraud-domain chargeback delay).

**Literature**

- [remediation] Designing Machine Learning Systems — Ch. 8 'Data Distribution Shifts and Monitoring' — specifically the subsections on covariate shift vs. label shift vs. concept drift, and the monitoring-signal taxonomy (input monitoring, prediction monitoring, accuracy-related metrics monitoring). — ~1h 15m
- [remediation] A Survey on Concept Drift Adaptation — §2 'Concept Drift Definitions' and §3 'Concept Drift Detection Methods' — the formal P(X,y) decomposition into P(X)·P(y|X) and the taxonomy of detectors that require labels vs. those that do not. — ~1h

</small>
</details>

<details>
<summary><samp>q4 · security · session-fixation · pre 3 → post 3 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A web application issues an anonymous session cookie when a visitor lands on the site (used to track cart contents pre-login). When the user logs in, the application validates credentials and then attaches the user identity to that existing session — same session ID, now authenticated. A penetration tester flags this as a session fixation vulnerability. Explain the attack mechanism: how does an attacker exploit the fact that the session ID does not change at the authentication boundary? What is the structural fix, and why is rotating the session ID at the privilege-elevation moment (rather than, e.g., adding a CSRF token or shortening session TTL) the correct mitigation?

 

**Refinement:** You said 'csrf can be'. Clarify: what specific property of session ID rotation at the privilege boundary makes it effective against the fixation attack vector that neither CSRF tokens nor TTL reduction can address?

 

**Assessment:** The answer commits to the correct structural fix (session ID rotation at the privilege-elevation boundary) and identifies the boundary-crossing nature of the bug, but never describes the fixation attack itself — how the attacker obtains or plants the pre-auth session ID and waits for the victim to authenticate on it. The refinement probe asked specifically why rotation defeats fixation where CSRF tokens and TTL reduction cannot; the response described how rotation is implemented (server-side, atomic) rather than why the replacement of the identifier severs the attacker's pre-auth knowledge from the post-auth credential. The gap is in articulating the attacker's capability and what each candidate mitigation does and does not remove from that capability.

**Literature**

- [remediation] OWASP Session Management Cheat Sheet — §Session ID Lifecycle — 'Renew the Session ID After Any Privilege Level Change' and §Session Attacks — 'Session Fixation' — ~25m
- [remediation] Session Fixation Vulnerability in Web-based Applications — §3 Attack Variants and §4 Countermeasures — full paper, focusing on the attack-tree distinguishing fixation from hijacking and why ID regeneration is the structural fix — ~45m

</small>
</details>

<details>
<summary><samp>q5 · ai-llm · reranker-cross-encoder · pre 2 → post 2 · ceiling —</samp></summary>

<small>

 

**Scenario:** A RAG system over a 2M-document corpus uses a bi-encoder (e.g., a sentence-transformer) to embed documents and queries, then retrieves the top-50 by cosine similarity. Faithfulness evaluations show the retrieved set often contains the right document but ranked at position 20-40, so the top-5 passed into the LLM context misses it. A teammate proposes adding a cross-encoder reranker over the top-50 before truncating to top-5. Explain the architectural distinction between a bi-encoder and a cross-encoder, why a cross-encoder produces better relevance ranking at the cost that prevents you from using it as the first-stage retriever, and what the two-stage retrieve-then-rerank pattern gives up in exchange for the improved top-k quality.

 

**Refinement:** You said 'the cross encoder does it both ways (two pass, forward back)'. Clarify: what is the actual input construction difference between a bi-encoder and a cross-encoder at inference time, and why does that difference prevent precomputing and caching document representations?

 

**Assessment:** The question tested whether the answerer can name the mechanism by which a cross-encoder produces better relevance than a bi-encoder, and why that same mechanism prevents first-stage use. The response correctly identified the latency/throughput tradeoff as the giveup of the two-stage pattern, which is a real B3 fact, but the architectural distinction was substituted with a fabricated 'forward vs forward-back / set-theory surjective-bijective' frame that does not describe either encoder. The refinement probe targeted exactly this gap, and the refine_response moved further from the canonical answer by introducing additional unfounded vocabulary ('canonical normalized tokens', 'hash', 'clustering of embed top-k') rather than committing to or correcting the input-construction model. The gap is at the input-pair construction and the role of joint self-attention.

**Literature**

- [remediation] Sentence-Transformers Documentation — Cross-Encoders — Cross-Encoders — full page including 'Bi-Encoder vs. Cross-Encoder' diagram and 'Retrieve & Re-Rank' chapter (https://www.sbert.net/examples/applications/retrieve_rerank/README.html) — ~45m
- [remediation] Passage Re-ranking with BERT — §3 Method — input representation and §4 Experiments — MS MARCO retrieval pipeline — ~1h 30m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
