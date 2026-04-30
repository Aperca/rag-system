# Multimodal Retrieval-Augmented Generation (RAG) System

##  Overview
This project is a multimodal RAG system designed to bridge the gap between fragmented text and image-based datasets. By combining vector-based retrieval with Large Language Models (LLMs), the system provides context-aware, grounded responses for complex, data-dense environments.

Unlike standard RAG implementations, this assistant treats **images and text as first-class citizens**, allowing you to query research papers, diagrams, and unstructured documents in a single unified workflow.

## Motivation
In real-world settings, information is rarely tidy. It’s often locked away in PDFs, diagrams, and scattered documents. This project explores building AI systems that:
*   **Improve accessibility** in low-resource or high-noise environments.
*   **Reduce friction** in knowledge discovery.
*   **Support reliability** by grounding LLM responses in verifiable visual and textual evidence.

## Key Features
*   **Multimodal Embedding Space:** Maps text and images into a single high-dimensional vector space using **OpenCLIP (ViT-B-32)**.
*   **Persistent Vector Storage:** Uses **ChromaDB** to maintain a long-term knowledge base across sessions.
*   **Semantic Ingestion Pipeline:** Custom loaders for PDF text extraction (via `pypdf`) and automated image preprocessing.
*   **Resource Optimization:** Implements **Streamlit caching** to prevent redundant model loading and optimize memory usage.
*   **History-Aware Generation:** Maintains conversational context for iterative, deep-dive research questions.

##  Tech Stack
*   **Language:** Python 3.12
*   **Embeddings:** OpenCLIP (ViT-B-32)
*   **Inference Engine:** Ollama (Llama 3)
*   **Vector Database:** ChromaDB
*   **UI Framework:** Streamlit
*   **PDF Engine:** pypdf

---

## Project Structure
```text
rag-system/
├── data/                   # Raw documents (PDFs, Images)
├── vector_store/           # Persistent ChromaDB storage
├── ingestion/              
│   ├── loader.py           # Document/Image loading logic
│   ├── chunker.py          # Text splitting strategies
│   ├── embedder.py         # OpenCLIP integration
│   └── ingest_pipeline.py  # Orchestration of data flow
├── retrieval/              
│   └── retriever.py        # Vector similarity search logic
├── generation/             
│   └── generator.py        # Llama 3 prompt engineering
├── app.py                  # Streamlit UI
└── requirements.txt



## Installation

### 1. Prerequisites

Install Ollama and pull the required LLM:

``` bash
ollama pull llama3
```

### 2. Environment Setup

``` bash
# Clone the repository
git clone <repository-url>
cd rag-system

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Application

``` bash
streamlit run app.py
```

### Workflow

-   **Upload:** Use the input to upload PDFs, TXT files, or diagrams.\
-   **Process:** Click "Process Documents" to generate embeddings and
    save them.\
-   **Query:** Ask questions in the chat interface to retrieve and
    synthesize answers.
##  Design Focus
*   **Grounded outputs:** Responses are tied to retrieved context.
*   **Scalability:** Built on a vector-based retrieval architecture.
*   **Modality flexibility:** Seamlessly handles text and image data.

## Limitations
*   Retrieval quality depends heavily on embedding coverage.
*   Performance is sensitive to the structure of the dataset.
*   Not yet optimized for production-scale latency.

##  Future Improvements
*   **Reranking:** Implementing a reranking stage to improve retrieval precision.
*   **Multimodal Fusion:** Developing better strategies for combining image and text context.
*   **Evaluation:** Building a framework to measure response grounding quality.

##  What Makes This Project Different?
Unlike basic RAG tutorials, this system:
*   Works across multiple modalities (text + image).
*   Focuses on **structured retrieval**, not just generation.
*   Is designed with real-world information access constraints in mind.
