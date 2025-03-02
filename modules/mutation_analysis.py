import pandas as pd
import os
import logging
import sys
from typing import Dict, Optional

# Add parent directory to path to import MutationAnalyzer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mutation_analyzer import MutationAnalyzer, analyze_mutations as analyze_vcf_mutations

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_mutations(patient_data, vcf_file: Optional[str] = None):
    """
    Analyzes patient genetic data to identify oncogenic drivers, resistance profiles,
    and suggest potential therapies.
    
    Args:
        patient_data: Patient genetic and clinical data
        vcf_file: Path to a VCF file to analyze. If provided, this will be used instead of mock data.
        
    Returns:
        Dictionary containing:
        - 'drivers': DataFrame of oncogenic driver mutations
        - 'resistance': Dictionary of resistance profiles for different therapies
        - 'therapies': List of recommended therapies
        - 'all_variants': DataFrame of all variants found (if using VCF)
        - 'statistics': Statistics about the analysis results
    """
    # If a VCF file is provided, use the MutationAnalyzer to analyze it
    if vcf_file and os.path.exists(vcf_file):
        logger.info(f"Analyzing VCF file: {vcf_file}")
        try:
            # Use the analyze_mutations function from mutation_analyzer.py
            results = analyze_vcf_mutations(vcf_file)
            
            # Convert resistance DataFrame to expected format
            if results.get('resistance') and isinstance(results['resistance'], dict):
                resistance_data = []
                for gene, mutations in results['resistance'].items():
                    for mutation in mutations:
                        # Estimate a score based on impact
                        score = 0.75  # Default score
                        
                        # Look up the gene+mutation in drivers to get impact
                        if not results['drivers'].empty:
                            matching_drivers = results['drivers'][
                                (results['drivers']['gene'] == gene) & 
                                (results['drivers']['mutation'] == mutation)
                            ]
                            if not matching_drivers.empty:
                                impact = matching_drivers.iloc[0].get('impact', 'UNKNOWN')
                                if impact == 'HIGH':
                                    score = 0.9
                                elif impact == 'MODERATE':
                                    score = 0.7
                                elif impact == 'LOW':
                                    score = 0.5
                        
                        # Determine therapy based on gene
                        therapy = 'Unknown'
                        if gene == 'EGFR':
                            therapy = 'EGFR Inhibitor'
                        elif gene == 'KRAS':
                            therapy = 'KRAS Inhibitor'
                        elif gene == 'BRAF':
                            therapy = 'BRAF Inhibitor'
                        elif gene == 'ALK':
                            therapy = 'ALK Inhibitor'
                        elif gene == 'ROS1':
                            therapy = 'ROS1 Inhibitor'
                        
                        resistance_data.append({
                            'gene': gene,
                            'mutation': mutation,
                            'score': score,
                            'therapy': therapy
                        })
                
                # Convert to DataFrame
                resistance_df = pd.DataFrame(resistance_data) if resistance_data else pd.DataFrame(
                    columns=['gene', 'score', 'therapy'])
                
                # Format therapies data to match expected format
                therapies_data = []
                for therapy in results.get('therapies', []):
                    therapy_name = therapy.split('(')[0].strip() if '(' in therapy else therapy
                    mechanism = therapy.split('(')[1].rstrip(')') if '(' in therapy else 'Unknown mechanism'
                    efficacy = 0.75  # Default efficacy
                    
                    therapies_data.append({
                        'name': therapy_name,
                        'mechanism': mechanism,
                        'efficacy': efficacy
                    })
                
                # Return the analysis results
                return {
                    'drivers': results['drivers'],
                    'resistance': resistance_df,
                    'therapies': therapies_data,
                    'all_variants': results.get('all_variants', pd.DataFrame()),
                    'statistics': results.get('statistics', {})
                }
            
        except Exception as e:
            logger.error(f"Error analyzing VCF file: {e}")
            logger.info("Falling back to simulated data")
    
    # If VCF analysis failed or wasn't requested, use mock data
    logger.warning("Using simulated data for mutation analysis")
    
    # Mock data for oncogenic drivers
    drivers_data = {
        'gene': ['KRAS', 'BRCA1', 'TP53', 'EGFR', 'PIK3CA'],
        'mutation': ['G12D', 'L1501fs', 'R273H', 'T790M', 'E545K'],
        'vaf': [0.42, 0.31, 0.44, 0.18, 0.22],
        'impact': ['High', 'High', 'High', 'Moderate', 'High'],
        'actionable': [True, True, False, True, True]
    }
    
    # Mock data for resistance profiles
    resistance_data = {
        'gene': ['KRAS', 'NRAS', 'BRAF', 'MDM2', 'PTEN', 'PIK3CA'],
        'score': [0.78, 0.45, 0.62, 0.53, 0.71, 0.59],
        'therapy': ['Anti-EGFR', 'Anti-EGFR', 'MEK Inhibitor', 'p53 Therapy', 'mTOR Inhibitor', 'PI3K Inhibitor']
    }
    
    # Mock data for therapy suggestions
    therapies_data = [
        {'name': 'Pembrolizumab', 'mechanism': 'PD-1 Inhibitor', 'efficacy': 0.82},
        {'name': 'Olaparib', 'mechanism': 'PARP Inhibitor', 'efficacy': 0.65},
        {'name': 'Sotorasib', 'mechanism': 'KRAS G12C Inhibitor', 'efficacy': 0.72},
        {'name': 'Alpelisib', 'mechanism': 'PI3K Inhibitor', 'efficacy': 0.58},
        {'name': 'Osimertinib', 'mechanism': 'EGFR Inhibitor', 'efficacy': 0.48}
    ]
    
    # Convert to DataFrames
    drivers = pd.DataFrame(drivers_data)
    resistance = pd.DataFrame(resistance_data)
    
    return {
        'drivers': drivers,
        'resistance': resistance,
        'therapies': therapies_data
    }

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from random import choices, sample, randint, random, uniform
import plotly.express as px
import plotly.graph_objects as go

