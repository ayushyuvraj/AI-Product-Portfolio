# 🏦 Fintech Compliance Copilot (RAG Pipeline)

**A Retrieval-Augmented Generation (RAG) tool designed to automate regulatory compliance queries for banking institutions.**

## 🚀 Overview
Bank Risk Managers often spend hours manually searching through dense PDF circulars (RBI/Fed guidelines) to find compliance answers. This tool solves that latency problem by allowing users to query documents using natural language, retrieving precise answers with source attribution.

This project demonstrates an end-to-end **ETL Pipeline** for unstructured financial data.

## 🛠️ Technical Architecture
* **Frontend:** Streamlit (Python) for rapid prototyping and secure user interaction.
* **Orchestration:** LangChain for managing the RAG workflow.
* **Embeddings:** OpenAI `text-embedding-3-small` for semantic vectorization.
* **Vector Database:** FAISS (Facebook AI Similarity Search) for high-speed local retrieval.
* **LLM:** GPT-3.5 Turbo with strict system prompting to act as a "Compliance Officer" (minimizing hallucinations).

## ✨ Key Features
1.  **Secure Ingestion:** Uploads generic PDFs and processes them locally in memory.
2.  **Semantic Search:** Uses vector embeddings to understand the *meaning* of a query, not just keywords.
3.  **Strict Context Windows:** Answers are generated *only* from the uploaded document to ensure regulatory accuracy.
4.  **Source Transparency:** (Optional) Displays the exact text chunks used to generate the answer.

## ⚙️ Setup & Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/fintech-compliance-rag.git](https://github.com/YOUR_USERNAME/fintech-compliance-rag.git)
    cd fintech-compliance-rag
    ```

2.  **Install Dependencies**
    ```bash
    pip install streamlit langchain langchain-openai faiss-cpu pypdf
    ```

3.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

## 📈 Future Roadmap
* **Multi-Document Support:** Ingesting multiple circulars simultaneously.
* **Hybrid Search:** Combining Keyword (BM25) and Semantic search for better precision.
* **Citation Highlighting:** Visual UI showing exact page numbers of the source text.

4.  **Quality Assurance**
    Implemented an automated evaluation pipeline using Ragas to track 'Faithfulness' and 'Answer Relevance' metrics, ensuring the model does not hallucinate regulatory facts.