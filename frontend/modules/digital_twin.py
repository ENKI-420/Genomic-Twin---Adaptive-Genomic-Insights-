import requests
import json
import random

# Define the FHIR API base URL and OAuth URL
FHIR_BASE_URL = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/"
OAUTH_URL = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"

# Define the Epic client credentials
EPIC_CLIENT_ID = "e098fdbf-3af1-4514-a08e-13cdbf4ba63c"
EPIC_CLIENT_SECRET = "weAxZbabPXHYceNeitbVyCgrlPUuXYcZoBFLTI7+OAHzsQ26XGj4Qi2SpwT6jykWAjEjqoQU4vmJ05Qfg4fJHA=="

def get_access_token():
    """
    Fetch access token for FHIR API using client credentials grant.
    """
    data = {
        "grant_type": "client_credentials",
        "client_id": EPIC_CLIENT_ID,
        "client_secret": EPIC_CLIENT_SECRET
    }
    try:
        response = requests.post(OAUTH_URL, data=data)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx errors
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error getting access token: {e}")

def get_patient_data(patient_id):
    """
    Fetch patient data from Epic's FHIR API, including genomic data, lab results, and conditions.
    """
    try:
        token = get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # Fetching basic patient info
        patient_url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
        patient_response = requests.get(patient_url, headers=headers)
        patient_response.raise_for_status()

        patient_data = patient_response.json()
        
        # Fetching conditions for the patient
        condition_url = f"{FHIR_BASE_URL}/Condition?patient={patient_id}"
        condition_response = requests.get(condition_url, headers=headers)
        condition_response.raise_for_status()
        conditions = condition_response.json().get("entry", [])
        
        # Fetching medications for the patient
        medication_url = f"{FHIR_BASE_URL}/MedicationRequest?patient={patient_id}"
        medication_response = requests.get(medication_url, headers=headers)
        medication_response.raise_for_status()
        medications = medication_response.json().get("entry", [])
        
        # Combine all data into the final patient digital twin
        patient_data["conditions"] = conditions
        patient_data["medications"] = medications

        # Optionally add genomic data and other lab results here
        # For simplicity, let's assume genomic data is available in another endpoint
        genomic_data = get_genomic_data(patient_id)
        patient_data["genomic_data"] = genomic_data

        return patient_data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching patient data: {e}")
    
def get_genomic_data(patient_id):
    """
    Placeholder function to fetch genomic data for the patient.
    This can be replaced with an actual API endpoint or logic for fetching genomic data.
    """
    # Simulate genomic data (real-world integration should pull actual genomic info)
    return {
        "BRCA1": "Mutated",
        "TP53": "Normal",
        "KRAS": "Mutated"
    }

def generate_digital_twin(patient_data):
    """
    Generates a digital twin for the patient using real-time patient data including genomic data and medical history.

    Args:
        patient_data (dict): The patient data from the FHIR API

    Returns:
        dict: A digital twin representation for the patient
    """
    digital_twin = {}

    # Extract relevant information from the patient data
    digital_twin["patient_id"] = patient_data.get("id", "N/A")
    digital_twin["name"] = patient_data.get("name", "Unknown")
    digital_twin["age"] = patient_data.get("age", "Unknown")
    digital_twin["gender"] = patient_data.get("gender", "Unknown")
    digital_twin["conditions"] = patient_data.get("conditions", [])
    digital_twin["medications"] = patient_data.get("medications", [])
    
    # Add genomic data
    digital_twin["genomic_data"] = patient_data.get("genomic_data", {})

    # Additional calculations (can be enhanced based on patient data)
    digital_twin["mutation_probability"] = random.uniform(0, 1)

    # Example of disease progression based on genomic data (add more logic if needed)
    if "BRCA1" in digital_twin["genomic_data"] and digital_twin["genomic_data"]["BRCA1"] == "Mutated":
        digital_twin["disease_progression"] = "Rapid"
    else:
        digital_twin["disease_progression"] = "Slow"

    # Simulating life expectancy (can be more complex)
    digital_twin["life_expectancy"] = 80 - patient_data.get("age", 50)

    return digital_twin

def save_digital_twin(digital_twin, filename="digital_twin.json"):
    """
    Saves the digital twin to a JSON file.

    Args:
        digital_twin (dict): The digital twin data.
        filename (str): The name of the file to save the data (default: "digital_twin.json")
    """
    with open(filename, 'w') as f:
        json.dump(digital_twin, f, indent=4)
    print(f"Digital twin saved to {filename}")

# Example usage:
if __name__ == "__main__":
    patient_id = "12345"  # Example patient ID, replace with real ID

    # Fetch patient data from Epic's FHIR API
    patient_data = get_patient_data(patient_id)

    # Generate the digital twin based on the fetched data
    digital_twin = generate_digital_twin(patient_data)

    # Save the digital twin to a file
    save_digital_twin(digital_twin)
