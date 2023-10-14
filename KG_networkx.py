import networkx as nx
import matplotlib.pyplot as plt
import json
# Create a directed graph
graph = nx.DiGraph()

with open('data/dataUWA/unitTriples_complete.json', 'r') as file:
    json_data = json.load(file)



for triplet in json_data[:50]:
    head = triplet['head']
    tail = triplet['tail']
    edge_type = triplet['type']

    # Add nodes and edges to the graph
    graph.add_node(head)
    graph.add_node(tail)
    graph.add_edge(head, tail, type=edge_type)

plt.figure(figsize=(10, 8))
pos = nx.spring_layout(graph)  # Positions for all nodes

# Draw the graph nodes and edges
nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=12, font_weight='bold', edge_color='gray', width=1.5)

# Draw edge labels
edge_labels = {(u, v): d['type'] for u, v, d in graph.edges(data=True)}
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10)

plt.title('Knowledge Graph')
plt.show()