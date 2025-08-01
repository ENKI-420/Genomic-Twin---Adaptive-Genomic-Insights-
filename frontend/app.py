import streamlit as st
from dotenv import load_dotenv
from modules.genomic_ai_module import analyze_genomic_data, plot_mutation_data, ai_genomic_interpretation, generate_reports
from modules.beaker_report import fetch_beaker_data
from modules.clinical_trials import find_trials
from modules.utils import authenticate_epic, fetch_patient_data, ai_chat_response
from modules.digital_twin import generate_digital_twin
from modules.tokenomics_dashboard import tokenomics_dashboard

# Load environment variables
load_dotenv()

# Constants
APP_VERSION = "v3.3"

# Streamlit UI
st.title("🚀 DNA-Lang Autonomous Bio-Digital Platform")
st.caption(f"Precision Medicine & Autonomous DeFi Platform {APP_VERSION}")

# Sidebar UI
with st.sidebar:
    st.header("🧬 DNA-Lang Platform")
    analysis_mode = st.radio("Select Module", [
        "Genomic Analysis", 
        "Beaker Reports", 
        "Clinical Trial Matching", 
        "AI Chatbot",
        "Tokenomics Dashboard"
    ])

    if analysis_mode not in ["Tokenomics Dashboard"]:
        st.subheader("🔑 Epic EHR Authentication")
        username = st.text_input("Epic Username")
        password = st.text_input("Epic Password", type="password")
        if st.button("Login"):
            token = authenticate_epic(username, password)
            if token:
                st.session_state['token'] = token
                st.success("Authenticated with Epic!")
            else:
                st.error("Authentication failed.")

# Main UI logic
if analysis_mode == "Tokenomics Dashboard":
    tokenomics_dashboard()
elif 'token' in st.session_state or analysis_mode in ["AI Chatbot"]:
    if analysis_mode != "AI Chatbot":
        patient_id = st.text_input("Enter Patient ID")

    if analysis_mode == "Genomic Analysis":
        uploaded_file = st.file_uploader("Upload Genomic File (VCF/CSV)")
        report_format = st.selectbox("Report Format", ["PDF", "DOCX"])

        if uploaded_file and st.button("Analyze Genomics 🚀"):
            mutations_df = analyze_genomic_data(uploaded_file)
            patient_data = fetch_patient_data(patient_id, st.session_state['token'])
            ai_insights = ai_genomic_interpretation(mutations_df)
            digital_twin = generate_digital_twin(patient_data)

            st.dataframe(mutations_df)
            plot_mutation_data(mutations_df)
            report_path = generate_reports(mutations_df, patient_data, insights=ai_insights, format_type=report_format)

            with open(report_path, "rb") as file:
                st.download_button("Download Report", file_name=report_path, data=file, mime="application/octet-stream")
            st.success("Reports Generated Successfully!")

    elif analysis_mode == "Beaker Reports":
        if st.button("Fetch Beaker Reports"):
            reports = fetch_beaker_data(patient_id, st.session_state['token'])
            st.dataframe(reports)

    elif analysis_mode == "Clinical Trial Matching":
        mutations_input = st.text_input("Enter mutations (comma-separated)")
        if st.button("Find Matching Trials"):
            mutations = mutations_input.split(',')
            trials = find_trials(mutations)
            st.json(trials)

    elif analysis_mode == "AI Chatbot":
        user_query = st.text_area("Ask DNA-Lang AI")
        if st.button("Get AI Response"):
            response = ai_chat_response(user_query)
            st.write(response)

else:
    st.info("Please authenticate via the sidebar to start using the genomic platform.")

st.caption("🔬 DNA-Lang Autonomous Platform | Powered by EPIC EHR & Autonomous Evolution | Secure & HIPAA-compliant")
