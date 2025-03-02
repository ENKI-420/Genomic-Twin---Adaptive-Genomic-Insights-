#!/usr/bin/env python3

import argparse
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional, Set
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define constants for driver genes and resistance mutations
DRIVER_GENES = ['EGFR', 'KRAS', 'TP53', 'BRAF', 'PIK3CA', 'PTEN', 'ALK', 'ROS1', 'MET', 'ERBB2', 'RET', 'NTRK1', 'NTRK2', 'NTRK3']
RESISTANCE_MUTATIONS = {
    'EGFR': ['T790M', 'C797S', 'L858R', 'exon19del', 'G719X'],
    'KRAS': ['G12C', 'G12D', 'G12V', 'G12A', 'G13D', 'Q61H'],
    'BRAF': ['V600E', 'V600K', 'L597Q'],
    'ALK': ['G1202R', 'L1196M', 'G1269A'],
    'ROS1': ['G2032R', 'D2033N'],
    'MET': ['exon14skip', 'D1228N', 'Y1230H'],
}

# Clinical significance categories
CLINICAL_SIGNIFICANCE = {
    'therapeutic': ['drug_response', 'responsive', 'resistance', 'poor_response'],
    'pathogenic': ['pathogenic', 'likely_pathogenic', 'risk_factor'],
    'benign': ['benign', 'likely_benign'],
    'uncertain': ['uncertain_significance', 'conflicting_interpretations', 'other']
}

# Mapping of canonical annotation names between different annotation tools
ANNOTATION_FIELD_MAPPING = {
    'snpeff': {
        'gene': 3,           # Gene Name index
        'impact': 2,         # Impact index
        'transcript': 6,     # Transcript ID index
        'mutation': 10,      # HGVS.p index (protein change)
        'cdna_change': 9,    # HGVS.c index (coding DNA change)
        'effect': 1,         # Effect (missense, frameshift, etc.)
    },
    'vep': {
        'gene': 3,           # SYMBOL field index
        'impact': 4,         # IMPACT field index
        'transcript': 6,     # Feature field index
        'mutation': 11,      # HGVSp field index
        'cdna_change': 10,   # HGVSc field index
        'effect': 1,         # Consequence field index
    }
}

