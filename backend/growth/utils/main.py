from query_only import search_mcp

def main():
    results = search_mcp("best MCP for browsing", top_k=5)
    for result in results:
        print(f"URL: {result.metadata['url']}")
        print(f"Text: {result.text}")

if __name__ == "__main__":
    main()
