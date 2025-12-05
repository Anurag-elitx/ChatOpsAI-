from langchain.tools import tool
from app.rag.retrieval import retrieve_context

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the company knowledge base for information about Astiva AI, competitive intelligence, or internal docs.
    """
    results = retrieve_context(query)
    if not results:
        return "No relevant information found in the knowledge base."
    return "\n\n".join(results)

@tool
def get_competitive_intelligence(brand_name: str) -> str:
    """
    Simulated API call to fetch competitive intelligence metrics for a brand across LLM platforms.
    """
    # In a real scenario, this would hit an external API or DB
    return f"Brand {brand_name} visibility metrics:\n- ChatGPT: 45%\n- Claude: 60%\n- Gemini: 50%"

def get_all_tools():
    return [search_knowledge_base, get_competitive_intelligence]
