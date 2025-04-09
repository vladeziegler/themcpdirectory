# import os
# from dotenv import load_dotenv
# from openai import OpenAI  # Import the OpenAI client
# from llama_index.indices.managed.llama_cloud import LlamaCloudIndex

# # Load environment variables
# load_dotenv()

# # Initialize the OpenAI client
# client = OpenAI()

# # Initialize the LlamaCloudIndex
# index = LlamaCloudIndex(
#     # name="frequent-primate-2025-04-08",
#     name="elegant-hawk-2025-04-08",
#     project_name="Default",
#     organization_id="8e327feb-280a-4a46-abcb-67662f3a4522",
#     api_key=os.getenv("LLAMA_CLOUD_API_KEY")  # Ensure this key is set in your .env file
# )

# def summarize_results_with_llm(results):
#     """
#     Summarize the search results using an LLM
    
#     Args:
#         results (list): List of search results with their scores and metadata
        
#     Returns:
#         str: A concise summary of the results
#     """
#     # Prepare the input for the LLM
#     input_text = "\n".join([
#         f"URL: {result['url']}\nDescription: {result['text']}"
#         for result in results
#     ])
    
#     # Define the system prompt
#     system_prompt = (
#         "You are an AI assistant. Summarize the following MCP server descriptions. You don't need to introduce the concept of MCP servers, just answer the question."
#         "to answer: What can the MCP server in question do? Why is it useful if added as a tool to AI agents? "
#         "Keep the URLs intact and unchanged."
#         "Keep the summary concise and to the point. Use markdown formatting whenever possible to separate each MCP server description. It should be very easy to distinguish each MCP server description, and their URLs."
#     )
    
#     # Call the LLM
#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=[
#             {
#                 "role": "system",
#                 "content": system_prompt
#             },
#             {
#                 "role": "user",
#                 "content": input_text
#             }
#         ]
#     )
    
#     # Extract the summary from the response
#     summary = response.choices[0].message.content.strip()
#     return summary

# def search_mcp(query: str, top_k: int = 5):
#     """
#     Search the MCP index with a natural language query and summarize results
    
#     Args:
#         query (str): The search query
#         top_k (int): Number of results to return (default: 5)
        
#     Returns:
#         dict: Dictionary containing the query, raw results, and summary
#     """
#     try:
#         # Retrieve nodes from the cloud index
#         nodes = index.as_retriever().retrieve(query)
        
#         # Sort and limit to top_k results
#         final_results = sorted(
#             nodes,
#             key=lambda x: x.score,
#             reverse=True
#         )[:top_k]
        
#         # Ensure results are in the correct format
#         formatted_results = [
#             {
#                 'url': node.metadata.get('url', 'N/A'),
#                 'text': node.text,
#                 'score': node.score
#             }
#             for node in final_results
#         ]
        
#         # Summarize the results using LLM
#         summary = summarize_results_with_llm(formatted_results)
        
#         return {
#             'query': query,
#             'results': formatted_results,
#             'summary': summary
#         }
        
#     except Exception as e:
#         print(f"Error during search: {e}")
#         return {
#             'query': query,
#             'results': [],
#             'summary': f"Error: {str(e)}"
#         }

# def main():
#     import argparse
    
#     parser = argparse.ArgumentParser(description='Search MCP Descriptions')
#     parser.add_argument('query', type=str, help='The search query')
#     parser.add_argument('--top-k', type=int, default=5, help='Number of results to return')
    
#     args = parser.parse_args()
    
#     results = search_mcp(args.query, args.top_k)
    
#     print(results['summary'])

# if __name__ == "__main__":
#     main()


import os
from dotenv import load_dotenv
from openai import OpenAI  # Import the OpenAI client
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from pydantic import BaseModel
import json

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

# Initialize the LlamaCloudIndex
index = LlamaCloudIndex(
    # name="frequent-primate-2025-04-08",
    name="elegant-hawk-2025-04-08",
    project_name="Default",
    organization_id="8e327feb-280a-4a46-abcb-67662f3a4522",
    api_key=os.getenv("LLAMA_CLOUD_API_KEY")  # Ensure this key is set in your .env file
)

class MCPServer(BaseModel):
    url: str
    description: str
    what_can_it_do: str
    why_is_it_useful: str