def analyze_mutations_for_visualization(sample_count=100, mutation_types=None, gene_list=None, vcf_file=None):
    """
    Analyze genetic mutations in cancer cells and return visualizable data.
    
    Parameters:
    -----------
    sample_count : int
        Number of samples to simulate if no VCF file is provided
    mutation_types : list
        List of mutation types to include in analysis. If None, defaults are used.
    gene_list : list
        List of genes to analyze. If None, common cancer genes are used.
    vcf_file : str, optional
        Path to a VCF file to analyze. If provided, real data will be used instead of simulated data.
    
    Returns:
    --------
    dict
        Dictionary containing multiple datasets for visualization:
        - mutation_counts_df: DataFrame with mutation counts by type
        - gene_mutation_df: DataFrame with mutation frequency by gene
        - mutation_impact_df: DataFrame with mutation impact scores
        - patient_mutations_df: DataFrame with mutation data per patient
        - mutation_correlation: DataFrame with correlation between mutations
    """
    # Check if we should use real VCF data
    if vcf_file and os.path.exists(vcf_file):
        logger.info(f"Using real VCF data for visualization: {vcf_file}")
        try:
            # Use the MutationAnalyzer to parse the VCF file
            mutations_df, impact_dict = MutationAnalyzer.analyze_vcf(vcf_file)
            
            if mutations_df.empty:
                logger.warning("No mutations found in VCF file, falling back to simulated data")
            else:
                # Process real VCF data for visualization
                return process_real_vcf_data(mutations_df, impact_dict)
        except Exception as e:
            logger.error(f"Error processing VCF file: {e}")
            logger.warning("Falling back to simulated data")
    # Set defaults if not provided
    if mutation_types is None:
        mutation_types = ['Missense', 'Nonsense', 'Frameshift', 'In-frame Indel', 
                          'Splice Site', 'Promoter', 'Amplification', 'Deletion']
    
    if gene_list is None:
        gene_list = ['TP53', 'KRAS', 'BRCA1', 'BRCA2', 'EGFR', 'PIK3CA', 'PTEN', 
                    'APC', 'BRAF', 'RB1', 'ATM', 'CDH1', 'CDKN2A', 'SMAD4', 'NF1']
    
    # 1. Generate mutation counts by type
    mutation_weights = [0.4, 0.1, 0.15, 0.05, 0.08, 0.07, 0.1, 0.05]  # Probabilities for each mutation type
    mutation_counts = np.random.multinomial(sample_count * 3, 
                                           mutation_weights[:len(mutation_types)])
    
    mutation_counts_df = pd.DataFrame({
        'Mutation Type': mutation_types,
        'Count': mutation_counts
    })
    
    # 2. Generate mutation frequency by gene
    gene_mutation_data = []
    cancer_types = ['Lung', 'Breast', 'Colorectal', 'Prostate', 'Melanoma', 'Leukemia']
    
    for gene in gene_list:
        for cancer in cancer_types:
            # Simulate different mutation patterns for different cancer types
            frequency = np.clip(np.random.normal(
                loc=0.2 + (gene_list.index(gene) % 5) * 0.05, 
                scale=0.1
            ), 0, 1)
            
            gene_mutation_data.append({
                'Gene': gene,
                'Cancer Type': cancer,
                'Mutation Frequency': frequency
            })
    
    gene_mutation_df = pd.DataFrame(gene_mutation_data)
    
    # 3. Generate mutation impact scores
    impact_categories = ['High', 'Moderate', 'Low', 'Modifier']
    impact_weights = [0.2, 0.3, 0.35, 0.15]
    
    mutation_impact_data = []
    for gene in gene_list:
        for m_type in sample(mutation_types, min(4, len(mutation_types))):
            impact = choices(impact_categories, weights=impact_weights)[0]
            score = uniform(0, 100) 
            if impact == 'High':
                score += 70
            elif impact == 'Moderate':
                score += 40
            elif impact == 'Low':
                score += 20
                
            score = min(score, 100)
            
            mutation_impact_data.append({
                'Gene': gene,
                'Mutation Type': m_type,
                'Impact': impact,
                'Impact Score': score
            })
    
    mutation_impact_df = pd.DataFrame(mutation_impact_data)
    
    # 4. Generate patient-level mutation data
    patient_ids = [f'PT{i:03d}' for i in range(1, sample_count + 1)]
    patient_data = []
    
    for pt_id in patient_ids:
        # Randomly assign patient characteristics
        age = randint(30, 85)
        gender = choices(['Male', 'Female'], weights=[0.48, 0.52])[0]
        cancer_type = choices(cancer_types)[0]
        stage = choices(['I', 'II', 'III', 'IV'], weights=[0.2, 0.3, 0.3, 0.2])[0]
        
        # Assign random mutations to each patient
        num_mutations = np.random.poisson(3)  # Average 3 mutations per patient
        for _ in range(num_mutations):
            gene = choices(gene_list)[0]
            mutation = choices(mutation_types)[0]
            
            # Calculate survival probability (simplified model)
            if stage == 'IV' and gene in ['TP53', 'KRAS', 'BRAF']:
                survival_prob = np.random.beta(2, 5) * 100  # Lower survival
            else:
                survival_prob = np.random.beta(5, 2) * 100  # Higher survival
                
            response_prob = np.random.beta(3, 3) * 100
            
            patient_data.append({
                'Patient ID': pt_id,
                'Age': age,
                'Gender': gender,
                'Cancer Type': cancer_type,
                'Stage': stage,
                'Mutated Gene': gene,
                'Mutation Type': mutation,
                'Treatment Response Probability': response_prob,
                'Survival Probability': survival_prob
            })
    
    patient_mutations_df = pd.DataFrame(patient_data)
    
    # 5. Generate mutation correlation data
    corr_data = {}
    for i, gene1 in enumerate(gene_list[:10]):  # Limit to 10 genes for correlation
        corr_row = {}
        for j, gene2 in enumerate(gene_list[:10]):
            if i == j:
                correlation = 1.0
            else:
                # Generate some interesting patterns
                base = 0.3 * random() - 0.15  # Base correlation
                
                # Some genes tend to be mutated together
                if (gene1 in ['BRCA1', 'BRCA2'] and gene2 in ['BRCA1', 'BRCA2']):
                    base += 0.6
                elif (gene1 in ['KRAS', 'BRAF'] and gene2 in ['KRAS', 'BRAF']):
                    base += 0.4
                
                # Some mutations tend to be mutually exclusive
                if (gene1 in ['TP53'] and gene2 in ['CDKN2A']) or (gene1 in ['CDKN2A'] and gene2 in ['TP53']):
                    base -= 0.5
                    
                correlation = max(min(base, 1.0), -1.0)  # Bound to [-1, 1]
            
            corr_row[gene2] = correlation
        corr_data[gene1] = corr_row
    
    mutation_correlation = pd.DataFrame(corr_data)
    
    return {
        'mutation_counts_df': mutation_counts_df,
        'gene_mutation_df': gene_mutation_df,
        'mutation_impact_df': mutation_impact_df,
        'patient_mutations_df': patient_mutations_df,
        'mutation_correlation': mutation_correlation
    }

