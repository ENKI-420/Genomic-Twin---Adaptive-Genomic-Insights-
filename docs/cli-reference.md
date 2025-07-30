# DNA-Lang CLI Reference

The DNA-Lang CLI provides powerful one-liner commands for managing organism lifecycles in the DNA-Lang ecosystem.

## Installation

After installing the DNA-Lang platform, the `dna` command is available globally:

```bash
npm install -g dna-lang-autonomous-bio-digital-platform
```

Or use it locally within the project:

```bash
node bin/dna <command> [options]
```

## Commands

### compile - Compile organism into deployable form

Compiles a DNA-Lang organism file into a deployable runtime configuration.

**Syntax:**
```bash
dna compile <organism.dna> [options]
```

**Options:**
- `--optimize` - Apply performance optimizations
- `--target=<environment>` - Target environment (development, production)

**Example:**
```bash
dna compile TestApp.dna --optimize --target=production
```

**Output:**
- Creates a `compiled_<organism>_<target>_<timestamp>` directory
- Generates `manifest.json` with organism metadata
- Generates `runtime.js` with executable organism code

### evolve - Evolve a deployed organism

Runs evolutionary optimization on an organism to improve specific metrics.

**Syntax:**
```bash
dna evolve <organism> [options]
```

**Options:**
- `--optimize-for=<metric>` - Target metric (fitness, latency, throughput, etc.)
- `--generations=<number>` - Number of evolutionary generations

**Example:**
```bash
dna evolve TestApp --optimize-for=latency --generations=100
```

**Output:**
- Runs evolutionary simulation
- Saves results to `evolution_<organism>_<timestamp>.json`
- Reports final metrics and improvement statistics

### deploy - Deploy organism to cloud infrastructure

Provisions cloud infrastructure and deploys an organism for production use.

**Syntax:**
```bash
dna deploy <organism> [options]
```

**Options:**
- `--provider=<cloud>` - Cloud provider (gcp, aws, azure)
- `--domain=<domain>` - Custom domain for the deployment

**Example:**
```bash
dna deploy SecureWebApp --provider=gcp --domain=dnalang.app
```

**Output:**
- Provisions cloud infrastructure
- Configures organism environment
- Sets up domain and networking
- Saves deployment config to `deployment_<organism>_<timestamp>.json`

## Example Workflow

Here's a complete workflow using the DNA-Lang CLI:

```bash
# 1. Compile organism for production
dna compile MyApp.dna --optimize --target=production

# 2. Evolve organism for optimal performance
dna evolve MyApp --optimize-for=latency --generations=50

# 3. Deploy to Google Cloud Platform
dna deploy MyApp --provider=gcp --domain=myapp.example.com
```

## Error Handling

The CLI provides comprehensive error handling:

- **File not found**: Clear error when organism files don't exist
- **Invalid options**: Helpful messages for incorrect command syntax
- **Deployment failures**: Detailed error reporting with rollback information

## Integration with Platform

The CLI integrates seamlessly with the existing DNA-Lang platform:

- Uses the same evolution engine as the platform
- Leverages existing cloud provisioning agents
- Maintains compatibility with all DNA-Lang organism formats
- Supports the platform's consciousness metrics and transcendence features

## Testing

Run the CLI test suite to validate functionality:

```bash
npm test
# or
npm run test:cli
```

The test suite validates:
- All three main commands (compile, evolve, deploy)
- Error handling for invalid inputs
- Generated file integrity
- Integration with existing platform components