class MutationAnalyzer:
    """
    Class for analyzing genomic mutations from VCF files.
    
    This class provides methods to:
    - Parse VCF files with SNPEff and VEP annotations
    - Extract detailed mutation information
    - Identify clinically relevant variants
    - Analyze mutations for driver genes and resistance markers
    """
    
    @staticmethod
    def _identify_annotation_format(info_field: str) -> str:
        """
        Identify the annotation format used in the VCF file (SNPEff or VEP)
        
        Args:
            info_field: The INFO field from a VCF line
            
        Returns:
            String indicating the annotation format ('snpeff', 'vep', or None)
        """
        if 'ANN=' in info_field:
            return 'snpeff'
        elif 'CSQ=' in info_field:
            return 'vep'
        return None
    
    @staticmethod
    def _extract_annotation_entry(info_field: str, ann_format: str) -> List[str]:
        """
        Extract annotation entries from the INFO field based on annotation format
        
        Args:
            info_field: The INFO field from a VCF line
            ann_format: The annotation format ('snpeff' or 'vep')
            
        Returns:
            List of annotation entries (split by pipe '|')
        """
        if ann_format == 'snpeff':
            for part in info_field.split(';'):
                if part.startswith('ANN='):
                    ann_entries = part[4:].split(',')
                    if ann_entries:
                        return ann_entries[0].split('|')  # Return first annotation
        
        elif ann_format == 'vep':
            for part in info_field.split(';'):
                if part.startswith('CSQ='):
                    ann_entries = part[4:].split(',')
                    if ann_entries:
                        return ann_entries[0].split('|')  # Return first annotation
        
        return []
    
    @staticmethod
    def _standardize_hgvs_notation(mutation: str) -> str:
        """
        Standardize HGVS notation for mutations
        
        Args:
            mutation: HGVS mutation string (e.g., p.Val600Glu, p.V600E)
            
        Returns:
            Standardized mutation string
        """
        if not mutation or mutation == '.':
            return ""
            
        # Remove the prefix if it exists (p. or c.)
        if mutation.startswith(('p.', 'c.')):
            mutation = mutation[2:]
            
        # Standardize three-letter amino acid codes to one-letter
        aa_map = {
            'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D', 'Cys': 'C',
            'Gln': 'Q', 'Glu': 'E', 'Gly': 'G', 'His': 'H', 'Ile': 'I',
            'Leu': 'L', 'Lys': 'K', 'Met': 'M', 'Phe': 'F', 'Pro': 'P',
            'Ser': 'S', 'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V',
            'Ter': '*', 'Stop': '*', 'del': 'del', 'ins': 'ins', 'dup': 'dup',
            'fs': 'fs'
        }
        
        # Convert three-letter to one-letter amino acid code
        for three_letter, one_letter in aa_map.items():
            mutation = mutation.replace(three_letter, one_letter)
            
        # Handle special cases like exon skipping
        if 'exon' in mutation.lower() and 'skip' in mutation.lower():
            return 'exonskip'
            
        return mutation
    
    @staticmethod
    def _extract_clinical_significance(info_field: str) -> List[str]:
        """
        Extract clinical significance from INFO field
        
        Args:
            info_field: The INFO field from a VCF line
            
        Returns:
            List of clinical significance terms
        """
        clinical_sig = []
        
        # Extract clinical significance from various annotation formats
        patterns = [
            r'CLNSIG=([^;]+)',  # ClinVar format
            r'Clinical_significance=([^;]+)',  # Some VEP annotations
            r'clinvar_sig=([^;]+)',  # SNPEff ClinVar annotations
        ]
        
        for pattern in patterns:
            match = re.search(pattern, info_field)
            if match:
                sig_values = match.group(1).lower().replace('_', ' ').split('|')
                clinical_sig.extend(sig_values)
        
        return clinical_sig
    
    @staticmethod
    def _determine_clinical_category(clinical_terms: List[str]) -> str:
        """
        Determine the clinical category based on clinical significance terms
        
        Args:
            clinical_terms: List of clinical significance terms
            
        Returns:
            Clinical category (therapeutic, pathogenic, benign, uncertain)
        """
        if not clinical_terms:
            return 'unknown'
            
        for category, terms in CLINICAL_SIGNIFICANCE.items():
            for term in clinical_terms:
                if any(t in term for t in terms):
                    return category
                    
        return 'unknown'
    
    @staticmethod
    def analyze_vcf(vcf_path: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Parse a VCF file and extract mutation information with detailed annotations.
        
        Args:
            vcf_path: Path to the VCF file
            
        Returns:
            Tuple containing:
                - DataFrame with columns: gene, mutation, impact, effect, transcript, 
                  cdna_change, clinical_significance, clinical_category
                - Dictionary mapping (gene, mutation) tuples to impact levels
        """
        if not os.path.exists(vcf_path):
            raise FileNotFoundError(f"VCF file not found: {vcf_path}")
        
        logger.info(f"Analyzing VCF file: {vcf_path}")
        
        mutations = []
        impact_dict = {}
        annotation_format = None
        processed_lines = 0
        annotation_found = 0
        
        with open(vcf_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                # Process header lines to identify annotation format
                if line.startswith('##INFO=<ID=ANN'):
                    annotation_format = 'snpeff'
                    logger.info("Detected SNPEff annotation format")
                elif line.startswith('##INFO=<ID=CSQ'):
                    annotation_format = 'vep'
                    logger.info("Detected VEP annotation format")
                    
                # Skip other header lines
                if line.startswith('#'):
                    continue
                
                processed_lines += 1
                fields = line.strip().split('\t')
                if len(fields) < 8:
                    logger.warning(f"Line {line_num}: Malformed VCF entry, skipping")
                    continue
                
                chrom = fields[0]
                pos = fields[1]
                ref = fields[3]
                alt = fields[4]
                info = fields[7]  # INFO field contains annotations
                
                # If annotation format wasn't detected from headers, try to identify from content
                if not annotation_format:
                    annotation_format = MutationAnalyzer._identify_annotation_format(info)
                    
                if not annotation_format:
                    logger.warning(f"Line {line_num}: No annotation format detected, skipping")
                    continue
                
                # Extract annotation entries
                ann_parts = MutationAnalyzer._extract_annotation_entry(info, annotation_format)
                if not ann_parts:
                    logger.warning(f"Line {line_num}: No annotation entries found, skipping")
                    continue
                
                annotation_found += 1
                
                # Extract fields based on annotation format
                field_indices = ANNOTATION_FIELD_MAPPING.get(annotation_format, {})
                
                # Extract gene and mutation information
                try:
                    gene = ann_parts[field_indices.get('gene', 0)] if len(ann_parts) > field_indices.get('gene', 0) else ''
                    impact = ann_parts[field_indices.get('impact', 0)] if len(ann_parts) > field_indices.get('impact', 0) else ''
                    effect = ann_parts[field_indices.get('effect', 0)] if len(ann_parts) > field_indices.get('effect', 0) else ''
                    transcript = ann_parts[field_indices.get('transcript', 0)] if len(ann_parts) > field_indices.get('transcript', 0) else ''
                    cdna_change = ann_parts[field_indices.get('cdna_change', 0)] if len(ann_parts) > field_indices.get('cdna_change', 0) else ''
                    
                    # Get mutation from protein notation if available, otherwise use cDNA
                    raw_mutation = ann_parts[field_indices.get('mutation', 0)] if len(ann_parts) > field_indices.get('mutation', 0) else ''
                    mutation = MutationAnalyzer._standardize_hgvs_notation(raw_mutation)
                    
                    # If protein mutation is not available, try to use the effect
                    if not mutation and effect:
                        mutation = effect.lower()
                    
                    # Skip entries with no gene or mutation information
                    if not gene or gene == '.':
                        continue
                    
                    # Extract clinical significance
                    clinical_terms = MutationAnalyzer._extract_clinical_significance(info)
                    clinical_category = MutationAnalyzer._determine_clinical_category(clinical_terms)
                    
                    # Create location string for variants without protein notation
                    location = f"{chrom}:{pos}_{ref}>{alt}"
                    
                    # Collect mutation information
                    mutation_data = {
                        'gene': gene,
                        'mutation': mutation if mutation else location,
                        'impact': impact.upper() if impact else 'UNKNOWN',
                        'effect': effect,
                        'transcript': transcript,
                        'cdna_change': cdna_change,
                        'clinical_significance': '|'.join(clinical_terms) if clinical_terms else 'unknown',
                        'clinical_category': clinical_category,
                        'chromosome': chrom,
                        'position': pos,
                        'ref': ref,
                        'alt': alt
                    }
                    
                    mutations.append(mutation_data)
                    
                    # Update impact dictionary
                    impact_dict[(gene, mutation if mutation else location)] = impact.upper() if impact else 'UNKNOWN'
                    
                except Exception as e:
                    logger.warning(f"Line {line_num}: Error processing annotation: {e}")
                    continue
        
        logger.info(f"Processed {processed_lines} variant lines, found {annotation_found} annotated variants")
        logger.info(f"Extracted {len(mutations)} mutations from {annotation_found} annotated variants")
        
        # Convert to DataFrame
        mutations_df = pd.DataFrame(mutations)
        
        # If DataFrame is empty, return empty DataFrame with expected columns
        if mutations_df.empty:
            columns = ['gene', 'mutation', 'impact', 'effect', 'transcript', 'cdna_change', 
                      'clinical_significance', 'clinical_category', 'chromosome', 'position', 'ref', 'alt']
            mutations_df = pd.DataFrame(columns=columns)
        
        return mutations_df, impact_dict

    @staticmethod
    def predict_mutation_impact(mutation_data: pd.DataFrame) -> Dict:
        """
        Advanced analysis to predict mutation impact on protein function and stability
        
        Args:
            mutation_data: DataFrame with mutation information
            
        Returns:
            Dictionary mapping mutations to predicted functional impact
        """
        # This is a placeholder for more advanced analysis
        # In a real implementation, this could include calls to prediction tools
        # or more sophisticated algorithms
        
        impact_predictions = {}
        
        # Simple heuristic-based predictions
        for _, row in mutation_data.iterrows():
            gene = row['gene']
            mutation = row['mutation']
            effect = row.get('effect', '').lower()
            
            prediction = 'uncertain'
            
            # Simple rules for prediction
            if any(term in effect for term in ['frameshift', 'nonsense', 'stop_gained']):
                prediction = 'loss_of_function'
            elif any(term in effect for term in ['missense', 'non_synonymous']):
                prediction = 'potentially_damaging'
            elif any(term in effect for term in ['synonymous', 'silent']):
                prediction = 'benign'
            elif any(term in effect for term in ['splice', 'donor', 'acceptor']):
                prediction = 'splicing_affected'
            
            impact_predictions[(gene, mutation)] = prediction
            
        return impact_predictions

def analyze_mutations(vcf_path: str) -> Dict:
    """
    Analyze mutations from a VCF file to identify driver mutations,
    resistance markers, and recommend therapies.
    
    Args:
        vcf_path: Path to the VCF file
        
    Returns:
        Dictionary containing analysis results: drivers, resistance, therapies,
        clinical_variants, and summary statistics
    """
    # Parse the VCF file
    mutations_df, impact_dict = MutationAnalyzer.analyze_vcf(vcf_path)
    
    if mutations_df.empty:
        return {
            'drivers': pd.DataFrame(columns=['gene', 'mutation', 'impact']),
            'resistance': {},
            'therapies': [],
            'clinical_variants': pd.DataFrame(columns=['gene', 'mutation', 'clinical_category']),
            'statistics': {'total_variants': 0, 'driver_genes': 0, 'resistance_markers': 0}
        }
    
    # Identify driver mutations (high or moderate impact mutations in driver genes)
    drivers = mutations_df[
        (mutations_df['gene'].isin(DRIVER_GENES)) & 
        (mutations_df['impact'].isin(['HIGH', 'MODERATE']))
    ].reset_index(drop=True)
    
    # Identify resistance mutations
    resistance = {}
    for gene, mut_list in RESISTANCE_MUTATIONS.items():
        gene_mutations = mutations_df[
            (mutations_df['gene'] == gene) & 
            (mutations_df['mutation'].isin(mut_list))
        ]
        if not gene_mutations.empty:
            resistance[gene] = gene_mutations['mutation'].tolist()
    
    # Suggest therapies based on driver mutations and resistance markers
    therapies = []
    
    # EGFR therapy recommendations
    if 'EGFR' in drivers['gene'].values:
        if 'EGFR' not in resistance:
            therapies.append('Erlotinib (EGFR inhibitor)')
        elif 'T790M' in resistance.get('EGFR', []):
            therapies.append('Osimertinib (third-generation EGFR inhibitor)')
        else:
            therapies.append('Consider alternative EGFR targeting strategy')
    
    # BRAF therapy recommendations
    braf_mutations = drivers[drivers['gene'] == 'BRAF']
    if not braf_mutations.empty and any('V600E' in m for m in braf_mutations['mutation']):
        therapies.append('Vemurafenib (BRAF inhibitor)')
    
    # KRAS therapy recommendations
    kras_mutations = drivers[drivers['gene'] == 'KRAS']
    if not kras_mutations.empty:
        if any('G12C' in m for m in kras_mutations['mutation']):
            therapies.append('Sotorasib (KRAS G12C inhibitor)')
        else:
            therapies.append('Consider MEK inhibitors for KRAS mutations')
    
    # Identify clinically significant variants
    clinical_variants = mutations_df[
        (mutations_df['clinical_category'].isin(['therapeutic', 'pathogenic'])) |
        ((mutations_df['gene'].isin(DRIVER_GENES)) & 
         (mutations_df['impact'].isin(['HIGH', 'MODERATE'])))
    ].reset_index(drop=True)
    
    # Generate summary statistics
    statistics = {
        'total_variants': len(mutations_df),
        'driver_genes': len(drivers),
        'resistance_markers': sum(len(muts) for muts in resistance.values()),
        'clinical_variants': len(clinical_variants),
        'high_impact': len(mutations_df[mutations_df['impact'] == 'HIGH']),
        'moderate_impact': len(mutations_df[mutations_df['impact'] == 'MODERATE']),
        'low_impact': len(mutations_df[mutations_df['impact'] == 'LOW']),
        'unknown_impact': len(mutations_df[mutations_df['impact'] == 'UNKNOWN'])
    }
    
    # Get additional impact predictions if available
    impact_predictions = MutationAnalyzer.predict_mutation_impact(mutations_df)
    
    return {
        'drivers': drivers,
        'resistance': resistance,
        'therapies': therapies,
        'clinical_variants': clinical_variants,
        'statistics': statistics,
        'impact_predictions': impact_predictions,
        'all_variants': mutations_df
    }


def visualize_mutations(analysis_results: Dict) -> None:
    """
    Create visualizations of mutation analysis results.
    
    Args:
        analysis_results: Dictionary containing analysis results
    """
    drivers = analysis_results['drivers']
    
    # Create a figure with 2 subplots
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Driver mutations by gene
    plt.subplot(2, 2, 1)
    if not drivers.empty:
        gene_counts = drivers['gene'].value_counts()
        gene_counts.plot(kind='bar', color='skyblue')
        plt.title('Driver Mutations by Gene')
        plt.xlabel('Gene')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
    else:
        plt.text(0.5, 0.5, 'No driver mutations identified', 
                 horizontalalignment='center', verticalalignment='center')
    
    # Plot 2: Impact distribution
    plt.subplot(2, 2, 2)
    if 'impact' in drivers.columns and not drivers.empty:
        impact_counts = drivers['impact'].value_counts()
        impact_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Mutation Impact Distribution')
        plt.ylabel('')
    else:
        plt.text(0.5, 0.5, 'No impact data available', 
                 horizontalalignment='center', verticalalignment='center')
    
    # Plot 3: Clinical significance distribution
    plt.subplot(2, 2, 3)
    if 'clinical_category' in analysis_results.get('all_variants', pd.DataFrame()).columns:
        variants_df = analysis_results.get('all_variants', pd.DataFrame())
        if not variants_df.empty:
            clinical_counts = variants_df['clinical_category'].value_counts()
            clinical_counts.plot(kind='bar', color='lightgreen')
            plt.title('Clinical Significance Distribution')
            plt.xlabel('Category')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
        else:
            plt.text(0.5, 0.5, 'No clinical significance data available', 
                     horizontalalignment='center', verticalalignment='center')
    else:
        plt.text(0.5, 0.5, 'No clinical significance data available', 
                 horizontalalignment='center', verticalalignment='center')
    
    # Plot 4: Resistance mutations
    plt.subplot(2, 2, 4)
    resistance = analysis_results.get('resistance', {})
    if resistance:
        genes = list(resistance.keys())
        counts = [len(mutations) for mutations in resistance.values()]
        plt.bar(genes, counts, color='salmon')
        plt.title('Resistance Mutations by Gene')
        plt.xlabel('Gene')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
    else:
        plt.text(0.5, 0.5, 'No resistance mutations identified', 
                 horizontalalignment='center', verticalalignment='center')
    
    plt.tight_layout()
    plt.show()


def main():
    """
    Main function providing a command-line interface for mutation analysis.
    """
    parser = argparse.ArgumentParser(description='Analyze genomic mutations from VCF files')
    parser.add_argument('vcf_file', help='Path to the VCF file to analyze')
    parser.add_argument('--no-plot', action='store_true', help='Disable plotting')
    parser.add_argument('--output', '-o', help='Save results to file')
    
    args = parser.parse_args()
    
    try:
        # Analyze mutations
        print(f"Analyzing mutations in {args.vcf_file}...")
        results = analyze_mutations(args.vcf_file)
        
        # Display results
        print("\nResults Summary:")
        stats = results.get('statistics', {})
        print(f"- Total Variants: {stats.get('total_variants', 0)}")
        print(f"- Driver Mutations: {len(results['drivers'])} identified")
        print(f"- Resistance Markers: {len(results['resistance'])} genes")
        print(f"- Clinical Variants: {stats.get('clinical_variants', 0)} identified")
        print(f"- Recommended Therapies: {len(results['therapies'])}")
        print(f"- Driver Mutations: {len(results['drivers'])} identified")
        print(f"- Resistance Markers: {len(results['resistance'])} genes")
        print(f"- Recommended Therapies: {len(results['therapies'])}")
        
        # Show detailed results
        if not results['drivers'].empty:
            print("\nDriver Mutations:")
            print(results['drivers'][['gene', 'mutation', 'impact']])
        
        if results['resistance']:
            print("\nResistance Markers:")
            for gene, mutations in results['resistance'].items():
                print(f"- {gene}: {', '.join(mutations)}")
        
        if results['therapies']:
            print("\nRecommended Therapies:")
            for therapy in results['therapies']:
                print(f"- {therapy}")
        
        # Generate visualizations
        if not args.no_plot:
            visualize_mutations(results)
        
        # Save results if requested
        # Save results if requested
        if args.output:
            results['drivers'].to_csv(f"{args.output}_drivers.csv", index=False)
            
            # Save all variants to a CSV file
            if 'all_variants' in results and not results['all_variants'].empty:
                results['all_variants'].to_csv(f"{args.output}_all_variants.csv", index=False)
                
            # Save statistics as text
            with open(f"{args.output}_summary.txt", 'w') as f:
                f.write("Mutation Analysis Summary\n")
                f.write("========================\n\n")
                f.write(f"VCF File: {args.vcf_file}\n\n")
                f.write("Statistics:\n")
                for key, value in stats.items():
                    f.write(f"- {key}: {value}\n")
                
                f.write("\nDriver Mutations:\n")
                if not results['drivers'].empty:
                    f.write(results['drivers'][['gene', 'mutation', 'impact']].to_string(index=False))
                else:
                    f.write("None identified\n")
                
                f.write("\nResistance Markers:\n")
                if results['resistance']:
                    for gene, mutations in results['resistance'].items():
                        f.write(f"- {gene}: {', '.join(mutations)}\n")
                else:
                    f.write("None identified\n")
                
                f.write("\nRecommended Therapies:\n")
                if results['therapies']:
                    for therapy in results['therapies']:
                        f.write(f"- {therapy}\n")
                else:
                    f.write("None recommended\n")
                
            print(f"Results saved to {args.output}_*.csv/txt")
    except Exception as e:
        print(f"Error analyzing mutations: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())


