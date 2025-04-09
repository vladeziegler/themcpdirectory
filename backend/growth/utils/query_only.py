import os
from pathlib import Path
from dotenv import load_dotenv
from llama_index.core import StorageContext
from llama_index.core.indices.loading import load_index_from_storage
from llama_index.core.settings import Settings
from llama_index.embeddings.openai import OpenAIEmbedding

# Load environment variables
load_dotenv()

# Get API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def initialize_search():
    """
    Initialize the search functionality by loading the index and configuring the embedding model
    """
    # Configure the same embedding model as used for creation
    embed_model = OpenAIEmbedding(
        model="text-embedding-3-small",
        api_key=OPENAI_API_KEY,
        dimensions=1536
    )
    
    # Configure settings with the embedding model
    Settings.embed_model = embed_model
    
    # Default index path
    index_path = Path("./storage/mcp_index")
    
    if not index_path.exists():
        raise FileNotFoundError(f"Index not found at {index_path}. Please create the index first using upsert_mcp_data.py")
    
    # Load the index
    storage_context = StorageContext.from_defaults(persist_dir=str(index_path))
    index = load_index_from_storage(storage_context)
    return index

def search_mcp(query: str, top_k: int = 5):
    """
    Search the MCP index with a natural language query
    
    Args:
        query (str): The search query
        top_k (int): Number of results to return (default: 5)
        
    Returns:
        list: List of search results with their scores and metadata
    """
    try:
        index = initialize_search()
        
        # Create retriever with specified number of results
        retriever = index.as_retriever(similarity_top_k=top_k * 2)
        
        # Get results
        results = retriever.retrieve(query)
        
        # Group results by URL to avoid duplicates
        grouped_results = {}
        for result in results:
            url = result.metadata.get('url')
            if url not in grouped_results or result.score > grouped_results[url].score:
                grouped_results[url] = result
        
        # Sort and limit to top_k results
        final_results = sorted(
            grouped_results.values(),
            key=lambda x: x.score,
            reverse=True
        )[:top_k]
        
        return final_results
        
    except Exception as e:
        print(f"Error during search: {e}")
        return []

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Search MCP Descriptions')
    parser.add_argument('query', type=str, help='The search query')
    parser.add_argument('--top-k', type=int, default=5, help='Number of results to return')
    
    args = parser.parse_args()
    
    results = search_mcp(args.query, args.top_k)
    
    print(f"\nFound {len(results)} results for query: {args.query}\n")
    for i, result in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"Score: {result.score:.4f}")
        print(f"URL: {result.metadata.get('url', 'N/A')}")
        print(f"Text: {result.text[:200]}...")
        print()

if __name__ == "__main__":
    main()