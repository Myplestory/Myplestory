

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
industry     swe                                  updated         2026-05-27
scope        cross-domain · grab-bag              duration        58m 13s
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  systems-distributedleader-election-split   ₂   2   ₁
q2  sre                connection-pool         ₅   4   ₃
q3  frontend           react-context-rerender  ₃   3   ₂
q4  ai-llm             rag-chunk-context-loss  ₂   2   ₁
q5  data-engineering   partition-key-skew-vs   ₂   2   ₁

strengths    connection-pool-exhaustion-cascade · downstream-slowdown-amplification · timeout-budget-propagation
gaps         election-liveness · high-cardinality-partition-anti-pattern · leader-election-split-vote · parent-child-chunking

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · systems-distributed · leader-election-split-vote · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A team is building a small coordination service for a fleet of 5 stateless workers. They've implemented Raft for leader election but are seeing a pathology in a test environment: when the current leader is killed, the cluster sometimes takes 8-15 seconds to elect a new leader instead of the expected sub-second recovery. Logs show multiple nodes incrementing `currentTerm` repeatedly, each triggering a new election that fails to gain a majority, then timing out and trying again at a higher term. All five nodes are configured with an election timeout of exactly 150ms. Explain what mechanism is producing the repeated failed elections, what specific configuration choice is causing it, and what the canonical fix is. Also explain *why* that fix works — what property of the system it restores.

 

**Refinement:** You said 'relaxing the timeout so the election properly propogates throughout the cluster'. Clarify: what specific property of the timeout values across nodes — not the absolute duration — prevents two nodes from both becoming candidates at the same moment?

 

**Assessment:** The response correctly identified that the 150ms election timeout is implicated but misdiagnosed the mechanism as a propagation/latency issue rather than a symmetry problem across nodes. The refinement probe pointed explicitly at the cross-node property of the timeout values (as distinct from the absolute duration), but the post-refinement answer invoked replication monotonicity and propagation latency — still missing the canonical Raft primitive that resolves this class of pathology. The gap is in recognizing why identical timeouts across all five nodes produce a self-perpetuating failure that no amount of absolute-duration relaxation will fix, and what specific Raft design choice restores election liveness without sacrificing safety.

**Literature**

- [remediation] In Search of an Understandable Consensus Algorithm (Extended Version) — the Raft paper — §5.2 'Leader Election', pp. 5–7 — specifically the paragraphs on election timeouts, split votes, and randomization (the 'randomized election timeouts' rationale) — ~30m
- [remediation] Designing Data-Intensive Applications — Ch. 9 §'Distributed Transactions and Consensus' → 'Fault-Tolerant Consensus' and 'Membership and Coordination Services', pp. 364–373 — ~45m

</small>
</details>

<details>
<summary><samp>q2 · sre · connection-pool-exhaustion-cascade · pre 4 → post 4 · ceiling b3 · transitional b4</samp></summary>

<small>

 

