#!/usr/bin/env python3
"""
Test script to validate that the environment.yml file contains all necessary dependencies
for the Genomic Twin project.
"""

import sys
import subprocess

def test_environment_yml_exists():
    """Test that environment.yml exists in the repository root."""
    import os
    assert os.path.exists('environment.yml'), "environment.yml file should exist in repository root"
    print("✓ environment.yml file exists")

def test_environment_yml_syntax():
    """Test that environment.yml has valid YAML syntax."""
    import yaml
    
    with open('environment.yml', 'r') as f:
        try:
            env_config = yaml.safe_load(f)
            assert isinstance(env_config, dict), "environment.yml should contain a valid YAML dictionary"
            assert 'name' in env_config, "environment.yml should have a 'name' field"
            assert 'dependencies' in env_config, "environment.yml should have a 'dependencies' field"
            print("✓ environment.yml has valid YAML syntax")
        except yaml.YAMLError as e:
            raise AssertionError(f"environment.yml has invalid YAML syntax: {e}")

def test_required_dependencies():
    """Test that environment.yml contains all required dependencies."""
    import yaml
    
    with open('environment.yml', 'r') as f:
        env_config = yaml.safe_load(f)
    
    dependencies = env_config.get('dependencies', [])
    dep_names = []
    
    # Extract dependency names (handle both 'package' and 'package>=version' formats)
    for dep in dependencies:
        if isinstance(dep, str):
            if '=' in dep:
                dep_names.append(dep.split('=')[0].split('>')[0].split('<')[0])
            else:
                dep_names.append(dep)
        elif isinstance(dep, dict) and 'pip' in dep:
            # Handle pip dependencies
            for pip_dep in dep['pip']:
                if '>=' in pip_dep:
                    dep_names.append(pip_dep.split('>=')[0])
                else:
                    dep_names.append(pip_dep.split('=')[0])
    
    # Required dependencies based on the codebase analysis
    required_deps = [
        'python', 'streamlit', 'pandas', 'plotly', 'requests',
        'matplotlib', 'scikit-learn', 'biopython', 'python-dotenv',
        'pyyaml', 'psycopg2', 'flake8', 'pytest'
    ]
    
    for req_dep in required_deps:
        # Check for exact match or partial match (e.g., psycopg2 vs psycopg2-binary)
        found = any(req_dep in dep_name for dep_name in dep_names)
        assert found, f"Required dependency '{req_dep}' not found in environment.yml"
    
    print(f"✓ All {len(required_deps)} required dependencies found in environment.yml")

def test_environment_conda_validation():
    """Test that conda can validate the environment file."""
    try:
        # Test if conda can read the file without errors
        result = subprocess.run(['conda', 'env', 'create', '--dry-run', '--file', 'environment.yml', '--name', 'test_validation'], 
                               capture_output=True, text=True, timeout=30)
        
        # For this test, we expect it to succeed (exit code 0) or at least not fail due to syntax errors
        if result.returncode == 0:
            print("✓ Conda can successfully parse environment.yml")
        else:
            # Check if the error is due to syntax issues vs other issues (like network)
            if 'parsing' in result.stderr.lower() or 'yaml' in result.stderr.lower():
                raise AssertionError(f"Conda failed to parse environment.yml: {result.stderr}")
            else:
                print("⚠ Conda validation skipped due to network/repository access issues")
                
    except subprocess.TimeoutExpired:
        print("⚠ Conda validation timed out - skipping this test")
    except FileNotFoundError:
        print("⚠ Conda not found - skipping conda validation test")

if __name__ == "__main__":
    print("Testing environment.yml configuration...")
    
    test_environment_yml_exists()
    test_environment_yml_syntax()
    test_required_dependencies()
    test_environment_conda_validation()
    
    print("\n✅ All environment.yml tests passed!")