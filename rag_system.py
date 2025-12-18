import os
import json
import time
from sentence_transformers import SentenceTransformer
from cyborgdb import Client
from dotenv import load_dotenv

load_dotenv()

# File to store encryption key persistently
KEY_FILE = "encryption_key.bin"

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
        
        # Load or generate encryption key (PERSIST IT!)
        self.encryption_key = self._get_or_create_key()
        print(f"Encryption key ready ({len(self.encryption_key)} bytes)")
        
        # Index settings
        self.index_name = "support_tickets"
        self.index = None

    def _get_or_create_key(self):
        """Load existing key or generate and save a new one"""
        if os.path.exists(KEY_FILE):
            print(f"Loading existing encryption key from {KEY_FILE}")
            with open(KEY_FILE, 'rb') as f:
                return f.read()
        else:
            print("Generating new encryption key...")
            key = self.client.generate_key()
            with open(KEY_FILE, 'wb') as f:
                f.write(key)
            print(f"Saved encryption key to {KEY_FILE}")
            return key

    def _ensure_index(self):
        """Create or load index"""
        if self.index is not None:
            return
        
        # Check if index exists
        existing = self.client.list_indexes()
        
        if self.index_name in existing:
            print(f"Loading existing index: {self.index_name}")
            try:
                self.index = self.client.load_index(
                    index_name=self.index_name,
                    index_key=self.encryption_key
                )
            except Exception as e:
                # Key mismatch - need to delete and recreate
                print(f"Key mismatch detected, recreating index...")
                self._delete_and_recreate_index()
        else:
            print(f"Creating new index: {self.index_name}")
            self.index = self.client.create_index(
                index_name=self.index_name,
                index_key=self.encryption_key
            )
        print(f"Index ready: {self.index_name}")

    def _delete_and_recreate_index(self):
        """Delete existing index and create fresh one"""
        try:
            # Delete old index
            print(f"Deleting old index: {self.index_name}")
            self.client.delete_index(self.index_name)
        except Exception as e:
            print(f"Could not delete index: {e}")
        
        # Create new index with current key
        print(f"Creating fresh index: {self.index_name}")
        self.index = self.client.create_index(
            index_name=self.index_name,
            index_key=self.encryption_key
        )
        
        # Reload tickets if they exist
        if os.path.exists('tickets.json'):
            print("Re-indexing tickets...")
            self._load_tickets_internal('tickets.json')

    def _load_tickets_internal(self, filepath):
        """Internal method to load tickets without ensuring index"""
        with open(filepath, 'r') as f:
            tickets = json.load(f)
        
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
        
        self.index.upsert(items)
        return len(tickets)

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

    def reset_index(self):
        """Force delete and recreate index - useful for fixing key issues"""
        print("Resetting index...")
        
        # Delete key file to generate new one
        if os.path.exists(KEY_FILE):
            os.remove(KEY_FILE)
            print(f"Deleted {KEY_FILE}")
        
        # Generate new key
        self.encryption_key = self._get_or_create_key()
        
        # Reset index reference
        self.index = None
        
        # Delete and recreate
        self._delete_and_recreate_index()
        
        print("Index reset complete!")


# Test
if __name__ == "__main__":
    rag = SecureSupportRAG()
    rag.load_tickets('tickets.json')
    results, latency = rag.search("How to fix SIM error?")
    print(f"\nResults: {results}")