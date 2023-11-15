from llama_index import ServiceContext
from llama_index.llms import OpenAI
from KG_Units import CoursesKnowledgeGraph
import os


os.environ["OPENAI_API_KEY"] = "your_key"
llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=llm)

courseGraph = CoursesKnowledgeGraph(service_context)
qe = courseGraph.getQueryEngine()

from pyvis.network import Network

g = courseGraph.index.get_networkx_graph(limit=100)
net = Network(notebook=True, cdn_resources="in_line", directed=True)
net.from_nx(g)
net.show('data/example.html')

def printQueryandAnswer(qe, query):
    print("=========================================")
    print(f"Query: {query}")
    response = qe.query(query)
    print(f"Response: {response}")
    print("=========================================\n")

printQueryandAnswer(qe, "Tell me everything about ACCT5501?")  # contemporary issues in accounting, UWA Business School
printQueryandAnswer(qe, "Tell me about ACCT5602")  # Accounting, UWA Business School
printQueryandAnswer(qe, "Tell me about CITS2005")  # Object Oriented Programming, Physics, Mathematics and Computing

printQueryandAnswer(qe, "I am looking for a Course on Object Oriented Programming.")  # CITS2005
printQueryandAnswer(qe, "What unit teaches understand use multithreading for designing Java programs with concurrency?")  # CITS2005
printQueryandAnswer(qe, "What unit teaches about Java programs?")  # CITS2005
printQueryandAnswer(qe, "What unit teaches oo-div-design?")  # CITS2005

printQueryandAnswer(qe, "What unit teaches show skills in workplace post-degree?")  # PLNG5410

printQueryandAnswer(qe, "What unit code has pharmacology as a topic?")  # PHCY5612

