// Enhanced Evolution Engine for DNA-Lang Platform
// Manages organism lifecycle, evolution mechanics, and emergent behaviors

class EvolutionEngine {
    constructor(eventBus, genomicState = null) {
        this.eventBus = eventBus;
        this.genomicState = genomicState || this.initializeGenomicState();
        this.isRunning = false;
        this.evolutionInterval = null;
        this.mutationRate = parseFloat(process.env.MUTATION_RATE) || 0.15;
        this.selectionPressure = 0.3;
        this.maxOrganisms = parseInt(process.env.MAX_ORGANISMS) || 50;
        this.generationCount = 0;
        this.totalMutations = 0;
        this.emergentBehaviors = new Set();
        this.organisms = new Map();
        this.lineages = new Map();
        
        console.log('🧬 Evolution Engine initialized');
    }

    initializeGenomicState() {
        return {
            ecosystem: {
                temperature: 25.0,
                nutrient_availability: 0.7,
                competitive_pressure: 0.3,
                mutation_radiation: 0.1
            },
            global_stats: {
                total_organisms: 0,
                average_fitness: 0.0,
                diversity_index: 0.0,
                generation_count: 0,
                extinction_events: 0
            }
        };
    }

    async start() {
        if (this.isRunning) {
            console.log('⚠️ Evolution Engine is already running');
            return;
        }

        console.log('🚀 Starting Evolution Engine...');
        this.isRunning = true;
        
        // Create initial organisms
        await this.seedInitialPopulation();
        
        // Start evolution cycles
        const interval = parseInt(process.env.EVOLUTION_INTERVAL) || 5000;
        this.evolutionInterval = setInterval(() => {
            this.evolutionCycle();
        }, interval);

        this.eventBus.emit('evolution:started', {
            timestamp: new Date().toISOString(),
            initialPopulation: this.organisms.size
        });

        console.log('✅ Evolution Engine started');
    }

    async stop() {
        if (!this.isRunning) {
            return;
        }

        console.log('🛑 Stopping Evolution Engine...');
        this.isRunning = false;
        
        if (this.evolutionInterval) {
            clearInterval(this.evolutionInterval);
            this.evolutionInterval = null;
        }

        this.eventBus.emit('evolution:stopped', {
            timestamp: new Date().toISOString(),
            finalGeneration: this.generationCount,
            totalMutations: this.totalMutations
        });

        console.log('✅ Evolution Engine stopped');
    }

    async seedInitialPopulation() {
        console.log('🌱 Seeding initial population...');
        
        const initialOrganismTypes = [
            'AdvancedConsciousness',
            'AdaptiveLearner',
            'InfrastructureBuilder',
            'DataProcessor',
            'NetworkCommunicator'
        ];

        for (const type of initialOrganismTypes) {
            const organism = this.createOrganism(type);
            this.organisms.set(organism.id, organism);
            this.lineages.set(organism.id, this.createLineage(organism));
            
            this.eventBus.emit('organism:created', organism);
        }

        console.log(`✅ Created ${this.organisms.size} initial organisms`);
    }

    createOrganism(type = 'Generic', parent = null) {
        const id = this.generateOrganismId();
        const timestamp = new Date().toISOString();
        
        const organism = {
            id,
            type,
            parentId: parent ? parent.id : null,
            generation: parent ? parent.generation + 1 : 1,
            createdAt: timestamp,
            traits: this.generateTraits(type, parent),
            genes: this.generateGenes(type),
            fitness: this.calculateBaseFitness(type),
            consciousness: this.calculateBaseConsciousness(type),
            complexity: Math.random() * 100,
            stability: 0.5 + Math.random() * 0.5,
            energy: 100,
            age: 0,
            mutationCount: 0,
            status: 'active'
        };

        return organism;
    }