**Scenario:** Service A (an HTTP API) calls Service B synchronously on every request. Service A runs 20 pods, each with a connection pool of 50 to Service B. Normal p50 latency to Service B is 30ms; Service A's request rate is ~2000 RPS aggregate. One afternoon, Service B's p50 latency degrades to 800ms (some upstream DB issue on B's side). Within minutes, Service A starts returning 503s on requests that don't even touch Service B's functionality — including health-check probes that hit local-only endpoints. Explain the mechanism by which Service B's slowdown produces Service A returning 503s on unrelated traffic. Quantify roughly how much offered concurrency Service A's pool can sustain at 30ms vs 800ms latency. Then describe two distinct mitigations Service A can adopt to prevent this failure mode, naming for each what it gives up.

 

**Refinement:** You said 'bulkhead and failfast, circuit breakers'. Clarify: what each mitigation gives up in terms of correctness, availability, or operational complexity when adopted by Service A.

 

**Assessment:** The answer correctly identifies pool saturation as the mechanism by which a downstream slowdown produces 503s on unrelated traffic, and arrives at a roughly correct order-of-magnitude quantification of pool capacity at the two latencies. The refinement adds the cost dimension to both mitigations — bulkhead's isolation overhead and circuit breaker's availability sacrifice — satisfying the B3 'bounded at what cost' invariant. Two gaps remain: the worker-pool-vs-connection-pool distinction that specifically explains health-probe 503s on local endpoints is implicit rather than named, and the quantification is never tightened into the explicit concurrency = RPS × latency relation that makes the cliff legible. The mitigation discussion also stops short of dismissing alternatives (timeout tightening, load shedding, async decoupling) that a B4 answer would weigh against the chosen pair.

**Literature**

- [remediation] Site Reliability Engineering — Addressing Cascading Failures — Ch. 22 §Server Overload and §Resource Exhaustion — caller-side thread/connection holding under retries; Little's-Law-style capacity arithmetic for synchronous calls — ~45m
- [growth] Release It! Design and Deploy Production-Ready Software (2nd ed.) — Connects the bulkhead + circuit breaker pair you named into the full stability-patterns catalog (timeouts, steady state, fail fast, handshaking, test harness) so the next-level question — which combination to commit to and what each commits the system's operating envelope to — becomes answerable. — ~6h

</small>
</details>

<details>
<summary><samp>q3 · frontend · react-context-rerender-fanout · pre 2 → post 3 · ceiling — · transitional b1–b3</samp></summary>

<small>

 

**Scenario:** A React app wraps its entire component tree in a single `<AppContext.Provider value={{ user, theme, notifications, cart, featureFlags }}>`. The provider's value is reconstructed as a new object literal on every render of the root component. A developer notices that typing in a search input (which only reads `featureFlags.searchEnabled` from context) causes the entire UI — including a 200-row product list, a notifications panel, and a cart sidebar — to re-render on every keystroke, even though none of those components read the field being changed. Explain the mechanism by which all these components re-render. Be specific about *what* React compares to decide whether a context consumer must re-render, and why `React.memo` on the consumer components does not fix this. Then describe two distinct remediations, and identify which one is more appropriate when the context legitimately contains five unrelated concerns.

 

**Refinement:** You said 'React decused to re-render the entire thing because it cannot identify at a root context level what node to isolate and change'. Clarify: what specific value does React compare between renders to decide whether a context consumer must re-render, and why that comparison produces the result it does when the provider's value is an object literal?

 

**Assessment:** The answer correctly identified that a root-level context with high-churn state causes wide re-rendering and chose a defensible remediation direction (segregating high-churn from low-churn state). The refinement probe did move the answer toward the correct primitive — recognizing that React compares the object literal between renders and re-renders when they 'do not equal' — but the candidate could not name the comparison (Object.is / referential identity) or explain why React.memo cannot intercept context-driven re-renders (because context consumers subscribe out-of-band, separate from the parent→child prop path that memo gates). The second remediation ('microtask rather than js Task') is incoherent and reveals the gap is in the consumer-subscription model itself, not in scheduling. The reading should fill in the value-identity comparison and the selector-subscription alternative.

**Literature**

- [remediation] React Docs — useContext: Optimizing re-renders — useContext reference, §'Optimizing re-renders when passing objects and functions' — single focused subsection covering the Provider value-identity rule, why useMemo is required for object literals, and the consumer-subscription model that bypasses React.memo — ~15m
- [remediation] Zustand Docs — Prevent rerenders with selectors — Zustand 'Prevent rerenders with selectors' guide — chapter covering selector subscriptions, shallow equality, and how this differs structurally from context fan-out — ~20m

</small>
</details>

<details>
<summary><samp>q4 · ai-llm · rag-chunk-context-loss · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A RAG system over a corpus of ~5000 technical PDFs (product manuals, each 50-300 pages) is producing answers that are factually correct at the sentence level but frequently miss critical qualifying context — e.g., the model confidently states a configuration value applies to all models when the surrounding paragraph in the source PDF made clear it applies only to a specific hardware revision. The pipeline uses 512-token chunks with 50-token overlap, top-k=5 retrieval, and a strong reranker. Embedding recall@5 on a labelled eval set is ~95%. Explain why a high retrieval recall can still produce answers that drop qualifying context. Name the canonical retrieval-architecture pattern that addresses this, describe its mechanism concretely (what gets embedded vs what gets sent to the LLM), and explain the tradeoff it makes against a naive 'just use bigger chunks' approach.

 

**Refinement:** You said 'you dont embed the whole document, you embed the heuristics/encoded value of the content and the canonicalized data as hashes, and then you fetch the relevant data before querying the actual content you need'. Clarify: what specific relationship between the unit used for similarity search and the unit sent to the LLM preserves the qualifying context that the 512-token chunk boundary cut off?

 

**Assessment:** The question was pointing at a specific, named retrieval-architecture pattern — small-to-big / parent-child / sentence-window retrieval — where the unit indexed for similarity search is intentionally different from the unit handed to the LLM. The response proposed an invented two-phase hashing scheme instead, and the refinement probe directly asked about the unit-relationship without surfacing the canonical decoupling. The gap is in the recognition that retrieval granularity and generation granularity are independently tunable through a parent-pointer in vector-store metadata. The 'bigger chunks' tradeoff was also dismissed without naming the actual axis (embedding-signal dilution under topic averaging).

**Literature**

- [remediation] LlamaIndex Documentation — Hierarchical Node Parser and Auto-Merging Retriever — Auto Merging Retriever example (full page) plus the HierarchicalNodeParser and SentenceWindowNodeParser sections of the node parsers guide — read the small-to-big mechanism, the parent_id pointer in node metadata, and the merge-on-retrieval logic. — ~45m
- [remediation] Chunking Strategies for LLM Applications — Chunk Size Considerations and Content-Aware Chunking sections — read why larger chunks dilute embedding signal and why retrieval-granularity and context-granularity should be decoupled. — ~25m

</small>
</details>

<details>
<summary><samp>q5 · data-engineering · partition-key-skew-vs-cardinality · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A Parquet/Iceberg table holds 3 years of clickstream events (~50 TB). The team partitioned by `event_date` (daily) and `user_id` thinking it would speed up per-user queries. After 18 months they have ~200 million tiny Parquet files; queries that filter by `event_date` alone now take 40 minutes because the planner spends most of its time listing files and reading footers. Per-user queries (filter on both `event_date` and `user_id`) are fast. Explain why partitioning on `user_id` produced this pathology, what property of a column makes it suitable vs unsuitable as a partition key, and why partition pruning doesn't rescue the date-only query path. Then commit to a partitioning redesign and explain how the desired per-user lookup performance can be preserved without using `user_id` as a partition key.

 

**Refinement:** You said 'partition based on event_date normally, but then at merge time generate a hybrid columnar scheme ( the user aggregate is chunked based on date)'. Clarify: what specific property of that chunking arrangement causes the planner to visit fewer files when filtering on event_date alone, compared to the current two-level partition layout?

 

**Assessment:** The answer correctly identifies that user_id partitioning is the source of the pathology and that the date-only query is the suffering path, but reasons about the mechanism at the wrong abstraction layer — CPU cache locality, page misses, and heap calls — rather than the metadata layer where this problem actually lives (per-file footer reads, object-store listing cost linear in file count, the inability of partition pruning to eliminate sub-partitions on a column not in the predicate). The refinement was a direct invitation to name what makes the redesigned layout visit fewer files; the response did not converge on the canonical primitives (compaction to right-size files, partition by date only, recover per-user lookup via Bloom filter in the Parquet footer or Z-order/liquid clustering on user_id with per-file min/max stats evaluated at scan planning). The gap is vocabulary and layer-of-abstraction, both addressable by the same reading.

**Literature**

- [remediation] Apache Parquet Documentation — File Format and Bloom Filter Specification — §File Format (footer/metadata layout, row groups, column chunks, pages) and §Bloom Filter (per-column footer storage, predicate pushdown evaluation) — ~45m
- [remediation] Delta Lake / Iceberg Documentation — Data Skipping, Z-Ordering, and Compaction — §Data Skipping (per-file min/max statistics), §Z-Ordering (multi-dimensional clustering via Morton curve), §Compaction / OPTIMIZE (rewrite_data_files, bin-packing, write amplification tradeoffs) — ~1h

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
