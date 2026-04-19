"""
Tests for conditional routing logic in graph/edges.py
"""

from graph.edges import route_after_classification, route_after_grading


def test_route_after_classification_in_scope():
    state = {"query_scope": "yes"}
    result = route_after_classification(state)
    assert result == "retrieve"


def test_route_after_classification_out_of_scope():
    state = {"query_scope": "no"}
    result = route_after_classification(state)
    assert result == "end"


def test_after_grading_filtered_documents():
    state = {"filtered_documents": ["doc1"]}
    result = route_after_grading(state)
    assert result == "generate"


def test_after_grading_no_filtered_documents():
    state = {"filtered_documents": []}
    result = route_after_grading(state)
    assert result == "rewrite_query"