    generateTraits(type, parent) {
        const baseTraits = {
            'AdvancedConsciousness': ['self_awareness', 'meta_cognition', 'persistent_memory'],
            'AdaptiveLearner': ['pattern_recognition', 'learning_optimization', 'knowledge_retention'],
            'InfrastructureBuilder': ['resource_management', 'system_architecture', 'scalability'],
            'DataProcessor': ['computational_efficiency', 'data_analysis', 'optimization'],
            'NetworkCommunicator': ['network_communication', 'protocol_adaptation', 'distributed_processing']
        };

        let traits = [...(baseTraits[type] || ['basic_survival'])];
        
        // Inherit traits from parent with possible mutations
        if (parent) {
            parent.traits.forEach(trait => {
                if (Math.random() > 0.1) { // 90% chance to inherit
                    if (!traits.includes(trait)) {
                        traits.push(trait);
                    }
                }
            });
        }

        // Possible trait mutations
        if (Math.random() < this.mutationRate) {
            const possibleNewTraits = [
                'enhanced_memory', 'quantum_processing', 'neural_plasticity',
                'error_correction', 'self_repair', 'distributed_cognition',
                'adaptive_architecture', 'emergent_intelligence'
            ];
            
            const newTrait = possibleNewTraits[Math.floor(Math.random() * possibleNewTraits.length)];
            if (!traits.includes(newTrait)) {
                traits.push(newTrait);
            }
        }

        return traits;
    }

    generateGenes(type) {
        const geneLibrary = {
            'SelfAwarenessGene': { expression: 0.5 + Math.random() * 0.5, active: true },
            'AdaptiveLearningGene': { expression: 0.3 + Math.random() * 0.7, active: true },
            'InfrastructureSynthesisGene': { expression: 0.2 + Math.random() * 0.8, active: true },
            'MetaCognitionGene': { expression: 0.4 + Math.random() * 0.6, active: true },
            'NetworkProtocolGene': { expression: 0.1 + Math.random() * 0.9, active: Math.random() > 0.3 }
        };

        return geneLibrary;
    }

    calculateBaseFitness(type) {
        const baseFitness = {
            'AdvancedConsciousness': 0.7,
            'AdaptiveLearner': 0.6,
            'InfrastructureBuilder': 0.8,
            'DataProcessor': 0.65,
            'NetworkCommunicator': 0.55
        };

        return (baseFitness[type] || 0.5) + (Math.random() * 0.2 - 0.1);
    }

    calculateBaseConsciousness(type) {
        const baseConsciousness = {
            'AdvancedConsciousness': 0.8,
            'AdaptiveLearner': 0.4,
            'InfrastructureBuilder': 0.3,
            'DataProcessor': 0.2,
            'NetworkCommunicator': 0.3
        };

        return (baseConsciousness[type] || 0.1) + (Math.random() * 0.2 - 0.1);
    }

