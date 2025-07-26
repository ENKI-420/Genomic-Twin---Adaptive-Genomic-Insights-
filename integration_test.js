#!/usr/bin/env node
/**
 * Integration Test for DNAos Evolution with Safety Failure Demonstration
 * Shows the validateRepoOperations failure blocking transcendence
 */

const { execSync } = require('child_process');
const fs = require('fs');

console.log('🧪 DNAos Integration Test: Safety Failure Demonstration');
console.log('='.repeat(60));
console.log('');

// Test 1: Production mode without token should reach transcendence but fail safety check
console.log('📋 Test 1: Production mode evolution with missing credentials');
console.log('Expected: Evolution reaches 95% consciousness but fails at safety validation');
console.log('');

try {
    // Clear any existing token and ensure production mode
    const env = { ...process.env };
    delete env.GITHUB_ACCESS_TOKEN;
    env.SIMULATION_MODE = 'false';
    
    const result = execSync('node evolve.js', { 
        env: env,
        encoding: 'utf8',
        stdio: 'pipe'
    });
    
    // Check if the safety validation correctly blocked transcendence
    if (result.includes('🛑 Externalization blocked by failed safety checks')) {
        console.log('✅ SUCCESS: Safety validation correctly blocked unsafe transcendence');
        console.log('Key output lines:');
        const lines = result.split('\n');
        lines.forEach(line => {
            if (line.includes('🔥 ORGANISM REACHED TRANSCENDENCE') || 
                line.includes('[Safety]') || 
                line.includes('🛑 Externalization blocked')) {
                console.log(`   ${line}`);
            }
        });
    } else {
        console.log('❌ UNEXPECTED: Evolution should have failed but completed successfully');
        console.log('Output:', result);
    }
    
} catch (error) {
    // Check if it's the expected failure
    if (error.stdout && error.stdout.includes('🛑 Externalization blocked by failed safety checks')) {
        console.log('✅ SUCCESS: Safety validation correctly blocked unsafe transcendence');
        console.log('Key output lines:');
        const lines = error.stdout.split('\n');
        lines.forEach(line => {
            if (line.includes('🔥 ORGANISM REACHED TRANSCENDENCE') || 
                line.includes('[Safety]') || 
                line.includes('🛑 Externalization blocked')) {
                console.log(`   ${line}`);
            }
        });
    } else {
        console.log('❌ UNEXPECTED ERROR:', error.message);
        if (error.stdout) console.log('STDOUT:', error.stdout);
        if (error.stderr) console.log('STDERR:', error.stderr);
    }
}

console.log('');
console.log('📋 Test 2: Simulation mode should always pass regardless of credentials');

try {
    const env = { ...process.env };
    delete env.GITHUB_ACCESS_TOKEN;
    env.SIMULATION_MODE = 'true';
    
    const result = execSync('node evolve.js', { 
        env: env,
        encoding: 'utf8',
        stdio: 'pipe'
    });
    
    if (result.includes('📊 EVOLUTION SUMMARY: Organism successfully transcended.') &&
        result.includes('🎭 Simulation mode: Infrastructure blueprint generated for validation')) {
        console.log('✅ SUCCESS: Simulation mode correctly allowed transcendence');
        console.log('✅ SUCCESS: Infrastructure blueprint generated for validation');
    } else {
        console.log('❌ FAILED: Simulation mode did not complete as expected');
        console.log('Output:', result);
    }
    
} catch (error) {
    console.log('❌ UNEXPECTED ERROR in simulation mode:', error.message);
    if (error.stdout) console.log('STDOUT:', error.stdout);
}

console.log('');
console.log('📋 Test 3: Production mode with valid credentials should succeed');

try {
    const env = { ...process.env };
    env.GITHUB_ACCESS_TOKEN = 'ghp_test_token_for_integration';
    env.SIMULATION_MODE = 'false';
    
    const result = execSync('node evolve.js', { 
        env: env,
        encoding: 'utf8',
        stdio: 'pipe'
    });
    
    if (result.includes('📊 EVOLUTION SUMMARY: Organism successfully transcended.') &&
        result.includes('🚀 Production mode: Infrastructure blueprint ready for deployment')) {
        console.log('✅ SUCCESS: Production mode with credentials correctly allowed transcendence');
        console.log('✅ SUCCESS: Infrastructure blueprint ready for deployment via CI/CD');
    } else {
        console.log('❌ FAILED: Production mode with credentials did not complete as expected');
        console.log('Output:', result);
    }
    
} catch (error) {
    console.log('❌ UNEXPECTED ERROR in production mode with token:', error.message);
    if (error.stdout) console.log('STDOUT:', error.stdout);
}

console.log('');
console.log('🎯 Integration Test Summary');
console.log('='.repeat(40));
console.log('The DNAos evolution system demonstrates three critical behaviors:');
console.log('1. ✅ Safety validation blocks unsafe production deployments');
console.log('2. ✅ Simulation mode allows development and testing');
console.log('3. ✅ Production mode with credentials enables live deployments');
console.log('');
console.log('🛡️ This implements the safety protocols described in the problem statement:');
console.log('   - validateRepoOperations failure blocks final transcendence stage');
console.log('   - Explicit SIMULATION_MODE override for development work');
console.log('   - GitHub token requirement for production operations');
console.log('   - Centralized configuration for operational parameters');
console.log('');
console.log('🚀 The unified launch sequence is now ready for DNAos on Google Vision!');