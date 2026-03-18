import streamlit as st
from ingestion.ingest_pipeline import run_ingestion_from_files
from retrieval.retriever import retrieve
from generation.generator import generate_answer

st.set_page_config(page_title="RAG Assistant", layout="wide")

st.title("🧠 RAG Assistant")
st.write("Upload documents and ask questions")

# -------------------------------
# SESSION STATE
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# FILE UPLOAD
# -------------------------------
st.subheader("📂 Upload Documents")

uploaded_files = st.file_uploader(
    "Upload TXT or PDF files",
    type=["txt", "pdf"],
    accept_multiple_files=True
)

if st.button("Process Documents"):
    if uploaded_files:
        run_ingestion_from_files(uploaded_files)
        st.success("Documents processed and stored!")
    else:
        st.warning("Please upload at least one file.")

# -------------------------------
# QUESTION INPUT
# -------------------------------
st.subheader("❓ Ask Questions")

query = st.text_input("Ask a question:")

if st.button("Submit") and query:

    results = retrieve(query)
    docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not docs or docs == ['']:
        answer = "I don’t have enough information in my knowledge base."
        sources = []
    else:
        answer = generate_answer(query, docs, st.session_state.history)
        sources = [m["source"] for m in metadatas]

    st.session_state.history.append({
        "question": query,
        "answer": answer,
        "sources": sources
    })

# -------------------------------
# DISPLAY CHAT
# -------------------------------
st.subheader("💬 Chat History")

for chat in reversed(st.session_state.history):
    st.markdown(f"**🧑 Question:** {chat['question']}")
    st.markdown(f"**🤖 Answer:** {chat['answer']}")

    if chat["sources"]:
        st.markdown("**📚 Sources:**")
        for src in chat["sources"]:
            st.markdown(f"- {src}")

    st.markdown("---")

# -------------------------------
# CLEAR
# -------------------------------
if st.button("Clear History"):
    st.session_state.history = []