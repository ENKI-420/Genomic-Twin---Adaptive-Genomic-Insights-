#!/usr/bin/env python3
"""
Simple Strategic Components Test
Tests the new strategic modules directly without dependencies
"""

def test_marketplace_direct():
    """Test marketplace module directly"""
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from modules.marketplace import DNALangMarketplace, MarketplaceCategory, DigitalOrganism
        from datetime import datetime
        
        marketplace = DNALangMarketplace("development")
        
        # Test organism registration
        organism_data = {
            "name": "Test Genomic Analyzer",
            "description": "Test organism for genomic analysis",
            "category": "biotech_organisms",
            "creator_id": "test_user",
            "price": 99.99,
            "capabilities": ["mutation_analysis", "variant_calling"]
        }
        
        organism_id = marketplace.register_organism(organism_data)
        print(f"✓ Organism registered: {organism_id}")
        
        # Test analytics
        analytics = marketplace.get_marketplace_analytics()
        print(f"✓ Analytics: {analytics['total_organisms']} organisms")
        
        return True
        
    except Exception as e:
        print(f"❌ Marketplace test failed: {e}")
        return False

def test_market_segmentation_direct():
    """Test market segmentation module directly"""
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from modules.market_segmentation import MarketSegmentation, MarketVertical
        
        market_seg = MarketSegmentation("development")
        
        # Test vertical configuration
        biotech_config = market_seg.get_vertical_config("biotech_life_sciences")
        print(f"✓ Biotech config: {biotech_config['name']}")
        
        # Test analytics
        analytics = market_seg.get_market_analytics()
        print(f"✓ Market analytics: {analytics['total_verticals_configured']} verticals")
        
        return True
        
    except Exception as e:
        print(f"❌ Market segmentation test failed: {e}")
        return False

def test_commercialization_direct():
    """Test commercialization module directly"""
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from modules.commercialization import CommercializationEngine, PricingModel
        from decimal import Decimal
        
        commerce = CommercializationEngine("development")
        
        # Test pricing calculation
        usage_data = {
            "analysis_runs": 150,
            "storage_gb": 25,
            "api_calls": 15000
        }
        
        pricing = commerce.calculate_pricing("professional", usage_data, "monthly")
        print(f"✓ Pricing calculated: ${pricing['total_cost']} total")
        
        # Test fee structure
        fees = commerce.create_marketplace_fee_structure()
        print(f"✓ Fee structure: {fees['organism_sales']['fee_percentage']}% fee")
        
        return True
        
    except Exception as e:
        print(f"❌ Commercialization test failed: {e}")
        return False

def test_developer_sdk_direct():
    """Test developer SDK module directly"""
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from modules.developer_sdk import DNALangSDK, SDKComponent
        from datetime import datetime, timedelta
        
        sdk = DNALangSDK("development")
        
        # Test package retrieval
        core_package = sdk.get_sdk_package("dna-lang-core")
        print(f"✓ Core package: {core_package['name']}")
        
        # Test event creation
        event_data = {
            "title": "Test Webinar",
            "description": "Test event",
            "date": (datetime.now() + timedelta(days=7)).isoformat(),
            "event_type": "webinar"
        }
        
        event_id = sdk.create_developer_event(event_data)
        print(f"✓ Event created: {event_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Developer SDK test failed: {e}")
        return False

def test_partner_integrations_direct():
    """Test partner integrations module directly"""
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from modules.partner_integrations import PartnerEcosystem, PartnerType
        
        ecosystem = PartnerEcosystem("development")
        
        # Test partner registration
        partner_data = {
            "name": "Test Partner",
            "type": "system_integrator",
            "description": "Test partner description",
            "capabilities": ["consulting"],
            "regions": ["us"]
        }
        
        partner_id = ecosystem.register_partner(partner_data)
        print(f"✓ Partner registered: {partner_id}")
        
        # Test analytics
        analytics = ecosystem.get_ecosystem_analytics()
        print(f"✓ Ecosystem analytics: {analytics['total_partners']} partners")
        
        return True
        
    except Exception as e:
        print(f"❌ Partner integrations test failed: {e}")
        return False

def test_compliance_governance_direct():
    """Test compliance governance module directly"""
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from modules.compliance_governance import ComplianceEngine, ComplianceFramework
        
        compliance = ComplianceEngine("development")
        
        # Test compliance assessment
        status = compliance.assess_compliance_status()
        print(f"✓ Compliance status: {status['compliance_score']}% score")
        
        # Test dashboard
        dashboard = compliance.get_governance_dashboard()
        print(f"✓ Governance dashboard: {dashboard['total_compliance_requirements']} requirements")
        
        return True
        
    except Exception as e:
        print(f"❌ Compliance governance test failed: {e}")
        return False

def main():
    """Run direct tests"""
    print("🧬 DNA-Lang Strategic Components Direct Test")
    print("=" * 50)
    
    tests = [
        ("Marketplace", test_marketplace_direct),
        ("Market Segmentation", test_market_segmentation_direct),
        ("Commercialization", test_commercialization_direct),
        ("Developer SDK", test_developer_sdk_direct),
        ("Partner Integrations", test_partner_integrations_direct),
        ("Compliance Governance", test_compliance_governance_direct)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- Testing {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*50)
    print("Results Summary:")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<25} {status}")
    
    print(f"\nPassed: {passed}/{len(results)}")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    
    if passed == len(results):
        print("\n🎉 All strategic components are working!")
        return 0
    else:
        print(f"\n⚠️  {failed} component(s) need attention.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())