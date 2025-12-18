import os
import json
import time
from sentence_transformers import SentenceTransformer
from cyborgdb import Client
from dotenv import load_dotenv

load_dotenv()

class SecureSupportRAG:
    def __init__(self):
        print("Initializing SecureSupport with CyborgDB...")
        
        # Initialize CyborgDB client
        self.client = Client(
            api_key=os.getenv('CYBORGDB_API_KEY'),
            base_url="http://localhost:8000"
        )
        
        # Load embedding model
        print("Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Generate encryption key
        self.encryption_key = self.client.generate_key()
        print(f"Generated encryption key ({len(self.encryption_key)} bytes)")
        
        # Index settings
        self.index_name = "support_tickets"
        self.index = None

    def _ensure_index(self):
        """Create or load index"""
        if self.index is not None:
            return
        
        # Check if index exists
        existing = self.client.list_indexes()
        
        if self.index_name in existing:
            print(f"Loading existing index: {self.index_name}")
            self.index = self.client.load_index(
                index_name=self.index_name,
                index_key=self.encryption_key
            )
        else:
            print(f"Creating new index: {self.index_name}")
            self.index = self.client.create_index(
                index_name=self.index_name,
                index_key=self.encryption_key
            )
        print(f"Index ready: {self.index_name}")

    def load_tickets(self, filepath):
        """Load and index support tickets"""
        self._ensure_index()
        
        print(f"\nLoading tickets from {filepath}...")
        
        with open(filepath, 'r') as f:
            tickets = json.load(f)
        
        print(f"Embedding and encrypting {len(tickets)} tickets...")
        start_time = time.time()
        
        # Prepare items in the format CyborgDB expects
        items = []
        for ticket in tickets:
            embedding = self.model.encode(ticket['text']).tolist()
            items.append({
                "id": ticket['id'],
                "vector": embedding,
                "metadata": {
                    "text": ticket['text'],
                    "category": ticket['category']
                }
            })
        
        # Upsert items
        self.index.upsert(items)
        
        elapsed = time.time() - start_time
        print(f"Indexed {len(tickets)} tickets in {elapsed:.2f}s")
        print(f"  Average: {elapsed/len(tickets)*1000:.2f}ms per ticket")
        return len(tickets)

    def search(self, query, top_k=3):
        """Search for relevant tickets"""
        self._ensure_index()
        
        print(f"\nSearching for: '{query}'")
        start_time = time.time()
        
        # Embed query
        query_embedding = self.model.encode(query).tolist()
        
        # Query encrypted index - returns list of dicts with 'id', 'metadata', etc.
        results = self.index.query(
            query_vectors=query_embedding,
            top_k=top_k,
            include=["metadata"]
        )
        
        elapsed = time.time() - start_time
        print(f"Search completed in {elapsed*1000:.2f}ms")
        
        # Format results for app.py compatibility
        formatted = {
            'ids': [[r.get('id', '') for r in results]],
            'metadata': [[r.get('metadata', {}) for r in results]]
        }
        
        return formatted, elapsed * 1000

# Test
if __name__ == "__main__":
    rag = SecureSupportRAG()
    rag.load_tickets('tickets.json')
    results, latency = rag.search("How to fix SIM error?")
    print(f"\nResults: {results}")
