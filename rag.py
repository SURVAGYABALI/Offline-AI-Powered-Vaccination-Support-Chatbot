from langchain import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.embeddings import SentenceTransformerEmbeddings
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
from query import query_ollama_streaming
import os
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



embeddings = SentenceTransformerEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")

url = "http://localhost:6333"

client = QdrantClient(
    url=url, prefer_grpc=False
)

print(client)
print("##############")

db = Qdrant(client=client, embeddings=embeddings, collection_name="vector_db")

print(db)
print("######")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_response")
async def get_response(query: str = Form(...)):
    docs = db.similarity_search_with_score(query=query, k=2)
    context = ''
    for i in docs:
        doc, score = i
        # print({"score": score, "content": doc.page_content, "metadata": doc.metadata})
        context+= doc.page_content
    question = query
    prompt_template = f"""Use the following pieces of information to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

            Context: {context}
            Question: {question}
        """
    response = query_ollama_streaming(query)
    print(response)
    # answer = response['result']
    # source_document = response['source_documents'][0].page_content
    # doc = response['source_documents'][0].metadata['source']
    response_data = jsonable_encoder(json.dumps({"answer": response, "source_document": context}))
    
    res = Response(response_data)
    return res