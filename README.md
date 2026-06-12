

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
industry     swe                                  updated         2026-06-12
scope        cross-domain · grab-bag              duration        1h 9m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  ai-llm             rag-retrieval           ₄   2   ₂
q2  backend            foreign-key-cascade     ₂   2   ₂
q3  security           insecure-direct-file    ₄   3   ₃
q4  systems-distributeddead-letter-queue       ₄   3   ₂
q5  frontend           optimistic-ui-update    ₄   3   ₂

gaps         foreign-key-cascade-semantics · hybrid-search-fusion · orphaned-row-cleanup · rag-retrieval-precision-recall

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · ai-llm · rag-retrieval-precision-recall · pre 3 → post 2 · ceiling b2</samp></summary>

<small>

 

**Scenario:** A documentation search system for 'HelpDeskAI' uses pure dense vector retrieval. Users complain that exact-match queries for product codes like 'SKU-7741-X' and acronyms like 'RBAC' often miss the relevant chunk even though it exists verbatim in the corpus, while conceptual queries ('how do I reset access') work well. The team proposes adding BM25 lexical retrieval alongside the existing dense retrieval and fusing the two result lists. Explain the mechanism: why does dense-only retrieval underperform on exact tokens and acronyms, what does BM25 contribute that embeddings do not, and how does a fusion method like Reciprocal Rank Fusion combine the two ranked lists into one? State what the hybrid approach gives up compared to dense-only (e.g. tuning surface, latency, score incomparability) and name one query class where adding BM25 would not help.

 

**Refinement:** You said 'ranks/merges into a singular list via an aggregated score through weighting'. Clarify: what specific property of Reciprocal Rank Fusion's scoring formula makes it usable across the two lists without requiring the raw scores from each retriever to be on the same scale?

 

**Assessment:** The response correctly characterizes the dense-vs-lexical division of labour, the IDF intuition for why exact codes favour BM25, the hybrid tradeoffs (latency, tuning surface), and a valid no-help query class — solid B3 identification. The gap is the fusion mechanism itself: the original turn describes it only as weighted score aggregation, and the refinement probe (which targets exactly the rank-based property of RRF) is answered with an explicit disclaimer plus three invented alternatives, including a non-existent NLI-entailment pass. The claim that 'raw scores being on the same scale is irrelevant' is directionally true but justified by the wrong mechanism, so the core insight — that RRF uses position (1/(k+rank)) rather than raw score — was never reached. The reading should lead to how RRF's rank-only formula sidesteps score normalization.

**Literature**

- [remediation] Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods — §3 'Reciprocal Rank Fusion' — the RRFscore(d) = Σ 1/(k + rank_i(d)) formula and why k tempers high rankings — ~20m
- [remediation] BM25 for Beginners / Pinecone Hybrid Search guide — §'Combining dense and sparse' and §'BM25' — TF/IDF lexical scoring and why dense embeddings miss high-IDF exact tokens — ~15m

</small>
</details>

<details>
<summary><samp>q2 · backend · foreign-key-cascade-semantics · pre 2 → post 2 · ceiling —</samp></summary>

<small>

 

**Scenario:** A backend service for 'OrderFlow' has an `orders` table and an `order_items` table with `order_items.order_id` referencing `orders.id`. The team is deciding between `ON DELETE CASCADE`, `ON DELETE RESTRICT`, and `ON DELETE SET NULL` on the foreign key, and separately considering doing the child-row cleanup in application code inside a transaction instead. Explain the mechanism of each FK option: what the database does to child rows when a parent is deleted, and which one blocks the delete. Then compare DB-enforced cascade against application-code cleanup — what does each give up (e.g. cross-table atomicity guarantees, visibility/auditability of the deletes, trigger interactions, bulk-delete lock scope)? Commit to which you'd choose for an order/order-items relationship and why.

 

**Refinement:** You said 'ON DELETE RESTRICT, the pointer from the FK table is removed, and the rows in the children references are set to locked/some kind of exclusive no read no write lock'. Clarify: what does the database do to the parent delete operation itself when child rows exist under RESTRICT — does the parent row get removed at any point in that process?

 

