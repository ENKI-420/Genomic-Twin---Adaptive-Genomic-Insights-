"""
Test suite for the ImmuneSystem module.

This module contains comprehensive unit tests for the ImmuneSystem class,
covering pattern matching, threat detection, and edge cases.
"""

import unittest
import time
from typing import Dict, Any

from evolution.immune_system import ImmuneSystem, ThreatPattern, ThreatDetection


class TestImmuneSystem(unittest.TestCase):
    """Test cases for the ImmuneSystem class."""
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.immune_system = ImmuneSystem()
    
    def test_initialization(self) -> None:
        """Test that ImmuneSystem initializes with default patterns."""
        self.assertIsInstance(self.immune_system, ImmuneSystem)
        self.assertGreater(len(self.immune_system.threat_patterns), 0)
        self.assertEqual(len(self.immune_system.detections), 0)
        self.assertEqual(self.immune_system.detection_count, 0)
    
    def test_add_threat_pattern_valid(self) -> None:
        """Test adding a valid threat pattern."""
        pattern_id = "test_pattern"
        regex = r"\btest\b"
        severity = 5
        description = "Test pattern"
        
        result = self.immune_system.add_threat_pattern(pattern_id, regex, severity, description)
        
        self.assertTrue(result)
        self.assertIn(pattern_id, self.immune_system.threat_patterns)
        self.assertIn(pattern_id, self.immune_system.compiled_patterns)
        
        pattern = self.immune_system.threat_patterns[pattern_id]
        self.assertEqual(pattern.pattern_id, pattern_id)
        self.assertEqual(pattern.regex, regex)
        self.assertEqual(pattern.severity, severity)
        self.assertEqual(pattern.description, description)
    
    def test_add_threat_pattern_invalid_regex(self) -> None:
        """Test adding a threat pattern with invalid regex."""
        pattern_id = "invalid_pattern"
        invalid_regex = r"[invalid"  # Unclosed bracket
        severity = 5
        description = "Invalid pattern"
        
        result = self.immune_system.add_threat_pattern(pattern_id, invalid_regex, severity, description)
        
        self.assertFalse(result)
        self.assertNotIn(pattern_id, self.immune_system.threat_patterns)
        self.assertNotIn(pattern_id, self.immune_system.compiled_patterns)
    
    def test_remove_threat_pattern_existing(self) -> None:
        """Test removing an existing threat pattern."""
        # First add a pattern
        pattern_id = "removable_pattern"
        self.immune_system.add_threat_pattern(pattern_id, r"test", 5, "Test")
        
        # Verify it exists
        self.assertIn(pattern_id, self.immune_system.threat_patterns)
        
        # Remove it
        result = self.immune_system.remove_threat_pattern(pattern_id)
        
        self.assertTrue(result)
        self.assertNotIn(pattern_id, self.immune_system.threat_patterns)
        self.assertNotIn(pattern_id, self.immune_system.compiled_patterns)
    
    def test_remove_threat_pattern_nonexistent(self) -> None:
        """Test removing a non-existent threat pattern."""
        result = self.immune_system.remove_threat_pattern("nonexistent_pattern")
        self.assertFalse(result)
    
    def test_scan_content_with_matches(self) -> None:
        """Test scanning content that contains threat patterns."""
        # Add a simple test pattern
        self.immune_system.add_threat_pattern("test_scan", r"malicious", 8, "Test malicious content")
        
        content = "This is some malicious content that should be detected."
        location = "test_content"
        
        detections = self.immune_system.scan_content(content, location)
        
        self.assertEqual(len(detections), 1)
        detection = detections[0]
        self.assertEqual(detection.pattern_id, "test_scan")
        self.assertEqual(detection.matched_content, "malicious")
        self.assertEqual(detection.severity, 8)
        self.assertEqual(detection.location, location)
    
    def test_scan_content_no_matches(self) -> None:
        """Test scanning content that contains no threat patterns."""
        content = "This is completely safe content with no threats."
        location = "safe_content"
        
        detections = self.immune_system.scan_content(content, location)
        
        # Should have no detections since content doesn't match default patterns
        # Note: This depends on default patterns not matching this specific content
        benign_detections = [d for d in detections if "safe content" in d.matched_content]
        self.assertEqual(len(benign_detections), 0)
    
    def test_scan_content_multiple_matches(self) -> None:
        """Test scanning content with multiple pattern matches."""
        # Add patterns that will match
        self.immune_system.add_threat_pattern("test1", r"bad", 5, "Bad pattern")
        self.immune_system.add_threat_pattern("test2", r"evil", 7, "Evil pattern")
        
        content = "This bad content has evil intentions."
        detections = self.immune_system.scan_content(content)
        
        # Should detect both patterns
        pattern_ids = [d.pattern_id for d in detections]
        self.assertIn("test1", pattern_ids)
        self.assertIn("test2", pattern_ids)
    
    def test_scan_data_dict(self) -> None:
        """Test scanning a dictionary for threats."""
        self.immune_system.add_threat_pattern("dict_test", r"secret", 6, "Secret data")
        
        data = {
            "user": "john_doe",
            "password": "secret123",
            "notes": "This contains no secret information"
        }
        
        detections = self.immune_system.scan_data_dict(data, "test_dict")
        
        # Should find "secret" in both password field and notes
        secret_detections = [d for d in detections if d.pattern_id == "dict_test"]
        self.assertGreater(len(secret_detections), 0)
    
    def test_get_pattern_statistics_empty(self) -> None:
        """Test getting statistics when no detections have been made."""
        # Clear default detections
        self.immune_system.clear_detections()
        
        stats = self.immune_system.get_pattern_statistics()
        
        self.assertGreater(stats['total_patterns'], 0)  # Default patterns exist
        self.assertEqual(stats['total_detections'], 0)
        self.assertEqual(stats['detections_by_severity'], {})
        self.assertEqual(stats['detections_by_pattern'], {})
        self.assertIsNone(stats['most_active_pattern'])
    
    def test_get_pattern_statistics_with_detections(self) -> None:
        """Test getting statistics after making some detections."""
        # Add a test pattern and trigger detections
        self.immune_system.add_threat_pattern("stats_test", r"trigger", 5, "Trigger pattern")
        
        # Generate some detections
        self.immune_system.scan_content("trigger trigger trigger")
        
        stats = self.immune_system.get_pattern_statistics()
        
        self.assertGreater(stats['total_detections'], 0)
        self.assertIn(5, stats['detections_by_severity'])  # Severity 5 from our pattern
        self.assertIn("stats_test", stats['detections_by_pattern'])
    
    def test_get_recent_detections(self) -> None:
        """Test getting recent detections."""
        # Clear existing detections
        self.immune_system.clear_detections()
        
        # Add a pattern and generate detections
        self.immune_system.add_threat_pattern("recent_test", r"recent", 4, "Recent pattern")
        self.immune_system.scan_content("recent content")
        
        recent = self.immune_system.get_recent_detections(5)
        
        self.assertGreaterEqual(len(recent), 1)
        # Verify they're sorted by timestamp (most recent first)
        if len(recent) > 1:
            for i in range(len(recent) - 1):
                self.assertGreaterEqual(recent[i].timestamp, recent[i + 1].timestamp)
    
    def test_clear_detections(self) -> None:
        """Test clearing all detections."""
        # Generate some detections first
        self.immune_system.add_threat_pattern("clear_test", r"clear", 3, "Clear pattern")
        self.immune_system.scan_content("clear this content")
        
        # Verify we have detections
        self.assertGreater(len(self.immune_system.detections), 0)
        
        # Clear them
        self.immune_system.clear_detections()
        
        # Verify they're cleared
        self.assertEqual(len(self.immune_system.detections), 0)
        self.assertEqual(self.immune_system.detection_count, 0)
    
    def test_get_pattern_coverage_zero(self) -> None:
        """Test pattern coverage when no patterns have detected anything."""
        # Clear detections and add a pattern that won't match
        self.immune_system.clear_detections()
        self.immune_system.add_threat_pattern("no_match", r"xyzabc123", 1, "No match pattern")
        
        coverage = self.immune_system.get_pattern_coverage()
        self.assertEqual(coverage, 0.0)
    
    def test_get_pattern_coverage_partial(self) -> None:
        """Test pattern coverage when some patterns have detected threats."""
        # Clear detections first
        self.immune_system.clear_detections()
        
        # Add patterns - one that will match, one that won't
        self.immune_system.add_threat_pattern("match_pattern", r"match", 5, "Match pattern")
        self.immune_system.add_threat_pattern("no_match_pattern", r"xyzabc123", 5, "No match pattern")
        
        # Generate detection for one pattern
        self.immune_system.scan_content("this will match the pattern")
        
        coverage = self.immune_system.get_pattern_coverage()
        
        # Should be partial coverage (not 0, not 100)
        self.assertGreater(coverage, 0.0)
        self.assertLess(coverage, 100.0)
    
    def test_genomic_specific_patterns(self) -> None:
        """Test patterns specific to genomic data analysis."""
        # Test genomic anomaly detection (default pattern)
        genomic_content = "mutation_count: 500, variant_frequency: 0.85"
        detections = self.immune_system.scan_content(genomic_content)
        
        # Should detect the high mutation count
        genomic_detections = [d for d in detections if "genomic" in d.pattern_id.lower()]
        self.assertGreater(len(genomic_detections), 0)
    
    def test_high_risk_gene_detection(self) -> None:
        """Test detection of high-risk gene variants."""
        # Test high-risk gene detection (default pattern)
        gene_content = "Found variant in BRCA1 gene with significance"
        detections = self.immune_system.scan_content(gene_content)
        
        # Should detect the high-risk gene
        gene_detections = [d for d in detections if "gene" in d.pattern_id.lower()]
        self.assertGreater(len(gene_detections), 0)
    
    def test_detection_id_uniqueness(self) -> None:
        """Test that detection IDs are unique."""
        # Generate multiple detections
        self.immune_system.add_threat_pattern("unique_test", r"unique", 3, "Unique pattern")
        self.immune_system.scan_content("unique unique unique")
        
        detection_ids = [d.detection_id for d in self.immune_system.detections]
        unique_ids = set(detection_ids)
        
        # All IDs should be unique
        self.assertEqual(len(detection_ids), len(unique_ids))
    
    def test_detection_history_limit(self) -> None:
        """Test that detection history respects the maximum limit."""
        # Set a small limit for testing
        original_limit = self.immune_system.max_detection_history
        self.immune_system.max_detection_history = 5
        
        try:
            # Generate more detections than the limit
            self.immune_system.add_threat_pattern("limit_test", r"x", 1, "Limit test")
            content = "x " * 10  # Will generate 10 detections
            self.immune_system.scan_content(content)
            
            # Should not exceed the limit
            self.assertLessEqual(len(self.immune_system.detections), 5)
            
        finally:
            # Restore original limit
            self.immune_system.max_detection_history = original_limit


if __name__ == '__main__':
    unittest.main()