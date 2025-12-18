import os
os.environ['CYBORGDB_API_KEY'] = 'cyborg_546893b7f62a4c2ea169caf396c2bf15'

from cyborgdb import Client

# Initialize client
print("Initializing CyborgDB client...")
client = Client(
    api_key=os.getenv('CYBORGDB_API_KEY'),
    base_url="https://api.cyborg.co"
)

print("✓ Client created successfully!")

# Generate encryption key
print("\nGenerating encryption key...")
encryption_key = client.generate_key()
print(f"✓ Encryption key generated (length: {len(encryption_key)} bytes)")

# Create an encrypted index
print("\nCreating encrypted index...")
index = client.create_index(
    index_name="support_tickets",
    index_key=encryption_key,
    metric="cosine"
)

print(f"✓ Index created successfully!")
print(f"  Index name: {index.index_name}")

# Test adding a vector
import numpy as np
print("\nAdding test vector...")

test_vector = np.random.rand(384).tolist()

index.add(
    ids=["ticket_1"],
    embeddings=[test_vector],
    metadata=[{"text": "Test ticket about SIM card error"}]
)

print("✓ Vector added successfully!")

# Query
print("\nQuerying...")
results = index.query(
    query_embeddings=[test_vector],
    k=1
)

print(f"✓ Query results: {results}")
print("\n🎉 CyborgDB is working!")