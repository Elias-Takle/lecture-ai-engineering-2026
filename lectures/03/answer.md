# Homework Report

## Level Worked On
Basic

## What I Did

Ran the same question 3 times with `--trace` ("LoRAとQLoRAの違いは？"), changing exactly one thing each time, and restored the file after each run.

- **Run 0:** No change (baseline).
- **Run A:** Deleted the INSTRUCTIONS line "必ず search_glossary で用語集を確認する".
- **Run B:** In the search_glossary docstring, changed "1つだけ" to "複数入れてよい".

## Results

| Run | Tool calls | tool_calls | requests | input tokens | cost |
|---|---|---:|---:|---:|---:|
| 0 | search_glossary('LoRA'), search_glossary('QLoRA') | 2 | 2 | 1402 | 0.0009306 |
| A | search_glossary('LoRA'), search_glossary('QLoRA') | 2 | 2 | 1354 | 0.0008937 |
| B | search_glossary('LoRA QLoRA') | 1 | 2 | 887 | 0.0008361 |

### Run A

The model still searched twice. The search_glossary docstring also says to use it before answering, so removing the INSTRUCTIONS line alone did not change tool use. Only the answer style changed: it no longer opened with "according to the glossary".

### Run B

The model made one combined search instead of two. Input tokens fell about 37% and cost about 10%, and the answer was still correct because search_glossary matches both words in one query.

## Observations / Questions

- Requests did not change even when tool_calls dropped. Requests counts LLM round trips. In Run 0 the model asked for both searches in one response (parallel calls), so it still needed only 2 requests.
- INSTRUCTIONS and docstrings overlap. To really stop the model from searching, I would probably have to change both places. I did not test this.
- Each run was done once, and LLM output varies, so style differences in the answers may be random. The tool-call and token counts are the stronger evidence.
- **Question:** If one query contains several terms and the code only returns the top 3 results, could a term be missed?
- I used an AI assistant to draft the code and plan, and I ran the commands and read the traces myself.
