# Market Segmentation and Vertical-Specific Configurations
# Enables targeting of biotech, cloud providers, AI research, finance, and IoT markets

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class MarketVertical(Enum):
    """Target market verticals for DNA-Lang platform"""
    BIOTECH_LIFE_SCIENCES = "biotech_life_sciences"
    CLOUD_INFRASTRUCTURE = "cloud_infrastructure"
    AI_RESEARCH = "ai_research"
    FINANCIAL_SERVICES = "financial_services"
    IOT_MANUFACTURING = "iot_manufacturing"
    HEALTHCARE_PROVIDERS = "healthcare_providers"
    PHARMACEUTICAL = "pharmaceutical"
    ACADEMIC_RESEARCH = "academic_research"

class RegionPriority(Enum):
    """Regional deployment priorities"""
    TIER_1 = "tier_1"  # US, EU, Singapore, Japan
    TIER_2 = "tier_2"  # Canada, Australia, South Korea
    TIER_3 = "tier_3"  # India, Brazil, Mexico
    EMERGING = "emerging"  # Other emerging markets

@dataclass
class VerticalConfig:
    """Configuration for specific market vertical"""
    vertical: MarketVertical
    name: str
    description: str
    target_personas: List[str]
    key_use_cases: List[str]
    compliance_requirements: List[str]
    preferred_deployment: str
    pricing_model: str
    feature_priorities: List[str]
    integration_requirements: List[str]
    go_to_market_strategy: Dict[str, Any]

@dataclass
class RegionalConfig:
    """Configuration for regional deployment"""
    region_code: str
    region_name: str
    priority: RegionPriority
    languages: List[str]
    currencies: List[str]
    compliance_frameworks: List[str]
    data_residency_required: bool
    local_partnerships: List[str]
    market_maturity: str
    regulatory_complexity: str

