import streamlit as st
from retrieval.retriever import retrieve
from generation.generator import generate_answer

st.set_page_config(page_title="RAG Assistant", layout="wide")

st.title("🧠 RAG Assistant")
st.write("Ask questions based on your knowledge base")

# -------------------------------
# SESSION STATE (CHAT HISTORY)
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# INPUT
# -------------------------------
query = st.text_input("Ask a question:")

# -------------------------------
# MAIN LOGIC
# -------------------------------
if st.button("Submit") and query:

    # Retrieve relevant docs
    results = retrieve(query)
    docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    # -------------------------------
    # SAFETY: HANDLE NO RESULTS
    # -------------------------------
    if not docs or docs == ['']:
        answer = "I don’t have enough information in my knowledge base to answer that."
        sources = []
    else:
        # Generate answer
        answer = generate_answer(query, docs, st.session_state.history)        sources = [m["source"] for m in metadatas]

    # Save to history
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
            st.markdown(f"- {src}")

    st.markdown("---")

# -------------------------------
# CLEAR BUTTON
# -------------------------------
if st.button("Clear History"):
    st.session_state.history = []