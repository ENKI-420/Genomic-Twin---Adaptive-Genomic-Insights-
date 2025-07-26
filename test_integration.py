#!/usr/bin/env python3
"""
Integration Test for Genomic Platform Components
Tests the new agent collaboration, quantum evolution, and validation systems
"""

import sys
import os
import json
from datetime import datetime

# Add modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_repository_operations():
    """Test repository operations validation"""
    print("🔍 Testing Repository Operations Validation...")
    
    try:
        from modules.repository_operations import validate_before_deployment, RepositoryOperationsValidator
        
        # Test validation for development environment
        validator = RepositoryOperationsValidator("development")
        results = validator.validateRepoOperations()
        
        print(f"  Repository validation status: {results['overall_status']}")
        print(f"  Deployment safe: {results['deployment_safe']}")
        print(f"  Checks completed: {len(results['checks'])}")
        
        if results['critical_issues']:
            print(f"  Critical issues: {len(results['critical_issues'])}")
            for issue in results['critical_issues']:
                print(f"    - {issue['issue']}")
        
        return results['deployment_safe']
        
    except Exception as e:
        print(f"  ❌ Repository operations test failed: {str(e)}")
        return False

def test_agent_collaboration():
    """Test agent collaboration system"""
    print("\n🤝 Testing Agent Collaboration System...")
    
    try:
        from modules.agent_collaboration import collaboration_hub, DevOpsAgent, ReplicationGuardian
        
        # Test feedback loop
        results = collaboration_hub.initiate_feedback_loop()
        
        print(f"  DevOps readiness: {results['devops_readiness']['ready']}")
        print(f"  Replication health: {results['replication_status']['all_healthy']}")
        print(f"  Expansion readiness score: {results['expansion_readiness']['readiness_score']:.2f}")
        
        # Test system health
        health = collaboration_hub.get_system_health()
        print(f"  Active agents: {len(health['agents_status'])}")
        print(f"  Collaboration activity: {health['collaboration_activity']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Agent collaboration test failed: {str(e)}")
        return False

def test_quantum_evolution():
    """Test quantum evolution system"""
    print("\n⚛️ Testing Quantum Evolution System...")
    
    try:
        from modules.quantum_evolution import quantum_evolution, EvolutionState
        
        # Test evolution monitoring
        fitness_scores = [0.75, 0.75, 0.74, 0.74, 0.73]  # Simulated plateau
        consciousness_scores = [0.68, 0.67, 0.67, 0.66, 0.66]
        
        for fitness, consciousness in zip(fitness_scores, consciousness_scores):
            result = quantum_evolution.monitor_evolution_progress(fitness, consciousness)
        
        status = quantum_evolution.get_quantum_evolution_status()
        print(f"  Evolution state: {status['evolution_state']}")
        print(f"  Active mutations: {status['active_mutations']}")
        print(f"  Evolution events: {status['evolution_events']}")
        
        # Test quantum trigger
        if result['should_trigger_quantum']:
            print(f"  Quantum evolution triggered: {len(result['quantum_mutations_triggered'])} mutations")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Quantum evolution test failed: {str(e)}")
        return False

def test_cloud_architect():
    """Test cloud architect agent"""
    print("\n☁️ Testing Cloud Architect Agent...")
    
    try:
        from modules.cloud_architect import CloudArchitectAgent
        
        architect = CloudArchitectAgent("development")
        
        # Test infrastructure config generation
        requirements = {
            'vpc': {'enabled': True},
            'storage': {'enabled': True},
            'bigquery': {'enabled': True}
        }
        
        configs = architect.generate_infrastructure_config(requirements)
        print(f"  Generated configs: {len(configs)} files")
        
        # Test infrastructure status
        status = architect.get_infrastructure_status()
        print(f"  Terraform directory exists: {status['terraform_dir_exists']}")
        print(f"  Config files: {len(status['config_files'])}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Cloud architect test failed: {str(e)}")
        return False

