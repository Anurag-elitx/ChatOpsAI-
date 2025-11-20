from app.rag.indexing import get_vectorstore

def retrieve_context(query: str, top_k: int = 3):
    """
    Retrieve top K matching documents for a given query from ChromaDB.
    """
    vectorstore = get_vectorstore()
    
    # Check if vectorstore has data
    if getattr(vectorstore, "_collection", None) is None or vectorstore._collection.count() == 0:
         return []
         
    docs = vectorstore.similarity_search(query, k=top_k)
    return [doc.page_content for doc in docs]
