"""LangGraph orchestration for the linear multi-agent QA flow."""

from functools import lru_cache
from typing import Any, Dict

from langgraph.constants import END, START
from langgraph.graph import StateGraph

from .agents import retrieval_node, summarization_node, verification_node,planning_node
from .state import QAState


def create_qa_graph() -> Any:
    """Create and compile the linear multi-agent QA graph.

    The graph executes in order:
    1. Retrieval Agent: gathers context from vector store
    2. Summarization Agent: generates draft answer from context
    3. Verification Agent: verifies and corrects the answer

    Returns:
        Compiled graph ready for execution.
    """
    builder = StateGraph(QAState)

    # Add nodes for each agent
    builder.add_node("planning", planning_node)
    builder.add_node("retrieval", retrieval_node)
    builder.add_node("summarization", summarization_node)
    builder.add_node("verification", verification_node)

    # Define linear flow: START -> retrieval -> summarization -> verification -> END
    builder.set_entry_point("planning")

    builder.add_conditional_edges(
        "planning",
        lambda state: "retrieval" if state["enable_planning"] else "retrieval",
    )

    builder.add_edge("planning", "retrieval")
    builder.add_edge("retrieval", "summarization")
    builder.add_edge("summarization", "verification")
    builder.add_edge("verification", END)

    return builder.compile()


@lru_cache(maxsize=1)
def get_qa_graph() -> Any:
    """Get the compiled QA graph instance (singleton via LRU cache)."""
    return create_qa_graph()


def run_qa_flow(question: str, enable_planning: bool = True) -> Dict[str, Any]:
    """Run the complete multi-agent QA flow for a question.

    This is the main entry point for the QA system. It:
    1. Initializes the graph state with the question
    2. Executes the agent flow (Planning → Retrieval → Summarization → Verification)
    3. Extracts and returns the final results

    Args:
        question: The user's question.
        enable_planning: Whether to enable the query planning agent.

    Returns:
        Dictionary with keys:
        - answer
        - context
        - plan
        - sub_questions
    """
    graph = get_qa_graph()

    initial_state: QAState = {
        "question": question,
        "enable_planning": enable_planning,  
        "plan": None,
        "sub_questions": None,
        "context": None,
        "draft_answer": None,
        "answer": None,
    }

    final_state: QAState = graph.invoke(initial_state)

    #Explicit response shaping (important)
    return {
        "answer": final_state.get("answer"),
        "context": final_state.get("context"),
        "plan": final_state.get("plan"),
        "sub_questions": final_state.get("sub_questions"),
    }
