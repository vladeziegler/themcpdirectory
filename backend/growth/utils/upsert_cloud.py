import os
import pandas as pd
from llama_cloud.client import LlamaCloud
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_cloud.types import CloudDocumentCreate, CloudPineconeVectorStore, CloudS3DataSource

# Load environment variables
LLAMACLOUD_API_KEY = os.getenv('LLAMA_CLOUD_API_KEY')

# Initialize LlamaCloud client
client = LlamaCloud(token=LLAMACLOUD_API_KEY)

# Define collection name and embedding model
COLLECTION_NAME = 'elegant-hawk-2025-04-08'
EMBEDDING_MODEL = 'text-embedding-3-small'

# Configure embedding model
embed_model = OpenAIEmbedding(
    model=EMBEDDING_MODEL,
    api_key=os.getenv('OPENAI_API_KEY'),
    dimensions=1536
)

# Load CSV data
csv_path = 'growth/source/MCP_description.csv'

# Process CSV data into document chunks
from upsert_mcp_data import process_csv_to_documents

documents = process_csv_to_documents(csv_path)

# Setup embedding and transformation config
embedding_config = {
    'type': 'OPENAI_EMBEDDING',
    'component': {
        'api_key': os.getenv('OPENAI_API_KEY'),
        'model_name': 'text-embedding-ada-002'
    }
}

transform_config = {
    'mode': 'auto',
    'config': {
        'chunk_size': 1024,
        'chunk_overlap': 20
    }
}

# Create or upsert pipeline
pipeline = {
    'name': COLLECTION_NAME,
    'embedding_config': embedding_config,
    'transform_config': transform_config
}

pipeline = client.pipelines.upsert_pipeline(request=pipeline)

# Add documents to the pipeline
cloud_documents = [
    CloudDocumentCreate(
        text=doc.text,
        metadata=doc.metadata
    )
    for doc in documents
]

client.pipelines.create_batch_pipeline_documents(pipeline.id, request=cloud_documents)

print("Documents upserted to LlamaCloud pipeline successfully.") 