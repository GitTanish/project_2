## FastAPI server
"""
Initializes FastAPI server for chat app.
- Loads environment variables.
- Imports modules for chat, crisis detection, logging, and docs.
- Sets up CORS middleware.
"""
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from models import ChatRequest
from chat_engine import get_response
from crisis import contains_crisis_keywords, SAFETY_MESSAGE
from logger import log_chat
from document_engine import query_documents
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware, # frontend can access backend
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mental Health Support Chat API. Visit /docs for API documentation."
}

@app.post("/chat")
def chat_with_memory(request: ChatRequest):
    session_id = request.session_id
    user_query = request.query

    # Check for crisis keywords
    if contains_crisis_keywords(user_query):
        log_chat(session_id, user_query, SAFETY_MESSAGE, is_crisis=True)
        return {"response": SAFETY_MESSAGE}
    
    # For non-crisis queries, get response from chat engine
    response = get_response(session_id, user_query)
    log_chat(session_id, user_query, response, is_crisis=False)
    return {"response": response }

@app.post('/documents')
def