def test_audit_logging():
    """Test audit logging system"""
    print("\n📋 Testing Audit Logging System...")
    
    try:
        from modules.audit_logging import audit_logger, AuditEventType, SeverityLevel
        
        # Test logging different event types
        mutation_event = audit_logger.log_mutation_proposed({
            "id": "test-mutation-001",
            "type": "structural",
            "expected_impact": 0.8
        })
        
        safety_event = audit_logger.log_safety_validation(
            "system_check",
            {"passed": True, "score": 0.85}
        )
        
        print(f"  Mutation event logged: {mutation_event}")
        print(f"  Safety event logged: {safety_event}")
        
        # Test audit summary
        summary = audit_logger.get_audit_summary(days=1)
        print(f"  Total events today: {summary['total_events']}")
        print(f"  Event types: {list(summary['events_by_type'].keys())}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Audit logging test failed: {str(e)}")
        return False

def test_platform_integration():
    """Test complete platform integration"""
    print("\n🔄 Testing Platform Integration...")
    
    try:
        from modules.platform_integration import validate_system_readiness, GenomicPlatformOrchestrator
        
        # Test system readiness validation
        is_ready, validation_results = validate_system_readiness("development")
        
        print(f"  System ready for deployment: {is_ready}")
        print(f"  Overall status: {validation_results['overall_status']}")
        print(f"  Components validated: {len(validation_results['components'])}")
        
        if validation_results['critical_issues']:
            print(f"  Critical issues: {len(validation_results['critical_issues'])}")
        
        # Test orchestrator
        orchestrator = GenomicPlatformOrchestrator("development")
        system_status = orchestrator.get_system_status()
        
        print(f"  System health: {system_status['system_state']['system_health']}")
        
        return is_ready
        
    except Exception as e:
        print(f"  ❌ Platform integration test failed: {str(e)}")
        return False

def test_github_workflow_components():
    """Test components used in GitHub workflow"""
    print("\n🔧 Testing GitHub Workflow Components...")
    
    try:
        # Test that all required components can be imported and used
        from modules.repository_operations import validate_before_deployment
        from modules.agent_collaboration import collaboration_hub
        from modules.quantum_evolution import quantum_evolution
        from modules.cloud_architect import CloudArchitectAgent
        from modules.audit_logging import audit_logger
        
        # Simulate the workflow validation steps
        print("  Simulating GitHub Actions workflow steps...")
        
        # Step 1: Repository validation
        is_safe, repo_results = validate_before_deployment("development")
        print(f"    ✓ Repository validation: {'PASSED' if is_safe else 'FAILED'}")
        
        # Step 2: Agent collaboration
        collab_results = collaboration_hub.initiate_feedback_loop()
        readiness_score = collab_results['expansion_readiness']['readiness_score']
        print(f"    ✓ Agent collaboration: {readiness_score:.2f} readiness")
        
        # Step 3: Infrastructure planning
        architect = CloudArchitectAgent("development")
        plan = architect.generate_deployment_plan({
            'vpc': {'enabled': True},
            'storage': {'enabled': True}
        })
        print(f"    ✓ Infrastructure planning: {'READY' if plan['deployment_ready'] else 'FAILED'}")
        
        # Step 4: Audit logging
        deployment_event = audit_logger.log_deployment_started({
            "id": "workflow-test-001",
            "environment": "development"
        })
        print(f"    ✓ Audit logging: Event {deployment_event[:8]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ GitHub workflow test failed: {str(e)}")
        return False

def main():
    """Run all integration tests"""
    print("🧬 Genomic Platform Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Repository Operations", test_repository_operations),
        ("Agent Collaboration", test_agent_collaboration),
        ("Quantum Evolution", test_quantum_evolution),
        ("Cloud Architect", test_cloud_architect),
        ("Audit Logging", test_audit_logging),
        ("Platform Integration", test_platform_integration),
        ("GitHub Workflow", test_github_workflow_components)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests PASSED! System is ready for deployment.")
        return 0
    else:
        print(f"⚠️ {total - passed} tests FAILED. Please review and fix issues.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)