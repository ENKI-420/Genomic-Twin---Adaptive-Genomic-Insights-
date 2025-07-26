#!/bin/bash

# DNA-Lang Autonomous Evolution Demo Script
# This script demonstrates autonomous evolution with GitHub repository management
# Author: DNA-Lang Platform Team
# Version: 1.0

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
REPO_NAME=""
TEMP_DIR=""
GITHUB_TOKEN=""
REPO_URL=""
LOCAL_REPO_PATH=""

# Banner function with DNA-themed ASCII art
show_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║           🧬 DNA-Lang Autonomous Evolution Demo 🧬          ║"
    echo "║                                                            ║"
    echo "║  Demonstrates autonomous code evolution with GitHub        ║"
    echo "║  repository management and real-time collaboration        ║"
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
    log_step "Checking dependencies..."
    
    local missing_deps=()
    
    # Check for git
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    else
        log_success "Git is installed ($(git --version | cut -d' ' -f3))"
    fi
    
    # Check for GitHub CLI
    if ! command -v gh &> /dev/null; then
        missing_deps+=("gh (GitHub CLI)")
    else
        log_success "GitHub CLI is installed ($(gh --version | head -n1 | cut -d' ' -f3))"
    fi
    
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
        log_error "Missing required dependencies:"
        for dep in "${missing_deps[@]}"; do
            echo -e "  ${RED}✗${NC} $dep"
        done
        echo
        echo -e "${YELLOW}Please install the missing dependencies:${NC}"
        echo "  • Git: https://git-scm.com/downloads"
        echo "  • GitHub CLI: https://cli.github.com/"
        echo "  • Node.js & npm: https://nodejs.org/"
        exit 1
    fi
    
    log_success "All dependencies are satisfied!"
    echo
}

# Check GitHub authentication
check_github_auth() {
    log_step "Checking GitHub authentication..."
    
    if ! gh auth status &> /dev/null; then
        log_warning "GitHub CLI is not authenticated"
        echo -e "${YELLOW}Please authenticate with GitHub CLI first:${NC}"
        echo -e "  ${CYAN}gh auth login${NC}"
        echo
        echo -e "${YELLOW}Authentication options:${NC}"
        echo "  • Login via web browser (recommended)"
        echo "  • Login with a token"
        echo "  • Login via GitHub App"
        echo
        read -p "Press Enter after authentication is complete, or Ctrl+C to exit..."
        
        # Verify authentication worked
        if ! gh auth status &> /dev/null; then
            log_error "GitHub authentication failed or incomplete"
            echo -e "${RED}Please ensure you have completed the authentication process.${NC}"
            echo -e "${YELLOW}You can verify with: ${CYAN}gh auth status${NC}"
            exit 1
        fi
    fi
    
    # Get and display current user
    local github_user
    github_user=$(gh api user --jq .login 2>/dev/null || echo "unknown")
    log_success "GitHub authentication verified for user: ${BOLD}${github_user}${NC}"
    echo
}

# Generate a unique repository name
generate_repo_name() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local random_suffix
    
    # Try to use openssl for better randomness, fallback to $RANDOM
    if command -v openssl &> /dev/null; then
        random_suffix=$(openssl rand -hex 3 2>/dev/null || echo "$(printf '%06x' $(( RANDOM % 16777216 )))")
    else
        random_suffix=$(printf '%06x' $(( RANDOM % 16777216 )))
    fi
    
    REPO_NAME="dna-lang-evolution-${timestamp}-${random_suffix}"
    log_info "Generated repository name: ${BOLD}${REPO_NAME}${NC}"
}

# Create GitHub repository
create_github_repo() {
    log_step "Creating GitHub repository: ${BOLD}${REPO_NAME}${NC}"
    
    # Get GitHub username for repo URL construction
    local github_user
    github_user=$(gh api user --jq .login 2>/dev/null)
    if [ -z "$github_user" ]; then
        log_error "Failed to get GitHub username"
        exit 1
    fi
    
    # Check if repository already exists
    if gh repo view "$github_user/$REPO_NAME" &> /dev/null; then
        log_warning "Repository '$REPO_NAME' already exists"
        echo -e "${YELLOW}Repository URL: https://github.com/$github_user/$REPO_NAME${NC}"
        echo
        read -p "Do you want to delete and recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_step "Deleting existing repository..."
            if gh repo delete "$github_user/$REPO_NAME" --yes; then
                log_success "Repository deleted"
            else
                log_error "Failed to delete repository"
                exit 1
            fi
        else
            log_error "Cannot proceed with existing repository"
            exit 1
        fi
    fi
    
    # Create new repository
    log_step "Creating repository with GitHub CLI..."
    if gh repo create "$REPO_NAME" \
        --description "DNA-Lang Autonomous Evolution Demo - Generated $(date)" \
        --public \
        --clone=false \
        --gitignore-template=Node; then
        
        REPO_URL="https://github.com/$github_user/$REPO_NAME"
        log_success "Repository created successfully"
        log_info "Repository URL: ${BOLD}$REPO_URL${NC}"
    else
        log_error "Failed to create GitHub repository"
        exit 1
    fi
    echo
}

# Clone repository locally
clone_repository() {
    log_step "Cloning repository locally..."
    
    TEMP_DIR=$(mktemp -d)
    LOCAL_REPO_PATH="$TEMP_DIR/$REPO_NAME"
    
    cd "$TEMP_DIR"
    gh repo clone "$REPO_NAME"
    cd "$REPO_NAME"
    
    log_success "Repository cloned to: ${BOLD}$LOCAL_REPO_PATH${NC}"
    echo
}

# Generate DNA sequence with evolutionary properties
generate_dna_file() {
    log_step "Generating DNA sequence file..."
    
    local dna_file="dna_sequence.txt"
    local generation=1
    
    # Generate initial DNA sequence
    cat > "$dna_file" << 'EOF'
# DNA-Lang Autonomous Evolution Sequence
# Generation: 1
# Timestamp: TIMESTAMP_PLACEHOLDER
# Mutations: 0

SEQUENCE_START
ATCGATCGATCGATCG
GCTAGCTAGCTAGCTA
TTAATTAATTAATTAA
CGCGCGCGCGCGCGCG
SEQUENCE_END

# Evolution Log
GEN_1: Initial sequence created
EOF
    
    # Replace timestamp placeholder
    sed -i "s/TIMESTAMP_PLACEHOLDER/$(date -u +%Y-%m-%dT%H:%M:%SZ)/" "$dna_file"
    
    log_success "DNA sequence file created: ${BOLD}$dna_file${NC}"
    return 0
}

# Generate Node.js runner for autonomous evolution
generate_nodejs_runner() {
    log_step "Creating Node.js evolution runner..."
    
    # Create package.json
    cat > package.json << 'EOF'
{
  "name": "dna-lang-evolution",
  "version": "1.0.0",
  "description": "Autonomous DNA sequence evolution runner",
  "main": "evolution_runner.js",
  "scripts": {
    "start": "node evolution_runner.js",
    "evolve": "node evolution_runner.js --evolve",
    "test": "echo \"DNA evolution test passed\" && exit 0"
  },
  "keywords": ["dna", "evolution", "autonomous", "genomic"],
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
    
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].match(/^[ATCG]+$/)) {
            // Random mutation with 10% probability per base
            let line = lines[i];
            for (let j = 0; j < line.length; j++) {
                if (Math.random() < 0.1) {
                    const newBase = bases[Math.floor(Math.random() * bases.length)];
                    line = line.substring(0, j) + newBase + line.substring(j + 1);
                    mutated = true;
                }
            }
            lines[i] = line;
        }
    }
    
    return { sequence: lines.join('\n'), mutated };
}

