import React, { useMemo } from 'react';

interface Organism {
  id: string;
  type: string;
  fitness: number;
  consciousness: number;
  age: number;
  generation: number;
}

interface EvolutionEvent {
  type: string;
  data: any;
  timestamp: string;
}

interface MetricsViewProps {
  organisms: Organism[];
  events: EvolutionEvent[];
}

const MetricsView: React.FC<MetricsViewProps> = ({ organisms, events }) => {
  const metrics = useMemo(() => {
    // Population metrics
    const totalOrganisms = organisms.length;
    const averageFitness = organisms.length > 0 
      ? organisms.reduce((sum, org) => sum + org.fitness, 0) / organisms.length 
      : 0;
    const averageConsciousness = organisms.length > 0
      ? organisms.reduce((sum, org) => sum + org.consciousness, 0) / organisms.length
      : 0;
    const averageAge = organisms.length > 0
      ? organisms.reduce((sum, org) => sum + org.age, 0) / organisms.length
      : 0;

    // Type distribution
    const typeDistribution: { [key: string]: number } = {};
    organisms.forEach(org => {
      typeDistribution[org.type] = (typeDistribution[org.type] || 0) + 1;
    });

    // Generation distribution
    const generationDistribution: { [key: number]: number } = {};
    organisms.forEach(org => {
      generationDistribution[org.generation] = (generationDistribution[org.generation] || 0) + 1;
    });

    // Event metrics
    const eventCounts: { [key: string]: number } = {};
    events.forEach(event => {
      eventCounts[event.type] = (eventCounts[event.type] || 0) + 1;
    });

    // Evolution trends (last 20 events)
    const recentEvents = events.slice(-20);
    const mutationEvents = recentEvents.filter(e => e.type === 'organism_mutated');
    const creationEvents = recentEvents.filter(e => e.type === 'organism_created');
    const deathEvents = recentEvents.filter(e => e.type === 'organism_died');

    // Fitness distribution
    const fitnessRanges = {
      'High (80-100%)': organisms.filter(o => o.fitness >= 0.8).length,
      'Medium (60-80%)': organisms.filter(o => o.fitness >= 0.6 && o.fitness < 0.8).length,
      'Low (40-60%)': organisms.filter(o => o.fitness >= 0.4 && o.fitness < 0.6).length,
      'Critical (<40%)': organisms.filter(o => o.fitness < 0.4).length
    };

    // Consciousness distribution
    const consciousnessRanges = {
      'Transcendent (90-100%)': organisms.filter(o => o.consciousness >= 0.9).length,
      'High (70-90%)': organisms.filter(o => o.consciousness >= 0.7 && o.consciousness < 0.9).length,
      'Medium (40-70%)': organisms.filter(o => o.consciousness >= 0.4 && o.consciousness < 0.7).length,
      'Basic (<40%)': organisms.filter(o => o.consciousness < 0.4).length
    };

    return {
      totalOrganisms,
      averageFitness,
      averageConsciousness,
      averageAge,
      typeDistribution,
      generationDistribution,
      eventCounts,
      mutationEvents: mutationEvents.length,
      creationEvents: creationEvents.length,
      deathEvents: deathEvents.length,
      fitnessRanges,
      consciousnessRanges
    };
  }, [organisms, events]);

  const renderDistributionChart = (data: { [key: string]: number }, title: string) => {
    const total = Object.values(data).reduce((sum, count) => sum + count, 0);
    if (total === 0) return null;

    return (
      <div className="distribution-chart">
        <h4>{title}</h4>
        <div className="chart-bars">
          {Object.entries(data).map(([key, count]) => (
            <div key={key} className="chart-bar">
              <div className="bar-label">{key}</div>
              <div className="bar-container">
                <div 
                  className="bar-fill"
                  style={{ width: `${(count / total) * 100}%` }}
                ></div>
                <span className="bar-value">{count}</span>
              </div>
              <div className="bar-percentage">
                {((count / total) * 100).toFixed(1)}%
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const getHealthColor = (value: number) => {
    if (value >= 0.8) return '#4CAF50';
    if (value >= 0.6) return '#FF9800';
    if (value >= 0.4) return '#FF5722';
    return '#F44336';
  };

  const formatPercentage = (value: number) => `${(value * 100).toFixed(1)}%`;

  return (
    <div className="metrics-view">
      <h2>Ecosystem Metrics</h2>
      
      <div className="metrics-grid">
        {/* Key Performance Indicators */}
        <div className="metrics-section">
          <h3>Key Performance Indicators</h3>
          <div className="kpi-cards">
            <div className="kpi-card">
              <div className="kpi-value">{metrics.totalOrganisms}</div>
              <div className="kpi-label">Total Organisms</div>
            </div>
            <div className="kpi-card">
              <div 
                className="kpi-value"
                style={{ color: getHealthColor(metrics.averageFitness) }}
              >
                {formatPercentage(metrics.averageFitness)}
              </div>
              <div className="kpi-label">Average Fitness</div>
            </div>
            <div className="kpi-card">
              <div 
                className="kpi-value"
                style={{ color: '#9C27B0' }}
              >
                {formatPercentage(metrics.averageConsciousness)}
              </div>
              <div className="kpi-label">Average Consciousness</div>
            </div>
            <div className="kpi-card">
              <div className="kpi-value">{metrics.averageAge.toFixed(1)}</div>
              <div className="kpi-label">Average Age</div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="metrics-section">
          <h3>Recent Activity (Last 20 Events)</h3>
          <div className="activity-stats">
            <div className="activity-item">
              <span className="activity-icon">🧬</span>
              <span className="activity-label">Mutations:</span>
              <span className="activity-value">{metrics.mutationEvents}</span>
            </div>
            <div className="activity-item">
              <span className="activity-icon">👶</span>
              <span className="activity-label">Births:</span>
              <span className="activity-value">{metrics.creationEvents}</span>
            </div>
            <div className="activity-item">
              <span className="activity-icon">💀</span>
              <span className="activity-label">Deaths:</span>
              <span className="activity-value">{metrics.deathEvents}</span>
            </div>
          </div>
        </div>

        {/* Organism Types */}
        <div className="metrics-section">
          {renderDistributionChart(metrics.typeDistribution, 'Organism Types')}
        </div>

        {/* Generation Distribution */}
        <div className="metrics-section">
          {renderDistributionChart(metrics.generationDistribution, 'Generation Distribution')}
        </div>

        {/* Fitness Distribution */}
        <div className="metrics-section">
          {renderDistributionChart(metrics.fitnessRanges, 'Fitness Distribution')}
        </div>

        {/* Consciousness Distribution */}
        <div className="metrics-section">
          {renderDistributionChart(metrics.consciousnessRanges, 'Consciousness Distribution')}
        </div>

        {/* Event Timeline */}
        <div className="metrics-section full-width">
          <h3>Recent Events Timeline</h3>
          <div className="events-timeline">
            {events.slice(-10).reverse().map((event, index) => (
              <div key={index} className="timeline-event">
                <div className="event-timestamp">
                  {new Date(event.timestamp).toLocaleTimeString()}
                </div>
                <div className="event-content">
                  <div className="event-type-badge">
                    {event.type.replace(/_/g, ' ')}
                  </div>
                  <div className="event-details">
                    {event.type === 'organism_created' && `New ${event.data.type} organism`}
                    {event.type === 'organism_mutated' && `Organism mutated (fitness: ${formatPercentage(event.data.newFitness || 0)})`}
                    {event.type === 'organism_died' && `Organism died (cause: ${event.data.cause})`}
                    {event.type === 'evolution:cycle_complete' && `Evolution cycle ${event.data.generation} completed`}
                    {event.type === 'agent:activated' && `${event.data.agentName} agent activated`}
                    {!['organism_created', 'organism_mutated', 'organism_died', 'evolution:cycle_complete', 'agent:activated'].includes(event.type) && 
                      JSON.stringify(event.data)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* System Health */}
        <div className="metrics-section">
          <h3>Ecosystem Health</h3>
          <div className="health-indicators">
            <div className="health-item">
              <div className="health-label">Population Stability</div>
              <div className="health-bar">
                <div 
                  className="health-fill"
                  style={{ 
                    width: `${Math.min((metrics.totalOrganisms / 10) * 100, 100)}%`,
                    backgroundColor: metrics.totalOrganisms > 5 ? '#4CAF50' : '#FF5722'
                  }}
                ></div>
              </div>
              <div className="health-status">
                {metrics.totalOrganisms > 5 ? 'Stable' : 'At Risk'}
              </div>
            </div>

            <div className="health-item">
              <div className="health-label">Average Fitness</div>
              <div className="health-bar">
                <div 
                  className="health-fill"
                  style={{ 
                    width: `${metrics.averageFitness * 100}%`,
                    backgroundColor: getHealthColor(metrics.averageFitness)
                  }}
                ></div>
              </div>
              <div className="health-status">
                {metrics.averageFitness > 0.7 ? 'Excellent' : 
                 metrics.averageFitness > 0.5 ? 'Good' : 'Poor'}
              </div>
            </div>

            <div className="health-item">
              <div className="health-label">Consciousness Level</div>
              <div className="health-bar">
                <div 
                  className="health-fill"
                  style={{ 
                    width: `${metrics.averageConsciousness * 100}%`,
                    backgroundColor: '#9C27B0'
                  }}
                ></div>
              </div>
              <div className="health-status">
                {metrics.averageConsciousness > 0.7 ? 'Transcendent' :
                 metrics.averageConsciousness > 0.4 ? 'Conscious' : 'Basic'}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetricsView;