#!/usr/bin/env node
/**
 * Test suite for DNA-Lang CLI
 * Validates the three main CLI commands: compile, evolve, deploy
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class DNALangCLITests {
    constructor() {
        this.testResults = [];
        this.tempFiles = [];
    }

    async runTests() {
        console.log('🧬 DNA-Lang CLI Test Suite');
        console.log('='.repeat(40));
        
        try {
            await this.testCLIHelp();
            await this.testCompileCommand();
            await this.testEvolveCommand();
            await this.testDeployCommand();
            await this.testErrorHandling();
            
            this.printResults();
            this.cleanup();
            
            const passed = this.testResults.filter(r => r.passed).length;
            const total = this.testResults.length;
            
            if (passed === total) {
                console.log(`\n✅ All ${total} tests passed!`);
                process.exit(0);
            } else {
                console.log(`\n❌ ${total - passed} of ${total} tests failed!`);
                process.exit(1);
            }
            
        } catch (error) {
            console.error('\n❌ Test suite error:', error.message);
            this.cleanup();
            process.exit(1);
        }
    }

    async testCLIHelp() {
        this.test('CLI Help Command', () => {
            const output = execSync('node bin/dna --help', { encoding: 'utf8' });
            if (!output.includes('DNA-Lang CLI')) {
                throw new Error('Help output missing CLI title');
            }
            if (!output.includes('compile') || !output.includes('evolve') || !output.includes('deploy')) {
                throw new Error('Help output missing required commands');
            }
        });
    }

    async testCompileCommand() {
        this.test('Compile TestApp.dna', () => {
            const output = execSync('node bin/dna compile TestApp.dna --optimize --target=production', { encoding: 'utf8' });
            
            if (!output.includes('DNA-Lang Compiler')) {
                throw new Error('Compiler output missing');
            }
            if (!output.includes('TestApp')) {
                throw new Error('Organism name not found in output');
            }
            if (!output.includes('Compilation complete')) {
                throw new Error('Compilation did not complete successfully');
            }
            
            // Check for generated files
            const outputDirs = fs.readdirSync('.').filter(dir => dir.startsWith('compiled_testapp_production_'));
            if (outputDirs.length === 0) {
                throw new Error('No compiled output directory found');
            }
            
            const outputDir = outputDirs[0];
            const manifestPath = path.join(outputDir, 'manifest.json');
            const runtimePath = path.join(outputDir, 'runtime.js');
            
            if (!fs.existsSync(manifestPath)) {
                throw new Error('manifest.json not generated');
            }
            if (!fs.existsSync(runtimePath)) {
                throw new Error('runtime.js not generated');
            }
            
            // Validate manifest content
            const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
            if (manifest.organism_name !== 'TestApp') {
                throw new Error('Incorrect organism name in manifest');
            }
            if (!manifest.optimized) {
                throw new Error('Optimization flag not set in manifest');
            }
            
            this.tempFiles.push(outputDir);
        });
    }

    async testEvolveCommand() {
        this.test('Evolve TestApp with latency optimization', () => {
            const output = execSync('node bin/dna evolve TestApp --optimize-for=latency --generations=5', { encoding: 'utf8' });
            
            if (!output.includes('DNA-Lang Evolution Engine')) {
                throw new Error('Evolution engine output missing');
            }
            if (!output.includes('TestApp')) {
                throw new Error('Organism name not found in evolution output');
            }
            if (!output.includes('Evolution complete')) {
                throw new Error('Evolution did not complete successfully');
            }
            if (!output.includes('latency')) {
                throw new Error('Optimization target not mentioned');
            }
            
            // Check for generated evolution file
            const evolutionFiles = fs.readdirSync('.').filter(file => file.startsWith('evolution_TestApp_'));
            if (evolutionFiles.length === 0) {
                throw new Error('No evolution results file found');
            }
            
            const evolutionFile = evolutionFiles[evolutionFiles.length - 1]; // Get latest
            const evolutionData = JSON.parse(fs.readFileSync(evolutionFile, 'utf8'));
            
            if (evolutionData.organism !== 'TestApp') {
                throw new Error('Incorrect organism name in evolution data');
            }
            if (evolutionData.evolution_type !== 'latency') {
                throw new Error('Incorrect evolution type in evolution data');
            }
            
            this.tempFiles.push(evolutionFile);
        });
    }

    async testDeployCommand() {
        this.test('Deploy SecureWebApp to GCP', () => {
            const output = execSync('node bin/dna deploy SecureWebApp --provider=gcp --domain=dnalang.app', { encoding: 'utf8' });
            
            if (!output.includes('DNA-Lang Deployment Engine')) {
                throw new Error('Deployment engine output missing');
            }
            if (!output.includes('SecureWebApp')) {
                throw new Error('Organism name not found in deployment output');
            }
            if (!output.includes('Deployment successful')) {
                throw new Error('Deployment did not complete successfully');
            }
            if (!output.includes('GCP')) {
                throw new Error('Provider not mentioned');
            }
            if (!output.includes('dnalang.app')) {
                throw new Error('Domain not mentioned');
            }
            
            // Check for generated deployment file
            const deploymentFiles = fs.readdirSync('.').filter(file => file.startsWith('deployment_securewebapp_'));
            if (deploymentFiles.length === 0) {
                throw new Error('No deployment config file found');
            }
            
            const deploymentFile = deploymentFiles[deploymentFiles.length - 1]; // Get latest
            const deploymentData = JSON.parse(fs.readFileSync(deploymentFile, 'utf8'));
            
            if (deploymentData.organism !== 'SecureWebApp') {
                throw new Error('Incorrect organism name in deployment data');
            }
            if (deploymentData.provider !== 'gcp') {
                throw new Error('Incorrect provider in deployment data');
            }
            if (deploymentData.domain !== 'dnalang.app') {
                throw new Error('Incorrect domain in deployment data');
            }
            
            this.tempFiles.push(deploymentFile);
        });
    }

    async testErrorHandling() {
        this.test('Error handling for invalid commands', () => {
            try {
                execSync('node bin/dna invalidcommand', { encoding: 'utf8' });
                throw new Error('Should have failed with invalid command');
            } catch (error) {
                // When execSync fails, the output is in error.stdout/stderr
                const allOutput = (error.stdout || '') + (error.stderr || '') + (error.output ? error.output.join('') : '');
                if (!allOutput.includes('Unknown command')) {
                    throw new Error(`Expected error message not found. Got: ${allOutput}`);
                }
            }
        });

        this.test('Error handling for missing file', () => {
            try {
                execSync('node bin/dna compile nonexistent.dna', { encoding: 'utf8' });
                throw new Error('Should have failed with missing file');
            } catch (error) {
                const allOutput = (error.stdout || '') + (error.stderr || '') + (error.output ? error.output.join('') : '');
                if (!allOutput.includes('not found')) {
                    throw new Error(`Expected file not found error message not found. Got: ${allOutput}`);
                }
            }
        });
    }

    test(name, testFn) {
        try {
            testFn();
            console.log(`✅ ${name}`);
            this.testResults.push({ name, passed: true });
        } catch (error) {
            console.log(`❌ ${name}: ${error.message}`);
            this.testResults.push({ name, passed: false, error: error.message });
        }
    }

    printResults() {
        console.log('\n' + '='.repeat(40));
        console.log('Test Results Summary:');
        console.log('='.repeat(40));
        
        this.testResults.forEach((result, index) => {
            const status = result.passed ? '✅' : '❌';
            console.log(`${status} ${index + 1}. ${result.name}`);
            if (!result.passed) {
                console.log(`   Error: ${result.error}`);
            }
        });
    }

    cleanup() {
        console.log('\n🧹 Cleaning up test files...');
        this.tempFiles.forEach(file => {
            try {
                if (fs.statSync(file).isDirectory()) {
                    fs.rmSync(file, { recursive: true, force: true });
                } else {
                    fs.unlinkSync(file);
                }
                console.log(`   Removed: ${file}`);
            } catch (error) {
                console.log(`   Warning: Could not remove ${file}: ${error.message}`);
            }
        });
    }
}

// Run tests if this script is executed directly
if (require.main === module) {
    const tests = new DNALangCLITests();
    tests.runTests();
}

module.exports = DNALangCLITests;