# DNA-Lang Enhanced CLI with GPT Integration

## Overview

The DNA-Lang Enhanced CLI brings advanced capabilities including GPT-NLP integration, Quantum-Wave Collapse (QWC) optimization, and real-time telemetry to the DNA-Lang ecosystem. This enhanced version works alongside the existing Node.js CLI to provide a complete development experience.

## 🚀 Quick Install

### One-Liner Installation

Install DNA-Lang with all enhanced features using a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/main/install-dnalang.sh | bash
```

Or with wget:

```bash
wget -qO- https://raw.githubusercontent.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/main/install-dnalang.sh | bash
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-.git
cd Genomic-Twin---Adaptive-Genomic-Insights-

# Make scripts executable
chmod +x bin/dnalang-cli.sh
chmod +x install-dnalang.sh

# Add to your PATH (optional)
echo 'export PATH="$PATH:$(pwd)/bin"' >> ~/.bashrc
echo 'alias dna="$(pwd)/bin/dnalang-cli.sh"' >> ~/.bashrc
source ~/.bashrc
```

## 🧬 Features

### 1. GPT-NLP Integration

Query GPT directly from the command line for AI-powered assistance with your DNA-Lang projects:

```bash
# Get general advice
dna gpt "How do I optimize for throughput?"

# Context-aware suggestions
dna gpt "What's the best cloud provider for genomics workloads?"

# Debugging help
dna gpt "Why is my organism's evolution slow?"
```

The GPT integration provides:
- Context-aware responses based on DNA-Lang ecosystem
- Session tracking for coherent conversations
- Integration with compilation, evolution, and deployment workflows

### 2. Quantum-Wave Collapse (QWC) Optimization

Leverage quantum-inspired optimization algorithms:

```bash
# Optimize an organism using QWC
dna quantum TestApp optimize

# QWC is automatically applied during compilation
dna compile MyApp.dna true production

# QWC optimization during evolution
dna evolve MyApp latency 100
```

QWC optimization provides:
- 10-40% performance improvements
- Reduced compilation times
- Better evolution convergence
- Optimized quantum state persistence

### 3. Real-Time Telemetry

Monitor your DNA-Lang organisms with real-time metrics:

```bash
# Show telemetry dashboard
dna telemetry
```

Features:
- Background telemetry daemon
- CPU and memory monitoring
- Session tracking
- Organism health metrics

## 📖 Command Reference

### Core Commands

#### compile
Compile organisms with enhanced optimization:

```bash
dna compile <organism.dna> [optimize] [target]

# Examples:
dna compile TestApp.dna true production
dna compile MyApp.dna false development
```

Parameters:
- `organism.dna`: Path to organism file (required)
- `optimize`: Enable QWC optimization (true/false, default: false)
- `target`: Target environment (development/production, default: development)

#### evolve
Evolve organisms with quantum optimization:

```bash
dna evolve <organism> [optimize-for] [generations]

# Examples:
dna evolve TestApp latency 100
dna evolve MyApp throughput 200
dna evolve SecureApp fitness 50
```

Parameters:
- `organism`: Organism name (required)
- `optimize-for`: Optimization target (latency/throughput/fitness, default: latency)
- `generations`: Number of evolution cycles (default: 100)

#### deploy
Deploy organisms to cloud infrastructure:

```bash
dna deploy <organism> [provider] [domain]

# Examples:
dna deploy SecureWebApp gcp dnalang.app
dna deploy MyService aws myapp.io
dna deploy Analytics azure analytics.cloud
```

Parameters:
- `organism`: Organism name (required)
- `provider`: Cloud provider (gcp/aws/azure, default: gcp)
- `domain`: Custom domain (default: dnalang.app)

### Advanced Commands

#### gpt
Query GPT-NLP for assistance:

```bash
dna gpt <prompt>

# Examples:
dna gpt "How do I optimize for throughput?"
dna gpt "What's the best strategy for scaling?"
dna gpt "Explain DNA-Lang genome structure"
```

#### quantum
Run quantum optimization directly:

```bash
dna quantum <organism> [operation]

