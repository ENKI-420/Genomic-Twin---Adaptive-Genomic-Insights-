import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple

class NanoparticleDeliverySimulator:
    def __init__(self, dose: float, elimination_rate: float, 
                distribution: Dict[str, float], size: float = 100, 
                charge: float = -20):
        """
        Initialize nanoparticle simulation parameters
        
        :param dose: Initial dose in mg/kg
        :param elimination_rate: Elimination rate constant (1/hours)
        :param distribution: Organ distribution percentages (must sum to 100)
        :param size: Nanoparticle diameter in nm
        :param charge: Surface charge in mV
        """
        self.dose = dose
        self.elimination_rate = elimination_rate
        self.distribution = distribution
        self.size = size
        self.charge = charge
        
        self._validate_distribution()
        
    def _validate_distribution(self):
        """Ensure organ distribution percentages sum to 100"""
        total = sum(self.distribution.values())
        if not np.isclose(total, 100, atol=0.1):
            raise ValueError(f"Distribution percentages must sum to 100 (current sum: {total})")

    def simulate_pk(self, hours: int = 24) -> pd.DataFrame:
        """Two-compartment pharmacokinetic model with size/charge effects"""
        # Adjust elimination rate based on nanoparticle properties
        size_factor = np.exp(-0.02 * self.size)
        charge_factor = 1 + 0.05 * abs(self.charge)
        ke = self.elimination_rate * size_factor * charge_factor
        
        time_points = np.arange(hours)
        concentrations = self.dose * np.exp(-ke * time_points)
        
        return pd.DataFrame({
            'hour': time_points,
            'concentration': concentrations
        })
    
    def simulate_distribution(self) -> pd.DataFrame:
        """Organ distribution based on charge-mediated affinity"""
        base_dist = pd.DataFrame({
            'organ': list(self.distribution.keys()),
            'percentage': list(self.distribution.values())
        })
        
        # Charge-based adjustment (example: positive charge increases liver uptake)
        if 'Liver' in base_dist['organ'].values:
            liver_idx = base_dist[base_dist['organ'] == 'Liver'].index[0]
            base_dist.at[liver_idx, 'percentage'] *= (1 + 0.02 * max(0, self.charge))
            
        # Renormalize to 100%
        total = base_dist['percentage'].sum()
        base_dist['percentage'] = base_dist['percentage'] * 100 / total
        
        return base_dist

    def plot_results(self, pk_data: pd.DataFrame, dist_data: pd.DataFrame):
        """Visualize pharmacokinetic and distribution results"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # PK Plot
        ax1.plot(pk_data['hour'], pk_data['concentration'], 'b-o')
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('Plasma Concentration (mg/L)')
        ax1.set_title('Pharmacokinetic Profile')
        ax1.grid(True)
        
        # Distribution Plot
        ax2.bar(dist_data['organ'], dist_data['percentage'], color='orange')
        ax2.set_ylabel('Distribution (%)')
        ax2.set_title('Organ Distribution')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    params = {
        'dose': 100,  # mg/kg
        'elimination_rate': 0.15,  # 1/hours
        'distribution': {'Liver': 50, 'Kidney': 30, 'Lung': 20},
        'size': 80,  # Nanoparticle size in nm
        'charge': -15  # Surface charge in mV
    }
    
    simulator = NanoparticleDeliverySimulator(**params)
    pk_results = simulator.simulate_pk()  # Simulate PK profile for 24 hours
    dist_results = simulator.simulate_distribution()  # Simulate organ distribution
    
    print("Pharmacokinetic Data:")
    print(pk_results.head())
    
    print("\nOrgan Distribution:")
    print(dist_results)
    
    simulator.plot_results(pk_results, dist_results)  # Visualize results

def simulate_delivery(particle_type="lipid", target_organ="liver", dose=100):
    """
    Simplified simulation function for the main application
    """
    try:
        params = {
            'drug_name': f'{particle_type}_delivery',
            'dose': dose,
            'target_organ': target_organ,
            'distribution': {'Liver': 50, 'Kidney': 30, 'Lung': 20},
            'size': 80,
            'charge': -15
        }
        
        simulator = NanoparticleDeliverySimulator(**params)
        pk_results = simulator.simulate_pk()
        dist_results = simulator.simulate_distribution()
        
        return {
            'success': True,
            'particle_type': particle_type,
            'target_organ': target_organ,
            'dose': dose,
            'max_concentration': pk_results['Concentration'].max(),
            'distribution': dist_results
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
