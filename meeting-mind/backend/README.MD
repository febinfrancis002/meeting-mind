# MeetingMind Backend

MeetingMind is an AI-powered backend designed to manage transcript uploads, indexing, and retrieval-augmented generation (RAG) for intelligent Q&A over meeting transcripts. Built with FastAPI, MeetingMind leverages TinyDB for lightweight document storage, Chroma as a vector store, and LangChain along with OpenAI to process and respond to natural language queries.

## Features

- **Transcript Upload:**  
  Upload transcript files which are processed by splitting the text into manageable chunks and embedding them into a vector store.

- **Chat Interface (RAG):**  
  Ask questions over the stored transcripts using a retrieval-augmented generation chain that utilizes the Chroma vector store and OpenAI.

## Requirements

- **Python Version:**  
  Python 3.8 or higher (Python 3.9+ is recommended).



- **OpenAI API Key:**  
  A valid OpenAI API key is required and must be set as an environment variable (`OPENAI_API_KEY`).

## Local Setup Instructions 

Follow these steps to set up and run the MeetingMind backend locally.


```bash
git clone <repository-url>
cd MeetingMind-backend
```

### 2. Install

#### On Windows

```bash
python -m venv env
env\Scripts\activate
```

#### On Mac

```bash
python3 -m venv env
source env/bin/activate
```

```bash
pip install -r requirements.txt
```

uvicorn meeting_mind:app --reload
