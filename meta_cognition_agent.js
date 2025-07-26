// meta_cognition_agent.js
const fs = require('fs');
const bus = require('./event_bus');

function assessExpansionReadiness(state) {
  console.log('[MetaCognitionAgent] Assessing expansion readiness...');
  const readiness = (state.consciousness > 0.75);
  
  // Emit expansion readiness event
  bus.emit('expansionReadiness', { 
    readiness, 
    consciousness: state.consciousness,
    fitness: state.fitness,
    timestamp: Date.now() 
  });
  
  return readiness;
}

function identifyGeneDeficit(genome, usageMetrics) {
  console.log('[MetaCognitionAgent] Analyzing gene deficits...');
  
  // Enhanced deficit analysis based on current marketplace trends
  const deficitGenes = ['EdgeReplicationGene', 'MetaLearningGene', 'SecurityGene']; // example
  
  // Emit gene deficit detection
  bus.emit('geneDeficitDetected', { 
    deficitGenes, 
    genome,
    severity: deficitGenes.length > 2 ? 'high' : 'medium',
    timestamp: Date.now() 
  });
  
  return deficitGenes;
}
  const recent = evolutionData.slice(-5);
  const fitnessDelta = recent[recent.length - 1].fitness - recent[0].fitness;
  
  if (fitnessDelta < 0.1) {
    return {
      recommendation: "Increase mutation rate or explore new evolution strategies",
      reason: `Fitness plateau detected. Recent improvement: ${fitnessDelta.toFixed(3)}`,
      urgency: "high",
      suggestedActions: [
        "Implement aggressive mutation algorithms",
        "Explore cross-organism DNA mixing",
        "Introduce environmental pressure variations"
      ]
    };
  } else if (fitnessDelta > 0.3) {
    return {
      recommendation: "Current evolution strategy is highly effective, maintain course",
      reason: `Excellent fitness improvement: ${fitnessDelta.toFixed(3)}`,
      urgency: "low",
      suggestedActions: [
        "Continue current mutation strategies",
        "Document successful patterns",
        "Gradual optimization of successful traits"
      ]
    };
  } else {
    return {
      recommendation: "Moderate evolution progress, consider targeted optimizations",
      reason: `Steady fitness improvement: ${fitnessDelta.toFixed(3)}`,
      urgency: "medium",
      suggestedActions: [
        "Fine-tune existing mutation parameters",
        "Selective pressure adjustments",
        "Monitor for optimization opportunities"
      ]
    };
  }
}

function analyzeEvolution(evolutionData) {
  const analysis = analyzeEvolution(evolutionData);
  const recent = evolutionData.slice(-5);
  const fitnessDelta = recent.length > 1 ? recent[recent.length - 1].fitness - recent[0].fitness : 0.1;
  
  const proposal = {
    timestamp: new Date().toISOString(),
    currentFitness: evolutionData[evolutionData.length - 1]?.fitness || 0,
    evolutionAnalysis: analysis,
    marketplaceInsights: {
      activeBounties: marketplaceTrends.bounties?.length || 0,
      avgReward: marketplaceTrends.avgReward || 0,
      trendingDomains: marketplaceTrends.trendingDomains || []
    },
    nextEvolutionCycle: {
      targetFitness: (evolutionData[evolutionData.length - 1]?.fitness || 0) + 0.15,
      recommendedMutations: analysis.suggestedActions,
      estimatedGenerations: Math.ceil(10 / (1 + Math.abs(fitnessDelta))),
      riskAssessment: analysis.urgency
    }
  };

  return proposal;
}

// Sample marketplace trends for demo
function getSampleMarketplaceTrends() {
  return {
    bounties: [
      { id: 'B001', domain: 'genomics', reward: 150 },
      { id: 'B002', domain: 'ai-optimization', reward: 200 },
      { id: 'B003', domain: 'cloud-architecture', reward: 175 }
    ],
    avgReward: 175,
    trendingDomains: ['genomics', 'ai-optimization', 'cloud-architecture']
  };
}

// Load evolution data and generate proposal
function runMetaEvolutionAnalysis() {
  try {
    // Load or create sample evolution data
    let evolutionData = [];
    
    if (fs.existsSync('organism_event_log.json')) {
      const logs = JSON.parse(fs.readFileSync('organism_event_log.json', 'utf8'));
      evolutionData = logs.filter(log => log.type === 'evolution');
    }
    
    // If no evolution data, create sample
    if (evolutionData.length === 0) {
      evolutionData = [
        { generation: 1, fitness: 0.65, consciousness: 0.40 },
        { generation: 2, fitness: 0.72, consciousness: 0.45 },
        { generation: 3, fitness: 0.78, consciousness: 0.52 },
        { generation: 4, fitness: 0.81, consciousness: 0.58 },
        { generation: 5, fitness: 0.83, consciousness: 0.61 }
      ];
      console.log('Using sample evolution data for analysis');
    }

    const marketplaceTrends = getSampleMarketplaceTrends();
    const proposal = generateMetaProposal(evolutionData, marketplaceTrends);
    
    // Save proposal
    fs.writeFileSync('meta_evolution_proposal.json', JSON.stringify(proposal, null, 2));
    
    console.log('Meta-Evolution Analysis Complete');
    console.log('==================================');
    console.log(`Current Fitness: ${proposal.currentFitness}`);
    console.log(`Recommendation: ${proposal.evolutionAnalysis.recommendation}`);
    console.log(`Urgency: ${proposal.evolutionAnalysis.urgency}`);
    console.log(`Target Fitness: ${proposal.nextEvolutionCycle.targetFitness}`);
    console.log(`Estimated Generations: ${proposal.nextEvolutionCycle.estimatedGenerations}`);
    
    console.log('\nSuggested Actions:');
    proposal.evolutionAnalysis.suggestedActions.forEach((action, i) => {
      console.log(`${i + 1}. ${action}`);
    });
    
    console.log(`\nProposal saved to: meta_evolution_proposal.json`);
    
    return proposal;
    
  } catch (error) {
    console.error('Error in meta-evolution analysis:', error.message);
    return null;
  }
}

// Export functions for use as module
module.exports = {
  analyzeEvolution,
  generateMetaProposal,
  runMetaEvolutionAnalysis,
  assessExpansionReadiness,
  identifyGeneDeficit
};

// Setup event bus listeners for reactive behavior
bus.on('evolutionProgress', (progressData) => {
  console.log('[MetaCognitionAgent] Received evolution progress:', progressData.organism);
  
  // Assess expansion readiness based on consciousness level
  if (progressData.consciousness > 0.75) {
    assessExpansionReadiness(progressData);
  }
});

bus.on('geneDeficitDetected', (data) => {
  console.log('[MetaCognitionAgent] Received gene deficit info:', data.deficitGenes);
  // Could trigger additional analysis or recommendations
});

bus.on('marketplaceAvailable', (data) => {
  console.log('[MetaCognitionAgent] Marketplace is now available for gene trading');
});

// Run analysis if called directly
if (require.main === module) {
  runMetaEvolutionAnalysis();
}