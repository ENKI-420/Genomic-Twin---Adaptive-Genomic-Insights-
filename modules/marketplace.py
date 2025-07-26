# DNA-Lang Digital Organism Marketplace
# Core marketplace infrastructure for gene blueprints, bounties, and collaborations

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class MarketplaceCategory(Enum):
    """Marketplace categories for digital organisms and genes"""
    BIOTECH_ORGANISMS = "biotech_organisms"
    CLOUD_INFRASTRUCTURE = "cloud_infrastructure" 
    AI_RESEARCH = "ai_research"
    FINANCIAL_MODELS = "financial_models"
    IOT_SENSORS = "iot_sensors"
    GENE_BLUEPRINTS = "gene_blueprints"
    ADAPTATION_PATTERNS = "adaptation_patterns"

class TransactionStatus(Enum):
    """Transaction status for marketplace operations"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

@dataclass
class DigitalOrganism:
    """Digital organism marketplace item"""
    id: str
    name: str
    description: str
    category: MarketplaceCategory
    version: str
    creator_id: str
    price: float
    license_type: str
    capabilities: List[str]
    requirements: Dict[str, str]
    created_at: datetime
    updated_at: datetime
    downloads: int = 0
    rating: float = 0.0
    reviews: List[Dict] = None
    
    def __post_init__(self):
        if self.reviews is None:
            self.reviews = []

@dataclass
class GeneBounty:
    """Gene bounty for marketplace collaborations"""
    id: str
    title: str
    description: str
    reward_amount: float
    sponsor_id: str
    category: MarketplaceCategory
    requirements: List[str]
    deadline: datetime
    status: str
    submissions: List[Dict] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.submissions is None:
            self.submissions = []
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class MarketplaceTransaction:
    """Marketplace transaction record"""
    id: str
    buyer_id: str
    seller_id: str
    item_id: str
    item_type: str
    amount: float
    fee_amount: float
    status: TransactionStatus
    created_at: datetime
    completed_at: Optional[datetime] = None

class DNALangMarketplace:
    """
    Core marketplace for DNA-Lang digital organisms and gene blueprints
    Enables monetization through transaction fees and premium services
    """
    
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.fee_percentage = self._get_fee_percentage()
        self.organisms = {}
        self.bounties = {}
        self.transactions = {}
        self.users = {}
        
    def _get_fee_percentage(self) -> float:
        """Get marketplace fee percentage based on environment"""
        fee_rates = {
            "production": 0.05,   # 5% fee for production
            "staging": 0.03,      # 3% fee for staging
            "development": 0.01   # 1% fee for development
        }
        return fee_rates.get(self.environment, 0.05)
    
    def register_organism(self, organism_data: Dict[str, Any]) -> str:
        """Register a new digital organism in the marketplace"""
        organism_id = str(uuid.uuid4())
        organism = DigitalOrganism(
            id=organism_id,
            name=organism_data["name"],
            description=organism_data["description"],
            category=MarketplaceCategory(organism_data["category"]),
            version=organism_data.get("version", "1.0.0"),
            creator_id=organism_data["creator_id"],
            price=organism_data.get("price", 0.0),
            license_type=organism_data.get("license_type", "MIT"),
            capabilities=organism_data.get("capabilities", []),
            requirements=organism_data.get("requirements", {}),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.organisms[organism_id] = organism
        return organism_id
    
    def create_bounty(self, bounty_data: Dict[str, Any]) -> str:
        """Create a new gene bounty"""
        bounty_id = str(uuid.uuid4())
        bounty = GeneBounty(
            id=bounty_id,
            title=bounty_data["title"],
            description=bounty_data["description"],
            reward_amount=bounty_data["reward_amount"],
            sponsor_id=bounty_data["sponsor_id"],
            category=MarketplaceCategory(bounty_data["category"]),
            requirements=bounty_data.get("requirements", []),
            deadline=datetime.fromisoformat(bounty_data["deadline"]),
            status="open"
        )
        
        self.bounties[bounty_id] = bounty
        return bounty_id
    
    def purchase_organism(self, buyer_id: str, organism_id: str) -> str:
        """Process organism purchase transaction"""
        if organism_id not in self.organisms:
            raise ValueError(f"Organism {organism_id} not found")
        
        organism = self.organisms[organism_id]
        fee_amount = organism.price * self.fee_percentage
        transaction_id = str(uuid.uuid4())
        
        transaction = MarketplaceTransaction(
            id=transaction_id,
            buyer_id=buyer_id,
            seller_id=organism.creator_id,
            item_id=organism_id,
            item_type="organism",
            amount=organism.price,
            fee_amount=fee_amount,
            status=TransactionStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.transactions[transaction_id] = transaction
        
        # Simulate payment processing
        transaction.status = TransactionStatus.COMPLETED
        transaction.completed_at = datetime.now()
        organism.downloads += 1
        
        return transaction_id
    
    def search_organisms(self, query: str = "", category: str = "", 
                        price_range: tuple = None) -> List[Dict]:
        """Search marketplace organisms with filters"""
        results = []
        
        for organism in self.organisms.values():
            # Text search
            if query and query.lower() not in organism.name.lower() and \
               query.lower() not in organism.description.lower():
                continue
            
            # Category filter
            if category and organism.category.value != category:
                continue
            
            # Price filter
            if price_range and not (price_range[0] <= organism.price <= price_range[1]):
                continue
            
            results.append(asdict(organism))
        
        return sorted(results, key=lambda x: x["rating"], reverse=True)
    
    def get_marketplace_analytics(self) -> Dict[str, Any]:
        """Get marketplace analytics and metrics"""
        total_organisms = len(self.organisms)
        total_transactions = len([t for t in self.transactions.values() 
                                if t.status == TransactionStatus.COMPLETED])
        total_revenue = sum(t.amount for t in self.transactions.values() 
                          if t.status == TransactionStatus.COMPLETED)
        total_fees = sum(t.fee_amount for t in self.transactions.values() 
                        if t.status == TransactionStatus.COMPLETED)
        
        category_distribution = {}
        for organism in self.organisms.values():
            category = organism.category.value
            category_distribution[category] = category_distribution.get(category, 0) + 1
        
        return {
            "total_organisms": total_organisms,
            "total_transactions": total_transactions,
            "total_revenue": round(total_revenue, 2),
            "total_fees_collected": round(total_fees, 2),
            "category_distribution": category_distribution,
            "average_organism_price": round(total_revenue / max(total_transactions, 1), 2),
            "top_categories": sorted(category_distribution.items(), 
                                   key=lambda x: x[1], reverse=True)[:3]
        }
    
    def submit_bounty_solution(self, bounty_id: str, submitter_id: str, 
                              solution_data: Dict[str, Any]) -> bool:
        """Submit solution for a gene bounty"""
        if bounty_id not in self.bounties:
            return False
        
        bounty = self.bounties[bounty_id]
        if bounty.status != "open" or datetime.now() > bounty.deadline:
            return False
        
        submission = {
            "id": str(uuid.uuid4()),
            "submitter_id": submitter_id,
            "solution_data": solution_data,
            "submitted_at": datetime.now(),
            "status": "pending_review"
        }
        
        bounty.submissions.append(submission)
        return True
    
    def get_user_portfolio(self, user_id: str) -> Dict[str, Any]:
        """Get user's marketplace portfolio"""
        owned_organisms = [org for org in self.organisms.values() 
                         if org.creator_id == user_id]
        purchases = [t for t in self.transactions.values() 
                    if t.buyer_id == user_id and t.status == TransactionStatus.COMPLETED]
        sales = [t for t in self.transactions.values() 
                if t.seller_id == user_id and t.status == TransactionStatus.COMPLETED]
        
        return {
            "created_organisms": len(owned_organisms),
            "total_downloads": sum(org.downloads for org in owned_organisms),
            "total_revenue": sum(t.amount - t.fee_amount for t in sales),
            "total_purchases": len(purchases),
            "total_spent": sum(t.amount for t in purchases),
            "average_rating": sum(org.rating for org in owned_organisms) / max(len(owned_organisms), 1)
        }

# Marketplace instance for global use
marketplace = DNALangMarketplace()

def get_marketplace_instance(environment: str = None) -> DNALangMarketplace:
    """Get marketplace instance for specific environment"""
    if environment:
        return DNALangMarketplace(environment)
    return marketplace