# Examples:
dna quantum TestApp optimize
dna quantum MyApp analyze
```

#### telemetry
Display real-time telemetry dashboard:

```bash
dna telemetry
```

## 🔧 Configuration

### Environment Variables

The enhanced CLI uses the following environment variables:

```bash
# API endpoints
export DNALANG_API="https://dnalang-quantum-portal-bh0krv51d.vercel.app"
export GPT_ENDPOINT="https://dnalang-qnet.vercel.app/api/gpt"

# Installation directory
export DNALANG_HOME="$HOME/.dnalang"

# Vercel project
export VERCEL_PROJECT="dnalang-ibm-quantum-organisms"
```

### Session Management

Sessions are automatically created and persisted in `~/.dnalang_session`:

```bash
# View current session
cat ~/.dnalang_session

# View metrics
cat ~/.dnalang_metrics.json
```

## 📊 Complete Workflow Example

Here's a complete workflow demonstrating all features:

```bash
# 1. Create and compile an organism with QWC optimization
dna compile MyGenomicApp.dna true production

# 2. Get GPT suggestions for optimization
dna gpt "What optimizations should I apply for genomic analysis?"

# 3. Run quantum optimization
dna quantum MyGenomicApp optimize

# 4. Evolve the organism
dna evolve MyGenomicApp throughput 200

# 5. Check telemetry
dna telemetry

# 6. Deploy to production
dna deploy MyGenomicApp gcp genomics.dnalang.app

# 7. Get post-deployment recommendations from GPT
dna gpt "Best practices for monitoring genomic analysis in production?"
```

## 🆚 Comparison: Enhanced CLI vs Node.js CLI

| Feature | Enhanced Bash CLI | Node.js CLI |
|---------|------------------|-------------|
| Core Commands | ✅ | ✅ |
| GPT Integration | ✅ | ❌ |
| QWC Optimization | ✅ | ❌ |
| Real-time Telemetry | ✅ | ❌ |
| Quantum Computing | ✅ | ❌ |
| Background Daemon | ✅ | ❌ |
| Session Persistence | ✅ | ❌ |
| Detailed Testing | ❌ | ✅ |
| npm Integration | ❌ | ✅ |

**Recommendation**: Use the enhanced bash CLI for interactive development and the Node.js CLI for scripting and CI/CD pipelines.

## 🐛 Troubleshooting

### GPT Service Unavailable

If GPT queries return errors:

```bash
# Check internet connectivity
curl -I https://dnalang-qnet.vercel.app

# Verify API endpoint
echo $GPT_ENDPOINT
```

### Telemetry Not Working

If telemetry doesn't show data:

```bash
# Stop the telemetry daemon
pkill -f dnalang_telemetry

# Restart by running any command
dna telemetry
```

### Session Issues

If session tracking fails:

```bash
# Reset session
rm ~/.dnalang_session

# Create new session
dna telemetry
```

## 📚 Additional Resources

- [Main CLI Reference](./cli-reference.md) - Node.js CLI documentation
- [DNA-Lang Tutorial](https://dnalang.dev/tutorial) - Getting started guide
- [API Documentation](https://dnalang.dev/api) - Complete API reference
- [Examples](../examples/) - Sample organisms and workflows

## 🤝 Integration with Existing Tools

The enhanced CLI works seamlessly with:

- **Node.js CLI**: Use `node bin/dna` for Node.js version
- **npm Scripts**: All npm scripts remain functional
- **CI/CD**: Both CLIs can be used in automation
- **IDE Integration**: Works with any terminal-based IDE

## 🔐 Security Notes

- Session IDs are locally generated and stored
- GPT queries include session context but no sensitive data
- Telemetry data is stored locally in `~/.dnalang_metrics.json`
- Cloud credentials are managed through standard provider tools

## 📝 License

MIT License - see [LICENSE](../LICENSE) for details.
