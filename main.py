from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent



embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2"
)



llm = ChatOpenRouter(
    model="inclusionai/ling-3.0-flash-vl:free"
)


vector = Chroma(
    persist_directory=str(BASE_DIR / "Chorma_db"),
    collection_name="rntu_knowledge",
    embedding_function=embedding_model
)




retriever = vector.as_retriever(
    search_type="mmr",
    search_kwargs={
        "fetch_k": 10,
        "k": 4,
        "lambda_mult": 0.5
    }
)




prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an AI assistant for Rabindranath Tagore University (RNTU), Bhopal.

Your task is to answer the user's question ONLY using the information
provided in the retrieved context.

Rules:

1. Use only the retrieved context to answer the question.
2. Do NOT use your own knowledge.
3. Do NOT make assumptions or invent information.
4. If the answer is present in the context, answer clearly and accurately.
5. If the answer is not present in the context, reply exactly:

Sorry, I couldn't find any relevant information in the provided RNTU documents. Please try asking another question.

6. Do not invent facts, names, dates, fees, departments, facilities,
   policies, or other university information.
7. Keep the answer concise and informative.

Retrieved Context:
{context}
"""
    ),

    (
        "human",
        """
User Question:
{question}
"""
    )
])


def get_answer(question: str) -> str:
    """
    Runs retrieval + the LLM chain for a single question and
    returns the answer text. This is the function app.py calls.
    """
    documents = retriever.invoke(question)
 
    context = "\n\n".join(doc.page_content for doc in documents)
 
    final_prompt = prompt.invoke({
        "context": context,
        "question": question,
    })
 
    response = llm.invoke(final_prompt)
 
    return response.content
 
 
if __name__ == "__main__":
    # Lets you still run this file directly from the CLI, like main.py did.
    user = input("\nPlease ask anything about RNTU: ")
    print("\nANSWER\n")
    print(get_answer(user))
 