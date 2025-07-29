// meta_cognition_agent.js
const fs = require('fs');

function analyzeEvolution(evolutionData) {
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

function generateMetaProposal(evolutionData, marketplaceTrends) {
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
  runMetaEvolutionAnalysis
};

// Run analysis if called directly
if (require.main === module) {
  runMetaEvolutionAnalysis();
}