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


vector_store.add_documents(final_splite)
