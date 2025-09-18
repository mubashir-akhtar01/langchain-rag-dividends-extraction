from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import helper


# Constants
chunk_size = 1000
chunk_overlap = 200
check_interval = 10

def ingest_file(file_path):
    print(f"start ingesting: {file_path}")
    loader = PyPDFLoader(file_path)
    loaded_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n"," ",""],
    )
    documents = text_splitter.split_documents(loaded_documents)

    document_id = helper.sanitize_filename(file_path)
    # Add metadata (document_id) to each document
    for doc in documents:
        doc.metadata["document_id"] = document_id

    return documents