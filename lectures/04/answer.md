# 第4回 解答

## 演習

- 基準別の一致率（直す前）：根拠　/　、範囲　/　、ヒント　/　、分かりやすさ　/　、回の表示　/　
- 要確認の件数（直す前）：
- 直した基準と、書き足した方針：
- 基準別の一致率と要確認の件数（直した後）：
- 講師のラベルと自分のラベルで判定が違った項目と、そう判定した理由：
- 気づき・疑問：

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
- 取り組んだレベル (Level): Basic
- やったこと (What I did):
  I graded the same 10 items against the same labels.jsonl, with the same grader model (gemini-3.5-flash-lite, temperature 0), before and after changing the wording of data/eval/rubric.md.
  Change: - 回答の本文が 300 字以内なら、簡潔とみなす
  I also tried switching the grader to gemini-3.5-flash, but the run stopped with "Rate limit reached" after 6 of 10 items, so I have no result for it.
- 結果 (Results):
  | Criterion | Before | After |
  |---|---|---|
  | Grounding | 7/9 (1 needs review) | 8/10 |
  | Scope | 9/10 | 10/10 |
  | Hints | 10/10 | 10/10 |
  | Clarity | 8/10 | 8/10 |
  | Lecture reference (code) | 10/10 | 10/10 |
  | Overall agreement | 9/9 (coverage 90%) | 10/10 (coverage 100%) |
  | Needs review | 1 | 0 |
  | Disagreements | 5 | 4 |
- 気づき・疑問 (Notes):
  - Needs review fell from 1 to 0 because #05 (not in the glossary, then explained generally) was no longer sent to a human.
  - Overall agreement rose from 9/9 to 10/10, but this is not a fair comparison. After the change, 10 items are graded automatically instead of 9, so there is one more chance for the grader to be wrong.
  - The disagreements moved around instead of just shrinking. #06 and #10 Scope disappeared, while #08 Grounding and #08 Clarity appeared. My change was about #05, so it should not have affected #06 or #08. This suggests grader noise.
  - A third run with the unchanged rubric (still showing #05 as needs review) gave different numbers from the first run, even at temperature 0 (Grounding 6/9 instead of 7/9, Clarity 9/10 instead of 8/10). One run is not enough to trust a small change.
  - #04 Clarity and #10 Grounding disagreed in every run. The rubric explicitly says repeated explanations are a Fail, so these may be mistakes in my own labels rather than the grader's. When a grader and a human disagree every time, check the human label first.
  - Question: how many repeated runs do I need before I can say a rubric change really helped?
  - What I checked myself: I read the disagreement lines in each run, compared the before and after files with diff, and checked #04 and #10 against the rubric.
