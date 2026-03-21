import ollama

def generate_answer(query, docs, history):
    # Label each chunk so the AI knows its context
    context = ""
    for i, doc in enumerate(docs):
        context += f"--- Source Chunk {i+1} ---\n{doc}\n\n"

    history_text = ""
    for chat in history[-3:]:
        history_text += f"User: {chat['question']}\nAssistant: {chat['answer']}\n"

    # We use a "System" role for the instructions and "User" for the query
    prompt = f"""You are an expert academic research assistant. 
Use the following context to answer the user's question accurately. Integrate the information naturally—do not say "According to Chunk X". instead say "according to the document..."
If the answer is not in the context, strictly say: "I don’t have enough information in my knowledge base."

Conversation History:
{history_text}

Context:
{context}

Question: {query}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]