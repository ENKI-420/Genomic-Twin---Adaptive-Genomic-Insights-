import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random

def find_trials(cancer_type=None, phase=None, location=None, intervention_type=None, min_participants=0):
    """
    Find and analyze clinical trials for cancer treatments.
    
    Parameters:
    -----------
    cancer_type : str, optional
        Type of cancer to filter trials for (e.g., 'Lung', 'Breast', 'Leukemia')
    phase : int or str, optional
        Clinical trial phase to filter for (1, 2, 3, 4, or 'Early', 'Late')
    location : str, optional
        Geographic location to filter trials by
    intervention_type : str, optional
        Type of intervention (e.g., 'Drug', 'Device', 'Procedure', 'Biological')
    min_participants : int, optional
        Minimum number of participants in the trial
    
    Returns:
    --------
    dict
        Dictionary containing DataFrames and visualization data:
        - 'trials': DataFrame of matching clinical trials
        - 'summary': DataFrame summarizing trials by phase and cancer type
        - 'efficacy': DataFrame of efficacy data for visualizations
        - 'timeline': DataFrame showing trial timelines
    """
    # Generate simulated clinical trials data
    trials = generate_trial_data(cancer_type, phase, location, intervention_type, min_participants)
    
    # Generate summary statistics
    summary = generate_summary_statistics(trials)
    
    # Generate efficacy data for the trials
    efficacy = generate_efficacy_data(trials)
    
    # Generate timeline data
    timeline = generate_timeline_data(trials)
    
    return {
        'trials': trials,
        'summary': summary,
        'efficacy': efficacy,
        'timeline': timeline
    }

def generate_trial_data(cancer_type=None, phase=None, location=None, intervention_type=None, min_participants=0):
    """Generate simulated clinical trial data for cancer treatments."""
    # Define possible values for each field
    cancer_types = ['Lung Cancer', 'Breast Cancer', 'Leukemia', 'Prostate Cancer', 
                   'Colorectal Cancer', 'Melanoma', 'Lymphoma', 'Pancreatic Cancer',
                   'Ovarian Cancer', 'Glioblastoma']
    phases = [1, 2, 3, 4]
    locations = ['United States', 'Europe', 'Asia', 'Global', 'Canada', 'Australia']
    statuses = ['Recruiting', 'Active', 'Completed', 'Suspended', 'Not yet recruiting']
    intervention_types = ['Drug', 'Biological', 'Device', 'Procedure', 'Radiation', 'Combination']
    sponsors = ['National Cancer Institute', 'Memorial Sloan Kettering', 'MD Anderson',
               'Mayo Clinic', 'Dana-Farber', 'Genentech', 'Novartis', 'Pfizer',
               'Merck', 'AstraZeneca', 'Roche', 'BMS', 'GSK']
    
    # Filter based on input parameters
    if cancer_type:
        cancer_types = [c for c in cancer_types if cancer_type.lower() in c.lower()]
    
    if phase:
        if isinstance(phase, str):
            if phase.lower() == 'early':
                phases = [1, 2]
            elif phase.lower() == 'late':
                phases = [3, 4]
        else:
            phases = [phase]
    
    if location:
        locations = [loc for loc in locations if location.lower() in loc.lower()]
    
    if intervention_type:
        intervention_types = [i for i in intervention_types if intervention_type.lower() in i.lower()]
    
    # Generate 20-50 random trials
    num_trials = random.randint(20, 50)
    
    # Create empty lists for each column
    trial_ids = []
    titles = []
    trial_cancer_types = []
    trial_phases = []
    trial_locations = []
    trial_statuses = []
    trial_interventions = []
    trial_sponsors = []
    start_dates = []
    end_dates = []
    participant_counts = []
    
    # Generate random data for each trial
    for i in range(num_trials):
        # Generate a unique trial ID
        trial_id = f"NCT{random.randint(1000000, 9999999)}"
        
        # Select a random cancer type
        selected_cancer = random.choice(cancer_types)
        
        # Select a random phase
        selected_phase = random.choice(phases)
        
        # Generate a title based on the cancer type and intervention
        selected_intervention = random.choice(intervention_types)
        if selected_intervention == 'Drug' or selected_intervention == 'Biological':
            drug_name = f"{random.choice(['A', 'B', 'C', 'D', 'E', 'M', 'N', 'P', 'R', 'Z'])}{random.choice(['av', 'en', 'ol', 'ib', 'ab', 'ix', 'mab', 'zol', 'tin'])}-{random.randint(100, 999)}"
            title = f"Study of {drug_name} in Patients With {selected_cancer}"
            intervention_detail = f"{selected_intervention}: {drug_name}"
        else:
            title = f"{selected_intervention} Therapy for {selected_cancer} - Phase {selected_phase} Trial"
            intervention_detail = selected_intervention
        
        # Generate random dates
        current_date = datetime.now()
        start_date = current_date - timedelta(days=random.randint(0, 1095))  # Up to 3 years ago
        duration = random.randint(180, 1095)  # 6 months to 3 years
        end_date = start_date + timedelta(days=duration)
        
        # Generate a random number of participants
        participants = random.randint(10, 1000)
        
        # Skip trials with fewer than min_participants
        if participants < min_participants:
            continue
        
        # Append values to lists
        trial_ids.append(trial_id)
        titles.append(title)
        trial_cancer_types.append(selected_cancer)
        trial_phases.append(selected_phase)
        trial_locations.append(random.choice(locations))
        trial_statuses.append(random.choice(statuses))
        trial_interventions.append(intervention_detail)
        trial_sponsors.append(random.choice(sponsors))
        start_dates.append(start_date)
        end_dates.append(end_date)
        participant_counts.append(participants)
    
    # Create a DataFrame
    df = pd.DataFrame({
        'Trial ID': trial_ids,
        'Title': titles,
        'Cancer Type': trial_cancer_types,
        'Phase': trial_phases,
        'Location': trial_locations,
        'Status': trial_statuses,
        'Intervention': trial_interventions,
        'Sponsor': trial_sponsors,
        'Start Date': start_dates,
        'End Date': end_dates,
        'Participants': participant_counts
    })
    
    return df

