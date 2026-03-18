import ollama

def generate_answer(query, docs):
    context = "\n\n".join(docs)

    prompt = f"""
You are a helpful assistant. Answer ONLY using the provided context.

Context:
{context}

Question:
{query}

Answer:
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]