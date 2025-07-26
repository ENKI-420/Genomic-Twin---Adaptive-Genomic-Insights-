import React, { useState } from 'react';

interface Gene {
  id: string;
  name: string;
  description: string;
  price: number;
  seller: string;
  timestamp: string;
}

interface MarketplaceData {
  genes: Gene[];
  trades: any[];
  activeOffers: any[];
}

interface MarketplaceData {
  genes: Gene[];
  trades: any[];
  activeOffers: any[];
}

interface MarketplaceViewProps {
  marketplaceData: MarketplaceData;
  onActivateAgent: (agentType: string) => void;
}

const MarketplaceView: React.FC<MarketplaceViewProps> = ({ marketplaceData, onActivateAgent }) => {
  const [selectedGene, setSelectedGene] = useState<Gene | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'price' | 'name' | 'recent'>('recent');

  const filteredGenes = marketplaceData.genes
    .filter(gene => 
      gene.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      gene.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      gene.seller.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      switch (sortBy) {
        case 'price':
          return a.price - b.price;
        case 'name':
          return a.name.localeCompare(b.name);
        case 'recent':
        default:
          return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime();
      }
    });

  const handlePurchaseGene = (gene: Gene) => {
    // Simulate gene purchase
    console.log('Purchasing gene:', gene.id);
    // In a real implementation, this would make an API call
  };

  const getGeneTypeIcon = (name: string) => {
    if (name.toLowerCase().includes('resilience')) return '🛡️';
    if (name.toLowerCase().includes('adaptation')) return '🔄';
    if (name.toLowerCase().includes('intelligence')) return '🧠';
    if (name.toLowerCase().includes('speed')) return '⚡';
    if (name.toLowerCase().includes('memory')) return '💾';
    return '🧬';
  };

  const getSellerIcon = (seller: string) => {
    const icons: { [key: string]: string } = {
      'cloud_architect': '☁️',
      'meta_cognition': '🧠',
      'biography': '📚',
      'evolution_engine': '🧬'
    };
    return icons[seller] || '🤖';
  };

  const agentTypes = [
    { id: 'cloud_architect', name: 'Cloud Architect', description: 'Manages infrastructure provisioning' },
    { id: 'meta_cognition', name: 'Meta Cognition', description: 'Advanced reasoning and optimization' },
    { id: 'biography', name: 'Biography Agent', description: 'Tracks organism history and lineage' }
  ];

  return (
    <div className="marketplace-view">
      <div className="marketplace-panel">
        <h2>Gene Marketplace</h2>
        
        <div className="marketplace-controls">
          <div className="search-section">
            <input
              type="text"
              placeholder="Search genes..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
          
          <div className="sort-section">
            <label>Sort by:</label>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value as 'price' | 'name' | 'recent')}
              className="sort-select"
            >
              <option value="recent">Most Recent</option>
              <option value="price">Price (Low to High)</option>
              <option value="name">Name (A-Z)</option>
            </select>
          </div>
        </div>

        <div className="genes-grid">
          {filteredGenes.length === 0 ? (
            <div className="empty-state">
              <p>No genes available in the marketplace</p>
              <p>Genes will appear as organisms evolve and agents become active</p>
            </div>
          ) : (
            filteredGenes.map(gene => (
              <div 
                key={gene.id}
                className={`gene-card ${selectedGene?.id === gene.id ? 'selected' : ''}`}
                onClick={() => setSelectedGene(gene)}
              >
                <div className="gene-header">
                  <span className="gene-icon">{getGeneTypeIcon(gene.name)}</span>
                  <h3 className="gene-name">{gene.name}</h3>
                </div>
                
                <p className="gene-description">{gene.description}</p>
                
                <div className="gene-footer">
                  <div className="gene-price">
                    <span className="price-label">Price:</span>
                    <span className="price-value">{gene.price} credits</span>
                  </div>
                  <div className="gene-seller">
                    <span className="seller-icon">{getSellerIcon(gene.seller)}</span>
                    <span className="seller-name">{gene.seller.replace(/_/g, ' ')}</span>
                  </div>
                </div>
                
                <button 
                  className="purchase-button"
                  onClick={(e) => {
                    e.stopPropagation();
                    handlePurchaseGene(gene);
                  }}
                >
                  Purchase Gene
                </button>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="agents-panel">
        <h3>Agent Control</h3>
        <p>Activate agents to generate new genes and marketplace activity</p>
        
        <div className="agents-grid">
          {agentTypes.map(agent => (
            <div key={agent.id} className="agent-card">
              <div className="agent-info">
                <h4>{agent.name}</h4>
                <p>{agent.description}</p>
              </div>
              <button 
                className="activate-button"
                onClick={() => onActivateAgent(agent.id)}
              >
                Activate {getSellerIcon(agent.id)}
              </button>
            </div>
          ))}
        </div>

        {marketplaceData.trades.length > 0 && (
          <div className="recent-trades">
            <h4>Recent Trades</h4>
            <div className="trades-list">
              {marketplaceData.trades.slice(-5).reverse().map((trade, index) => (
                <div key={index} className="trade-item">
                  <span className="trade-gene">{trade.geneName || 'Unknown Gene'}</span>
                  <span className="trade-price">{trade.price || 0} credits</span>
                  <span className="trade-time">
                    {trade.timestamp ? new Date(trade.timestamp).toLocaleTimeString() : 'Unknown time'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {selectedGene && (
        <div className="gene-details">
          <h3>Gene Details</h3>
          <button 
            className="close-button"
            onClick={() => setSelectedGene(null)}
          >
            ✕
          </button>
          
          <div className="detail-section">
            <div className="gene-detail-header">
              <span className="detail-icon">{getGeneTypeIcon(selectedGene.name)}</span>
              <h4>{selectedGene.name}</h4>
            </div>
            
            <div className="detail-info">
              <p><strong>Description:</strong> {selectedGene.description}</p>
              <p><strong>Seller:</strong> {getSellerIcon(selectedGene.seller)} {selectedGene.seller.replace(/_/g, ' ')}</p>
              <p><strong>Price:</strong> {selectedGene.price} credits</p>
              <p><strong>Listed:</strong> {new Date(selectedGene.timestamp).toLocaleString()}</p>
            </div>
          </div>

          <div className="detail-section">
            <h4>Gene Properties</h4>
            <div className="properties-grid">
              <div className="property">
                <span>Type:</span>
                <span>Enhancement</span>
              </div>
              <div className="property">
                <span>Rarity:</span>
                <span>Common</span>
              </div>
              <div className="property">
                <span>Compatibility:</span>
                <span>Universal</span>
              </div>
              <div className="property">
                <span>Effect Duration:</span>
                <span>Permanent</span>
              </div>
            </div>
          </div>

          <div className="detail-actions">
            <button 
              className="action-button primary"
              onClick={() => handlePurchaseGene(selectedGene)}
            >
              💳 Purchase Gene
            </button>
            <button className="action-button secondary">
              📊 View Analytics
            </button>
            <button className="action-button secondary">
              💬 Contact Seller
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default MarketplaceView;