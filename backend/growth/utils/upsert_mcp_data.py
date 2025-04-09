import csv
import os
import json
import argparse
import sys
from dotenv import load_dotenv
from pathlib import Path
from tqdm import tqdm

# Import from llama_index components
from llama_index.core import Document
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core.settings import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.indices.loading import load_index_from_storage

# Import functions from claude.py
sys.path.append(str(Path(__file__).parent))
from claude import list_llamacloud_indices, create_llamacloud_index, get_index_by_name

# Load environment variables
load_dotenv()

# Get API keys from environment variables
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def list_indices():
    """
    List all available indices in LlamaCloud
    """
    indices = list_llamacloud_indices()
    if indices:
        print(f"Found {len(indices)} indices:")
        for i, index in enumerate(indices):
            print(f"{i+1}. {index.get('name')} (ID: {index.get('id')})")
            print(f"   Status: {index.get('status')}")
            print(f"   Type: {index.get('pipeline_type')}")
    else:
        print("No indices found")
    
    return indices

def process_csv_to_documents(csv_file):
    """
    Process CSV file and convert to LlamaIndex Document objects with improved text processing
    """
    documents = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                text = row.get('Description', '')
                url = row.get('URL', '')
                
                if not text.strip():
                    continue
                
                # Create a structured document that preserves the full context
                # and makes it easier for the embedding model to understand
                doc_text = f"""
                Repository: {url}
                
                Description:
                {text}
                
                This MCP server provides the following capabilities:
                {text}
                """
                
                # Create smaller chunks for better semantic matching
                chunks = chunk_text(doc_text, chunk_size=512, overlap=50)
                
                for i, chunk in enumerate(chunks):
                    doc = Document(
                        text=chunk,
                        metadata={
                            "url": url,
                            "chunk_id": i,
                            "total_chunks": len(chunks),
                            "source": "MCP_description.csv"
                        }
                    )
                    documents.append(doc)
                
        print(f"Processed {len(documents)} document chunks from {csv_file}")
        return documents
        
    except FileNotFoundError:
        print(f"Error: File not found: {csv_file}")
        return []
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return []

def chunk_text(text, chunk_size=512, overlap=50):
    """
    Split text into overlapping chunks to improve semantic search
    """
    words = text.split()
    chunks = []
    start = 0
    
    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start = start + (chunk_size - overlap)
    
    return chunks

def create_and_populate_index(documents, index_name=None):
    """
    Create a new local index and populate it with documents
    
    Args:
        documents (list): List of Document objects
        index_name (str): Optional name for the index
        
    Returns:
        VectorStoreIndex: The created index
    """
    # Configure embedding model - IMPORTANT: Use the same model consistently
    embed_model = OpenAIEmbedding(
        model="text-embedding-3-small",  # or "text-embedding-3-large", but be consistent
        api_key=OPENAI_API_KEY,
        dimensions=1536  # explicitly set dimensions for text-embedding-3-small
    )
    
    # Configure settings with the embedding model
    Settings.embed_model = embed_model
    
    # Create a new index with the documents
    index = VectorStoreIndex.from_documents(documents)
    
    print(f"Created new index with {len(documents)} documents")
    
    # Save the index to disk
    index_path = Path("./storage") / (index_name or "mcp_index")
    index_path.mkdir(parents=True, exist_ok=True)
    
    index.storage_context.persist(persist_dir=str(index_path))
    print(f"Index saved to {index_path}")
    
    return index

def load_existing_index(index_path):
    """
    Load an existing index from disk
    """
    # Configure the same embedding model as used for creation
    embed_model = OpenAIEmbedding(
        model="text-embedding-3-small",  # must match the model used for creation
        api_key=OPENAI_API_KEY,
        dimensions=1536
    )
    
    # Configure settings with the embedding model
    Settings.embed_model = embed_model
    
    storage_context = StorageContext.from_defaults(persist_dir=index_path)
    index = load_index_from_storage(storage_context)
    print(f"Loaded existing index from {index_path}")
    return index

def search_index(index, query, top_k=5):
    """
    Enhanced search with better relevance scoring and result grouping
    """
    retriever = index.as_retriever(
        similarity_top_k=top_k * 2  # Retrieve more results initially for better filtering
    )
    
    results = retriever.retrieve(query)
    
    # Group results by URL to avoid duplicate sources
    grouped_results = {}
    for result in results:
        url = result.metadata.get('url')
        if url not in grouped_results or result.score > grouped_results[url].score:
            grouped_results[url] = result
    
    # Sort grouped results by score and take top_k
    final_results = sorted(
        grouped_results.values(), 
        key=lambda x: x.score, 
        reverse=True
    )[:top_k]
    
    return final_results

def main():
    parser = argparse.ArgumentParser(description='MCP Data Management')
    parser.add_argument('--index-path', type=str, default='./storage/mcp_index', help='Path to the index directory')
    parser.add_argument('--csv-file', type=str, default='growth/source/MCP_description.csv', help='Path to CSV file')
    parser.add_argument('--search', type=str, help='Perform semantic search with given query')
    parser.add_argument('--top-k', type=int, default=5, help='Number of search results to return')
    parser.add_argument('--list-cloud', action='store_true', help='List all available indices in LlamaCloud')
    parser.add_argument('--create', action='store_true', help='Create a new index')
    parser.add_argument('--name', type=str, help='Name for the new index')
    
    args = parser.parse_args()
    
    if args.list_cloud:
        list_indices()
    elif args.create:
        documents = process_csv_to_documents(args.csv_file)
        if documents:
            create_and_populate_index(documents, args.name)
    elif args.search:
        # Load the index if it exists
        index_path = Path(args.index_path)
        if not index_path.exists():
            print(f"Error: Index directory {index_path} does not exist")
            print("Use --create to create a new index first")
            return
            
        index = load_existing_index(str(index_path))
        results = search_index(index, args.search, args.top_k)
        
        print(f"\nFound {len(results)} results for query: {args.search}\n")
        for i, result in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"Score: {result.score}")
            print(f"URL: {result.metadata.get('url', 'N/A')}")
            print(f"Text: {result.text[:200]}...")
            print()
    else:
        print("No action specified. Please use one of the following:")
        print("  --list-cloud: List all available indices in LlamaCloud")
        print("  --create: Create a new index")
        print("  --search: Search an existing index")
        parser.print_help()

if __name__ == "__main__":
    main() 