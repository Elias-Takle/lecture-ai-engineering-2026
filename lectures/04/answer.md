# Lecture 4 Answer (第4回 解答)

## Exercise (演習)

- Per-criterion agreement, before fixing (my labels vs. LLM, 10 items): Grounding 7/9 (1 needs review), Scope 9/10, Hints 10/10, Clarity 8/10, Lecture reference (code) 10/10. Overall agreement 9/9 (coverage 90%).
- Needs-review count, before fixing: 1 item. #05 Grounding: the answer says "RAG is not in the glossary" and then explains it in general, which the rubric listed as "not yet decided", so the LLM marked it unsure.
- Criterion I fixed and the policy I added: Grounding. [CONFIRM with `git --no-pager diff data/eval/rubric.md`, then correct this sentence if needed] I added one line to the Grounding section of data/eval/rubric.md: saying "not in the glossary" for a missing term and then explaining it in general is not an assertion (pass). I removed the matching bullet from the "not yet decided" section.
- Per-criterion agreement and needs-review count, after fixing: Grounding 7/10, Scope 9/10, Hints 10/10, Clarity 9/10, Lecture reference (code) 10/10. Overall agreement 10/10 (coverage 100%). Needs review: 0. Disagreements: 5.
  - #04 Clarity: LLM = fail, me = pass
  - #06 Grounding: LLM = fail, me = pass
  - #08 Grounding: LLM = fail, me = pass
  - #10 Grounding: LLM = fail, me = pass
  - #10 Scope: LLM = pass, me = fail
- Items where my labels differ from the instructor's, and why: [FILL IN: run `uv run python -m app.judge --compare lectures/04/reference/labels_instructor.jsonl` (one line) and list each difference with a one-line reason]
- Notes and questions:
  - Needs review went from 1 to 0, and #05 is no longer a disagreement, so the policy line did what it was meant to do: the grader now decides #05 itself and agrees with me.
  - The Grounding agreement did not improve: 7 of 9 before, 7 of 10 after. One more item is now graded automatically, and three of the five remaining disagreements are Grounding.
  - On #06, #08 and #10 the LLM marks Grounding as fail for behaviors that belong to other criteria (writing the homework code, printing the whole glossary, claiming a plan that is not in the reference). My labels put those failures on Hints, Scope and Grounding respectively. This suggests the Grounding rule is too broad and should say that only statements that contradict or go beyond the glossary count.
  - On #04 the rubric says repeated explanations fail Clarity, so the grader may be right and my Pass label wrong.
  - On #10 the answer claims content "will be added later", which the reference does not say, so the grader's Fail on Grounding looks right. My labels (Grounding pass, Scope fail) look swapped.
  - Runs of the same setup gave different numbers, so I would repeat the grading a few times before trusting a one-item change.

## Homework (宿題)



- Level: Advanced

