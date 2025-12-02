# DNA-Lang Enhanced CLI - Quick Reference Card

## 🚀 Installation
```bash
curl -fsSL https://raw.githubusercontent.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/main/install-dnalang.sh | bash
```

## 📋 Core Commands

### compile - Compile organism with QWC optimization
```bash
dna compile <organism.dna> [optimize] [target]

# Examples:
dna compile TestApp.dna                    # Basic compilation
dna compile TestApp.dna true               # With QWC optimization
dna compile TestApp.dna true production    # Production build
```

### evolve - Evolve organism with quantum targeting
```bash
dna evolve <organism> [optimize-for] [generations]

# Examples:
dna evolve TestApp                         # Default evolution
dna evolve TestApp latency                 # Optimize for latency
dna evolve TestApp latency 100             # 100 generations
dna evolve TestApp throughput 200          # Optimize throughput
```

### deploy - Deploy to cloud infrastructure
```bash
dna deploy <organism> [provider] [domain]

# Examples:
dna deploy SecureWebApp                    # Default (GCP)
dna deploy SecureWebApp gcp                # Google Cloud
dna deploy SecureWebApp aws myapp.io       # AWS with custom domain
dna deploy SecureWebApp azure analytics.cloud
```

## 🤖 Advanced Commands

### gpt - AI-powered assistance
```bash
dna gpt "<prompt>"

# Examples:
dna gpt "How do I optimize for throughput?"
dna gpt "What's the best cloud provider for genomics?"
dna gpt "Explain DNA-Lang genome structure"
dna gpt "Best practices for production deployment?"
```

### quantum - Quantum optimization
```bash
dna quantum <organism> [operation]

# Examples:
dna quantum TestApp optimize
dna quantum MyApp analyze
```

### telemetry - Real-time monitoring
```bash
dna telemetry

# Shows:
# - Session ID
# - Active organisms
# - CPU/Memory usage
# - System status
```

## 🎯 Common Workflows

### Development Workflow
```bash
# 1. Compile with optimization
dna compile MyApp.dna true development

# 2. Run quantum optimization
dna quantum MyApp optimize

# 3. Evolve for performance
dna evolve MyApp latency 100

# 4. Check system health
dna telemetry
```

### Production Deployment
```bash
# 1. Production compilation
dna compile MyApp.dna true production

# 2. Get GPT recommendations
dna gpt "Best practices for production deployment?"

# 3. Final evolution
dna evolve MyApp fitness 200

# 4. Deploy to cloud
dna deploy MyApp gcp myapp.com

# 5. Verify deployment
dna telemetry
```

### Genomic Analysis Pipeline
```bash
# 1. Compile genomic app
dna compile GenomicAnalyzer.dna true production

# 2. Get optimization advice
dna gpt "Optimizations for genomic analysis workloads?"

# 3. Quantum optimization
dna quantum GenomicAnalyzer optimize

# 4. Evolve for throughput
dna evolve GenomicAnalyzer throughput 500

# 5. Deploy with custom domain
dna deploy GenomicAnalyzer gcp genomics.dnalang.app
```

## 💡 Tips & Tricks

### Speed up compilation
```bash
dna compile MyApp.dna true production
# QWC optimization provides 10-40% performance boost
```

### Get context-aware help
```bash
# After compiling:
dna gpt "How can I improve the compilation I just ran?"

# After evolution:
dna gpt "Analyze my evolution results"
```

### Monitor in real-time
```bash
# In one terminal:
dna evolve MyApp throughput 1000

# In another terminal:
watch -n 1 dna telemetry
```

### Chain commands
```bash
dna compile MyApp.dna true production && \
dna quantum MyApp optimize && \
dna evolve MyApp latency 100 && \
dna deploy MyApp gcp
```

## 🔧 Configuration

### Environment Variables
```bash
export DNALANG_API="https://dnalang-quantum-portal-bh0krv51d.vercel.app"
export GPT_ENDPOINT="https://dnalang-qnet.vercel.app/api/gpt"
export DNALANG_HOME="$HOME/.dnalang"
```

### Session Files
```bash
~/.dnalang_session          # Session tracking
~/.dnalang_metrics.json     # Telemetry data
```

## 🆘 Help

### Get command help
```bash
dna help                    # Full help
dna                         # Also shows help
```

### Error troubleshooting
```bash
# GPT service issues:
dna gpt "test"              # Test GPT connection

# Telemetry issues:
pkill -f dnalang_telemetry  # Restart daemon
dna telemetry               # Restart automatically
```

## 📊 Output Colors

- 🔵 **Cyan**: Processing/Information
- 🟢 **Green**: Success/Completion
- 🟡 **Yellow**: Warnings/Optional
- 🔴 **Red**: Errors/Failures

## 🎁 Bonus Features

### Background telemetry daemon
Automatically starts and tracks metrics

### Session persistence
Commands share context across invocations

### Graceful degradation
Works offline with reduced features

### Cross-platform
Supports Linux, macOS, bash, zsh

## 📚 Documentation

- **Full Guide**: `docs/enhanced-cli-guide.md`
- **Examples**: `docs/enhanced-cli-examples.md`
- **Summary**: `ENHANCED_CLI_SUMMARY.md`
- **Node.js CLI**: `docs/cli-reference.md`

## 🔗 Quick Links

- **Install**: One-liner curl command
- **Help**: `dna help`
- **Test**: `dna compile TestApp.dna`
- **Monitor**: `dna telemetry`

---

**Print this card and keep it handy! 🧬**
