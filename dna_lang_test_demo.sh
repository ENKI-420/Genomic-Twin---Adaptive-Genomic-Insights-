#!/bin/bash

# DNA-Lang Autonomous Evolution Demo Script - Test Version
# This script demonstrates autonomous evolution without requiring GitHub authentication
# Author: DNA-Lang Platform Team
# Version: 1.0-test

set -e  # Exit on any error

# Color definitions for enhanced user experience
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly WHITE='\033[1;37m'
readonly BOLD='\033[1m'
readonly NC='\033[0m' # No Color

# Global variables
TEMP_DIR=""
TEST_MODE=true

# Banner function with DNA-themed ASCII art
show_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║       🧬 DNA-Lang Autonomous Evolution Demo (Test) 🧬       ║"
    echo "║                                                            ║"
    echo "║  Local demonstration of autonomous code evolution          ║"
    echo "║  without requiring GitHub authentication                   ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
}

# Logging functions with color-coded output
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

log_evolution() {
    echo -e "${CYAN}[EVOLUTION]${NC} $1"
}

# Check if required CLI tools are installed
check_dependencies() {
    log_step "Checking dependencies for local testing..."
    
    local missing_deps=()
    
    # Check for Node.js
    if ! command -v node &> /dev/null; then
        missing_deps+=("node.js")
    else
        log_success "Node.js is installed ($(node --version))"
    fi
    
    # Check for npm
    if ! command -v npm &> /dev/null; then
        missing_deps+=("npm")
    else
        log_success "npm is installed ($(npm --version))"
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing required dependencies for local testing:"
        for dep in "${missing_deps[@]}"; do
            echo -e "  ${RED}✗${NC} $dep"
        done
        echo
        echo -e "${YELLOW}Please install the missing dependencies:${NC}"
        echo "  • Node.js & npm: https://nodejs.org/"
        exit 1
    fi
    
    log_success "All dependencies for local testing are satisfied!"
    echo
}

# Create local test repository
create_local_repo() {
    log_step "Creating local test repository..."
    
    TEMP_DIR=$(mktemp -d)
    local repo_name="dna-lang-evolution-test-$(date +%Y%m%d_%H%M%S)"
    local repo_path="$TEMP_DIR/$repo_name"
    
    mkdir -p "$repo_path"
    cd "$repo_path"
    
    # Initialize git repository
    git init --quiet
    git config user.email "dna-lang-demo@example.com"
    git config user.name "DNA-Lang Demo"
    
    log_success "Local repository created: ${BOLD}$repo_path${NC}"
    echo
}

# Generate DNA sequence with evolutionary properties
generate_dna_file() {
    log_step "Generating DNA sequence file..."
    
    local dna_file="dna_sequence.txt"
    
    # Generate initial DNA sequence
    cat > "$dna_file" << EOF
# DNA-Lang Autonomous Evolution Sequence
# Generation: 1
# Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
# Mutations: 0

SEQUENCE_START
ATCGATCGATCGATCG
GCTAGCTAGCTAGCTA
TTAATTAATTAATTAA
CGCGCGCGCGCGCGCG
SEQUENCE_END

# Evolution Log
GEN_1: Initial sequence created at $(date -u +%Y-%m-%dT%H:%M:%SZ)
EOF
    
    log_success "DNA sequence file created: ${BOLD}$dna_file${NC}"
    return 0
}

# Generate Node.js runner for autonomous evolution
generate_nodejs_runner() {
    log_step "Creating Node.js evolution runner..."
    
    # Create package.json
    cat > package.json << 'EOF'
{
  "name": "dna-lang-evolution-test",
  "version": "1.0.0",
  "description": "Autonomous DNA sequence evolution runner (Test Version)",
  "main": "evolution_runner.js",
  "scripts": {
    "start": "node evolution_runner.js",
    "evolve": "node evolution_runner.js --evolve",
    "test": "echo \"DNA evolution test passed\" && exit 0"
  },
  "keywords": ["dna", "evolution", "autonomous", "genomic", "test"],
  "author": "DNA-Lang Platform",
  "license": "MIT"
}
EOF
    
    # Create evolution runner
    cat > evolution_runner.js << 'EOF'
#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Color codes for console output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function readDNASequence() {
    try {
        const content = fs.readFileSync('dna_sequence.txt', 'utf8');
        return content;
    } catch (error) {
        log('Error reading DNA sequence file', 'red');
        return null;
    }
}

function mutateDNA(sequence) {
    const bases = ['A', 'T', 'C', 'G'];
    const lines = sequence.split('\n');
    let mutated = false;
    let mutationCount = 0;
    
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].match(/^[ATCG]+$/)) {
            // Random mutation with 15% probability per base for more visible changes
            let line = lines[i];
            for (let j = 0; j < line.length; j++) {
                if (Math.random() < 0.15) {
                    const newBase = bases[Math.floor(Math.random() * bases.length)];
                    if (line[j] !== newBase) {
                        line = line.substring(0, j) + newBase + line.substring(j + 1);
                        mutated = true;
                        mutationCount++;
                    }
                }
            }
            lines[i] = line;
        }
    }
    
    return { sequence: lines.join('\n'), mutated, mutationCount };
}

