# Compliance, Security, and Governance Framework
# Implements GDPR, HIPAA, SOC2, and other compliance requirements

import json
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

class ComplianceFramework(Enum):
    """Supported compliance frameworks"""
    GDPR = "gdpr"
    HIPAA = "hipaa"
    SOC2 = "soc2"
    HITECH = "hitech"
    ISO_27001 = "iso_27001"
    NIST = "nist"
    FDA_21_CFR_11 = "fda_21_cfr_11"
    GXP = "gxp"
    PIPEDA = "pipeda"
    CCPA = "ccpa"

class AuditStatus(Enum):
    """Audit status tracking"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REMEDIATION_REQUIRED = "remediation_required"

class GovernanceLevel(Enum):
    """Governance levels for different operations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ComplianceRequirement:
    """Individual compliance requirement"""
    id: str
    framework: ComplianceFramework
    requirement_id: str
    title: str
    description: str
    category: str
    criticality: GovernanceLevel
    controls: List[str]
    evidence_required: List[str]
    compliance_status: str
    last_assessed: datetime
    next_assessment: datetime
    responsible_team: str

@dataclass
class SecurityAudit:
    """Security audit record"""
    id: str
    audit_type: str
    auditor: str
    scope: List[str]
    start_date: datetime
    end_date: Optional[datetime]
    status: AuditStatus
    findings: List[Dict[str, Any]]
    recommendations: List[str]
    remediation_plan: List[Dict[str, str]]
    certification_achieved: bool = False

@dataclass
class GovernancePolicy:
    """Governance policy definition"""
    id: str
    name: str
    category: str
    description: str
    scope: List[str]
    governance_level: GovernanceLevel
    approval_workflow: List[str]
    review_frequency_months: int
    effective_date: datetime
    last_review: datetime
    next_review: datetime
    approved_by: str
    version: str

