"""
Visualization module for oncology data analysis.

This module provides functions for visualizing various types of oncology data
including gene expression, mutations, and survival analysis using different
plotting libraries (matplotlib, seaborn, and plotly).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from lifelines import KaplanMeierFitter, CoxPHFitter
from typing import List, Dict, Optional, Union, Tuple
import io
import base64


def plot_gene_expression(
    data: pd.DataFrame, 
    gene_ids: List[str],
    sample_groups: Optional[Dict[str, List[str]]] = None,
    plot_type: str = 'boxplot',
    title: str = 'Gene Expression Analysis',
    figsize: Tuple[int, int] = (12, 8),
    color_palette: str = 'Set1',
    log_scale: bool = True,
    return_fig: bool = False
) -> Optional[plt.Figure]:
    """
    Plot gene expression data for selected genes across sample groups.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with gene expression data (genes as columns, samples as rows)
    gene_ids : List[str]
        List of gene identifiers to visualize
    sample_groups : Dict[str, List[str]], optional
        Dictionary mapping group names to lists of sample IDs
    plot_type : str
        Type of plot ('boxplot', 'violin', 'heatmap', 'bar')
    title : str
        Plot title
    figsize : Tuple[int, int]
        Figure size as (width, height) in inches
    color_palette : str
        Name of seaborn color palette to use
    log_scale : bool
        Whether to log-transform expression values
    return_fig : bool
        If True, return the figure object; otherwise, display the plot
        
    Returns:
    --------
    plt.Figure or None
        Matplotlib figure object if return_fig is True, otherwise None
    """
    # Filter data to include only specified genes
    plot_data = data[gene_ids].copy()
    
    if log_scale:
        # Apply log2(x+1) transformation to handle zeros
        plot_data = np.log2(plot_data + 1)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    if plot_type == 'heatmap':
        # Prepare data for heatmap
        if sample_groups:
            # Reorganize data by sample groups
            group_data = []
            for group, samples in sample_groups.items():
                group_samples = plot_data.loc[samples]
                group_samples['Group'] = group
                group_data.append(group_samples)
            plot_data = pd.concat(group_data)
            
            # Create heatmap with samples organized by group
            sns.heatmap(
                plot_data[gene_ids].T, 
                cmap='viridis', 
                center=0, 
                robust=True,
                yticklabels=gene_ids,
                ax=ax
            )
        else:
            # Simple heatmap without grouping
            sns.heatmap(
                plot_data.T, 
                cmap='viridis', 
                center=0, 
                robust=True,
                yticklabels=gene_ids,
                ax=ax
            )
            
    elif plot_type in ['boxplot', 'violin']:
        # Convert to long format for boxplot or violin plot
        plot_data_long = plot_data.reset_index().melt(
            id_vars='index', 
            value_vars=gene_ids,
            var_name='Gene', 
            value_name='Expression'
        )
        
        # Add group information if provided
        if sample_groups:
            # Create a mapping from sample ID to group
            sample_to_group = {}
            for group, samples in sample_groups.items():
                for sample in samples:
                    sample_to_group[sample] = group
                    
            # Add group column
            plot_data_long['Group'] = plot_data_long['index'].map(
                lambda x: sample_to_group.get(x, 'Unknown')
            )
            
            # Create plot with group information
            if plot_type == 'boxplot':
                sns.boxplot(
                    x='Gene', 
                    y='Expression', 
                    hue='Group',
                    data=plot_data_long,
                    palette=color_palette,
                    ax=ax
                )
            else:  # violin plot
                sns.violinplot(
                    x='Gene', 
                    y='Expression', 
                    hue='Group',
                    data=plot_data_long,
                    palette=color_palette,
                    split=True,
                    inner='quart',
                    ax=ax
                )
        else:
            # Create plot without group information
            if plot_type == 'boxplot':
                sns.boxplot(
                    x='Gene', 
                    y='Expression',
                    data=plot_data_long,
                    palette=color_palette,
                    ax=ax
                )
            else:  # violin plot
                sns.violinplot(
                    x='Gene', 
                    y='Expression',
                    data=plot_data_long,
                    palette=color_palette,
                    inner='quart',
                    ax=ax
                )
                
    elif plot_type == 'bar':
        # Calculate mean expression per gene
        if sample_groups:
            group_means = {}
            for group, samples in sample_groups.items():
                group_means[group] = plot_data.loc[samples].mean()
                
            # Convert to DataFrame for plotting
            mean_data = pd.DataFrame(group_means).T
            mean_data.plot(
                kind='bar', 
                ax=ax, 
                width=0.7, 
                colormap=color_palette
            )
        else:
            # Simple bar plot of mean expression
            plot_data.mean().plot(
                kind='bar',
                ax=ax,
                color=sns.color_palette(color_palette, len(gene_ids))
            )
    
    plt.title(title)
    plt.tight_layout()
    
    if return_fig:
        return fig
    
    plt.show()
    return None


def plot_gene_expression_interactive(
    data: pd.DataFrame,
    gene_ids: List[str],
    sample_groups: Optional[Dict[str, List[str]]] = None,
    plot_type: str = 'boxplot',
    title: str = 'Gene Expression Analysis',
    color_palette: Optional[List[str]] = None,
    log_scale: bool = True,
    height: int = 600,
    width: int = 900
) -> go.Figure:
    """
    Create interactive gene expression plots using Plotly.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with gene expression data (genes as columns, samples as rows)
    gene_ids : List[str]
        List of gene identifiers to visualize
    sample_groups : Dict[str, List[str]], optional
        Dictionary mapping group names to lists of sample IDs
    plot_type : str
        Type of plot ('boxplot', 'violin', 'heatmap', 'bar')
    title : str
        Plot title
    color_palette : List[str], optional
        List of color hex codes
    log_scale : bool
        Whether to log-transform expression values
    height : int
        Plot height in pixels
    width : int
        Plot width in pixels
        
    Returns:
    --------
    go.Figure
        Plotly figure object
    """
    # Filter data to include only specified genes
    plot_data = data[gene_ids].copy()
    
    if log_scale:
        # Apply log2(x+1) transformation to handle zeros
        plot_data = np.log2(plot_data + 1)
    
    # Default color palette if none provided
    if color_palette is None:
        color_palette = px.colors.qualitative.Set1
    
    # Convert to long format for most plot types
    plot_data_long = plot_data.reset_index().melt(
        id_vars='index', 
        value_vars=gene_ids,
        var_name='Gene', 
        value_name='Expression'
    )
    
    # Add group information if provided
    if sample_groups:
        # Create a mapping from sample ID to group
        sample_to_group = {}
        for group, samples in sample_groups.items():
            for sample in samples:
                sample_to_group[sample] = group
                
        # Add group column
        plot_data_long['Group'] = plot_data_long['index'].map(
            lambda x: sample_to_group.get(x, 'Unknown')
        )
    
    # Create appropriate plot type
    if plot_type == 'boxplot':
        if sample_groups:
            fig = px.box(
                plot_data_long, 
                x='Gene', 
                y='Expression',
                color='Group',
                title=title,
                color_discrete_sequence=color_palette,
                height=height,
                width=width
            )
        else:
            fig = px.box(
                plot_data_long, 
                x='Gene', 
                y='Expression',
                title=title,
                color_discrete_sequence=color_palette,
                height=height,
                width=width
            )
            
    elif plot_type == 'violin':
        if sample_groups:
            fig = px.violin(
                plot_data_long,
                x='Gene',
                y='Expression',
                color='Group',
                box=True,
                title=title,
                color_discrete_sequence=color_palette,
                height=height,
                width=width
            )
        else:
            fig = px.violin(
                plot_data_long,
                x='Gene',
                y='Expression',
                box=True,
                title=title,
                color_discrete_sequence=color_palette,
                height=height,
                width=width
            )
            
    elif plot_type == 'heatmap':
        # For heatmap, we use a different approach
        if sample_groups:
            # Reorganize data by sample groups
            samples_order = []
            group_labels = []
            
            for group, samples in sample_groups.items():
                samples_order.extend(samples)
                group_labels.extend([group] * len(samples))
            
            # Create heatmap with samples organized by group
            fig = px.imshow(
                plot_data.loc[samples_order, gene_ids].T,
                title=title,
                labels=dict(x="Sample", y="Gene", color="Expression"),
                height=height,
                width=width,
                color_continuous_scale="Viridis"
            )
            
            # Add annotations for groups
            fig.update_layout(
                annotations=[
                    dict(
                        x=i,
                        y=-0.5,
                        text=group,
                        textangle=-90,
                        showarrow=False,
                        xref="x",
                        yref="paper"
                    ) for i, group in enumerate(group_labels)
                ]
            )
        else:
            # Simple heatmap without grouping
            fig = px.imshow(
                plot_data.T,
                title=title,
                labels=dict(x="Sample", y="Gene", color="Expression"),
                height=height,
                width=width,
                color_continuous_scale="Viridis"
            )
            
    elif plot_type == 'bar':
        # Calculate mean expression per gene
        if sample_groups:
            group_means = {}
            for group, samples in sample_groups.items():
                group_means[group] = plot_data.loc[samples].mean()
                
            # Convert to DataFrame for plotting
            mean_data = pd.DataFrame(group_means).T
            
            # Use plotly for bar plot
            fig = px.bar(
                mean_data,
                x=mean_data.index,
                y=gene_ids,
                title=title,
                barmode='group',
                color_discrete_sequence=color_palette,
                height=height,
                width=width
            )
        else:
            # Simple bar plot of mean expression
            mean_values = plot_data.mean().reset_index()
            mean_values.columns = ['Gene', 'Mean Expression']
            
            fig = px.bar(
                mean_values,
                x='Gene',
                y='Mean Expression',
                title=title,
                color='Gene',
                color_discrete_sequence=color_palette,
                height=height,
                width=width
            )
    
    # Update layout for better appearance
    fig.update_layout(
        plot_bgcolor='white',
        legend_title_text='',
        xaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12)
        )
    )
    
    return fig


def plot_mutation_heatmap(
    mutation_data: pd.DataFrame,
    genes: Optional[List[str]] = None,
    samples: Optional[List[str]] = None,
    annotation_data: Optional[pd.DataFrame] = None,
    title: str = 'Mutation Heatmap',
    figsize: Tuple[int, int] = (12, 10),
    cmap: str = 'YlOrRd',
    cluster: bool = True,
    return_fig: bool = False
) -> Optional[plt.Figure]:
    """
    Create a heatmap visualization of mutation data across genes and samples.
    
    Parameters:
    -----------
    mutation_data : pd.DataFrame
        DataFrame with mutation data (1/0 or mutation types),
        with genes as rows and samples as columns
    genes : List[str], optional
        List of genes to include (default: all genes in mutation_data)
    samples : List[str], optional
        List of samples to include (default: all samples in mutation_data)
    annotation_data : pd.DataFrame, optional
        DataFrame with sample annotations for additional visualization,
        must have same sample IDs as columns
    title : str
        Plot title
    figsize : Tuple[int, int]
        Figure size as (width, height) in inches
    cmap : str
        Colormap name for the heatmap
    cluster : bool
        Whether to cluster genes and samples
    return_fig : bool
        If True, return the figure object; otherwise, display the plot
        
    Returns:
    --------
    plt.Figure or None
        Matplotlib figure object if return_fig is True, otherwise None
    """
    # Filter data if necessary
    if genes is not None:
        mutation_data = mutation_data.loc[mutation_data.index.isin(genes)]
    if samples is not None:
        mutation_data = mutation_data.loc[:, mutation_data.columns.isin(samples)]
    
    # Create figure
    if annotation_data is not None:
        # Calculate the height ratio for annotations
        n_annot_rows = len(annotation_data)
        heatmap_height = len(mutation_data)
        height_ratios = [1] * n_annot_rows + [heatmap_height / n_annot_rows * 3]

def plot_survival_curve(
    gene: str,
    survival_type: str = "Overall Survival",
    expression_cutoff_percentile: int = 50,
    show_censors: bool = True,
    show_ci: bool = True,
    figsize: Tuple[int, int] = (10, 6),
    palette: List[str] = ["#3498db", "#e74c3c"],
    return_fig: bool = True
) -> plt.Figure:
    """
    Generate Kaplan-Meier survival curves for patients with high vs low expression of a specified gene.
    
    Parameters:
    -----------
    gene : str
        Gene symbol/identifier to analyze
    survival_type : str
        Type of survival analysis (e.g., "Overall Survival", "Progression-Free Survival")
    expression_cutoff_percentile : int
        Percentile cutoff for high/low expression grouping (1-99)
    show_censors : bool
        Whether to show censored data points
    show_ci : bool
        Whether to show confidence intervals around survival curves
    figsize : Tuple[int, int]
        Figure size as (width, height) in inches
    palette : List[str]
        List of two colors for high/low expression groups
    return_fig : bool
        If True, return the figure object
        
    Returns:
    --------
    plt.Figure
        Matplotlib figure object with the survival plot
    """
    # Generate simulated data for demonstration
    np.random.seed(42)  # For reproducibility
    
    # Create a simulated patient dataset
    n_patients = 200
    
    # Create expression data
    expression_values = np.random.exponential(scale=5, size=n_patients)
    
    # Create survival times - using Weibull distribution for more realistic survival data
    # Making high expression patients have different outcomes based on gene
    # For some genes, high expression is good, for others it's bad
    high_expr_coef = 0.8 if gene in ["BRCA1", "PTEN", "TP53"] else 1.2
    
    # Create a dataframe with patient data
    patients = pd.DataFrame({
        'patient_id': [f'P{i:03d}' for i in range(n_patients)],
        'expression': expression_values,
        'time': np.random.weibull(2, n_patients) * 50 * (high_expr_coef if expression_values > np.percentile(expression_values, expression_cutoff_percentile) else 1.0),
        'event': np.random.binomial(1, 0.7, n_patients)  # 1 = event occurred, 0 = censored
    })
    
    # Calculate cutoff based on percentile
    cutoff = np.percentile(patients['expression'], expression_cutoff_percentile)
    
    # Add a group column based on expression cutoff
    patients['group'] = patients['expression'].apply(lambda x: 'High expression' if x > cutoff else 'Low expression')
    
    # Create figure and axes
    fig, ax = plt.subplots(figsize=figsize)
    
    # Initialize KaplanMeierFitter
    kmf = KaplanMeierFitter()
    
    # Plot for low expression group
    low_expr = patients[patients['group'] == 'Low expression']
    kmf.fit(low_expr['time'], low_expr['event'], label=f"Low {gene} expression")
    kmf.plot(ax=ax, ci_show=show_ci, show_censors=show_censors, color=palette[0])
    
    # Plot for high expression group
    high_expr = patients[patients['group'] == 'High expression']
    kmf.fit(high_expr['time'], high_expr['event'], label=f"High {gene} expression")
    kmf.plot(ax=ax, ci_show=show_ci, show_censors=show_censors, color=palette[1])
    
    # Add labels and title
    ax.set_xlabel("Time (months)", fontsize=12)
    ax.set_ylabel("Survival Probability", fontsize=12)
    
    # Handle different survival types
    if survival_type == "Overall Survival":
        title = f"Overall Survival by {gene} Expression"
        y_label = "Overall Survival Probability"
    elif survival_type == "Progression-Free Survival":
        title = f"Progression-Free Survival by {gene} Expression"
        y_label = "Progression-Free Survival Probability"
    elif survival_type == "Disease-Specific Survival":
        title = f"Disease-Specific Survival by {gene} Expression"
        y_label = "Disease-Specific Survival Probability"
    else:
        title = f"Survival Analysis by {gene} Expression"
        y_label = "Survival Probability"
    
    ax.set_title(title, fontsize=14)
    ax.set_ylabel(y_label, fontsize=12)
    
    # Improve visual appearance
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='-', alpha=0.3)
    
    # Add legend
    ax.legend(fontsize=10, frameon=False)
    
    plt.tight_layout()
    
    return fig

