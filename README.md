# Monitoring Platform + RAG

A full-stack, automated pipeline for monitoring, scraping, and analyzing simulated retail websites using RAG (Retrieval-Augmented Generation), PostgreSQL, ChromaDB, and LLMs (e.g., Gemma via Ollama). Includes a Streamlit dashboard for data exploration and chat.

---

## Features
- **Mock Sites:** 5 Flask apps simulating dynamic retail, news, weather, stock, and event sites.
- **Scraper Engine:** Automated scraping, normalization, and delta detection.
- **Storage Layer:** Structured data in PostgreSQL, embeddings in ChromaDB (persistent).
- **RAG Engine:** Embedding-based retrieval and LLM-powered Q&A.
- **Dashboard:** Streamlit UI for deltas, RAG chat, and ChromaDB viewer.
- **Automation:** Full pipeline runs hourly via cronjob.

---

## Project Structure
```
web_monitor_rag/
  web_monitor_rag/
    dashboard/           # Streamlit dashboard app
    data/                # Scraped data, logs, deltas
    mock_sites/          # Flask mock sites (site1.py ... site5.py)
    rag_engine/          # RAG engine: embedder, query handler, LLM integration
    scraper/             # Scraper, normalizer, delta detector
    storage/             # PostgreSQL and ChromaDB connectors, insertion scripts
    run_full_pipeline.sh # Master automation script
    requirements.txt     # All dependencies
```

---

## Setup

### 1. Clone & Install
```sh
git clone <repo-url>
cd web_monitor_rag/web_monitor_rag
python3 -m venv ../../venv
source ../../venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure PostgreSQL
- Create a database (e.g., `postgres`)
- Set environment variables as needed:
  - `PG_HOST`, `PG_PORT`, `PG_USER`, `PG_PASSWORD`, `PG_DATABASE`

### 3. Start Mock Sites
```sh
cd mock_sites
bash run_all.sh
```

### 4. Run the Full Pipeline Manually
```sh
cd /Users/nithinyanna/Downloads/web_monitor_rag/web_monitor_rag
./run_full_pipeline.sh
```

### 5. Start the Dashboard
```sh
cd /Users/nithinyanna/Downloads/web_monitor_rag
PYTHONPATH=. streamlit run web_monitor_rag/dashboard/app.py
```

### 6. (Optional) Run LLM (Gemma) with Ollama
- Pull and run your desired Gemma model with Ollama:
  ```sh
  ollama pull gemma3:27b-it-qat
  ollama run gemma3:27b-it-qat
  ```
- The RAG engine will connect to Ollama at `http://localhost:11434/api/chat`.

---

## Automation (Cronjob)
To run the pipeline hourly, add to your crontab:
```sh
0 * * * * /Users/nithinyanna/Downloads/web_monitor_rag/web_monitor_rag/run_full_pipeline.sh >> /Users/nithinyanna/Downloads/web_monitor_rag/web_monitor_rag/data/run_logs/cron.log 2>&1
```

---

## Dashboard Features
- **Delta Viewer:** Browse and inspect changes between scrapes.
- **RAG Chat:** Ask questions, see the prompt/context, and get LLM answers.
- **ChromaDB Viewer:** Browse all stored documents and metadata in your vector DB.

---

## Extending & Customizing
- Add more mock sites or connect to real sites.
- Enhance normalization, delta detection, or prompt templates.
- Integrate notifications, analytics, or more advanced LLMs.

---

## Troubleshooting
- **ModuleNotFoundError:** Run Streamlit with `PYTHONPATH=.` from the outer project directory.
- **No data in ChromaDB:** Ensure you run the insertion script after each scrape and use persistent storage.
- **LLM not using context:** Check that ChromaDB is populated and queries are semantically close to stored data.

---

## Credits
- Built with [Streamlit](https://streamlit.io/), [ChromaDB](https://www.trychroma.com/), [PostgreSQL](https://www.postgresql.org/), [Ollama](https://ollama.com/), [sentence-transformers](https://www.sbert.net/), and open-source LLMs.

---

## License
MIT
