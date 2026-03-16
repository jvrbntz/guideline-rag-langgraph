#!/usr/bin/env python3
"""
Query entrypoint for GuidelineGraph.

Accepts a natural language clinical query, runs it through the
RAG pipeline, and prints the referenced answer.

Usage:
    uv run python query.py
"""

from graph.graph import guideline_graph


def run_query(query: str) -> None:
    """Run a query through the GuidelineGraph pipeline."""
    print(f"\nQuery: {query}\n")

    result = guideline_graph.invoke({"query": query})

    print(f"Answer:\n{result['answer']}")


if __name__ == "__main__":
    query = input("Enter your clinical query: ")
    run_query(query)
