# Genomic AI Analysis Functions
def analyze_genomic_data(genomic_data, clinical_guidelines="NCCN"):
    """
    Analyze genomic data using AI with integration of clinical guidelines
    Returns structured report with actionable mutations and therapy recommendations
    """
    if not openai_api_key:
        st.error("OpenAI API Key is missing. Please provide a valid key.")
        return None

    client = OpenAI(api_key=openai_api_key)
    
    try:
        # Process input data
        if isinstance(genomic_data, str):  # Assume file path
            if genomic_data.endswith('.vcf'):
                df = pd.read_csv(genomic_data, sep='\t', comment='#')
            else:
                df = pd.read_csv(genomic_data)
        elif isinstance(genomic_data, pd.DataFrame):
            df = genomic_data
        else:
            raise ValueError("Unsupported genomic data format")

        # Validate required columns
        required_cols = ['Gene', 'Mutation', 'Variant_Classification', 'Allele_Frequency']
        if not all(col in df.columns for col in required_cols):
            missing = [col for col in required_cols if col not in df.columns]
            raise ValueError(f"Missing required columns: {', '.join(missing)}")

        # Prepare AI prompt
        genomic_summary = "\n".join(
            [f"- {row['Gene']} {row['Mutation']} ({row['Variant_Classification']}) - AF: {row['Allele_Frequency']}%"
             for _, row in df.iterrows()]
        )

        prompt = f"""As a molecular oncology expert, analyze these genomic findings according to {clinical_guidelines} guidelines:

        {genomic_summary}

        Provide:
        1. Actionable biomarkers with FDA-approved therapies
        2. Clinical trial opportunities (include NCT IDs when possible)
        3. Prognostic implications
        4. Therapeutic resistance mechanisms to consider
        5. Follow-up testing recommendations

        Format response in markdown with sections and emoji icons. Highlight urgent findings."""

        # Get AI analysis
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a precision oncology expert specializing in NGS interpretation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Genomic Analysis Error: {str(e)}")
        return None

# Streamlit UI Integration for Genomic Analysis
if selected_option == "Genomic AI Analysis":
    st.subheader("🧬 Genomic Profiling Analysis")
    
    uploaded_file = st.file_uploader("Upload Genomic Data (VCF/CSV)", type=['vcf', 'csv'])
    guidelines = st.selectbox("Clinical Guidelines", ["NCCN", "ESMO", "ASCO", "Custom"])
    
    if uploaded_file:
        with st.spinner("🔍 Analyzing genomic variants..."):
            # Save uploaded file
            file_path = f"temp_{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process and analyze
            analysis = analyze_genomic_data(file_path, guidelines)
            
            if analysis:
                st.subheader("🧪 AI-Powered Genomic Report")
                st.markdown(analysis)
                st.divider()
                
                # Add disclaimer
                st.caption("""**Clinical Validation Required**  
                This AI-generated report should be interpreted by a certified molecular pathologist.  
                Always confirm biomarker status with orthogonal testing methods.""")
                
                # Add download button
                st.download_button(
                    label="📥 Download Report",
                    data=analysis,
                    file_name="genomic_analysis_report.md",
                    mime="text/markdown"
