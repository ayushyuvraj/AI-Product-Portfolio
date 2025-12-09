# 🏦 Financial Compliance Copilot (Enterprise RAG)

**[🟢 Live Demo](https://ayush-fintech-copilot.streamlit.app)** | **[📄 Project Architecture](#-technical-architecture)**

> **Status:** Production-Grade Product
> **Stack:** LangChain, OpenAI, FAISS, Streamlit, **Ragas (Custom Evals)**

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
    E --> F["🤖 LLM Inference (GPT-3.5)"]
    F --> G["✅ Final Answer"]
    G --> H["⚖️ The Trust Layer (Async Judge)"]