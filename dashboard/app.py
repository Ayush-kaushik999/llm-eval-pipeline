import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="LLM Evaluation Benchmark Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Automated LLM Output Benchmark & Evaluation Pipeline")
st.markdown("Evaluate model responses, monitor latency, and track semantic faithfulness across test datasets.")

# --- Sidebar Configuration ---
st.sidebar.header("Configuration")
api_url = st.sidebar.text_input("FastAPI Endpoint", value="http://127.0.0.1:8000/evaluate/")
model_name = st.sidebar.selectbox(
    "Select Model to Benchmark",
    ["gemini-1.5-flash", "llama-3-8b-instruct", "gpt-3.5-turbo"]
)

# --- Main Workspace ---
st.subheader("📁 Upload Test Dataset")
uploaded_file = st.file_uploader("Upload a JSON test case file", type=["json"])

# Default sample test data if no file is uploaded
default_test_cases = [
    {
        "test_id": "test_001",
        "prompt": "Explain the concept of Reciprocal Rank Fusion in search systems.",
        "ground_truth": "RRF combines multiple result lists without score normalization.",
        "expected_keywords": ["Reciprocal Rank Fusion", "lists", "normalization"]
    },
    {
        "test_id": "test_002",
        "prompt": "What are the benefits of using Pydantic with FastAPI?",
        "ground_truth": "Pydantic provides runtime data validation and clear schema definition.",
        "expected_keywords": ["validation", "schema", "FastAPI"]
    }
]

test_cases_to_run = default_test_cases
if uploaded_file is not None:
    import json
    try:
        test_cases_to_run = json.load(uploaded_file)
        st.success(f"Successfully loaded {len(test_cases_to_run)} test cases from file.")
    except Exception as e:
        st.error(f"Error reading JSON file: {e}")

if st.button("🚀 Run Evaluation Pipeline", type="primary"):
    payload = {
        "model_name": model_name,
        "test_cases": test_cases_to_run
    }
    
    with st.spinner("Running evaluation pipeline and logging metrics..."):
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 201:
                data = response.json()
                st.success(f"Evaluation complete! Evaluated {data['total_evaluated']} test cases in {data['total_duration_seconds']}s.")
                
                # Convert results to DataFrame
                df = pd.DataFrame(data["results"])
                
                # --- Metrics Summary Cards ---
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Tests", len(df))
                col2.metric("Avg Latency", f"{df['latency_seconds'].mean():.3f} s")
                col3.metric("Avg Faithfulness", f"{df['faithfulness_score'].mean():.2f}")
                col4.metric("Avg Deterministic Score", f"{df['deterministic_score'].mean():.2f}")
                
                # --- Detailed Results Table ---
                st.subheader("📋 Evaluation Log Details")
                st.dataframe(df, use_container_width=True)
                
                # --- Visualizations ---
                st.subheader("📈 Performance Visualizations")
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    fig_latency = px.bar(df, x="test_id", y="latency_seconds", color="model_name", title="Latency per Test Case (seconds)")
                    st.plotly_chart(fig_latency, use_container_width=True)
                    
                with col_chart2:
                    fig_scores = px.bar(df, x="test_id", y=["deterministic_score", "faithfulness_score", "relevance_score"], barmode="group", title="Score Breakdown by Test ID")
                    st.plotly_chart(fig_scores, use_container_width=True)
                    
            else:
                st.error(f"API Error ({response.status_code}): {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server. Make sure Uvicorn is running on localhost:8000.")
            