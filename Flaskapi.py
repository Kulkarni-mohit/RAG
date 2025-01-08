import os
import dataIngestion
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings
import time
from typing import List
from io import BytesIO
from fastapi import FastAPI, Query, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


start = time.time()

Settings.llm = Gemini(model = "models/gemini-1.5-flash",temperature=0.9)
Settings.embed_model = GeminiEmbedding(model_name="models/embedding-001")

index = dataIngestion.vsAlreadyExists()
query_engine = index.as_query_engine()


class Item(BaseModel):
    items: List[str]
app = FastAPI()

# Allowing CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the endpoint for chatbot response
@app.get('/')
def d():
    print("Root endpoint hit")
    return {"message": "Server is running"}

@app.get('/chatbot')
async def chatbot_response(prompt: str = Query(...), language: str = Query('english')):
    start = time.time()

    if language:
        prompt = "Give the answer in detail and in simple words and return 'No context' if not found." + prompt + f"Give answer in {language}"
    else:  # default to English
        prompt = "Give the answer in detail and in simple words and return 'No context' if not found. " + prompt

        # First Database
    streaming_response = query_engine.query(prompt)
    msg = streaming_response.response
    a = streaming_response.metadata
    print(msg)
        # Check if the result is found in the first database
    if "No context" not in msg:
        end = time.time()
        return {"response": msg, "source": a, "time_taken": end - start}

# # Define the endpoint for updating the vector database
@app.post('/update_vector_database')
async def update_vector_database(item: Item):
    print(item.items)
    dataIngestion.listofURLs(item)
    return {"message": "Vector database updated successfully"}

@app.post('/update_vector_database_with_pdf')
async def update_vector_database_with_pdf(file: UploadFile = File(...)):
    file_data = BytesIO(await file.read())
    index = dataIngestion.pdfdataLoader(file_data)
    return {"message": "Vector database updated successfully"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)