class ComplianceEngine:
    """
    Comprehensive compliance, security, and governance engine
    Supports multiple frameworks and automated compliance monitoring
    """
    
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.compliance_requirements = self._initialize_compliance_requirements()
        self.security_audits = {}
        self.governance_policies = self._initialize_governance_policies()
        self.audit_logs = []
        self.compliance_dashboard = {}
        
    def _initialize_compliance_requirements(self) -> Dict[str, ComplianceRequirement]:
        """Initialize compliance requirements for supported frameworks"""
        requirements = {}
        
        # GDPR Requirements
        requirements["gdpr_data_minimization"] = ComplianceRequirement(
            id="gdpr_data_minimization",
            framework=ComplianceFramework.GDPR,
            requirement_id="GDPR-5.1.c",
            title="Data Minimization",
            description="Personal data shall be adequate, relevant and limited to what is necessary",
            category="data_protection",
            criticality=GovernanceLevel.HIGH,
            controls=[
                "Data collection approval workflow",
                "Automated data retention policies",
                "Data purpose limitation enforcement"
            ],
            evidence_required=[
                "Data processing records",
                "Privacy impact assessments",
                "Data retention logs"
            ],
            compliance_status="compliant",
            last_assessed=datetime.now() - timedelta(days=30),
            next_assessment=datetime.now() + timedelta(days=60),
            responsible_team="Privacy Engineering"
        )
        
        requirements["gdpr_consent_management"] = ComplianceRequirement(
            id="gdpr_consent_management",
            framework=ComplianceFramework.GDPR,
            requirement_id="GDPR-7",
            title="Consent Management",
            description="Conditions for consent and withdrawing consent",
            category="consent",
            criticality=GovernanceLevel.CRITICAL,
            controls=[
                "Consent capture mechanisms",
                "Consent withdrawal processing",
                "Consent audit trails"
            ],
            evidence_required=[
                "Consent records",
                "Withdrawal processing logs",
                "User interface documentation"
            ],
            compliance_status="compliant",
            last_assessed=datetime.now() - timedelta(days=15),
            next_assessment=datetime.now() + timedelta(days=45),
            responsible_team="Legal & Privacy"
        )
        
        # HIPAA Requirements
        requirements["hipaa_access_controls"] = ComplianceRequirement(
            id="hipaa_access_controls",
            framework=ComplianceFramework.HIPAA,
            requirement_id="164.312(a)(1)",
            title="Access Control",
            description="Implement technical policies for electronic PHI access",
            category="access_control",
            criticality=GovernanceLevel.CRITICAL,
            controls=[
                "Role-based access control",
                "Multi-factor authentication",
                "Access logging and monitoring"
            ],
            evidence_required=[
                "Access control matrices",
                "Authentication logs",
                "User access reviews"
            ],
            compliance_status="compliant",
            last_assessed=datetime.now() - timedelta(days=20),
            next_assessment=datetime.now() + timedelta(days=40),
            responsible_team="Security"
        )
        
        requirements["hipaa_encryption"] = ComplianceRequirement(
            id="hipaa_encryption",
            framework=ComplianceFramework.HIPAA,
            requirement_id="164.312(a)(2)(iv)",
            title="Encryption and Decryption",
            description="Implement encryption/decryption of PHI",
            category="encryption",
            criticality=GovernanceLevel.CRITICAL,
            controls=[
                "Data encryption at rest",
                "Data encryption in transit",
                "Key management procedures"
            ],
            evidence_required=[
                "Encryption implementation docs",
                "Key rotation logs",
                "Cryptographic standards compliance"
            ],
            compliance_status="compliant",
            last_assessed=datetime.now() - timedelta(days=10),
            next_assessment=datetime.now() + timedelta(days=90),
            responsible_team="Infrastructure Security"
        )
        
        # SOC2 Requirements
        requirements["soc2_security_principle"] = ComplianceRequirement(
            id="soc2_security_principle",
            framework=ComplianceFramework.SOC2,
            requirement_id="CC6.1",
            title="Security Principle Implementation",
            description="Logical and physical access controls protect information and systems",
            category="security",
            criticality=GovernanceLevel.HIGH,
            controls=[
                "Physical access controls",
                "Logical access controls",
                "Network security controls"
            ],
            evidence_required=[
                "Security control documentation",
                "Penetration test results",
                "Vulnerability scan reports"
            ],
            compliance_status="compliant",
            last_assessed=datetime.now() - timedelta(days=45),
            next_assessment=datetime.now() + timedelta(days=90),
            responsible_team="Information Security"
        )
        
        return requirements
    
    def _initialize_governance_policies(self) -> Dict[str, GovernancePolicy]:
        """Initialize governance policies"""
        policies = {}
        
        # Data Governance Policy
        policies["data_governance"] = GovernancePolicy(
            id="data_governance",
            name="Data Governance and Stewardship Policy",
            category="data_management",
            description="Defines data governance frameworks, stewardship roles, and data quality standards",
            scope=["all_data_systems", "genomic_data", "clinical_data", "marketplace_data"],
            governance_level=GovernanceLevel.CRITICAL,
            approval_workflow=["Data Council", "Chief Data Officer", "Board Review"],
            review_frequency_months=6,
            effective_date=datetime.now() - timedelta(days=90),
            last_review=datetime.now() - timedelta(days=30),
            next_review=datetime.now() + timedelta(days=150),
            approved_by="Chief Data Officer",
            version="2.1"
        )
        
        # Security Policy
        policies["information_security"] = GovernancePolicy(
            id="information_security",
            name="Information Security Policy",
            category="security",
            description="Comprehensive security controls and procedures",
            scope=["all_systems", "data_processing", "user_access", "third_party_integrations"],
            governance_level=GovernanceLevel.CRITICAL,
            approval_workflow=["CISO", "Risk Committee", "Executive Leadership"],
            review_frequency_months=12,
            effective_date=datetime.now() - timedelta(days=180),
            last_review=datetime.now() - timedelta(days=60),
            next_review=datetime.now() + timedelta(days=300),
            approved_by="Chief Information Security Officer",
            version="3.0"
        )
        
        # Marketplace Governance
        policies["marketplace_governance"] = GovernancePolicy(
            id="marketplace_governance",
            name="Digital Organism Marketplace Governance",
            category="marketplace",
            description="Governance framework for digital organism marketplace operations",
            scope=["marketplace_operations", "organism_validation", "partner_management"],
            governance_level=GovernanceLevel.HIGH,
            approval_workflow=["Marketplace Council", "Product Leadership", "Legal Review"],
            review_frequency_months=3,
            effective_date=datetime.now() - timedelta(days=30),
            last_review=datetime.now() - timedelta(days=15),
            next_review=datetime.now() + timedelta(days=75),
            approved_by="Chief Product Officer",
            version="1.2"
        )
        
        return policies
    
    def schedule_security_audit(self, audit_data: Dict[str, Any]) -> str:
        """Schedule a security audit"""
        audit_id = str(uuid.uuid4())
        
        audit = SecurityAudit(
            id=audit_id,
            audit_type=audit_data.get("audit_type", "annual_security"),
            auditor=audit_data.get("auditor", "Internal Audit Team"),
            scope=audit_data.get("scope", ["all_systems"]),
            start_date=datetime.fromisoformat(audit_data["start_date"]),
            end_date=None,
            status=AuditStatus.SCHEDULED,
            findings=[],
            recommendations=[],
            remediation_plan=[]
        )
        
        self.security_audits[audit_id] = audit
        
        # Log audit scheduling
        self._log_audit_event("audit_scheduled", {
            "audit_id": audit_id,
            "audit_type": audit.audit_type,
            "auditor": audit.auditor,
            "start_date": audit.start_date.isoformat()
        })
        
        return audit_id
    
    def record_audit_finding(self, audit_id: str, finding_data: Dict[str, Any]) -> bool:
        """Record an audit finding"""
        if audit_id not in self.security_audits:
            return False
        
        audit = self.security_audits[audit_id]
        
        finding = {
            "id": str(uuid.uuid4()),
            "title": finding_data["title"],
            "description": finding_data["description"],
            "severity": finding_data.get("severity", "medium"),
            "category": finding_data.get("category", "security"),
            "affected_systems": finding_data.get("affected_systems", []),
            "evidence": finding_data.get("evidence", []),
            "recommendation": finding_data.get("recommendation", ""),
            "target_remediation_date": finding_data.get("target_remediation_date"),
            "identified_date": datetime.now(),
            "status": "open"
        }
        
        audit.findings.append(finding)
        
        # Log finding
        self._log_audit_event("finding_recorded", {
            "audit_id": audit_id,
            "finding_id": finding["id"],
            "severity": finding["severity"],
            "category": finding["category"]
        })
        
        return True
    
    def assess_compliance_status(self, framework: str = None) -> Dict[str, Any]:
        """Assess overall compliance status"""
        
        if framework:
            # Assess specific framework
            framework_enum = ComplianceFramework(framework)
            relevant_requirements = [
                req for req in self.compliance_requirements.values()
                if req.framework == framework_enum
            ]
        else:
            # Assess all frameworks
            relevant_requirements = list(self.compliance_requirements.values())
        
        total_requirements = len(relevant_requirements)
        compliant_requirements = len([
            req for req in relevant_requirements
            if req.compliance_status == "compliant"
        ])
        
        # Calculate compliance score
        compliance_score = (compliant_requirements / max(total_requirements, 1)) * 100
        
        # Identify upcoming assessments
        upcoming_assessments = [
            req for req in relevant_requirements
            if req.next_assessment <= datetime.now() + timedelta(days=30)
        ]
        
        # Identify critical non-compliance
        critical_issues = [
            req for req in relevant_requirements
            if req.compliance_status != "compliant" and 
            req.criticality == GovernanceLevel.CRITICAL
        ]
        
        return {
            "compliance_score": round(compliance_score, 1),
            "total_requirements": total_requirements,
            "compliant_requirements": compliant_requirements,
            "upcoming_assessments": len(upcoming_assessments),
            "critical_issues": len(critical_issues),
            "framework_breakdown": self._get_framework_breakdown(relevant_requirements),
            "assessment_schedule": [
                {
                    "requirement_id": req.id,
                    "title": req.title,
                    "framework": req.framework.value,
                    "next_assessment": req.next_assessment.isoformat(),
                    "criticality": req.criticality.value
                }
                for req in upcoming_assessments[:5]  # Top 5 upcoming
            ]
        }
    
    def _get_framework_breakdown(self, requirements: List[ComplianceRequirement]) -> Dict[str, Dict]:
        """Get compliance breakdown by framework"""
        breakdown = {}
        
        for req in requirements:
            framework = req.framework.value
            if framework not in breakdown:
                breakdown[framework] = {
                    "total": 0,
                    "compliant": 0,
                    "non_compliant": 0,
                    "pending_assessment": 0
                }
            
            breakdown[framework]["total"] += 1
            
            if req.compliance_status == "compliant":
                breakdown[framework]["compliant"] += 1
            elif req.compliance_status == "non_compliant":
                breakdown[framework]["non_compliant"] += 1
            else:
                breakdown[framework]["pending_assessment"] += 1
        
        # Calculate percentages
        for framework_data in breakdown.values():
            total = framework_data["total"]
            framework_data["compliance_percentage"] = round(
                (framework_data["compliant"] / max(total, 1)) * 100, 1
            )
        
        return breakdown
    
    def create_privacy_impact_assessment(self, processing_activity: Dict[str, Any]) -> str:
        """Create Privacy Impact Assessment (PIA)"""
        pia_id = str(uuid.uuid4())
        
        pia = {
            "id": pia_id,
            "processing_activity": processing_activity["name"],
            "description": processing_activity["description"],
            "data_types": processing_activity.get("data_types", []),
            "processing_purposes": processing_activity.get("purposes", []),
            "data_subjects": processing_activity.get("data_subjects", []),
            "recipients": processing_activity.get("recipients", []),
            "retention_period": processing_activity.get("retention_period", ""),
            "transfer_countries": processing_activity.get("transfer_countries", []),
            "risk_assessment": {
                "likelihood": "medium",
                "impact": "medium", 
                "overall_risk": "medium"
            },
            "mitigation_measures": [
                "Data encryption at rest and in transit",
                "Access controls and authentication",
                "Regular security assessments",
                "Data minimization practices"
            ],
            "legal_basis": processing_activity.get("legal_basis", "consent"),
            "created_date": datetime.now(),
            "review_date": datetime.now() + timedelta(days=365),
            "status": "draft",
            "approved_by": None
        }
        
        # Log PIA creation
        self._log_audit_event("pia_created", {
            "pia_id": pia_id,
            "processing_activity": pia["processing_activity"],
            "risk_level": pia["risk_assessment"]["overall_risk"]
        })
        
        return pia_id
    
    def generate_compliance_report(self, frameworks: List[str] = None) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        
        if not frameworks:
            frameworks = [f.value for f in ComplianceFramework]
        
        report = {
            "report_id": str(uuid.uuid4()),
            "generated_date": datetime.now().isoformat(),
            "reporting_period": {
                "start": (datetime.now() - timedelta(days=90)).isoformat(),
                "end": datetime.now().isoformat()
            },
            "frameworks_covered": frameworks,
            "executive_summary": {},
            "detailed_findings": {},
            "recommendations": [],
            "action_items": []
        }
        
        # Generate executive summary
        overall_compliance = self.assess_compliance_status()
        report["executive_summary"] = {
            "overall_compliance_score": overall_compliance["compliance_score"],
            "total_requirements_assessed": overall_compliance["total_requirements"],
            "critical_issues_count": overall_compliance["critical_issues"],
            "upcoming_assessments": overall_compliance["upcoming_assessments"]
        }
        
        # Generate detailed findings for each framework
        for framework in frameworks:
            framework_compliance = self.assess_compliance_status(framework)
            report["detailed_findings"][framework] = framework_compliance
        
        # Generate recommendations
        report["recommendations"] = [
            "Implement automated compliance monitoring",
            "Establish continuous control testing",
            "Enhance incident response procedures",
            "Strengthen vendor risk management",
            "Improve documentation and evidence collection"
        ]
        
        # Generate action items
        report["action_items"] = [
            {
                "priority": "high",
                "item": "Complete outstanding GDPR consent management updates",
                "owner": "Privacy Engineering",
                "due_date": (datetime.now() + timedelta(days=30)).isoformat()
            },
            {
                "priority": "medium", 
                "item": "Conduct quarterly SOC2 control testing",
                "owner": "Internal Audit",
                "due_date": (datetime.now() + timedelta(days=60)).isoformat()
            }
        ]
        
        return report
    
    def implement_governance_controls(self, operation_type: str, 
                                   data: Dict[str, Any]) -> Dict[str, Any]:
        """Implement governance controls for operations"""
        
        # Determine governance level required
        governance_level = self._determine_governance_level(operation_type, data)
        
        controls = {
            "operation_type": operation_type,
            "governance_level": governance_level.value,
            "controls_applied": [],
            "approvals_required": [],
            "audit_trail": [],
            "compliance_validation": []
        }
        
        # Apply controls based on governance level
        if governance_level in [GovernanceLevel.HIGH, GovernanceLevel.CRITICAL]:
            controls["controls_applied"].extend([
                "Multi-party approval required",
                "Audit logging enabled",
                "Compliance validation required"
            ])
            
            if governance_level == GovernanceLevel.CRITICAL:
                controls["approvals_required"].extend([
                    "Data Steward approval",
                    "Security team approval",
                    "Legal team review"
                ])
        
        # Log governance application
        self._log_audit_event("governance_controls_applied", {
            "operation_type": operation_type,
            "governance_level": governance_level.value,
            "controls_count": len(controls["controls_applied"])
        })
        
        return controls
    
    def _determine_governance_level(self, operation_type: str, 
                                  data: Dict[str, Any]) -> GovernanceLevel:
        """Determine appropriate governance level"""
        
        # High-risk operations require critical governance
        critical_operations = [
            "genomic_data_processing",
            "clinical_data_access",
            "marketplace_organism_approval",
            "enterprise_data_export"
        ]
        
        high_risk_operations = [
            "user_data_processing",
            "third_party_integration",
            "research_data_sharing"
        ]
        
        if operation_type in critical_operations:
            return GovernanceLevel.CRITICAL
        elif operation_type in high_risk_operations:
            return GovernanceLevel.HIGH
        elif "sensitive" in data.get("data_classification", "").lower():
            return GovernanceLevel.HIGH
        else:
            return GovernanceLevel.MEDIUM
    
    def _log_audit_event(self, event_type: str, event_data: Dict[str, Any]):
        """Log audit event for compliance tracking"""
        
        audit_log_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "event_data": event_data,
            "environment": self.environment,
            "user_context": event_data.get("user_id", "system"),
            "session_id": event_data.get("session_id", ""),
            "ip_address": event_data.get("ip_address", ""),
            "system_component": "compliance_engine"
        }
        
        self.audit_logs.append(audit_log_entry)
        
        # In production, this would be sent to a secure audit log system
        # For now, we store in memory and would implement persistent storage
    
    def get_governance_dashboard(self) -> Dict[str, Any]:
        """Get governance dashboard metrics"""
        
        # Count policies by category
        policy_categories = {}
        for policy in self.governance_policies.values():
            category = policy.category
            policy_categories[category] = policy_categories.get(category, 0) + 1
        
        # Count audit events by type
        recent_events = [
            log for log in self.audit_logs
            if datetime.fromisoformat(log["timestamp"]) > datetime.now() - timedelta(days=30)
        ]
        
        event_types = {}
        for event in recent_events:
            event_type = event["event_type"]
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        return {
            "total_compliance_requirements": len(self.compliance_requirements),
            "active_governance_policies": len(self.governance_policies),
            "security_audits_in_progress": len([
                a for a in self.security_audits.values()
                if a.status == AuditStatus.IN_PROGRESS
            ]),
            "recent_audit_events": len(recent_events),
            "policy_categories": policy_categories,
            "recent_event_types": event_types,
            "compliance_frameworks_supported": len(ComplianceFramework),
            "governance_levels_implemented": len(GovernanceLevel),
            "last_updated": datetime.now().isoformat()
        }

# Global compliance engine instance
compliance_engine = ComplianceEngine()

def get_compliance_engine(environment: str = None) -> ComplianceEngine:
    """Get compliance engine instance"""
    if environment:
        return ComplianceEngine(environment)
    return compliance_engine