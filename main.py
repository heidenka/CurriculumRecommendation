import pandas as pd
# from SoupExtractor import *
from LLMParser import *
from llama_index import (SimpleDirectoryReader, LLMPredictor, ServiceContext, KnowledgeGraphIndex, GPTKnowledgeGraphIndex)
import json
from llama_index.graph_stores import SimpleGraphStore

from llama_index.llms import OpenAI
from IPython.display import Markdown, display

from llama_index.node_parser import SimpleNodeParser
import os

os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=llm)

# Parse html units with bs4 & save into csv

# soupedUnits = SoupExtractor("data/dataUWA/Outlines/2023")
# df1 = soupedUnits.extract()
# df1.transpose().to_json(f"data/dataUWA/extractedInformation/soupedUnits2023.json")
#df1.to_csv(f"data/dataUWA/extractedInformation/soupedUnits2023.csv")


# Parse csv units with chatGPT
#LLMUnits = LLMParser("data/dataUWA/extractedInformation/soupedUnits2023.csv")
#parsedUnits = LLMUnits.extract()ß
#parsedUnits.to_csv("data/dataUWA/extractedInformation/parsedUnits2023.csv", index=False, sep=";")



from KgraphFromTriples import CoursesKnowledgeGraph

index = CoursesKnowledgeGraph(service_context)
qe = index.getQueryEngine()

def prettyQuery(qe, query):
    print("=========================================")
    print(f"Query: {query}")
    response = qe.query(query)
    print(f"Response: {response}")
    print("=========================================\n")

prettyQuery(qe, "Tell me everything about ACCT5501?")  # contemporary issues in accounting, UWA Business School
prettyQuery(qe, "Tell me about ACCT5602")  # Accounting, UWA Business School
prettyQuery(qe, "Tell me about CITS2005")  # Object Oriented Programming, Physics, Mathematics and Computing

prettyQuery(qe, "I am looking for a Course on Object Oriented Programming.")  # CITS2005
prettyQuery(qe, "What unit teaches understand use multithreading for designing Java programs with concurrency?")  # CITS2005
prettyQuery(qe, "What unit teaches about Java programs?")  # CITS2005
prettyQuery(qe, "What unit teaches oo-div-design?")  # CITS2005

prettyQuery(qe, "What unit teaches show skills in workplace post-degree?")  # PLNG5410

prettyQuery(qe, "What unit code has pharmacology as a topic?")  # PHCY5612

