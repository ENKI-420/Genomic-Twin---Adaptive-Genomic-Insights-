#!/usr/bin/env bash
#
# DNA-Lang One-Liner Installer
# Install the enhanced DNA-Lang CLI with GPT integration
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/main/install-dnalang.sh | bash
#   
# Or:
#   wget -qO- https://raw.githubusercontent.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/main/install-dnalang.sh | bash
#

set -e

# Colors
BOLD=$(tput bold 2>/dev/null || echo "")
GREEN=$(tput setaf 2 2>/dev/null || echo "")
CYAN=$(tput setaf 6 2>/dev/null || echo "")
YELLOW=$(tput setaf 3 2>/dev/null || echo "")
RED=$(tput setaf 1 2>/dev/null || echo "")
NC=$(tput sgr0 2>/dev/null || echo "")

echo "${BOLD}${CYAN}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🧬  DNA-Lang Quantum Orchestrator Installer  🧬      ║
║                                                           ║
║              With GPT-NLP Integration                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo "${NC}"

# Check dependencies
check_dependencies() {
  echo "${CYAN}Checking dependencies...${NC}"
  
  local missing_deps=()
  
  if ! command -v curl &> /dev/null; then
    missing_deps+=("curl")
  fi
  
  if ! command -v git &> /dev/null; then
    missing_deps+=("git")
  fi
  
  if ! command -v node &> /dev/null; then
    echo "${YELLOW}⚠️  Node.js not found. Installing Node.js is recommended for full functionality.${NC}"
  fi
  
  if ! command -v jq &> /dev/null; then
    echo "${YELLOW}⚠️  jq not found. Installing jq is recommended for JSON processing.${NC}"
  fi
  
  if [ ${#missing_deps[@]} -ne 0 ]; then
    echo "${RED}❌ Missing required dependencies: ${missing_deps[*]}${NC}"
    echo "Please install the missing dependencies and try again."
    exit 1
  fi
  
  echo "${GREEN}✅ All required dependencies found${NC}"
}

# Install DNA-Lang CLI
install_dnalang() {
  local install_dir="${DNALANG_HOME:-$HOME/.dnalang}"
  
  echo ""
  echo "${CYAN}📦 Installing DNA-Lang to: $install_dir${NC}"
  
  # Create installation directory
  mkdir -p "$install_dir"
  cd "$install_dir"
  
  # Clone or update repository
  if [ -d "$install_dir/.git" ]; then
    echo "${CYAN}Updating existing installation...${NC}"
    git pull --quiet
  else
    echo "${CYAN}Cloning DNA-Lang repository...${NC}"
    git clone --quiet https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-.git .
  fi
  
  # Make CLI scripts executable
  chmod +x bin/dnalang-cli.sh 2>/dev/null || true
  chmod +x bin/dna 2>/dev/null || true
  
  # Install Node.js dependencies if Node is available
  if command -v npm &> /dev/null; then
    echo "${CYAN}Installing Node.js dependencies...${NC}"
    npm install --silent &> /dev/null || echo "${YELLOW}⚠️  npm install failed, continuing...${NC}"
  fi
  
  echo "${GREEN}✅ DNA-Lang installed successfully${NC}"
}

# Setup PATH
setup_path() {
  local install_dir="${DNALANG_HOME:-$HOME/.dnalang}"
  local shell_rc=""
  
  # Detect shell configuration file
  if [ -n "$BASH_VERSION" ]; then
    if [ -f "$HOME/.bashrc" ]; then
      shell_rc="$HOME/.bashrc"
    elif [ -f "$HOME/.bash_profile" ]; then
      shell_rc="$HOME/.bash_profile"
    fi
  elif [ -n "$ZSH_VERSION" ]; then
    shell_rc="$HOME/.zshrc"
  fi
  
  if [ -n "$shell_rc" ]; then
    # Check if PATH is already configured
    if ! grep -q "DNALANG_HOME" "$shell_rc" 2>/dev/null; then
      echo ""
      echo "${CYAN}Adding DNA-Lang to PATH...${NC}"
      
      cat >> "$shell_rc" << EOF

# DNA-Lang Configuration
export DNALANG_HOME="$install_dir"
export PATH="\$DNALANG_HOME/bin:\$PATH"
alias dna="$install_dir/bin/dnalang-cli.sh"
alias dna-node="node $install_dir/bin/dna"
EOF
      
      echo "${GREEN}✅ Added to $shell_rc${NC}"
      echo "${YELLOW}Please run: source $shell_rc${NC}"
    else
      echo "${GREEN}✅ PATH already configured${NC}"
    fi
  fi
  
  # Create symlink for current session
  if [ -w "/usr/local/bin" ]; then
    ln -sf "$install_dir/bin/dnalang-cli.sh" /usr/local/bin/dna 2>/dev/null && \
      echo "${GREEN}✅ Created symlink in /usr/local/bin${NC}" || true
  fi
}

# Verify installation
verify_installation() {
  local install_dir="${DNALANG_HOME:-$HOME/.dnalang}"
  
  echo ""
  echo "${CYAN}Verifying installation...${NC}"
  
  if [ -x "$install_dir/bin/dnalang-cli.sh" ]; then
    echo "${GREEN}✅ Enhanced bash CLI installed${NC}"
  fi
  
  if [ -x "$install_dir/bin/dna" ]; then
    echo "${GREEN}✅ Node.js CLI installed${NC}"
  fi
  
  if [ -f "$install_dir/package.json" ]; then
    echo "${GREEN}✅ Package configuration found${NC}"
  fi
}

# Show completion message
show_completion() {
  local install_dir="${DNALANG_HOME:-$HOME/.dnalang}"
  
  echo ""
  echo "${BOLD}${GREEN}"
  cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        ✅  Installation Complete!  ✅                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
  echo "${NC}"
  
  echo "🧬 DNA-Lang Quantum Orchestrator is ready to use!"
  echo ""
  echo "Quick Start:"
  echo "  ${CYAN}# Enhanced bash CLI (with GPT & QWC)${NC}"
  echo "  $install_dir/bin/dnalang-cli.sh help"
  echo ""
  echo "  ${CYAN}# Node.js CLI${NC}"
  echo "  node $install_dir/bin/dna --help"
  echo ""
  echo "  ${CYAN}# Or use the alias (after sourcing your shell rc):${NC}"
  echo "  dna help"
  echo ""
  echo "Examples:"
  echo "  ${YELLOW}dna compile TestApp.dna true production${NC}"
  echo "  ${YELLOW}dna evolve TestApp latency 100${NC}"
  echo "  ${YELLOW}dna deploy SecureWebApp gcp dnalang.app${NC}"
  echo "  ${YELLOW}dna gpt 'How do I optimize for throughput?'${NC}"
  echo "  ${YELLOW}dna quantum MyApp optimize${NC}"
  echo ""
  echo "Documentation: https://dnalang.dev"
  echo ""
}

# Main installation flow
main() {
  check_dependencies
  install_dnalang
  setup_path
  verify_installation
  show_completion
}

# Run installer
main "$@"
