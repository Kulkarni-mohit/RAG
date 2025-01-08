import os
# from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.llms import Gemini
from llama_index.vector_stores import PineconeVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import GeminiEmbedding
from llama_index import ServiceContext, VectorStoreIndex, download_loader, set_global_service_context
import dataIngestion
import streamlit as st

GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
PINECONE_API_KEY = "YOUR_PINECONE_API_KEY"
# load_dotenv()

os.environ["GOOGLE_API_KEY"] = "AIzaSyC0Pm_Ij4yPbBNlmpLU96BGRk-uTTzHK2Y"
os.environ["PINECONE_API_KEY"] = "0b80c750-46ab-410f-8378-3847a7e79607"

DATA_URL = ["https://www.acko.com/life-insurance/", "https://www.acko.com/health-insurance/for-parents/", "https://www.acko.com/car-insurance/","https://www.acko.com/two-wheeler-insurance/"]

llm = Gemini(temperature=0.5)
# Define which embedding model to use "models/embedding-001"
gemini_embed_model = GeminiEmbedding(model_name="models/embedding-001")

# Create a service context using the Gemini LLM and the model
service_context = ServiceContext.from_defaults(llm=llm, embed_model=gemini_embed_model)

# Set the global service context to the created service_context
set_global_service_context(service_context)

index = dataIngestion.vsAlreadyExists()

query_engine = index.as_query_engine()

st.title("💬 Chatbot") 
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    msg = query_engine.query(prompt).response

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)