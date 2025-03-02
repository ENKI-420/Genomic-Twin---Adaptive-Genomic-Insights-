import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_digital_twin(
    age=None, 
    gender=None, 
    cancer_type=None, 
    stage=None, 
    genetic_markers=None, 
    num_timepoints=10
):
    """
    Generate a simulated digital twin for oncology analysis.
    
    Parameters:
    -----------
    age : int, optional
        Patient age (18-90)
    gender : str, optional
        Patient gender ('M' or 'F')
    cancer_type : str, optional
        Type of cancer (e.g., 'Lung', 'Breast', 'Colorectal', 'Prostate', 'Melanoma')
    stage : int, optional
        Cancer stage (1-4)
    genetic_markers : list, optional
        List of genetic markers present in the patient
    num_timepoints : int, optional
        Number of timepoints to simulate for the patient journey
        
    Returns:
    --------
    pandas.DataFrame
        Digital twin data containing simulated patient information and biomarkers
    """
    # Set default values if not provided
    if age is None:
        age = random.randint(18, 90)
    
    if gender is None:
        gender = random.choice(['M', 'F'])
    
    if cancer_type is None:
        cancer_type = random.choice(['Lung', 'Breast', 'Colorectal', 'Prostate', 'Melanoma', 'Lymphoma', 'Leukemia'])
    
    if stage is None:
        stage = random.randint(1, 4)
    
    if genetic_markers is None:
        possible_markers = ['BRCA1', 'BRCA2', 'TP53', 'KRAS', 'EGFR', 'ALK', 'HER2', 'BRAF', 'PTEN', 'RB1']
        genetic_markers = random.sample(possible_markers, random.randint(1, 5))
    
    # Generate patient ID
    patient_id = f"PT{random.randint(10000, 99999)}"
    
    # Determine treatment based on cancer type and stage
    treatments = {
        'Lung': ['Chemotherapy', 'Radiation', 'Immunotherapy', 'Targeted Therapy'],
        'Breast': ['Surgery', 'Chemotherapy', 'Hormone Therapy', 'Radiation'],
        'Colorectal': ['Surgery', 'Chemotherapy', 'Immunotherapy', 'Targeted Therapy'],
        'Prostate': ['Surgery', 'Radiation', 'Hormone Therapy', 'Watchful Waiting'],
        'Melanoma': ['Surgery', 'Immunotherapy', 'Targeted Therapy', 'Radiation'],
        'Lymphoma': ['Chemotherapy', 'Immunotherapy', 'Stem Cell Transplant', 'Targeted Therapy'],
        'Leukemia': ['Chemotherapy', 'Targeted Therapy', 'Stem Cell Transplant', 'Immunotherapy'],
    }
    
    # Select appropriate treatments based on cancer type and stage
    available_treatments = treatments.get(cancer_type, ['Chemotherapy', 'Radiation'])
    primary_treatment = random.choice(available_treatments)
    
    # Determine treatment response probability based on stage
    response_probability = {
        1: 0.9,
        2: 0.7,
        3: 0.5,
        4: 0.3
    }
    
    # Generate baseline data
    data = []
    start_date = datetime.now() - timedelta(days=num_timepoints*30)  # Monthly intervals
    
    # Initial tumor size based on stage
    initial_tumor_size = {
        1: random.uniform(0.5, 2.0),
        2: random.uniform(2.0, 5.0),
        3: random.uniform(5.0, 10.0),
        4: random.uniform(10.0, 20.0)
    }
    
    tumor_size = initial_tumor_size[stage]
    
    # Biomarker reference ranges
    biomarkers = {
        'WBC': {'normal': (4.0, 11.0), 'units': 'K/µL'},
        'RBC': {'normal': (4.2, 5.9), 'units': 'M/µL'},
        'Platelets': {'normal': (150, 450), 'units': 'K/µL'},
        'Hemoglobin': {'normal': (12.0, 16.0), 'units': 'g/dL'},
        'Neutrophils': {'normal': (40, 70), 'units': '%'},
        'Lymphocytes': {'normal': (20, 40), 'units': '%'},
        'ALT': {'normal': (7, 56), 'units': 'U/L'},
        'AST': {'normal': (5, 40), 'units': 'U/L'},
        'Creatinine': {'normal': (0.6, 1.2), 'units': 'mg/dL'},
        'CRP': {'normal': (0, 10), 'units': 'mg/L'}
    }
    
    # Cancer-specific biomarkers
    cancer_biomarkers = {
        'Lung': {'marker': 'CEA', 'normal': (0, 3), 'units': 'ng/mL'},
        'Breast': {'marker': 'CA 15-3', 'normal': (0, 30), 'units': 'U/mL'},
        'Colorectal': {'marker': 'CEA', 'normal': (0, 3), 'units': 'ng/mL'},
        'Prostate': {'marker': 'PSA', 'normal': (0, 4), 'units': 'ng/mL'},
        'Melanoma': {'marker': 'LDH', 'normal': (100, 190), 'units': 'U/L'},
        'Lymphoma': {'marker': 'LDH', 'normal': (100, 190), 'units': 'U/L'},
        'Leukemia': {'marker': 'LDH', 'normal': (100, 190), 'units': 'U/L'}
    }
    
    cancer_marker = cancer_biomarkers.get(cancer_type, {'marker': 'CEA', 'normal': (0, 3), 'units': 'ng/mL'})
    
    # Initial cancer marker value
    initial_marker_level = cancer_marker['normal'][1] * (stage ** 1.5)
    cancer_marker_level = initial_marker_level
    
    # Simulate treatment effectiveness
    responds_to_treatment = random.random() < response_probability[stage]
    
    # Generate timepoint data
    for i in range(num_timepoints):
        timepoint_date = start_date + timedelta(days=i*30)
        
        # Adjust tumor size based on treatment response
        if i > 0:  # After treatment begins
            if responds_to_treatment:
                # Tumor shrinks with treatment
                tumor_size = max(0, tumor_size * random.uniform(0.7, 0.95))
                cancer_marker_level = max(cancer_marker['normal'][0], cancer_marker_level * random.uniform(0.8, 0.95))
            else:
                # Tumor grows despite treatment
                tumor_size = tumor_size * random.uniform(1.0, 1.1)
                cancer_marker_level = cancer_marker_level * random.uniform(1.0, 1.15)
        
        # Generate biomarker data
        timepoint_data = {
            'Patient_ID': patient_id,
            'Age': age,
            'Gender': gender,
            'Cancer_Type': cancer_type,
            'Stage': stage,
            'Timepoint': i,
            'Date': timepoint_date.strftime('%Y-%m-%d'),
            'Treatment': primary_treatment,
            'Tumor_Size_cm': round(tumor_size, 2),
            cancer_marker['marker']: round(cancer_marker_level, 2),
            f"{cancer_marker['marker']}_Units": cancer_marker['units'],
            'Genetic_Markers': ', '.join(genetic_markers)
        }
        
        # Add standard biomarkers
        for marker, info in biomarkers.items():
            # Abnormal values more likely in advanced stages and non-responders
            abnormality_factor = stage / 4.0
            if not responds_to_treatment:
                abnormality_factor += 0.2
            
            if random.random() < abnormality_factor:
                # Generate abnormal value
                low_abnormal = info['normal'][0] * random.uniform(0.5, 0.9)
                high_abnormal = info['normal'][1] * random.uniform(1.1, 2.0)
                if random.random() < 0.5:
                    value = round(low_abnormal, 2)
                else:
                    value = round(high_abnormal, 2)
            else:
                # Generate normal value
                value = round(random.uniform(info['normal'][0], info['normal'][1]), 2)
            
            timepoint_data[marker] = value
            timepoint_data[f"{marker}_Units"] = info['units']
        
        data.append(timepoint_data)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    return df
