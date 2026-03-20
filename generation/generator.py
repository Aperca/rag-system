import ollama

def generate_answer(query, docs, history):
    context = "\n\n".join(docs)

    # Format chat history
    history_text = ""
    for chat in history[-3:]:  # last 3 messages only (keep it light)
        history_text += f"User: {chat['question']}\nAssistant: {chat['answer']}\n"

    prompt = f"""
ou are an expert academic assistant. Analyze the provided context thoroughly.
Use the conversation history AND the provided context to answer the question.

If the answer is not in the context, say:
"I don’t have enough information in my knowledge base."

---------------------
Conversation History:
{history_text}

---------------------
Context:
{context}

---------------------
Question:
{query}

Answer:
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]