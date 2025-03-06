import streamlit as st
import pandas as pd
import requests
import json
import os
import logging
import time
import matplotlib.pyplot as plt
from openai import OpenAI
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Ensure streamlit is installed
try:
    import streamlit as st
except ModuleNotFoundError:
    print("Error: The 'streamlit' module is not installed. Install it using 'pip install streamlit'.")
    exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load API Keys
openai_api_key = os.getenv("OPENAI_API_KEY", "")
clinical_trials_api = "https://clinicaltrials.gov/api/v2/studies"
epic_fhir_base_url = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/"

# Setup session for retries
session = requests.Session()
retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

def fetch_clinical_trials(gene, mutation):
    """Fetch relevant clinical trials from ClinicalTrials.gov API based on gene and mutation."""
    query = {
        "condition": "cancer",  # Searching trials related to cancer
        "term": f"{gene} {mutation}",  # Searching for specific gene mutation
        "status": "Recruiting",  # Only retrieving active recruiting trials
        "fields": "NCTId,BriefTitle,EligibilityCriteria,LocationCountry,Phase,LeadSponsorName"  # Fetching more trial details
    }
    try:
        response = session.get(clinical_trials_api, params=query)
        response.raise_for_status()
        trials = response.json()
        return trials.get("studies", [])  # Returning list of trials
    except requests.RequestException as e:
        logging.error(f"Clinical Trials API Error: {e}")
        return []

def fetch_beaker_reports(patient_id, auth_token):
    """Fetch Beaker pathology reports from Epic FHIR API using patient ID."""
    headers = {"Authorization": f"Bearer {auth_token}", "Accept": "application/fhir+json"}
    report_url = f"{epic_fhir_base_url}DiagnosticReport?patient={patient_id}"
    try:
        response = session.get(report_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Beaker API Error: {e}")
        return None

def plot_mutation_frequencies(df):
    """Plot mutation frequencies in genomic data."""
    plt.figure(figsize=(8, 4))
    df['Gene'].value_counts().plot(kind='bar', color='blue')
    plt.title("Gene Mutation Frequencies")
    plt.xlabel("Gene")
    plt.ylabel("Count")
    st.pyplot(plt)

def analyze_genomic_data(genomic_data, clinical_guidelines="NCCN"):
    """Enhanced Genomic AI Analysis Function using OpenAI for interpretation."""
    if not openai_api_key:
        st.error("🔑 OpenAI API Key is missing. Please provide a valid key.")
        return None
    client = OpenAI(api_key=openai_api_key)
    try:
        # Load genomic data from file or DataFrame
        if isinstance(genomic_data, str):
            df = pd.read_csv(genomic_data) if genomic_data.endswith('.csv') else pd.read_csv(genomic_data, sep='\t', comment='#')
        elif isinstance(genomic_data, pd.DataFrame):
            df = genomic_data
        else:
            raise ValueError("❌ Unsupported genomic data format")

        # Verify required columns
        required_cols = ['Gene', 'Mutation', 'Variant_Classification', 'Allele_Frequency']
        if not all(col in df.columns for col in required_cols):
            missing = [col for col in required_cols if col not in df.columns]
            raise ValueError(f"🚨 Missing required columns: {', '.join(missing)}")

        # Summarize genomic data for AI input
        genomic_summary = "\n".join(
            [f"- {row['Gene']} {row['Mutation']} ({row['Variant_Classification']}) - AF: {row['Allele_Frequency']}%"
             for _, row in df.iterrows()]
        )

        # Generate AI prompt for interpretation
        prompt = {
            "role": "user", "content": f"Analyze these genomic findings using {clinical_guidelines} guidelines: {genomic_summary}"
        }

        # Generate AI-based interpretation
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are an expert in precision oncology."}, prompt],
            response_format="json"
        )

        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Genomic Analysis Error: {str(e)}")
        return None

# Streamlit UI Integration for Genomic AI Analysis
if __name__ == "__main__":
    st.subheader("🧬 **AI-Driven Genomic Profiling Analysis**")
    
    uploaded_file = st.file_uploader("📂 **Upload Genomic Data (VCF/CSV)**", type=['vcf', 'csv'])
    guidelines = st.selectbox("📜 **Clinical Guidelines**", ["NCCN", "ESMO", "ASCO", "Custom"])
    patient_id = st.text_input("🆔 Enter Patient ID (for Beaker/Epic FHIR Integration)")
    auth_token = st.text_input("🔑 Enter Epic FHIR Auth Token", type="password")
    
    if uploaded_file:
        with st.spinner("🔍 **Analyzing genomic variants...**"):
            file_path = f"temp_{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            analysis = analyze_genomic_data(file_path, guidelines)
            trials = []
            
            if patient_id and auth_token:
                beaker_data = fetch_beaker_reports(patient_id, auth_token)
                st.subheader("📊 **Epic Beaker Pathology Report**")
                st.json(beaker_data)
            
            if analysis:
                st.subheader("🧪 **AI-Powered Genomic Report**")
                st.markdown(analysis)
                
                genes = pd.read_csv(file_path)['Gene'].unique()
                for gene in genes:
                    mutation = pd.read_csv(file_path).query("Gene == @gene")['Mutation'].values[0]
                    trials.extend(fetch_clinical_trials(gene, mutation))
                
                if trials:
                    st.subheader("🩺 **Matching Clinical Trials**")
                    for trial in trials:
                        st.markdown(f"🔹 **{trial['BriefTitle']}** (NCT{trial['NCTId']})")
                        st.markdown(f"🌎 Locations: {trial.get('LocationCountry', 'Unknown')}")
                        st.markdown(f"📜 Eligibility: {trial.get('EligibilityCriteria', 'N/A')}")
                        st.divider()
                st.download_button("📥 Download Report", data=analysis, file_name="genomic_analysis_report.md", mime="text/markdown")
