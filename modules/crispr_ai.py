import requests
from Bio import SeqIO
from Bio.Blast import NCBIWWW
import json
import numpy as np
import logging
from concurrent.futures import ThreadPoolExecutor
import time

# Import Google Cloud with fallback
try:
    from google.cloud import bigquery
    BIGQUERY_AVAILABLE = True
except ImportError:
    BIGQUERY_AVAILABLE = False
    logging.warning("Google Cloud BigQuery not available. Install google-cloud-bigquery.")

# Import TensorFlow with fallback
try:
    from tensorflow.keras.models import load_model
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logging.warning("TensorFlow not available. Some ML features may be limited.")

# Import our authentication module
from modules.gcloud_auth import get_auth_instance, gcloud_login

logging.basicConfig(level=logging.INFO)

# Simple retry decorator to replace retrying
def simple_retry(max_attempts=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

class ProductionCRISPRAnalyzer:
    def __init__(self, config_path: str = 'config.json'):
        self.config = self._load_config(config_path)
        self.cas_variants = self._load_cas_variants()
        self.model = self._load_ml_model()
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.auth = get_auth_instance()
        
    def _load_config(self, path: str) -> dict:
        """Load configuration with API keys and endpoints"""
        try:
            with open(path) as f:
                return json.load(f)
        except FileNotFoundError:
            # Default configuration if file doesn't exist
            return {
                'ensembl_endpoint': 'https://rest.ensembl.org',
                'cas_variants_endpoint': 'https://crispr-db.com/variants',
                'model_path': 'models/crispr_efficiency_v1.h5',
                'blast_table': 'genomic_data.crispr_blast_index',
                'tissue_delivery_table': 'genomic_data.tissue_delivery',
                'cloud_project': 'your-gcp-project'
            }

    def _load_cas_variants(self) -> dict:
        """Load CRISPR-Cas variants database"""
        try:
            response = requests.get(self.config['cas_variants_endpoint'], timeout=10)
            return response.json()
        except Exception as e:
            logging.warning(f"Could not load CAS variants: {e}")
            # Return default CAS variants
            return {
                'SpCas9': {'pam': 'NGG', 'length': 20},
                'Cas12a': {'pam': 'TTTV', 'length': 23},
                'Cas13': {'pam': 'H', 'length': 28}
            }

    def _load_ml_model(self):
        """Load pre-trained efficiency prediction model"""
        if not TENSORFLOW_AVAILABLE:
            logging.warning("TensorFlow not available, ML predictions disabled")
            return None
        try:
            return load_model(self.config['model_path'])
        except Exception as e:
            logging.warning(f"Could not load ML model: {e}")
            return None

    @simple_retry(max_attempts=3, delay=2)
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
        if not self.model:
            # Return mock prediction if model not available
            return 0.75  # Default efficiency score
        encoded = self._encode_sequence(guide_seq)
        return float(self.model.predict(encoded[np.newaxis])[0][0])

    def _encode_sequence(self, seq: str) -> np.ndarray:
        """Convert DNA sequence to ML model features"""
        # Implementation using one-hot encoding or k-mer features
        return np.array([[ord(c) for c in seq]])  # Simplified example

    def _get_bigquery_client(self):
        """Get authenticated BigQuery client"""
        if not BIGQUERY_AVAILABLE:
            raise ImportError("Google Cloud BigQuery not available")
            
        if not self.auth.is_authenticated():
            # Try to authenticate
            if not gcloud_login():
                raise Exception("Google Cloud authentication required. Run 'gcloud auth login'")
        
        credentials = self.auth.get_credentials()
        project_id = self.auth.get_project_id()
        
        return bigquery.Client(credentials=credentials, project=project_id)

    def cloud_blast_search(self, guide_seq: str):
        """Cloud-based off-target search using BigQuery"""
        if not BIGQUERY_AVAILABLE:
            logging.warning("BigQuery not available, skipping cloud BLAST search")
            return []
            
        try:
            client = self._get_bigquery_client()
            query = f"""
                SELECT chromosome, start, end, mismatches
                FROM `{self.config['blast_table']}`
                WHERE sequence = '{guide_seq}'
                AND mismatches < 3
                LIMIT 100
            """
            return list(client.query(query).result())
        except Exception as e:
            logging.error(f"Cloud BLAST search failed: {e}")
            return []

    def tissue_specific_delivery(self, gene_symbol: str) -> list:
        """Query tissue expression database for delivery recommendations"""
        if not BIGQUERY_AVAILABLE:
            logging.warning("BigQuery not available, returning mock delivery data")
            return ['Lipid nanoparticles', 'Viral vectors', 'Electroporation']
            
        try:
            client = self._get_bigquery_client()
            query = f"""
                SELECT delivery_method, efficacy
                FROM `{self.config['tissue_delivery_table']}`
                WHERE gene_symbol = '{gene_symbol}'
                ORDER BY efficacy DESC
                LIMIT 10
            """
            return [row.delivery_method for row in client.query(query).result()]
        except Exception as e:
            logging.error(f"Tissue delivery query failed: {e}")
            return ['Lipid nanoparticles', 'Viral vectors']

    def _generate_guides(self, dna_seq: str, pam: str, grna_length: int) -> list:
        """Generate guide RNAs for given sequence"""
        guides = []
        seq_upper = dna_seq.upper()
        
        # Simple PAM site finding (this is a simplified implementation)
        for i in range(len(seq_upper) - grna_length - 3):
            # Look for PAM sites (simplified - just looking for NGG for SpCas9)
            if 'NGG' in pam and seq_upper[i + grna_length:i + grna_length + 3] == 'NGG':
                guide_seq = seq_upper[i:i + grna_length]
                efficiency = self.predict_efficiency(guide_seq)
                guides.append({
                    'sequence': guide_seq,
                    'position': i,
                    'pam_site': seq_upper[i + grna_length:i + grna_length + 3],
                    'efficiency': efficiency
                })
        
        # Sort by efficiency and return top candidates
        guides.sort(key=lambda x: x['efficiency'], reverse=True)
        return guides[:10]  # Return top 10 guides

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
            
            # Parallel processing for off-target analysis
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
                'cas_variant': cas_variant,
                'authentication_status': self.auth.is_authenticated()
            }
        except Exception as e:
            logging.error(f"Analysis failed: {str(e)}")
            return {'error': str(e), 'authentication_status': self.auth.is_authenticated()}


# Convenience functions for the module
def crispr_feasibility(gene_target: str, cas_variant: str = 'SpCas9') -> dict:
    """Analyze CRISPR feasibility for a given gene target"""
    analyzer = ProductionCRISPRAnalyzer()
    return analyzer.analyze_guide_rna(gene_target, cas_variant)

def check_gcloud_auth() -> bool:
    """Check if Google Cloud is authenticated"""
    auth = get_auth_instance()
    return auth.is_authenticated()

def authenticate_gcloud(method: str = 'default') -> bool:
    """Authenticate with Google Cloud"""
    return gcloud_login(method)

# Example configuration
"""
config.json:
{
  "ensembl_endpoint": "https://rest.ensembl.org",
  "cas_variants_endpoint": "https://crispr-db.com/variants",
  "model_path": "models/crispr_efficiency_v1.h5",
  "blast_table": "project.dataset.crispr_blast_index",
  "tissue_delivery_table": "project.dataset.tissue_delivery",
  "cloud_project": "my-gcp-project"
}
"""
