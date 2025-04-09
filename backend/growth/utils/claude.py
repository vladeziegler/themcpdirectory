import requests
import json
import os
import random
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Generate a unique index name following the pattern in existing indices
def generate_index_name():
    adjectives = ["happy", "quick", "clever", "brave", "mighty", "gentle", "calm", "bright", "elegant", "fierce"]
    animals = ["panda", "tiger", "eagle", "wolf", "dolphin", "fox", "lion", "hawk", "bear", "whale"]
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    adjective = random.choice(adjectives)
    animal = random.choice(animals)
    
    return f"{adjective}-{animal}-{today}"

def list_llamacloud_indices():
    """
    List all existing indices in LlamaCloud
    """
    url = "https://api.cloud.llamaindex.ai/api/v1/pipelines"
    
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {LLAMA_CLOUD_API_KEY}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error listing indices: {e}")
        return []

def create_llamacloud_index(index_name=None, verbose=False):
    """
    Create a new index in LlamaCloud
    
    Args:
        index_name (str, optional): Name for the index. If None, a name will be generated.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
    
    Returns:
        dict: The created index data or None if creation failed
    """
    # Ensure we have the necessary API keys
    if not LLAMA_CLOUD_API_KEY:
        print("Error: LLAMA_CLOUD_API_KEY is not set in the environment variables")
        return None
    
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY is not set in the environment variables")
        return None
        
    # Check existing indices
    existing_indices = list_llamacloud_indices()
    
    if verbose:
        print(f"Found {len(existing_indices)} existing indices:")
        for idx, index in enumerate(existing_indices):
            print(f"{idx+1}. {index.get('name')} (ID: {index.get('id')})")
    
    # Generate a name if not provided
    if not index_name:
        index_name = generate_index_name()
    
    # Check if the name already exists
    if any(index.get("name") == index_name for index in existing_indices):
        print(f"Index with name '{index_name}' already exists")
        return None
    
    print(f"\nCreating index with name: {index_name}")
    
    url = "https://api.cloud.llamaindex.ai/api/v1/pipelines"
    
    # Create payload based on API requirements
    payload = {
        "name": index_name,
        "description": "Index for MCP descriptions",
        "pipeline_type": "MANAGED",
        "embedding_config": {
            "type": "OPENAI_EMBEDDING",
            "component": {
                "model_name": "text-embedding-3-small",
                "embed_batch_size": 10,
                "api_key": OPENAI_API_KEY,
                "api_base": "https://api.openai.com/v1",
                "max_retries": 10,
                "timeout": 60.0,
                "reuse_client": True
            }
        },
        "transform_config": {
            "mode": "auto",
            "chunk_size": 1024,
            "chunk_overlap": 200
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {LLAMA_CLOUD_API_KEY}'
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"Index created successfully!")
        print(f"Index ID: {result.get('id')}")
        return result
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 409:
            print(f"Server says index '{index_name}' already exists.")
            print(f"Response: {response.text}")
        else:
            print(f"Error creating index: {e}")
            print(f"Response: {response.text}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_index_by_name(name):
    """
    Find an index by name
    
    Args:
        name (str): Name of the index to find
        
    Returns:
        dict: The index data or None if not found
    """
    indices = list_llamacloud_indices()
    for index in indices:
        if index.get("name") == name:
            return index
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LlamaCloud Index Management')
    parser.add_argument('--list', action='store_true', help='List all indices')
    parser.add_argument('--create', action='store_true', help='Create a new index')
    parser.add_argument('--name', type=str, help='Name for the new index')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.list:
        indices = list_llamacloud_indices()
        print(f"Found {len(indices)} indices:")
        for i, index in enumerate(indices):
            print(f"{i+1}. {index.get('name')} (ID: {index.get('id')})")
    elif args.create:
        create_llamacloud_index(args.name, args.verbose)
    else:
        # Default behavior (backwards compatibility)
        create_llamacloud_index(verbose=True)