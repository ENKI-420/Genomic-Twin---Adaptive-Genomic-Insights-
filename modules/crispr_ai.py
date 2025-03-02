import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Optional, Union
import random

def generate_crispr_data(
    gene_targets: List[str],
    cancer_types: List[str],
    sample_size: int = 50,
    random_seed: Optional[int] = None
) -> pd.DataFrame:
    """
    Generate simulated CRISPR gene editing data for cancer research.
    
    Parameters:
    -----------
    gene_targets : List[str]
        List of gene targets for CRISPR editing
    cancer_types : List[str]
        List of cancer types to analyze
    sample_size : int
        Number of samples to generate
    random_seed : Optional[int]
        Random seed for reproducibility
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with simulated CRISPR gene editing data
    """
    if random_seed is not None:
        np.random.seed(random_seed)
        random.seed(random_seed)
    
    data = []
    
    for _ in range(sample_size):
        gene = random.choice(gene_targets)
        cancer = random.choice(cancer_types)
        
        # Simulate editing efficiency (0-100%)
        efficiency = round(np.random.beta(5, 2) * 100, 1)
        
        # Simulate off-target effects (0-10 count)
        off_target = np.random.poisson(2)
        
        # Simulate delivery success (0-100%)
        delivery_success = round(np.random.beta(7, 3) * 100, 1)
        
        # Simulate cell viability post-editing (0-100%)
        cell_viability = round(np.random.normal(75, 15), 1)
        if cell_viability > 100:
            cell_viability = 100.0
        elif cell_viability < 0:
            cell_viability = 0.0
        
        # Calculate overall feasibility score (0-10)
        feasibility = round((
            (efficiency / 100) * 0.4 +
            (1 - (off_target / 10)) * 0.2 +
            (delivery_success / 100) * 0.2 +
            (cell_viability / 100) * 0.2
        ) * 10, 1)
        
        data.append({
            'Gene_Target': gene,
            'Cancer_Type': cancer,
            'Editing_Efficiency': efficiency,
            'Off_Target_Effects': off_target,
            'Delivery_Success': delivery_success,
            'Cell_Viability': cell_viability,
            'Feasibility_Score': feasibility
        })
    
    return pd.DataFrame(data)

def analyze_gene_cancer_combinations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze the effectiveness of different gene-cancer combinations.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with CRISPR data
        
    Returns:
    --------
    pd.DataFrame
        Summary dataframe of gene-cancer combinations
    """
    # Group by gene target and cancer type and calculate mean values
    summary = df.groupby(['Gene_Target', 'Cancer_Type']).agg({
        'Editing_Efficiency': 'mean',
        'Off_Target_Effects': 'mean',
        'Delivery_Success': 'mean',
        'Cell_Viability': 'mean',
        'Feasibility_Score': 'mean'
    }).reset_index()
    
    # Round values for better readability
    for col in summary.columns:
        if col not in ['Gene_Target', 'Cancer_Type']:
            summary[col] = summary[col].round(2)
    
    return summary.sort_values('Feasibility_Score', ascending=False)

def create_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create data for a heatmap visualization of gene-cancer feasibility.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with CRISPR data
        
    Returns:
    --------
    pd.DataFrame
        Pivoted dataframe suitable for heatmap visualization
    """
    # Group by gene and cancer type, calculate mean feasibility
    heatmap_data = df.groupby(['Gene_Target', 'Cancer_Type'])['Feasibility_Score'].mean().reset_index()
    
    # Pivot the data for the heatmap
    pivot_data = heatmap_data.pivot(
        index='Gene_Target', 
        columns='Cancer_Type', 
        values='Feasibility_Score'
    )
    
    return pivot_data

def crispr_feasibility(
    gene_targets: Optional[List[str]] = None,
    cancer_types: Optional[List[str]] = None,
    sample_size: int = 50,
    random_seed: Optional[int] = 42
) -> Dict[str, Union[pd.DataFrame, plt.Figure]]:
    """
    Analyze the feasibility of CRISPR gene editing for cancer targets.
    
    Parameters:
    -----------
    gene_targets : Optional[List[str]]
        List of gene targets for CRISPR editing (default provides common cancer genes if None)
    cancer_types : Optional[List[str]]
        List of cancer types to analyze (default provides common cancer types if None)
    sample_size : int
        Number of samples to generate
    random_seed : Optional[int]
        Random seed for reproducibility
        
    Returns:
    --------
    Dict[str, Union[pd.DataFrame, plt.Figure]]
        Dictionary containing dataframes and figures for visualization
    """
    # Default gene targets if none provided
    if gene_targets is None:
        gene_targets = ['TP53', 'KRAS', 'BRCA1', 'BRCA2', 'EGFR', 'HER2', 'BRAF', 'PTEN', 'RB1', 'APC']
    
    # Default cancer types if none provided
    if cancer_types is None:
        cancer_types = ['Lung', 'Breast', 'Colorectal', 'Prostate', 'Pancreatic', 'Ovarian', 'Melanoma', 'Leukemia']
    
    # Generate the simulated data
    df = generate_crispr_data(gene_targets, cancer_types, sample_size, random_seed)
    
    # Analyze gene-cancer combinations
    summary_df = analyze_gene_cancer_combinations(df)
    
    # Create heatmap data
    heatmap_df = create_heatmap_data(df)
    
    # Calculate overall stats
    overall_stats = df.describe()
    
    # Prepare the return dictionary
    results = {
        'raw_data': df,
        'summary': summary_df,
        'heatmap_data': heatmap_df,
        'overall_stats': overall_stats
    }
    
    return results

def crispr():
    """Legacy function - maintained for backward compatibility"""
    st.warning("The crispr() function is deprecated. Please use crispr_feasibility() instead.")
    return crispr_feasibility()
