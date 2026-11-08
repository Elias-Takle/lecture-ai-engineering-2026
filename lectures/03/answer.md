# Lecture 3 Answer

## Exercise

- How the Lecture 1 (plain LLM) answer differs from the agent's (question: 「AIE2026の講座の宿題にある「3レベル」とは何ですか？」):
  - Plain LLM (`app.ask`): it did not know the course. It gave several generic guesses (for example levels of AI usage, or course difficulty such as Basic / Advanced / Expert) and asked me for more details, such as slide wording. It never mentioned the course's real levels (基礎 / 実装 / 発展) or that completing any one finishes the homework.
  - Agent (`app.agent`): it answered with the course definition: three levels, 基礎 (check the lecture content), 実装 (write code yourself), 発展 (investigate or try something new), and choosing any one completes the homework (generally not graded). It ended with "(関連回: 第1回)".
  - Difference: a plain LLM only has its training memory, so it fills the gap with plausible general answers. The agent can look up the glossary before answering, so its answer matches the course data (`homework-levels` in data/glossary.json).

- Tool calls seen with `--trace` (question: "LoRAとQLoRAの違いは？"):
  ```
  [tool call]   search_glossary({'query': 'LoRA'})
  [tool call]   search_glossary({'query': 'QLoRA'})
  [tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "...
  [tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "...
  [usage] ... requests=2, tool_calls=2
  ```

- LLM calls for one question (`requests`): 2 (with 2 tool calls).
  Both searches were requested in the same model response (parallel calls), so one request asked for the tools and one request wrote the final answer.

- Tool I added and the description in its docstring:
  - `make_quiz(lecture: int) -> str` in app/tools.py, registered with `agent.tool_plain(tools.make_quiz)` in app/agent.py.
  - It collects the glossary terms of the given lecture, picks one at random and returns JSON `{question, answer, lecture}`. If the lecture has no terms it returns a message instead of crashing.
  - Docstring (the model reads this): "Pick one term of the given lecture and return a review question and its answer. Use it when asked for a quiz / review question / check question, like 'Give me one review question for Lecture 2'. `lecture` is the lecture number (integer, from 1)."
  - `--list-tools` shows make_quiz with its docstring and argument `{"lecture": {"type": "integer"}}`.
  - Trace for "第2回の内容から確認問題を1問出して":
    ```
    [tool call]   make_quiz({'lecture': 2})
    [tool return] make_quiz -> {"question": "「Hugging Face Hub」とは何ですか？", "answer": "公開されたモデルやデータセットを共有・ダウンロードできるプラットフォーム。...
    [usage] ... requests=2, tool_calls=1
    ```
    The model showed only the question and did not reveal the answer, which follows the INSTRUCTIONS line "don't write homework answers, guide with hints".
  - `uv run pytest -q`: 18 passed in 5.25s (final run, after all homework changes).

## Homework

- Level worked on: Basic, Implementation and Advanced (a). Any one completes the homework; I did all three.

### Basic: change INSTRUCTIONS / a docstring and compare

Same question every time: `uv run python -m app.agent --trace "LoRAとQLoRAの違いは？"`. I changed one thing per run and restored the file afterwards.

- Run 0: no change (baseline)
- Run A: deleted the INSTRUCTIONS line "必ず search_glossary で用語集を確認する"
- Run B: in the search_glossary docstring, changed "1つだけ" to "複数入れてよい"

| Run | Tool calls | tool_calls | requests | input tokens | output tokens | cost |
|---|---|---|---|---|---|---|
| 0 | search_glossary('LoRA'), search_glossary('QLoRA') | 2 | 2 | 1402 | 204 | 0.0009306 |
| A | search_glossary('LoRA'), search_glossary('QLoRA') | 2 | 2 | 1354 | 195 | 0.0008937 |
| B | search_glossary('LoRA QLoRA') | 1 | 2 | 887 | 228 | 0.0008361 |

- Run A: The model still searched twice. The search_glossary docstring also says "use before answering", so removing the INSTRUCTIONS line alone did not change tool use. Only the answer style changed: it no longer opened with "according to the glossary". Input tokens dropped slightly because the prompt is shorter.
- Run B: The model made one combined search instead of two. Input tokens fell about 37% (1402 to 887) and cost about 10%. The answer was still correct because my search function matches both words in one query (I also checked this by hand: `search_glossary("LoRA QLoRA")` returns LoRA and QLoRA).
- `requests` stayed at 2 in every run. It counts LLM round trips, not tool calls. In Run 0 both searches were asked for in one response, so it still took only 2 requests.

### Implementation: save_learning_log with approval

