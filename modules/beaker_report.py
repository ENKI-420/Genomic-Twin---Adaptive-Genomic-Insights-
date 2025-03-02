import pandas as pd
import random
from datetime import datetime, timedelta

def fetch_beaker_data(patient_id):
    """
    Fetches simulated laboratory data for a given patient ID.
    In a real application, this would connect to a laboratory information system like Beaker.
    
    Args:
        patient_id (str): The unique identifier for the patient
        
    Returns:
        dict: A dictionary containing simulated patient data including genomic information
    """
    # For demo purposes, create consistent but randomized data based on patient_id
    random.seed(hash(patient_id) % 10000)
    
    # Common oncogenic mutations
    possible_mutations = [
        {"gene": "EGFR", "variant": "T790M", "allele_frequency": round(random.uniform(0.05, 0.45), 2)},
        {"gene": "KRAS", "variant": "G12C", "allele_frequency": round(random.uniform(0.1, 0.6), 2)},
        {"gene": "BRAF", "variant": "V600E", "allele_frequency": round(random.uniform(0.15, 0.55), 2)},
        {"gene": "PIK3CA", "variant": "E545K", "allele_frequency": round(random.uniform(0.08, 0.4), 2)},
        {"gene": "TP53", "variant": "R273H", "allele_frequency": round(random.uniform(0.2, 0.7), 2)},
        {"gene": "MET", "variant": "Exon 14 Skipping", "allele_frequency": round(random.uniform(0.1, 0.5), 2)},
        {"gene": "ALK", "variant": "EML4-ALK Fusion", "allele_frequency": round(random.uniform(0.05, 0.4), 2)},
        {"gene": "ROS1", "variant": "CD74-ROS1 Fusion", "allele_frequency": round(random.uniform(0.05, 0.35), 2)},
        {"gene": "RET", "variant": "KIF5B-RET Fusion", "allele_frequency": round(random.uniform(0.1, 0.45), 2)},
        {"gene": "NTRK1", "variant": "TPM3-NTRK1 Fusion", "allele_frequency": round(random.uniform(0.05, 0.3), 2)}
    ]
    
    # Select 2-5 random mutations for this patient
    num_mutations = random.randint(2, 5)
    patient_mutations = random.sample(possible_mutations, num_mutations)
    
    # Generate lab values
    lab_values = {
        "WBC": round(random.uniform(3.5, 11.0), 1),  # 10^3/µL
        "RBC": round(random.uniform(3.5, 5.5), 1),   # 10^6/µL
        "Hemoglobin": round(random.uniform(11.0, 16.0), 1),  # g/dL
        "Hematocrit": round(random.uniform(35.0, 48.0), 1),  # %
        "Platelets": random.randint(140, 450),  # 10^3/µL
        "Neutrophils": round(random.uniform(40.0, 75.0), 1),  # %
        "Lymphocytes": round(random.uniform(20.0, 45.0), 1),  # %
        "Monocytes": round(random.uniform(2.0, 10.0), 1),  # %
        "Eosinophils": round(random.uniform(0.0, 6.0), 1),  # %
        "Basophils": round(random.uniform(0.0, 2.0), 1),  # %
        "Glucose": random.randint(70, 140),  # mg/dL
        "BUN": random.randint(8, 25),  # mg/dL
        "Creatinine": round(random.uniform(0.6, 1.3), 1),  # mg/dL
        "Sodium": random.randint(135, 145),  # mEq/L
        "Potassium": round(random.uniform(3.5, 5.0), 1),  # mEq/L
        "Chloride": random.randint(98, 108),  # mEq/L
        "CO2": random.randint(22, 30),  # mEq/L
        "Calcium": round(random.uniform(8.5, 10.5), 1),  # mg/dL
    }
    
    # Tumor markers (relevant for oncology)
    tumor_markers = {
        "CEA": round(random.uniform(0, 30.0), 1),  # ng/mL
        "CA 19-9": round(random.uniform(0, 100.0), 1),  # U/mL
        "PSA": round(random.uniform(0, 15.0), 2),  # ng/mL
        "AFP": round(random.uniform(0, 50.0), 1),  # ng/mL
        "CA 125": round(random.uniform(0, 150.0), 1),  # U/mL
        "CA 15-3": round(random.uniform(0, 50.0), 1),  # U/mL
    }
    
    # Biomarkers for treatment response (for oncology)
    biomarkers = {
        "PD-L1 Expression": f"{random.randint(0, 100)}%",
        "MSI Status": random.choice(["MSI-High", "MSI-Low", "MSS"]),
        "TMB": round(random.uniform(0, 50.0), 1),  # mutations/Mb
        "HER2 Status": random.choice(["Positive", "Negative"]),
        "HR Status": random.choice(["ER+/PR+", "ER+/PR-", "ER-/PR+", "ER-/PR-"]),
    }
    
    # Create history of sample collections
    today = datetime.now()
    collection_history = []
    for i in range(3):
        collection_date = today - timedelta(days=30*i)
        collection_history.append({
            "sample_id": f"{patient_id}-{collection_date.strftime('%Y%m%d')}",
            "collection_date": collection_date.strftime("%Y-%m-%d"),
            "specimen_type": random.choice(["Blood", "Tissue Biopsy", "Bone Marrow"]),
            "test_performed": random.choice(["NGS Panel", "CBC", "Chemistry Panel", "Liquid Biopsy"])
        })
    
    # Create the complete patient data dict
    patient_data = {
        "patient_id": patient_id,
        "demographic": {
            "age": random.randint(35, 85),
            "sex": random.choice(["Male", "Female"]),
            "ethnicity": random.choice(["Caucasian", "African American", "Hispanic", "Asian", "Other"]),
        },
        "diagnosis": {
            "cancer_type": random.choice([
                "Non-Small Cell Lung Cancer", 
                "Breast Cancer", 
                "Colorectal Cancer", 
                "Prostate Cancer", 
                "Pancreatic Cancer",
                "Melanoma",
                "Multiple Myeloma"
            ]),
            "stage": random.choice(["I", "II", "III", "IV"]),
            "date_of_diagnosis": (today - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
        },
        "genomic_profile": {
            "mutations": patient_mutations,
            "biomarkers": biomarkers,
        },
        "laboratory_results": {
            "hematology": lab_values,
            "tumor_markers": tumor_markers,
        },
        "specimen_collection": collection_history,
    }
    
    return patient_data

def format_beaker_report(patient_data):
    """
    Formats the patient data into a readable report.
    
    Args:
        patient_data (dict): Patient data returned from fetch_beaker_data
        
    Returns:
        pd.DataFrame: A formatted DataFrame for displaying in the UI
    """
    # Create a DataFrame for mutations
    if patient_data and "genomic_profile" in patient_data:
        mutations_df = pd.DataFrame(patient_data["genomic_profile"]["mutations"])
        return mutations_df
    return pd.DataFrame()

