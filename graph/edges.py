"""
Conditional edge functions for GuidelineGraph.

V1: route_after_trading - proceed to generate or end.
V2: route_after_classification - scope guard before retrieval.
     route_after_grading - updated to support query rewriting loop (max 3 retries).
"""

from graph.state import GraphState


def route_after_grading(state: GraphState) -> str:
    """Route after grading — proceed to generate or end if no relevant docs found."""
    if state["filtered_documents"]:
        return "generate"
    elif state.get("rewrite_count", 0) < 3:
        return "rewrite_query"
    else:
        return "end"


def route_after_classification(state: GraphState) -> str:
    """Route after classifying the query whether it's within scope."""
    if state["query_scope"] == "yes":
        return "retrieve"
    return "end"