**Assessment:** The answer recognizes this is a foreign-key on-delete question and ultimately commits to CASCADE for order/order_items, but it models the database as an OS memory allocator (pointers, overwritable memory, zeroing) rather than as transactional referential actions, so each option's actual effect on child rows and on the parent delete is mischaracterized. The refinement probe asked the decisive question — whether the parent row is ever removed under RESTRICT — and the response stayed unsure and introduced a fabricated queue mechanism, then pivoted to sharding/DHT concerns unrelated to what cascade vs application cleanup trade off. The gap is in the core mechanism of referential actions: what the DB does to child rows for each action, which one aborts the parent delete, and how DB-enforced atomicity compares with application-transaction cleanup on visibility, triggers, and lock scope.

**Literature**

- [remediation] PostgreSQL Documentation — §5.4 Constraints, Foreign Keys — §5.4.5 Foreign Keys — the ON DELETE action subsection (CASCADE / RESTRICT / NO ACTION / SET NULL / SET DEFAULT) — ~20m
- [remediation] Designing Data-Intensive Applications — Ch. 7 §Atomicity and the meaning of ACID (transactions spanning multiple rows/tables) — ~40m

</small>
</details>

<details>
<summary><samp>q3 · security · insecure-direct-file-access · pre 3 → post 3 · ceiling b1–b2 · transitional b3–b4</samp></summary>

<small>

 

**Scenario:** A file-sharing app, 'VaultShare', lets authenticated users download uploaded documents via `GET /download?path=<filename>`, and the handler reads `/var/app/uploads/<path>` from disk. A reviewer flags two issues: (1) a user can pass `path=../../etc/passwd` and (2) any authenticated user can read any other user's file by guessing the filename. Explain the mechanism of the path-traversal vulnerability (why `..` segments escape the intended directory and why naive string prefix checks fail). Then explain why this is also a broken-access-control problem distinct from the traversal. Commit to a fix for each: name the canonical defense for traversal (canonicalize-then-verify-within-base, or opaque ID indirection) and the defense for the authorization gap (server-side ownership lookup). Explain why fixing only the traversal does not fix the access-control issue.

 

**Refinement:** You said '1) This is an issue with the parsing, which is both orthogonal and hinged on the...'. What breaks if that assumption is wrong?

 

