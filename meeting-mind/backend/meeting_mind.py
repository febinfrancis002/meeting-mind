import os
import uuid
import datetime
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tinydb import TinyDB, Query
from dotenv import load_dotenv


from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()
app = FastAPI(title="AI Agentic Transcript Manager")

# Enable CORS for communication with your frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging to ensure logs show in the console.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Initialize TinyDB for storing transcript metadata.
db = TinyDB("transcripts_db.json")

# Ensure the OpenAI API key is set.
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set your OPENAI_API_KEY environment variable in the .env file.")

# Initialize embeddings and Chroma vector store.
embedding_model = OpenAIEmbeddings()  # Updated import
db_path = "./chroma_db"
vector_store = Chroma(
    persist_directory=db_path,
    embedding_function=embedding_model,
    collection_name="transcripts"
)


MODEL = "gpt-4o-mini"  
llm = ChatOpenAI(temperature=0.7, model_name=MODEL)
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
retriever = vector_store.as_retriever()
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)


def store_transcript_to_vector_db(transcript_text, meeting_date, filename):
    logger.info("Storing to vector db started")
    global vector_store, conversation_chain
    # Split transcript into chunks.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(transcript_text)
    logger.info("Split into chunks done")
    # Create metadata for each chunk.
    metadata = [{"meeting_date": meeting_date, "filename": filename} for _ in chunks]

    vector_store.add_texts(chunks, metadatas=metadata)
    logger.info("Inserted all chunks into vector store")
    print("Inserted all chunks into vector store")
    
    # Update the retriever and conversation chain to include the newly added data.
    retriever = vector_store.as_retriever()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
    )
    print("New transcript added successfully.")
    
   

    

@app.post("/upload")
async def upload_transcript(file: UploadFile = File(...)):
    """
    Uploads a transcript file, stores it in TinyDB, splits the text into manageable chunks,
    and indexes each chunk in the Chroma vector store.
    """
    logger.info("Upload started")
    try:
        content = await file.read()
        content = content.decode("utf-8")
        transcript_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "id": transcript_id,
            "filename": file.filename,
            "content": content,
            "timestamp": timestamp
        }
        db.insert(record)
        store_transcript_to_vector_db(content, timestamp, file.filename)
        return {
            "status": "success",
            "message": "Transcript uploaded and processed by AI agent.",
            "id": transcript_id
        }
    
    except Exception as e:
        logger.error("Error in upload_transcript: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/chat")
def chat_with_transcripts(payload: dict):
    """
    Receives a user question and returns an answer generated using the conversational retrieval chain.
    The conversation chain uses memory to keep track of chat history.
    """
    question = payload.get("question", "")
    if not question:
        raise HTTPException(status_code=400, detail="No question provided.")
    try:
        result = conversation_chain.invoke({"question": question})
        answer = result["answer"]
        return {"answer": answer}
    except Exception as e:
        logger.error("Error in chat: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("meeting_mind:app", host="0.0.0.0", port=8000, reload=True)
