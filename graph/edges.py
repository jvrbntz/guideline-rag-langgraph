"""
Conditional edge functions for GuidelineGraph.

V1: route_after_grading - proceed to generate or end.
V2: route_after_classification - scope guard before retrieval.
     route_after_grading - updated to support query rewriting loop (max 3 retries).
"""

from graph.state import GraphState
from logger import get_logger

logger = get_logger(__name__)


def route_after_grading(state: GraphState) -> str:
    """Route after grading — proceed to generate or end if no relevant docs found."""
    if state["filtered_documents"]:
        route = "generate"
    elif state.get("rewrite_count", 0) < 3:
        route = "rewrite_query"
    else:
        route = "end"

    logger.info(
        f"route_after_grading: kept={len(state['filtered_documents'])} rewrite_count={state.get('rewrite_count', 0)} → {route}"
    )
    return route


def route_after_classification(state: GraphState) -> str:
    """Route after classifying the query whether it's within scope."""
    route = "retrieve" if state["query_scope"] == "yes" else "end"
    logger.info(
        f"route_after_classification: query_scope={state['query_scope']} → {route}"
    )
    return route
