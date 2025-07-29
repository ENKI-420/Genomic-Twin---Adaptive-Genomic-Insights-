# Clinical Trials Integration Module
CLINICAL_TRIALS_API = "https://clinicaltrials.gov/api/v2/studies"
DEFAULT_PARAMS = {
    "format": "json",
    "query.term": "",
    "filter.advanced": "AREA[LocationCountry]United States AND AREA[StudyType]Interventional",
    "pageSize": 5
}

def fetch_clinical_trials(conditions, biomarkers, location=None, phase=None):
    """Fetch clinical trials from ClinicalTrials.gov API with safety controls"""
    try:
        # Construct evidence-based query
        query_terms = [
            f'"{cond}"' for cond in conditions
        ] + [
            f'"{gene} {variant}"' for gene, variant in biomarkers
        ]
        
        params = DEFAULT_PARAMS.copy()
        params["query.term"] = " OR ".join(query_terms)
        
        if location:
            params["filter.advanced"] += f" AND AREA[LocationCity]{location}"
        if phase:
            params["filter.advanced"] += f" AND AREA[Phase]{phase}"
            
        # Add rate limiting
        time.sleep(1.5)  # Respect API limits
        
        response = requests.get(
            CLINICAL_TRIALS_API,
            params=params,
            headers={"User-Agent": "NortonOncologyAI/1.0 (research)"},
            timeout=10
        )
        response.raise_for_status()
        
        return parse_trial_data(response.json())
        
    except Exception as e:
        st.error(f"Trial API Error: {str(e)}")
        return []

def parse_trial_data(json_response):
    """Transform API response into structured format"""
    trials = []
    for study in json_response.get("studies", [])[:5]:  # Limit to top 5
        try:
            trial = {
                "nct_id": study["protocolSection"]["identificationModule"]["nctId"],
                "title": study["protocolSection"]["identificationModule"]["officialTitle"],
                "phase": study["protocolSection"]["designModule"]["phases"][0] if study["protocolSection"]["designModule"]["phases"] else "N/A",
                "status": study["protocolSection"]["statusModule"]["overallStatus"],
                "conditions": ", ".join(study["protocolSection"]["conditionsModule"]["conditions"]),
                "interventions": ", ".join(
                    [i["name"] for i in study["protocolSection"]["armsInterventionsModule"]["interventions"]]
                ),
                "locations": ", ".join(
                    [site["city"] for site in study["protocolSection"]["contactsLocationsModule"]["locations"]]
                ),
                "url": f"https://clinicaltrials.gov/study/{study['protocolSection']['identificationModule']['nctId']}"
            }
            trials.append(trial)
        except KeyError:
            continue
    return trials

# Enhanced Genomic Analysis Function
def analyze_genomic_data(genomic_data, clinical_guidelines="NCCN", patient_context=None):
    # ... (previous processing code) ...
    
    # Get AI analysis
    ai_report = get_ai_analysis(prompt)  # From previous implementation
    
    # Get clinical trials
    conditions = extract_conditions(patient_context)
    biomarkers = [(row['GENE'], row['MUTATION']) for _, row in df.iterrows()]
    trials = fetch_clinical_trials(
        conditions=conditions,
        biomarkers=biomarkers,
        location=patient_context.get("location", None),
        phase="II OR III"
    )
    
    # Integrate trials into report
    final_report = integrate_trials_into_report(ai_report, trials)
    
    return final_report

def integrate_trials_into_report(ai_report, trials):
    """Combine AI analysis with clinical trial data"""
    trial_section = "## 🔬 Relevant Clinical Trials\n\n"
    
    if not trials:
        trial_section += "No matching clinical trials found in current databases\n"
    else:
        for trial in trials:
            trial_section += f"""### 🧪 [{trial['title']}]({trial['url']})
- **NCT ID**: {trial['nct_id']}
- **Phase**: {trial['phase']}
- **Status**: {trial['status']}
- **Locations**: {trial['locations']}
- **Interventions**: {trial['interventions']}
\n"""
    
    return f"{ai_report}\n\n{trial_section}"

# Streamlit UI Additions
if selected_option == "Genomic AI Analysis":
    # ... previous UI code ...
    
    with st.expander("🌍 Clinical Trial Search Parameters"):
        cols = st.columns(2)
        with cols[0]:
            location = st.text_input("Search Radius (City, State)", "New York, NY")
        with cols[1]:
            trial_phase = st.multiselect("Trial Phase", ["I", "II", "III", "IV"], ["II", "III"])
            
    # ... analysis button ...
    
    if analysis:
        st.subheader("📊 Genomic Insights Report")
        st.markdown(analysis)
        
        # Interactive trial explorer
        st.subheader("🗺️ Trial Map Visualization")
        trials = parse_trials_from_report(analysis)  # Implement parsing logic
        if trials:
            plot_trial_map(trials)
        else:
            st.info("No trial geographic data available")
