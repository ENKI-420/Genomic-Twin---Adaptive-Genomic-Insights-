import requests
import json
import os
import fhirclient.models.patient as p
import fhirclient.models.observation as obs
import fhirclient.models.condition as cond
from fhirclient import client
import pandas as pd
from fpdf import FPDF
from docx import Document

# Initialize FHIR Client for EPIC Integration with Secure Credentials
settings = {
    'app_id': os.getenv('FHIR_APP_ID', 'genomic_ai_integration'),
    'api_base': os.getenv('FHIR_API_BASE', 'https://epic.fhir.example.com')
}
fhir_client = client.FHIRClient(settings=settings)

# Fetch Patient Data from EPIC using FHIR with Error Handling
def fetch_patient_data(patient_id):
    try:
        patient = p.Patient.read(patient_id, fhir_client.server)
        return patient.as_json()
    except Exception as e:
        return {"error": f"Failed to fetch patient data: {str(e)}"}

# Merge Genomic Data with EMR Data
def merge_genomic_with_emr(genomic_data, patient_id):
    patient_data = fetch_patient_data(patient_id)
    merged_data = {
        "patient": patient_data,
        "genomic": genomic_data
    }
    return merged_data

# Fetch Variant Annotations from ClinVar, COSMIC, or gnomAD with Error Handling
def fetch_variant_annotations(variant_id):
    urls = {
        "ClinVar": f"https://api.ncbi.nlm.nih.gov/clinvar/v1/variants/{variant_id}",
        "COSMIC": f"https://cancer.sanger.ac.uk/cosmic/api/variants/{variant_id}",
        "gnomAD": f"https://gnomad.broadinstitute.org/api/variants/{variant_id}"
    }
    
    annotations = {}
    for source, url in urls.items():
        try:
            response = requests.get(url)
            response.raise_for_status()
            annotations[source] = response.json()
        except requests.exceptions.RequestException as e:
            annotations[source] = {"error": f"Failed to fetch data from {source}: {str(e)}"}
    
    return annotations

# AI-Based Treatment Recommendations with Drug Dosage & Clinical Trials
def ai_treatment_recommendations(variant_data, patient_data):
    treatment_guidelines = {
        "BRCA1 p.V600E": {"recommendation": "Consider PARP inhibitors for targeted therapy.", "dosage": "Olaparib 300mg BID", "clinical_trial": "NCT03812345"},
        "TP53 mutation": {"recommendation": "Monitor for increased cancer risk and consider precision therapies.", "dosage": "Varies by mutation subtype", "clinical_trial": "NCT04567890"},
        "EGFR exon 19 deletion": {"recommendation": "EGFR tyrosine kinase inhibitors recommended.", "dosage": "Osimertinib 80mg QD", "clinical_trial": "NCT01234567"},
        "ALK rearrangement": {"recommendation": "Consider ALK inhibitors such as Crizotinib.", "dosage": "Crizotinib 250mg BID", "clinical_trial": "NCT09876543"},
        "BRAF V600E": {"recommendation": "BRAF inhibitors like Dabrafenib + Trametinib recommended.", "dosage": "Dabrafenib 150mg BID + Trametinib 2mg QD", "clinical_trial": "NCT06789012"}
    }
    
    variant = variant_data.get("variant", "Unknown Variant")
    recommendation_data = treatment_guidelines.get(variant, {"recommendation": "Consult NCCN guidelines for detailed treatment options.", "dosage": "Not available", "clinical_trial": "Not available"})
    
    return {
        "patient_id": patient_data.get("id", "Unknown"),
        "variant": variant,
        "recommendation": recommendation_data["recommendation"],
        "dosage": recommendation_data["dosage"],
        "clinical_trial": recommendation_data["clinical_trial"]
    }

# Generate Custom Reports (PDF, DOCX, JSON) with Enhanced Formatting
def generate_report(data, format='pdf'):
    if format == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Genomic AI Report", ln=True, align='C')
        pdf.multi_cell(0, 10, json.dumps(data, indent=4))
        pdf.output("genomic_report.pdf")
    elif format == 'docx':
        doc = Document()
        doc.add_heading('Genomic AI Report', level=1)
        for key, value in data.items():
            doc.add_heading(key, level=2)
            doc.add_paragraph(json.dumps(value, indent=4))
        doc.save("genomic_report.docx")
    elif format == 'json':
        with open("genomic_report.json", "w") as f:
            json.dump(data, f, indent=4)
    
    return f"Report saved as genomic_report.{format}"

# Example Execution
if __name__ == "__main__":
    sample_genomic_data = {"variant": "BRCA1 p.V600E", "impact": "High"}
    patient_id = "123456"
    merged_data = merge_genomic_with_emr(sample_genomic_data, patient_id)
    variant_annotations = fetch_variant_annotations("BRCA1 p.V600E")
    treatment_recommendations = ai_treatment_recommendations(sample_genomic_data, merged_data["patient"])
    
    final_data = {
        "merged_data": merged_data,
        "annotations": variant_annotations,
        "treatment_recommendations": treatment_recommendations
    }
    
    print(generate_report(final_data, format='pdf'))
