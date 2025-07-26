import React, { useState } from 'react';

interface Organism {
  id: string;
  type: string;
  generation: number;
  parentId?: string | null;
}

interface LineageViewProps {
  organisms: Organism[];
  selectedOrganism: Organism | null;
}

const LineageView: React.FC<LineageViewProps> = ({ organisms, selectedOrganism }) => {
  const [selectedLineage, setSelectedLineage] = useState<string | null>(null);

  const buildLineageTree = () => {
    const tree: { [key: string]: Organism[] } = {};
    const roots: Organism[] = [];

    // Group organisms by parent
    organisms.forEach(organism => {
      if (!organism.parentId) {
        roots.push(organism);
      } else {
        if (!tree[organism.parentId]) {
          tree[organism.parentId] = [];
        }
        tree[organism.parentId].push(organism);
      }
    });

    return { tree, roots };
  };

  const renderOrganismNode = (organism: Organism, depth: number = 0): React.ReactNode => {
    const { tree } = buildLineageTree();
    const children = tree[organism.id] || [];
    const hasChildren = children.length > 0;
    const isSelected = selectedOrganism?.id === organism.id;
    const isInSelectedLineage = selectedLineage === organism.id || 
      (selectedLineage && isDescendantOf(selectedLineage, organism.id));

    return (
      <div key={organism.id} className="lineage-node" style={{ marginLeft: `${depth * 20}px` }}>
        <div 
          className={`organism-node ${isSelected ? 'selected' : ''} ${isInSelectedLineage ? 'highlighted' : ''}`}
          onClick={() => setSelectedLineage(organism.id)}
        >
          <span className="node-icon">
            {hasChildren ? '👑' : '🧬'}
          </span>
          <div className="node-info">
            <div className="node-type">{organism.type}</div>
            <div className="node-details">
              Gen {organism.generation} • ID: {organism.id.slice(-6)}
            </div>
          </div>
          <div className="node-stats">
            <span className="children-count">
              {hasChildren ? `${children.length} offspring` : 'no offspring'}
            </span>
          </div>
        </div>
        
        {hasChildren && (
          <div className="children-container">
            {children
              .sort((a, b) => a.generation - b.generation)
              .map(child => renderOrganismNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  const isDescendantOf = (ancestorId: string, potentialDescendantId: string): boolean => {
    const organism = organisms.find(o => o.id === potentialDescendantId);
    if (!organism || !organism.parentId) return false;
    if (organism.parentId === ancestorId) return true;
    return isDescendantOf(ancestorId, organism.parentId);
  };

  const getLineageStats = (rootId: string) => {
    const descendants = organisms.filter(org => 
      org.id === rootId || isDescendantOf(rootId, org.id)
    );
    
    const generations = Math.max(...descendants.map(org => org.generation));
    const totalDescendants = descendants.length - 1; // Exclude the root itself
    
    return { generations, totalDescendants, descendants };
  };

  const { roots } = buildLineageTree();

  return (
    <div className="lineage-view">
      <div className="lineage-panel">
        <h2>Evolutionary Lineages</h2>
        
        <div className="lineage-controls">
          <button 
            className={selectedLineage === null ? 'active' : ''}
            onClick={() => setSelectedLineage(null)}
          >
            Show All
          </button>
          <button onClick={() => setSelectedLineage(selectedOrganism?.id || null)}>
            Focus Selected
          </button>
        </div>

        <div className="lineage-tree">
          {roots.length === 0 ? (
            <div className="empty-state">
              <p>No organisms available for lineage visualization</p>
            </div>
          ) : (
            roots
              .sort((a, b) => a.generation - b.generation)
              .map(root => renderOrganismNode(root))
          )}
        </div>
      </div>

      {selectedLineage && (
        <div className="lineage-details">
          <h3>Lineage Analysis</h3>
          <button 
            className="close-button"
            onClick={() => setSelectedLineage(null)}
          >
            ✕
          </button>
          
          {(() => {
            const stats = getLineageStats(selectedLineage);
            const rootOrganism = organisms.find(o => o.id === selectedLineage);
            
            return (
              <div>
                <div className="detail-section">
                  <h4>Lineage Statistics</h4>
                  <div className="stats-grid">
                    <div className="stat-item">
                      <span className="stat-label">Root Organism:</span>
                      <span className="stat-value">{rootOrganism?.type}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Total Descendants:</span>
                      <span className="stat-value">{stats.totalDescendants}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Generations:</span>
                      <span className="stat-value">{stats.generations}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Survival Rate:</span>
                      <span className="stat-value">
                        {stats.descendants.filter(o => o.id !== 'dead').length}/{stats.descendants.length} 
                        ({((stats.descendants.filter(o => o.id !== 'dead').length / stats.descendants.length) * 100).toFixed(1)}%)
                      </span>
                    </div>
                  </div>
                </div>

                <div className="detail-section">
                  <h4>Generation Breakdown</h4>
                  <div className="generation-chart">
                    {Array.from({ length: stats.generations }, (_, i) => i + 1).map(gen => {
                      const genOrganisms = stats.descendants.filter(o => o.generation === gen);
                      return (
                        <div key={gen} className="generation-bar">
                          <span className="gen-label">Gen {gen}</span>
                          <div className="gen-bar">
                            <div 
                              className="gen-fill"
                              style={{ width: `${(genOrganisms.length / stats.descendants.length) * 100}%` }}
                            ></div>
                          </div>
                          <span className="gen-count">{genOrganisms.length}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div className="detail-section">
                  <h4>Lineage Members</h4>
                  <div className="lineage-members">
                    {stats.descendants
                      .sort((a, b) => a.generation - b.generation)
                      .map(organism => (
                        <div key={organism.id} className="member-item">
                          <span className="member-gen">Gen {organism.generation}</span>
                          <span className="member-type">{organism.type}</span>
                          <span className="member-id">{organism.id.slice(-8)}</span>
                        </div>
                      ))}
                  </div>
                </div>
              </div>
            );
          })()}
        </div>
      )}
    </div>
  );
};

export default LineageView;