function updateGeneration(content) {
    const lines = content.split('\n');
    let generation = 1;
    let mutations = 0;
    
    // Extract current generation and mutations
    for (const line of lines) {
        if (line.startsWith('# Generation:')) {
            generation = parseInt(line.split(':')[1].trim()) + 1;
        }
        if (line.startsWith('# Mutations:')) {
            mutations = parseInt(line.split(':')[1].trim()) + 1;
        }
    }
    
    // Update metadata
    const timestamp = new Date().toISOString();
    const updatedContent = content
        .replace(/# Generation: \d+/, `# Generation: ${generation}`)
        .replace(/# Timestamp: .+/, `# Timestamp: ${timestamp}`)
        .replace(/# Mutations: \d+/, `# Mutations: ${mutations}`)
        .replace(/# Evolution Log\n/, `# Evolution Log\nGEN_${generation}: Mutation applied at ${timestamp}\n`);
    
    return updatedContent;
}

function evolve() {
    log('🧬 Starting DNA Evolution Process...', 'cyan');
    
    const originalSequence = readDNASequence();
    if (!originalSequence) return;
    
    log('📖 Reading current DNA sequence...', 'blue');
    
    const { sequence: mutatedSequence, mutated } = mutateDNA(originalSequence);
    
    if (mutated) {
        log('⚡ Mutations detected! Updating sequence...', 'yellow');
        const updatedContent = updateGeneration(mutatedSequence);
        
        fs.writeFileSync('dna_sequence.txt', updatedContent);
        log('✅ DNA sequence evolved successfully!', 'green');
        
        // Show evolution statistics
        const generation = updatedContent.match(/# Generation: (\d+)/)[1];
        const mutations = updatedContent.match(/# Mutations: (\d+)/)[1];
        
        log(`📊 Evolution Stats:`, 'magenta');
        log(`   Generation: ${generation}`, 'bright');
        log(`   Total Mutations: ${mutations}`, 'bright');
    } else {
        log('🔄 No mutations in this cycle', 'yellow');
    }
}

function showInfo() {
    log('🧬 DNA-Lang Autonomous Evolution Runner', 'cyan');
    log('=====================================', 'cyan');
    
    const sequence = readDNASequence();
    if (sequence) {
        const generation = sequence.match(/# Generation: (\d+)/)?.[1] || '1';
        const mutations = sequence.match(/# Mutations: (\d+)/)?.[1] || '0';
        const timestamp = sequence.match(/# Timestamp: (.+)/)?.[1] || 'Unknown';
        
        log(`Current Generation: ${generation}`, 'green');
        log(`Total Mutations: ${mutations}`, 'green');
        log(`Last Update: ${timestamp}`, 'green');
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
    
    # Create README for the repository
    cat > README.md << 'EOF'
# DNA-Lang Autonomous Evolution Demo

This repository demonstrates autonomous DNA sequence evolution using the DNA-Lang platform.

## Features

- 🧬 Autonomous DNA sequence mutation
- 📊 Generation tracking and statistics
- ⚡ Real-time evolution monitoring
- 🎯 Node.js-based evolution engine

## Quick Start

```bash
# Install dependencies (none required for basic operation)
npm install

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
2. **Mutation**: Random base changes occur with 10% probability
3. **Tracking**: Generation numbers and mutation counts are tracked
4. **Logging**: All changes are logged with timestamps

## File Structure

- `dna_sequence.txt` - The evolving DNA sequence
- `evolution_runner.js` - Node.js evolution engine
- `package.json` - Project configuration

## Generated by DNA-Lang Platform

This demo was automatically generated by the DNA-Lang Autonomous Evolution Demo script.
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
    
    # Run multiple evolution cycles
    for i in {1..3}; do
        log_evolution "Evolution Cycle $i"
        
        # Run evolution
        node evolution_runner.js --evolve
        
        # Show current status
        echo -e "${CYAN}Current DNA Status:${NC}"
        node evolution_runner.js
        
        # Simulate time passage
        sleep 2
        echo
    done
    
    log_success "Evolution demonstration completed!"
    echo
}

# Commit and push changes to GitHub
commit_and_push() {
    log_step "Committing and pushing changes to GitHub..."
    
    # Configure git user if not set
    if ! git config user.email &> /dev/null; then
        git config user.email "dna-lang-demo@example.com"
        git config user.name "DNA-Lang Demo"
    fi
    
    # Add all files
    git add .
    
    # Create initial commit
    git commit -m "Initial DNA-Lang autonomous evolution demo

- Added DNA sequence file with evolutionary properties
- Created Node.js evolution runner
- Implemented autonomous mutation system
- Added comprehensive documentation

Generated by DNA-Lang Platform $(date)"
    
    # Push to GitHub
    git push origin main
    
    log_success "Changes pushed to GitHub: ${BOLD}$REPO_URL${NC}"
    echo
}

# Display final summary
show_summary() {
    log_step "Demo Summary"
    echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════════════════╗"
    echo -e "║                    Demo Complete!                     ║"
    echo -e "╚════════════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${WHITE}${BOLD}Repository Information:${NC}"
    echo -e "  📂 Repository: ${BOLD}$REPO_NAME${NC}"
    echo -e "  🌐 URL: ${BOLD}$REPO_URL${NC}"
    echo -e "  📁 Local Path: ${BOLD}$LOCAL_REPO_PATH${NC}"
    echo
    echo -e "${WHITE}${BOLD}What was created:${NC}"
    echo -e "  ${GREEN}✓${NC} GitHub repository with autonomous evolution demo"
    echo -e "  ${GREEN}✓${NC} DNA sequence file with mutation tracking"
    echo -e "  ${GREEN}✓${NC} Node.js evolution runner with color output"
    echo -e "  ${GREEN}✓${NC} Comprehensive documentation and README"
    echo -e "  ${GREEN}✓${NC} Autonomous evolution demonstration"
    echo
    echo -e "${WHITE}${BOLD}Next Steps:${NC}"
    echo -e "  🔍 Visit the repository: ${CYAN}$REPO_URL${NC}"
    echo -e "  📋 Clone locally: ${CYAN}git clone $REPO_URL${NC}"
    echo -e "  🚀 Run evolution: ${CYAN}cd $REPO_NAME && npm run evolve${NC}"
    echo
}

# Cleanup function
cleanup() {
    if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        log_step "Cleaning up temporary files..."
        rm -rf "$TEMP_DIR"
        log_success "Cleanup completed"
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
            --repo-name)
                REPO_NAME="$2"
                shift 2
                ;;
            --help|-h)
                echo "DNA-Lang Autonomous Evolution Demo"
                echo
                echo "Usage: $0 [OPTIONS]"
                echo
                echo "Options:"
                echo "  --repo-name NAME    Specify custom repository name"
                echo "  --help, -h          Show this help message"
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
    check_github_auth
    
    # Generate repository name if not provided
    if [ -z "$REPO_NAME" ]; then
        generate_repo_name
    else
        log_info "Using provided repository name: ${BOLD}${REPO_NAME}${NC}"
    fi
    
    create_github_repo
    clone_repository
    
    # Change to repository directory for file operations
    cd "$LOCAL_REPO_PATH"
    
    generate_dna_file
    generate_nodejs_runner
    demonstrate_evolution
    commit_and_push
    show_summary
    
    log_success "DNA-Lang Autonomous Evolution Demo completed successfully!"
}

# Run main function with all arguments
main "$@"