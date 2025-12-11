# 🏦 Financial Compliance Copilot (Enterprise RAG)

**[🟢 Live Demo](https://ayush-fintech-copilot.streamlit.app)** | **[📄 Project Architecture](#️-technical-architecture)**

> **Status:** Production-Grade PoC with Privacy-Preserving Audit Logs.
> **Stack:** Google Gemini 1.5 Flash, Streamlit, Python, **Custom Evals**

---

## 🚀 The Business Problem
Banks spend millions annually on manual KYC (Know Your Customer) verification. Human agents must manually inspect ID cards (PAN/Aadhaar) to check for:
1.  **Data Extraction:** Typing out names and numbers (slow, error-prone).
2.  **Liveness/Fraud:** Detecting photocopies, screen captures, or Photoshop tampering.

This project utilizes **Google's Multimodal Gemini 1.5 Flash** model to automate this visual audit in <2 seconds.

---

## 🏗️ Technical Architecture

The system implements a **"Privacy-First"** logging architecture. It processes the image for verification but **does not store PII (images)**. Instead, it logs the **AI's Reasoning Trace** for audit purposes.

```mermaid
graph TD
    A["User Uploads ID"] --> B{"🛡️ Safety Guardrails"}
    B -- Unsafe/Non-ID --> C["Block Request & Log Event"]
    B -- Safe --> D["⚡ Gemini 2.5 Vision"]
    D --> E{"📝 Multimodal Inference"}
    E --> F["Extract Data & Check Fraud"]
    F --> G["✅ User Verdict"]
    F --> H["📝 Log Reasoning Trace (CSV)"]
    H --> I["⚖️ Async Logic Audit"]```


### 1. The Vision Engine
* **Zero-Shot Extraction**: No OCR templates required. Generalizes across PAN, Aadhaar, and DLs.
* **Fraud Markers**: Detects "Screen Glare" (screen capture) and "Photocopy Grain" (non-original).

### 2. The Safety Layer (Guardrails)
Before retrieval, every image passes through a Pre-Extraction Check:
* **Intent Classification**: Detects unsafe/unacceptable images (e.g., not an Id Card, Explicit content etc.).
* **Scope Enforcement**: Blocks Images unrelated to Id Cards 
* **Outcome**: A Pre-Computation check that rejects images before they hit the expensive extraction logic.

### 3. The Trust Layer (Logic Audit)
Since we cannot store sensitive ID images for re-evaluation, we implement a Consistency Audit:
* **The Logger**: Saves the Verdict (Approved/Rejected) and the Reasoning ("Blurry text detected") to a secure log.
* **The Auditor**: A separate process reads these text logs to check for logical contradictions (e.g., Verdict: Approved but Reason: Image is blurry).

## ⚙️ How to Run Locally

### 1. Clone the Repository
``` 
git clone [https://github.com/ayushyuvraj/AI-Product-Portfolio.git](https://github.com/ayushyuvraj/AI-Product-Portfolio.git)
cd 07_Gemini_Vision_KYC
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Run the Application
```
streamlit run app.py
```

### 4. Run the Trust Layer (Evaluation)
```
python evaluate_vision.py
# Audits the log file for logical inconsistencies without needing the original images.
```