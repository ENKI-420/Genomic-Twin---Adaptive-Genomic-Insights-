// --- Interfaces for Core Quantum/Genetics/Visualization API ---
export interface Allele {
  id: string;
  gene: string;
  value: number;
}

export interface QuantumCircuit {
  id: string;
  qubits: number;
  gates: string[];
}

export interface SimulationResult {
  telemetry: Record<string, any>;
  state: Record<string, any>;
}

export interface DNALangModule {
  id: string;
  circuit: QuantumCircuit;
  metadata: Record<string, any>;
}

export interface BenchmarkResult {
  fidelity: number;
  runtime: number;
  details: string;
}

export interface Visualization3D {
  meshData: string;
  audioStream: string;
}

// --- Service Class for Quantum/Genetics API ---
export class QuantumDNAApiService {
  constructor(private baseUrl: string, private apiKey: string) {}

  private async post<TReq, TRes>(path: string, data: TReq): Promise<TRes> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`API call failed: ${response.statusText}`);
    }

    return (await response.json()) as TRes;
  }

  /** Performs mutation on a list of alleles. */
  mutateAlleles(alleles: Allele[]): Promise<Allele[]> {
    return this.post('/genetics/mutate', alleles);
  }

  /** Performs crossover between two parent allele sets. */
  crossoverAlleles(parentA: Allele[], parentB: Allele[]): Promise<Allele[]> {
    return this.post('/genetics/crossover', { parentA, parentB });
  }

  /** Simulates a quantum circuit and returns the final state and telemetry. */
  simulateCircuit(circuit: QuantumCircuit): Promise<SimulationResult> {
    return this.post('/simulation/run', circuit);
  }

  /** Uploads a DNALang module for decentralized package management. */
  uploadModule(module: DNALangModule): Promise<string> {
    return this.post('/package/upload', module);
  }

  /** Fetches a DNALang module by ID. */
  fetchModule(moduleId: string): Promise<DNALangModule> {
    // Note: GET method requires fetch/query parameter handling
    return fetch(`${this.baseUrl}/package/fetch?moduleId=${moduleId}`, { 
      headers: { 'X-API-Key': this.apiKey } 
    }).then(res => {
      if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
      return res.json();
    }) as Promise<DNALangModule>;
  }

  /** Runs a benchmark suite against an uploaded module. */
  runBenchmark(moduleId: string, benchmarkSuite: string): Promise<BenchmarkResult> {
    return this.post('/benchmark/run', { moduleId, benchmarkSuite });
  }

  /** Renders a 3D visualization of the quantum chromosome/module. */
  renderChromosome(module: DNALangModule): Promise<Visualization3D> {
    return this.post('/visualization/render', module);
  }
}
