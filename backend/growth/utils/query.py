from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
# pip install llama-index-indices-managed-llama-cloud

index = LlamaCloudIndex(
  name="frequent-primate-2025-04-08",
  project_name="Default",
  organization_id="8e327feb-280a-4a46-abcb-67662f3a4522",
  api_key="llx-Mhi1SgWcY5jO9CRPnqfbEjVPur1VaqtP71wToEAzBQeAT2gm",
)

query = "What are the top 3 MCPs for web search? Return the URLs of the MCPs."
nodes = index.as_retriever().retrieve(query)
response = index.as_query_engine().query(query)

print(response)