def generate_summary_statistics(trials_df):
    """Generate summary statistics for clinical trials."""
    # Count trials by phase
    phase_counts = trials_df['Phase'].value_counts().reset_index()
    phase_counts.columns = ['Phase', 'Number of Trials']
    
    # Count trials by cancer type
    cancer_counts = trials_df['Cancer Type'].value_counts().reset_index()
    cancer_counts.columns = ['Cancer Type', 'Number of Trials']
    
    # Average participants by phase
    avg_participants = trials_df.groupby('Phase')['Participants'].mean().reset_index()
    avg_participants.columns = ['Phase', 'Average Participants']
    
    # Count trials by status
    status_counts = trials_df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Number of Trials']
    
    # Return as a dictionary of dataframes
    return {
        'phase_counts': phase_counts,
        'cancer_counts': cancer_counts,
        'avg_participants': avg_participants,
        'status_counts': status_counts
    }

def generate_efficacy_data(trials_df):
    """Generate simulated efficacy data for the clinical trials."""
    # Select completed trials for efficacy data
    completed_trials = trials_df[trials_df['Status'] == 'Completed']
    
    if completed_trials.empty:
        # If no completed trials, use a sample of all trials
        completed_trials = trials_df.sample(min(5, len(trials_df)))
    
    # Create empty lists for efficacy metrics
    trial_ids = []
    response_rates = []
    survival_months = []
    p_values = []
    hazard_ratios = []
    
    # Generate random efficacy data for each trial
    for _, trial in completed_trials.iterrows():
        trial_ids.append(trial['Trial ID'])
        
        # Higher phase trials tend to have better efficacy
        phase_factor = trial['Phase'] / 4.0
        
        # Generate simulated response rate (higher for higher phases)
        response_rate = random.uniform(0.1, 0.3) + (phase_factor * 0.4)
        response_rates.append(round(response_rate, 2))
        
        # Generate simulated survival in months (higher for higher phases)
        base_survival = random.uniform(6, 12)
        survival = base_survival + (phase_factor * 24)
        survival_months.append(round(survival, 1))
        
        # Generate p-value (lower for higher phases, indicating stronger evidence)
        p_value = random.uniform(0.001, 0.2) * (1 - (phase_factor * 0.5))
        p_values.append(round(p_value, 3))
        
        # Generate hazard ratio (lower is better, indicating reduced risk)
        hr_base = random.uniform(0.5, 1.0)
        hazard_ratio = hr_base - (phase_factor * 0.3)
        hazard_ratios.append(round(hazard_ratio, 2))
    
    # Create a DataFrame
    efficacy_df = pd.DataFrame({
        'Trial ID': trial_ids,
        'Response Rate': response_rates,
        'Median Survival (months)': survival_months,
        'P-value': p_values,
        'Hazard Ratio': hazard_ratios
    })
    
    # Join with trial information
    efficacy_df = efficacy_df.merge(
        completed_trials[['Trial ID', 'Cancer Type', 'Phase', 'Intervention']], 
        on='Trial ID'
    )
    
    return efficacy_df

def generate_timeline_data(trials_df):
    """Generate timeline data for visualizing trial durations and milestones."""
    # Sample up to 15 trials for the timeline view
    timeline_trials = trials_df.sample(min(15, len(trials_df)))
    
    # Create lists for the timeline data
    trial_ids = []
    titles = []
    start_dates = []
    end_dates = []
    current_phases = []
    next_milestones = []
    milestone_dates = []
    
    # Generate timeline data for each trial
    for _, trial in timeline_trials.iterrows():
        trial_ids.append(trial['Trial ID'])
        titles.append(trial['Title'])
        start_dates.append(trial['Start Date'])
        end_dates.append(trial['End Date'])
        
        # Current phase
        current_phases.append(f"Phase {trial['Phase']}")
        
        # Generate a future milestone
        if trial['Status'] == 'Completed':
            next_milestone = "Final Results Publication"
            # Publication typically happens 6-12 months after completion
            milestone_date = trial['End Date'] + timedelta(days=random.randint(180, 365))
        elif trial['Status'] == 'Recruiting':
            next_milestone = "Enrollment Complete"
            # Calculate a date between now and the end date
            today = datetime.now()
            days_until_end = (trial['End Date'] - today).days
            if days_until_end > 0:
                milestone_date = today + timedelta(days=random.randint(30, days_until_end))
            else:
                milestone_date = today + timedelta(days=random.randint(30, 180))
        else:
            next_milestone = "Interim Analysis"
            # Calculate a date between start and end
            total_days = (trial['End Date'] - trial['Start Date']).days
            milestone_date = trial['Start Date'] + timedelta(days=int(total_days * 0.6))
        
        next_milestones.append(next_milestone)
        milestone_dates.append(milestone_date)
    
    # Create a DataFrame
    timeline_df = pd.DataFrame({
        'Trial ID': trial_ids,
        'Title': titles,
        'Start Date': start_dates,
        'End Date': end_dates,
        'Current Phase': current_phases,
        'Next Milestone': next_milestones,
        'Milestone Date': milestone_dates
    })
    
    return timeline_df

# For backward compatibility
def clinical():
    """Legacy function, use find_trials() instead."""
    st.warning("The clinical() function is deprecated. Please use find_trials() instead.")
    return find_trials()
