#!/usr/bin/env python3
import random
from datetime import datetime, timedelta
import json

# Mock the essential parts of generate_digital_twin function
def generate_digital_twin(
    patient_data=None,  # Added to accept patient_data directly
    age=None, 
    gender=None, 
    cancer_type=None, 
    stage=None, 
    genetic_markers=None, 
    num_timepoints=10,
    therapies=None,  # Added to accept therapies
    days=None        # Added to accept days instead of num_timepoints
):
    """
    Generate a realistic digital twin for cancer patients based on provided parameters.
    
    Parameters:
    -----------
    patient_data : dict, optional
        Patient data dictionary containing demographic and clinical information
    age : int, optional
        Age of the patient
    gender : str, optional
        Gender of the patient ('Male' or 'Female')
    cancer_type : str, optional
        Type of cancer
    stage : str, optional
        Cancer stage
    genetic_markers : list, optional
        List of genetic markers
    num_timepoints : int, optional
        Number of timepoints to simulate (default: 10)
    therapies : list, optional
        List of therapies to simulate
    days : int, optional
        Number of days to simulate (replaces num_timepoints if provided)
    
    Returns:
    --------
    dict
        Digital twin data including patient info and simulation results
    """
    # Use days parameter if provided
    if days is not None:
        num_timepoints = days
    
    print(f"Using num_timepoints/days: {num_timepoints}")
    
    # Extract data from patient_data if provided
    if patient_data:
        if age is None and 'age' in patient_data:
            age = patient_data['age']
        if gender is None and 'gender' in patient_data:
            gender = patient_data['gender']
        if cancer_type is None and 'cancer_type' in patient_data:
            cancer_type = patient_data['cancer_type']
        if stage is None and 'stage' in patient_data:
            stage = patient_data['stage']
        if genetic_markers is None and 'genetic_markers' in patient_data:
            genetic_markers = patient_data['genetic_markers']
    
    # Use default values if still None
    age = age or random.randint(30, 85)
    gender = gender or random.choice(['Male', 'Female'])
    cancer_type = cancer_type or random.choice(['Lung', 'Breast', 'Colorectal', 'Prostate'])
    stage = stage or random.choice(['I', 'II', 'III', 'IV'])
    genetic_markers = genetic_markers or []
    
    # Check if therapies were provided
    treatment_options = []
    if therapies:
        # Use provided therapies
        treatment_options = therapies
        print(f"Using provided therapies: {treatment_options}")
    else:
        # Default treatment options based on cancer type
        default_treatments = {
            'Lung': ['Surgery', 'Chemotherapy', 'Radiation'],
            'Breast': ['Surgery', 'Chemotherapy', 'Hormone Therapy'],
            'Colorectal': ['Surgery', 'Chemotherapy'],
            'Prostate': ['Surgery', 'Radiation', 'Hormone Therapy']
        }
        treatment_options = default_treatments.get(cancer_type, ['Chemotherapy'])
        print(f"Using default therapies: {treatment_options}")
    
    # Create a simple simulation
    start_date = datetime.now()
    dates = [(start_date + timedelta(days=i*7)).strftime('%Y-%m-%d') for i in range(num_timepoints)]
    
    # Simple simulated tumor size reduction
    tumor_size = [random.uniform(3.0, 8.0)]
    for i in range(1, num_timepoints):
        # Random treatment effect with overall decreasing trend
        reduction = random.uniform(0.1, 0.5)
        new_size = max(0, tumor_size[-1] - reduction)
        tumor_size.append(new_size)
    
    # Create simulation results
    simulation_results = {
        'dates': dates,
        'tumor_size': tumor_size,
        'treatment': treatment_options
    }
    
    # Patient information
    patient_info = {
        'age': age,
        'gender': gender,
        'cancer_type': cancer_type,
        'stage': stage,
        'genetic_markers': genetic_markers
    }
    
    # Combine all data
    digital_twin_data = {
        'patient_info': patient_info,
        'simulation_results': simulation_results
    }
    
    return digital_twin_data

# Main test code
def main():
    # Create mock patient data
    mock_patient_data = {
        'age': 65,
        'gender': 'Female',
        'cancer_type': 'Breast',
        'stage': 'II',
        'genetic_markers': ['BRCA1', 'HER2']
    }
    
    # Test therapies and days parameters
    therapy_options = ['Immunotherapy', 'Targeted Therapy', 'Hormone Therapy']
    simulation_days = 30
    
    print("Testing generate_digital_twin with therapies and days parameters...")
    try:
        results = generate_digital_twin(
            mock_patient_data,
            therapies=therapy_options,
            days=simulation_days
        )
        print("Function executed successfully!")
        print(f"Simulation days: {simulation_days}")
        print(f"Dates generated: {len(results['simulation_results']['dates'])}")
        print(f"Treatments used: {results['simulation_results']['treatment']}")
        print("Test passed!")
    except TypeError as e:
        print(f"TypeError occurred: {e}")
        print("Test failed!")

if __name__ == "__main__":
    main()

