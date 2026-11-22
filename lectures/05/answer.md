# 第5回 解答 (Lecture 5 Answer)

## 演習 (Exercise)

- Answer model (`[model]` at run time): gemini-3.5-flash-lite
- Question compared: 「第2回の説明では、LoRAは何を固定し何を学習しますか？ QLoRAは何を加えますか？」 (In Lecture 2, what does LoRA freeze and what does it train? What does QLoRA add?). One question only; each method run once.
- Target materials: Full text used all 9 documents / 438 pages (227,971 characters of input). Vector search, Tree and Graph used the Lectures 1–3 main lectures, 214 pages. The scopes differ, so this is not a strictly like-for-like comparison.

### Results per method

| Method | Answer summary and correctness | Cited pages and evidence | Time (s) | Input / output tokens | Model responses | Est. generation API cost (USD) |
|---|---|---|---|---|---|---|
| Full text | Partial. It did not explain what LoRA freezes or trains, or what QLoRA adds. It only pointed to pages and gave "hints". | p.51, p.52 (right pages, but their content was not used in the answer) | 5.22 | 117,025 / 335 | 1 | $0.035945 |
| Vector search | Correct. LoRA freezes the original weights and trains only two thin small matrices A and B (the delta). QLoRA adds 4-bit compression of the original weights. | p.51, p.52 | 6.73 | 3,028 / 196 | 2 | $0.001398 |
| Tree | Correct. Same content, explained from the full text of p.52 alone. | p.52 only | 12.55 | 9,214 / 307 | 5 | $0.003532 |
| Graph | Correct. Same LoRA/QLoRA explanation as vector search. | p.51, p.52 | 7.90 | 5,776 / 197 | 2 | $0.002225 |

- **Search only (what was found, and what the text confirmed):**
  `uv run python -m app.retrieval "LoRA QLoRA 違い"` returned p.52, p.51, p.60, p.47, p.61 in that order.
  The text of p.52 says the original weights are frozen and only a small delta is trained (LoRA), and that QLoRA also compresses the original weights to 4 bit. That page alone answers the question. p.51 is the PEFT overview and adds supporting detail on LoRA vs QLoRA.
  p.60 and p.61 are Lecture 2 exercise pages that only mention QLoRA, and p.47 is about "RAG works better for adding knowledge". They are pages on a similar topic, not evidence for the answer.
- **Tool calls seen with `--trace`:**
  - Vector search: `search_materials` called once (query "LoRA 固定 学習 QLoRA 加える"); 2 model responses.
  - Tree: `browse_tree` called 4 times. Path: lecture list → `lec02-main` → chapter `lec02-main-s045` → page `lec02-main-p052`. Only p.52 was read in full (717 characters). 5 model responses. p.51 was never opened, so only p.52 was cited.
  - Graph: `search_graph` called once (query "LoRA QLoRA 固定 学習 第2回"). In another run with the same default setting, the model also called `search_graph("term:lora")` as a second search, which raised input to 16,484 tokens and cost to $0.004413 (see Advanced below).
- **Missing evidence vs. evidence not used:**
  - Missing evidence: none. Every method retrieved p.52, so there was no retrieval miss on this question.
  - Evidence available but not used: full text. It cited p.51 and p.52 but did not state their content. There was no input-limit error (117,025 tokens ran fine), so the cause is not search or input size. It is more likely the answer policy in the instructions ("do not write the homework answer itself; guide with hints"). This is a single run, so I can't call it a weakness of full text itself.
  - Tree read only the pages it needed, so the p.51 supplement was not cited.
- **Method I would adopt, why, and limits of the comparison:**
  For single-page questions like this one I would adopt vector search. It was correct, cited p.51 and p.52, and was the cheapest: 3,028 input tokens and $0.001398 (about 1/26 of the full-text cost and about 1/39 of its input tokens).
  Limits: (1) only one question, each method run once. (2) Full text covered 438 pages while the others covered 214. (3) Time varied between runs of the same setting (6.73 s, 9.67 s, 8.68 s for vector search), so I did not use time to rank methods and compared tokens, cost and cited evidence instead. (4) I did not run a multi-page or a not-in-the-materials question, so I can't say where Tree or Graph would be better.
- **Observations and questions:**
  - Input tokens are almost identical for the same setting (3,027–3,028), but output tokens and time change every run.
  - Even when retrieval is right, cost can swing depending on whether the model makes extra searches (Graph: 2.9x more tokens in one run).
  - Question: on a multi-page question (Lecture 3 p.13, 39, 40), can Tree or Graph reach all the needed pages?

## 宿題 (Homework)

