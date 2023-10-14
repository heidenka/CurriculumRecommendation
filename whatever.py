import json

import networkx as nx
import matplotlib.pyplot as plt

# Initialize a directed graph
knowledge_graph = nx.DiGraph()

with open('data/dataUWA/unitTriples_complete.json', 'r') as file:
    json_data = json.load(file)

for item in json_data[:1000]:
    head = item["head"]
    tail = item["tail"]
    knowledge_graph.add_node(head)
    knowledge_graph.add_node(tail)
    knowledge_graph.add_edge(head, tail, type=item["type"])


# Visualize the knowledge graph
pos = nx.spring_layout(knowledge_graph)
nx.draw(knowledge_graph, pos, with_labels=True, node_color="lightblue", node_size=300, font_size=8, font_weight="normal", edge_color="gray")
plt.title("Knowledge Graph")
plt.show()
