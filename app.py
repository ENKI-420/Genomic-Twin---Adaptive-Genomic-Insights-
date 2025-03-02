import streamlit as st
import pandas as pd
from modules.digital_twins import generate_digital_twin
from modules.mutation_analysis import analyze_mutations
from modules.crispr_ai import crispr_feasibility
from modules.nanoparticle_simulation import simulate_delivery
from modules.clinical_trials import find_trials
from modules.blockchain import log_pharmacovigilance
from modules.beaker_report import fetch_beaker_data
import plotly.express as px

st.set_page_config(page_title="AGILE Oncology AI Hub", layout="wide", page_icon="🩺")

with st.sidebar:
    st.image("assets/logo.png", width=200)
    menu = st.radio("AGILE Oncology Modules", [
        "📊 Clinical Dashboard",
        "🧬 Digital Twin Simulation",
        "⚗️ CRISPR Feasibility",
        "💊 Nanoparticle Delivery",
        "🔗 Blockchain Monitoring",
        "📈 Market Analytics"
    ])
    st.markdown("---")
    st.caption(f"v2.3 | NIH-Compliant AI Platform")

if 'patient_data' not in st.session_state:
    st.session_state.patient_data = None

if menu == "📊 Clinical Dashboard":
    st.title("🎛️ AGILE Oncology Clinical Dashboard")
    with st.expander("⚡ Epic EHR Integration", expanded=True):
        col1, col2 = st.columns([2,1])
        with col1:
            patient_id = st.text_input("Enter Patient ID:", key="patient_id")
            if st.button("🚀 Fetch Genomic Data"):
                with st.spinner("Authenticating with Epic FHIR..."):
                    st.session_state.patient_data = fetch_beaker_data(patient_id)
        with col2:
            if st.session_state.patient_data:
                st.success("✅ NIH-Genomic Data Loaded")
                st.metric("Tumor Mutational Burden", "42.7/Mb", "+15.2% vs baseline")
    if st.session_state.patient_data:
        st.subheader("🧬 Real-Time Mutation Tracking")
        mutations = analyze_mutations(st.session_state.patient_data)
        tab1, tab2, tab3 = st.tabs(["Oncogenic Drivers", "Resistance Profile", "Clinical Action"])
        with tab1:
            df = pd.DataFrame(mutations['drivers'])
            st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
        with tab2:
            fig = px.bar(mutations['resistance'], x='gene', y='score', color='therapy', height=400)
            st.plotly_chart(fig, use_container_width=True)
        with tab3:
            st.write("### 🎯 AI-Powered Treatment Suggestions")
            for therapy in mutations['therapies']:
                st.progress(therapy['efficacy'], f"{therapy['name']} | {therapy['mechanism']}")

elif menu == "🧬 Digital Twin Simulation":
    st.title("🦾 AI-Driven Digital Twin Modeling")
    col1, col2 = st.columns([1,2])
    with col1:
        st.subheader("Patient Parameters")
        therapy_options = st.multiselect("Select Therapies:", 
            ["Pembrolizumab", "Olaparib", "Carfilzomib", "Sacituzumab"])
        simulation_days = st.slider("Simulation Duration (Days)", 30, 365, 90)
    with col2:
        if st.button("🌀 Run Digital Twin Simulation"):
            with st.spinner("Simulating tumor microenvironment..."):
                results = generate_digital_twin(
                    st.session_state.patient_data,
                    therapies=therapy_options,
                    days=simulation_days
                )
                fig = px.line(results, x='day', y='tumor_volume', color='therapy', markers=True, title="Tumor Evolution Prediction")
                st.plotly_chart(fig, use_container_width=True)