def visualize_mutation_data(mutation_data):
    """
    Create visualizations for mutation analysis data.
    
    Parameters:
    -----------
    mutation_data : dict
        Dictionary containing the datasets from analyze_mutations()
    
    Returns:
    --------
    None (displays visualizations in Streamlit)
    """
    # Extract dataframes from input dictionary
    mutation_counts_df = mutation_data['mutation_counts_df']
    gene_mutation_df = mutation_data['gene_mutation_df']
    mutation_impact_df = mutation_data['mutation_impact_df']
    patient_mutations_df = mutation_data['patient_mutations_df']
    mutation_correlation = mutation_data['mutation_correlation']
    
    # 1. Mutation type distribution
    st.subheader("Distribution of Mutation Types")
    fig1 = px.bar(mutation_counts_df, x='Mutation Type', y='Count',
                 color='Mutation Type', title="Frequency of Mutation Types")
    st.plotly_chart(fig1)
    
    # 2. Gene mutation frequency by cancer type
    st.subheader("Gene Mutation Frequency by Cancer Type")
    fig2 = px.bar(gene_mutation_df, x='Gene', y='Mutation Frequency',
                 color='Cancer Type', barmode='group',
                 title="Mutation Frequency by Gene and Cancer Type")
    st.plotly_chart(fig2)
    
    # 3. Mutation impact heatmap
    st.subheader("Mutation Impact Analysis")
    pivot_impact = mutation_impact_df.pivot_table(
        index='Gene', columns='Mutation Type', values='Impact Score', aggfunc='mean')
    
    fig3 = px.imshow(pivot_impact, color_continuous_scale='Viridis',
                    title="Average Impact Score by Gene and Mutation Type")
    st.plotly_chart(fig3)
    
    # 4. Patient mutation analysis
    st.subheader("Patient Mutation Analysis")
    
    # Distribution of mutations by cancer stage
    stage_gene_count = patient_mutations_df.groupby(['Stage', 'Mutated Gene']).size().reset_index(name='Count')
    fig4 = px.bar(stage_gene_count, x='Stage', y='Count', color='Mutated Gene',
                 title="Distribution of Gene Mutations by Cancer Stage")
    st.plotly_chart(fig4)
    
    # Survival probability by mutation
    fig5 = px.box(patient_mutations_df, x='Mutated Gene', y='Survival Probability',
                 color='Stage', title="Survival Probability by Gene Mutation and Stage")
    st.plotly_chart(fig5)
    
    # 5. Mutation correlation heatmap
    st.subheader("Gene Mutation Correlation")
    fig6 = px.imshow(mutation_correlation, color_continuous_scale='RdBu_r',
                    title="Correlation Between Gene Mutations", 
                    zmin=-1, zmax=1)
    st.plotly_chart(fig6)
