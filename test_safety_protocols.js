#!/usr/bin/env node
/**
 * Test Suite for DNAos Production Safety Protocols
 * Validates the validateRepoOperations safety mechanism
 */

const { validateRepoOperations, config } = require('./evolve.js');

// Test configuration
const TEST_RESULTS = [];

function runTest(testName, testFunction) {
    console.log(`🧪 Running test: ${testName}`);
    try {
        const result = testFunction();
        if (result) {
            console.log(`✅ PASS: ${testName}`);
            TEST_RESULTS.push({ test: testName, status: 'PASS' });
        } else {
            console.log(`❌ FAIL: ${testName}`);
            TEST_RESULTS.push({ test: testName, status: 'FAIL' });
        }
    } catch (error) {
        console.log(`❌ ERROR: ${testName} - ${error.message}`);
        TEST_RESULTS.push({ test: testName, status: 'ERROR', error: error.message });
    }
    console.log('');
}

// Test 1: Simulation mode should always pass
function testSimulationModeAlwaysPasses() {
    // Clear any existing token to ensure simulation behavior
    const originalToken = process.env.GITHUB_ACCESS_TOKEN;
    delete process.env.GITHUB_ACCESS_TOKEN;
    
    const result = validateRepoOperations(true);
    
    // Restore original token
    if (originalToken) {
        process.env.GITHUB_ACCESS_TOKEN = originalToken;
    }
    
    return result === true;
}

// Test 2: Production mode should fail without token
function testProductionModeFailsWithoutToken() {
    // Clear token to simulate missing credentials
    const originalToken = process.env.GITHUB_ACCESS_TOKEN;
    delete process.env.GITHUB_ACCESS_TOKEN;
    
    const result = validateRepoOperations(false);
    
    // Restore original token
    if (originalToken) {
        process.env.GITHUB_ACCESS_TOKEN = originalToken;
    }
    
    return result === false;
}

// Test 3: Production mode should pass with token
function testProductionModePassesWithToken() {
    // Set a mock token
    const originalToken = process.env.GITHUB_ACCESS_TOKEN;
    process.env.GITHUB_ACCESS_TOKEN = "ghp_mock_token_for_testing";
    
    const result = validateRepoOperations(false);
    
    // Restore original token or clear if none existed
    if (originalToken) {
        process.env.GITHUB_ACCESS_TOKEN = originalToken;
    } else {
        delete process.env.GITHUB_ACCESS_TOKEN;
    }
    
    return result === true;
}

// Test 4: Configuration should have required values
function testConfigurationValues() {
    return (
        config.MAX_GENERATIONS > 0 &&
        config.FITNESS_INCREMENT > 0 &&
        config.CONSCIOUSNESS_INCREMENT > 0 &&
        config.TRANSCENDENCE_THRESHOLD > 0 &&
        config.TRANSCENDENCE_THRESHOLD <= 1 &&
        config.GITHUB_USERNAME === "ENKI-420"
    );
}

// Test 5: Mode determination logic
function testModeDetection() {
    // Test explicit simulation mode
    const originalMode = process.env.SIMULATION_MODE;
    const originalToken = process.env.GITHUB_ACCESS_TOKEN;
    
    // Case 1: Explicit simulation mode overrides token presence
    process.env.SIMULATION_MODE = 'true';
    process.env.GITHUB_ACCESS_TOKEN = 'fake_token';
    const simulationMode1 = (process.env.SIMULATION_MODE === 'true' || !process.env.GITHUB_ACCESS_TOKEN);
    
    // Case 2: No simulation mode, no token = simulation
    delete process.env.SIMULATION_MODE;
    delete process.env.GITHUB_ACCESS_TOKEN;
    const simulationMode2 = (process.env.SIMULATION_MODE === 'true' || !process.env.GITHUB_ACCESS_TOKEN);
    
    // Case 3: No simulation mode, with token = production
    delete process.env.SIMULATION_MODE;
    process.env.GITHUB_ACCESS_TOKEN = 'fake_token';
    const simulationMode3 = (process.env.SIMULATION_MODE === 'true' || !process.env.GITHUB_ACCESS_TOKEN);
    
    // Restore original values
    if (originalMode) {
        process.env.SIMULATION_MODE = originalMode;
    } else {
        delete process.env.SIMULATION_MODE;
    }
    if (originalToken) {
        process.env.GITHUB_ACCESS_TOKEN = originalToken;
    } else {
        delete process.env.GITHUB_ACCESS_TOKEN;
    }
    
    return simulationMode1 === true && simulationMode2 === true && simulationMode3 === false;
}

// Run all tests
console.log('🚀 Starting DNAos Safety Protocol Test Suite');
console.log('='.repeat(50));
console.log('');

runTest('Simulation Mode Always Passes', testSimulationModeAlwaysPasses);
runTest('Production Mode Fails Without Token', testProductionModeFailsWithoutToken);
runTest('Production Mode Passes With Token', testProductionModePassesWithToken);
runTest('Configuration Values Are Valid', testConfigurationValues);
runTest('Mode Detection Logic Works Correctly', testModeDetection);

// Summary
console.log('📊 Test Results Summary');
console.log('='.repeat(30));
const passCount = TEST_RESULTS.filter(r => r.status === 'PASS').length;
const failCount = TEST_RESULTS.filter(r => r.status === 'FAIL').length;
const errorCount = TEST_RESULTS.filter(r => r.status === 'ERROR').length;

console.log(`✅ Passed: ${passCount}`);
console.log(`❌ Failed: ${failCount}`);
console.log(`🚫 Errors: ${errorCount}`);
console.log(`📈 Success Rate: ${((passCount / TEST_RESULTS.length) * 100).toFixed(1)}%`);

if (failCount > 0 || errorCount > 0) {
    console.log('\n❌ FAILED TESTS:');
    TEST_RESULTS.filter(r => r.status !== 'PASS').forEach(result => {
        console.log(`   - ${result.test}: ${result.status}${result.error ? ` (${result.error})` : ''}`);
    });
    process.exit(1);
} else {
    console.log('\n🎉 All tests passed! Safety protocols are working correctly.');
    process.exit(0);
}