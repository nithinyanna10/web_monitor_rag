#!/bin/bash
set -e

VENV_PYTHON="/Users/nithinyanna/Downloads/web_monitor_rag/venv/bin/python3"
cd /Users/nithinyanna/Downloads/web_monitor_rag/web_monitor_rag

# 1. Scrape all sites
$VENV_PYTHON scraper/scrape_runner.py

# 2. Normalize the latest scrape
LATEST=$(ls -t data/run_logs/sites_*.json | head -1)
$VENV_PYTHON scraper/normalizer.py "$LATEST" "data/run_logs/normalized_output.json"

# 3. Delta detection (compare with previous run, if exists)
PREV=$(ls -t data/run_logs/sites_*.json | head -2 | tail -1)
if [ -f "$PREV" ]; then
    $VENV_PYTHON scraper/delta_detector.py "$PREV" "$LATEST" "data/run_logs/delta_output_$(date +%Y%m%d_%H%M%S).json"
fi

# 4. Insert normalized data into PostgreSQL
$VENV_PYTHON storage/postgres_connector.py

# 5. Insert normalized data into ChromaDB
$VENV_PYTHON storage/insert_normalized_to_chroma.py data/run_logs/normalized_output.json

# (Optional) Log the run
echo "Pipeline run at $(date)" >> data/run_logs/pipeline.log 