def process_real_vcf_data(mutations_df, impact_dict):
    """
    Process real VCF data from MutationAnalyzer for visualization
    
    Parameters:
    -----------
    mutations_df : pd.DataFrame
        DataFrame containing mutation data from VCF
    impact_dict : dict
        Dictionary containing impact information for mutations
    
    Returns:
    --------
    dict
        Dictionary containing datasets for visualization
    """
    # Define cancer types and known driver genes for categorization
    cancer_types = ['Lung', 'Breast', 'Colorectal', 'Prostate', 'Melanoma', 'Leukemia']
    driver_genes = {
        'TP53': ['Lung', 'Breast', 'Colorectal', 'Prostate', 'Melanoma', 'Leukemia'],
        'KRAS': ['Lung', 'Colorectal', 'Pancreatic'],
        'EGFR': ['Lung'],
        'BRAF': ['Melanoma', 'Colorectal'],
        'PIK3CA': ['Breast', 'Colorectal'],
        'PTEN': ['Breast', 'Prostate'],
        'APC': ['Colorectal'],
        'BRCA1': ['Breast', 'Ovarian'],
        'BRCA2': ['Breast', 'Ovarian', 'Prostate'],
        'RB1': ['Retinoblastoma', 'Lung', 'Breast'],
        'CDKN2A': ['Melanoma', 'Pancreatic'],
        'SMAD4': ['Colorectal', 'Pancreatic'],
        'NF1': ['Melanoma', 'Lung'],
        'ATM': ['Breast', 'Leukemia'],
        'IDH1': ['Glioma', 'Leukemia'],
        'RET': ['Lung', 'Thyroid']
    }
    
    # 1. Generate mutation counts by type
    # Extract mutation types from the variations in the data
    mutation_types = []
    mutation_counts = []
    
    # Simple mapping to categorize mutations
    mutation_type_mapping = {
        'missense_variant': 'Missense',
        'frameshift_variant': 'Frameshift',
        'stop_gained': 'Nonsense',
        'splice_acceptor_variant': 'Splice Site',
        'splice_donor_variant': 'Splice Site',
        'inframe_insertion': 'In-frame Indel',
        'inframe_deletion': 'In-frame Indel',
        'protein_altering_variant': 'Missense',
        'start_lost': 'Nonsense',
        'stop_lost': 'Nonsense',
        'exon_loss_variant': 'Deletion',
        'upstream_gene_variant': 'Promoter',
        '5_prime_UTR_variant': 'Promoter',
        '3_prime_UTR_variant': 'Modifier',
        'intron_variant': 'Modifier',
        'synonymous_variant': 'Synonymous'
    }
    
    # Extract mutation types and count occurrences
    mutation_type_counts = {}
    for _, row in mutations_df.iterrows():
        # Get variant type from mutation description or infer from impact
        variant_description = row.get('mutation', '').lower()
        impact = row.get('impact', 'UNKNOWN')
        
        # Try to determine mutation type
        mutation_type = 'Other'
        for key, value in mutation_type_mapping.items():
            if key in variant_description:
                mutation_type = value
                break
                
        # Use impact as fallback for categorization
        if mutation_type == 'Other' and impact:
            if impact == 'HIGH':
                mutation_type = 'Nonsense' if 'stop' in variant_description else 'Frameshift'
            elif impact == 'MODERATE':
                mutation_type = 'Missense'
            elif impact == 'LOW':
                mutation_type = 'Synonymous'
                
        # Count this mutation type
        mutation_type_counts[mutation_type] = mutation_type_counts.get(mutation_type, 0) + 1
    
    # Convert to lists for DataFrame
    for m_type, count in mutation_type_counts.items():
        mutation_types.append(m_type)
        mutation_counts.append(count)
    
    mutation_counts_df = pd.DataFrame({
        'Mutation Type': mutation_types,
        'Count': mutation_counts
    })
    
    # 2. Generate mutation frequency by gene
    gene_mutation_data = []
    
    # Count mutations per gene
    gene_counts = mutations_df['gene'].value_counts().to_dict()
    total_mutations = sum(gene_counts.values())
    
    # Calculate frequency for each gene and assign to likely cancer types
    for gene, count in gene_counts.items():
        frequency = count / total_mutations
        
        # Assign to cancer types based on knowledge of driver genes
        associated_cancers = driver_genes.get(gene, [sample(cancer_types, 1)[0]])
        
        for cancer in associated_cancers:
            # Slightly vary frequency for visualization
            adjusted_frequency = frequency * uniform(0.8, 1.2)
            gene_mutation_data.append({
                'Gene': gene,
                'Cancer Type': cancer,
                'Mutation Frequency': min(adjusted_frequency, 1.0)
            })
    
    gene_mutation_df = pd.DataFrame(gene_mutation_data)
    
    # 3. Generate mutation impact scores
    mutation_impact_data = []
    
    # Map impact levels to score ranges
    impact_score_ranges = {
        'HIGH': (70, 100),
        'MODERATE': (40, 70),
        'LOW': (20, 40),
        'MODIFIER': (0, 20),
        'UNKNOWN': (0, 100)
    }
    
    # Process each mutation to determine its impact score
    for _, row in mutations_df.iterrows():
        gene = row['gene']
        mutation = row['mutation']
        impact = row.get('impact', 'UNKNOWN')
        
        # Determine mutation type from mutation string
        mutation_type = 'Other'
        for key, value in mutation_type_mapping.items():
            if key in str(mutation).lower():
                mutation_type = value
                break
        
        # Determine impact category
        impact_category = 'Modifier'
        if impact == 'HIGH':
            impact_category = 'High'
        elif impact == 'MODERATE':
            impact_category = 'Moderate'
        elif impact == 'LOW':
            impact_category = 'Low'
        
        # Calculate impact score
        min_score, max_score = impact_score_ranges.get(impact, impact_score_ranges['UNKNOWN'])
        score = uniform(min_score, max_score)
        
        mutation_impact_data.append({
            'Gene': gene,
            'Mutation Type': mutation_type,
            'Impact': impact_category,
            'Impact Score': score
        })
    
    mutation_impact_df = pd.DataFrame(mutation_impact_data)
    
    # 4. Generate patient-level mutation data
    # Since real VCF doesn't contain patient IDs, we'll simulate this part
    # based on the detected mutations
    patient_data = []
    
    # Use the number of unique genes as a proxy for number of patients
    sample_count = min(100, len(gene_counts) * 3)  # Ensure reasonable number
    patient_ids = [f'PT{i:03d}' for i in range(1, sample_count + 1)]
    
    # Assign mutations to simulated patients based on real mutation data
    mutation_records = mutations_df.to_dict('records')
    
    # Distribute mutations across patients with some realistic patterns
    for pt_id in patient_ids:
        # Randomly assign patient characteristics
        age = randint(30, 85)
        gender = choices(['Male', 'Female'], weights=[0.48, 0.52])[0]
        cancer_type = choices(cancer_types)[0]
        stage = choices(['I', 'II', 'III', 'IV'], weights=[0.2, 0.3, 0.3, 0.2])[0]
        
        # Assign 1-5 mutations to each patient
        num_mutations = min(5, randint(1, min(5, len(mutation_records))))
        selected_mutations = sample(mutation_records, num_mutations)
        
        for mutation in selected_mutations:
            gene = mutation['gene']
            mutation_name = mutation['mutation']
            
            # Determine mutation type
            mutation_type = 'Other'
            for key, value in mutation_type_mapping.items():
                if key in str(mutation_name).lower():
                    mutation_type = value
                    break
            
            # Calculate survival probability (simplified model)
            if stage == 'IV' and gene in ['TP53', 'KRAS', 'BRAF']:
                survival_prob = np.random.beta(2, 5) * 100  # Lower survival
            else:
                survival_prob = np.random.beta(5, 2) * 100  # Higher survival
                
            # Treatment response depends on gene and mutation impact
            impact = mutation.get('impact', 'UNKNOWN')
            if impact == 'HIGH' and gene in ['EGFR', 'BRAF', 'ALK']:
                response_prob = np.random.beta(5, 2) * 100  # Higher response for targeted therapies
            else:
                response_prob = np.random.beta(3, 3) * 100
            
            patient_data.append({
                'Patient ID': pt_id,
                'Age': age,
                'Gender': gender,
                'Cancer Type': cancer_type,
                'Stage': stage,
                'Mutated Gene': gene,
                'Mutation Type': mutation_type,
                'Mutation': mutation_name,
                'Treatment Response Probability': response_prob,
                'Survival Probability': survival_prob
            })
    
    patient_mutations_df = pd.DataFrame(patient_data)
    
    # 5. Generate mutation correlation data
    # Get top genes by mutation frequency
    top_genes = list(gene_counts.keys())[:10]  # Top 10 genes
    
    # Create correlation matrix
    corr_data = {}
    for i, gene1 in enumerate(top_genes):
        corr_row = {}
        for j, gene2 in enumerate(top_genes):
            if i == j:
                correlation = 1.0
            else:
                # Generate correlation based on biological knowledge
                base = 0.3 * random() - 0.15  # Base correlation
                
                # Some genes tend to be mutated together
                if (gene1 in ['BRCA1', 'BRCA2'] and gene2 in ['BRCA1', 'BRCA2']):
                    base += 0.6
                elif (gene1 in ['KRAS', 'BRAF'] and gene2 in ['KRAS', 'BRAF']):
                    base += 0.4
                
                # Some mutations tend to be mutually exclusive
                if (gene1 in ['TP53'] and gene2 in ['CDKN2A']) or (gene1 in ['CDKN2A'] and gene2 in ['TP53']):
                    base -= 0.5
                elif (gene1 in ['KRAS'] and gene2 in ['EGFR']) or (gene1 in ['EGFR'] and gene2 in ['KRAS']):
                    base -= 0.7
                    
                correlation = max(min(base, 1.0), -1.0)  # Bound to [-1, 1]
            
            corr_row[gene2] = correlation
        corr_data[gene1] = corr_row
    
    mutation_correlation = pd.DataFrame(corr_data)
    
    return {
        'mutation_counts_df': mutation_counts_df,
        'gene_mutation_df': gene_mutation_df,
        'mutation_impact_df': mutation_impact_df,
        'patient_mutations_df': patient_mutations_df,
        'mutation_correlation': mutation_correlation
    }
