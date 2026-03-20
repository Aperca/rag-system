# app.py
import streamlit as st
st.set_page_config(page_title="🧠 RAG Assistant", layout="wide")
from ingestion.ingest_pipeline import run_ingestion_from_files
from retrieval.retriever import retrieve
from generation.generator import generate_answer
from PIL import Image

st.title("🧠 RAG Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR FOR UPLOAD ---
with st.sidebar:
    st.subheader("📂 Knowledge Base")
    uploaded_files = st.file_uploader(
        "Upload TXT, PDF, or images",
        type=["txt", "pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )
    if st.button("Process Documents"):
        if uploaded_files:
            with st.spinner("Analyzing..."):
                run_ingestion_from_files(uploaded_files)
            st.success("✅ Knowledge Base Updated!")
        else:
            st.warning("⚠️ Upload a file first.")

# --- MAIN CHAT INTERFACE ---
query = st.text_input("💬 Ask about your research:", placeholder="e.g., What are the research questions?")

if st.button("Submit") and query:
    results = retrieve(query)
    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not docs or docs == ['']:
        answer = "I couldn't find relevant information in the uploaded documents."
        sources = []
    else:
        answer = generate_answer(query, docs, st.session_state.history)
        sources = [f"{m.get('source')} (Page {m.get('page')})" for m in metadatas]

    st.session_state.history.append({"question": query, "answer": answer, "sources": sources})

    # DEBUG EXPANDER - Only shows up when there is a result
    with st.expander("🔍 Raw Context (What the AI is reading)"):
        for i, content in enumerate(docs):
            st.info(f"**Chunk {i+1} Metadata:** {metadatas[i]}")
            st.code(content)

# --- DISPLAY HISTORY ---
for chat in reversed(st.session_state.history):
    with st.chat_message("user"):
        st.write(chat["question"])
    with st.chat_message("assistant"):
        st.write(chat["answer"])
        if chat["sources"]:
            st.caption(f"📚 Sources: {', '.join(list(set(chat['sources'])))}")

# -------------------------------
# CLEAR HISTORY
# -------------------------------
if st.button("Clear History"):
    st.session_state.history = []
    st.success("Chat history cleared!")


