from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
from pathlib import Path
from growth.utils.rag import search_mcp
from growth.utils.query_index import create_and_upsert_index
# Add the growth directory to Python path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))
sys.path.append(str(current_dir / 'growth' / 'utils'))

try:
    # from growth.utils.query_only import search_mcp
    from growth.utils.upsert_mcp_data import process_csv_to_documents, create_and_populate_index
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Configure CORS to allow requests from your Next.js frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://themcpdirectory.com",
            "https://www.themcpdirectory.com",
            "https://theworldofmcp.com",
            "https://www.theworldofmcp.com",
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

def ensure_index_exists():
    """Ensure the search index exists and create it if it doesn't"""
    index_path = current_dir / 'storage' / 'mcp_index'
    if not index_path.exists():
        print("Creating search index...")
        csv_file = current_dir / 'growth' / 'source' / 'MCP_description.csv'
        if not csv_file.exists():
            raise FileNotFoundError(f"CSV file not found at {csv_file}")
        
        documents = process_csv_to_documents(str(csv_file))
        if documents:
            create_and_populate_index(documents, "mcp_index")
            print("Search index created successfully!")
        else:
            raise Exception("Failed to process documents from CSV")


@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.json
        query = data.get('query')
        top_k = data.get('top_k', 2)

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        # Ensure index exists before searching
        # ensure_index_exists()

        # Perform the search using the search_mcp function from rag.py
        results = search_mcp(query, top_k=top_k)

        # Format results for JSON response
        formatted_results = results['results']

        return jsonify({
            'query': query,
            'results': formatted_results  # Ensure all fields are included
        })

    except Exception as e:
        print(f"Search error: {str(e)}")  # Add logging
        return jsonify({'error': str(e)}), 500

@app.route('/api/recent-searches', methods=['GET'])
def get_recent_searches():
    # For now, return an empty list since we haven't set up MongoDB yet
    return jsonify([])

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Check if index exists or can be created
        # ensure_index_exists()
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    try:
        # Ensure index exists on startup
        ensure_index_exists()
        print("Starting Flask server...")
        print("CORS configured for http://localhost:3000 and http://127.0.0.1:3000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1) 