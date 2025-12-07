import streamlit as st
import pandas as pd
from transformers import pipeline
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Customer Voice AI", page_icon="🗣️")

st.title("🗣️ Customer Voice Pulse")
st.markdown("Analyze customer reviews using Open Source AI (HuggingFace) to detect churn risk.")

# --- 1. LOAD DATA ---
uploaded_file = st.file_uploader("Upload Reviews (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Raw Data Preview")
    st.dataframe(df.head())
    
    if st.button("Analyze Sentiment"):
        with st.spinner("Downloading Model & Analyzing... (This uses your CPU)"):
            
            # --- 2. AI ENGINE (HuggingFace) ---
            # We use a 'distilbert' model which is fast and free
            sentiment_pipeline = pipeline("sentiment-analysis")
            
            # Apply AI to every row
            def analyze(text):
                result = sentiment_pipeline(text)[0]
                return result['label'] # RETURNS 'POSITIVE' or 'NEGATIVE'
            
            df['Sentiment'] = df['Review'].apply(analyze)
            
            st.success("Analysis Complete!")
            
            # --- 3. DASHBOARD ---
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Sentiment Breakdown")
                counts = df['Sentiment'].value_counts()
                st.bar_chart(counts)
            
            with col2:
                st.subheader("Critical Alerts (Negative)")
                negatives = df[df['Sentiment'] == 'NEGATIVE']
                st.write(f"Found {len(negatives)} negative reviews.")
                st.dataframe(negatives[['Review']])

else:
    st.info("Please upload a CSV file to begin.")