import streamlit as st
import os
import json
from glob import glob
from web_monitor_rag.rag_engine.query_handler import query_rag
from web_monitor_rag.storage.chroma_connector import get_collection

st.set_page_config(page_title="web monitor Dashboard", layout="wide")
st.title("Smart Web Monitor Dashboard")

TABS = ["Delta Viewer", "RAG Chat", "ChromaDB Viewer"]
tab1, tab2, tab3 = st.tabs(TABS)

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/run_logs')

with tab1:
    st.header("Delta Viewer")
    delta_files = sorted(glob(os.path.join(DATA_DIR, 'delta_output*.json')) + glob(os.path.join(DATA_DIR, 'delta*.json')))
    if not delta_files:
        st.info("No delta files found. Run the delta detector to generate deltas.")
    else:
        selected = st.selectbox("Select a delta file", delta_files)
        if selected:
            with open(selected, 'r', encoding='utf-8') as f:
                delta = json.load(f)
            st.subheader("Delta Changes")
            for site, changes in delta.items():
                st.markdown(f"**{site}**")
                if not changes:
                    st.write("No changes.")
                else:
                    for key, val in changes.items():
                        st.write(f"- {key}:\n    Old: {val['old']}\n    New: {val['new']}")

with tab2:
    st.header("RAG Chat (Ask the LLM)")
    user_query = st.text_input("Enter your question:")
    if st.button("Ask") and user_query:
        with st.spinner("Retrieving answer..."):
            rag_result = query_rag(user_query)
            st.markdown("**Prompt sent to LLM:**")
            st.code(rag_result['prompt'])
            from web_monitor_rag.rag_engine.rag_llm_integration import ask_gemma
            answer = ask_gemma(rag_result['prompt'])
            st.markdown("**LLM Answer:**")
            st.success(answer)

with tab3:
    st.header("ChromaDB Viewer")
    col = get_collection()
    all_data = col.get()
    st.markdown(f"**Total documents:** {len(all_data['documents'])}")
    for doc, meta in zip(all_data['documents'], all_data['metadatas']):
        with st.expander(f"Site: {meta.get('site', 'unknown')}"):
            st.write(doc)
            st.json(meta)
