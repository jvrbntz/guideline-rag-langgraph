"""
Conditional edge functions for GuidelineGraph.

V1: Single routing function after grade_documents.
V2: Will add query rewriting loop and hallucination check routing.
"""

from graph.state import GraphState


def route_after_grading(state: GraphState) -> str:
    """Route after grading — proceed to generate or end if no relevant docs found."""
    if state["filtered_documents"]:
        return "generate"
    elif state["rewrite_count"] < 3:
        return "rewrite_query"
    else:
        return "end"


def route_after_classification(state: GraphState) -> str:
    """Route after classifying the query whether it's within scope."""
    if state["query_scope"] == "yes":
        return "retrieve"
    return "end"
