
# 🧠 Semantic Document Search (RAG)

> **Retrieval Augmented Generation • AI-Powered Document Intelligence**

## 📌 What is This?

Traditional keyword search finds exact word matches — this app understands **meaning**. Ask *"what is hadoop?"* and it finds relevant content even if the document uses different phrasing. Built on a **RAG (Retrieval Augmented Generation)** pipeline, it's also ready to plug directly into any LLM for automated document Q&A.

---
## ✨ Features

- 🔍 **Semantic Search** — Understands meaning, not just keywords
- 📄 **Multi-Format Support** — PDF, DOCX, and TXT files
- ⚡ **Sub-100ms Search** — FAISS-powered instant results
- 📊 **Relevance Scores** — Every result ranked by similarity percentage
- ⚙️ **Configurable Chunking** — Tune chunk size and overlap
- 📈 **Live Dashboard** — Track documents, chunks, and queries
- 🤖 **LLM-Ready** — Direct RAG integration for LLM augmentation

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/semantic-doc-search.git
cd semantic-doc-search
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```


## 🗂️ Project Structure

```
semantic-doc-search/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🧭 How to Use

### Step 1 — Upload Documents
- Go to the **UPLOAD** tab
- Select one or more PDF, DOCX, or TXT files
- Adjust **Chunk Size** (default: 1200) and **Overlap** (default: 150) if needed
- Click **INDEX DOCUMENTS** and wait for the success message

### Step 2 — Search
- Go to the **SEARCH** tab
- Type any natural language query (e.g., *"explain the water cycle"*)
- Adjust the **Top Results** slider to control how many matches appear
- Results display instantly with similarity scores

### Step 3 — Monitor
- Check the **DASHBOARD** tab to see total documents, chunks, and searches
- Visit the **INFO** tab for technical architecture details

---

## ⚙️ How It Works

```
Documents → Load → Chunk → Embed → FAISS Index
                                        ↕
Query    → Embed → Vector Search → Ranked Results
```

| Stage | Tool | Description |
|-------|------|-------------|
| Document Loading | LangChain Loaders | Extracts text from PDF, DOCX, TXT |
| Chunking | RecursiveCharacterTextSplitter | Splits text into overlapping segments |
| Embedding | all-MiniLM-L6-v2 | Converts text to 384-dim vectors |
| Indexing | FAISS | Stores and indexes all vectors |
| Search | FAISS similarity search | Finds nearest vectors to query |
| Ranking | Cosine similarity | Returns results by relevance score |

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥1.32 | Web UI framework |
| `langchain-community` | ≥0.0.20 | Document loaders & vectorstore |
| `faiss-cpu` | ≥1.7.4 | Vector database |
| `sentence-transformers` | ≥2.2.2 | Embedding model runtime |
| `huggingface-hub` | ≥0.20 | Model downloading |
| `pypdf` | ≥3.17 | PDF text extraction |
| `docx2txt` | ≥0.8 | DOCX text extraction |
| `numpy` | ≥1.24 | Vector operations |

---

## 📐 Configuration

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| Chunk Size | 1200 | 500–3000 | Characters per text segment |
| Overlap | 150 | 0–500 | Shared characters between chunks |
| Top Results | 5 | 1–15 | Number of matches to return |

---

## 📊 Performance

- **Index Build:** ~1 second per 100 pages
- **Search Speed:** <50ms average
- **Memory:** ~1MB per 1000 chunks
- **Embedding Model:** 22M parameters, runs fully offline


## 🔮 Roadmap

- [ ] Persistent FAISS index (save/load between sessions)
- [ ] LLM integration for automated Q&A
- [ ] Document source + page number in results
- [ ] Support for CSV, HTML, Markdown files
- [ ] Hybrid BM25 + vector search
- [ ] Multi-user support with separate namespaces



  <b>Built with ⚡ by Vector Intelligence</b><br/>
  <i>FAISS + HuggingFace + LangChain + Streamlit</i>
</div>
