from ingestion.ingest_pipeline import run_ingestion
from retrieval.retriever import retrieve
from generation.generator import generate_answer


if __name__ == "__main__":

    # run once (comment later)
    # run_ingestion()

    query = "What is artificial intelligence?"

    results = retrieve(query)

    docs = results["documents"][0]

    answer = generate_answer(query, docs)

    print("\nFINAL ANSWER:\n")
    print(answer)