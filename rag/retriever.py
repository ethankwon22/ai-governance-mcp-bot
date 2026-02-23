from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_DB_PATH = "rag/vector_store"

def retrieve_context(query: str, k: int = 3):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    docs = vectorstore.similarity_search(query, k=k)
    return [d.page_content for d in docs]

if __name__ == "__main__":
    results = retrieve_context("How do I reset my password?")
    for r in results:
        print("----")
        print(r)