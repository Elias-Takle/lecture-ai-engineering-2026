"""第3回 演習・宿題（実装）のテスト。APIキーもLLMも使わない（TestModel）。"""

import json

import pytest
from pydantic_ai import DeferredToolRequests
from pydantic_ai.messages import ToolCallPart, ToolReturnPart
from pydantic_ai.models.test import TestModel

from app import tools
from app.agent import agent, run_with_approval


def _parts(result, kind):
    return [p for m in result.all_messages() for p in m.parts if isinstance(p, kind)]


def test_make_quiz_returns_question_and_answer_from_that_lecture():
    quiz = json.loads(tools.make_quiz(2))
    assert quiz["question"] and quiz["answer"] and quiz["lecture"] == 2
    lecture2_defs = {t["definition"] for t in tools.load_glossary() if t["lecture"] == 2}
    assert quiz["answer"] in lecture2_defs


def test_make_quiz_handles_lecture_without_terms():
    assert "ありません" in tools.make_quiz(0)
    assert "ありません" in tools.make_quiz(99)


def test_make_quiz_is_registered_and_visible_to_the_model():
    model = TestModel(call_tools=["make_quiz"])
    with agent.override(model=model):
        result = agent.run_sync("第2回の復習問題を1問出して")
    offered = {t.name: t for t in model.last_model_request_parameters.function_tools}
    assert "make_quiz" in offered
    assert "復習問題" in offered["make_quiz"].description
    assert {p.tool_name for p in _parts(result, ToolCallPart)} == {"make_quiz"}
    assert _parts(result, ToolReturnPart)


@pytest.fixture
def log_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path / "learning_log")
    return tmp_path / "learning_log"


def test_save_learning_log_writes_a_file(log_dir):
    msg = tools.save_learning_log("LoRA", "rank r は表現力を決める")
    files = list(log_dir.glob("*.md"))
    assert len(files) == 1 and "保存しました" in msg
    text = files[0].read_text(encoding="utf-8")
    assert "# LoRA" in text and "rank r" in text


def test_without_approval_nothing_is_saved(log_dir):
    with agent.override(model=TestModel(call_tools=["save_learning_log"])):
        result = agent.run_sync("今日の学びを記録して")
    assert isinstance(result.output, DeferredToolRequests)
    assert [c.tool_name for c in result.output.approvals] == ["save_learning_log"]
    assert not log_dir.exists()


def test_approved_call_is_saved(log_dir):
    result = run_with_approval(agent, "記録して", TestModel(call_tools=["save_learning_log"]), approve=lambda c: True)
    assert isinstance(result.output, str)
    assert len(list(log_dir.glob("*.md"))) == 1


def test_denied_call_is_not_saved(log_dir):
    result = run_with_approval(agent, "記録して", TestModel(call_tools=["save_learning_log"]), approve=lambda c: False)
    assert isinstance(result.output, str)
    assert not log_dir.exists() or not list(log_dir.glob("*.md"))
