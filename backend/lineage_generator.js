// lineage_generator.js
const fs = require('fs');

function createLineage(root, generations) {
  let nodes = [];
  let queue = [{ id: root, generation: 1, parent: null }];

  while (queue.length > 0) {
    const current = queue.shift();
    nodes.push(current);
    
    if (current.generation < generations) {
      // Create 2-3 children per node
      const childCount = Math.floor(Math.random() * 2) + 2;
      for (let i = 0; i < childCount; i++) {
        const childId = `${current.id}-${current.generation + 1}-${i + 1}`;
        queue.push({
          id: childId,
          generation: current.generation + 1,
          parent: current.id
        });
      }
    }
  }

  return nodes;
}

function generateLineageData(rootOrganism = "GenesisOrg", generations = 4) {
  console.log(`Generating lineage for ${rootOrganism} across ${generations} generations...`);
  
  const lineage = createLineage(rootOrganism, generations);
  
  // Add metadata to nodes
  const enrichedLineage = lineage.map(node => ({
    ...node,
    fitness: Math.random() * 0.3 + 0.7, // Fitness between 0.7-1.0
    mutations: Math.floor(Math.random() * 5) + 1,
    timestamp: new Date(Date.now() - Math.random() * 86400000 * 30).toISOString() // Random time in last 30 days
  }));
  
  // Sort by generation for better visualization
  enrichedLineage.sort((a, b) => a.generation - b.generation);
  
  return enrichedLineage;
}

function saveLineageData(lineageData, filename = 'lineage.json') {
  try {
    fs.writeFileSync(filename, JSON.stringify(lineageData, null, 2));
    console.log(`Lineage data saved to ${filename}`);
    
    // Generate summary statistics
    const stats = {
      totalOrganisms: lineageData.length,
      generations: Math.max(...lineageData.map(n => n.generation)),
      avgFitness: lineageData.reduce((sum, n) => sum + n.fitness, 0) / lineageData.length,
      maxFitness: Math.max(...lineageData.map(n => n.fitness)),
      totalMutations: lineageData.reduce((sum, n) => sum + n.mutations, 0)
    };
    
    console.log('\nLineage Statistics:');
    console.log(`- Total Organisms: ${stats.totalOrganisms}`);
    console.log(`- Generations: ${stats.generations}`);
    console.log(`- Average Fitness: ${stats.avgFitness.toFixed(3)}`);
    console.log(`- Maximum Fitness: ${stats.maxFitness.toFixed(3)}`);
    console.log(`- Total Mutations: ${stats.totalMutations}`);
    
    return stats;
  } catch (error) {
    console.error('Error saving lineage data:', error.message);
    return null;
  }
}

// Export functions for use as module
module.exports = {
  createLineage,
  generateLineageData,
  saveLineageData
};

// Run generator if called directly
if (require.main === module) {
  const rootName = process.argv[2] || "GenomicTwin-Genesis";
  const generations = parseInt(process.argv[3]) || 4;
  
  console.log('=== Digital Organism Lineage Generator ===');
  
  const lineageData = generateLineageData(rootName, generations);
  const stats = saveLineageData(lineageData);
  
  if (stats) {
    console.log('\nLineage generation completed successfully!');
    console.log('Next steps:');
    console.log('1. Open lineage_visualizer.html in a web browser');
    console.log('2. Or run: python3 -m http.server 8000');
    console.log('3. Navigate to: http://localhost:8000/lineage_visualizer.html');
  }
}