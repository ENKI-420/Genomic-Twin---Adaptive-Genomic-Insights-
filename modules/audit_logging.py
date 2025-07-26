"""
Audit Logging System for Mutations and Deployments
Comprehensive logging for tracking all mutations, deployments and safety validations
"""

import json
import os
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuditEventType(Enum):
    MUTATION_PROPOSED = "mutation_proposed"
    MUTATION_VALIDATED = "mutation_validated"
    MUTATION_APPLIED = "mutation_applied"
    MUTATION_ROLLBACK = "mutation_rollback"
    DEPLOYMENT_STARTED = "deployment_started"
    DEPLOYMENT_COMPLETED = "deployment_completed"
    DEPLOYMENT_FAILED = "deployment_failed"
    SAFETY_VALIDATION = "safety_validation"
    AGENT_COLLABORATION = "agent_collaboration"
    QUANTUM_EVOLUTION = "quantum_evolution"
    INFRASTRUCTURE_CHANGE = "infrastructure_change"
    SECURITY_EVENT = "security_event"

class SeverityLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class AuditEvent:
    """Audit event data structure"""
    event_id: str
    event_type: AuditEventType
    timestamp: datetime
    environment: str
    severity: SeverityLevel
    actor: str  # User, system, or agent that triggered the event
    description: str
    details: Dict[str, Any]
    related_events: List[str] = None  # IDs of related audit events
    metadata: Dict[str, Any] = None

