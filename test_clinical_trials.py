#!/usr/bin/env python3
"""
Test script for the clinical trials module.
This script demonstrates basic functionality without using streamlit or advanced NLP features.
"""

import json
import random
from datetime import datetime, timedelta
# Import the basic functionality without streamlit dependency
from modules.clinical_trials import generate_trial_data, generate_summary_statistics

def simple_find_trials(cancer_type, phase=None, num_trials=10):
    """
    A simplified function to generate mock clinical trial data.
    This replaces the find_trials function that depends on streamlit.
    """
    # Create basic trial data
    trials = []
    phases = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"] if phase == "all" else [f"Phase {phase}"]
    statuses = ["Recruiting", "Active, not recruiting", "Completed", "Not yet recruiting"]
    
    for i in range(num_trials):
        # Generate a random NCT ID
        nct_id = f"NCT{random.randint(1000000, 9999999)}"
        
        # Create trial data
        trial = {
            'id': nct_id,
            'title': f"{cancer_type} {random.choice(['Treatment', 'Prevention', 'Screening'])} Study",
            'phase': random.choice(phases),
            'status': random.choice(statuses),
            'conditions': [cancer_type, random.choice(["Metastatic", "Advanced", "Early Stage"])],
            'start_date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            'completion_date': (datetime.now() + timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d"),
            'locations': [
                {'name': f"Medical Center {i}", 'city': "New York", 'country': "United States"}
                for i in range(random.randint(1, 5))
            ],
            'eligibility': {
                'criteria': f"- Diagnosis of {cancer_type}\n- Age: 18-75 years\n- ECOG Performance Status 0-2",
                'gender': random.choice(["All", "Male", "Female"]),
                'min_age': 18,
                'max_age': 75
            },
            'interventions': [
                f"{random.choice(['Drug', 'Procedure', 'Radiation', 'Behavioral'])}: {random.choice(['Treatment A', 'Treatment B', 'Standard of Care'])}"
            ],
            'enrollment': random.randint(30, 500),
            'match_score': round(random.uniform(0.4, 0.95), 2)  # Simulated match score
        }
        trials.append(trial)
    
    # Sort by match score (highest first)
    trials.sort(key=lambda x: x['match_score'], reverse=True)
    return trials

def main():
    print("Clinical Trials Matching System Test (Simplified Version)")
    print("-" * 60)
    
    # Create a simple patient profile
    patient_profile = {
        'diagnosis': ['Lung cancer', 'Stage IV'],
        'biomarkers': ['EGFR+'],
        'age': 65,
        'gender': 'female',
        'location': "New York, NY",
        'ecog_status': 1,
        'treatment_history': ['radiation', 'surgery']
    }
    
    print(f"Patient Profile:")
    for key, value in patient_profile.items():
        print(f"  {key}: {value}")
    print("-" * 60)
    
    # Use simple_find_trials to generate mock data
    print("Searching for matching clinical trials...")
    matching_trials = simple_find_trials(
        cancer_type="Lung Cancer", 
        phase="all",
        num_trials=15
    )
    
    # Print the results in a readable format
    print(f"\nFound {len(matching_trials)} matching trials:")
    print("-" * 60)
    
    for i, trial in enumerate(matching_trials[:5], 1):  # Show top 5 trials
        print(f"Trial #{i} - Match Score: {trial['match_score']}")
        print(f"  ID: {trial['id']}")
        print(f"  Title: {trial['title']}")
        print(f"  Phase: {trial['phase']}")
        print(f"  Status: {trial['status']}")
        print(f"  Conditions: {', '.join(trial['conditions'])}")
        print(f"  Locations: {len(trial['locations'])} sites available")
        print(f"  Enrollment: {trial['enrollment']} participants")
        print("-" * 60)
    
    # Generate and display summary statistics
    summary_stats = {
        'total_trials': len(matching_trials),
        'recruiting_trials': sum(1 for t in matching_trials if t['status'] == 'Recruiting'),
        'by_phase': {f"Phase {i}": sum(1 for t in matching_trials if t['phase'] == f"Phase {i}") for i in range(1, 5)},
        'avg_enrollment': sum(t['enrollment'] for t in matching_trials) // len(matching_trials),
        'avg_match_score': round(sum(t['match_score'] for t in matching_trials) / len(matching_trials), 2)
    }
    
    print("\nSummary Statistics:")
    print(f"  Total matching trials: {summary_stats['total_trials']}")
    print(f"  Recruiting trials: {summary_stats['recruiting_trials']}")
    print(f"  Average enrollment: {summary_stats['avg_enrollment']} participants")
    print(f"  Average match score: {summary_stats['avg_match_score']}")
    print("  Trials by phase:")
    for phase, count in summary_stats['by_phase'].items():
        print(f"    {phase}: {count}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error running test: {e}")
        print("\nTest failed. Please check your Python environment.")
