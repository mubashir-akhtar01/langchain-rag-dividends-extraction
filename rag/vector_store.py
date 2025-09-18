from langchain_chroma import Chroma
from rag.models import Models

# Initialize Models
models = Models()
embeddings = models.embeddings_google
llm = models.model_google

# Constants
PERSIST_DIR = "./chroma_db"

def vector_store_obj():
    return Chroma(
        collection_name="dividends",
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR
    )

def add_documents(documents, document_id):
    """Check if document exists, if not, add it to ChromaDB."""
    print(f"document exists: {document_exists(document_id)}")
    if document_exists(document_id):
        print(f"Document '{document_id}' already exists")
        return vector_store_obj()
    else:
        vector_store = vector_store_obj().add_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=PERSIST_DIR,
        )
        print(f"Added new document: {document_id}")
        return vector_store

def document_exists(document_id):
    """Check if a document with the given document_id exists in ChromaDB"""
    existing_docs = vector_store_obj().get(where={"document_id": document_id},limit=1)["metadatas"]
    if existing_docs:
        return True
    return False