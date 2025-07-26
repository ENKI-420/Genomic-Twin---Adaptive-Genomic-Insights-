"""
CloudArchitectAgent - Terraform Generation and Infrastructure Management
Generates and manages terraform configurations for cloud infrastructure
"""

import os
import json
import yaml
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from jinja2 import Template
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudArchitectAgent:
    """
    Cloud Architect Agent responsible for generating and managing terraform configurations
    """
    
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.terraform_templates = self._load_terraform_templates()
        self.infrastructure_state = {}
        
    def _load_terraform_templates(self) -> Dict[str, str]:
        """Load terraform templates for different components"""
        return {
            'vpc_template': '''
# VPC Configuration for {{ environment }}
resource "google_compute_network" "{{ environment }}_vpc" {
  name                    = "dna-lang-{{ environment }}-vpc"
  auto_create_subnetworks = false
  enable_logging          = {{ enable_logging }}
}

resource "google_compute_subnetwork" "{{ environment }}_subnet" {
  name          = "dna-lang-{{ environment }}-subnet"
  ip_cidr_range = "{{ subnet_cidr }}"
  region        = var.region
  network       = google_compute_network.{{ environment }}_vpc.id
  
  private_ip_google_access = {{ private_google_access }}
  
  {% if enable_flow_logs %}
  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
  {% endif %}
}
''',
            'storage_template': '''
# Cloud Storage Configuration for {{ environment }}
resource "google_storage_bucket" "{{ bucket_name }}" {
  name     = "{{ bucket_name }}"
  location = "{{ location }}"
  
  uniform_bucket_level_access = true
  
  {% if encryption_key %}
  encryption {
    default_kms_key_name = {{ encryption_key }}
  }
  {% endif %}
  
  {% if versioning_enabled %}
  versioning {
    enabled = true
  }
  {% endif %}
  
  {% if lifecycle_rules %}
  {% for rule in lifecycle_rules %}
  lifecycle_rule {
    condition {
      age = {{ rule.age }}
    }
    action {
      type          = "{{ rule.action }}"
      {% if rule.storage_class %}
      storage_class = "{{ rule.storage_class }}"
      {% endif %}
    }
  }
  {% endfor %}
  {% endif %}
}
''',
            'bigquery_template': '''
# BigQuery Configuration for {{ environment }}
resource "google_bigquery_dataset" "{{ dataset_name }}" {
  dataset_id    = "{{ dataset_name }}"
  friendly_name = "{{ friendly_name }}"
  description   = "{{ description }}"
  location      = "{{ location }}"

  {% if encryption_key %}
  default_encryption_configuration {
    kms_key_name = {{ encryption_key }}
  }
  {% endif %}
  
  {% for access in access_controls %}
  access {
    role          = "{{ access.role }}"
    {% if access.user_by_email %}
    user_by_email = "{{ access.user_by_email }}"
    {% endif %}
    {% if access.group_by_email %}
    group_by_email = "{{ access.group_by_email }}"
    {% endif %}
    {% if access.special_group %}
    special_group = "{{ access.special_group }}"
    {% endif %}
  }
  {% endfor %}
}
''',
            'iam_template': '''
# IAM Configuration for {{ environment }}
resource "google_service_account" "{{ service_account_name }}" {
  account_id   = "{{ service_account_name }}"
  display_name = "{{ display_name }}"
}

{% for binding in iam_bindings %}
resource "google_project_iam_member" "{{ binding.name }}" {
  project = var.project_id
  role    = "{{ binding.role }}"
  member  = "serviceAccount:${google_service_account.{{ service_account_name }}.email}"
}
{% endfor %}
''',
            'monitoring_template': '''
# Monitoring Configuration for {{ environment }}
resource "google_monitoring_alert_policy" "{{ policy_name }}" {
  display_name = "{{ display_name }}"
  combiner     = "OR"
  
  conditions {
    display_name = "{{ condition_name }}"
    condition_threshold {
      filter          = "{{ filter }}"
      duration        = "{{ duration }}"
      comparison      = "{{ comparison }}"
      threshold_value = {{ threshold_value }}
    }
  }
  
  {% if notification_channels %}
  notification_channels = [
    {% for channel in notification_channels %}
    "{{ channel }}",
    {% endfor %}
  ]
  {% endif %}
}
'''
        }
    
    def generate_infrastructure_config(self, requirements: Dict[str, Any]) -> Dict[str, str]:
        """Generate terraform configuration based on infrastructure requirements"""
        logger.info(f"Generating infrastructure config for {self.environment}")
        
        generated_configs = {}
        
        # Load environment-specific configuration
        env_config = self._load_environment_config()
        
        # Generate VPC configuration
        if requirements.get('vpc', {}).get('enabled', True):
            vpc_config = self._generate_vpc_config(requirements.get('vpc', {}), env_config)
            generated_configs['vpc.tf'] = vpc_config
        
        # Generate storage configuration
        if requirements.get('storage', {}).get('enabled', True):
            storage_config = self._generate_storage_config(requirements.get('storage', {}), env_config)
            generated_configs['storage.tf'] = storage_config
        
        # Generate BigQuery configuration
        if requirements.get('bigquery', {}).get('enabled', True):
            bigquery_config = self._generate_bigquery_config(requirements.get('bigquery', {}), env_config)
            generated_configs['bigquery.tf'] = bigquery_config
        
        # Generate IAM configuration
        if requirements.get('iam', {}).get('enabled', True):
            iam_config = self._generate_iam_config(requirements.get('iam', {}), env_config)
            generated_configs['iam.tf'] = iam_config
        
        # Generate monitoring configuration
        if requirements.get('monitoring', {}).get('enabled', True):
            monitoring_config = self._generate_monitoring_config(requirements.get('monitoring', {}), env_config)
            generated_configs['monitoring.tf'] = monitoring_config
        
        # Generate variables file
        variables_config = self._generate_variables_config(env_config)
        generated_configs['variables.tf'] = variables_config
        
        # Generate main configuration file that ties everything together
        main_config = self._generate_main_config(env_config)
        generated_configs['main.tf'] = main_config
        
        return generated_configs
    
    def _load_environment_config(self) -> Dict[str, Any]:
        """Load environment-specific configuration"""
        from environment_config import EnvironmentConfig
        config = EnvironmentConfig(self.environment)
        
        return {
            'environment': self.environment,
            'project_id': config.project_id,
            'region': 'us-central1',
            'security_level': config.security_level,
            'encryption_at_rest': config.encryption_config.get('at_rest', 'GOOGLE_DEFAULT_ENCRYPTION'),
            'requires_mfa': config.requires_mfa,
            'bigquery_config': config.get_bigquery_config(),
            'storage_config': config.get_storage_config(),
            'network_config': config.get_network_config()
        }
    
    def _generate_vpc_config(self, vpc_requirements: Dict[str, Any], env_config: Dict[str, Any]) -> str:
        """Generate VPC terraform configuration"""
        template = Template(self.terraform_templates['vpc_template'])
        
        context = {
            'environment': self.environment,
            'enable_logging': env_config['security_level'] in ['STRICT', 'MODERATE'],
            'subnet_cidr': vpc_requirements.get('subnet_cidr', '10.1.0.0/24'),
            'private_google_access': env_config['network_config']['private_google_access'],
            'enable_flow_logs': env_config['security_level'] == 'STRICT'
        }
        
        return template.render(**context)
    
    def _generate_storage_config(self, storage_requirements: Dict[str, Any], env_config: Dict[str, Any]) -> str:
        """Generate Cloud Storage terraform configuration"""
        template = Template(self.terraform_templates['storage_template'])
        
        storage_config = env_config['storage_config']
        
        context = {
            'environment': self.environment,
            'bucket_name': storage_config['bucket_name'],
            'location': storage_config['location'],
            'encryption_key': 'google_kms_crypto_key.genomic_key.id' if storage_config['encryption'] != 'GOOGLE_DEFAULT_ENCRYPTION' else None,
            'versioning_enabled': storage_config.get('versioning', False),
            'lifecycle_rules': storage_requirements.get('lifecycle_rules', [
                {'age': 30, 'action': 'SetStorageClass', 'storage_class': 'COLDLINE'},
                {'age': 365, 'action': 'Delete'}
            ])
        }
        
        return template.render(**context)
    
    def _generate_bigquery_config(self, bigquery_requirements: Dict[str, Any], env_config: Dict[str, Any]) -> str:
        """Generate BigQuery terraform configuration"""
        template = Template(self.terraform_templates['bigquery_template'])
        
        bigquery_config = env_config['bigquery_config']
        
        context = {
            'environment': self.environment,
            'dataset_name': bigquery_config['dataset_id'],
            'friendly_name': f"DNA-Lang Genomic Data {self.environment.title()}",
            'description': f"{self.environment.title()} genomic analysis data",
            'location': bigquery_config['location'],
            'encryption_key': 'google_kms_crypto_key.genomic_key.id' if bigquery_config['encryption'] != 'GOOGLE_DEFAULT_ENCRYPTION' else None,
            'access_controls': bigquery_requirements.get('access_controls', [
                {'role': 'OWNER', 'user_by_email': f'dna-lang-{self.environment}-admin@company.com'},
                {'role': 'READER', 'special_group': 'projectReaders'}
            ])
        }
        
        return template.render(**context)
    
    def _generate_iam_config(self, iam_requirements: Dict[str, Any], env_config: Dict[str, Any]) -> str:
        """Generate IAM terraform configuration"""
        template = Template(self.terraform_templates['iam_template'])
        
        context = {
            'environment': self.environment,
            'service_account_name': f'dna-lang-{self.environment}-app',
            'display_name': f'DNA-Lang {self.environment.title()} Application Service Account',
            'iam_bindings': iam_requirements.get('bindings', [
                {'name': f'{self.environment}_genomics_viewer', 'role': 'roles/genomics.viewer'},
                {'name': f'{self.environment}_storage_viewer', 'role': 'roles/storage.objectViewer'},
                {'name': f'{self.environment}_bigquery_user', 'role': 'roles/bigquery.user'}
            ])
        }
        
        return template.render(**context)
    
    def _generate_monitoring_config(self, monitoring_requirements: Dict[str, Any], env_config: Dict[str, Any]) -> str:
        """Generate monitoring terraform configuration"""
        template = Template(self.terraform_templates['monitoring_template'])
        
        context = {
            'environment': self.environment,
            'policy_name': f'dna-lang-{self.environment}-alert-policy',
            'display_name': f'DNA-Lang {self.environment.title()} Alert Policy',
            'condition_name': 'High Error Rate',
            'filter': f'resource.type="gce_instance" AND resource.labels.project_id="{env_config["project_id"]}"',
            'duration': '300s',
            'comparison': 'COMPARISON_GREATER_THAN',
            'threshold_value': 0.05,
            'notification_channels': monitoring_requirements.get('notification_channels', [])
        }
        
        return template.render(**context)
    
    def _generate_variables_config(self, env_config: Dict[str, Any]) -> str:
        """Generate terraform variables configuration"""
        variables = {
            'project_id': {
                'description': 'GCP Project ID',
                'type': 'string',
                'default': env_config['project_id']
            },
            'region': {
                'description': 'GCP Region',
                'type': 'string',
                'default': env_config['region']
            },
            'environment': {
                'description': 'Environment name',
                'type': 'string',
                'default': env_config['environment']
            }
        }
        
        config_content = []
        for var_name, var_config in variables.items():
            config_content.append(f'''
variable "{var_name}" {{
  description = "{var_config['description']}"
  type        = {var_config['type']}
  default     = "{var_config['default']}"
}}''')
        
        return '\n'.join(config_content)
    
    def _generate_main_config(self, env_config: Dict[str, Any]) -> str:
        """Generate main terraform configuration"""
        backend_bucket = f"dna-lang-terraform-state-{self.environment}"
        
        return f'''# {env_config['environment'].title()} Environment Terraform Configuration
# DNA-Lang Platform - {env_config['environment'].title()} Infrastructure

terraform {{
  required_version = ">= 1.0"
  required_providers {{
    google = {{
      source  = "hashicorp/google"
      version = "~> 4.0"
    }}
  }}
  
  backend "gcs" {{
    bucket = "{backend_bucket}"
    prefix = "terraform/state"
  }}
}}

# Provider Configuration
provider "google" {{
  project = var.project_id
  region  = var.region
}}

# KMS Key Ring for encryption (if needed)
resource "google_kms_key_ring" "genomic_keyring" {{
  name     = "dna-lang-genomic-keyring-{self.environment}"
  location = "global"
}}

resource "google_kms_crypto_key" "genomic_key" {{
  name     = "dna-lang-genomic-key-{self.environment}"
  key_ring = google_kms_key_ring.genomic_keyring.id
  
  rotation_period = "7776000s"  # 90 days
}}'''
    
    def save_terraform_configs(self, configs: Dict[str, str], output_dir: Optional[str] = None) -> str:
        """Save generated terraform configurations to files"""
        if output_dir is None:
            output_dir = f"gcp-organization/terraform/{self.environment}"
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save each configuration file
        for filename, content in configs.items():
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w') as f:
                f.write(content)
            logger.info(f"Saved terraform config: {file_path}")
        
        return output_dir
    
    def validate_terraform_configs(self, config_dir: str) -> Dict[str, Any]:
        """Validate generated terraform configurations"""
        validation_result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'config_dir': config_dir
        }
        
        try:
            # Change to terraform directory
            original_cwd = os.getcwd()
            os.chdir(config_dir)
            
            # Initialize terraform
            init_result = subprocess.run(
                ['terraform', 'init', '-backend=false'],
                capture_output=True,
                text=True
            )
            
            if init_result.returncode != 0:
                validation_result['errors'].append(f"Terraform init failed: {init_result.stderr}")
                return validation_result
            
            # Validate terraform configuration
            validate_result = subprocess.run(
                ['terraform', 'validate'],
                capture_output=True,
                text=True
            )
            
            if validate_result.returncode == 0:
                validation_result['valid'] = True
                logger.info("Terraform configuration validation passed")
            else:
                validation_result['errors'].append(f"Terraform validation failed: {validate_result.stderr}")
            
            # Format check
            fmt_result = subprocess.run(
                ['terraform', 'fmt', '-check'],
                capture_output=True,
                text=True
            )
            
            if fmt_result.returncode != 0:
                validation_result['warnings'].append("Terraform formatting issues detected")
        
        except FileNotFoundError:
            validation_result['errors'].append("Terraform CLI not found")
        except Exception as e:
            validation_result['errors'].append(f"Validation error: {str(e)}")
        finally:
            # Return to original directory
            os.chdir(original_cwd)
        
        return validation_result
    
    def generate_deployment_plan(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete deployment plan with terraform configs"""
        logger.info("Generating deployment plan")
        
        # Generate terraform configurations
        configs = self.generate_infrastructure_config(requirements)
        
        # Save configurations
        config_dir = self.save_terraform_configs(configs)
        
        # Validate configurations
        validation_result = self.validate_terraform_configs(config_dir)
        
        deployment_plan = {
            'environment': self.environment,
            'config_directory': config_dir,
            'generated_files': list(configs.keys()),
            'validation': validation_result,
            'deployment_ready': validation_result['valid'],
            'requirements': requirements,
            'generated_at': datetime.utcnow().isoformat()
        }
        
        return deployment_plan
    
    def get_infrastructure_status(self) -> Dict[str, Any]:
        """Get current infrastructure status"""
        terraform_dir = f"gcp-organization/terraform/{self.environment}"
        
        status = {
            'environment': self.environment,
            'terraform_dir_exists': os.path.exists(terraform_dir),
            'config_files': [],
            'last_deployment': None
        }
        
        if status['terraform_dir_exists']:
            status['config_files'] = [
                f for f in os.listdir(terraform_dir) 
                if f.endswith('.tf')
            ]
        
        return status


# Export main components
__all__ = ['CloudArchitectAgent']