import streamlit as st
st.set_page_config(page_title="🧠 RAG Assistant", layout="wide")
from ingestion.ingest_pipeline import run_ingestion_from_files
from retrieval.retriever import retrieve
from generation.generator import generate_answer
from PIL import Image

st.title("🧠 RAG Assistant")
st.write("Upload documents (TXT, PDF, images) and ask questions based on them.")

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
    "Upload TXT, PDF, or image files",
    type=["txt", "pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if st.button("Process Documents"):
    if uploaded_files:
        run_ingestion_from_files(uploaded_files)
        st.success("✅ Documents processed and stored!")
    else:
        st.warning("⚠️ Please upload at least one file.")

# -------------------------------
# QUESTION INPUT
# -------------------------------
st.subheader("❓ Ask Questions")
query = st.text_input("Ask a question:")

if st.button("Submit") and query:

    # Retrieve relevant chunks from Chroma
    results = retrieve(query)
    st.write(f"Debug: Found {len(results['documents'][0])} matching chunks.") 
    docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Generate answer using retrieved context and chat history
    if not docs or docs == ['']:
        answer = "I don’t have enough information in my knowledge base."
        sources = []
    else:
        answer = generate_answer(query, docs, st.session_state.history)
        sources = [m.get("source") for m in metadatas]

    # Append to memory
    st.session_state.history.append({
        "question": query,
        "answer": answer,
        "sources": sources
    })

# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------
st.subheader("💬 Chat History")
for chat in reversed(st.session_state.history):
    st.markdown(f"**🧑 Question:** {chat['question']}")
    st.markdown(f"**🤖 Answer:** {chat['answer']}")

    if chat["sources"]:
        st.markdown("**📚 Sources:**")
        for src in chat["sources"]:
            # Show images inline if available
            if src.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    img = Image.open(src)
                    st.image(img, caption=src, use_column_width=True)
                except:
                    st.markdown(f"- {src} (image not loaded)")
            else:
                st.markdown(f"- {src}")
    st.markdown("---")

# -------------------------------
# CLEAR HISTORY
# -------------------------------
if st.button("Clear History"):
    st.session_state.history = []
    st.success("Chat history cleared!")