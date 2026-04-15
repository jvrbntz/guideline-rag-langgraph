#!/usr/bin/env python3
"""
Query entrypoint for guideline-rag-langgraph.

Accepts a natural language guideline query, runs it through the
RAG pipeline, and prints the referenced answer.

Usage:
    uv run python query.py
"""

import logging

import config
from graph.graph import guideline_graph
from logger import get_logger

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("chromadb").setLevel(logging.WARNING)

logger = get_logger(__name__)


def run_query(query: str) -> dict:
    """Run a query through the guideline-rag-langgraph pipeline and return the result."""
    logger.info(f"query received: '{query}'")
    result = guideline_graph.invoke(
        {"query": query, "rewritten_query": "", "rewrite_count": 0}
    )
    logger.info("query completed")
    return result


if __name__ == "__main__":
    query = input("Enter your clinical guideline query: ")
    result = run_query(query)
    print(f"\nQuery: {query}\n")
    if result.get("answer"):
        print(f"Answer:\n{result['answer']}")
    elif result.get("query_scope") == "no":
        print("This query is outside the scope of the ATS/IDSA 2019 CAP guideline.")
    else:
        print("No relevant guideline found after 3 query rewrites.")
