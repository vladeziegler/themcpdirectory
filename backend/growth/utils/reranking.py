import os

os.environ[
    "LLAMA_CLOUD_API_KEY"
] = "llx-Mhi1SgWcY5jO9CRPnqfbEjVPur1VaqtP71wToEAzBQeAT2gm"  # can provide API-key in env or in the constructor later on

from llama_index.indices.managed.llama_cloud import LlamaCloudIndex

# connect to existing index 
index = LlamaCloudIndex("frequent-primate-2025-04-08", project_name="Default")

# configure retriever
retriever = index.as_retriever(
  dense_similarity_top_k=3,
  sparse_similarity_top_k=3,
  alpha=0.5,
  enable_reranking=True, 
  rerank_top_n=3,
)
nodes = retriever.retrieve("What are the top 3 MCPs for web search? Return the URLs of the MCPs.")

print(nodes)
print("--------------------------------")
print(nodes[0].metadata)
print("--------------------------------")
print(nodes[0].text)
print("--------------------------------")
print(nodes[1].metadata)
print("--------------------------------")
print(nodes[1].text)
print("--------------------------------")
print(nodes[2].metadata)
print("--------------------------------")