

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
industry     swe                                  updated         2026-05-25
scope        cross-domain · grab-bag              duration        54m 11s
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  backend            serializable-vs         ₃   2   ₁
q2  security           open-redirect           ₂   2   ₁
q3  ml-engineering     regularization-path     ₂   2   ₁
q4  systems-distributedread-repair             ₂   2   ₁
q5  frontend           controlled-input        ₂   2   ₁

gaps         anti-entropy · controlled-input-cursor-jump · feature-correlation-l1-instability · l1-vs-l2-mechanism

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · backend · serializable-vs-snapshot-isolation · pre 2 → post 2 · ceiling — · transitional b1–b2</samp></summary>

<small>

 

**Scenario:** A scheduling app stores on-call shifts in PostgreSQL. The business rule: at least one engineer must be on-call at all times. The handoff transaction reads `SELECT COUNT(*) FROM oncall WHERE shift = 'graveyard' AND active = true` and, if the count is at least 2, sets one engineer's `active` to false. Two engineers click 'go off-call' simultaneously. The app uses the default isolation level (Read Committed). After both transactions commit, zero engineers are on-call. The team proposes upgrading to Repeatable Read. Will that fix it? Explain what anomaly is occurring, why Repeatable Read is or isn't sufficient, and what the correct mechanism is. Identify the tradeoff of your chosen fix.

 

**Refinement:** You said 'write commited ensures the state is not a "speculative at read" but a "on write commit then we read in and select count(*)" kind of thing'. Clarify: what specific ordering guarantee prevents two concurrent transactions from each reading a count of 2, deciding it is safe to deactivate, and both committing their update — even when writes are atomic?

 

**Assessment:** The answer never names the anomaly under test (write-skew) and never names the actual isolation levels relevant to the question (Snapshot Isolation, Serializable). It invents an isolation level ('write committed') that does not exist in the SQL standard or in PostgreSQL, and misattributes the fix to ordering atomic writes ahead of reads — inverting the real mechanism, since both transactions' reads were already valid within their own snapshots; the violation is a property of the conjunction of disjoint writes against a predicate. The refinement probe correctly redirected attention to the read snapshot, and the answer surfaced MVCC by name, but treated MVCC as the reconciliation mechanism rather than as the substrate of snapshot isolation that is itself the reason write-skew is possible. The gap is in distinguishing what snapshot isolation guarantees (per-transaction consistent reads, first-committer-wins on the same row) from what it does not (multi-row predicate invariants), and in knowing the canonical Postgres-level fix.

**Literature**

- [remediation] Designing Data-Intensive Applications — Chapter 7 — Transactions, especially §Snapshot Isolation and Repeatable Read (pp. 237–242), §Write Skew and Phantoms (pp. 246–251), and §Serializability — Serializable Snapshot Isolation (SSI) (pp. 261–266). — ~4h
- [remediation] PostgreSQL Documentation — Chapter 13: Concurrency Control — §13.2.2 Repeatable Read Isolation Level and §13.2.3 Serializable Isolation Level — read both to see Postgres's explicit statement that Repeatable Read = Snapshot Isolation and does not detect write-skew, and that SERIALIZABLE adds predicate locking (SIREAD) with serialization_failure (SQLSTATE 40001) requiring application retry. — ~45m

</small>
</details>

<details>
<summary><samp>q2 · security · open-redirect · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A SaaS login page accepts a `?next=` query parameter and, after successful login, issues an HTTP 302 redirect to the value of `next`. The developer added validation: the value must start with `/`. A security report shows attackers are using URLs like `https://app.example.com/login?next=//evil.example/phish` to redirect users to attacker-controlled sites post-login, where a clone of the app harvests credentials on a follow-up 're-login' prompt. Explain why the `startsWith('/')` validation fails, what class of vulnerability this is, and the correct mechanism to fix it. Identify the tradeoff between a strict allowlist of redirect targets versus a same-origin parse-and-check approach.

 

**Refinement:** You said 'the '/' only addresses the start, does not allow the cross request to be sane or valid'. Clarify: what specific property of the string `//evil.example/phish` allows a browser to treat it as a cross-origin destination despite beginning with `/`?

 

**Assessment:** The answer recognized the validation was unsafe and reached for a defense-in-depth posture, but did not name the vulnerability class (Open Redirect, CWE-601) and could not articulate why `//evil.example/phish` is parsed as an authority component despite beginning with `/`. The refinement was a direct probe for the parsing primitive and the answer fell back on DNS and unspecified browser behavior. The gap is in URL grammar — specifically the distinction between path-relative and authority-relative references — and in the corresponding mitigation pattern that parses the candidate URL against the app's origin rather than inspecting its prefix.

**Literature**

- [remediation] OWASP Cheat Sheet Series — Unvalidated Redirects and Forwards Cheat Sheet — Full cheat sheet (Background, Safe URL Redirects, Dangerous URL Redirects, Preventing Unvalidated Redirects and Forwards) — ~20m
- [remediation] RFC 3986: Uniform Resource Identifier (URI): Generic Syntax — §4.2 Relative Reference (network-path, absolute-path, relative-path references) and §5.3 Component Recomposition — ~25m

</small>
</details>

<details>
<summary><samp>q3 · ml-engineering · regularization-path · pre 1 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A team trains a logistic regression on 200 features to predict churn. They try L1 regularization (alpha=0.1) and get a sparse model selecting 12 features with AUC 0.81. They retrain on a refreshed dataset that's 90% the same rows, expecting roughly the same selected features — but only 4 of the 12 features overlap, even though AUC is again 0.81. The product team is alarmed: 'the model is unstable.' Explain the mechanism that causes L1 to swap among correlated features between runs, why the AUC stays stable even as the selected feature set shifts, and what the correct tool is if the goal is reliable feature selection rather than predictive performance. Identify the tradeoff of switching to L2 or elastic net.

 

