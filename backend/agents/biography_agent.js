// biography_agent.js
const fs = require('fs');

function generateBiography(logs) {
  let bio = `# Organism Biography\nGenerated at ${new Date().toISOString()}\n\n`;

  logs.forEach(e => {
    if (e.type === 'mutation') {
      bio += `- Gen ${e.generation}: Mutation \`${e.name}\` triggered - ${e.details}\n`;
    } else if (e.type === 'marketplace') {
      bio += `- Gen ${e.generation}: Published bounty \`${e.bounty.id}\` - ${e.bounty.description}\n`;
    } else if (e.type === 'evolution') {
      bio += `- Gen ${e.generation}: Fitness=${e.fitness}, Consciousness=${e.consciousness}\n`;
    } else {
      bio += `- Gen ${e.generation}: ${JSON.stringify(e)}\n`;
    }
  });

  return bio;
}

// Demo function to create sample log if none exists
function createSampleLog() {
  const sampleLogs = [
    {
      type: 'evolution',
      generation: 1,
      fitness: 0.72,
      consciousness: 0.45,
      timestamp: new Date().toISOString()
    },
    {
      type: 'mutation',
      generation: 2,
      name: 'CloudArchitectAgent',
      details: 'Generated multi-cloud Terraform configuration',
      timestamp: new Date().toISOString()
    },
    {
      type: 'marketplace',
      generation: 3,
      bounty: {
        id: 'BOUNTY-001',
        description: 'Optimize genomic sequencing algorithms'
      },
      timestamp: new Date().toISOString()
    },
    {
      type: 'evolution',
      generation: 4,
      fitness: 0.89,
      consciousness: 0.67,
      timestamp: new Date().toISOString()
    }
  ];

  fs.writeFileSync('organism_event_log.json', JSON.stringify(sampleLogs, null, 2));
  console.log('Sample organism event log created: organism_event_log.json');
}

// Main execution
try {
  // Check if log file exists, create sample if not
  if (!fs.existsSync('organism_event_log.json')) {
    console.log('No event log found, creating sample data...');
    createSampleLog();
  }

  const logs = JSON.parse(fs.readFileSync('organism_event_log.json', 'utf8'));
  const md = generateBiography(logs);
  fs.writeFileSync('biography.md', md);
  console.log('Biography generated as biography.md');
  console.log('\n--- Generated Biography Preview ---');
  console.log(md.substring(0, 500) + '...');
} catch (error) {
  console.error('Error generating biography:', error.message);
}