What I built:
- `save_learning_log(topic, note)` in app/tools.py writes a markdown file into `learning_log/`.
- Registered in app/agent.py with `agent.tool_plain(tools.save_learning_log, requires_approval=True)`, and the agent has `output_type=[str, DeferredToolRequests]`.
- `run_with_approval()` runs the agent. When the result is `DeferredToolRequests`, it shows the pending call, asks `[y/N]`, and continues the run with `DeferredToolResults`.

Results:
- Question: `--trace "学習記録を保存して: 題名 LoRA, 内容 rank r はアダプタの大きさ"`
- Answered `y`:
  ```
  [承認が必要] save_learning_log({'topic': 'LoRA', 'note': 'rank r はアダプタの大きさ'})
  実行してよいですか？ [y/N]: y
  [tool return] save_learning_log -> 保存しました: 20261108-140542-312911.md
  [usage] ... requests=1, tool_calls=1
  ```
  The file was saved.
- Answered `n`:
  ```
  [承認が必要] save_learning_log(...)
  実行してよいですか？ [y/N]: n
  [tool return] save_learning_log -> The tool call was denied.
  [usage] ... requests=1
  ```
  The tool did not run (no `tool_calls` in the usage), and the model told me the save was refused and nothing was saved.
- Tests with TestModel (no API key): `uv run pytest -q` gives 18 passed (11 original tests plus 7 new ones in tests/test_homework.py). They check that without approval nothing is saved, approved saves a file, and denied saves nothing.

Observations:
- The approval is enforced by my program, not by the model. The tool really did not run when I answered `n`.
- In the `y` run the model did not call search_glossary at all and ended with "(関連回: 第6回)". The glossary only has lectures 1, 2, 3 and 5, and LoRA is in Lecture 2. So that lecture number was a guess. The INSTRUCTIONS rule "end with the related lecture" is followed in form but not guaranteed in content.
- `requests=1` in these runs. I think this is because the run is resumed with the earlier message history, and the usage shown only counts the resumed part. The first request (which asked for the tool call) is not included. I did not verify this.
- An old test (`test_base_tools_are_registered_and_called`) had to be changed to call only the two base tools. A tool that waits for approval has a call but no return yet, so the old check "returns == calls" fails.

### Advanced (a): rebuild with Google ADK

- Files: adk_agent/glossary_agent/__init__.py (`from . import agent`) and adk_agent/glossary_agent/agent.py. The INSTRUCTIONS and the tools (search_glossary, get_lecture_summary, make_quiz) are reused from app/. Run command:
  `PYTHONPATH=. uv run --with google-adk adk run adk_agent/glossary_agent`
- Code comparison:

  | | Pydantic AI (app/agent.py) | ADK (adk_agent/glossary_agent/agent.py) |
  |---|---|---|
  | Create the agent | `Agent(instructions=..., output_type=...)` | `Agent(model=, name=, instruction=, tools=[...])` |
  | Instructions argument | `instructions` | `instruction` (no "s") |
  | Register tools | `agent.tool_plain(fn)` one by one | `tools=[fn, fn, ...]` in the constructor |
  | Model | passed at run time (`run_sync(..., model=)`) | passed in the constructor |
  | Approval / trace | `requires_approval`, `--trace` | not rebuilt (not required) |

- Answers: I asked "LoRAとQLoRAの違いは？" twice in one ADK session. Both answers described LoRA as training small low-rank matrices and QLoRA as 4-bit quantization plus LoRA, and both ended with "関係する回: 第2回". The wording was different each time. Compared with the Pydantic AI runs, the facts and the closing lecture line are the same.
- Limit: `adk run` has no `--trace`, so I cannot see which tools ADK called. I can only say that the answers match the glossary definitions and cite the right lecture, which suggests the glossary was used.

## Observations / questions

- An agent is model + loop + tools. The model only writes text, and my program runs the tools and feeds the results back.
- The Lecture 1 vs Lecture 3 comparison shows why tools matter: the plain LLM guessed generic "levels", while the agent returned the course's real definition.
- Instructions and docstrings both steer tool use. Removing one of two overlapping sentences did not change behavior (Run A), but changing the docstring did (Run B).
- LLM output varies between runs (the two ADK answers differ), and each of my experiments was run once, so the style differences may be random. The tool-call and token counts are stronger evidence.
- Actions that cannot be undone, such as saving, should be gated by program code (`requires_approval`), because the model can be confidently wrong, as with "第6回" above.
- Question: if a query contains several terms and the glossary search only returns the top 3 results, could one of the terms be missed?
- AI tools: I used an AI assistant to help draft the code (make_quiz, save_learning_log, the approval flow, the ADK agent) and to help structure this write-up. I ran every command myself in Codespaces, and the traces, token counts, approval prompts, ADK answers and the 18 passing tests above are from my own runs.
