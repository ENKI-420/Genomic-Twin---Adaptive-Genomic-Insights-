#!/usr/bin/env python3
"""
Manual test script to demonstrate the evolution framework functionality.

This script exercises the key features of the implemented evolution framework
to verify that all components work correctly.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evolution.immune_system import ImmuneSystem
from evolution.genes import AuthenticationGene, PerformanceGene, LoggingVerbosityGene


def test_immune_system():
    """Test the ImmuneSystem functionality."""
    print("=" * 50)
    print("TESTING IMMUNE SYSTEM")
    print("=" * 50)
    
    immune = ImmuneSystem()
    
    # Test scanning genomic content
    genomic_data = {
        "patient_id": "P001",
        "mutations": "BRCA1 variant detected with mutation_count: 850",
        "analysis": "High-risk genetic profile identified"
    }
    
    print("Scanning genomic data for threats...")
    detections = immune.scan_data_dict(genomic_data, "patient_data")
    
    print(f"Found {len(detections)} potential threats:")
    for detection in detections:
        print(f"  - {detection.pattern_id}: {detection.matched_content} (severity: {detection.severity})")
    
    # Get statistics
    stats = immune.get_pattern_statistics()
    print(f"\nImmune System Statistics:")
    print(f"  Total patterns: {stats['total_patterns']}")
    print(f"  Total detections: {stats['total_detections']}")
    print(f"  Pattern coverage: {immune.get_pattern_coverage():.1f}%")
    
    return len(detections) > 0


def test_authentication_gene():
    """Test the AuthenticationGene functionality."""
    print("\n" + "=" * 50)
    print("TESTING AUTHENTICATION GENE")
    print("=" * 50)
    
    auth_gene = AuthenticationGene()
    
    # Test successful login
    print("Testing successful login...")
    login_result = auth_gene.execute({
        'action': 'login',
        'username': 'genomic_user',
        'password': 'secure_password123'
    })
    
    print(f"Login successful: {login_result['success']}")
    if login_result['success']:
        session_token = login_result['session_token']
        print(f"Session token: {session_token[:16]}...")
        
        # Test session validation
        print("\nTesting session validation...")
        validation_result = auth_gene.execute({
            'action': 'validate_session',
            'session_token': session_token
        })
        print(f"Session valid: {validation_result['valid']}")
    
    # Test failed login
    print("\nTesting failed login...")
    failed_login = auth_gene.execute({
        'action': 'login',
        'username': 'user',
        'password': 'short'
    })
    print(f"Login failed as expected: {not failed_login['success']}")
    
    return login_result['success']


def test_performance_gene():
    """Test the PerformanceGene functionality."""
    print("\n" + "=" * 50)
    print("TESTING PERFORMANCE GENE")
    print("=" * 50)
    
    perf_gene = PerformanceGene()
    
    # Test performance monitoring
    print("Monitoring system performance...")
    monitor_result = perf_gene.execute({
        'action': 'monitor',
        'duration': 1
    })
    
    if monitor_result['success']:
        metrics = monitor_result['metrics']
        print(f"CPU Usage: {metrics['cpu_percent']:.1f}%")
        print(f"Memory Usage: {metrics['memory_percent']:.1f}%")
        print(f"Disk Usage: {metrics['disk_percent']:.1f}%")
        print(f"Process Count: {metrics['process_count']}")
        
        issues = monitor_result['issues']
        if issues:
            print(f"Performance Issues Detected: {len(issues)}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("No performance issues detected")
    
    # Test getting metrics summary
    print("\nGetting performance summary...")
    summary_result = perf_gene.execute({'action': 'get_metrics'})
    
    if summary_result['success']:
        print(f"Total measurements: {summary_result['total_measurements']}")
        print(f"Average CPU: {summary_result['average_cpu']:.1f}%")
        print(f"Average Memory: {summary_result['average_memory']:.1f}%")
    
    return monitor_result['success']


def test_logging_gene():
    """Test the LoggingVerbosityGene functionality."""
    print("\n" + "=" * 50)
    print("TESTING LOGGING VERBOSITY GENE")
    print("=" * 50)
    
    logging_gene = LoggingVerbosityGene()
    
    # Test getting current level
    print("Getting current logging level...")
    current_level = logging_gene.execute({'action': 'get_level'})
    print(f"Current level: {current_level['current_level']}")
    
    # Test setting DEBUG level
    print("\nSetting logging level to DEBUG...")
    set_result = logging_gene.execute({
        'action': 'set_level',
        'level': 'DEBUG'
    })
    
    if set_result['success']:
        print(f"Level changed from {set_result['previous_level']} to {set_result['new_level']}")
    
    # Test setting ERROR level
    print("\nSetting logging level to ERROR...")
    error_result = logging_gene.execute({
        'action': 'set_level',
        'level': 'ERROR'
    })
    
    # Test reset to previous level
    print("\nResetting to previous level...")
    reset_result = logging_gene.execute({'action': 'reset_level'})
    
    if reset_result['success']:
        print(f"Reset successful: {reset_result['message']}")
    
    # Test getting level history
    print("\nGetting logging level history...")
    history_result = logging_gene.execute({'action': 'get_history'})
    
    if history_result['success']:
        print(f"History entries: {len(history_result['level_history'])}")
        for entry in history_result['level_history'][-3:]:  # Show last 3
            print(f"  {entry['old_level']} -> {entry['new_level']} (logger: {entry['logger_name']})")
    
    return set_result['success']


def test_integration():
    """Test integration between components."""
    print("\n" + "=" * 50)
    print("TESTING INTEGRATION")
    print("=" * 50)
    
    # Create components
    immune = ImmuneSystem()
    auth_gene = AuthenticationGene()
    logging_gene = LoggingVerbosityGene()
    
    # Enable debug logging to see gene activity
    logging_gene.execute({'action': 'set_level', 'level': 'DEBUG'})
    
    # Simulate a complete workflow
    print("Simulating genomic analysis workflow...")
    
    # 1. Authenticate user
    auth_result = auth_gene.execute({
        'action': 'login',
        'username': 'researcher',
        'password': 'genomics2024!'
    })
    
    if not auth_result['success']:
        print("Authentication failed!")
        return False
    
    print("✓ User authenticated successfully")
    
    # 2. Process genomic data with immune system monitoring
    suspicious_data = {
        "sample_id": "GS001",
        "data": "Patient has BRCA2 mutation with variant_frequency: 0.95",
        "notes": "union select * from patients where mutation_count > 500",
        "researcher_email": "suspicious@tempmail.com"
    }
    
    detections = immune.scan_data_dict(suspicious_data, "genomic_workflow")
    print(f"✓ Scanned data, found {len(detections)} potential threats")
    
    # 3. Generate summary
    stats = immune.get_pattern_statistics()
    coverage = immune.get_pattern_coverage()
    
    print(f"✓ Analysis complete:")
    print(f"  - Threat patterns active: {stats['total_patterns']}")
    print(f"  - Total detections: {stats['total_detections']}")
    print(f"  - Pattern coverage: {coverage:.1f}%")
    
    return True


def main():
    """Run all tests."""
    print("Evolution Framework Manual Testing")
    print("=" * 50)
    
    tests = [
        ("Immune System", test_immune_system),
        ("Authentication Gene", test_authentication_gene),
        ("Performance Gene", test_performance_gene),
        ("Logging Gene", test_logging_gene),
        ("Integration", test_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Evolution framework is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    exit(main())