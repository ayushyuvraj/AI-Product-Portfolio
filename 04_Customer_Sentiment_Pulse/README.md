# 🗣️ Customer Voice Pulse (Open Source AI)

**A Sentiment Analysis Dashboard utilizing HuggingFace Transformers to detect churn risk in banking reviews.**

## 🚀 Overview
Unlike expensive API-based solutions (GPT-4), this project demonstrates the use of **DistilBERT** (an open-source, lightweight model) to perform local sentiment inference. This approach reduces privacy risk and operational costs to near zero.

## 🛠️ Tech Stack
* **Model:** `distilbert-base-uncased-finetuned-sst-2-english` (via HuggingFace).
* **Frontend:** Streamlit.
* **Data Processing:** Pandas & Matplotlib.

## ⚙️ Usage
```bash
pip install transformers torch streamlit
streamlit run app.py