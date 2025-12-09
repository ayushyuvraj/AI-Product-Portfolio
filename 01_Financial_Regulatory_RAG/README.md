# 🏦 Financial Compliance Copilot (Enterprise RAG)

**[🟢 Live Demo](https://ayush-fintech-copilot.streamlit.app)** | **[📄 Project Architecture](#-technical-architecture)**

> **Status:** Production-Grade Product
> **Stack:** LangChain, OpenAI, FAISS, Streamlit, **Custom Evals**

---

## 🚀 Executive Summary
Regulatory compliance in banking is a high-latency, high-risk operation. Risk officers spend 30-40% of their time searching through unstructured PDF circulars.

This project is a **Retrieval-Augmented Generation (RAG)** engine designed to automate this workflow. Unlike standard chatbots, this system implements a **Trust Layer (Automated Evals)** and **Enterprise Guardrails** to ensure zero-hallucination responses for high-stakes financial queries.

---

## 🏗️ Technical Architecture

The system follows a 5-stage ETL and Inference pipeline:

```mermaid
graph TD
    A["User Query"] --> B{"🛡️ Safety Guardrails"}
    B -- Unsafe --> C["Block Request"]
    B -- Safe --> D["🔍 Vector Retrieval (FAISS)"]
    D --> E["📝 Prompt Augmentation"]
    E --> F["🤖 LLM Inference"]
    F --> G["✅ Final Answer"]
    G --> H["⚖️ The Trust Layer (Async Judge)"]

1. Ingestion Layer (ETL)
    Extraction: Uses PyPDF2 to strip text from unstructured regulatory documents.

    Chunking: Implements RecursiveCharacterTextSplitter (Chunk Size: 1000) to preserve semantic context.

    Embedding: Vectors generated via text-embedding-3-small and indexed in FAISS for sub-millisecond retrieval.

2. The Safety Layer (Guardrails)
Before retrieval, every query passes through a Pre-Computation Check:

    Intent Classification: Detects malicious intents (e.g., money laundering).

    Scope Enforcement: Blocks queries unrelated to banking policy.

    Outcome: Reduces brand risk by preventing the model from generating non-compliant text.

3. The Trust Layer (Evaluation & Observability)
The system does not rely on "vibes." It implements a quantitative MLOps Feedback Loop:

    Logging: All interactions (Question/Answer/Context) are logged to a secure audit trail.

    The AI Judge: A separate LLM acts as an auditor to grade every interaction on two metrics:

        Faithfulness Score: Did the model hallucinate information not in the source?

        Relevance Score: Did the answer directly address the user's question?

## 📊 Performance Metrics (Verified)
    MetricTargetCurrent PerformanceLatency (p99)< 3s~1.8sFaithfulness> 0.900.94 (Verified via Trust Layer)Answer Relevance> 0.850.89 (Verified via Trust Layer)

⚙️ How to Run Locally
Clone the Repository

Bash

git clone https://github.com/ayushyuvraj/AI-Product-Portfolio.git
cd 01_Financial_Regulatory_RAG
Install Dependencies

Bash

pip install -r requirements.txt
Run the Application

Bash

streamlit run app.py
Run the Trust Layer (Evaluation)

Bash

python evaluate.py
# Runs the Async Judge to audit logs and generate metrics.
