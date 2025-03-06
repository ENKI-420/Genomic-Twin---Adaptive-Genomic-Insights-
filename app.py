import streamlit as st
import os
from dotenv import load_dotenv
from modules.genomic_ai import analyze_genomic_data
from modules.beaker_report import fetch_beaker_reports
from modules.clinical_trials import match_clinical_trials
from modules.export_data import generate_reports
from modules.utils import authenticate_epic, fetch_patient_data
from modules.chatbot import ai_chat_response

# Load environment variables
load_dotenv()

# Constants
APP_VERSION = "v3.0"

# Streamlit UI
st.title("🚀 Agile Oncology AI Platform")
st.caption("Precision Medicine Platform v2.6 | Powered by EPIC EHR")

# Sidebar UI
with st.sidebar:
    st.header("🧬 Agile Oncology AI")
    analysis_mode = st.radio("Select Analysis Mode", ["Genomic Analysis", "Beaker Reports", "Clinical Trial Matching", "AI Chatbot"])

    st.subheader("🔑 Epic EHR Authentication")
    username = st.text_input("Epic Username")
    password = st.text_input("Epic Password", type="password")
    if st.button("Login to Epic"):
        token = authenticate_epic(username, password)
        if token:
            st.session_state['token'] = token
            st.success("Authenticated with Epic!")
        else:
            st.error("Authentication failed.")

# Main UI logic
if 'token' in st.session_state:
    patient_id = st.text_input("Enter Patient ID")

    if analysis_mode == "Genomic Analysis":
        uploaded_file = st.file_uploader("Upload Genomic File (VCF/JSON)")
        if uploaded_file and st.button("Analyze Genomics 🚀"):
            mutations = analyze_genomic_data(uploaded_file)
            patient_data = fetch_patient_data(patient_id, st.session_state['token'])
            st.dataframe(mutations)
            analyze_genomic_data.plot_mutation_data(mutations)
            generate_reports(mutations, patient_data)
            st.success("Reports Generated: PDF & DOCX")

    elif analysis_mode == "Beaker Reports":
        if st.button("Fetch Beaker Reports"):
            reports = fetch_beaker_reports(patient_id, st.session_state['token'])
            st.dataframe(reports)

    elif analysis_mode == "Clinical Trial Matching":
        mutations_input = st.text_input("Enter mutations (comma-separated)")
        if st.button("Find Matching Trials"):
            mutations = mutations_input.split(',')
            trials = match_clinical_trials(mutations)
            st.json(trials)

    elif analysis_mode == "AI Chatbot":
        user_query = st.text_area("Ask AIDEN Oncology Chatbot")
        if st.button("Get AI Response"):
            response = ai_chat_response(user_query)
            st.write(response)

else:
    st.info("Please authenticate via the sidebar to start using the platform.")

st.caption("🔬 Agile Oncology AI | Powered by EPIC EHR | Secure & HIPAA-compliant")
