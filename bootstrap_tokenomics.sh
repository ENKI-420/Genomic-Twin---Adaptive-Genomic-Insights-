#!/bin/bash

# Tokenomics Bootstrap Script
# Sets up and runs the DNA-Lang Tokenomics Platform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

print_evolution() {
    echo -e "${CYAN}[EVOLUTION]${NC} $1"
}

# Banner
echo "╔════════════════════════════════════════════════════════════╗"
echo "║          💰 DNA-Lang Tokenomics Bootstrap 💰               ║"
echo "║                                                            ║"
echo "║  Autonomous DeFi management with DNA-Lang evolution        ║"
echo "║  Creates living tokenomics organisms that self-optimize    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check dependencies
print_step "Checking dependencies..."

command -v node >/dev/null 2>&1 || { print_error "Node.js is required but not installed. Aborting."; exit 1; }
command -v npm >/dev/null 2>&1 || { print_error "npm is required but not installed. Aborting."; exit 1; }
command -v python3 >/dev/null 2>&1 || { print_error "Python 3 is required but not installed. Aborting."; exit 1; }

NODE_VERSION=$(node --version)
NPM_VERSION=$(npm --version)
PYTHON_VERSION=$(python3 --version)

print_success "Node.js is installed ($NODE_VERSION)"
print_success "npm is installed ($NPM_VERSION)"
print_success "Python 3 is installed ($PYTHON_VERSION)"

# Install Node.js dependencies
print_step "Installing Node.js dependencies..."
if npm install; then
    print_success "Node.js dependencies installed successfully"
else
    print_error "Failed to install Node.js dependencies"
    exit 1
fi

# Install Python dependencies
print_step "Installing Python dependencies..."
if pip3 install -r frontend/requirements.txt > /dev/null 2>&1; then
    print_success "Python dependencies installed successfully"
else
    print_warning "Some Python dependencies may not have installed correctly"
fi

# Check if DNA files exist
print_step "Checking DNA organism files..."

if [ -f "AdvancedConsciousness.dna" ]; then
    print_success "AdvancedConsciousness.dna found"
else
    print_warning "AdvancedConsciousness.dna not found"
fi

if [ -f "Tokenomics.dna" ]; then
    print_success "Tokenomics.dna found"
else
    print_error "Tokenomics.dna not found. This is required for tokenomics functionality."
    exit 1
fi

# Run tokenomics evolution
print_step "Running tokenomics evolution..."
print_evolution "Starting TokenomicsCore organism evolution..."

if npm run start:tokenomics; then
    print_success "Tokenomics evolution completed successfully!"
else
    print_error "Tokenomics evolution failed"
    exit 1
fi

# Check generated files
print_step "Checking generated files..."

GENERATED_FILES=(
    "tokenomics_state.json"
    "tokenomics_dashboard.json"
    "tokenomics_dashboard.html"
)

for file in "${GENERATED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "Generated: $file"
    else
        print_warning "Missing: $file"
    fi
done

# Start the web dashboard (optional)
print_step "Bootstrap complete! Available commands:"
echo ""
echo "  🚀 Start Streamlit Dashboard:"
echo "     streamlit run frontend/app.py"
echo ""
echo "  💰 Run Tokenomics Evolution:"
echo "     npm run start:tokenomics"
echo ""
echo "  🧬 Run Consciousness Evolution:"
echo "     npm run start"
echo ""
echo "  📊 View Tokenomics Dashboard:"
echo "     open tokenomics_dashboard.html"
echo ""
echo "  🌐 Serve Static Files:"
echo "     npm run serve"
echo ""

# Auto-start option
if [ "$1" = "--auto-start" ]; then
    print_step "Auto-starting Streamlit dashboard..."
    print_status "Dashboard will be available at http://localhost:8501"
    print_status "Press Ctrl+C to stop"
    streamlit run frontend/app.py
elif [ "$1" = "--serve-dashboard" ]; then
    print_step "Starting HTTP server for tokenomics dashboard..."
    print_status "Dashboard will be available at http://localhost:8000/tokenomics_dashboard.html"
    print_status "Press Ctrl+C to stop"
    python3 -m http.server 8000
else
    print_success "Bootstrap completed successfully!"
    echo ""
    print_status "Add --auto-start to automatically launch Streamlit"
    print_status "Add --serve-dashboard to serve the HTML dashboard"
fi