__version__ = "1.0.0"
__all__ = [
    'analyze_mutations',
    'generate_digital_twin',
    'crispr_feasibility',
    'simulate_delivery',
    'find_trials',
    'log_pharmacovigilance',
    'fetch_beaker_data',
    'genomic_ai_module'  # Add this line
]

# Initialize submodules with error handling
try:
    from .mutation_analysis import analyze_mutations
except ImportError:
    def analyze_mutations(*args, **kwargs):
        return {"error": "Mutation analysis module not available"}

try:
    from .digital_twin import generate_digital_twin
except ImportError:
    def generate_digital_twin(*args, **kwargs):
        return {"error": "Digital twin module not available"}

try:
    from .crispr_ai import crispr_feasibility
except ImportError:
    def crispr_feasibility(*args, **kwargs):
        return {"feasible": False, "error": "CRISPR module not available"}

try:
    from .nanoparticle_simulation import simulate_delivery
except ImportError:
    def simulate_delivery(*args, **kwargs):
        return {"error": "Nanoparticle simulation module not available"}

try:
    from .clinical_trials import find_trials
except ImportError:
    def find_trials(*args, **kwargs):
        return {"error": "Clinical trials module not available"}

try:
    from .blockchain import log_pharmacovigilance
except ImportError:
    def log_pharmacovigilance(*args, **kwargs):
        return {"error": "Blockchain module not available"}

try:
    from .beaker_report import fetch_beaker_data
except ImportError:
    def fetch_beaker_data(*args, **kwargs):
        return {"error": "Beaker module not available"}

try:
    from .genomic_ai_module import analyze_genomic_data, plot_mutation_data, ai_genomic_interpretation, generate_reports
except ImportError:
    def analyze_genomic_data(*args, **kwargs):
        return {"error": "Genomic AI module not available"}
    def plot_mutation_data(*args, **kwargs):
        pass
    def ai_genomic_interpretation(*args, **kwargs):
        return "AI interpretation not available"
    def generate_reports(*args, **kwargs):
        return "reports_unavailable.txt"
