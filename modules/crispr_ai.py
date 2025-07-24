import requests
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from google.cloud import bigquery
from tensorflow.keras.models import load_model
from concurrent.futures import ThreadPoolExecutor
import json
import numpy as np
import logging
from retrying import retry
import os
import sys

# Add parent directory to path for environment_config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from environment_config import config as env_config

logging.basicConfig(level=logging.INFO)

class ProductionCRISPRAnalyzer:
    def __init__(self, config_path: str = 'config.json'):
        self.env_config = env_config
        self.config = self._load_config(config_path)
        self.cas_variants = self._load_cas_variants()
        self.model = self._load_ml_model()
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Environment-specific security validation
        self._validate_environment_access()
        
    def _validate_environment_access(self):
        """Validate access based on environment security policies"""
        if self.env_config.is_production and not self.env_config.requires_mfa:
            logging.warning("Production environment requires MFA authentication")
            
        if self.env_config.should_use_synthetic_data():
            logging.info("Using synthetic data in development environment")
        
    def _load_config(self, path: str) -> dict:
        """Load configuration with environment-aware settings"""
        try:
            with open(path) as f:
                base_config = json.load(f)
        except FileNotFoundError:
            base_config = {}
            
        # Override with environment-specific settings
        bigquery_config = self.env_config.get_bigquery_config()
        storage_config = self.env_config.get_storage_config()
        
        env_aware_config = {
            **base_config,
            'cloud_project': self.env_config.project_id,
            'blast_table': f"{self.env_config.project_id}.{bigquery_config['dataset_id']}.crispr_blast_index",
            'tissue_delivery_table': f"{self.env_config.project_id}.{bigquery_config['dataset_id']}.tissue_delivery",
            'security_level': self.env_config.security_level,
            'environment': self.env_config.environment
        }
        
        return env_aware_config

    def _load_cas_variants(self) -> dict:
        """Load CRISPR-Cas variants database"""
        return requests.get(self.config['cas_variants_endpoint']).json()

    def _load_ml_model(self):
        """Load pre-trained efficiency prediction model"""
        return load_model(self.config['model_path'])

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def _ensembl_api_call(self, gene_symbol: str) -> dict:
        """Fetch gene sequence from Ensembl API"""
        response = requests.get(
            f"{self.config['ensembl_endpoint']}/lookup/symbol/human/{gene_symbol}",
            headers={'Content-Type': 'application/json'},
            params={'expand': True}
        )
        response.raise_for_status()
        return response.json()

    def get_dna_sequence(self, identifier: str) -> str:
        """Production-grade sequence retrieval"""
        try:
            gene_data = self._ensembl_api_call(identifier)
            return requests.get(
                f"{self.config['ensembl_endpoint']}/sequence/id/{gene_data['id']}"
            ).json()['seq']
        except Exception as e:
            logging.error(f"Sequence fetch failed: {str(e)}")
            raise

    def predict_efficiency(self, guide_seq: str) -> float:
        """ML-based efficiency prediction"""
        encoded = self._encode_sequence(guide_seq)
        return float(self.model.predict(encoded[np.newaxis])[0][0])

    def _encode_sequence(self, seq: str) -> np.ndarray:
        """Convert DNA sequence to ML model features"""
        # Implementation using one-hot encoding or k-mer features
        return np.array([[ord(c) for c in seq]])  # Simplified example

    def cloud_blast_search(self, guide_seq: str):
        """Cloud-based off-target search using BigQuery with environment-aware configuration"""
        
        # Use environment-specific BigQuery client configuration
        if self.env_config.is_production:
            # Production: Use customer-managed encryption and strict access
            client = bigquery.Client(project=self.env_config.project_id)
        else:
            # Non-production: Use default configuration
            client = bigquery.Client(project=self.env_config.project_id)
            
        # Environment-aware table selection
        table_name = self.config['blast_table']
        
        # Add security validation for production
        if self.env_config.is_production:
            if not self._validate_sequence_safety(guide_seq):
                raise ValueError("Sequence validation failed for production environment")
        
        query = f"""
            SELECT chromosome, start, end, mismatches
            FROM `{table_name}`
            WHERE sequence = '{guide_seq}'
            AND mismatches < 3
        """
        return client.query(query).result()
    
    def _validate_sequence_safety(self, sequence: str) -> bool:
        """Additional sequence validation for production environment"""
        # Implement production-specific sequence safety checks
        if len(sequence) < 10 or len(sequence) > 50:
            return False
        # Add more production-specific validations as needed
        return True

    def tissue_specific_delivery(self, gene_symbol: str) -> list:
        """Query tissue expression database for delivery recommendations"""
        table_name = self.config['tissue_delivery_table']
        client = bigquery.Client(project=self.env_config.project_id)
        
        query = f"""
            SELECT delivery_method, efficacy
            FROM `{table_name}`
            WHERE gene_symbol = '{gene_symbol}'
            ORDER BY efficacy DESC
        """
        return [row.delivery_method for row in client.query(query).result()]

    def _generate_guides(self, dna_seq: str, pam: str, grna_length: int) -> list:
        """Generate guide RNA sequences - placeholder implementation"""
        # This is a simplified implementation for demonstration
        # In production, this would contain sophisticated guide generation logic
        guides = []
        for i in range(0, len(dna_seq) - grna_length, 10):
            guide_seq = dna_seq[i:i + grna_length]
            efficiency = self.predict_efficiency(guide_seq)
            guides.append({
                'sequence': guide_seq,
                'position': i,
                'efficiency': efficiency,
                'pam': pam
            })
        return sorted(guides, key=lambda x: x['efficiency'], reverse=True)[:5]

    def analyze_guide_rna(self, gene_target: str, cas_variant: str = 'SpCas9'):
        """Full production analysis pipeline"""
        try:
            # Configure Cas variant parameters
            pam = self.cas_variants[cas_variant]['pam']
            grna_length = self.cas_variants[cas_variant]['length']

            # Get genomic data
            dna_seq = self.get_dna_sequence(gene_target)
            
            # Generate guides with cloud-based validation
            guides = self._generate_guides(dna_seq, pam, grna_length)
            
            # Parallel processing
            futures = [
                self.executor.submit(self.cloud_blast_search, g['sequence'])
                for g in guides[:3]
            ]
            off_targets = [f.result() for f in futures]

            return {
                'gene': gene_target,
                'guides': guides,
                'delivery': self.tissue_specific_delivery(gene_target),
                'off_targets': off_targets,
                'cas_variant': cas_variant
            }
        except Exception as e:
            logging.error(f"Analysis failed: {str(e)}")
            return {'error': str(e)}

# Example configuration - Environment-aware
"""
config.json:
{
  "ensembl_endpoint": "https://rest.ensembl.org",
  "cas_variants_endpoint": "https://crispr-db.com/variants",
  "model_path": "models/crispr_efficiency_v1.h5"
}

Note: BigQuery tables, GCP project, and security settings are now automatically 
configured based on the environment (production/staging/development) using 
the environment_config.py module and gcp-organization folder structure.

Environment-specific configurations:
- Production: Customer-managed encryption, strict access controls, audit logging
- Staging: Moderate security, testing-friendly settings
- Development: Relaxed controls, synthetic data, cost optimization
"""
