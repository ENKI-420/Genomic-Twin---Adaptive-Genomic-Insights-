import streamlit as st
import requests
import pandas as pd
import os
from openai import OpenAI
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from modules.genomics_analysis import perform_genomic_analysis



# Load environment variables
load_dotenv()

# Constants
FHIR_BASE_URL = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/"
OAUTH_URL = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
GENOMIC_API_URL = "https://genomic-api-url.com/analyze"

# Load OpenAI API Key from .env
openai_api_key = os.getenv("OPENAI_API_KEY", "")

# Setup session for retries
session = requests.Session()
retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

# Sidebar Configuration for Advanced Genomic Analysis
with st.sidebar:
    st.header("🧬 Advanced Genomic Analysis")

    # Navigation menu
    st.subheader("📌 Genomic Analysis Options")
    menu_options = [
        "Upload Genomic Data",
        "Review Mutations",
        "Treatment Predictions",
        "Clinical Trials Matching"
    ]
    selected_option = st.radio("Select an analysis module:", menu_options)

    # OpenAI API Key input (preloaded from .env but allows manual override)
    st.subheader("🔑 OpenAI API Key")
    openai_api_key = st.text_input("Enter your OpenAI API Key", value=openai_api_key, type="password")

    # Quick Links for Genomic Databases
    st.subheader("🔗 Genomic Databases")
    st.markdown("[COSMIC Database](https://cancer.sanger.ac.uk/cosmic)")
    st.markdown("[ClinVar Database](https://www.ncbi.nlm.nih.gov/clinvar/)")

# Display selected module
st.title(f"🚀 {selected_option}")
st.caption("AI-driven genomic analysis for precision medicine.")

# Perform Genomic Data Upload & Analysis
def perform_genomic_data_analysis(genomic_data):
    try:
        response = session.post(GENOMIC_API_URL, json={"genomic_data": genomic_data})
        response.raise_for_status()
        return response.json()  # Returning mutation analysis results
    except requests.exceptions.RequestException as e:
        st.error(f"Genomic analysis failed: {e}")
        return None

# Auto-Enhanced Genomic Insights
def generate_genomic_insights(mutated_genes):
    client = OpenAI(api_key=openai_api_key)
    prompt = f"Analyze the following mutated genes and suggest possible oncogenic implications and treatments:\n{mutated_genes}"
    response = client.completions.create(model="gpt-4-turbo", prompt=prompt, max_tokens=500)
    return response.choices[0].text.strip()

# Display & Navigate Through Genomic Results
st.subheader("🧬 Upload and Analyze Genomic Data")
genomic_data = st.file_uploader("Upload your genomic sequencing file (e.g., VCF, JSON)", type=["vcf", "json"])
if genomic_data:
    # Perform genomic data analysis (using a hypothetical function or API)
    genomic_analysis_results = perform_genomic_data_analysis(genomic_data)
    if genomic_analysis_results:
        st.write("### Genomic Mutation Results")
        st.json(genomic_analysis_results)  # Show results as JSON
        mutated_genes = genomic_analysis_results.get("mutated_genes", [])
        
        st.write("### 🤖 AI-Powered Genomic Insights")
        ai_response = generate_genomic_insights(mutated_genes)
        if ai_response:
            st.write(ai_response)

        # Recursively provide context-aware options
        st.subheader("🔍 Next Steps")
        options = [
            "[A] → Refine Mutation Analysis",
            "[B] → Suggest Treatment Options",
            "[C] → Search Clinical Trials for Mutation",
            "[D] → Visualize Genomic Data"
        ]
        selected_action = st.radio("What would you like to do next?", options)
        
        if selected_action == "[A] → Refine Mutation Analysis":
            st.write("Refining mutation analysis using additional databases.")
            # Integrate enhanced genomic analysis, like cross-referencing with ClinVar, COSMIC, etc.
        
        elif selected_action == "[B] → Suggest Treatment Options":
            st.write("Generating personalized treatment options based on mutations.")
            # Implement treatment suggestions based on genomic analysis
        
        elif selected_action == "[C] → Search Clinical Trials for Mutation":
            st.write("Searching clinical trials matching your mutation.")
            # Integrate with trial APIs to find relevant trials
        
        elif selected_action == "[D] → Visualize Genomic Data":
            st.write("Visualizing genomic data with charts and graphs.")
            # Use matplotlib/plotly to show data visually

st.caption("🔗 Powered by Agile Defense Systems | Norton Oncology | AI-Driven Precision Medicine | Epic EHR Integration")
