const WebSocket = require('ws');
const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

// Import modules
const EvolutionEngine = require('./evolution_engine');
const EventBus = require('./lib/event_bus');
const AgentManager = require('./lib/agent_manager');
const CloudProvisioner = require('./lib/cloud_provisioner');

class DNALangServer {
    constructor() {
        this.port = process.env.PORT || 8081;
        this.app = express();
        this.wss = null;
        this.eventBus = new EventBus();
        this.agentManager = new AgentManager(this.eventBus);
        this.evolutionEngine = new EvolutionEngine(this.eventBus);
        this.cloudProvisioner = new CloudProvisioner(this.eventBus);
        
        this.setupMiddleware();
        this.setupRoutes();
        this.setupEventHandlers();
    }

    setupMiddleware() {
        this.app.use(cors());
        this.app.use(express.json());
        this.app.use(express.static(path.join(__dirname, '../frontend/build')));
    }

    setupRoutes() {
        // Health check
        this.app.get('/health', (req, res) => {
            res.json({ 
                status: 'healthy', 
                timestamp: new Date().toISOString(),
                organisms: this.evolutionEngine.getOrganismCount(),
                agents: this.agentManager.getActiveAgentCount()
            });
        });

        // API endpoints
        this.app.get('/api/organisms', (req, res) => {
            res.json(this.evolutionEngine.getAllOrganisms());
        });

        this.app.get('/api/lineage/:organismId', (req, res) => {
            const lineage = this.evolutionEngine.getLineage(req.params.organismId);
            res.json(lineage);
        });

        this.app.get('/api/marketplace', (req, res) => {
            res.json(this.agentManager.getMarketplaceData());
        });

        this.app.post('/api/organisms/:id/mutate', (req, res) => {
            const result = this.evolutionEngine.triggerMutation(req.params.id);
            res.json(result);
        });

        // Serve React app for all other routes
        this.app.get('*', (req, res) => {
            res.sendFile(path.join(__dirname, '../frontend/build/index.html'));
        });
    }

    setupEventHandlers() {
        // Evolution events
        this.eventBus.on('organism:created', (data) => {
            this.broadcast('evolution', {
                type: 'organism_created',
                data
            });
        });

        this.eventBus.on('organism:mutated', (data) => {
            this.broadcast('evolution', {
                type: 'organism_mutated',
                data
            });
        });

        this.eventBus.on('organism:died', (data) => {
            this.broadcast('evolution', {
                type: 'organism_died',
                data
            });
        });

        // Agent events
        this.eventBus.on('agent:activated', (data) => {
            this.broadcast('agents', {
                type: 'agent_activated',
                data
            });
        });

        this.eventBus.on('marketplace:trade', (data) => {
            this.broadcast('marketplace', {
                type: 'gene_trade',
                data
            });
        });

        // Cloud events
        this.eventBus.on('cloud:provisioned', (data) => {
            this.broadcast('cloud', {
                type: 'resources_provisioned',
                data
            });
        });
    }

    setupWebSocket() {
        this.wss = new WebSocket.Server({ port: parseInt(this.port) + 1 });
        
        this.wss.on('connection', (ws) => {
            console.log('🔌 New WebSocket connection established');
            
            // Send initial state
            ws.send(JSON.stringify({
                type: 'init',
                data: {
                    organisms: this.evolutionEngine.getAllOrganisms(),
                    agents: this.agentManager.getActiveAgents(),
                    marketplace: this.agentManager.getMarketplaceData()
                }
            }));

            ws.on('message', (message) => {
                try {
                    const data = JSON.parse(message);
                    this.handleWebSocketMessage(ws, data);
                } catch (error) {
                    console.error('📢 WebSocket message error:', error);
                }
            });

            ws.on('close', () => {
                console.log('🔌 WebSocket connection closed');
            });
        });

        console.log(`🌐 WebSocket server running on port ${parseInt(this.port) + 1}`);
    }

    handleWebSocketMessage(ws, data) {
        switch (data.type) {
            case 'subscribe':
                // Handle subscription to specific events
                break;
            case 'trigger_mutation':
                this.evolutionEngine.triggerMutation(data.organismId);
                break;
            case 'activate_agent':
                this.agentManager.activateAgent(data.agentType);
                break;
            default:
                console.log('Unknown WebSocket message type:', data.type);
        }
    }

    broadcast(category, message) {
        if (this.wss) {
            const payload = JSON.stringify({
                category,
                timestamp: new Date().toISOString(),
                ...message
            });

            this.wss.clients.forEach((client) => {
                if (client.readyState === WebSocket.OPEN) {
                    client.send(payload);
                }
            });
        }
    }

    async start() {
        // Start the HTTP server
        this.server = this.app.listen(this.port, () => {
            console.log(`🚀 DNA-Lang Backend Server running on port ${this.port}`);
        });

        // Start WebSocket server
        this.setupWebSocket();

        // Initialize subsystems
        await this.agentManager.initialize();
        await this.evolutionEngine.start();
        await this.cloudProvisioner.initialize();

        console.log('🧬 DNA-Lang Live Digital Ecosystem is running!');
        console.log(`📊 Dashboard: http://localhost:${this.port}`);
        console.log(`🔗 WebSocket: ws://localhost:${parseInt(this.port) + 1}`);
    }

    async stop() {
        console.log('🛑 Shutting down DNA-Lang server...');
        
        if (this.wss) {
            this.wss.close();
        }
        
        if (this.server) {
            this.server.close();
        }

        await this.evolutionEngine.stop();
        await this.agentManager.shutdown();
        
        console.log('✅ Server shutdown complete');
    }
}

// Handle graceful shutdown
process.on('SIGINT', async () => {
    if (global.dnaLangServer) {
        await global.dnaLangServer.stop();
        process.exit(0);
    }
});

process.on('SIGTERM', async () => {
    if (global.dnaLangServer) {
        await global.dnaLangServer.stop();
        process.exit(0);
    }
});

// Start the server
if (require.main === module) {
    const server = new DNALangServer();
    global.dnaLangServer = server;
    server.start().catch(console.error);
}

module.exports = DNALangServer;