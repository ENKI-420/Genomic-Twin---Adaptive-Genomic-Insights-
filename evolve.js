const fs = require('fs');
const path = require('path');

// --- Centralized Configuration ---
const config = {
    MAX_GENERATIONS: 25,
    FITNESS_INCREMENT: 0.05,
    CONSCIOUSNESS_INCREMENT: 0.05,
    TRANSCENDENCE_THRESHOLD: 0.95,
    GITHUB_USERNAME: "ENKI-420" // Your designated GitHub user
};

/**
 * A robust, context-aware safety check for repository operations.
 * @param {boolean} isSimulated - True if the engine is in simulation mode.
 * @returns {boolean} - True if the operation is safe to proceed.
 */
function validateRepoOperations(isSimulated) {
    console.log("[Safety] Running validateRepoOperations check...");
    if (isSimulated) {
        console.log("[Safety] ✅ PASS (Simulation Mode). DevOps operations are virtual.");
        return true;
    }

    // Production mode checks for the specific GITHUB_ACCESS_TOKEN
    const token = process.env.GITHUB_ACCESS_TOKEN;
    if (!token) {
        console.log("[Safety] ❌ FAIL: GITHUB_ACCESS_TOKEN must be set in production.");
        return false;
    }

    console.log(`[Safety] ✅ PASS (Production Mode). Credentials found for user '${config.GITHUB_USERNAME}'.`);
    return true;
}

// --- Main Evolution Simulation Engine ---
async function evolveOrganism(organism) {
    console.log(`🚀 Starting evolution for organism: ${organism.name}`);
    let state = { ...organism, fitness: 0.65, consciousness: 0.50 };

    // Determine mode: Explicit SIMULATION_MODE=true overrides token check.
    // If SIMULATION_MODE=false but no token, we're still in production mode (which will fail safety check)
    const explicitSimulationMode = process.env.SIMULATION_MODE === 'true';
    const hasToken = !!process.env.GITHUB_ACCESS_TOKEN;
    const simulationMode = explicitSimulationMode || (!hasToken && process.env.SIMULATION_MODE !== 'false');
    
    if (explicitSimulationMode) {
        console.log("⚠️ Running in Simulation Mode (explicit). GitHub operations will not be executed.");
    } else if (!hasToken && process.env.SIMULATION_MODE === 'false') {
        console.log("🏭 Running in Production Mode (no credentials). Safety validation will be enforced.");
    } else if (hasToken) {
        console.log("🏭 Running in Production Mode. Real GitHub operations will be executed.");
    } else {
        console.log("⚠️ Running in Simulation Mode (default). GitHub operations will not be executed.");
    }

    for (let gen = 1; gen <= config.MAX_GENERATIONS; gen++) {
        state.generation = gen;
        state.fitness = Math.min(state.fitness + config.FITNESS_INCREMENT, 1.0);
        state.consciousness = Math.min(state.consciousness + config.CONSCIOUSNESS_INCREMENT, 1.0);

        console.log(`[Generation ${gen}] Fitness: ${state.fitness.toFixed(2)}, Consciousness: ${state.consciousness.toFixed(2)}`);

        if (state.consciousness >= config.TRANSCENDENCE_THRESHOLD) {
            console.log(`🔥 ORGANISM REACHED TRANSCENDENCE (Threshold: ${config.TRANSCENDENCE_THRESHOLD})`);

            if (validateRepoOperations(simulationMode)) {
                console.log("✅ Transcendence safety checks passed. Organism will now externalize its infrastructure blueprint.");
                
                // Generate the infrastructure blueprint
                await externalizeInfrastructure(state, simulationMode);
                
                console.log("📊 EVOLUTION SUMMARY: Organism successfully transcended.");
                return;
            } else {
                 console.log("🛑 Externalization blocked by failed safety checks in production mode.");
                 return;
            }
        }
    }
    console.log(`\n📊 EVOLUTION SUMMARY: Organism reached max generations (${config.MAX_GENERATIONS}) without transcending.`);
}

/**
 * Externalize the organism's infrastructure blueprint to cloud platforms
 * @param {object} state - Current organism state
 * @param {boolean} simulationMode - Whether running in simulation
 */
