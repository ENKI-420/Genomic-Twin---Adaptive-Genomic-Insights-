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

# Initialize submodules
from .mutation_analysis import analyze_mutations
from .digital_twins import generate_digital_twin
from .crispr_ai import crispr_feasibility
from .nanoparticle_simulation import simulate_delivery
from .clinical_trials import find_trials
from .blockchain import log_pharmacovigilance
from .beaker_report import fetch_beaker_data
from .genomic_ai_module import analyze_genomic_data, plot_mutation_data, ai_genomic_interpretation, generate_reports