class AuditLogger:
    """
    Centralized audit logging system for all mutations and deployments
    """
    
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.audit_dir = "audit_logs"
        self.ensure_audit_directory()
        
    def ensure_audit_directory(self) -> None:
        """Ensure audit directory exists"""
        os.makedirs(self.audit_dir, exist_ok=True)
        
        # Create environment-specific subdirectory
        env_audit_dir = os.path.join(self.audit_dir, self.environment)
        os.makedirs(env_audit_dir, exist_ok=True)
    
    def log_audit_event(self, 
                       event_type: AuditEventType,
                       description: str,
                       details: Dict[str, Any],
                       actor: str = "system",
                       severity: SeverityLevel = SeverityLevel.INFO,
                       related_events: List[str] = None,
                       metadata: Dict[str, Any] = None) -> str:
        """Log an audit event and return event ID"""
        
        event_id = str(uuid.uuid4())
        
        audit_event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            environment=self.environment,
            severity=severity,
            actor=actor,
            description=description,
            details=details,
            related_events=related_events or [],
            metadata=metadata or {}
        )
        
        # Write to audit log file
        self._write_audit_event(audit_event)
        
        # Log to application logger
        log_level = {
            SeverityLevel.INFO: logging.INFO,
            SeverityLevel.WARNING: logging.WARNING,
            SeverityLevel.ERROR: logging.ERROR,
            SeverityLevel.CRITICAL: logging.CRITICAL
        }[severity]
        
        logger.log(log_level, f"AUDIT [{event_type.value}] {description}")
        
        return event_id
    
    def _write_audit_event(self, event: AuditEvent) -> None:
        """Write audit event to file"""
        # Create daily log file
        date_str = event.timestamp.strftime("%Y-%m-%d")
        log_file = os.path.join(self.audit_dir, self.environment, f"audit_{date_str}.jsonl")
        
        # Convert to JSON-serializable format
        event_dict = asdict(event)
        event_dict['timestamp'] = event.timestamp.isoformat()
        event_dict['event_type'] = event.event_type.value
        event_dict['severity'] = event.severity.value
        
        # Append to log file
        with open(log_file, 'a') as f:
            f.write(json.dumps(event_dict) + '\n')
    
    def log_mutation_proposed(self, mutation_data: Dict[str, Any], actor: str = "quantum_strategist") -> str:
        """Log when a mutation is proposed"""
        return self.log_audit_event(
            event_type=AuditEventType.MUTATION_PROPOSED,
            description=f"Mutation proposed: {mutation_data.get('type', 'unknown')}",
            details={
                "mutation_id": mutation_data.get("id"),
                "mutation_type": mutation_data.get("type"),
                "target_system": mutation_data.get("target"),
                "expected_impact": mutation_data.get("expected_impact"),
                "risk_level": mutation_data.get("risk_level"),
                "quantum_parameters": mutation_data.get("quantum_parameters", {})
            },
            actor=actor,
            severity=SeverityLevel.INFO
        )
    
    def log_mutation_validated(self, mutation_id: str, validation_result: Dict[str, Any], actor: str = "replication_guardian") -> str:
        """Log mutation validation results"""
        severity = SeverityLevel.INFO if validation_result.get("passed", False) else SeverityLevel.WARNING
        
        return self.log_audit_event(
            event_type=AuditEventType.MUTATION_VALIDATED,
            description=f"Mutation validation: {'PASSED' if validation_result.get('passed', False) else 'FAILED'}",
            details={
                "mutation_id": mutation_id,
                "validation_passed": validation_result.get("passed", False),
                "safety_level": validation_result.get("safety_level"),
                "violations": validation_result.get("violations", []),
                "rollback_triggers": validation_result.get("rollback_triggers", []),
                "recommendations": validation_result.get("recommendations", [])
            },
            actor=actor,
            severity=severity
        )
    
    def log_mutation_applied(self, mutation_id: str, application_result: Dict[str, Any], actor: str = "system") -> str:
        """Log mutation application"""
        severity = SeverityLevel.INFO if application_result.get("success", False) else SeverityLevel.ERROR
        
        return self.log_audit_event(
            event_type=AuditEventType.MUTATION_APPLIED,
            description=f"Mutation application: {'SUCCESS' if application_result.get('success', False) else 'FAILED'}",
            details={
                "mutation_id": mutation_id,
                "success": application_result.get("success", False),
                "start_time": application_result.get("start_time"),
                "end_time": application_result.get("end_time"),
                "steps_completed": application_result.get("steps_completed", []),
                "error": application_result.get("error"),
                "rollback_required": application_result.get("rollback_required", False)
            },
            actor=actor,
            severity=severity
        )
    
    def log_mutation_rollback(self, mutation_id: str, rollback_reason: str, rollback_result: Dict[str, Any], actor: str = "safety_system") -> str:
        """Log mutation rollback"""
        severity = SeverityLevel.WARNING if rollback_result.get("success", False) else SeverityLevel.CRITICAL
        
        return self.log_audit_event(
            event_type=AuditEventType.MUTATION_ROLLBACK,
            description=f"Mutation rollback: {rollback_reason}",
            details={
                "mutation_id": mutation_id,
                "rollback_reason": rollback_reason,
                "rollback_success": rollback_result.get("success", False),
                "rollback_steps": rollback_result.get("steps", []),
                "system_state": rollback_result.get("system_state"),
                "integrity_verified": rollback_result.get("integrity_verified", False)
            },
            actor=actor,
            severity=severity
        )
    
    def log_deployment_started(self, deployment_info: Dict[str, Any], actor: str = "ci_cd") -> str:
        """Log deployment start"""
        return self.log_audit_event(
            event_type=AuditEventType.DEPLOYMENT_STARTED,
            description=f"Deployment started to {deployment_info.get('environment', 'unknown')}",
            details={
                "deployment_id": deployment_info.get("id"),
                "target_environment": deployment_info.get("environment"),
                "git_sha": deployment_info.get("git_sha"),
                "git_ref": deployment_info.get("git_ref"),
                "triggered_by": deployment_info.get("triggered_by"),
                "terraform_plan": deployment_info.get("terraform_plan"),
                "safety_validations": deployment_info.get("safety_validations", [])
            },
            actor=actor,
            severity=SeverityLevel.INFO
        )
    
    def log_deployment_completed(self, deployment_info: Dict[str, Any], actor: str = "ci_cd") -> str:
        """Log successful deployment completion"""
        return self.log_audit_event(
            event_type=AuditEventType.DEPLOYMENT_COMPLETED,
            description=f"Deployment completed successfully to {deployment_info.get('environment', 'unknown')}",
            details={
                "deployment_id": deployment_info.get("id"),
                "target_environment": deployment_info.get("environment"),
                "start_time": deployment_info.get("start_time"),
                "end_time": deployment_info.get("end_time"),
                "terraform_outputs": deployment_info.get("terraform_outputs", {}),
                "infrastructure_changes": deployment_info.get("infrastructure_changes", []),
                "post_deployment_health": deployment_info.get("health_check", {})
            },
            actor=actor,
            severity=SeverityLevel.INFO
        )
    
    def log_deployment_failed(self, deployment_info: Dict[str, Any], failure_reason: str, actor: str = "ci_cd") -> str:
        """Log deployment failure"""
        return self.log_audit_event(
            event_type=AuditEventType.DEPLOYMENT_FAILED,
            description=f"Deployment failed: {failure_reason}",
            details={
                "deployment_id": deployment_info.get("id"),
                "target_environment": deployment_info.get("environment"),
                "failure_reason": failure_reason,
                "error_details": deployment_info.get("error_details", {}),
                "rollback_initiated": deployment_info.get("rollback_initiated", False),
                "recovery_actions": deployment_info.get("recovery_actions", [])
            },
            actor=actor,
            severity=SeverityLevel.ERROR
        )
    
    def log_safety_validation(self, validation_type: str, validation_result: Dict[str, Any], actor: str = "safety_system") -> str:
        """Log safety validation events"""
        severity = SeverityLevel.INFO if validation_result.get("passed", False) else SeverityLevel.WARNING
        
        return self.log_audit_event(
            event_type=AuditEventType.SAFETY_VALIDATION,
            description=f"Safety validation ({validation_type}): {'PASSED' if validation_result.get('passed', False) else 'FAILED'}",
            details={
                "validation_type": validation_type,
                "passed": validation_result.get("passed", False),
                "score": validation_result.get("score"),
                "checks": validation_result.get("checks", {}),
                "recommendations": validation_result.get("recommendations", []),
                "critical_issues": validation_result.get("critical_issues", [])
            },
            actor=actor,
            severity=severity
        )
    
    def log_agent_collaboration(self, collaboration_data: Dict[str, Any], actor: str = "collaboration_hub") -> str:
        """Log agent collaboration events"""
        return self.log_audit_event(
            event_type=AuditEventType.AGENT_COLLABORATION,
            description="Agent collaboration feedback loop executed",
            details={
                "participating_agents": collaboration_data.get("agents", []),
                "collaboration_results": collaboration_data.get("results", {}),
                "system_health": collaboration_data.get("system_health", {}),
                "recommendations": collaboration_data.get("recommendations", []),
                "expansion_readiness": collaboration_data.get("expansion_readiness", {})
            },
            actor=actor,
            severity=SeverityLevel.INFO
        )
    
    def log_quantum_evolution(self, evolution_data: Dict[str, Any], actor: str = "quantum_evolution") -> str:
        """Log quantum evolution events"""
        severity = SeverityLevel.WARNING if evolution_data.get("triggered", False) else SeverityLevel.INFO
        
        return self.log_audit_event(
            event_type=AuditEventType.QUANTUM_EVOLUTION,
            description=f"Quantum evolution: {evolution_data.get('event', 'monitoring')}",
            details={
                "evolution_state": evolution_data.get("evolution_state"),
                "fitness_score": evolution_data.get("fitness_score"),
                "consciousness_level": evolution_data.get("consciousness_level"),
                "stagnation_period": evolution_data.get("stagnation_period"),
                "quantum_triggered": evolution_data.get("triggered", False),
                "mutations_generated": evolution_data.get("mutations_generated", 0),
                "quantum_strategy": evolution_data.get("quantum_strategy", {})
            },
            actor=actor,
            severity=severity
        )
    
    def log_infrastructure_change(self, change_data: Dict[str, Any], actor: str = "cloud_architect") -> str:
        """Log infrastructure changes"""
        return self.log_audit_event(
            event_type=AuditEventType.INFRASTRUCTURE_CHANGE,
            description=f"Infrastructure change: {change_data.get('type', 'unknown')}",
            details={
                "change_type": change_data.get("type"),
                "resources_affected": change_data.get("resources", []),
                "terraform_plan": change_data.get("terraform_plan", {}),
                "validation_passed": change_data.get("validation_passed", False),
                "change_impact": change_data.get("impact", "unknown"),
                "approval_required": change_data.get("approval_required", False)
            },
            actor=actor,
            severity=SeverityLevel.INFO
        )
    
    def log_security_event(self, event_data: Dict[str, Any], actor: str = "security_system") -> str:
        """Log security-related events"""
        severity_map = {
            "low": SeverityLevel.INFO,
            "medium": SeverityLevel.WARNING,
            "high": SeverityLevel.ERROR,
            "critical": SeverityLevel.CRITICAL
        }
        severity = severity_map.get(event_data.get("severity", "medium"), SeverityLevel.WARNING)
        
        return self.log_audit_event(
            event_type=AuditEventType.SECURITY_EVENT,
            description=f"Security event: {event_data.get('type', 'unknown')}",
            details={
                "security_event_type": event_data.get("type"),
                "threat_level": event_data.get("severity"),
                "source": event_data.get("source"),
                "target": event_data.get("target"),
                "detection_method": event_data.get("detection_method"),
                "mitigation_actions": event_data.get("mitigation_actions", []),
                "investigation_required": event_data.get("investigation_required", False)
            },
            actor=actor,
            severity=severity
        )
    
    def get_audit_trail(self, 
                       start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None,
                       event_types: Optional[List[AuditEventType]] = None,
                       severity_levels: Optional[List[SeverityLevel]] = None) -> List[Dict[str, Any]]:
        """Retrieve audit trail with filtering options"""
        
        audit_events = []
        
        # If no date range specified, get last 30 days
        if start_date is None:
            start_date = datetime.now(timezone.utc).replace(day=1)  # First day of current month
        if end_date is None:
            end_date = datetime.now(timezone.utc)
        
        # Read audit files in date range
        current_date = start_date.date()
        end_date_only = end_date.date()
        
        while current_date <= end_date_only:
            date_str = current_date.strftime("%Y-%m-%d")
            log_file = os.path.join(self.audit_dir, self.environment, f"audit_{date_str}.jsonl")
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    for line in f:
                        try:
                            event = json.loads(line.strip())
                            
                            # Apply filters
                            if event_types and event['event_type'] not in [et.value for et in event_types]:
                                continue
                            
                            if severity_levels and event['severity'] not in [sl.value for sl in severity_levels]:
                                continue
                            
                            # Check if event is in time range
                            event_time = datetime.fromisoformat(event['timestamp'])
                            if start_date <= event_time <= end_date:
                                audit_events.append(event)
                                
                        except (json.JSONDecodeError, KeyError) as e:
                            logger.warning(f"Failed to parse audit event: {e}")
            
            # Move to next day
            current_date = current_date.replace(day=current_date.day + 1) if current_date.day < 28 else \
                          current_date.replace(month=current_date.month + 1, day=1) if current_date.month < 12 else \
                          current_date.replace(year=current_date.year + 1, month=1, day=1)
        
        # Sort by timestamp
        audit_events.sort(key=lambda x: x['timestamp'])
        
        return audit_events
    
    def get_audit_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get audit summary for the last N days"""
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        events = self.get_audit_trail(start_date, end_date)
        
        summary = {
            "period": f"{start_date.date()} to {end_date.date()}",
            "total_events": len(events),
            "events_by_type": {},
            "events_by_severity": {},
            "recent_critical_events": [],
            "mutation_activity": {
                "proposed": 0,
                "applied": 0,
                "rolled_back": 0
            },
            "deployment_activity": {
                "started": 0,
                "completed": 0,
                "failed": 0
            }
        }
        
        for event in events:
            # Count by type
            event_type = event['event_type']
            summary["events_by_type"][event_type] = summary["events_by_type"].get(event_type, 0) + 1
            
            # Count by severity
            severity = event['severity']
            summary["events_by_severity"][severity] = summary["events_by_severity"].get(severity, 0) + 1
            
            # Track critical events
            if severity == SeverityLevel.CRITICAL.value:
                summary["recent_critical_events"].append({
                    "timestamp": event['timestamp'],
                    "description": event['description'],
                    "event_id": event['event_id']
                })
            
            # Track mutation activity
            if event_type == AuditEventType.MUTATION_PROPOSED.value:
                summary["mutation_activity"]["proposed"] += 1
            elif event_type == AuditEventType.MUTATION_APPLIED.value:
                summary["mutation_activity"]["applied"] += 1
            elif event_type == AuditEventType.MUTATION_ROLLBACK.value:
                summary["mutation_activity"]["rolled_back"] += 1
            
            # Track deployment activity
            if event_type == AuditEventType.DEPLOYMENT_STARTED.value:
                summary["deployment_activity"]["started"] += 1
            elif event_type == AuditEventType.DEPLOYMENT_COMPLETED.value:
                summary["deployment_activity"]["completed"] += 1
            elif event_type == AuditEventType.DEPLOYMENT_FAILED.value:
                summary["deployment_activity"]["failed"] += 1
        
        return summary


# Global audit logger instance
audit_logger = AuditLogger()

# Export main components
__all__ = [
    'AuditLogger', 'AuditEvent', 'AuditEventType', 'SeverityLevel',
    'audit_logger'
]