**Refinement:** You said 'those 4 categories have some kind of'. Clarify: what property of the L1 penalty's geometry causes it to select different members from a group of correlated features even when no data leakage is present?

 

**Assessment:** The answer misclassified an L1-regularization-instability scenario as a data-leakage / metric-selection problem, despite the scenario explicitly stating the data is 90% overlapping and AUC is stable across runs — both of which are diagnostic against leakage and for the canonical L1 correlated-feature instability. Under refinement the answerer pivoted toward the regularization hyperparameter but, by their own admission, lacked the formal grounding to name the geometric property of the L1 penalty (axis-aligned constraint region producing near-degenerate optima among correlated features) and did not surface stability selection, elastic net's grouping effect, or the L2-loses-sparsity tradeoff. The gap is foundational: the mechanism by which L1 produces sparsity, and why that same mechanism is unstable under feature correlation.

**Literature**

- [remediation] An Introduction to Statistical Learning — Ch. 6 §6.2 Shrinkage Methods — read 6.2.1 Ridge Regression and 6.2.2 The Lasso end-to-end, paying particular attention to Figure 6.7 (the diamond vs circle constraint regions) and the discussion of why L1 produces sparse solutions while L2 does not — ~1h 30m
- [remediation] Regularization Paths for Generalized Linear Models via Coordinate Descent / Elastic Net for sparse high-dimensional models — Zou & Hastie 2005 §2 'Naive Elastic Net' and §3 'Grouping Effect' (pp. 304–308) — establishes why elastic net handles correlated feature groups; then Meinshausen & Bühlmann 2010 'Stability Selection' §1–2 for the resampling-based stable-selection procedure — ~2h

</small>
</details>

<details>
<summary><samp>q4 · systems-distributed · read-repair · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A Dynamo-style key-value store uses quorum reads/writes (N=3, R=2, W=2) over three replicas. The team observes that some keys remain divergent across replicas for hours after a transient network blip — specifically, keys that are written once and rarely read. They have read-repair on the read path. Explain why read-repair alone is insufficient for this access pattern, name the mechanism that is the correct complement, and describe how it works at a high level (what data structure, what is exchanged between replicas, why it's bandwidth-efficient). Identify the tradeoff in tuning its frequency.

 

**Refinement:** You said 'it somehow generates the mapping per write time (flips the bit? reconciles at snapshot sync during quorum, divergences or blips surface it in a simple xor bit check or the likes)'. Clarify: what property of the data structure allows two replicas to identify *which specific key ranges* are divergent without exchanging the full keyspace, and how does the structure's shape enable that localization?

 

**Assessment:** The answerer correctly diagnosed why read-repair is insufficient — the access pattern means rarely-read keys never trigger healing — which is the B1-level identification. Beyond that, the answer never reaches the canonical complement (Merkle-tree anti-entropy) and its defining property (hierarchical hash comparison enabling O(log N) range localization). The refinement probe pointed directly at the structural property that enables range-localization without full keyspace exchange; the response instead committed to DHT hash-table routing, conflating a key-placement structure with a replica-reconciliation structure. The gap is in recognizing the canonical Dynamo-family primitive for background convergence and its structural shape, not in articulation.

**Literature**

- [remediation] Dynamo: Amazon's Highly Available Key-value Store — §4.7 'Handling Permanent Failures: Replica Synchronization' — Merkle tree construction, root-hash comparison, and recursive descent into divergent subtrees — ~25m
- [remediation] Designing Data-Intensive Applications — Ch. 5 §Leaderless Replication — 'Read repair and anti-entropy' subsection (pp. 178–179) — ~15m

</small>
</details>

<details>
<summary><samp>q5 · frontend · controlled-input-cursor-jump · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A React form has a controlled text input bound to component state. The onChange handler uppercases the value before calling setState. Users report that when they type a character in the middle of an existing word, the cursor jumps to the end of the input on every keystroke. Explain the mechanism causing the cursor jump (what does React do with the input's value attribute on each render, and how does that interact with the browser's selection state), and describe the correct fix. Identify the tradeoff between using an uncontrolled input with a ref versus preserving the cursor position manually in the controlled-input approach.

 

**Refinement:** You said 'React probably calls a state update on the attribute/the dom render node with the attribute'. Clarify: what specifically does React do to the DOM input's value attribute during reconciliation, and why does that DOM operation cause the browser to reset the cursor position rather than preserve it?

 

**Assessment:** The answer identifies the right surface elements — controlled input, reconciliation, selection state, the two candidate fixes — but substitutes a fabricated mechanism (re-render scheduling, microtask fencing, 'cursor bound to render-space') for the documented DOM behavior that actually drives the bug. The refinement probe asked specifically what React does to the input's value during reconciliation and why that resets the cursor; the response doubled down on a spatial subtree-re-render metaphor rather than naming the DOM property assignment whose specified side effect collapses the selection. The tradeoff discussion gestures at the right axis (rigidity vs. flakiness) without naming what each approach actually owns. The gap is at the level of a single specific DOM API and its specified interaction with selection state.

**Literature**

- [remediation] HTMLInputElement: setSelectionRange() method & value property — MDN — HTMLInputElement.value §'Setting the value' note on selection reset, and HTMLInputElement.setSelectionRange() reference. Read both pages end-to-end (roughly one focused chapter's worth). — ~30m
- [remediation] How (and why) React updates DOM input values during reconciliation — 'React as a UI Runtime' — Reconciliation section, focused chapter read. Covers how React diffs props and applies them to host DOM nodes, including value, which directly addresses what the refinement probe asked. — ~45m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
