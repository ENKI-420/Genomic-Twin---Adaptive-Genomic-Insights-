"""
Repository Operations Validation System
Critical checkpoint ensuring repository and deployment safety before externalization
"""

import os
import subprocess
import yaml
import json
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RepositoryOperationsValidator:
    """
    Validates repository operations ensuring safety before deployment
    """
    
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.validation_results = {}
        self.safety_checks = []
        
    def validateRepoOperations(self) -> Dict[str, Any]:
        """
        Main validation entry point - ensures repository and deployment safety
        Returns validation results with pass/fail status and recommendations
        """
        logger.info(f"Starting repository operations validation for {self.environment}")
        
        validation_results = {
            "timestamp": datetime.utcnow().isoformat(),
            "environment": self.environment,
            "overall_status": "PENDING",
            "checks": {},
            "recommendations": [],
            "critical_issues": [],
            "deployment_safe": False
        }
        
        # Run all validation checks
        checks = [
            ("repository_access", self._validate_repository_access),
            ("ci_cd_integration", self._validate_ci_cd_integration),
            ("terraform_deployment", self._validate_terraform_deployment),
            ("mutation_safety", self._validate_mutation_safety),
            ("security_policies", self._validate_security_policies),
            ("backup_systems", self._validate_backup_systems)
        ]
        
        all_passed = True
        for check_name, check_function in checks:
            try:
                result = check_function()
                validation_results["checks"][check_name] = result
                if not result.get("passed", False):
                    all_passed = False
                    if result.get("critical", False):
                        validation_results["critical_issues"].append({
                            "check": check_name,
                            "issue": result.get("message", "Unknown issue"),
                            "recommendation": result.get("recommendation", "Manual review required")
                        })
            except Exception as e:
                logger.error(f"Validation check {check_name} failed with error: {str(e)}")
                validation_results["checks"][check_name] = {
                    "passed": False,
                    "critical": True,
                    "message": f"Check failed with exception: {str(e)}",
                    "recommendation": "Investigate and resolve the underlying issue"
                }
                all_passed = False
        
        # Set overall status
        validation_results["overall_status"] = "PASSED" if all_passed else "FAILED"
        validation_results["deployment_safe"] = all_passed and len(validation_results["critical_issues"]) == 0
        
        # Generate recommendations
        if not validation_results["deployment_safe"]:
            validation_results["recommendations"].extend([
                "Address all critical issues before proceeding with deployment",
                "Run validateRepoOperations again after fixes",
                "Consider rolling back to last known good state if issues persist"
            ])
        
        self.validation_results = validation_results
        return validation_results
    
    def _validate_repository_access(self) -> Dict[str, Any]:
        """Validate repository access permissions for deployment agents"""
        try:
            # Check git repository status
            git_status = subprocess.run(
                ["git", "status", "--porcelain"], 
                capture_output=True, 
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            # Check for uncommitted changes
            has_uncommitted = len(git_status.stdout.strip()) > 0
            
            # Check git remote access
            git_remote = subprocess.run(
                ["git", "remote", "-v"], 
                capture_output=True, 
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            has_remote = "origin" in git_remote.stdout
            
            # Check branch protection
            current_branch = subprocess.run(
                ["git", "branch", "--show-current"], 
                capture_output=True, 
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            ).stdout.strip()
            
            return {
                "passed": not has_uncommitted and has_remote,
                "critical": has_uncommitted,
                "message": f"Repository status: uncommitted={'Yes' if has_uncommitted else 'No'}, remote={'Yes' if has_remote else 'No'}, branch={current_branch}",
                "recommendation": "Commit all changes and ensure remote access before deployment" if has_uncommitted else "Repository access validated",
                "details": {
                    "uncommitted_changes": has_uncommitted,
                    "has_remote": has_remote,
                    "current_branch": current_branch
                }
            }
        except Exception as e:
            return {
                "passed": False,
                "critical": True,
                "message": f"Repository access validation failed: {str(e)}",
                "recommendation": "Ensure git repository is properly configured and accessible"
            }
    
    def _validate_ci_cd_integration(self) -> Dict[str, Any]:
        """Validate CI/CD pipeline integrations for terraform application"""
        workflow_path = ".github/workflows/"
        workflow_files = []
        
        if os.path.exists(workflow_path):
            workflow_files = [f for f in os.listdir(workflow_path) if f.endswith(('.yml', '.yaml'))]
        
        # Check for required workflow components
        has_terraform_workflow = any('terraform' in f.lower() for f in workflow_files)
        has_mutation_validation = any('mutation' in f.lower() or 'validation' in f.lower() for f in workflow_files)
        
        # Validate existing workflows
        workflow_valid = len(workflow_files) > 0
        
        return {
            "passed": workflow_valid,
            "critical": not workflow_valid,
            "message": f"Found {len(workflow_files)} workflow files. Terraform: {has_terraform_workflow}, Mutation validation: {has_mutation_validation}",
            "recommendation": "Ensure CI/CD workflows include terraform deployment and mutation validation" if not workflow_valid else "CI/CD integration validated",
            "details": {
                "workflow_files": workflow_files,
                "has_terraform": has_terraform_workflow,
                "has_mutation_validation": has_mutation_validation
            }
        }
    
    def _validate_terraform_deployment(self) -> Dict[str, Any]:
        """Validate terraform deployment configuration"""
        terraform_path = f"gcp-organization/terraform/{self.environment}/"
        
        if not os.path.exists(terraform_path):
            return {
                "passed": False,
                "critical": True,
                "message": f"Terraform configuration not found for environment: {self.environment}",
                "recommendation": f"Create terraform configuration for {self.environment} environment"
            }
        
        # Check for required terraform files
        tf_files = [f for f in os.listdir(terraform_path) if f.endswith('.tf')]
        has_main_tf = 'main.tf' in tf_files
        
        # Check terraform format (if terraform is available)
        terraform_valid = True
        try:
            # Try to validate terraform format
            result = subprocess.run(
                ["terraform", "fmt", "-check"], 
                cwd=terraform_path,
                capture_output=True,
                text=True
            )
            terraform_valid = result.returncode == 0
        except FileNotFoundError:
            logger.warning("Terraform CLI not found, skipping format validation")
        
        return {
            "passed": has_main_tf and terraform_valid,
            "critical": not has_main_tf,
            "message": f"Terraform files: {len(tf_files)}, main.tf: {has_main_tf}, format valid: {terraform_valid}",
            "recommendation": "Ensure terraform configuration is properly formatted and includes main.tf" if not (has_main_tf and terraform_valid) else "Terraform deployment configuration validated",
            "details": {
                "terraform_files": tf_files,
                "has_main_tf": has_main_tf,
                "format_valid": terraform_valid
            }
        }
    
    def _validate_mutation_safety(self) -> Dict[str, Any]:
        """Validate mutation rollback triggers and safety conditions"""
        # Check for mutation safety configuration
        safety_config_path = "gcp-organization/security-controls/mutation-safety.yaml"
        has_safety_config = os.path.exists(safety_config_path)
        
        # Check for rollback mechanisms
        rollback_mechanisms = [
            "modules/mutation_analysis.py",  # Existing mutation analysis
            "modules/digital_twin.py",       # Digital twin for simulation
        ]
        
        existing_mechanisms = [m for m in rollback_mechanisms if os.path.exists(m)]
        
        # Validate mutation monitoring is in place
        monitoring_ready = len(existing_mechanisms) >= 2
        
        return {
            "passed": monitoring_ready,
            "critical": not monitoring_ready,
            "message": f"Mutation safety: config={has_safety_config}, mechanisms={len(existing_mechanisms)}/{len(rollback_mechanisms)}",
            "recommendation": "Implement comprehensive mutation safety monitoring and rollback triggers" if not monitoring_ready else "Mutation safety systems validated",
            "details": {
                "safety_config": has_safety_config,
                "existing_mechanisms": existing_mechanisms,
                "monitoring_ready": monitoring_ready
            }
        }
    
    def _validate_security_policies(self) -> Dict[str, Any]:
        """Validate security policies are in place"""
        security_files = [
            "gcp-organization/security-controls/security-config.yaml",
            "gcp-organization/iam-policies/",
            "gcp-organization/resource-policies/"
        ]
        
        existing_security = [f for f in security_files if os.path.exists(f)]
        security_score = len(existing_security) / len(security_files)
        
        return {
            "passed": security_score >= 0.8,
            "critical": security_score < 0.5,
            "message": f"Security policies: {len(existing_security)}/{len(security_files)} found ({security_score:.1%})",
            "recommendation": "Ensure all security policies are in place and up to date" if security_score < 0.8 else "Security policies validated",
            "details": {
                "existing_files": existing_security,
                "security_score": security_score
            }
        }
    
    def _validate_backup_systems(self) -> Dict[str, Any]:
        """Validate backup and recovery systems"""
        # Check for backup configuration in environment config
        from environment_config import EnvironmentConfig
        config = EnvironmentConfig(self.environment)
        backup_config = config.backup_config
        
        has_backup_config = len(backup_config) > 0
        backup_frequency = backup_config.get('frequency', 'NONE')
        
        return {
            "passed": has_backup_config and backup_frequency != 'NONE',
            "critical": not has_backup_config,
            "message": f"Backup system: configured={has_backup_config}, frequency={backup_frequency}",
            "recommendation": "Configure backup and recovery systems" if not has_backup_config else "Backup systems validated",
            "details": backup_config
        }
    
    def get_deployment_readiness(self) -> bool:
        """Check if repository is ready for deployment"""
        if not self.validation_results:
            self.validateRepoOperations()
        return self.validation_results.get("deployment_safe", False)
    
    def get_critical_issues(self) -> List[Dict[str, str]]:
        """Get list of critical issues preventing deployment"""
        if not self.validation_results:
            self.validateRepoOperations()
        return self.validation_results.get("critical_issues", [])


def validate_before_deployment(environment: str = "development") -> Tuple[bool, Dict[str, Any]]:
    """
    Convenience function to validate repository operations before deployment
    Returns: (is_safe, validation_results)
    """
    validator = RepositoryOperationsValidator(environment)
    results = validator.validateRepoOperations()
    return results["deployment_safe"], results


# Export main validation function
__all__ = ['RepositoryOperationsValidator', 'validate_before_deployment']