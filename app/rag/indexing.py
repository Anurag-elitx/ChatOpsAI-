import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

def get_vectorstore():
    embeddings = OpenAIEmbeddings()
    return Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings)

def index_document(file_path: str):
    """
    Load a document, chunk it using LangChain, and insert into ChromaDB.
    """
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found: {file_path}"}
        
    loader = TextLoader(file_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)
    vectorstore.persist()
    
    return {"status": "success", "chunks_indexed": len(chunks)}
