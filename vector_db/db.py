from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

pdf_path = BASE_DIR / "data" / "RNTU_Bhopal_RAG_Knowledge_Base.pdf"

chroma_path = BASE_DIR  / "Chorma_db"

loader = PyPDFLoader(str(pdf_path))

docs = loader.load()

splite= RecursiveCharacterTextSplitter(
    chunk_size= 100,
    chunk_overlap = 5
)

final_splite = splite.split_documents(docs)

embb_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2"
)


vector_store = Chroma(
    collection_name="rntu_knowledge",
    embedding_function=embb_model,
    persist_directory=str(chroma_path)
)


BATCH_SIZE = 20

total = len(final_splite)

for start in range(0, total, BATCH_SIZE):
    end = min(start + BATCH_SIZE, total)

    batch = final_splite[start:end]

    print(f"Embedding chunks {start + 1} → {end} / {total}")

    vector_store.add_documents(batch)

    print(f" Stored {len(batch)} chunks")

    # Give Gemini time before the next batch
    if end < total:
        print(" Waiting 10 seconds...")
        time.sleep(10)

print("\n All chunks stored successfully!")