**Assessment:** The answer correctly separates the two vulnerabilities and asserts the right top-level direction for each fix (a canonicalize-style traversal defense and a server-side authorization scoping), and correctly insists that containing the traversal does not close the access-control gap. The core articulation gap is twofold: it never states why naive string checks fail (the `..` is resolved by the filesystem after the application's check runs on the pre-resolution string), and it collapses canonicalize-then-verify-within-base into `../`-denylisting — which is the failing approach the prompt flagged. The refinement narrowed but did not close the gap: it reached the pwd/position-in-time intuition without naming the resolution-order mechanism or the precise canonical defense.

**Literature**

- [remediation] OWASP Path Traversal & File Inclusion Prevention — Path Traversal attack page + linked Input Validation Cheat Sheet §'File Path Traversal' — focused chapter on canonicalize-then-verify and why substring/denylist checks fail against `..`, encoded, and symlink variants — ~30m
- [remediation] OWASP API Security Top 10 (2023) — API1:2023 Broken Object Level Authorization — API1:2023 §Description and §How to Prevent — one focused chapter on why object-level authorization is orthogonal to input containment and must be a server-side ownership lookup — ~20m

</small>
</details>

<details>
<summary><samp>q4 · systems-distributed · dead-letter-queue · pre 2 → post 3 · ceiling b1–b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A distributed system, 'EventBus', has consumers reading from a message queue with at-least-once delivery and automatic redelivery on processing failure. One malformed message that always throws on deserialization is now stuck in an infinite redelivery loop, blocking the partition and starving valid messages behind it. The team proposes a dead-letter queue (DLQ) with a max-redelivery count. Explain the mechanism: how a redelivery counter plus a DLQ breaks the loop, where the count is tracked (broker-side delivery count vs. message-header attempt count the consumer increments), and what happens to the message when the threshold is crossed. Explain the tradeoff of setting the retry threshold too low (transient failures get dead-lettered) versus too high (head-of-line blocking persists longer). Distinguish a genuinely poison message from a transient downstream outage and say why the DLQ is the right tool for one but not the other.

 

**Refinement:** You said 'The core issue is the malformed message that throws on deserialization. This is ...'. What breaks if that assumption is wrong?

 

**Assessment:** The answer correctly identifies the poison-message starvation domain and names both the broker delivery-count and consumer header attempt-count tracking sites, but it inverts the central mechanism judgment: it claims the DLQ is the right tool for the transient downstream outage and 'best for timeout retries,' when in fact the DLQ exists to isolate deterministically-failing poison messages while transient outages call for retry/backoff. The refinement walks this back partially — distinguishing a timeout-bound throw from a malformed-schema/registry/trust-boundary failure — but never cleanly states why a deterministic poison message is exactly what the DLQ is for, leaving the core why-under-retry invariant only marginally satisfied. The gap is in the poison-vs-transient classification and the precise consequence of crossing the threshold (out-of-band retention for replay, not 'drop').

**Literature**

- [remediation] Enterprise Integration Patterns — Dead Letter Channel + Invalid Message Channel chapter — the focused chapter distinguishing an invalid (poison) message from a transient processing failure and which channel each belongs to — ~30m
- [remediation] Designing Data-Intensive Applications — DDIA Ch. 11 §Fault Tolerance — at-least-once delivery + idempotent processing, and the distinction between deterministic and transient processing failures (one focused chapter) — ~1h

</small>
</details>

<details>
<summary><samp>q5 · frontend · optimistic-ui-update · pre 3 → post 3 · ceiling b2 · transitional b3</samp></summary>

<small>

 

**Scenario:** A frontend for 'TaskBoard' lets users toggle a task's 'done' checkbox. Currently it disables the checkbox, fires a PATCH request, and only re-enables/updates the UI when the server responds — users perceive lag. The team wants an optimistic update: flip the checkbox immediately, then send the request. Explain the mechanism of an optimistic update: how you snapshot prior state, apply the change to local state before the network call, and reconcile on response. Describe the failure path — what must happen if the PATCH fails or times out (rollback to the snapshot, surface an error). Compare optimistic update against the pessimistic (wait-for-server) approach on the axes of perceived latency and consistency risk, and name one scenario where you would NOT use an optimistic update (e.g. irreversible or money-moving actions) and why.

 

**Refinement:** You said 'the ordering when sent via debounce is incorrect, so the latest state returned persists but not the accurate one'. Clarify: what property of the network or request lifecycle causes an earlier-fired request to resolve after a later one, and how does a snapshot-per-request approach address or fail to address that property?

 

**Assessment:** The answer correctly identified the optimistic snapshot/apply/rollback lifecycle and correctly named the money-moving/irreversible case as off-limits for optimistic updates, which carries it to the B3 direction. The refinement probe targeted the rapid-toggle response-order race; the answer correctly recognized that response resolution order is independent of fire order, but reconciled it via passing full component state to the server for server-side ordering rather than the canonical client-side primitive. The gap is in which layer owns the reconciliation and what primitive enforces last-write-wins on the client without a round trip to the server for ordering.

**Literature**

- [remediation] TanStack Query — Optimistic Updates — Optimistic Updates guide — onMutate (snapshot via getQueryData + cancelQueries), onError (rollback to snapshot), onSettled (invalidate/refetch to reconcile) — ~15m
- [remediation] A Complete Guide to useEffect — Race Conditions in Fetch — §Race conditions / cleanup — response order is independent of request order; AbortController-in-cleanup or a per-request ignore flag collapses the rapid-fire race on the client — ~30m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
