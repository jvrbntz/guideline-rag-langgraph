"""
The GraphState for guideline_rag_langgraph

Defines the shared state object passed between all nodes in the pipeline.
Every field represents data that needs to flow between nodes.
"""

from typing_extensions import TypedDict
from langchain_core.documents import Document


class GraphState(TypedDict):
    """Shared state passed between all nodes in the guideline_rag_langgraph pipeline."""

    query: str  # user's original question
    documents: list[Document]  # retrieved chunks from ChromaDB
    filtered_documents: list[Document]  # chunks that passed grading
    answer: str  # final generated response
