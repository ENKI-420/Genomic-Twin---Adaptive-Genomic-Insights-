import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random

def simulate_delivery(nanoparticle_type="Liposome", particle_size=100, drug_load=0.5, 
                     targeting_mechanism="Passive", simulation_hours=72, tumor_permeability=0.3,
                     clearance_rate=0.05, include_visualization=True):
    """
    Simulates nanoparticle drug delivery systems for cancer treatment.
    
    Parameters:
    -----------
    nanoparticle_type : str
        Type of nanoparticle carrier (Liposome, Polymer, Gold, Silica, etc.)
    particle_size : int
        Size of nanoparticles in nanometers
    drug_load : float
        Drug loading capacity (0.0 - 1.0)
    targeting_mechanism : str
        Targeting approach (Passive, Active, Magnetic, pH-responsive)
    simulation_hours : int
        Duration of simulation in hours
    tumor_permeability : float
        Tumor vasculature permeability (0.0 - 1.0)
    clearance_rate : float
        Rate of nanoparticle clearance from bloodstream
    include_visualization : bool
        Whether to generate and return visualization objects
        
    Returns:
    --------
    dict
        Dictionary containing simulation dataframes and optionally plot figures
    """
    
    # Parameter validation
    if particle_size < 10 or particle_size > 500:
        st.warning("Particle size should be between 10-500 nm for most oncology applications")
    
    if drug_load < 0 or drug_load > 1:
        drug_load = max(0, min(drug_load, 1))
        st.warning("Drug load adjusted to be between 0 and 1")
    
    # Efficiency factors based on parameters
    targeting_efficiency = {
        "Passive": 0.3,
        "Active": 0.6,
        "Magnetic": 0.7,
        "pH-responsive": 0.5
    }.get(targeting_mechanism, 0.3)
    
    size_efficiency = 1.0 - (abs(particle_size - 100) / 400)  # Optimal size around 100nm
    
    nanoparticle_stability = {
        "Liposome": 0.7,
        "Polymer": 0.8,
        "Gold": 0.9,
        "Silica": 0.75,
        "Dendrimer": 0.65
    }.get(nanoparticle_type, 0.7)
    
    # Generate time points
    time_points = np.arange(0, simulation_hours + 1, 1)
    
    # Blood concentration simulation
    initial_blood_conc = 1.0
    blood_conc = initial_blood_conc * np.exp(-clearance_rate * time_points)
    
    # Calculate tumor accumulation based on EPR effect and targeting
    tumor_accumulation = np.zeros_like(time_points, dtype=float)
    for i, t in enumerate(time_points):
        if i > 0:
            # New accumulation depends on blood concentration, permeability and targeting
            new_accum = blood_conc[i] * tumor_permeability * targeting_efficiency * size_efficiency
            # Total accumulation includes previous amount minus some degradation
            tumor_accumulation[i] = tumor_accumulation[i-1] + new_accum - (tumor_accumulation[i-1] * 0.02)
    
    # Drug release profile (sigmoid for controlled release)
    release_midpoint = simulation_hours / 2
    release_rate = 0.15
    drug_release = drug_load * (1 / (1 + np.exp(-(time_points - release_midpoint) * release_rate)))
    
    # Calculate effective drug concentration in tumor
    effective_concentration = tumor_accumulation * drug_release * nanoparticle_stability
    
    # Therapeutic effect (simplified model)
    max_effect = 0.8  # Maximum possible tumor reduction
    therapeutic_effect = max_effect * (1 - np.exp(-0.05 * effective_concentration * time_points))
    
    # Side effects (inversely related to targeting efficiency)
    side_effects = (1 - targeting_efficiency) * blood_conc * drug_release
    
    # Create dataframe with results
    results_df = pd.DataFrame({
        'Time_Hours': time_points,
        'Blood_Concentration': blood_conc,
        'Tumor_Accumulation': tumor_accumulation,
        'Drug_Release': drug_release,
        'Effective_Concentration': effective_concentration,
        'Therapeutic_Effect': therapeutic_effect,
        'Side_Effects': side_effects
    })
    
    # Generate synthetic data for tissue distribution
    tissue_distribution = {
        'Tissue': ['Tumor', 'Liver', 'Spleen', 'Kidney', 'Lung', 'Heart', 'Brain'],
        'Concentration': [
            effective_concentration[-1],
            blood_conc[-1] * 0.4,
            blood_conc[-1] * 0.3,
            blood_conc[-1] * 0.15,
            blood_conc[-1] * 0.1,
            blood_conc[-1] * 0.05,
            blood_conc[-1] * 0.01 * targeting_efficiency  # BBB penetration is limited
        ]
    }
    tissue_df = pd.DataFrame(tissue_distribution)
    
    # Collate patient response data (simulated)
    num_patients = 20
    patient_data = []
    
    for i in range(num_patients):
        response_variation = random.uniform(0.7, 1.3)
        patient_data.append({
            'Patient_ID': f'P{i+1:03d}',
            'Age': random.randint(35, 85),
            'Cancer_Type': random.choice(['Breast', 'Lung', 'Colon', 'Pancreatic', 'Melanoma']),
            'Tumor_Size_cm': round(random.uniform(0.5, 8.0), 1),
            'Response_Rate': therapeutic_effect[-1] * response_variation,
            'Side_Effect_Severity': round(side_effects[-1] * response_variation, 2)
        })
    
    patient_df = pd.DataFrame(patient_data)
    
    # Prepare return data
    return_data = {
        'kinetics_data': results_df,
        'tissue_distribution': tissue_df,
        'patient_responses': patient_df,
        'simulation_params': {
            'nanoparticle_type': nanoparticle_type,
            'particle_size': particle_size,
            'drug_load': drug_load,
            'targeting_mechanism': targeting_mechanism,
            'simulation_hours': simulation_hours,
            'tumor_permeability': tumor_permeability
        }
    }
    
    # Generate visualizations if requested
    if include_visualization:
        # Concentration over time plot
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(time_points, blood_conc, 'b-', label='Blood Concentration')
        ax1.plot(time_points, tumor_accumulation, 'r-', label='Tumor Accumulation')
        ax1.plot(time_points, effective_concentration, 'g-', label='Effective Drug Concentration')
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('Relative Concentration')
        ax1.set_title('Nanoparticle Delivery Kinetics')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Tissue distribution bar chart
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Tissue', y='Concentration', data=tissue_df, ax=ax2)
        ax2.set_title('Nanoparticle Distribution Across Tissues')
        ax2.set_ylabel('Relative Concentration')
        plt.xticks(rotation=45)
        
        # Patient response scatter plot
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        scatter = ax3.scatter(
            patient_df['Tumor_Size_cm'], 
            patient_df['Response_Rate'],
            c=patient_df['Side_Effect_Severity'], 
            cmap='coolwarm', 
            alpha=0.7,
            s=100
        )
        ax3.set_xlabel('Tumor Size (cm)')
        ax3.set_ylabel('Treatment Response Rate')
        ax3.set_title('Patient Response vs. Tumor Size')
        cbar = plt.colorbar(scatter)
        cbar.set_label('Side Effect Severity')
        
        return_data['figures'] = {
            'kinetics_plot': fig1,
            'distribution_plot': fig2,
            'response_plot': fig3
        }
    
    return return_data
