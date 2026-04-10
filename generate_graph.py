"""
Generate a visual representation of the GuidelineGraph V2 pipeline
Run after any graph changes to update the visualization.

usage:
    uv run python generate_graph.py
"""

from graph.graph import guideline_graph

graph_image = guideline_graph.get_graph().draw_mermaid_png()
with open("docs/graph_v2.png", "wb") as f:
    f.write(graph_image)

print("Graph saved to docs/graph_v2.png")
