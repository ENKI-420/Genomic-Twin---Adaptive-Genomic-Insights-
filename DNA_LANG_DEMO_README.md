# DNA-Lang Autonomous Evolution Demo

This repository includes scripts that demonstrate autonomous DNA sequence evolution with GitHub repository management capabilities.

## Overview

The DNA-Lang Autonomous Evolution Demo showcases:

- 🧬 **Autonomous DNA Sequence Evolution**: Self-mutating genetic sequences
- 🚀 **GitHub Integration**: Automatic repository creation and management
- 📊 **Real-time Tracking**: Generation-based mutation tracking
- 🎨 **Color-coded Output**: Enhanced user experience with visual feedback
- 🔧 **Dependency Management**: Robust CLI tool checking
- 📝 **Git Integration**: Version control for evolutionary changes

## Scripts

### 1. `dna_lang_autonomous_evolution_demo.sh`

The main demo script that creates GitHub repositories and demonstrates autonomous evolution.

**Features:**
- Creates a new GitHub repository via GitHub CLI
- Generates DNA sequence files with evolutionary properties
- Creates Node.js evolution runner with autonomous mutation logic
- Commits and pushes changes to GitHub
- Provides comprehensive error handling and user feedback

**Requirements:**
- Git
- GitHub CLI (`gh`) with authentication
- Node.js and npm

**Usage:**
```bash
# Run with automatic repository name generation
./dna_lang_autonomous_evolution_demo.sh

# Run with custom repository name
./dna_lang_autonomous_evolution_demo.sh --repo-name my-custom-repo

# Show help
./dna_lang_autonomous_evolution_demo.sh --help
```

### 2. `dna_lang_test_demo.sh`

A local test version that runs without GitHub authentication requirements.

**Features:**
- Local repository creation for testing
- Same autonomous evolution logic as main script
- Git commit tracking without remote push
- Perfect for testing and development

**Requirements:**
- Node.js and npm (Git not strictly required)

**Usage:**
```bash
# Run local test demo
./dna_lang_test_demo.sh

# Show help
./dna_lang_test_demo.sh --help
```

## Evolution Process

The autonomous evolution follows this process:

1. **Initial Generation**: Base DNA sequence created with specific patterns
2. **Mutation Cycles**: Random base substitutions (A↔T, C↔G, etc.)
3. **Tracking**: Each generation tracked with timestamps and mutation counts
4. **Logging**: Complete evolution history maintained in sequence files
5. **Version Control**: Git commits for each significant evolutionary step

## Generated Repository Structure

When the script creates a repository, it includes:

```
repository-name/
├── README.md                 # Comprehensive documentation
├── package.json             # Node.js project configuration
├── evolution_runner.js      # Autonomous evolution engine
├── dna_sequence.txt         # Evolving DNA sequence file
└── .gitignore              # Node.js gitignore template
```

## Color-Coded Output

The scripts use color-coded output for enhanced user experience:

- 🔵 **[INFO]** - General information (Blue)
- 🟢 **[SUCCESS]** - Successful operations (Green)
- 🟡 **[WARNING]** - Warnings and non-critical issues (Yellow)
- 🔴 **[ERROR]** - Errors requiring attention (Red)
- 🟣 **[STEP]** - Current operation steps (Purple)
- 🔷 **[EVOLUTION]** - Evolution-specific events (Cyan)

## Error Handling

Both scripts include comprehensive error handling:

- **Dependency Checking**: Validates required CLI tools before execution
- **Authentication Verification**: Ensures GitHub CLI is authenticated (main script)
- **Repository Existence**: Gracefully handles existing repositories
- **Cleanup**: Automatic cleanup of temporary files on exit
- **User Guidance**: Clear error messages with solution suggestions

## Safety Features

- **Non-destructive**: Scripts ask before deleting existing repositories
- **Temporary Directories**: All operations use temporary directories initially
- **Error Recovery**: Comprehensive error trapping with cleanup
- **Validation**: Input validation and sanitization

## Example Output

```bash
╔════════════════════════════════════════════════════════════╗
║           🧬 DNA-Lang Autonomous Evolution Demo 🧬          ║
║                                                            ║
║  Demonstrates autonomous code evolution with GitHub        ║
║  repository management and real-time collaboration        ║
╚════════════════════════════════════════════════════════════╝

[STEP] Checking dependencies...
[SUCCESS] Git is installed (2.50.1)
[SUCCESS] GitHub CLI is installed (2.76.0)
[SUCCESS] Node.js is installed (v20.19.4)
[SUCCESS] npm is installed (10.8.2)
[SUCCESS] All dependencies are satisfied!

[STEP] Creating GitHub repository: dna-lang-evolution-20250726_032319-abc123
[SUCCESS] Repository created: https://github.com/user/dna-lang-evolution-20250726_032319-abc123

[EVOLUTION] Evolution Cycle 1
🧬 Starting DNA Evolution Process...
⚡ 9 mutations detected! Updating sequence...
✅ DNA sequence evolved successfully!
📊 Evolution Stats:
   Generation: 2
   Total Mutations: 9
```

## Integration with DNA-Lang Platform

These scripts are designed to integrate with the broader DNA-Lang platform:

- Compatible with existing environment configurations
- Follows DNA-Lang naming conventions and patterns
- Supports the platform's multi-environment architecture
- Designed for genomic research and educational use

## Contributing

When modifying the scripts:

1. Maintain color-coded output consistency
2. Preserve error handling patterns
3. Ensure backward compatibility
4. Test both scripts thoroughly
5. Update documentation for any new features

## Troubleshooting

### Common Issues

**GitHub Authentication Failed**
```bash
# Solution: Authenticate with GitHub CLI
gh auth login
```

**Missing Dependencies**
```bash
# Install Node.js from https://nodejs.org/
# Install GitHub CLI from https://cli.github.com/
# Install Git from https://git-scm.com/
```

**Repository Already Exists**
- Script will prompt to delete and recreate
- Choose 'y' to proceed or 'N' to exit

**Permission Denied**
```bash
# Make scripts executable
chmod +x dna_lang_autonomous_evolution_demo.sh
chmod +x dna_lang_test_demo.sh
```

## License

This demo is part of the DNA-Lang Platform and follows the same licensing terms as the main project.