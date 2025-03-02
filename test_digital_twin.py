#!/usr/bin/env python3

"""
Test script to verify that the generate_digital_twin function
works correctly with the therapies and days parameters.
"""

from modules.digital_twins import generate_digital_twin

def main():
    # Create test patient data (simulating st.session_state.patient_data)
    test_patient_data = {
        "age": 65,
        "gender": "Male",
        "cancer_type": "Lung",
        "stage": "III",
        "genetic_markers": ["EGFR", "KRAS"]
    }
    
    # Create test therapy options
    test_therapies = ["Chemotherapy", "Immunotherapy", "Radiation"]
    
    # Set simulation days
    test_days = 30
    
    print("Testing generate_digital_twin function...")
    print(f"Patient data: {test_patient_data}")
    print(f"Therapies: {test_therapies}")
    print(f"Days: {test_days}")
    
    # Call the function with the test parameters
    try:
        results = generate_digital_twin(
            **test_patient_data,
            therapies=test_therapies,
            days=test_days
        )
        
        print("\nFunction call successful!")
        print(f"Results type: {type(results)}")
        print(f"Results length: {len(results) if isinstance(results, (list, dict)) else 'N/A'}")
        print("Sample results:")
        if isinstance(results, list) and results:
            print(results[0])
        elif isinstance(results, dict) and results:
            print(next(iter(results.items())))
        else:
            print(results)
            
    except Exception as e:
        print(f"\nError occurred: {type(e).__name__}: {e}")
        raise

if __name__ == "__main__":
    main()

