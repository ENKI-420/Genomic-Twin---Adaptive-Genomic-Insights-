"""
Test suite for the gene library.

This module contains unit tests for all gene implementations
in the evolution framework.
"""

import unittest
import logging
import time
from unittest.mock import patch

from evolution.genes import Gene, AuthenticationGene, PerformanceGene, LoggingVerbosityGene


class TestBaseGene(unittest.TestCase):
    """Test cases for the base Gene class."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        # Create a concrete implementation for testing
        class TestGene(Gene):
            def execute(self, context):
                return {"result": "test"}
        
        self.test_gene = TestGene("test_gene", "1.0")
    
    def test_initialization(self) -> None:
        """Test gene initialization."""
        self.assertEqual(self.test_gene.name, "test_gene")
        self.assertEqual(self.test_gene.version, "1.0")
        self.assertTrue(self.test_gene.active)
    
    def test_activate_deactivate(self) -> None:
        """Test gene activation and deactivation."""
        self.assertTrue(self.test_gene.is_active())
        
        self.test_gene.deactivate()
        self.assertFalse(self.test_gene.is_active())
        
        self.test_gene.activate()
        self.assertTrue(self.test_gene.is_active())
    
    def test_repr(self) -> None:
        """Test string representation."""
        repr_str = repr(self.test_gene)
        self.assertIn("TestGene", repr_str)
        self.assertIn("test_gene", repr_str)
        self.assertIn("1.0", repr_str)
        self.assertIn("active", repr_str)


class TestAuthenticationGene(unittest.TestCase):
    """Test cases for the AuthenticationGene class."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.auth_gene = AuthenticationGene()
    
    def test_initialization(self) -> None:
        """Test authentication gene initialization."""
        self.assertEqual(self.auth_gene.name, "authentication_gene")
        self.assertEqual(self.auth_gene.session_timeout, 3600)
        self.assertEqual(self.auth_gene.max_login_attempts, 3)
    
    def test_successful_login(self) -> None:
        """Test successful login."""
        context = {
            'action': 'login',
            'username': 'testuser',
            'password': 'validpassword123'
        }
        
        result = self.auth_gene.execute(context)
        
        self.assertTrue(result['success'])
        self.assertIn('session_token', result)
        self.assertIn('expires_at', result)
        self.assertEqual(len(result['session_token']), 64)  # SHA256 hash length
    
    def test_failed_login_short_password(self) -> None:
        """Test failed login with short password."""
        context = {
            'action': 'login',
            'username': 'testuser',
            'password': 'short'
        }
        
        result = self.auth_gene.execute(context)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_failed_login_missing_credentials(self) -> None:
        """Test failed login with missing credentials."""
        context = {
            'action': 'login',
            'username': 'testuser'
            # Missing password
        }
        
        result = self.auth_gene.execute(context)
        
        self.assertFalse(result['success'])
        self.assertIn('Username and password required', result['error'])
    
    def test_logout(self) -> None:
        """Test logout functionality."""
        context = {'action': 'logout'}
        
        result = self.auth_gene.execute(context)
        
        self.assertTrue(result['success'])
        self.assertIn('message', result)
    
    def test_session_validation_missing_token(self) -> None:
        """Test session validation with missing token."""
        context = {'action': 'validate_session'}
        
        result = self.auth_gene.execute(context)
        
        self.assertFalse(result['success'])
        self.assertIn('Session token required', result['error'])
    
    def test_session_validation_valid_token(self) -> None:
        """Test session validation with valid token."""
        # First login to get a token
        login_context = {
            'action': 'login',
            'username': 'testuser',
            'password': 'validpassword123'
        }
        login_result = self.auth_gene.execute(login_context)
        token = login_result['session_token']
        
        # Then validate the token
        validate_context = {
            'action': 'validate_session',
            'session_token': token
        }
        
        result = self.auth_gene.execute(validate_context)
        
        self.assertTrue(result['success'])
        self.assertTrue(result['valid'])
    
    def test_unknown_action(self) -> None:
        """Test unknown action handling."""
        context = {'action': 'unknown_action'}
        
        result = self.auth_gene.execute(context)
        
        self.assertFalse(result['success'])
        self.assertIn('Unknown action', result['error'])


