import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
print(gpus)
tf.config.experimental.set_memory_growth(gpus[0], True)

from transformers import pipeline
import openai
import os
from llama_index.llm_predictor import LLMPredictor
from llama_index import VectorStoreIndex, GPTVectorStoreIndex, KnowledgeGraphIndex, ServiceContext
from llama_index.llms import OpenAI
from llama_index import Document
from llama_index import download_loader
from pathlib import Path

# Uses openai to generate natural language responses over the paul graham esay
os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.environ["OPENAI_API_KEY"]

class TripletsGenerator():
    def __init__(self):
        self.triplet_extractor = pipeline('text2text-generation', model='Babelscape/rebel-large', tokenizer='Babelscape/rebel-large', device='0')

    def extract_triplets(self, input):
        text = self.triplet_extractor.tokenizer.batch_decode(
            [self.triplet_extractor(input, return_tensors=True, return_text=False)[0]["generated_token_ids"]])[0]

        triplets = []
        relation, subject, relation, object_ = '', '', '', ''
        text = text.strip()
        current = 'x'
        for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
            if token == "<triplet>":
                current = 't'
                if relation != '':
                    triplets.append({'head': subject.strip(), 'type': relation.strip(), 'tail': object_.strip()})
                    relation = ''
                subject = ''
            elif token == "<subj>":
                current = 's'
                if relation != '':
                    triplets.append({'head': subject.strip(), 'type': relation.strip(), 'tail': object_.strip()})
                object_ = ''
            elif token == "<obj>":
                current = 'o'
                relation = ''
            else:
                if current == 't':
                    subject += ' ' + token
                elif current == 's':
                    object_ += ' ' + token
                elif current == 'o':
                    relation += ' ' + token
        if subject != '' and relation != '' and object_ != '':
            triplets.append((subject.strip(), relation.strip(), object_.strip()))

        return triplets

    def createDocuments(self) -> [Document]:
        print("Generating Documents...")

        SimpleCSVReader = download_loader("SimpleCSVReader")
        loader = SimpleCSVReader(concat_rows=False)
        documents = loader.load_data(file=Path('data/dataUWA/extractedInformation/soupedUnits2023.csv'))

        return documents

    def graphBuilder2(self):
        llm_predictor = LLMPredictor(llm=OpenAI(model_name="gpt-3.5-turbo"))
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
        documents = self.createDocuments()

        print("Generating GPTVectorStoreIndex from Documents")
        return GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

    def graphBuilder(self):
        service_context = ServiceContext.from_defaults(llm=OpenAI(model_name="gpt-3.5-turbo"), chunk_size=256)
        documents = self.createDocuments()

        print(documents)

        print("Generating KnowledgeGraphIndex from Documents")
        return KnowledgeGraphIndex.from_documents(documents, kg_triplet_extract_fn=self.extract_triplets, service_context=service_context)


generator = TripletsGenerator()
index = generator.graphBuilder()

print("Querying Index...")

queryEngine = index.as_query_engine()

def queryEngineWith(query):
    print("==========================================")
    print(f'Query: {query}')

    response = queryEngine.query(query)

    print(f'Response: {response}')
    print("==========================================\n")

queryEngineWith("Name 3 Courses and their Unit Code, which I can study to improve my Science skills")
queryEngineWith("Name 3 Courses and their Unit Code, which I can study to improve my Math skills")
queryEngineWith("Name 3 Courses and their Unit Code, which I can study to improve my ComputerScience skills")
queryEngineWith("Which course would you recommend me if I wanted to learn about Artificial Intelligence?")
queryEngineWith("Provide me with all Courses (and their Unit Code) which are taught at the Agriculture and Environment school")
queryEngineWith("Which 3 Courses would you recommend me if I wanted to learn about the Human body?")


from pyvis.network import Network

g = index.get_networkx_graph()
net = Network(notebook=True, cdn_resources="in_line", directed=True)
net.from_nx(g)
net.show('/content/example.html')

import IPython
IPython.display.HTML(filename='/content/example.html')