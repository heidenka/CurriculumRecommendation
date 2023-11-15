import json
import networkx as nx # neo4j
import matplotlib.pyplot as plt
from pyvis.network import Network
from llama_index import GPTKnowledgeGraphIndex, KnowledgeGraphIndex
from llama_index.schema import TextNode



class CoursesKnowledgeGraph:
    def __init__(self, service_context):
        self.index = GPTKnowledgeGraphIndex([], service_context=service_context)
        self.generate()

    def load(self):
        pass

    def generate(self):
        with open('data/dataUWA/unitTriples_complete.json', 'r') as file:
            json_data = json.load(file)

        node = TextNode()
        for triplet in json_data:
            triplet_head = triplet['head'].split(" - ")[0]
            triplet_type = triplet['type']
            triplet_tail = triplet['tail'].split(" - ")[0]
            triplets_as_tuple = (triplet_head, triplet_type, triplet_tail)

            self.index.upsert_triplet_and_node(triplets_as_tuple, node)
            print(triplets_as_tuple)
            if triplet_type == 'unit code':
                self.index.upsert_triplet_and_node((triplet_tail, 'unit', triplet_head), node)

            if triplet_type == 'outcome':
                self.index.upsert_triplet_and_node((triplet_tail, 'outcome of', triplet_head), node)

            if triplet_type == 'topic':
                self.index.upsert_triplet_and_node((triplet_tail, 'topic of', triplet_head), node)

    def saveGraphHtml(self):
        g = index.get_networkx_graph(limit=9999999)
        net = Network(notebook=True, cdn_resources="in_line", directed=True)
        net.from_nx(g)
        net.show("example.html")


    def showGraphHtml(self):
        print(self.index.get_networkx_graph(limit=9999999))
        fig = plt.figure(1, figsize=(100, 40), dpi=30)
        nx.draw_networkx(self.index.get_networkx_graph(), font_size=18)

    def getQueryEngine(self):
        return self.index.as_query_engine(include_text=False, response_mode="tree_summarize")