- **Level attempted:** Basic / Implementation / Advanced (all three done; any one completes the homework, so Basic alone is enough).
- **What I did:**
  - Basic: changed `RAG_TOP_K` in `app/config.py` from 5 to 2 (nothing else changed).
  - Implementation: added `search_with_neighbors()` to `app/retrieval.py`. For each search hit it also adds the text of the page before and after in the same document, skips duplicate pages, and keeps the hits first. In `app/tools.py`, `search_materials` uses it only when the environment variable `AIE_NEIGHBORS=1` is set, so I could switch between normal and neighbour search.
  - Advanced: added `GRAPH_RELATIONS` (environment variable `AIE_GRAPH_RELATIONS`) to `app/config.py`, so `search_graph` can follow only `next_page` edges, only `mentions` edges, or both.
    - Data shape: in `graph.json` the nodes are pages and terms; the edges are `next_page` (page to the next page) and `mentions` (a term appears on a page).
    - Search method: vector search finds the top 3 pages as entry points, then the graph is walked up to 2 hops, returning at most 10 pages including the entry pages.
    - Why this design: I did not know whether "neighbouring page" edges or "shared term" edges add candidates, so I compared results per edge type.
- **Question and fixed conditions:** same question as the exercise (Lecture 2, LoRA and QLoRA), model gemini-3.5-flash-lite, target = Lectures 1–3 main lectures (214 pages). One run per condition.

### Results (from `--trace` output)

**Basic: RAG_TOP_K 5 → 2**

| | Before (K=5) | After (K=2) |
|---|---|---|
| Tool calls | `search_materials` once, query "LoRA 固定 学習 QLoRA 加える" | same |
| Cited pages | p.51, p.52 | p.51, p.52 |
| Answer correct? | Yes | Yes |
| Time | 6.73 s | 10.26 s |
| Input / output tokens | 3,028 / 196 | 1,741 / 207 |
| Est. cost | $0.001398 | $0.001040 |

Input tokens dropped about 42% and cost about 26%. Time went up, but the same setting varies between 6.73 and 9.67 s, so I do not attribute that to K.

**Implementation: add the previous and next page**

| | Normal search | With neighbour pages (AIE_NEIGHBORS=1) |
|---|---|---|
| Tool calls | `search_materials` once, query "LoRA QLoRA 固定 学習" | same |
| Cited pages | p.51, p.52 | p.51, p.52 |
| Answer correct? | Yes | Yes |
| Time | 9.67 s | 5.49 s |
| Input / output tokens | 3,027 / 218 | 5,334 / 213 |
| Est. cost | $0.001453 | $0.002133 |

Input rose about 76% and cost about 47%, with no change in the answer or the cited evidence.

**Advanced: which graph edges to follow**

| Setting | Cited pages | Time | Input / output | Est. cost | Tool calls |
|---|---|---|---|---|---|
| `next_page` only | LoRA: p.52; QLoRA: p.51, p.52 | 4.02 s | 5,814 / 156 | $0.002134 | `search_graph` once |
| `mentions` only | p.51, p.52 | 4.14 s | 6,047 / 228 | $0.002384 | `search_graph` once |
| both (default), run 1 | p.51, p.52 | 7.90 s | 5,776 / 197 | $0.002225 | `search_graph` once |
| both (default), run 2 | p.51, p.52 | 6.63 s | 16,484 / 227 | $0.004413 | `search_graph` twice (second query `term:lora`) |
| (baseline) vector search | p.51, p.52 | 6.73 s | 3,028 / 196 | $0.001398 | `search_materials` once |

- **Examples that improved, and what still fails:**
  - Improved: Basic K=2. The two needed pages (p.51 and p.52) were already the top 2 hits, so the same evidence cost about 42% fewer input tokens.
  - Did not improve: Implementation neighbour pages. p.51 and p.52 were already found by normal search, so the extra neighbour pages were not needed for this question and only added cost. The trace truncates the tool output, so I could not confirm exactly which pages were added.
  - Advanced: for this question, `next_page` only, `mentions` only and both gave the same correct answer. All three graph settings used about 5.8–6.0k input tokens, roughly 2x vector search, and none added new evidence. I could not see any effect of the edge type on this question.
  - The biggest cost increase came not from the edge type but from the model making an extra search (`term:lora`): 16,484 tokens, $0.004413. The same setting gives different results from run to run.
  - Remaining limits: all three levels used a single question and a single run per condition, and time is noisy. I did not test a multi-page question (Lecture 3 p.13, 39, 40; p.39 and p.40 are adjacent pages) where neighbour pages or graph edges are most likely to help.
- **Observations and questions:**
  - Changing the number or range of retrieved pages changes cost before it changes answer quality. Comparing before/after by cited pages, tokens and cost was clearer than comparing time.
  - Without repeating runs under the same conditions, I can't tell whether a difference in time or extra searches comes from the setting or from chance.
  - Question: do neighbour pages and `mentions` edges actually add evidence on questions that span several pages?
- **AI tool use:** I did this work myself, with Claude helping me understand the steps, suggest the code changes and organise the report. I ran every command in Codespaces, checked the cited lecture pages myself, and the numbers are from my own terminal output.
