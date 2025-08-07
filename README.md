# Qdrant Vector Search API with Flask

This project provides a simple REST API built with **Flask** for storing and retrieving string data using **vector embeddings** in a **Qdrant vector database**. It allows users to store textual data and retrieve the most relevant matches based on partial input queries using cosine similarity.

---

## 🚀 Features

- Store strings with their vector embeddings
- Retrieve original strings using partial matches
- Uses **Qdrant** as the vector search backend
- Embeddings generated using `SentenceTransformer`
- Fully containerized using Docker and Docker Compose
- Easy-to-use API endpoints

---

## Setup Instructions

### 1. Clone the Repository
<pre>git clone https://github.com/theashishmavii/Qdrant-API-project.git</pre>

### 2. Make sure docker is running
<pre>docker-compose up --build</pre>

---

## 📁 Project Structure

```plaintext
.
├── app/
│ ├── init.py
│ ├── main.py
| ├──qdrant_client.py
| ├──embedding.py
│ └── static/
│ └── index.html # (Optional UI for testing)
├── .env # Environment variables
├── requirements.txt # Python dependencies
├── Dockerfile # Image for Flask service
├── docker-compose.yml # Setup Flask + Qdrant services
└── README.md # You’re here!

---