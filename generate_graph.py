"""
Generate a visual representation of the LangGraph pipeline
Run once to produce graph.png for documentation
"""

from graph.graph import guideline_graph

graph_image = guideline_graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(graph_image)

print("Graph saved to graph.png")
