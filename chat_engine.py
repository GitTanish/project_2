import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from document_engine import query_documents
load_dotenv() 
groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key is not None:
    os.environ["GROQ_API_KEY"] = groq_api_key
else:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# llm initialization
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.5)

# per user memory session

session_memory_map = {}

# session id is a unique identifier for each user session, to retain the conversational context
def get_response(session_id: str, user_query: str) -> str:
    # Step 1: Retrieve context from documents
    doc_context = query_documents(user_query)

    # Step 2: Add doc_context into the user query (RAG style)
    enriched_query = f"User asked: {user_query}\n\nRelevant context:\n{doc_context}\n\nAnswer in a helpful way using this context."

    # Step 3: Use memory + conversation chain
    if session_id not in session_memory_map:
        memory = ConversationBufferMemory()
        session_memory_map[session_id] = ConversationChain(llm=llm, memory=memory, verbose=True)

    conversation = session_memory_map[session_id]
    return conversation.predict(input=enriched_query)