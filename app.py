import streamlit as st
import requests
import os
from openai import OpenAI
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
GENOMIC_API_URL = "https://genomic-api-url.com/analyze"
CLINVAR_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
COSMIC_API_URL = "https://cancer.sanger.ac.uk/cosmic/api/v1"

# Load API keys
openai_api_key = os.getenv("OPENAI_API_KEY", "")
cosmic_api_key = os.getenv("COSMIC_API_KEY", "")

# Setup session for retries
session = requests.Session()
retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

# Sidebar Configuration
with st.sidebar:
    st.header("🧬 Advanced Genomic Analysis")
    menu_options = [
        "Upload Genomic Data",
        "Review Mutations",
        "Treatment Predictions",
        "Clinical Trials Matching"
    ]
    selected_option = st.radio("Select an analysis module:", menu_options)
    st.subheader("🔑 API Keys")
    openai_api_key = st.text_input("OpenAI API Key", value=openai_api_key, type="password")
    cosmic_api_key = st.text_input("COSMIC API Key", value=cosmic_api_key, type="password")

# Main Interface
st.title(f"🚀 {selected_option}")
st.caption("AI-driven genomic analysis for precision medicine.")

# Genomic Analysis Functions
def perform_genomic_data_analysis(genomic_data):
    try:
        response = session.post(
            GENOMIC_API_URL,
            json={"genomic_data": genomic_data.getvalue()},
            timeout=30
        )
        response.raise_for_status()
        analysis_results = response.json()
        analysis_results["clinvar"] = cross_reference_clinvar(analysis_results)
        analysis_results["cosmic"] = cross_reference_cosmic(analysis_results)
        return analysis_results
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        return None

def cross_reference_clinvar(analysis_results):
    clinvar_data = {}
    try:
        for gene in analysis_results.get("mutated_genes", []):
            params = {
                "db": "clinvar",
                "term": f"{gene}[gene]+AND+human[organism]",
                "retmode": "json"
            }
            response = session.get(CLINVAR_API_URL, params=params, timeout=15)
            response.raise_for_status()
            clinvar_data[gene] = response.json().get("esearchresult", {})
    except Exception as e:
        st.error(f"ClinVar lookup failed: {str(e)}")
    return clinvar_data

def cross_reference_cosmic(analysis_results):
    cosmic_data = {}
    if not cosmic_api_key:
        st.error("COSMIC API key required")
        return cosmic_data
    try:
        for gene in analysis_results.get("mutated_genes", []):
            headers = {"Authorization": f"Bearer {cosmic_api_key}"}
            response = session.get(
                f"{COSMIC_API_URL}/gene/{gene}",
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            cosmic_data[gene] = response.json()
    except Exception as e:
        st.error(f"COSMIC lookup failed: {str(e)}")
    return cosmic_data

def generate_genomic_insights(mutated_genes):
    client = OpenAI(api_key=openai_api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{
                "role": "user",
                "content": f"Analyze these mutated genes and suggest oncogenic implications and treatments based on ClinVar/COSMIC data:\n{mutated_genes}"
            }],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Insight generation failed: {str(e)}"

# Main Application Flow
st.subheader("🧬 Upload and Analyze Genomic Data")
uploaded_file = st.file_uploader("Upload genomic file (VCF, JSON)", type=["vcf", "json"])

if uploaded_file:
    analysis_results = perform_genomic_data_analysis(uploaded_file)
    
    if analysis_results:
        st.subheader("Analysis Results")
        with st.expander("Raw Data"):
            st.json(analysis_results)

        mutated_genes = analysis_results.get("mutated_genes", [])
        if mutated_genes:
            st.subheader("AI-Generated Insights")
            insights = generate_genomic_insights(mutated_genes)
            st.write(insights)

            st.subheader("🔍 Next Steps")
            action = st.radio("Choose action:", [
                "Refine Mutation Analysis",
                "View Treatment Options",
                "Find Clinical Trials",
                "Visualize Genomic Data"
            ])

            if action == "View Treatment Options":
                treatments = analysis_results.get("clinvar", {}).get("treatment_recommendations", [])
                st.write("### Targeted Treatment Options")
                st.table(pd.DataFrame(treatments))

        st.subheader("Database Cross-References")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**ClinVar Data**")
            st.write(analysis_results.get("clinvar", {}))
        with col2:
            st.write("**COSMIC Data**")
            st.write(analysis_results.get("cosmic", {}))

st.caption("🔗 Powered by Advanced Genomic Analytics | Real-time Database Integration")
