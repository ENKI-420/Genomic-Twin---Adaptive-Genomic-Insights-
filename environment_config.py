# Environment-aware Configuration for DNA-Lang Platform
# Supports production, staging, and development environments

import os
import yaml
from typing import Dict, Any

class EnvironmentConfig:
    """
    Environment-aware configuration management for DNA-Lang platform
    Implements different security controls and access policies per environment
    """
    
    def __init__(self, environment: str = None):
        self.environment = environment or os.getenv('DNA_LANG_ENV', 'development')
        self.config = self._load_environment_config()
        
    def _load_environment_config(self) -> Dict[str, Any]:
        """Load environment-specific configuration"""
        # Map environment names to folder names
        env_folder_mapping = {
            'production': 'prod',
            'staging': 'staging', 
            'development': 'dev'
        }
        
        folder_name = env_folder_mapping.get(self.environment, self.environment)
        
        # Try different possible paths
        possible_paths = [
            f"gcp-organization/environments/{folder_name}/config.yaml",
            f"./gcp-organization/environments/{folder_name}/config.yaml",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), f"gcp-organization/environments/{folder_name}/config.yaml")
        ]
        
        for config_path in possible_paths:
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f)
            except FileNotFoundError:
                continue
                
        # Fallback to default configuration
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Default configuration when environment config not found"""
        return {
            'project_id': f'dna-lang-{self.environment}',
            'environment': self.environment,
            'security_level': 'MODERATE',
            'encryption': {
                'at_rest': 'GOOGLE_DEFAULT_ENCRYPTION',
                'in_transit': 'TLS_1_2'
            }
        }
    
    @property
    def project_id(self) -> str:
        """Get GCP project ID for current environment"""
        return self.config.get('project_id', f'dna-lang-{self.environment}')
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == 'production'
    
    @property
    def security_level(self) -> str:
        """Get security level for current environment"""
        return self.config.get('security_level', 'MODERATE')
    
    @property
    def requires_mfa(self) -> bool:
        """Check if MFA is required for current environment"""
        auth_config = self.config.get('authentication', {})
        return auth_config.get('mfa_required', False)
    
    @property
    def session_timeout(self) -> int:
        """Get session timeout in seconds"""
        auth_config = self.config.get('authentication', {})
        return auth_config.get('session_timeout', 7200)
    
    @property
    def encryption_config(self) -> Dict[str, str]:
        """Get encryption configuration"""
        return self.config.get('encryption', {})
    
    @property
    def monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring and logging configuration"""
        return self.config.get('monitoring', {})
    
    @property
    def backup_config(self) -> Dict[str, Any]:
        """Get backup configuration"""
        return self.config.get('backup', {})
    
    @property
    def compliance_config(self) -> Dict[str, Any]:
        """Get compliance configuration"""
        return self.config.get('compliance', {})
    
    @property
    def resource_limits(self) -> Dict[str, Any]:
        """Get resource limits configuration"""
        return self.config.get('resource_limits', {})
    
    def get_bigquery_config(self) -> Dict[str, str]:
        """Get BigQuery configuration for current environment"""
        return {
            'dataset_id': f'genomic_data_{self.environment}',
            'location': 'US',
            'encryption': self.encryption_config.get('at_rest', 'GOOGLE_DEFAULT_ENCRYPTION')
        }
    
    def get_storage_config(self) -> Dict[str, Any]:
        """Get Cloud Storage configuration for current environment"""
        return {
            'bucket_name': f'dna-lang-genomic-files-{self.environment}',
            'location': 'US',
            'encryption': self.encryption_config.get('at_rest', 'GOOGLE_DEFAULT_ENCRYPTION'),
            'versioning': self.is_production
        }
    
    def get_network_config(self) -> Dict[str, Any]:
        """Get network configuration for current environment"""
        return {
            'vpc_name': f'dna-lang-{self.environment}-vpc',
            'subnet_name': f'dna-lang-{self.environment}-subnet',
            'private_google_access': self.is_production or self.environment == 'staging'
        }
    
    def validate_access(self, user_role: str, required_permissions: list) -> bool:
        """
        Validate user access based on environment policies
        Implements environment-specific access control
        """
        if self.is_production:
            # Strict access control for production
            production_roles = ['admin', 'viewer']
            return user_role in production_roles
        elif self.environment == 'staging':
            # Moderate access control for staging
            staging_roles = ['admin', 'editor', 'viewer']
            return user_role in staging_roles
        else:
            # Relaxed access control for development
            return True
    
    def get_service_account_email(self) -> str:
        """Get service account email for current environment"""
        return f'dna-lang-{self.environment}-app@{self.project_id}.iam.gserviceaccount.com'
    
    def should_use_synthetic_data(self) -> bool:
        """Check if synthetic data should be used (for development)"""
        dev_features = self.config.get('dev_features', {})
        return dev_features.get('synthetic_data_only', False)

# Global configuration instance
config = EnvironmentConfig()

# Backwards compatibility with existing config.py
API_KEY = os.getenv('API_KEY', 'YOUR_API_KEY')
BASE_URL = os.getenv('BASE_URL', 'https://api.oncology.ai')

# Environment-aware settings
PROJECT_ID = config.project_id
ENVIRONMENT = config.environment
SECURITY_LEVEL = config.security_level