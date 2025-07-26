# Utility functions for the platform
def calculate_risk(factor1, factor2):
    return factor1 * factor2

def authenticate_epic(username, password):
    """Mock Epic EHR authentication for demonstration"""
    # In production, this would connect to actual Epic EHR system
    if username and password:
        return "mock_token_12345"
    return None

def fetch_patient_data(patient_id, token):
    """Mock patient data fetch for demonstration"""
    # In production, this would fetch from Epic EHR using the token
    return {
        "id": patient_id,
        "name": f"Patient {patient_id}",
        "age": 45,
        "gender": "Unknown"
    }

def ai_chat_response(user_query, patient_id=None, token=None):
    """Mock AI chat response for demonstration"""
    # In production, this would use actual AI/ML models and patient context
    context = ""
    if patient_id and token:
        context = f" [Patient Context: {patient_id}]"
    return f"AI Response to: {user_query}{context}. This is a mock response for demonstration purposes."