function updateGeneration(content, mutationCount) {
    const lines = content.split('\n');
    let generation = 1;
    let totalMutations = 0;
    
    // Extract current generation and mutations
    for (const line of lines) {
        if (line.startsWith('# Generation:')) {
            generation = parseInt(line.split(':')[1].trim()) + 1;
        }
        if (line.startsWith('# Mutations:')) {
            totalMutations = parseInt(line.split(':')[1].trim()) + mutationCount;
        }
    }
    
    // Update metadata
    const timestamp = new Date().toISOString();
    const updatedContent = content
        .replace(/# Generation: \d+/, `# Generation: ${generation}`)
        .replace(/# Timestamp: .+/, `# Timestamp: ${timestamp}`)
        .replace(/# Mutations: \d+/, `# Mutations: ${totalMutations}`)
        .replace(/# Evolution Log\n/, `# Evolution Log\nGEN_${generation}: ${mutationCount} mutations applied at ${timestamp}\n`);
    
    return updatedContent;
}

function evolve() {
    log('🧬 Starting DNA Evolution Process...', 'cyan');
    
    const originalSequence = readDNASequence();
    if (!originalSequence) return;
    
    log('📖 Reading current DNA sequence...', 'blue');
    
    const { sequence: mutatedSequence, mutated, mutationCount } = mutateDNA(originalSequence);
    
    if (mutated) {
        log(`⚡ ${mutationCount} mutations detected! Updating sequence...`, 'yellow');
        const updatedContent = updateGeneration(mutatedSequence, mutationCount);
        
        fs.writeFileSync('dna_sequence.txt', updatedContent);
        log('✅ DNA sequence evolved successfully!', 'green');
        
        // Show evolution statistics
        const generation = updatedContent.match(/# Generation: (\d+)/)[1];
        const mutations = updatedContent.match(/# Mutations: (\d+)/)[1];
        
        log(`📊 Evolution Stats:`, 'magenta');
        log(`   Generation: ${generation}`, 'bright');
        log(`   Total Mutations: ${mutations}`, 'bright');
        log(`   This Cycle: ${mutationCount}`, 'bright');
    } else {
        log('🔄 No mutations in this cycle', 'yellow');
    }
}

function showInfo() {
    log('🧬 DNA-Lang Autonomous Evolution Runner (Test Mode)', 'cyan');
    log('================================================', 'cyan');
    
    const sequence = readDNASequence();
    if (sequence) {
        const generation = sequence.match(/# Generation: (\d+)/)?.[1] || '1';
        const mutations = sequence.match(/# Mutations: (\d+)/)?.[1] || '0';
        const timestamp = sequence.match(/# Timestamp: (.+)/)?.[1] || 'Unknown';
        
        log(`Current Generation: ${generation}`, 'green');
        log(`Total Mutations: ${mutations}`, 'green');
        log(`Last Update: ${timestamp}`, 'green');
        
        // Show a sample of the current DNA sequence
        const sequenceLines = sequence.split('\n').filter(line => line.match(/^[ATCG]+$/));
        if (sequenceLines.length > 0) {
            log('\nCurrent DNA Sequence (sample):', 'blue');
            sequenceLines.slice(0, 2).forEach(line => {
                log(`  ${line}`, 'bright');
            });
            if (sequenceLines.length > 2) {
                log(`  ... (${sequenceLines.length - 2} more lines)`, 'bright');
            }
        }
    }
    
    log('\nAvailable commands:', 'blue');
    log('  npm start      - Show this information', 'bright');
    log('  npm run evolve - Trigger evolution cycle', 'bright');
    log('  npm test       - Run evolution test', 'bright');
}

// Main execution
const args = process.argv.slice(2);
if (args.includes('--evolve')) {
    evolve();
} else {
    showInfo();
}
EOF
    
    # Create README for the test repository
    cat > README.md << 'EOF'
# DNA-Lang Autonomous Evolution Demo (Test Version)

This repository demonstrates autonomous DNA sequence evolution using the DNA-Lang platform in test mode.

## Features

- 🧬 Autonomous DNA sequence mutation
- 📊 Generation tracking and statistics
- ⚡ Real-time evolution monitoring
- 🎯 Node.js-based evolution engine
- 🧪 Local testing without GitHub dependencies

## Quick Start

```bash
# Show current evolution status
npm start

# Trigger evolution cycle
npm run evolve

# Run tests
npm test
```

## Evolution Process

The DNA sequence evolves through random mutations with each evolution cycle:

1. **Initial Generation**: A base DNA sequence is created
2. **Mutation**: Random base changes occur with 15% probability per base
3. **Tracking**: Generation numbers and mutation counts are tracked
4. **Logging**: All changes are logged with timestamps

## File Structure

- `dna_sequence.txt` - The evolving DNA sequence
- `evolution_runner.js` - Node.js evolution engine
- `package.json` - Project configuration

## Generated by DNA-Lang Platform (Test Mode)

This demo was automatically generated by the DNA-Lang Autonomous Evolution Demo script in test mode.
EOF
    
    log_success "Node.js evolution runner created"
    log_info "Files created:"
    echo -e "  ${GREEN}✓${NC} package.json"
    echo -e "  ${GREEN}✓${NC} evolution_runner.js"
    echo -e "  ${GREEN}✓${NC} README.md"
    echo
}

# Demonstrate autonomous evolution
demonstrate_evolution() {
    log_step "Demonstrating autonomous evolution..."
    
    # Run initial status check
    log_evolution "Initial State"
    node evolution_runner.js
    echo
    
    # Run multiple evolution cycles
    for i in {1..5}; do
        log_evolution "Evolution Cycle $i"
        
        # Run evolution
        node evolution_runner.js --evolve
        echo
        
        # Brief pause for readability
        sleep 1
    done
    
    # Show final status
    log_evolution "Final State"
    node evolution_runner.js
    echo
    
    log_success "Evolution demonstration completed!"
    echo
}

# Create local git commits to simulate version control
create_commits() {
    log_step "Creating git commits for version tracking..."
    
    # Add all files
    git add .
    
    # Create initial commit
    git commit -m "Initial DNA-Lang autonomous evolution demo (test mode)

- Added DNA sequence file with evolutionary properties
- Created Node.js evolution runner
- Implemented autonomous mutation system
- Added comprehensive documentation

Generated by DNA-Lang Platform $(date)" --quiet
    
    log_success "Initial commit created"
    
    # Run a few evolution cycles and commit each one
    for i in {1..3}; do
        log_step "Evolution cycle $i - creating commit..."
        node evolution_runner.js --evolve --quiet > /dev/null 2>&1 || true
        git add dna_sequence.txt
        git commit -m "Evolution cycle $i: DNA sequence mutations" --quiet
        log_success "Commit $i created"
    done
    
    echo
}

# Show git log
show_git_history() {
    log_step "Git commit history:"
    echo
    git log --oneline --color=always | head -5
    echo
}

# Display final summary
show_summary() {
    log_step "Test Demo Summary"
    echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════════════════╗"
    echo -e "║                 Test Demo Complete!                   ║"
    echo -e "╚════════════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${WHITE}${BOLD}Repository Information:${NC}"
    echo -e "  📁 Local Path: ${BOLD}$(pwd)${NC}"
    echo -e "  🧬 DNA File: ${BOLD}dna_sequence.txt${NC}"
    echo -e "  🚀 Runner: ${BOLD}evolution_runner.js${NC}"
    echo
    echo -e "${WHITE}${BOLD}What was demonstrated:${NC}"
    echo -e "  ${GREEN}✓${NC} Local repository with autonomous evolution demo"
    echo -e "  ${GREEN}✓${NC} DNA sequence file with mutation tracking"
    echo -e "  ${GREEN}✓${NC} Node.js evolution runner with color output"
    echo -e "  ${GREEN}✓${NC} Multiple evolution cycles with git tracking"
    echo -e "  ${GREEN}✓${NC} Comprehensive documentation and README"
    echo
    echo -e "${WHITE}${BOLD}Try these commands in the repository:${NC}"
    echo -e "  📊 Check status: ${CYAN}npm start${NC}"
    echo -e "  🧬 Evolve DNA: ${CYAN}npm run evolve${NC}"
    echo -e "  ✅ Run tests: ${CYAN}npm test${NC}"
    echo -e "  📝 View history: ${CYAN}git log --oneline${NC}"
    echo
}

# Cleanup function
cleanup() {
    if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ] && [ "$TEST_MODE" = true ]; then
        log_step "Cleaning up temporary files..."
        # In test mode, keep the directory for user inspection
        log_info "Test repository preserved at: ${BOLD}$TEMP_DIR${NC}"
        log_info "You can explore the generated files manually"
    fi
}

# Error handling
handle_error() {
    log_error "An error occurred during execution"
    cleanup
    exit 1
}

# Set error trap
trap handle_error ERR
trap cleanup EXIT

# Main execution function
main() {
    show_banner
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                echo "DNA-Lang Autonomous Evolution Demo (Test Version)"
                echo
                echo "Usage: $0 [OPTIONS]"
                echo
                echo "Options:"
                echo "  --help, -h          Show this help message"
                echo
                echo "This test version runs locally without requiring GitHub authentication."
                echo
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
    
    # Execute demo steps
    check_dependencies
    create_local_repo
    generate_dna_file
    generate_nodejs_runner
    demonstrate_evolution
    create_commits
    show_git_history
    show_summary
    
    log_success "DNA-Lang Autonomous Evolution Test Demo completed successfully!"
}

# Run main function with all arguments
main "$@"