def summarize_results_with_llm(results):
    """
    Summarize the search results using an LLM
    
    Args:
        results (list): List of search results with their scores and metadata
        
    Returns:
        str: A concise summary of the results
    """
    # Prepare the input for the LLM
    input_text = "\n".join([
        f"URL: {result['url']}\nDescription: {result['text']}"
        for result in results
    ])
    
    # Define the system prompt
    system_prompt = (
        "You are an AI assistant. Summarize the following MCP server descriptions. You don't need to introduce the concept of MCP servers, just answer the question."
        "to answer: What can the MCP server in question do? Why is it useful if added as a tool to AI agents? "
        "Keep the URLs intact and unchanged."
        "Keep the summary concise and to the point. Use markdown formatting whenever possible to separate each MCP server description. It should be very easy to distinguish each MCP server description, and their URLs."
    )
    
    # Call the LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
        temperature=0.1  # Set low temperature for deterministic output
    )
    
    # Extract the summary from the response
    summary = response.choices[0].message.content.strip()
    return summary

def convert_to_structured_objects(results):
    """
    Use LLM to convert results into structured MCPServer objects
    
    Args:
        results (list): List of raw results from RAG
        
    Returns:
        list: List of structured MCPServer objects
    """
    # Prepare the input for the LLM
    input_text = "\n".join([
        f"URL: {result['url']}\nDescription: {result['text']}"
        for result in results
    ])
    
    # Define the system prompt
    system_prompt = (
        "You are an AI assistant. Convert the following MCP server descriptions into structured JSON objects. "
        "Each object should contain a 'url', 'description', 'what_can_it_do', and 'why_is_it_useful'. Output the objects in a JSON array format."
    )
    
    # Call the LLM
    response = client.chat.completions.create(
        model="gpt-4o",  # Consider switching back to gpt-4 for better output
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
        temperature=0.1  # Set low temperature for deterministic output
    )
    
    # Extract the structured objects from the response
    structured_objects = response.choices[0].message.content.strip()
    print(f"LLM Output (raw): {structured_objects}")  # Detailed logging for inspection
    
    # Remove Markdown formatting (triple backticks and json label)
    if structured_objects.startswith('```json') and structured_objects.endswith('```'):
        structured_objects = structured_objects[7:-3].strip()
    elif structured_objects.startswith('```') and structured_objects.endswith('```'):
        structured_objects = structured_objects[3:-3].strip()
    
    print(f"LLM Output (cleaned): {structured_objects}")  # Log cleaned output
    
    # Check if the structured_objects is empty
    if not structured_objects:
        print("Error: LLM output is empty.")
        return []
    
    # Convert the structured objects into MCPServer instances
    try:
        structured_results = json.loads(structured_objects)  # Use json.loads for safe parsing
        return [MCPServer(**obj) for obj in structured_results]
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        # Attempt to clean the output and retry parsing
        try:
            # Remove any leading/trailing whitespace and retry
            cleaned_output = structured_objects.strip()
            structured_results = json.loads(cleaned_output)
            return [MCPServer(**obj) for obj in structured_results]
        except json.JSONDecodeError as e:
            print(f"Retry JSON decoding error: {e}")
            return []
    except Exception as e:
        print(f"Error converting to structured objects: {e}")
        return []

def search_mcp(query: str, top_k: int = 5):
    """
    Search the MCP index with a natural language query and return structured results
    
    Args:
        query (str): The search query
        top_k (int): Number of results to return (default: 5)
        
    Returns:
        dict: Dictionary containing the query and structured results
    """
    try:
        # Retrieve nodes from the cloud index
        nodes = index.as_retriever().retrieve(query)
        
        # Sort and limit to top_k results
        final_results = sorted(
            nodes,
            key=lambda x: x.score,
            reverse=True
        )[:top_k]
        
        # Ensure results are in the correct format
        raw_results = [
            {
                'url': node.metadata.get('url', 'N/A'),
                'text': node.text
            }
            for node in final_results
        ]
        
        # Convert raw results to structured objects using LLM
        structured_results = convert_to_structured_objects(raw_results)
        
        return {
            'query': query,
            'results': [result.model_dump() for result in structured_results]
        }
        
    except Exception as e:
        print(f"Error during search: {e}")
        return {
            'query': query,
            'results': [],
            'error': str(e)
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Search MCP Descriptions')
    parser.add_argument('query', type=str, help='The search query')
    parser.add_argument('--top-k', type=int, default=2, help='Number of results to return')
    
    args = parser.parse_args()
    
    results = search_mcp(args.query, args.top_k)
    
    print(results['results'])  # Print results instead of summary

if __name__ == "__main__":
    main()