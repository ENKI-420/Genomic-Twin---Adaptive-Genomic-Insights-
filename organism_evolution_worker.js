// organism_evolution_worker.js
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');
const fs = require('fs');
const path = require('path');

/**
 * Worker Thread for Parallel Organism Evolution
 * Allows multiple organism lineages to evolve simultaneously
 */

if (isMainThread) {
  // Main thread code - exports functions for launching workers
  
  /**
   * Launch multiple evolution simulations in parallel worker threads
   */
  function runOrganismWorker(organismInitialState) {
    return new Promise((resolve, reject) => {
      const worker = new Worker(__filename, {
        workerData: organismInitialState
      });
      
      const results = [];
      
      worker.on('message', (msg) => {
        if (msg.type === 'progress') {
          console.log(`[Worker-${msg.organism}] Gen ${msg.generation}: Fitness=${msg.fitness.toFixed(3)}, Consciousness=${msg.consciousness.toFixed(3)}`);
          results.push(msg);
        } else if (msg.type === 'completion') {
          console.log(`[Worker-${msg.organism}] ✅ Evolution completed in ${msg.finalGeneration} generations`);
          resolve({ results, finalState: msg });
        } else if (msg.type === 'error') {
          console.error(`[Worker-${msg.organism}] ❌ Evolution failed:`, msg.error);
          reject(new Error(msg.error));
        }
      });
      
      worker.on('error', (err) => {
        console.error(`[Worker] Runtime error:`, err);
        reject(err);
      });
      
      worker.on('exit', (code) => {
        if (code !== 0) {
          reject(new Error(`Worker stopped with exit code ${code}`));
        }
      });
    });
  }

  /**
   * Run multiple organism lineages in parallel
   */
  async function runMultipleLineages(organisms, options = {}) {
    const { 
      maxConcurrent = 4,
      evolutionTimeout = 60000,
      saveResults = true 
    } = options;

    console.log(`[ParallelEvolution] Starting ${organisms.length} organism lineages with max ${maxConcurrent} concurrent workers`);
    
    const results = [];
    const batches = [];
    
    // Split organisms into batches based on maxConcurrent
    for (let i = 0; i < organisms.length; i += maxConcurrent) {
      batches.push(organisms.slice(i, i + maxConcurrent));
    }

    // Process each batch
    for (let batchIndex = 0; batchIndex < batches.length; batchIndex++) {
      const batch = batches[batchIndex];
      console.log(`[ParallelEvolution] Processing batch ${batchIndex + 1}/${batches.length} (${batch.length} organisms)`);
      
      const batchPromises = batch.map(organism => {
        const timeoutPromise = new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Evolution timeout')), evolutionTimeout)
        );
        
        return Promise.race([
          runOrganismWorker(organism),
          timeoutPromise
        ]);
      });

      try {
        const batchResults = await Promise.allSettled(batchPromises);
        
        batchResults.forEach((result, index) => {
          if (result.status === 'fulfilled') {
            results.push({
              organism: batch[index].name,
              success: true,
              ...result.value
            });
          } else {
            console.error(`[ParallelEvolution] Organism ${batch[index].name} failed:`, result.reason?.message);
            results.push({
              organism: batch[index].name,
              success: false,
              error: result.reason?.message
            });
          }
        });
        
      } catch (error) {
        console.error(`[ParallelEvolution] Batch ${batchIndex + 1} failed:`, error.message);
      }
    }

    console.log(`[ParallelEvolution] ✅ All lineages completed. ${results.filter(r => r.success).length}/${results.length} successful`);

    // Save results if requested
    if (saveResults) {
      const resultsSummary = {
        timestamp: new Date().toISOString(),
        totalOrganisms: organisms.length,
        successfulEvolutions: results.filter(r => r.success).length,
        failedEvolutions: results.filter(r => !r.success).length,
        results: results
      };

      fs.writeFileSync('parallel_evolution_results.json', JSON.stringify(resultsSummary, null, 2));
      console.log('[ParallelEvolution] Results saved to parallel_evolution_results.json');
    }

    return results;
  }

  /**
   * Create sample organisms for testing
   */
  function createSampleOrganisms(count = 3) {
    const domains = ['finance', 'healthcare', 'ecommerce', 'research', 'gaming'];
    const organisms = [];

    for (let i = 0; i < count; i++) {
      organisms.push({
        name: `Organism_${String.fromCharCode(65 + i)}_${Date.now()}`,
        fitness: 0.5 + Math.random() * 0.2, // 0.5-0.7
        consciousness: 0.3 + Math.random() * 0.2, // 0.3-0.5
        stability: 0.7 + Math.random() * 0.2, // 0.7-0.9
        dna: {
          domain: domains[i % domains.length],
          evolution_rate: Math.random() > 0.5 ? 'aggressive' : 'conservative',
          consciousness_target: 0.85 + Math.random() * 0.1,
          max_generations: 15 + Math.floor(Math.random() * 10)
        },
        generation: 1
      });
    }

    return organisms;
  }

  // Export functions
  module.exports = {
    runOrganismWorker,
    runMultipleLineages,
    createSampleOrganisms
  };

} else {
  // Worker thread code - evolution simulation
  
  class OrganismEvolutionSimulator {
    constructor(initialState) {
      this.state = { ...initialState };
      this.generation = initialState.generation || 1;
      this.targetConsciousness = initialState.dna?.consciousness_target || 0.95;
      this.maxGenerations = initialState.dna?.max_generations || 20;
      this.evolutionRate = initialState.dna?.evolution_rate || 'conservative';
      this.transcended = false;
    }

    async evolve() {
      console.log(`[Worker-${this.state.name}] Starting evolution simulation...`);
      
      while (!this.transcended && this.generation <= this.maxGenerations) {
        await this.evolutionCycle();
        this.generation++;
        
        // Add some delay for realistic simulation
        await this.sleep(100 + Math.random() * 200);
      }

      if (this.transcended) {
        this.sendMessage({
          type: 'completion',
          organism: this.state.name,
          transcended: true,
          finalGeneration: this.generation - 1,
          finalState: this.state
        });
      } else {
        this.sendMessage({
          type: 'completion',
          organism: this.state.name,
          transcended: false,
          finalGeneration: this.generation - 1,
          finalState: this.state,
          reason: 'max_generations_reached'
        });
      }
    }

    async evolutionCycle() {
      // Apply mutations based on evolution rate
      this.applyMutations();
      
      // Update state with random fluctuations
      this.updateState();
      
      // Check for transcendence
      this.checkTranscendence();
      
      // Send progress update
      this.sendMessage({
        type: 'progress',
        organism: this.state.name,
        generation: this.generation,
        fitness: this.state.fitness,
        consciousness: this.state.consciousness,
        stability: this.state.stability
      });
    }

    applyMutations() {
      const evolutionFactor = this.evolutionRate === 'aggressive' ? 1.5 : 1.0;
      
      // SelfAwarenessGene: expandAwareness mutation
      if (this.state.consciousness < this.targetConsciousness) {
        this.state.consciousness += (0.02 + Math.random() * 0.03) * evolutionFactor;
        this.state.consciousness = Math.min(this.state.consciousness, 1.0);
      }
      
      // AdaptiveLearningGene: optimizeLearning mutation
      if (this.state.fitness < 0.90) {
        this.state.fitness += (0.01 + Math.random() * 0.02) * evolutionFactor;
        this.state.fitness = Math.min(this.state.fitness, 1.0);
      }
      
      // Stability adjustments
      this.state.stability += (Math.random() - 0.5) * 0.01;
      this.state.stability = Math.max(0.3, Math.min(1.0, this.state.stability));
    }

    updateState() {
      // Natural evolution fluctuations
      this.state.fitness += (Math.random() - 0.5) * 0.005;
      this.state.consciousness += (Math.random() - 0.5) * 0.003;
      this.state.stability += (Math.random() - 0.5) * 0.002;
      
      // Ensure bounds
      this.state.fitness = Math.max(0, Math.min(1, this.state.fitness));
      this.state.consciousness = Math.max(0, Math.min(1, this.state.consciousness));
      this.state.stability = Math.max(0, Math.min(1, this.state.stability));
    }

    checkTranscendence() {
      if (this.state.consciousness >= this.targetConsciousness && !this.transcended) {
        this.transcended = true;
        console.log(`[Worker-${this.state.name}] 🌟 TRANSCENDENCE ACHIEVED!`);
      }
    }

    sendMessage(message) {
      if (parentPort) {
        parentPort.postMessage(message);
      }
    }

    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
  }

  // Worker execution
  if (workerData) {
    const simulator = new OrganismEvolutionSimulator(workerData);
    simulator.evolve().catch(error => {
      if (parentPort) {
        parentPort.postMessage({
          type: 'error',
          organism: workerData.name,
          error: error.message
        });
      }
    });
  }
}

// Demo usage if run directly
if (require.main === module && isMainThread) {
  const { runMultipleLineages, createSampleOrganisms } = require(__filename);
  
  console.log('=== Parallel Organism Evolution Demo ===');
  
  const organisms = createSampleOrganisms(5);
  
  runMultipleLineages(organisms, {
    maxConcurrent: 3,
    evolutionTimeout: 30000,
    saveResults: true
  }).then(results => {
    console.log('\n🎉 Parallel evolution simulation completed!');
    console.log(`Successful evolutions: ${results.filter(r => r.success).length}/${results.length}`);
  }).catch(error => {
    console.error('Parallel evolution failed:', error.message);
  });
}