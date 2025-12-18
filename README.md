# SecureSupport - Encrypted RAG for Telecom Customer Support

**CyborgDB Hackathon 2025 Submission**

Submitted by: Sunanda Mandal

## Overview

SecureSupport is a privacy-preserving RAG system for telecom customer support that uses CyborgDB's encrypted vector search to eliminate the vector inversion vulnerability present in traditional vector databases.

## Problem

Vector embeddings in standard databases can be inverted to reconstruct original data. For telecom companies handling sensitive customer data (PII, account details, support history), this is unacceptable.

## Solution

Encrypted vector search using CyborgDB where:
- Vectors encrypted client-side before storage
- Search performed on encrypted data
- Decryption only in application memory
- Customer-controlled encryption keys

## Features

- ✅ End-to-end encrypted vector storage
- ✅ Sub-400ms query latency (337ms average)
- ✅ Local LLM integration (Llama 3.2)
- ✅ 100 sample telecom support tickets
- ✅ Zero-trust architecture

## Tech Stack

- **CyborgDB SDK** - Encrypted vector search
- **PostgreSQL** - Encrypted vector storage
- **sentence-transformers** - Embedding generation (all-MiniLM-L6-v2)
- **Ollama** - Local LLM (Llama 3.2 1B)
- **Streamlit** - Web interface

## Installation

### Prerequisites
- Python 3.10+
- Docker Desktop
- Ollama
- CyborgDB API Key (from db.cyborg.co)

### Quick Start

1. Clone repository:
```bash
git clone https://github.com/28sunanda/securesupport.git
cd securesupport
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
# Copy .env.example to .env and add your API key
cp .env.example .env
# Edit .env with your CYBORGDB_API_KEY from db.cyborg.co
```

5. Start PostgreSQL:
```bash
docker-compose up -d
```

6. Start Ollama:
```bash
# In separate terminal
ollama serve
ollama pull llama3.2:1b
```

7. Start CyborgDB Service:
```bash
# Follow CyborgDB documentation for local service setup
# Service should run on http://localhost:8000
```

8. Run application:
```bash
python generate_tickets.py
streamlit run app.py
```

9. Open http://localhost:8501

## Performance

- **Query Latency**: 150-400ms (337ms average)
- **Encryption Overhead**: ~20ms per query
- **Dataset**: 100 tickets across 6 categories
- **Vector Dimension**: 384

## Architecture
```
User Query
  ↓
Embedding Model (all-MiniLM-L6-v2)
  ↓
CyborgDB Client Encryption
  ↓
Encrypted Vector Search (localhost:8000)
  ↓
Results Decrypted (client-side only)
  ↓
LLM Context Generation (Ollama)
  ↓
Response
```

## CyborgDB Evaluation

### What Works Well
✅ Simple SDK integration
✅ Sub-second encrypted queries  
✅ Client-controlled encryption keys
✅ Familiar API patterns

### Integration Challenges
⚠️ CyborgDB service Docker setup needs clearer documentation
⚠️ Service base URL configuration not obvious (localhost:8000 vs api.cyborg.co)
⚠️ No batch query API for bulk operations
⚠️ Limited metadata filtering capabilities

### Recommendations for CyborgDB Team
- Provide official Docker Compose template with all services
- Add comprehensive troubleshooting guide
- Document encryption key rotation procedures
- Add monitoring/metrics integration examples
- Create batch query API for high-throughput scenarios

## Security Benefits

| Threat | Traditional RAG | SecureSupport |
|--------|----------------|---------------|
| Database Breach | ⚠️ Vectors exposed | ✅ Encrypted, unusable |
| Vector Inversion | ⚠️ Data recoverable | ✅ Mathematically impossible |
| Insider Threat | ⚠️ Admin sees all | ✅ Zero-knowledge storage |
| Memory Dump | ⚠️ Vectors in RAM | ✅ Decryption client-only |

## Project Structure
```
securesupport/
├── app.py                    # Streamlit web interface
├── rag_system.py            # Core RAG logic with CyborgDB
├── generate_tickets.py      # Sample data generator
├── docker-compose.yml       # PostgreSQL setup
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

## Future Enhancements

- Multi-tenant isolation patterns
- Real-time ticket ingestion from Zendesk/Salesforce
- Enterprise SSO integration for key management
- Audit logging for compliance reporting
- Horizontal scaling with multiple CyborgDB instances

## License

MIT License - See LICENSE file

## Hackathon Submission

This project was built for the CyborgDB Hackathon 2025 to demonstrate secure, encrypted vector search for sensitive enterprise data.

**Key Achievement**: Eliminated vector inversion vulnerability while maintaining sub-400ms query performance.

## Contact

Sunanda Mandal
- GitHub: [@28sunanda](https://github.com/28sunanda)
- Linkedin: https://www.linkedin.com/in/sunanda-mandal
