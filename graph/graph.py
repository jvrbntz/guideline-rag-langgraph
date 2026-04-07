"""
Graph assembly for GuidelineGraph.

Builds and compiles the LangGraph pipeline:
classify_query → retrieve → grade_documents → generate (or END if out of scope or no relevant documents found)
"""

from langgraph.graph import END, START, StateGraph

from graph.edges import route_after_classification, route_after_grading
from graph.nodes import classify_query, generate, grade_documents, retrieve
from graph.state import GraphState

graph_builder = StateGraph(GraphState)

graph_builder.add_node("classify_query", classify_query)
graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("grade_documents", grade_documents)
graph_builder.add_node("generate", generate)

graph_builder.add_edge(START, "classify_query")
graph_builder.add_edge("retrieve", "grade_documents")
graph_builder.add_conditional_edges(
    "classify_query", route_after_classification, {"retrieve": "retrieve", "end": END}
)

graph_builder.add_conditional_edges(
    "grade_documents", route_after_grading, {"generate": "generate", "end": END}
)

graph_builder.add_edge("generate", END)

guideline_graph = graph_builder.compile()
