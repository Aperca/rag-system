# Multimodal RAG Research Assistant

## Overview

This project implements a Multimodal Retrieval-Augmented Generation
(RAG) system designed for analyzing heterogeneous research datasets. The
system enables unified querying across text documents (PDF, TXT) and
visual data (PNG, JPG).

By leveraging **OpenCLIP (ViT-B-32)** for cross-modal vector embeddings
and **Llama 3** for natural language synthesis, the assistant provides
context-grounded answers derived from both textual descriptions and
visual evidence.

## Key Features

-   **Multimodal Embedding Space:** Maps text and images into a single
    high-dimensional vector space using CLIP.
-   **Persistent Vector Storage:** Uses ChromaDB's `PersistentClient` to
    maintain a long-term knowledge base across sessions.
-   **Semantic Ingestion Pipeline:** Includes custom loaders for PDF
    text extraction (via `pypdf`) and image preprocessing.
-   **Resource Optimization:** Implements Streamlit caching
    (`@st.cache_resource`) to prevent redundant model loading and memory
    leaks.
-   **History-Aware Generation:** Maintains conversational context for
    iterative research questions.

## Project Structure

``` text
rag-system/
├── data/                   
├── vector_store/           
├── ingestion/              
│   ├── loader.py           
│   ├── chunker.py          
│   ├── embedder.py         
│   └── ingest_pipeline.py  
├── retrieval/              
│   └── retriever.py        
├── generation/             
│   └── generator.py        
├── models/                 
│   └── embedding_model.py  
├── app.py                  
└── requirements.txt        
```

## Technical Stack

-   Language: Python 3.12\
-   Vision-Language Model: OpenCLIP (ViT-B-32/OpenAI)\
-   Inference Engine: Ollama (Llama 3)\
-   Vector Database: ChromaDB\
-   UI Framework: Streamlit\
-   PDF Engine: pypdf

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
