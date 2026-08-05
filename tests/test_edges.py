"""
Tests for conditional routing logic in graph/edges.py
"""

from graph.edges import route_after_classification, route_after_grading


def test_route_after_classification_in_scope():
    """route_after_classification returns 'retrieve' when query_scope is 'yes'."""
    state = {"query_scope": "yes"}
    result = route_after_classification(state)
    assert result == "retrieve"


def test_route_after_classification_out_of_scope():
    """route_after_classification returns 'end' when query_scope is 'no'."""
    state = {"query_scope": "no"}
    result = route_after_classification(state)
    assert result == "end"


def test_route_after_classification_absent_key():
    """route_after_classification fails safe to 'end' when query_scope is absent.

    Unreachable via graph.py's current wiring (classify_query always runs
    first) — documents the function's own fail-safe contract in isolation.
    """
    state = {}
    result = route_after_classification(state)
    assert result == "end"


def test_route_after_grading_filtered_documents():
    """route_after_grading returns 'generate' when filtered_documents is non-empty."""
    state = {"filtered_documents": ["doc1"]}
    result = route_after_grading(state)
    assert result == "generate"


def test_route_after_grading_no_filtered_documents():
    """route_after_grading returns 'rewrite_query' when no documents passed grading."""
    state = {"filtered_documents": []}
    result = route_after_grading(state)
    assert result == "rewrite_query"
