"""LangGraph state schema for the multi-agent QA flow."""

from typing import TypedDict


class QAState(TypedDict,total=False):
    """
    The state flows through four agents:
1. Planning Agent: analyzes `question` and generates a search `plan` and `sub_questions`
2. Retrieval Agent: populates `context` using `question` and `sub_questions`
3. Summarization Agent: generates `draft_answer` from `question` + `context`
4. Verification Agent: produces final `answer` from `question` + `context` + `draft_answer``

The `enable_planning` flag allows toggling query decomposition on/off.
    """

    question: str
    plan: str | None
    sub_questions: str | None
    context: str | None
    draft_answer: str | None
    answer: str | None
    enable_planning: bool