class MarketSegmentation:
    """
    Market segmentation engine for DNA-Lang platform
    Provides vertical-specific and regional configurations
    """
    
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.vertical_configs = self._initialize_vertical_configs()
        self.regional_configs = self._initialize_regional_configs()
        self.market_analytics = {}
    
    def _initialize_vertical_configs(self) -> Dict[MarketVertical, VerticalConfig]:
        """Initialize configurations for each market vertical"""
        configs = {}
        
        # Biotech & Life Sciences
        configs[MarketVertical.BIOTECH_LIFE_SCIENCES] = VerticalConfig(
            vertical=MarketVertical.BIOTECH_LIFE_SCIENCES,
            name="Biotech & Life Sciences",
            description="Genomic research, drug discovery, and personalized medicine",
            target_personas=["Research Scientists", "Bioinformaticians", "Lab Directors", "CROs"],
            key_use_cases=[
                "Genomic variant analysis",
                "Drug target identification", 
                "Personalized treatment protocols",
                "Clinical trial optimization",
                "Biomarker discovery"
            ],
            compliance_requirements=["HIPAA", "GDPR", "FDA 21 CFR Part 11", "GxP"],
            preferred_deployment="hybrid_cloud",
            pricing_model="per_analysis_subscription",
            feature_priorities=[
                "genomic_analysis", "digital_twins", "clinical_integration",
                "regulatory_reporting", "research_collaboration"
            ],
            integration_requirements=[
                "LIMS systems", "EHR integration", "Clinical trial management",
                "Regulatory databases", "Research data repositories"
            ],
            go_to_market_strategy={
                "primary_channels": ["scientific_conferences", "peer_reviewed_publications", "KOL_engagement"],
                "content_strategy": ["research_papers", "case_studies", "webinars"],
                "partnership_focus": ["academic_institutions", "biotech_companies", "CROs"],
                "trial_approach": "pilot_studies_with_publications"
            }
        )
        
        # Cloud Infrastructure Providers
        configs[MarketVertical.CLOUD_INFRASTRUCTURE] = VerticalConfig(
            vertical=MarketVertical.CLOUD_INFRASTRUCTURE,
            name="Cloud Infrastructure Providers",
            description="Adaptive cloud infrastructure and autonomous orchestration",
            target_personas=["Cloud Architects", "DevOps Engineers", "Platform Teams", "CTOs"],
            key_use_cases=[
                "Autonomous infrastructure scaling",
                "Cost optimization through adaptation",
                "Multi-cloud orchestration",
                "Edge computing management",
                "Resource prediction and allocation"
            ],
            compliance_requirements=["SOC2", "ISO 27001", "PCI DSS", "FedRAMP"],
            preferred_deployment="multi_cloud",
            pricing_model="usage_based_consumption",
            feature_priorities=[
                "autonomous_scaling", "cost_optimization", "multi_cloud_support",
                "monitoring_analytics", "api_integration"
            ],
            integration_requirements=[
                "Kubernetes", "Terraform", "Cloud provider APIs",
                "Monitoring tools", "CI/CD pipelines"
            ],
            go_to_market_strategy={
                "primary_channels": ["cloud_marketplaces", "technology_partnerships", "developer_communities"],
                "content_strategy": ["technical_blogs", "architecture_guides", "performance_benchmarks"],
                "partnership_focus": ["cloud_providers", "devops_vendors", "system_integrators"],
                "trial_approach": "free_tier_with_usage_limits"
            }
        )
        
        # AI Research
        configs[MarketVertical.AI_RESEARCH] = VerticalConfig(
            vertical=MarketVertical.AI_RESEARCH,
            name="AI Research & Development",
            description="Advanced AI research and autonomous learning systems",
            target_personas=["AI Researchers", "ML Engineers", "Data Scientists", "Research Directors"],
            key_use_cases=[
                "Autonomous model evolution",
                "Research experiment management",
                "Collaborative AI development",
                "Model marketplace and sharing",
                "Advanced analytics and insights"
            ],
            compliance_requirements=["Research Ethics", "Data Protection", "IP Protection"],
            preferred_deployment="research_cloud",
            pricing_model="academic_subscription",
            feature_priorities=[
                "model_evolution", "experiment_tracking", "collaboration_tools",
                "data_management", "compute_optimization"
            ],
            integration_requirements=[
                "ML frameworks", "Jupyter notebooks", "Version control",
                "Research databases", "Compute clusters"
            ],
            go_to_market_strategy={
                "primary_channels": ["academic_conferences", "research_partnerships", "open_source_community"],
                "content_strategy": ["research_papers", "open_source_contributions", "technical_documentation"],
                "partnership_focus": ["universities", "research_institutes", "tech_companies"],
                "trial_approach": "academic_free_access"
            }
        )
        
        # Financial Services
        configs[MarketVertical.FINANCIAL_SERVICES] = VerticalConfig(
            vertical=MarketVertical.FINANCIAL_SERVICES,
            name="Financial Services",
            description="Risk modeling, algorithmic trading, and financial analytics",
            target_personas=["Quants", "Risk Managers", "Trading Desks", "FinTech CTOs"],
            key_use_cases=[
                "Adaptive risk modeling",
                "Algorithmic trading optimization",
                "Fraud detection and prevention",
                "Regulatory compliance automation",
                "Portfolio optimization"
            ],
            compliance_requirements=["PCI DSS", "SOX", "MiFID II", "Basel III", "GDPR"],
            preferred_deployment="private_cloud",
            pricing_model="enterprise_license",
            feature_priorities=[
                "real_time_analytics", "risk_modeling", "compliance_reporting",
                "high_frequency_trading", "security_controls"
            ],
            integration_requirements=[
                "Trading systems", "Risk management platforms", "Market data feeds",
                "Regulatory reporting", "Core banking systems"
            ],
            go_to_market_strategy={
                "primary_channels": ["industry_conferences", "executive_briefings", "proof_of_concepts"],
                "content_strategy": ["whitepapers", "regulatory_guides", "ROI_studies"],
                "partnership_focus": ["fintech_vendors", "consulting_firms", "system_integrators"],
                "trial_approach": "enterprise_pilot_programs"
            }
        )
        
        # IoT & Manufacturing
        configs[MarketVertical.IOT_MANUFACTURING] = VerticalConfig(
            vertical=MarketVertical.IOT_MANUFACTURING,
            name="IoT & Manufacturing",
            description="Industrial IoT, smart manufacturing, and autonomous systems",
            target_personas=["IoT Architects", "Manufacturing Engineers", "Operations Managers", "Plant Directors"],
            key_use_cases=[
                "Predictive maintenance",
                "Quality control automation",
                "Supply chain optimization",
                "Energy management",
                "Safety monitoring"
            ],
            compliance_requirements=["ISO 27001", "IEC 62443", "NIST Framework"],
            preferred_deployment="edge_cloud_hybrid",
            pricing_model="per_device_subscription",
            feature_priorities=[
                "edge_computing", "real_time_processing", "predictive_analytics",
                "device_management", "industrial_protocols"
            ],
            integration_requirements=[
                "Industrial protocols", "SCADA systems", "MES integration",
                "ERP systems", "IoT platforms"
            ],
            go_to_market_strategy={
                "primary_channels": ["industrial_trade_shows", "manufacturing_partnerships", "system_integrators"],
                "content_strategy": ["case_studies", "ROI_calculators", "technical_specifications"],
                "partnership_focus": ["industrial_vendors", "system_integrators", "IoT_platforms"],
                "trial_approach": "factory_floor_pilots"
            }
        )
        
        return configs
    
    def _initialize_regional_configs(self) -> Dict[str, RegionalConfig]:
        """Initialize regional deployment configurations"""
        configs = {}
        
        # Tier 1 Regions
        configs["us"] = RegionalConfig(
            region_code="us",
            region_name="United States",
            priority=RegionPriority.TIER_1,
            languages=["en-US"],
            currencies=["USD"],
            compliance_frameworks=["HIPAA", "SOC2", "FedRAMP", "NIST"],
            data_residency_required=True,
            local_partnerships=["AWS", "Microsoft", "Google", "Accenture", "Deloitte"],
            market_maturity="mature",
            regulatory_complexity="high"
        )
        
        configs["eu"] = RegionalConfig(
            region_code="eu",
            region_name="European Union",
            priority=RegionPriority.TIER_1,
            languages=["en-GB", "de-DE", "fr-FR", "es-ES", "it-IT"],
            currencies=["EUR", "GBP"],
            compliance_frameworks=["GDPR", "MedDRA", "EMA", "ISO 27001"],
            data_residency_required=True,
            local_partnerships=["SAP", "Siemens", "Atos", "Capgemini"],
            market_maturity="mature",
            regulatory_complexity="very_high"
        )
        
        configs["sg"] = RegionalConfig(
            region_code="sg",
            region_name="Singapore",
            priority=RegionPriority.TIER_1,
            languages=["en-SG", "zh-CN"],
            currencies=["SGD"],
            compliance_frameworks=["PDPA", "MAS", "HSA"],
            data_residency_required=False,
            local_partnerships=["GovTech", "A*STAR", "NCS"],
            market_maturity="high",
            regulatory_complexity="moderate"
        )
        
        configs["jp"] = RegionalConfig(
            region_code="jp",
            region_name="Japan",
            priority=RegionPriority.TIER_1,
            languages=["ja-JP", "en-JP"],
            currencies=["JPY"],
            compliance_frameworks=["APPI", "PMDA", "NISC"],
            data_residency_required=True,
            local_partnerships=["NTT", "Fujitsu", "NEC", "SoftBank"],
            market_maturity="mature",
            regulatory_complexity="high"
        )
        
        # Tier 2 Regions
        configs["ca"] = RegionalConfig(
            region_code="ca",
            region_name="Canada",
            priority=RegionPriority.TIER_2,
            languages=["en-CA", "fr-CA"],
            currencies=["CAD"],
            compliance_frameworks=["PIPEDA", "Health Canada", "CSA"],
            data_residency_required=True,
            local_partnerships=["Shopify", "CGI", "IBM Canada"],
            market_maturity="mature",
            regulatory_complexity="moderate"
        )
        
        return configs
    
    def get_vertical_config(self, vertical: str) -> Dict[str, Any]:
        """Get configuration for specific vertical"""
        vertical_enum = MarketVertical(vertical)
        if vertical_enum in self.vertical_configs:
            return asdict(self.vertical_configs[vertical_enum])
        return {}
    
    def get_regional_config(self, region: str) -> Dict[str, Any]:
        """Get configuration for specific region"""
        if region in self.regional_configs:
            return asdict(self.regional_configs[region])
        return {}
    
    def recommend_verticals_for_region(self, region: str) -> List[Dict[str, Any]]:
        """Recommend target verticals for specific region"""
        regional_config = self.regional_configs.get(region)
        if not regional_config:
            return []
        
        # Market maturity and regulatory complexity influence vertical prioritization
        if regional_config.market_maturity == "mature":
            if regional_config.regulatory_complexity in ["high", "very_high"]:
                # Mature, high-regulation markets
                priority_verticals = [
                    MarketVertical.BIOTECH_LIFE_SCIENCES,
                    MarketVertical.FINANCIAL_SERVICES,
                    MarketVertical.HEALTHCARE_PROVIDERS
                ]
            else:
                # Mature, moderate-regulation markets
                priority_verticals = [
                    MarketVertical.CLOUD_INFRASTRUCTURE,
                    MarketVertical.AI_RESEARCH,
                    MarketVertical.IOT_MANUFACTURING
                ]
        else:
            # Emerging markets - focus on technology adoption
            priority_verticals = [
                MarketVertical.CLOUD_INFRASTRUCTURE,
                MarketVertical.AI_RESEARCH,
                MarketVertical.ACADEMIC_RESEARCH
            ]
        
        recommendations = []
        for vertical in priority_verticals:
            if vertical in self.vertical_configs:
                config = asdict(self.vertical_configs[vertical])
                config["fit_score"] = self._calculate_regional_fit(vertical, region)
                recommendations.append(config)
        
        return sorted(recommendations, key=lambda x: x["fit_score"], reverse=True)
    
    def _calculate_regional_fit(self, vertical: MarketVertical, region: str) -> float:
        """Calculate fit score between vertical and region"""
        regional_config = self.regional_configs.get(region)
        vertical_config = self.vertical_configs.get(vertical)
        
        if not regional_config or not vertical_config:
            return 0.0
        
        fit_score = 0.0
        
        # Market maturity alignment
        if regional_config.market_maturity == "mature":
            if vertical in [MarketVertical.BIOTECH_LIFE_SCIENCES, MarketVertical.FINANCIAL_SERVICES]:
                fit_score += 0.3
        
        # Regulatory complexity alignment
        if regional_config.regulatory_complexity in ["high", "very_high"]:
            if "compliance_reporting" in vertical_config.feature_priorities:
                fit_score += 0.3
        
        # Partnership ecosystem alignment
        partnership_bonus = len(set(regional_config.local_partnerships) & 
                               set(vertical_config.go_to_market_strategy.get("partnership_focus", []))) * 0.1
        fit_score += min(partnership_bonus, 0.2)
        
        # Data residency requirements
        if regional_config.data_residency_required:
            if vertical_config.preferred_deployment in ["private_cloud", "hybrid_cloud"]:
                fit_score += 0.2
        
        return min(fit_score, 1.0)
    
    def create_market_entry_plan(self, vertical: str, regions: List[str]) -> Dict[str, Any]:
        """Create market entry plan for vertical across regions"""
        vertical_config = self.get_vertical_config(vertical)
        regional_analysis = []
        
        for region in regions:
            regional_config = self.get_regional_config(region)
            if regional_config:
                fit_score = self._calculate_regional_fit(MarketVertical(vertical), region)
                regional_analysis.append({
                    "region": region,
                    "config": regional_config,
                    "fit_score": fit_score,
                    "entry_complexity": self._assess_entry_complexity(region),
                    "time_to_market_months": self._estimate_time_to_market(region, vertical)
                })
        
        # Sort regions by fit score and entry complexity
        regional_analysis.sort(key=lambda x: (x["fit_score"], -x["entry_complexity"]), reverse=True)
        
        entry_plan = {
            "vertical": vertical,
            "target_regions": regions,
            "regional_analysis": regional_analysis,
            "recommended_sequence": [r["region"] for r in regional_analysis],
            "total_addressable_market": self._estimate_tam(vertical, regions),
            "go_to_market_strategy": vertical_config.get("go_to_market_strategy", {}),
            "success_metrics": self._define_market_entry_metrics(vertical),
            "risk_mitigation": self._identify_market_risks(vertical, regions),
            "created_at": datetime.now().isoformat()
        }
        
        return entry_plan
    
    def _assess_entry_complexity(self, region: str) -> int:
        """Assess market entry complexity (1-10 scale)"""
        regional_config = self.regional_configs.get(region)
        if not regional_config:
            return 10
        
        complexity = 1
        
        # Regulatory complexity
        if regional_config.regulatory_complexity == "very_high":
            complexity += 4
        elif regional_config.regulatory_complexity == "high":
            complexity += 3
        elif regional_config.regulatory_complexity == "moderate":
            complexity += 1
        
        # Data residency requirements
        if regional_config.data_residency_required:
            complexity += 2
        
        # Language localization needs
        if len(regional_config.languages) > 2:
            complexity += 1
        
        # Number of compliance frameworks
        if len(regional_config.compliance_frameworks) > 3:
            complexity += 1
        
        return min(complexity, 10)
    
    def _estimate_time_to_market(self, region: str, vertical: str) -> int:
        """Estimate time to market in months"""
        base_time = 6  # Base 6 months
        complexity = self._assess_entry_complexity(region)
        
        # Add time based on complexity
        additional_time = (complexity - 1) * 0.5
        
        # Vertical-specific adjustments
        if vertical in ["biotech_life_sciences", "financial_services"]:
            additional_time += 3  # Higher regulatory requirements
        
        return int(base_time + additional_time)
    
    def _estimate_tam(self, vertical: str, regions: List[str]) -> Dict[str, Any]:
        """Estimate Total Addressable Market"""
        # Simplified TAM estimation based on vertical and regions
        vertical_market_sizes = {
            "biotech_life_sciences": 100_000_000,  # $100M
            "cloud_infrastructure": 500_000_000,   # $500M
            "ai_research": 50_000_000,             # $50M
            "financial_services": 200_000_000,     # $200M
            "iot_manufacturing": 150_000_000       # $150M
        }
        
        region_multipliers = {
            "us": 1.0,
            "eu": 0.8,
            "sg": 0.1,
            "jp": 0.6,
            "ca": 0.2
        }
        
        base_tam = vertical_market_sizes.get(vertical, 50_000_000)
        total_multiplier = sum(region_multipliers.get(region, 0.1) for region in regions)
        
        return {
            "total_tam_usd": int(base_tam * total_multiplier),
            "vertical_base_tam": base_tam,
            "regional_multiplier": total_multiplier,
            "regions_included": regions
        }
    
    def _define_market_entry_metrics(self, vertical: str) -> List[str]:
        """Define success metrics for market entry"""
        base_metrics = [
            "Customer acquisition rate",
            "Revenue growth rate",
            "Market share capture",
            "Partner channel development",
            "Brand awareness metrics"
        ]
        
        vertical_specific = {
            "biotech_life_sciences": ["Research publication citations", "Clinical trial partnerships"],
            "cloud_infrastructure": ["API adoption rate", "Compute resource utilization"],
            "ai_research": ["Academic collaborations", "Open source contributions"],
            "financial_services": ["Regulatory compliance score", "Risk reduction metrics"],
            "iot_manufacturing": ["Device deployment count", "Operational efficiency gains"]
        }
        
        return base_metrics + vertical_specific.get(vertical, [])
    
    def _identify_market_risks(self, vertical: str, regions: List[str]) -> List[Dict[str, str]]:
        """Identify and categorize market entry risks"""
        risks = [
            {
                "type": "regulatory",
                "description": "Changing regulatory requirements",
                "mitigation": "Maintain compliance monitoring and legal partnerships"
            },
            {
                "type": "competitive",
                "description": "Strong local competitors",
                "mitigation": "Focus on differentiation and partnership advantages"
            },
            {
                "type": "technical",
                "description": "Integration complexity with local systems",
                "mitigation": "Develop regional system integrator partnerships"
            }
        ]
        
        return risks
    
    def get_market_analytics(self) -> Dict[str, Any]:
        """Get market segmentation analytics"""
        total_verticals = len(self.vertical_configs)
        total_regions = len(self.regional_configs)
        
        tier_1_regions = len([r for r in self.regional_configs.values() 
                             if r.priority == RegionPriority.TIER_1])
        
        high_value_verticals = len([v for v in self.vertical_configs.values()
                                   if v.pricing_model in ["enterprise_license", "per_analysis_subscription"]])
        
        return {
            "total_verticals_configured": total_verticals,
            "total_regions_configured": total_regions,
            "tier_1_regions": tier_1_regions,
            "high_value_verticals": high_value_verticals,
            "compliance_frameworks_supported": len(set(
                framework for config in self.regional_configs.values()
                for framework in config.compliance_frameworks
            )),
            "languages_supported": len(set(
                lang for config in self.regional_configs.values()
                for lang in config.languages
            ))
        }

# Global market segmentation instance
market_segmentation = MarketSegmentation()

def get_market_segmentation(environment: str = None) -> MarketSegmentation:
    """Get market segmentation instance"""
    if environment:
        return MarketSegmentation(environment)
    return market_segmentation