import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from random import choices, sample, randint, random, uniform
import plotly.express as px
import plotly.graph_objects as go

def analyze_mutations(sample_count=100, mutation_types=None, gene_list=None):
    """
    Analyze genetic mutations in cancer cells and return visualizable data.
    
    Parameters:
    -----------
    sample_count : int
        Number of samples to simulate
    mutation_types : list
        List of mutation types to include in analysis. If None, defaults are used.
    gene_list : list
        List of genes to analyze. If None, common cancer genes are used.
    
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