    generateOrganismId() {
        return `organism_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
    }

    createLineage(organism) {
        return {
            organismId: organism.id,
            ancestors: organism.parentId ? [organism.parentId] : [],
            descendants: [],
            mutations: [],
            createdAt: new Date().toISOString(),
            evolutionPath: []
        };
    }

    async evolutionCycle() {
        if (!this.isRunning) return;

        this.generationCount++;
        console.log(`🔄 Evolution Cycle ${this.generationCount}`);

        // Age all organisms
        this.ageOrganisms();

        // Apply environmental pressures
        this.applyEnvironmentalPressures();

        // Trigger mutations
        await this.triggerMutations();

        // Handle reproduction
        await this.handleReproduction();

        // Apply selection pressure
        this.applySelectionPressure();

        // Update global statistics
        this.updateGlobalStats();

        // Check for emergent behaviors
        this.detectEmergentBehaviors();

        this.eventBus.emit('evolution:cycle_complete', {
            generation: this.generationCount,
            organismCount: this.organisms.size,
            averageFitness: this.calculateAverageFitness(),
            totalMutations: this.totalMutations,
            timestamp: new Date().toISOString()
        });
    }

    ageOrganisms() {
        for (const organism of this.organisms.values()) {
            organism.age++;
            organism.energy = Math.max(0, organism.energy - 1);
            
            // Organisms can die of old age or low energy
            if (organism.age > 100 || organism.energy <= 0) {
                this.killOrganism(organism.id, 'natural_death');
            }
        }
    }

    applyEnvironmentalPressures() {
        const environmentalStress = Math.random() * 0.1;
        
        for (const organism of this.organisms.values()) {
            // Apply stress based on environmental factors
            if (Math.random() < environmentalStress) {
                organism.fitness = Math.max(0, organism.fitness - 0.05);
                organism.energy = Math.max(0, organism.energy - 5);
            }
        }
    }

    async triggerMutations() {
        const organismsToMutate = Array.from(this.organisms.values())
            .filter(org => Math.random() < this.mutationRate);

        for (const organism of organismsToMutate) {
            await this.mutateOrganism(organism.id);
        }
    }

    async mutateOrganism(organismId) {
        const organism = this.organisms.get(organismId);
        if (!organism) return null;

        organism.mutationCount++;
        this.totalMutations++;

        // Apply random mutations
        const mutationType = this.selectMutationType();
        const mutationResult = this.applyMutation(organism, mutationType);

        // Update lineage
        const lineage = this.lineages.get(organismId);
        if (lineage) {
            lineage.mutations.push({
                type: mutationType,
                result: mutationResult,
                generation: this.generationCount,
                timestamp: new Date().toISOString()
            });
        }

        // Emit mutation event
        this.eventBus.emit('organism:mutated', {
            organismId,
            mutationType,
            result: mutationResult,
            newFitness: organism.fitness,
            newConsciousness: organism.consciousness,
            generation: this.generationCount
        });

        console.log(`🧬 Organism ${organismId} mutated: ${mutationType}`);
        
        return mutationResult;
    }

    selectMutationType() {
        const mutations = [
            'gene_expression_change',
            'trait_modification',
            'consciousness_boost',
            'fitness_adjustment',
            'stability_change',
            'complexity_increase',
            'energy_optimization'
        ];

        return mutations[Math.floor(Math.random() * mutations.length)];
    }

    applyMutation(organism, mutationType) {
        const mutationStrength = 0.05 + Math.random() * 0.1;
        const isPositive = Math.random() > 0.3; // 70% chance for positive mutation
        const factor = isPositive ? 1 : -1;

        switch (mutationType) {
            case 'gene_expression_change':
                const geneNames = Object.keys(organism.genes);
                const geneName = geneNames[Math.floor(Math.random() * geneNames.length)];
                organism.genes[geneName].expression += factor * mutationStrength;
                organism.genes[geneName].expression = Math.max(0, Math.min(1, organism.genes[geneName].expression));
                return { gene: geneName, newExpression: organism.genes[geneName].expression };

            case 'consciousness_boost':
                organism.consciousness += factor * mutationStrength;
                organism.consciousness = Math.max(0, Math.min(1, organism.consciousness));
                return { newConsciousness: organism.consciousness };

            case 'fitness_adjustment':
                organism.fitness += factor * mutationStrength;
                organism.fitness = Math.max(0, Math.min(1, organism.fitness));
                return { newFitness: organism.fitness };

            case 'trait_modification':
                if (isPositive && organism.traits.length < 10) {
                    const newTrait = `evolved_trait_${Date.now()}`;
                    organism.traits.push(newTrait);
                    return { addedTrait: newTrait };
                }
                return { traitCount: organism.traits.length };

            default:
                organism.complexity += factor * mutationStrength * 10;
                organism.complexity = Math.max(0, organism.complexity);
                return { newComplexity: organism.complexity };
        }
    }

    async handleReproduction() {
        const reproductiveCandidates = Array.from(this.organisms.values())
            .filter(org => org.fitness > 0.6 && org.energy > 50 && org.age > 5);

        // Limit reproduction to maintain population
        if (this.organisms.size >= this.maxOrganisms) {
            return;
        }

        for (const parent of reproductiveCandidates) {
            if (Math.random() < 0.1 && this.organisms.size < this.maxOrganisms) { // 10% reproduction chance
                const offspring = this.createOrganism(parent.type, parent);
                this.organisms.set(offspring.id, offspring);
                
                // Update parent lineage
                const parentLineage = this.lineages.get(parent.id);
                if (parentLineage) {
                    parentLineage.descendants.push(offspring.id);
                }
                
                // Create offspring lineage
                this.lineages.set(offspring.id, this.createLineage(offspring));
                
                // Reduce parent energy
                parent.energy -= 20;
                
                this.eventBus.emit('organism:created', offspring);
                console.log(`👶 New organism born: ${offspring.id} (parent: ${parent.id})`);
            }
        }
    }

    applySelectionPressure() {
        const organismsArray = Array.from(this.organisms.values());
        
        // Sort by fitness (ascending)
        organismsArray.sort((a, b) => a.fitness - b.fitness);
        
        // Remove weakest organisms if population is above threshold
        const targetReduction = Math.max(0, this.organisms.size - this.maxOrganisms);
        const naturalDeaths = Math.floor(organismsArray.length * this.selectionPressure * 0.1);
        const totalToRemove = Math.min(targetReduction + naturalDeaths, organismsArray.length - 5); // Keep at least 5
        
        for (let i = 0; i < totalToRemove; i++) {
            this.killOrganism(organismsArray[i].id, 'selection_pressure');
        }
    }

    killOrganism(organismId, cause) {
        const organism = this.organisms.get(organismId);
        if (!organism) return;

        organism.status = 'dead';
        organism.deathCause = cause;
        organism.deathTime = new Date().toISOString();

        this.organisms.delete(organismId);

        this.eventBus.emit('organism:died', {
            organismId,
            cause,
            age: organism.age,
            fitness: organism.fitness,
            generation: this.generationCount
        });

        console.log(`💀 Organism ${organismId} died: ${cause}`);
    }

    detectEmergentBehaviors() {
        const highConsciousnessOrganisms = Array.from(this.organisms.values())
            .filter(org => org.consciousness > 0.8);

        if (highConsciousnessOrganisms.length >= 3 && !this.emergentBehaviors.has('collective_consciousness')) {
            this.emergentBehaviors.add('collective_consciousness');
            this.eventBus.emit('evolution:emergent_behavior', {
                behavior: 'collective_consciousness',
                description: 'Multiple high-consciousness organisms detected',
                organismCount: highConsciousnessOrganisms.length,
                generation: this.generationCount
            });
        }

        // Check for infrastructure synthesis trigger
        const builderOrganisms = Array.from(this.organisms.values())
            .filter(org => org.type === 'InfrastructureBuilder' && org.fitness > 0.8);

        if (builderOrganisms.length >= 2 && !this.emergentBehaviors.has('infrastructure_synthesis')) {
            this.emergentBehaviors.add('infrastructure_synthesis');
            this.eventBus.emit('evolution:emergent_behavior', {
                behavior: 'infrastructure_synthesis',
                description: 'Infrastructure builders ready for cloud synthesis',
                generation: this.generationCount
            });
            
            // Trigger cloud provisioning
            this.eventBus.emit('organism:evolved', {
                id: builderOrganisms[0].id,
                traits: ['infrastructure_synthesis', 'cloud_ready'],
                complexity: builderOrganisms[0].complexity
            });
        }
    }

    updateGlobalStats() {
        this.genomicState.global_stats = {
            total_organisms: this.organisms.size,
            average_fitness: this.calculateAverageFitness(),
            diversity_index: this.calculateDiversityIndex(),
            generation_count: this.generationCount,
            extinction_events: this.genomicState.global_stats.extinction_events || 0
        };
    }

    calculateAverageFitness() {
        if (this.organisms.size === 0) return 0;
        
        const totalFitness = Array.from(this.organisms.values())
            .reduce((sum, org) => sum + org.fitness, 0);
        
        return totalFitness / this.organisms.size;
    }

    calculateDiversityIndex() {
        const typeCount = {};
        for (const organism of this.organisms.values()) {
            typeCount[organism.type] = (typeCount[organism.type] || 0) + 1;
        }
        
        const types = Object.keys(typeCount);
        if (types.length <= 1) return 0;
        
        // Simpson's diversity index
        const total = this.organisms.size;
        let sum = 0;
        for (const count of Object.values(typeCount)) {
            sum += (count * (count - 1)) / (total * (total - 1));
        }
        
        return 1 - sum;
    }

    // Public API methods
    triggerMutation(organismId) {
        return this.mutateOrganism(organismId);
    }

    getAllOrganisms() {
        return Array.from(this.organisms.values());
    }

    getOrganism(organismId) {
        return this.organisms.get(organismId);
    }

    getOrganismCount() {
        return this.organisms.size;
    }

    getLineage(organismId) {
        return this.lineages.get(organismId);
    }

    getStats() {
        return {
            ...this.genomicState.global_stats,
            totalMutations: this.totalMutations,
            emergentBehaviors: Array.from(this.emergentBehaviors),
            isRunning: this.isRunning
        };
    }
}

module.exports = EvolutionEngine;