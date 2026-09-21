# RNTU Insight AI

RNTU Insight AI is a retrieval-augmented generation (RAG) chatbot for answering questions about Rabindranath Tagore University (RNTU), Bhopal. It retrieves relevant passages from the university knowledge base and asks an LLM to answer using only that retrieved context.

## Features

- Streamlit chat interface with conversation history
- Semantic retrieval from a locally persisted Chroma vector store
- Maximum marginal relevance (MMR) retrieval for diverse results
- Google Gemini embeddings for document and query vectors
- OpenRouter-hosted chat model for answer generation
- Grounded-response prompt that declines to invent information
- PDF ingestion script with chunking and batched embedding

## Tech Stack

- Python 3.10+
- Streamlit
- LangChain
- ChromaDB
- Google Generative AI embeddings
- OpenRouter
- PyPDF

## Project Architecture

```text
Rag_understandin/
├── app.py                         # Streamlit user interface
├── main.py                        # Retrieval and answer-generation pipeline
├── vector_db/db.py                # PDF ingestion and Chroma indexing script
├── data/
│   └── RNTU_Bhopal_RAG_Knowledge_Base.pdf
├── .env.example                   # Required environment variable names
├── requirements.txt
└── Chorma_db/                     # Generated locally; ignored by Git
```

The PDF is the versioned source knowledge base. `vector_db/db.py` creates the local Chroma store from it, while `main.py` loads that store at application startup.

## RAG Workflow

1. `vector_db/db.py` loads the source PDF with `PyPDFLoader`.
2. The document is split into small overlapping chunks.
3. Google Generative AI creates an embedding for each chunk.
4. Chroma persists the embeddings and document text in `Chorma_db/`.
5. A user question is embedded and searched with MMR (`k=4`, `fetch_k=10`).
6. The retrieved context and question are sent to the OpenRouter chat model.
7. The model returns a concise answer grounded in the retrieved RNTU documents.

## Installation

Clone the repository and create a virtual environment:

```powershell
git clone https://github.com/akashgoswami139/RNTU-Insight-AI.git
cd RNTU-Insight-AI
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS or Linux, activate the environment with `source .venv/bin/activate`.

## Environment Variables

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Set these values in `.env`:

```dotenv
GOOGLE_API_KEY=your_google_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

Never commit `.env` or real API keys. The application loads these values with `python-dotenv`.

## Build the Vector Store

Run this once after installation, or whenever the source PDF changes:

```powershell
python vector_db/db.py
```

This creates the local `Chorma_db/` directory. It is generated data and is intentionally excluded from Git.

## Run the Project

Start the Streamlit application from the repository root:

```powershell
streamlit run app.py
```

Then open the local URL shown by Streamlit, typically `http://localhost:8501`.

For a command-line question, run:

```powershell
python main.py
```

## Example Usage

After the vector store has been built, ask questions such as:

```text
What programs and facilities are described in the RNTU documents?
```

The assistant answers from the indexed PDF. When the documents do not contain the requested information, it returns the configured not-found response rather than guessing.

## Future Improvements

- Add source citations and page references to answers
- Add an ingestion command with duplicate-document protection
- Add automated tests for retrieval, prompt behavior, and configuration
- Add document upload and index-refresh support
- Add observability for retrieval quality and model responses
- Pin dependency versions for repeatable deployments

## License

No license has been specified yet.