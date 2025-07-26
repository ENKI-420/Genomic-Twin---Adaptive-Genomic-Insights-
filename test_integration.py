#!/usr/bin/env python3
"""
Integration test for the genomic analysis platform
Tests that all modules can be imported and basic functionality works
"""

import os
import sys
import logging

# Configure logging to reduce Streamlit warnings during testing
logging.getLogger('streamlit').setLevel(logging.ERROR)
os.environ['STREAMLIT_CLI_LOG_LEVEL'] = 'ERROR'

def test_main_app_import():
    """Test that the main application can be imported"""
    try:
        import app
        print("✅ Main application imports successfully")
        return True
    except Exception as e:
        print(f"❌ Main application import failed: {e}")
        return False

def test_all_modules_import():
    """Test that all modules can be imported"""
    try:
        import modules
        expected_functions = [
            'analyze_mutations',
            'generate_digital_twin', 
            'crispr_feasibility',
            'simulate_delivery',
            'find_trials',
            'log_pharmacovigilance',
            'fetch_beaker_data',
            'genomic_ai_module'
        ]
        
        available_functions = modules.__all__
        for func in expected_functions:
            if func not in available_functions:
                print(f"❌ Missing function: {func}")
                return False
        
        print("✅ All modules imported successfully")
        print(f"✅ Available functions: {available_functions}")
        return True
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        return False

def test_crispr_functionality():
    """Test basic CRISPR functionality with fallbacks"""
    try:
        from modules.crispr_ai import crispr_feasibility
        
        # Test with a simple gene target
        result = crispr_feasibility("BRCA1")
        
        # Check that result has expected structure
        required_keys = ['gene', 'guides', 'delivery', 'cas_variant']
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing key in CRISPR result: {key}")
                return False
                
        print("✅ CRISPR feasibility analysis working")
        print(f"✅ Result structure: {list(result.keys())}")
        return True
    except Exception as e:
        print(f"❌ CRISPR functionality test failed: {e}")
        return False

def test_nanoparticle_functionality():
    """Test basic nanoparticle simulation functionality"""
    try:
        from modules.nanoparticle_simulation import simulate_delivery
        
        # Test with default parameters
        result = simulate_delivery()
        
        # Check that result has expected structure
        required_keys = ['pharmacokinetics', 'distribution', 'parameters']
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing key in nanoparticle result: {key}")
                return False
                
        print("✅ Nanoparticle delivery simulation working")
        print(f"✅ Result structure: {list(result.keys())}")
        return True
    except Exception as e:
        print(f"❌ Nanoparticle functionality test failed: {e}")
        return False

def test_clinical_trials_functionality():
    """Test basic clinical trials functionality"""
    try:
        from modules.clinical_trials import find_trials
        
        # Test with sample mutations
        result = find_trials(["BRCA1", "TP53"])
        
        # Should return some result (even if error or empty)
        if result is None:
            print("❌ Clinical trials function returned None")
            return False
                
        print("✅ Clinical trials search working")
        print(f"✅ Result type: {type(result)}")
        return True
    except Exception as e:
        print(f"❌ Clinical trials functionality test failed: {e}")
        return False

def test_environment_config():
    """Test that environment configuration still works"""
    try:
        from environment_config import EnvironmentConfig
        
        # Test different environments
        for env in ['production', 'staging', 'development']:
            config = EnvironmentConfig(env)
            
            # Test key properties
            assert config.environment == env
            assert config.project_id is not None
            assert config.security_level is not None
            
        print("✅ Environment configuration working")
        return True
    except Exception as e:
        print(f"❌ Environment configuration test failed: {e}")
        return False

def test_verification_script():
    """Test that the GCP organization verification still works"""
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, 'verify_implementation.py'], 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        if 'Implementation Complete!' in result.stdout:
            print("✅ GCP organization verification working")
            return True
        else:
            print("❌ GCP organization verification failed")
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Verification script test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🧬 DNA-Lang Platform - Integration Test Suite")
    print("=" * 50)
    
    tests = [
        test_main_app_import,
        test_all_modules_import,
        test_crispr_functionality,
        test_nanoparticle_functionality,
        test_clinical_trials_functionality,
        test_environment_config,
        test_verification_script,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\n🔬 Running {test.__name__}...")
        if test():
            passed += 1
        else:
            print(f"Test {test.__name__} failed!")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed - check the output above")
        return 1

if __name__ == '__main__':
    sys.exit(main())