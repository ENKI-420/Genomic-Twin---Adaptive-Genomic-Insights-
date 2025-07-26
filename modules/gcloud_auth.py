# Google Cloud Authentication module for the platform
import os
import subprocess
import json
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_authenticated() -> bool:
    """Check if Google Cloud is authenticated"""
    try:
        # Check for service account key file
        if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            if os.path.exists(os.getenv('GOOGLE_APPLICATION_CREDENTIALS')):
                logger.info("Service account authentication detected")
                return True
        
        # Check gcloud CLI authentication
        result = subprocess.run(
            ['gcloud', 'auth', 'list', '--filter=status:ACTIVE', '--format=json'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            accounts = json.loads(result.stdout)
            if accounts:
                logger.info(f"Active gcloud account found: {accounts[0].get('account', 'Unknown')}")
                return True
        
        return False
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Authentication check failed: {str(e)}")
        return False

def gcloud_login(method: str = 'default') -> bool:
    """
    Authenticate with Google Cloud
    
    Args:
        method: 'default' for gcloud CLI, 'service_account' for service account key
    
    Returns:
        bool: True if authentication successful, False otherwise
    """
    try:
        if method == 'service_account':
            # Check for service account key file in environment
            key_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if not key_file:
                logger.error("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
                return False
            
            if not os.path.exists(key_file):
                logger.error(f"Service account key file not found: {key_file}")
                return False
            
            # Activate service account
            result = subprocess.run(
                ['gcloud', 'auth', 'activate-service-account', '--key-file', key_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info("Service account authentication successful")
                return True
            else:
                logger.error(f"Service account authentication failed: {result.stderr}")
                return False
        
        else:  # default method
            # Try application default credentials first
            result = subprocess.run(
                ['gcloud', 'auth', 'application-default', 'login', '--no-launch-browser'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                logger.info("Application default credentials authentication successful")
                return True
            else:
                logger.warning(f"Application default login failed: {result.stderr}")
                # Fallback to regular gcloud auth
                result = subprocess.run(
                    ['gcloud', 'auth', 'login', '--no-launch-browser'],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    logger.info("Gcloud authentication successful")
                    return True
                else:
                    logger.error(f"Gcloud authentication failed: {result.stderr}")
                    return False
    
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Authentication process failed: {str(e)}")
        return False

def setup_authentication_instructions() -> str:
    """
    Return setup instructions for Google Cloud authentication
    
    Returns:
        str: Formatted instructions for setting up authentication
    """
    instructions = """
Google Cloud Authentication Setup Instructions:

METHOD 1: gcloud CLI (Recommended for development)
1. Install Google Cloud SDK:
   - Visit: https://cloud.google.com/sdk/docs/install
   - Follow installation instructions for your OS

2. Initialize and authenticate:
   $ gcloud init
   $ gcloud auth login
   $ gcloud auth application-default login

METHOD 2: Service Account (Recommended for production)
1. Create a service account in Google Cloud Console:
   - Go to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Assign necessary roles (BigQuery Data Viewer, Storage Object Viewer, etc.)

2. Download the JSON key file:
   - Click on the service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key" > "JSON"

3. Set environment variable:
   $ export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

METHOD 3: Workload Identity (For GKE/Cloud Run)
1. Configure workload identity for your cluster
2. Bind Kubernetes service account to Google service account
3. No additional authentication needed in application

TROUBLESHOOTING:
- Ensure your Google Cloud project is set: gcloud config set project YOUR_PROJECT_ID
- Check permissions: gcloud auth list
- Verify project access: gcloud projects list
- For BigQuery: Ensure you have BigQuery Data Viewer role
- For Cloud Storage: Ensure you have Storage Object Viewer role

ENVIRONMENT VARIABLES:
- GOOGLE_APPLICATION_CREDENTIALS: Path to service account key file
- GOOGLE_CLOUD_PROJECT: Your Google Cloud project ID
- GOOGLE_APPLICATION_CREDENTIALS_JSON: Base64 encoded service account JSON (alternative)

For more help, visit: https://cloud.google.com/docs/authentication
"""
    return instructions.strip()

def get_current_project() -> Optional[str]:
    """Get the current Google Cloud project ID"""
    try:
        result = subprocess.run(
            ['gcloud', 'config', 'get-value', 'project'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        
        # Fallback to environment variable
        return os.getenv('GOOGLE_CLOUD_PROJECT')
    
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        return os.getenv('GOOGLE_CLOUD_PROJECT')

def get_authentication_status() -> dict:
    """Get detailed authentication status information"""
    status = {
        'authenticated': False,
        'method': None,
        'account': None,
        'project': None
    }
    
    try:
        # Check service account
        if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            key_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if os.path.exists(key_file):
                status['authenticated'] = True
                status['method'] = 'service_account'
                status['account'] = 'Service Account'
        
        # Check gcloud CLI
        if not status['authenticated']:
            result = subprocess.run(
                ['gcloud', 'auth', 'list', '--filter=status:ACTIVE', '--format=json'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                accounts = json.loads(result.stdout)
                if accounts:
                    status['authenticated'] = True
                    status['method'] = 'gcloud_cli'
                    status['account'] = accounts[0].get('account', 'Unknown')
        
        # Get project
        status['project'] = get_current_project()
        
    except Exception as e:
        logger.warning(f"Status check failed: {str(e)}")
    
    return status