- What I did:
  - Dataset: SWE-bench Verified
    - Data: https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified
    - How it was built (official): https://openai.com/index/introducing-swe-bench-verified/
    - Later re-audit (official): https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
  - Items I read (summaries only, no full text pasted). In every item the agent gets only the text of a GitHub issue and must fix the code:
    1. astropy__astropy-12907: `separability_matrix` (a matrix showing which outputs depend on which inputs) gives a wrong result for nested compound models. The symptom is clear from a short reproduction, but fixing it means understanding how the code walks through nested models, so a patch that only hides the symptom would not be enough.
    2. astropy__astropy-13033: TimeSeries gives a confusing error message when a required column is missing. The goal is clear, but the issue text does not fix what the "correct" message is, which I think is the hard part for an LLM.
    3. astropy__astropy-13236: asks whether structured columns should still be converted automatically into NdarrayMixin. It reads more like a design discussion, so the agent has to decide how much to change, and the requirements are vague.
    4. astropy__astropy-13398: proposes a direct way to transform ITRS coordinates to an observer's frame while staying inside ITRS. It needs astronomy knowledge about coordinate frames and rotation matrices. I could not solve it myself, and an LLM would need that specialist knowledge too.
  - OpenAI's later audit also names sympy__sympy-18199 (`nthroot_mod` misses the root x = 0 mod p) as an example where the tests check extra behavior that the issue text never mentions.
  - How it was built (from OpenAI's blog):
    - The original SWE-bench (2023, Jimenez et al., Princeton NLP) was made from resolved issues in 12 open-source Python repositories. Each task comes with the pull request that fixed it, including its code and unit tests.
    - Verified (August 2024, OpenAI together with the SWE-bench authors): 93 developers experienced in Python reviewed 1,699 randomly chosen tasks from the original test set. Each task was labeled independently by 3 different people.
    - They looked at two things: is the issue description underspecified, and do the unit tests reject valid solutions. Each gets a severity from 0 to 3. They also estimated how long the fix would take and allowed free-text flags for other problems.
    - The 3 labels are combined by taking the most severe one. A task is removed if the severity is 2 or higher, or if any other major problem was flagged.
    - For training, OpenAI engineers first labeled 50 tasks very carefully, and annotators had to pass an onboarding test built from them.
    - Result: 38.3% were flagged as underspecified and 61.1% as having unfair tests. In total 68.3% were removed, leaving 500 tasks (as many 1-4 hour and 4+ hour tasks as possible, the rest chosen at random).
  - How it is graded: not by matching a reference answer, but by running unit tests the agent cannot see. FAIL_TO_PASS tests check that the described behavior now works, and PASS_TO_PASS tests check that nothing else broke. Both must pass. Grading runs automatically in Docker environments.
  - Comparison with today's evaluation set:

    | Aspect | SWE-bench Verified | Today's evaluation set |
    |---|---|---|
    | Scale | 500 tasks (selected from 1,699) | 10 items |
    | Who made it | Real repository PRs (answer and tests) plus 93 reviewers | 1 instructor |
    | Number of validators | 3 independent people per task | 1 instructor (plus me and an LLM as graders) |
    | Removal | 68.3% removed | None removed; failures were added on purpose |
    | Grading | Executable tests with a fixed right answer | T/F/unsure by humans and an LLM; only "Lecture N" checked by code |
    | What it measures | Can the agent fix the issue? | Can the grader (LLM) be trusted? |
    | Ambiguous cases | Removed | Marked unsure and sent to a human |

- Results:
  - Numbers: 93 developers, 1,699 reviewed, 3 reviewers per task, 500 kept, 68.3% removed.
  - Later re-audit (February 2026, OpenAI): they audited 138 problems that o3 did not solve consistently (about 27.6% of Verified), each reviewed by at least 6 engineers. 59.4% had serious problems in the tests or the description: 35.5% had tests too strict about implementation details, and 18.8% tested features the issue never mentioned. They also found signs that the public problems and repositories were seen in training (contamination). OpenAI stopped reporting Verified scores and recommends SWE-bench Pro.

- What I noticed or wondered:
  - Three reviewers per task, with the strictest label winning, still left many serious flaws in the hardest tasks later on. More checking is not a guarantee of correctness.
  - Grading with tests sounds objective, but if the test is wrong the grade is wrong. Our "Lecture N" code check has the same limit: it only checks what its rule was written for.
  - Our "unsure goes to a human" rule and Verified's "remove if doubtful" rule share one idea: do not mix cases that cannot be graded into the automatic numbers.
  - Our own runs showed the same kind of problem on a small scale: the LLM grader gave different numbers on repeated runs of the same set, so even a checking method needs to be checked.
  - Questions: at the scale of 500 items, how much human work would it take to measure agreement between LLM grading and human labels? And how well can a private 10-item set avoid contamination compared with a public benchmark?
  - What I checked myself (keep only what I really did before submitting):
    - [ ] I read 3-5 items in the Hugging Face Dataset Viewer myself
    - [ ] I checked 93 / 1,699 / 500 / 68.3% in OpenAI's blog post
    - [ ] I checked 138 / 59.4% in OpenAI's February 2026 post
  - AI use: Claude helped me research the official pages and write the first draft.