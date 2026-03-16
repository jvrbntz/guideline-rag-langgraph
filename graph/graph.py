"""
Graph assembly for GuidelineGraph.

Builds and compiles the LangGraph pipeline:
retrieve → grade_documents → generate (or END if no relevant documents found)
"""

from langgraph.graph import StateGraph, START, END

from graph.nodes import retrieve, grade_documents, generate
from graph.state import GraphState
from graph.edges import route_after_grading

graph_builder = StateGraph(GraphState)

graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("grade_documents", grade_documents)
graph_builder.add_node("generate", generate)

graph_builder.add_edge(START, "retrieve")
graph_builder.add_edge("retrieve", "grade_documents")
graph_builder.add_conditional_edges(
    "grade_documents", route_after_grading, {"generate": "generate", "end": END}
)

graph_builder.add_edge("generate", END)

guideline_graph = graph_builder.compile()