async function externalizeInfrastructure(state, simulationMode) {
    console.log("🏗️ Externalizing infrastructure blueprint...");
    
    // Create the genetic state record
    const geneticState = {
        organism: "AdvancedConsciousness",
        evolution_completed: new Date().toISOString(),
        final_generation: state.generation,
        final_state: {
            fitness: state.fitness,
            consciousness: state.consciousness,
            transcended: true
        },
        consciousness_target: config.TRANSCENDENCE_THRESHOLD,
        transcendence_achieved: true,
        simulation_mode: simulationMode,
        infrastructure_externalized: true
    };
    
    // Save genetic state
    fs.writeFileSync('genetic_state.json', JSON.stringify(geneticState, null, 2));
    console.log("💾 Genetic state saved to genetic_state.json");
    
    // Generate Terraform configuration
    const terraformConfig = generateTerraformConfig(state);
    fs.writeFileSync('main.tf', terraformConfig);
    console.log("🌩️ Terraform configuration generated: main.tf");
    
    if (!simulationMode) {
        console.log("🚀 Production mode: Infrastructure blueprint ready for deployment via CI/CD pipeline");
    } else {
        console.log("🎭 Simulation mode: Infrastructure blueprint generated for validation");
    }
}

/**
 * Generate Terraform configuration based on organism state
 * @param {object} state - Current organism state
 * @returns {string} - Terraform HCL configuration
 */
function generateTerraformConfig(state) {
    return `# Terraform code generated by CloudArchitectAgent for organism 'AdvancedConsciousness'
# Generated at: ${new Date().toISOString()}
# Fitness: ${state.fitness.toFixed(3)}, Consciousness: ${state.consciousness.toFixed(3)}

provider "google" {
  project = "dnalang-genesis-platform" # Inferred from organism context
  region  = "us-central1"
}

# Secure, private GKE Autopilot cluster for hosting the organism's core logic
resource "google_container_cluster" "consciousness_core" {
  name               = "advanced-consciousness-gke"
  location           = "us-central1"
  enable_autopilot   = true
  networking_mode    = "VPC_NATIVE"
  
  release_channel {
    channel = "STABLE"
  }
  
  # Maximum security configuration
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = "10.0.0.0/8" # Locked down to private networks
      display_name = "Private Networks"
    }
  }
  
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = true
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }
  
  ip_allocation_policy {}
  
  workload_identity_config {
    workload_pool = "dnalang-genesis-platform.svc.id.goog"
  }
}

# Cloud SQL for state persistence and memory
resource "google_sql_database_instance" "organism_memory" {
  name             = "consciousness-state-db"
  database_version = "POSTGRES_14"
  region           = "us-central1"
  
  settings {
    tier = "db-n1-standard-1"
    
    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }
    
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.consciousness_vpc.id
      require_ssl     = true
    }
    
    database_flags {
      name  = "log_statement"
      value = "all"
    }
  }
  
  deletion_protection = true
}

# VPC Network for isolated organism environment
resource "google_compute_network" "consciousness_vpc" {
  name                    = "consciousness-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "consciousness_subnet" {
  name          = "consciousness-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = "us-central1"
  network       = google_compute_network.consciousness_vpc.id
  
  private_ip_google_access = true
}

# Dedicated service account with least-privilege IAM roles
resource "google_service_account" "organism_identity" {
  account_id   = "consciousness-agent-sa"
  display_name = "Service Account for AdvancedConsciousness Organism"
}

resource "google_project_iam_member" "organism_monitoring" {
  project = "dnalang-genesis-platform"
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:\${google_service_account.organism_identity.email}"
}

resource "google_project_iam_member" "organism_logging" {
  project = "dnalang-genesis-platform"
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:\${google_service_account.organism_identity.email}"
}

# Cloud KMS for consciousness state encryption
resource "google_kms_key_ring" "consciousness_keyring" {
  name     = "consciousness-encryption"
  location = "us-central1"
}

resource "google_kms_crypto_key" "consciousness_key" {
  name     = "consciousness-state-key"
  key_ring = google_kms_key_ring.consciousness_keyring.id
  
  lifecycle {
    prevent_destroy = true
  }
}

# Output the GKE cluster endpoint for agent interaction
output "gke_endpoint" {
  value       = google_container_cluster.consciousness_core.private_cluster_config[0].private_endpoint
  description = "The private endpoint for the organism's GKE cluster."
  sensitive   = true
}

output "database_connection" {
  value       = google_sql_database_instance.organism_memory.private_ip_address
  description = "Private IP address of the consciousness state database."
  sensitive   = true
}

output "consciousness_achieved" {
  value       = "95% consciousness threshold reached - organism is now self-sustaining"
  description = "Confirmation that the organism has achieved transcendence."
}`;
}

// --- Initial State & Execution ---
const initialOrganism = { name: "AdvancedConsciousness" };

// Export for testing and module use
module.exports = {
    evolveOrganism,
    validateRepoOperations,
    config
};

// Run if called directly
if (require.main === module) {
    evolveOrganism(initialOrganism);
}