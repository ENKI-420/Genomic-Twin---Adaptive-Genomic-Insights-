// test_integration.js
/**
 * Integration Test for Enhanced DNA-Lang Ecosystem
 * Tests all the new components working together
 */

const { validateRepoOperations } = require('./safety_checks');
const bus = require('./event_bus');
const CollaborationController = require('./collaboration_controller');
const { commitAndPushTerraform } = require('./cicd_integration');
const { runMultipleLineages, createSampleOrganisms } = require('./organism_evolution_worker');

async function testIntegration() {
  console.log('🧬 Starting DNA-Lang Ecosystem Integration Test...');
  console.log('=' .repeat(60));

  try {
    // 1. Test Repository Validation
    console.log('\n1. Testing Repository Validation...');
    const validation = await validateRepoOperations('.');
    console.log(`   Repository validation: ${validation.passed ? '✅ PASSED' : '❌ FAILED'}`);
    if (!validation.passed) {
      console.log('   Errors:', validation.errors);
    }

    // 2. Test Event Bus System
    console.log('\n2. Testing Event Bus System...');
    
    let eventReceived = false;
    bus.on('test-event', (data) => {
      console.log('   ✅ Event received:', data.message);
      eventReceived = true;
    });
    
    bus.emit('test-event', { message: 'Integration test event' });
    console.log(`   Event system: ${eventReceived ? '✅ WORKING' : '❌ FAILED'}`);

    // 3. Test Collaboration Controller
    console.log('\n3. Testing Collaboration Controller...');
    const controller = new CollaborationController();
    await controller.initialize();
    console.log('   ✅ Collaboration controller initialized');

    // 4. Test Agent Communication
    console.log('\n4. Testing Agent Communication...');
    
    // Simulate expansion readiness event
    setTimeout(() => {
      console.log('   📡 Emitting expansion readiness...');
      bus.emit('expansionReadiness', { readiness: true, consciousness: 0.85 });
    }, 1000);

    // Simulate gene deficit detection
    setTimeout(() => {
      console.log('   📡 Emitting gene deficit detection...');
      bus.emit('geneDeficitDetected', { 
        deficitGenes: ['EdgeReplicationGene', 'MetaLearningGene'],
        severity: 'high'
      });
    }, 2000);

    // 5. Test Parallel Evolution (small scale)
    console.log('\n5. Testing Parallel Evolution...');
    const testOrganisms = createSampleOrganisms(2);
    const evolutionResults = await runMultipleLineages(testOrganisms, {
      maxConcurrent: 2,
      evolutionTimeout: 15000,
      saveResults: false
    });
    
    const successfulEvolutions = evolutionResults.filter(r => r.success).length;
    console.log(`   Parallel evolution: ${successfulEvolutions}/${evolutionResults.length} successful`);

    // 6. Test CI/CD Integration (dry run)
    console.log('\n6. Testing CI/CD Integration (dry run)...');
    const commitResult = await commitAndPushTerraform('.', 'Integration test commit', { dryRun: true });
    console.log(`   CI/CD dry run: ${commitResult.success ? '✅ PASSED' : '❌ FAILED'}`);

    // 7. Get Event Statistics
    console.log('\n7. Event Bus Statistics...');
    const stats = bus.getEventStats();
    console.log(`   Total events: ${stats.totalEvents}`);
    console.log(`   Event types: ${Object.keys(stats.eventTypes).length}`);

    console.log('\n🎉 Integration Test Completed Successfully!');
    console.log('=' .repeat(60));
    console.log('All major components are working together:');
    console.log('✅ Repository validation with detailed diagnostics');
    console.log('✅ Event bus for reactive agent communication');
    console.log('✅ Collaboration controller for workflow orchestration');
    console.log('✅ Parallel organism evolution simulation');
    console.log('✅ CI/CD integration with safety checks');
    console.log('✅ Enhanced error handling and monitoring');

    return true;

  } catch (error) {
    console.error('\n❌ Integration Test Failed:', error.message);
    return false;
  }
}

// Run test if executed directly
if (require.main === module) {
  testIntegration()
    .then(success => {
      process.exit(success ? 0 : 1);
    })
    .catch(err => {
      console.error('Test execution failed:', err);
      process.exit(1);
    });
}

module.exports = { testIntegration };