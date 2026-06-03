

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
industry     swe                                  updated         2026-06-03
scope        cross-domain · grab-bag              duration        1h 2m
calibration  b3 "practitioner"                    rotation bias   underindexed-weighted

                                              b₂  b3  b₄
q1  security           security-headers-hsts   ₂   2   ₂
q2  ai-llm             rag-chunk-overlap       ₃   3   ₂
q3  frontend           intersection-observer   ₂   2   ₂
q4  data-engineering   broadcast-join-vs       ₂   2   ₂
q5  sre                connection-draining     ₃   3   ₂

gaps         broadcast-join-vs-shuffle-join · intersection-observer-vs-scroll-listener · join-strategy-selection · layout-thrash

score (dreyfus)    1 (novice) → 3 (competent) → 5 (mastered)
band  (swecom)     b1 (technician) → b3 (practitioner) → b5 (principal)
```

<details>
<summary><samp>q1 · security · security-headers-hsts · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A consumer SaaS app, ShopVerse, serves its login page over HTTPS but does not send an HSTS header. A security reviewer says this exposes users to an SSL-stripping (downgrade) attack even though every page is served over TLS. Walk through (a) the mechanism of an SSL-stripping attack on a first visit when the user types 'shopverse.com' into the address bar, (b) precisely what adding 'Strict-Transport-Security: max-age=31536000; includeSubDomains' changes about the browser's behavior on subsequent visits, and (c) what residual gap HSTS alone does NOT close on the very first-ever visit, and which mechanism (name it) addresses that gap. Explain why each part works the way it does.

 

**Refinement:** You said 'the loophole allows the attacker an attack vector before the actual https is served'. Clarify: what specific network position and action does the attacker take that causes the browser to send the initial request in plaintext rather than over TLS?

 

**Assessment:** The answer correctly places the attacker on-path at the local-network/gateway layer (ARP/routing) and recognizes that a plaintext window precedes TLS, which the refinement sharpened. However, it inverts what HSTS does — it never states that HSTS causes the browser to upgrade http:// to https:// before the request is ever sent — and it names a fabricated mechanism for the first-visit residual instead of the established one. The gaps are in why the header is sufficient on return visits and in identifying the named list-based mechanism that removes the trust-on-first-use exposure.

**Literature**

- [remediation] RFC 6797: HTTP Strict Transport Security (HSTS) — §5 HSTS Mechanism Overview and §8.3 'URI Loading and Port Mapping' — how a UA upgrades http to https before sending; plus §12.1 'No Bootstrap MITM Defense' for the first-visit gap — ~45m
- [remediation] HSTS Preload List Submission — Landing page + 'How does it work?' — the preload directive and the browser-baked list that removes trust-on-first-use exposure — ~10m

</small>
</details>

<details>
<summary><samp>q2 · ai-llm · rag-chunk-overlap · pre 2 → post 3 · ceiling — · transitional b1–b3</samp></summary>

<small>

 

**Scenario:** A RAG system over technical manuals splits documents into fixed 512-token chunks with zero overlap. Users report that answers to questions whose relevant content spans a chunk boundary are frequently incomplete. A teammate proposes adding a 50-token overlap between adjacent chunks. Explain (a) the mechanism by which zero-overlap chunking causes boundary-spanning answers to fail at retrieval time — be specific about what the embedding represents and why a query embedding may match neither neighbouring chunk well; (b) how adding overlap changes the retrieval behaviour and what it gives up (name the cost dimensions); and (c) one alternative approach that addresses boundary loss differently from raw overlap, and the tradeoff that distinguishes it from the overlap approach.

 

**Refinement:** You said 'it gives up similarity/relevance in the chunks at retrieval time/treats each individual retrieval as distint and discrete rather than continious'. Clarify: what property of how a dense embedding is computed over a fixed token window causes a boundary-straddling concept to be underrepresented in both neighbouring chunk vectors, even before any retrieval decision is made?

 

**Assessment:** The answer locates the right domain and, after the refinement probe, arrives at the correct directional insight — that a fixed-window dense embedding's representation biases toward the bulk/body of the chunk, leaving a boundary-straddling concept underrepresented in both neighbouring vectors before any retrieval decision. The gap is in mechanism precision and vocabulary: the pooling operation that produces one vector per window is never named, 'identity/content hashing' and naming Deberta as the embedder point the wrong way on what an embedding is, and the proposed alternative is a hand-rolled context-stream rather than the canonical parent-child / sentence-window pattern that decouples retrieval granularity from context granularity. The cost dimensions and the tradeoff distinguishing the alternative from raw overlap are gestured at but not named as the question explicitly required.

**Literature**

- [remediation] Chunking Strategies for LLM Applications — §Chunk Size Considerations and §Content-Aware Chunking — one focused read on how chunk size and pooled-embedding semantics interact, and why a single vector averages over the window — ~25m
- [remediation] Sentence-Transformers: Retrieve & Re-Rank and Semantic Search — §'Bi-Encoder vs. Cross-Encoder' and §Semantic Search — one chapter on how a bi-encoder produces one independent dense vector per text and why that is semantic, not a hash — ~20m

</small>
</details>

<details>
<summary><samp>q3 · frontend · intersection-observer-vs-scroll-listener · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A media-heavy feed page (think a generic image-grid site, PicWall) lazy-loads images by attaching a scroll event listener that, on each scroll event, calls getBoundingClientRect() on every off-screen image to decide whether to load it. The page janks badly on long feeds. Explain (a) the two distinct mechanisms by which this implementation causes jank — be precise about scroll event firing cadence and what getBoundingClientRect() forces the browser to do mid-scroll; (b) why replacing it with IntersectionObserver fixes both, mechanically (what work moves off the main thread / out of the synchronous path); and (c) one thing IntersectionObserver does NOT give you for free that the scroll-listener approach did, and the tradeoff that implies.

 

**Refinement:** You said 'getBoundingClientRect() is probably doing a top-level parsing of the dom tree to get the bounds for the draw'. Clarify: what specific browser rendering pipeline stage does calling getBoundingClientRect() inside a scroll handler force to run synchronously, and why does that stage become expensive when called repeatedly on many elements in a single event?

 

**Assessment:** The answer correctly identified the two surface culprits (scroll-bound listener + per-element getBoundingClientRect) and correctly flagged getBoundingClientRect as a synchronous call, but never named the specific pipeline stage it forces — a style/layout flush (forced synchronous layout, a.k.a. layout thrashing) — nor the precise scroll-event cadence that multiplies it. The IntersectionObserver explanation substituted Suspense/microtask machinery for the actual mechanism (intersection computed asynchronously, off the synchronous scroll path, delivered only on threshold crossings). The refinement probe pointed directly at the rendering-pipeline stage and the answer still routed into thread/microtask scheduling rather than layout. Part (c) reached for 'pagination/scroll-position' as the lost capability but framed it through a wrong heuristic-pagination model rather than the precise-scroll-geometry tradeoff.

**Literature**

- [remediation] Avoid large, complex layouts and layout thrashing — Chapter: 'Avoid forced synchronous layouts' and 'Avoid layout thrashing' — the read-after-write reflow loop and getBoundingClientRect forcing a synchronous style+layout flush — ~20m
- [remediation] IntersectionObserver API — Section: 'Intersection observer concepts and usage' and 'How does it work' — asynchronous, out-of-band threshold-crossing callbacks vs. synchronous scroll-handler geometry — ~25m

</small>
</details>

<details>
<summary><samp>q4 · data-engineering · broadcast-join-vs-shuffle-join · pre 2 → post 2 · ceiling — · transitional b1</samp></summary>

<small>

 

**Scenario:** A daily Spark batch job joins a 2 TB fact table against a 40 MB dimension table on a single key. By default it triggers a shuffle (sort-merge) join and is slow. An engineer suggests forcing a broadcast join. Explain (a) the mechanism of a shuffle/sort-merge join and why the 40 MB dimension makes it unnecessarily expensive here — be specific about what gets moved across the network; (b) what a broadcast join does instead, mechanically, and why that eliminates the expensive step; and (c) the failure mode and tradeoff of broadcasting — what happens if the engineer broadcasts a table that is too large, and where that cost lands (name the component). Give a rough sense of where the size threshold sits and why it is bounded.

 

**Refinement:** You said 'The full table could overwhelm the endpoint, or even cause cascading failures'. Clarify: which specific component in the Spark architecture receives the full broadcast table on every executor, and why that component — not the network — is typically the binding constraint on broadcast table size?

 

**Assessment:** The answer holds the correct domain — broadcast-vs-shuffle join selection — but the mechanism is described through a borrowed messaging/pub-sub abstraction rather than Spark's actual execution model: it never states that sort-merge hash-partitions and shuffles both sides (the 2 TB fact being the dominant cost), nor that broadcast ships the small side to every executor for a local map-side join. The refinement probe targeted exactly the binding-constraint component, and the candidate honestly disclaimed knowledge, guessing at a state-log/block-partitioning structure rather than naming where the broadcast table actually lands and why memory — not network — bounds its size. The gap is in the physical join-execution mechanism and the memory-replication cost model; the reader should work through how each join physically moves data and which Spark component holds the broadcast copy.

**Literature**

- [remediation] Spark: The Definitive Guide — Ch. 19 §How Spark Performs Joins — the shuffle (sort-merge) join vs. the broadcast join, including which side is sent where — ~45m
- [remediation] Spark SQL Performance Tuning — §Broadcast Hint for SQL Queries and spark.sql.autoBroadcastJoinThreshold — where the broadcast table is collected and why driver/executor memory bounds its size — ~15m

</small>
</details>

<details>
<summary><samp>q5 · sre · connection-draining-load-balancer · pre 2 → post 3 · ceiling — · transitional b1–b3</samp></summary>

<small>

 

**Scenario:** A web service behind an L7 load balancer does rolling deployments. During each deploy, a small but consistent spike of 502/504 errors appears for clients, even though new pods pass readiness checks before old pods are removed. Explain (a) the mechanism producing the errors despite readiness gating — be specific about the race between the load balancer's view of backend health and the actual termination of an old backend, including the role of in-flight and keep-alive connections; (b) how enabling connection draining (deregistration delay) on the load balancer changes the shutdown sequence and why that removes the errors; and (c) one residual case that connection draining alone does NOT fix, and the additional mechanism that closes it.

 

**Refinement:** You said 'letting consumers finish and clean up'. Clarify: what specifically happens to a keep-alive connection that is idle (no in-flight request) during the draining window, and why that behavior produces a residual error case that draining alone does not cover?

 

**Assessment:** The answer correctly localizes the residual failure to the idle keep-alive connection that connection draining cannot observe or wait on, and recognizes it requires explicit retirement rather than passive drain — that core distinction is the heart of part (c). The gap is in the bounding mechanism: it does not state how draining is bounded (LB stops opening new connections and drains in-flight ones up to the deregistration delay) or at what cost (slower deploy), and it names the retirement mechanism in language-runtime terms (cancellation tokens, RAII guards, circuit breaker) instead of the HTTP-layer mechanism that actually closes the case. The refinement reached the right shape of the problem but reached for in-process resource-management vocabulary where the protocol-level keep-alive retirement signal was the answer.

**Literature**

- [remediation] learnk8s — Graceful shutdown and zero downtime deployments in Kubernetes — §'Sending traffic to Pods before they are ready' through §'Delaying shutdown to wait for in-flight requests' — the one focused chapter covering endpoint-propagation lag, preStop sleep, and the SIGTERM/deregistration ordering — ~25m
- [remediation] HTTP/1.1 Connection Management & HTTP/2 GOAWAY — MDN / RFC 9113 — MDN 'Connection management in HTTP/1.x' §Keep-alive and the Connection header; companion RFC 9113 §6.8 GOAWAY — the focused subsection on how a server retires a persistent connection it intends to close — ~20m

</small>
</details>

<sub><samp><i>widget regenerated from fortifai's data/session.json via profile_widget.py</i></samp></sub>
</details>
