"""
Google Cloud Authentication Module for Genomic Twin Platform
Provides authentication functionality for Google Cloud services including BigQuery
"""
import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Google Cloud imports with fallback for development/testing
try:
    from google.auth import default
    from google.auth.exceptions import DefaultCredentialsError
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False
    logging.warning("Google Cloud SDK not installed. Some features may be limited.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GCloudAuth:
    """Google Cloud Authentication Manager"""
    
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        self.credentials = None
        self._authenticated = False
        
    def authenticate(self, method: str = 'default') -> bool:
        """
        Authenticate with Google Cloud
        
        Args:
            method: Authentication method ('default', 'service_account', 'oauth')
        
        Returns:
            bool: True if authentication successful
        """
        if not GOOGLE_CLOUD_AVAILABLE:
            logger.error("Google Cloud SDK not available. Install google-cloud-bigquery and dependencies.")
            return False
            
        try:
            if method == 'default':
                self.credentials, project = default()
                self.project_id = self.project_id or project
            elif method == 'service_account':
                self.credentials = self._load_service_account_credentials()
            elif method == 'oauth':
                self.credentials = self._oauth_login()
            else:
                raise ValueError(f"Unknown authentication method: {method}")
                
            self._authenticated = True
            logger.info(f"Successfully authenticated with Google Cloud (project: {self.project_id})")
            return True
            
        except DefaultCredentialsError as e:
            logger.error(f"Authentication failed: {e}")
            logger.info("Run 'gcloud auth login' or set up service account credentials")
            return False
        except Exception as e:
            logger.error(f"Unexpected authentication error: {e}")
            return False
    
    def _load_service_account_credentials(self):
        """Load service account credentials from environment or file"""
        # Try environment variable first
        creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        if creds_json:
            try:
                creds_dict = json.loads(creds_json)
                return service_account.Credentials.from_service_account_info(creds_dict)
            except json.JSONDecodeError:
                logger.error("Invalid JSON in GOOGLE_APPLICATION_CREDENTIALS_JSON")
        
        # Try file path
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if creds_path and Path(creds_path).exists():
            return service_account.Credentials.from_service_account_file(creds_path)
        
        raise FileNotFoundError("Service account credentials not found")
    
    def _oauth_login(self):
        """Interactive OAuth login (requires browser)"""
        # This would typically use google-auth-oauthlib flow
        logger.info("OAuth login not implemented. Use 'gcloud auth login' instead.")
        raise NotImplementedError("Use gcloud auth login or service account authentication")
    
    def is_authenticated(self) -> bool:
        """Check if currently authenticated"""
        return self._authenticated and self.credentials is not None
    
    def get_credentials(self):
        """Get current credentials object"""
        if not self.is_authenticated():
            self.authenticate()
        return self.credentials
    
    def get_project_id(self) -> Optional[str]:
        """Get current project ID"""
        return self.project_id
    
    def refresh_credentials(self) -> bool:
        """Refresh expired credentials"""
        if not self.credentials:
            return self.authenticate()
            
        try:
            self.credentials.refresh(Request())
            return True
        except Exception as e:
            logger.error(f"Failed to refresh credentials: {e}")
            return self.authenticate()
    
    def set_project(self, project_id: str):
        """Set the Google Cloud project ID"""
        self.project_id = project_id
        logger.info(f"Project set to: {project_id}")


# Global authentication instance
_auth_instance = None

def get_auth_instance() -> GCloudAuth:
    """Get the global authentication instance"""
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = GCloudAuth()
    return _auth_instance

def gcloud_login(method: str = 'default', project_id: Optional[str] = None) -> bool:
    """
    Convenient function to perform gcloud authentication
    
    Args:
        method: Authentication method ('default', 'service_account', 'oauth')
        project_id: Optional project ID to set
        
    Returns:
        bool: True if authentication successful
    """
    auth = get_auth_instance()
    if project_id:
        auth.set_project(project_id)
    return auth.authenticate(method)

def is_authenticated() -> bool:
    """Check if gcloud is authenticated"""
    return get_auth_instance().is_authenticated()

def get_credentials():
    """Get current Google Cloud credentials"""
    return get_auth_instance().get_credentials()

def get_project_id() -> Optional[str]:
    """Get current Google Cloud project ID"""
    return get_auth_instance().get_project_id()

def setup_authentication_instructions():
    """Print setup instructions for Google Cloud authentication"""
    instructions = """
    Google Cloud Authentication Setup:
    
    Option 1: Use gcloud CLI (Recommended for development)
    1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
    2. Run: gcloud auth login
    3. Run: gcloud config set project YOUR_PROJECT_ID
    
    Option 2: Service Account (Recommended for production)
    1. Create a service account in Google Cloud Console
    2. Download the JSON key file
    3. Set environment variable: export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
    
    Option 3: Environment Variable (Alternative)
    1. Set GOOGLE_APPLICATION_CREDENTIALS_JSON with the JSON content directly
    2. Set GOOGLE_CLOUD_PROJECT with your project ID
    """
    print(instructions)
    return instructions