class TestPerformanceGene(unittest.TestCase):
    """Test cases for the PerformanceGene class."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.perf_gene = PerformanceGene()
    
    def test_initialization(self) -> None:
        """Test performance gene initialization."""
        self.assertEqual(self.perf_gene.name, "performance_gene")
        self.assertEqual(self.perf_gene.max_history_size, 100)
        self.assertEqual(self.perf_gene.performance_threshold, 80.0)
        self.assertEqual(len(self.perf_gene.metrics_history), 0)
    
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    @patch('psutil.net_connections')
    @patch('psutil.pids')
    def test_monitor_performance(self, mock_pids, mock_net, mock_disk, mock_memory, mock_cpu):
        """Test performance monitoring."""
        # Mock system metrics
        mock_cpu.return_value = 45.0
        mock_memory.return_value.percent = 60.0
        mock_disk.return_value.percent = 50.0
        mock_net.return_value = [1, 2, 3]  # 3 connections
        mock_pids.return_value = [1, 2, 3, 4, 5]  # 5 processes
        
        context = {'action': 'monitor', 'duration': 1}
        
        result = self.perf_gene.execute(context)
        
        self.assertTrue(result['success'])
        self.assertIn('metrics', result)
        self.assertIn('issues', result)
        self.assertIn('recommendations', result)
        
        metrics = result['metrics']
        self.assertEqual(metrics['cpu_percent'], 45.0)
        self.assertEqual(metrics['memory_percent'], 60.0)
        self.assertEqual(metrics['disk_percent'], 50.0)
    
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    @patch('psutil.net_connections')
    @patch('psutil.pids')
    def test_optimize_performance(self, mock_pids, mock_net, mock_disk, mock_memory, mock_cpu):
        """Test performance optimization."""
        # Mock high CPU usage
        mock_cpu.return_value = 85.0  # Above threshold
        mock_memory.return_value.percent = 85.0  # Above threshold
        mock_disk.return_value.percent = 50.0
        mock_net.return_value = []
        mock_pids.return_value = []
        
        context = {'action': 'optimize'}
        
        result = self.perf_gene.execute(context)
        
        self.assertTrue(result['success'])
        self.assertIn('optimizations_applied', result)
        self.assertIn('metrics_before', result)
        self.assertIn('metrics_after', result)
        
        # Should have applied optimizations for high CPU and memory
        optimizations = result['optimizations_applied']
        self.assertGreater(len(optimizations), 0)
    
    def test_get_metrics_summary_empty(self) -> None:
        """Test getting metrics summary with no data."""
        context = {'action': 'get_metrics'}
        
        result = self.perf_gene.execute(context)
        
        self.assertFalse(result['success'])
        self.assertIn('No metrics available', result['error'])
    
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    @patch('psutil.net_connections')
    @patch('psutil.pids')
    def test_get_metrics_summary_with_data(self, mock_pids, mock_net, mock_disk, mock_memory, mock_cpu):
        """Test getting metrics summary with data."""
        # Mock system metrics
        mock_cpu.return_value = 45.0
        mock_memory.return_value.percent = 60.0
        mock_disk.return_value.percent = 50.0
        mock_net.return_value = []
        mock_pids.return_value = []
        
        # First monitor to collect some data
        monitor_context = {'action': 'monitor'}
        self.perf_gene.execute(monitor_context)
        
        # Then get summary
        context = {'action': 'get_metrics'}
        result = self.perf_gene.execute(context)
        
        self.assertTrue(result['success'])
        self.assertIn('total_measurements', result)
        self.assertIn('latest_metrics', result)
        self.assertIn('average_cpu', result)
        self.assertIn('average_memory', result)
        self.assertIn('average_disk', result)
        
        self.assertEqual(result['total_measurements'], 1)
        self.assertEqual(result['average_cpu'], 45.0)
    
    def test_unknown_action(self) -> None:
        """Test unknown action handling."""
        context = {'action': 'unknown_action'}
        
        result = self.perf_gene.execute(context)
        
        self.assertFalse(result['success'])
        self.assertIn('Unknown action', result['error'])


class TestLoggingVerbosityGene(unittest.TestCase):
    """Test cases for the LoggingVerbosityGene class."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.logging_gene = LoggingVerbosityGene()
        # Store original root logger level to restore later
        self.original_level = logging.getLogger().getEffectiveLevel()
    
    def tearDown(self) -> None:
        """Clean up after tests."""
        # Restore original logging level
        logging.getLogger().setLevel(self.original_level)
    
    def test_initialization(self) -> None:
        """Test logging gene initialization."""
        self.assertEqual(self.logging_gene.name, "logging_verbosity_gene")
        self.assertEqual(self.logging_gene.current_level, 'INFO')
        self.assertIsNone(self.logging_gene.previous_level)
        self.assertEqual(len(self.logging_gene.level_history), 0)
    
    def test_set_logging_level_valid(self) -> None:
        """Test setting a valid logging level."""
        context = {
            'action': 'set_level',
            'level': 'DEBUG'
        }
        
        result = self.logging_gene.execute(context)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['new_level'], 'DEBUG')
        self.assertIn('previous_level', result)
        self.assertEqual(self.logging_gene.current_level, 'DEBUG')
        
        # Verify the actual logging level was changed
        self.assertEqual(logging.getLogger().getEffectiveLevel(), logging.DEBUG)
    
    def test_set_logging_level_invalid(self) -> None:
        """Test setting an invalid logging level."""
        context = {
            'action': 'set_level',
            'level': 'INVALID'
        }
        
        result = self.logging_gene.execute(context)
        
        self.assertFalse(result['success'])
        self.assertIn('Invalid logging level', result['error'])
    
    def test_get_logging_level(self) -> None:
        """Test getting the current logging level."""
        context = {'action': 'get_level'}
        
        result = self.logging_gene.execute(context)
        
        self.assertTrue(result['success'])
        self.assertIn('current_level', result)
        self.assertIn('numeric_level', result)
        self.assertIn('logger_name', result)
        self.assertEqual(result['logger_name'], 'root')
    
    def test_reset_logging_level(self) -> None:
        """Test resetting to previous logging level."""
        # First set a level
        set_context = {
            'action': 'set_level',
            'level': 'ERROR'
        }
        self.logging_gene.execute(set_context)
        
        # Then reset
        reset_context = {'action': 'reset_level'}
        result = self.logging_gene.execute(reset_context)
        
        self.assertTrue(result['success'])
        self.assertIn('reset to previous level', result['message'])
    
    def test_reset_without_previous_level(self) -> None:
        """Test resetting when no previous level exists."""
        # Clear previous level
        self.logging_gene.previous_level = None
        
        context = {'action': 'reset_level'}
        result = self.logging_gene.execute(context)
        
        self.assertFalse(result['success'])
        self.assertIn('No previous logging level', result['error'])
    
    def test_get_level_history(self) -> None:
        """Test getting the logging level history."""
        # Make some level changes first
        self.logging_gene.execute({'action': 'set_level', 'level': 'DEBUG'})
        self.logging_gene.execute({'action': 'set_level', 'level': 'ERROR'})
        
        context = {'action': 'get_history'}
        result = self.logging_gene.execute(context)
        
        self.assertTrue(result['success'])
        self.assertIn('level_history', result)
        self.assertIn('current_level', result)
        self.assertIn('previous_level', result)
        
        # Should have at least 2 entries in history
        self.assertGreaterEqual(len(result['level_history']), 2)
    
    def test_specific_logger_modification(self) -> None:
        """Test modifying a specific logger instead of root."""
        logger_name = "test.logger"
        context = {
            'action': 'set_level',
            'level': 'DEBUG',
            'logger_name': logger_name
        }
        
        result = self.logging_gene.execute(context)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['logger_name'], logger_name)
        
        # Verify the specific logger was modified
        test_logger = logging.getLogger(logger_name)
        self.assertEqual(test_logger.getEffectiveLevel(), logging.DEBUG)
    
    def test_level_history_limit(self) -> None:
        """Test that level history respects the limit."""
        # Make many level changes
        for i in range(60):  # More than the 50-entry limit
            level = 'DEBUG' if i % 2 == 0 else 'INFO'
            self.logging_gene.execute({'action': 'set_level', 'level': level})
        
        # Check that history is limited
        self.assertLessEqual(len(self.logging_gene.level_history), 50)
    
    def test_unknown_action(self) -> None:
        """Test unknown action handling."""
        context = {'action': 'unknown_action'}
        
        result = self.logging_gene.execute(context)
        
        self.assertFalse(result['success'])
        self.assertIn('Unknown action', result['error'])
    
    def test_level_mapping_completeness(self) -> None:
        """Test that all expected logging levels are mapped."""
        expected_levels = ['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL']
        
        for level in expected_levels:
            self.assertIn(level, LoggingVerbosityGene.LEVEL_MAPPING)
            self.assertIsInstance(LoggingVerbosityGene.LEVEL_MAPPING[level], int)


if __name__ == '__main__':
    unittest.main()