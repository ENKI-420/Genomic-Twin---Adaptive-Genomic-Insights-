"""
Tests for Google Cloud Authentication module
"""
import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from modules.gcloud_auth import GCloudAuth, gcloud_login, is_authenticated, get_project_id


class TestGCloudAuth(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.auth = GCloudAuth(project_id='test-project')
    
    def test_init(self):
        """Test GCloudAuth initialization"""
        self.assertEqual(self.auth.project_id, 'test-project')
        self.assertFalse(self.auth._authenticated)
        self.assertIsNone(self.auth.credentials)
    
    def test_set_project(self):
        """Test setting project ID"""
        self.auth.set_project('new-project')
        self.assertEqual(self.auth.project_id, 'new-project')
    
    def test_is_authenticated_false(self):
        """Test authentication status when not authenticated"""
        self.assertFalse(self.auth.is_authenticated())
    
    @patch.dict(os.environ, {'GOOGLE_CLOUD_PROJECT': 'env-project'})
    def test_init_with_env_project(self):
        """Test initialization with environment project"""
        auth = GCloudAuth()
        self.assertEqual(auth.project_id, 'env-project')
    
    def test_authentication_without_gcloud_sdk(self):
        """Test authentication when Google Cloud SDK is not available"""
        # This test runs in environment where google-cloud might not be installed
        result = self.auth.authenticate()
        # Should handle gracefully whether SDK is available or not
        self.assertIsInstance(result, bool)
    
    def test_convenience_functions(self):
        """Test convenience functions"""
        # These should not raise exceptions
        auth_status = is_authenticated()
        self.assertIsInstance(auth_status, bool)
        
        project = get_project_id()
        # project can be None or string
        self.assertTrue(project is None or isinstance(project, str))
    
    @patch('modules.gcloud_auth.GOOGLE_CLOUD_AVAILABLE', False)
    def test_authenticate_no_sdk(self):
        """Test authentication when SDK is not available"""
        result = self.auth.authenticate()
        self.assertFalse(result)
    
    def test_setup_instructions(self):
        """Test that setup instructions are provided"""
        from modules.gcloud_auth import setup_authentication_instructions
        instructions = setup_authentication_instructions()
        self.assertIsInstance(instructions, str)
        self.assertIn('gcloud auth login', instructions)
        self.assertIn('service account', instructions.lower())


class TestGCloudCLI(unittest.TestCase):
    """Test the CLI interface"""
    
    def test_cli_script_exists(self):
        """Test that CLI script exists and is readable"""
        cli_path = project_root / 'gcloud_cli.py'
        self.assertTrue(cli_path.exists())
        self.assertTrue(cli_path.is_file())
    
    def test_cli_imports(self):
        """Test that CLI script imports work"""
        try:
            import gcloud_cli
            self.assertTrue(hasattr(gcloud_cli, 'main'))
        except ImportError as e:
            self.fail(f"CLI imports failed: {e}")


class TestCRISPRIntegration(unittest.TestCase):
    """Test CRISPR AI module integration with authentication"""
    
    def test_crispr_imports(self):
        """Test that CRISPR module imports with new authentication"""
        try:
            from modules.crispr_ai import check_gcloud_auth, authenticate_gcloud
            self.assertTrue(callable(check_gcloud_auth))
            self.assertTrue(callable(authenticate_gcloud))
        except ImportError as e:
            self.fail(f"CRISPR auth integration failed: {e}")
    
    def test_crispr_analyzer_creation(self):
        """Test that CRISPR analyzer can be created"""
        try:
            from modules.crispr_ai import ProductionCRISPRAnalyzer
            analyzer = ProductionCRISPRAnalyzer()
            self.assertIsNotNone(analyzer)
            self.assertIsNotNone(analyzer.auth)
        except Exception as e:
            self.fail(f"CRISPR analyzer creation failed: {e}")


if __name__ == '__main__':
    unittest.main()