from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
# pip install llama-index-core
# pip install llama-index-llms-openai
# pip install llama-index-embeddings-openai
# pip install llama-index-indices-managed-llama-cloud
# pip install pandas
# pip install python-dotenv
# pip install requests

import os
import pandas as pd
import numpy as np
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def create_pipeline(api_key):
    url = "https://api.cloud.llamaindex.ai/api/v1/pipelines"
    
    payload = {
        "embedding_config": {
            "type": "OPENAI_EMBEDDING",
            "component": {
                "model_name": "text-embedding-ada-002",
                "embed_batch_size": 10,
                "num_workers": 0,
                "additional_kwargs": {},
                "max_retries": 10,
                "timeout": 60,
                "default_headers": {},
                "reuse_client": True
            }
        },
        "transform_config": {
            "mode": "auto",
            "chunk_size": 1024,
            "chunk_overlap": 200
        },
        "configured_transformations": [
            {
                "configurable_transformation_type": "CHARACTER_SPLITTER",
                "component": {}
            }
        ],
        "name": "modo_pipeline",
        "pipeline_type": "MANAGED"
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def upsert_documents(api_key, documents):
    url = "https://api.cloud.llamaindex.ai/api/v1/pipelines"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # Convert documents to the expected format
    docs_payload = []
    for doc in documents:
        docs_payload.append({
            "text": doc.text,
            "metadata": doc.metadata
        })
    
    payload = {
        "documents": docs_payload
    }
    
    response = requests.put(url, headers=headers, json=payload)
    return response.json()

def create_and_upsert_index():
    # Configure LlamaIndex settings
    Settings.llm = OpenAI(model="gpt-3.5-turbo")
    Settings.embed_model = OpenAIEmbedding()
    
    # Initialize the index
    api_key = "llx-Mhi1SgWcY5jO9CRPnqfbEjVPur1VaqtP71wToEAzBQeAT2gm"
    index = LlamaCloudIndex(
        name="modo",
        project_name="Default",
        organization_id="8e327feb-280a-4a46-abcb-67662f3a4522",
        api_key=api_key,
    )
    
    # Create pipeline first
    pipeline = create_pipeline(api_key)
    print("Pipeline created:", pipeline)
    
    # Read the CSV file
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'source', 'MCP_description.csv')
    df = pd.read_csv(csv_path)
    
    # Create documents for each row
    documents = []
    for idx, row in df.iterrows():
        # Skip rows where Description is NaN
        if pd.isna(row['Description']) or pd.isna(row['URL']):
            print(f"Skipping row {idx} due to missing data")
            continue
            
        # Create a document with the description as the text content
        doc = Document(
            text=str(row['Description']).strip(),
            metadata={
                'url': str(row['URL']).strip(),
                'id': f"doc_{idx}"
            }
        )
        documents.append(doc)
    
    print(f"Upserting {len(documents)} documents...")
    
    # Use batch processing for better performance
    batch_size = 20
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        response = upsert_documents(api_key, batch)
        print(f"Upserted batch {i//batch_size + 1} of {(len(documents)-1)//batch_size + 1}")
        print("Response:", response)
    
    print("Upsert complete!")
    return index

def search_index(query_text, top_k=5):
    # Configure LlamaIndex settings
    Settings.llm = OpenAI(model="gpt-3.5-turbo")
    Settings.embed_model = OpenAIEmbedding()
    
    # Initialize the index
    index = LlamaCloudIndex(
        name="modo",
        project_name="Default",
        organization_id="8e327feb-280a-4a46-abcb-67662f3a4522",
        api_key="llx-Mhi1SgWcY5jO9CRPnqfbEjVPur1VaqtP71wToEAzBQeAT2gm",
    )
    
    # Create a retriever with similarity search
    retriever = index.as_retriever(similarity_top_k=top_k)
    
    # Get relevant documents
    retrieved_nodes = retriever.retrieve(query_text)
    
    # Create a query engine with the retrieved context
    query_engine = index.as_query_engine(
        similarity_top_k=top_k,
        response_mode="compact"
    )
    
    # Perform the search
    response = query_engine.query(query_text)
    
    print("\nRetrieved Sources:")
    for node in retrieved_nodes:
        print(f"- {node.metadata['url']}")
        
    return response

if __name__ == "__main__":
    # First check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set your OPENAI_API_KEY environment variable")
        exit(1)
        
    # Create and populate the index
    index = create_and_upsert_index()
    
    # Example search
    query = "What MCP servers are available for database interactions?"
    print("\nSearching for:", query)
    response = search_index(query)
    print("\nResponse:", response)