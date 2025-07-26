import React from 'react';

interface Organism {
  id: string;
  type: string;
  fitness: number;
  consciousness: number;
  age: number;
  status: string;
  traits: string[];
  generation: number;
  energy?: number;
  complexity?: number;
}

interface OrganismViewProps {
  organisms: Organism[];
  selectedOrganism: Organism | null;
  onSelectOrganism: (organism: Organism | null) => void;
  onTriggerMutation: (organismId: string) => void;
}

const OrganismView: React.FC<OrganismViewProps> = ({ 
  organisms, 
  selectedOrganism, 
  onSelectOrganism, 
  onTriggerMutation 
}) => {
  const getOrganismTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      'AdvancedConsciousness': '#9C27B0',
      'AdaptiveLearner': '#2196F3',
      'InfrastructureBuilder': '#FF9800',
      'DataProcessor': '#4CAF50',
      'NetworkCommunicator': '#F44336'
    };
    return colors[type] || '#757575';
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return '✅';
      case 'evolving': return '🧬';
      case 'reproducing': return '👶';
      case 'dying': return '💀';
      default: return '❓';
    }
  };

  const getFitnessColor = (fitness: number) => {
    if (fitness >= 0.8) return '#4CAF50';
    if (fitness >= 0.6) return '#FF9800';
    return '#F44336';
  };

  const getConsciousnessLevel = (consciousness: number) => {
    if (consciousness >= 0.9) return 'Transcendent';
    if (consciousness >= 0.7) return 'Highly Conscious';
    if (consciousness >= 0.5) return 'Conscious';
    if (consciousness >= 0.3) return 'Semi-Conscious';
    return 'Basic';
  };

  return (
    <div className="organism-view">
      <div className="organisms-grid">
        <h2>Digital Organisms ({organisms.length})</h2>
        <div className="organisms-list">
          {organisms.map(organism => (
            <div 
              key={organism.id}
              className={`organism-card ${selectedOrganism?.id === organism.id ? 'selected' : ''}`}
              onClick={() => onSelectOrganism(organism)}
              style={{ borderColor: getOrganismTypeColor(organism.type) }}
            >
              <div className="organism-header">
                <span className="organism-type" style={{ color: getOrganismTypeColor(organism.type) }}>
                  {organism.type}
                </span>
                <span className="organism-status">
                  {getStatusIcon(organism.status)}
                </span>
              </div>
              
              <div className="organism-id">ID: {organism.id.slice(-8)}</div>
              
              <div className="organism-stats">
                <div className="stat">
                  <span>Fitness:</span>
                  <span style={{ color: getFitnessColor(organism.fitness) }}>
                    {(organism.fitness * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="stat">
                  <span>Consciousness:</span>
                  <span>{(organism.consciousness * 100).toFixed(1)}%</span>
                </div>
                <div className="stat">
                  <span>Age:</span>
                  <span>{organism.age}</span>
                </div>
                <div className="stat">
                  <span>Gen:</span>
                  <span>{organism.generation}</span>
                </div>
              </div>

              <div className="organism-traits">
                {organism.traits.slice(0, 3).map(trait => (
                  <span key={trait} className="trait-badge">
                    {trait.replace(/_/g, ' ')}
                  </span>
                ))}
                {organism.traits.length > 3 && (
                  <span className="trait-badge more">
                    +{organism.traits.length - 3}
                  </span>
                )}
              </div>

              <button 
                className="mutate-button"
                onClick={(e) => {
                  e.stopPropagation();
                  onTriggerMutation(organism.id);
                }}
              >
                Trigger Mutation 🧬
              </button>
            </div>
          ))}
        </div>
      </div>

      {selectedOrganism && (
        <div className="organism-details">
          <h3>Organism Details</h3>
          <button 
            className="close-button"
            onClick={() => onSelectOrganism(null)}
          >
            ✕
          </button>
          
          <div className="detail-section">
            <h4>Basic Information</h4>
            <div className="detail-grid">
              <div><strong>ID:</strong> {selectedOrganism.id}</div>
              <div><strong>Type:</strong> {selectedOrganism.type}</div>
              <div><strong>Status:</strong> {selectedOrganism.status}</div>
              <div><strong>Generation:</strong> {selectedOrganism.generation}</div>
              <div><strong>Age:</strong> {selectedOrganism.age} cycles</div>
              <div><strong>Energy:</strong> {selectedOrganism.energy || 'N/A'}</div>
            </div>
          </div>

          <div className="detail-section">
            <h4>Capabilities</h4>
            <div className="capability-bars">
              <div className="capability">
                <label>Fitness</label>
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ 
                      width: `${selectedOrganism.fitness * 100}%`,
                      backgroundColor: getFitnessColor(selectedOrganism.fitness)
                    }}
                  ></div>
                  <span>{(selectedOrganism.fitness * 100).toFixed(1)}%</span>
                </div>
              </div>
              
              <div className="capability">
                <label>Consciousness ({getConsciousnessLevel(selectedOrganism.consciousness)})</label>
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ 
                      width: `${selectedOrganism.consciousness * 100}%`,
                      backgroundColor: '#9C27B0'
                    }}
                  ></div>
                  <span>{(selectedOrganism.consciousness * 100).toFixed(1)}%</span>
                </div>
              </div>

              {selectedOrganism.complexity && (
                <div className="capability">
                  <label>Complexity</label>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill"
                      style={{ 
                        width: `${Math.min(selectedOrganism.complexity, 100)}%`,
                        backgroundColor: '#FF9800'
                      }}
                    ></div>
                    <span>{selectedOrganism.complexity.toFixed(1)}</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="detail-section">
            <h4>Traits</h4>
            <div className="traits-list">
              {selectedOrganism.traits.map(trait => (
                <span key={trait} className="trait-detail">
                  {trait.replace(/_/g, ' ')}
                </span>
              ))}
            </div>
          </div>

          <div className="detail-actions">
            <button 
              className="action-button primary"
              onClick={() => onTriggerMutation(selectedOrganism.id)}
            >
              🧬 Force Mutation
            </button>
            <button className="action-button secondary">
              📊 View Lineage
            </button>
            <button className="action-button secondary">
              🔬 Analyze Genes
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default OrganismView;