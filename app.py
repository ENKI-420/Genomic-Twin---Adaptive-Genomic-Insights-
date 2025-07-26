import streamlit as st
from dotenv import load_dotenv
import sys
import os

# Add current directory to path to avoid __init__.py issues
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import only working modules directly
try:
    # Import these carefully to avoid dependency issues
    from modules.genomic_ai_module import analyze_genomic_data, plot_mutation_data, ai_genomic_interpretation, generate_reports
    from modules.beaker_report import fetch_beaker_data
    from modules.clinical_trials import find_trials
    from modules.utils import authenticate_epic, fetch_patient_data, ai_chat_response
    from modules.digital_twin import generate_digital_twin
    GENOMIC_MODULES_AVAILABLE = True
except ImportError as e:
    GENOMIC_MODULES_AVAILABLE = False
    print(f"Note: Some genomic modules not available: {e}")

# Import new strategic modules directly
try:
    from simple_strategic_dashboard import render_strategic_dashboard
    STRATEGIC_DASHBOARD_AVAILABLE = True
except ImportError as e:
    STRATEGIC_DASHBOARD_AVAILABLE = False
    print(f"Strategic dashboard not available: {e}")

# Load environment variables
load_dotenv()

# Constants
APP_VERSION = "v4.0"

# Configure page
st.set_page_config(
    page_title="DNA-Lang Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Streamlit UI
st.title("🧬 DNA-Lang Digital Organism Platform")
st.caption("Advanced Genomic AI & Market Penetration Platform v4.0")

# Sidebar UI
with st.sidebar:
    st.header("🧬 DNA-Lang Platform")
    
    # Main navigation
    platform_mode = st.selectbox(
        "Platform Mode",
        ["Genomic Analysis", "Strategic Dashboard", "Marketplace", "Developer Portal", "Compliance Center"]
    )
    
    st.markdown("---")
    
    # Secondary navigation based on platform mode
    if platform_mode == "Genomic Analysis":
        analysis_mode = st.radio("Analysis Type", ["Genomic Analysis", "Beaker Reports", "Clinical Trial Matching", "AI Chatbot"])
    elif platform_mode == "Strategic Dashboard":
        st.info("📊 Comprehensive market penetration analytics")
    elif platform_mode == "Marketplace":
        st.info("🛒 Digital organism marketplace")
    elif platform_mode == "Developer Portal":
        st.info("⚡ SDK, documentation, and community")
    elif platform_mode == "Compliance Center":
        st.info("🔒 Compliance, security, and governance")

    
    # Authentication section (for genomic analysis)
    if platform_mode == "Genomic Analysis":
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

# Main content area
if platform_mode == "Strategic Dashboard" and STRATEGIC_DASHBOARD_AVAILABLE:
    render_strategic_dashboard()
elif platform_mode == "Strategic Dashboard":
    st.error("Strategic Dashboard module is not available due to missing dependencies.")
    st.markdown("## Strategic Market Penetration Overview")
    st.markdown("""
    ### 🎯 Market Segmentation & Targeting
    - **5 Target Verticals**: Biotech, Cloud Infrastructure, AI Research, Financial Services, IoT Manufacturing
    - **6 Global Regions**: US, EU, Singapore, Japan, Canada, and emerging markets
    - **Regional Strategy**: Tier 1 focus on mature markets with high compliance requirements
    
    ### 🤝 Partner Ecosystem
    - **Cloud Provider Integrations**: AWS, Azure, GCP marketplace distribution
    - **System Integrator Partnerships**: Accenture, Deloitte, regional consultants
    - **Co-branded Launches**: Joint go-to-market with major cloud providers
    
    ### 🛒 Digital Organism Marketplace
    - **Organism Categories**: 5 major categories covering all target verticals
    - **Bounty System**: Gene bounties for collaborative development
    - **Monetization**: 5% marketplace fee + premium listing options
    
    ### ⚡ Developer Engagement
    - **SDK Components**: Core library, CLI tools, API client, templates
    - **Community Events**: Hackathons, webinars, workshops, conferences
    - **Quickstart Guides**: Vertical-specific onboarding paths
    
    ### 💰 Commercialization Strategy
    - **SaaS Packages**: Free, Basic ($49), Professional ($199), Enterprise ($999), Research ($25)
    - **Certification Programs**: Foundation ($99), Professional ($299), Expert ($499)
    - **Revenue Optimization**: Value-based pricing, mid-tier packages, premium services
    
    ### 🔒 Compliance & Governance
    - **Framework Support**: GDPR, HIPAA, SOC2, ISO 27001, NIST, FDA 21 CFR 11
    - **Security Audits**: Regular third-party assessments and vulnerability scans
    - **Governance Policies**: Data governance, security policies, marketplace governance
    """)

elif platform_mode == "Marketplace":
    try:
        from modules.marketplace import get_marketplace_instance
        
        st.header("🛒 Digital Organism Marketplace")
        
        marketplace = get_marketplace_instance()
        analytics = marketplace.get_marketplace_analytics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Organisms", analytics["total_organisms"])
        with col2:
            st.metric("Total Transactions", analytics["total_transactions"])
        with col3:
            st.metric("Total Revenue", f"${analytics['total_revenue']}")
        with col4:
            st.metric("Fees Collected", f"${analytics['total_fees_collected']}")
        
        st.subheader("Search Organisms")
        search_query = st.text_input("Search organisms...")
        category_filter = st.selectbox("Category", ["", "biotech_organisms", "cloud_infrastructure", "ai_research"])
        
        if st.button("Search"):
            results = marketplace.search_organisms(query=search_query, category=category_filter)
            if results:
                st.dataframe(results)
            else:
                st.info("No organisms found matching your criteria.")
    except ImportError as e:
        st.error(f"Marketplace module not available: {e}")

elif platform_mode == "Developer Portal":
    try:
        from modules.developer_sdk import get_sdk_instance
        
        st.header("⚡ DNA-Lang Developer Portal")
        
        sdk = get_sdk_instance()
        
        tab1, tab2, tab3 = st.tabs(["📦 SDK Packages", "📚 Quickstart Guides", "🎉 Events"])
        
        with tab1:
            st.subheader("Available SDK Packages")
            packages = sdk.search_packages()
            for package in packages:
                with st.expander(package["name"]):
                    st.write(package["description"])
                    st.code(package["installation_command"])
                    st.write(f"License: {package['license']}")
                    st.write(f"GitHub: {package['github_repo']}")
        
        with tab2:
            st.subheader("Quickstart Guides")
            guide_type = st.selectbox("Select Guide", ["biotech-quickstart", "cloud-quickstart"])
            guide = sdk.get_quickstart_guide(guide_type)
            if guide:
                st.markdown(f"### {guide['title']}")
                st.write(guide["description"])
                st.write(f"Duration: {guide['duration_minutes']} minutes")
                
                st.markdown("#### Prerequisites")
                for prereq in guide["prerequisites"]:
                    st.write(f"- {prereq}")
        
        with tab3:
            st.subheader("Developer Events")
            metrics = sdk.get_community_engagement_metrics()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Events", metrics["total_events"])
            with col2:
                st.metric("Upcoming Events", metrics["upcoming_events"])
            with col3:
                st.metric("Total Participants", metrics["total_event_participants"])
    except ImportError as e:
        st.error(f"Developer SDK module not available: {e}")

elif platform_mode == "Compliance Center":
    try:
        from modules.compliance_governance import get_compliance_engine
        
        st.header("🔒 Compliance & Governance Center")
        
        compliance = get_compliance_engine()
        
        tab1, tab2, tab3 = st.tabs(["📊 Compliance Dashboard", "🛡️ Security Audits", "📋 Governance Policies"])
        
        with tab1:
            st.subheader("Compliance Status")
            compliance_status = compliance.assess_compliance_status()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Compliance Score", f"{compliance_status['compliance_score']}%")
            with col2:
                st.metric("Total Requirements", compliance_status["total_requirements"])
            with col3:
                st.metric("Compliant Requirements", compliance_status["compliant_requirements"])
            with col4:
                st.metric("Critical Issues", compliance_status["critical_issues"])
            
            if compliance_status["assessment_schedule"]:
                st.subheader("Upcoming Assessments")
                st.dataframe(compliance_status["assessment_schedule"])
        
        with tab2:
            st.subheader("Security Audits")
            dashboard = compliance.get_governance_dashboard()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Audits in Progress", dashboard["security_audits_in_progress"])
            with col2:
                st.metric("Recent Events", dashboard["recent_audit_events"])
        
        with tab3:
            st.subheader("Governance Policies")
            st.metric("Active Policies", dashboard["active_governance_policies"])
            st.metric("Policy Categories", len(dashboard["policy_categories"]))
    except ImportError as e:
        st.error(f"Compliance module not available: {e}")

elif platform_mode == "Genomic Analysis" and GENOMIC_MODULES_AVAILABLE:
    # Original genomic analysis functionality
    if 'token' in st.session_state:
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
        st.info("Please authenticate via the sidebar to start using the genomic analysis features.")

else:
    st.warning("⚠️ Some modules may not be available due to missing dependencies. Please check the logs.")
    st.info("The Strategic Dashboard and new strategic components are available and working!")

st.caption("🧬 DNA-Lang Platform | Advanced Digital Organism Technology | Market-Leading Genomic AI")
