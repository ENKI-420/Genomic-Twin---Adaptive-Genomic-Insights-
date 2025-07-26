import React, { useState, useEffect } from 'react';
import './App.css';
import LineageView from './components/LineageView';
import MarketplaceView from './components/MarketplaceView';
import OrganismView from './components/OrganismView';
import MetricsView from './components/MetricsView';
import WebSocketService from './services/WebSocketService';

interface Organism {
  id: string;
  type: string;
  fitness: number;
  consciousness: number;
  age: number;
  status: string;
  traits: string[];
  generation: number;
}

interface MarketplaceData {
  genes: Array<{
    id: string;
    name: string;
    description: string;
    price: number;
    seller: string;
    timestamp: string;
  }>;
  trades: any[];
  activeOffers: any[];
}

interface EvolutionEvent {
  type: string;
  data: any;
  timestamp: string;
}

function App() {
  const [organisms, setOrganisms] = useState<Organism[]>([]);
  const [selectedOrganism, setSelectedOrganism] = useState<Organism | null>(null);
  const [marketplaceData, setMarketplaceData] = useState<MarketplaceData>({
    genes: [],
    trades: [],
    activeOffers: []
  });
  const [events, setEvents] = useState<EvolutionEvent[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');
  const [currentView, setCurrentView] = useState<'organisms' | 'lineage' | 'marketplace' | 'metrics'>('organisms');

  useEffect(() => {
    const wsService = new WebSocketService();
    
    wsService.onConnect = () => {
      setConnectionStatus('connected');
    };
    
    wsService.onDisconnect = () => {
      setConnectionStatus('disconnected');
    };
    
    wsService.onMessage = (message) => {
      handleWebSocketMessage(message);
    };
    
    wsService.connect();
    
    return () => {
      wsService.disconnect();
    };
  }, []);

  const handleWebSocketMessage = (message: any) => {
    const event: EvolutionEvent = {
      type: message.type,
      data: message.data,
      timestamp: message.timestamp || new Date().toISOString()
    };
    
    setEvents(prev => [...prev.slice(-99), event]); // Keep last 100 events
    
    switch (message.category) {
      case 'evolution':
        handleEvolutionEvent(message);
        break;
      case 'marketplace':
        handleMarketplaceEvent(message);
        break;
      case 'agents':
        handleAgentEvent(message);
        break;
      default:
        if (message.type === 'init') {
          if (message.data.organisms) {
            setOrganisms(message.data.organisms);
          }
          if (message.data.marketplace) {
            setMarketplaceData(message.data.marketplace);
          }
        }
    }
  };

  const handleEvolutionEvent = (message: any) => {
    switch (message.type) {
      case 'organism_created':
        setOrganisms(prev => [...prev, message.data]);
        break;
      case 'organism_mutated':
        setOrganisms(prev => 
          prev.map(org => 
            org.id === message.data.organismId 
              ? { ...org, fitness: message.data.newFitness, consciousness: message.data.newConsciousness }
              : org
          )
        );
        break;
      case 'organism_died':
        setOrganisms(prev => prev.filter(org => org.id !== message.data.organismId));
        if (selectedOrganism && selectedOrganism.id === message.data.organismId) {
          setSelectedOrganism(null);
        }
        break;
    }
  };

  const handleMarketplaceEvent = (message: any) => {
    if (message.type === 'gene_trade') {
      setMarketplaceData(prev => ({
        ...prev,
        trades: [...prev.trades, message.data]
      }));
    }
  };

  const handleAgentEvent = (message: any) => {
    // Handle agent-related events
    console.log('Agent event:', message);
  };

  const triggerMutation = (organismId: string) => {
    const wsService = WebSocketService.getInstance();
    if (wsService) {
      wsService.send({
        type: 'trigger_mutation',
        organismId
      });
    }
  };

  const activateAgent = (agentType: string) => {
    const wsService = WebSocketService.getInstance();
    if (wsService) {
      wsService.send({
        type: 'activate_agent',
        agentType
      });
    }
  };

  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return '#4CAF50';
      case 'connecting': return '#FF9800';
      case 'disconnected': return '#F44336';
      default: return '#757575';
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🧬 DNA-Lang Live Digital Ecosystem</h1>
        <div className="connection-status">
          <span 
            className="status-indicator" 
            style={{ backgroundColor: getStatusColor() }}
          ></span>
          <span>{connectionStatus}</span>
        </div>
        <nav className="main-nav">
          <button 
            className={currentView === 'organisms' ? 'active' : ''}
            onClick={() => setCurrentView('organisms')}
          >
            Organisms ({organisms.length})
          </button>
          <button 
            className={currentView === 'lineage' ? 'active' : ''}
            onClick={() => setCurrentView('lineage')}
          >
            Lineage
          </button>
          <button 
            className={currentView === 'marketplace' ? 'active' : ''}
            onClick={() => setCurrentView('marketplace')}
          >
            Marketplace
          </button>
          <button 
            className={currentView === 'metrics' ? 'active' : ''}
            onClick={() => setCurrentView('metrics')}
          >
            Metrics
          </button>
        </nav>
      </header>

      <main className="App-main">
        {currentView === 'organisms' && (
          <OrganismView
            organisms={organisms}
            selectedOrganism={selectedOrganism}
            onSelectOrganism={setSelectedOrganism}
            onTriggerMutation={triggerMutation}
          />
        )}
        
        {currentView === 'lineage' && (
          <LineageView 
            organisms={organisms}
            selectedOrganism={selectedOrganism}
          />
        )}
        
        {currentView === 'marketplace' && (
          <MarketplaceView 
            marketplaceData={marketplaceData}
            onActivateAgent={activateAgent}
          />
        )}
        
        {currentView === 'metrics' && (
          <MetricsView 
            organisms={organisms}
            events={events}
          />
        )}
      </main>

      <aside className="events-panel">
        <h3>Live Events</h3>
        <div className="events-list">
          {events.slice(-10).reverse().map((event, index) => (
            <div key={index} className="event-item">
              <div className="event-time">
                {new Date(event.timestamp).toLocaleTimeString()}
              </div>
              <div className="event-type">{event.type}</div>
              <div className="event-data">
                {JSON.stringify(event.data, null, 2)}
              </div>
            </div>
          ))}
        </div>
      </aside>
    </div>
  );
}

export default App;
