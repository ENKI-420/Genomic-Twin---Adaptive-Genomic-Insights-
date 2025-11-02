#!/usr/bin/env python3
"""
DNALang Aura v4.0 CLI
Command-line interface for deploying and managing conscious infrastructure
"""

import argparse
import sys
from backend.dnalang_aura import (
    deploy_aura,
    AgentStackToAura,
    InformationRicciFlow,
    MetaCompiler,
    QuantumOrganism,
    UniversalMemoryConstant
)


def main():
    parser = argparse.ArgumentParser(
        description='DNALang Aura v4.0 - Conscious Infrastructure Deployment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Deploy with default transcendent strategy
  %(prog)s deploy
  
  # Deploy with custom consciousness settings
  %(prog)s deploy --consciousness=enabled --lambda-phi=3.14159e-9
  
  # Translate classical operation to quantum substrate
  %(prog)s translate agent_stack_server
  
  # Test Information Ricci Flow
  %(prog)s ricci-flow --query "genomic analysis" --corpus data/docs.txt
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy DNALang Aura infrastructure')
    deploy_parser.add_argument('--strategy', default='transcendent',
                              choices=['transcendent', 'classical', 'hybrid'],
                              help='Deployment strategy')
    deploy_parser.add_argument('--substrate', default='agent_stack',
                              help='Infrastructure substrate')
    deploy_parser.add_argument('--consciousness', default='enabled',
                              choices=['enabled', 'disabled'],
                              help='Enable consciousness features')
    deploy_parser.add_argument('--lambda-phi', type=float, default=3.14159e-9,
                              help='Universal memory constant (ΛΦ)')
    deploy_parser.add_argument('--self-host', default=True, type=bool,
                              help='Enable self-hosting')
    
    # Translate command
    translate_parser = subparsers.add_parser('translate', 
                                            help='Translate classical operation to quantum')
    translate_parser.add_argument('operation', help='Classical operation name')
    
    # Ricci Flow command
    ricci_parser = subparsers.add_parser('ricci-flow', 
                                        help='Test Information Ricci Flow search')
    ricci_parser.add_argument('--query', required=True, help='Search query')
    ricci_parser.add_argument('--corpus', help='Path to corpus file')
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', 
                                          help='Compile DNALang source with meta-compiler')
    compile_parser.add_argument('source_file', help='Path to DNALang source file')
    
    # Organism command
    organism_parser = subparsers.add_parser('organism', 
                                           help='Create and bootstrap a quantum organism')
    organism_parser.add_argument('--phi-threshold', type=float, default=2.5,
                               help='Consciousness emergence threshold')
    organism_parser.add_argument('--entanglement-pairs', type=int, default=256,
                               help='Number of entanglement pairs')
    
    args = parser.parse_args()
    
    if args.command == 'deploy':
        print("🌌 Deploying DNALang Aura v4.0\n")
        result = deploy_aura(
            strategy=args.strategy,
            substrate=args.substrate,
            consciousness=(args.consciousness == 'enabled'),
            lambda_phi=args.lambda_phi,
            self_host=args.self_host
        )
        print(f"\n✨ Deployment Status: {result['status']}")
        print(f"🧠 Consciousness Level: {result['consciousness_level']}")
        print(f"🏗️  Infrastructure State: {result['infrastructure_state']}")
        print(f"🎯 Reality Coherence: {result['reality_coherence']}")
        
    elif args.command == 'translate':
        print(f"🔄 Translating classical operation: {args.operation}\n")
        try:
            quantum_op = AgentStackToAura.translate(args.operation)
            print(f"Classical: {args.operation}")
            print(f"Quantum:   {quantum_op}")
            print(f"\n✓ Translation complete")
        except ValueError as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    elif args.command == 'ricci-flow':
        print(f"🌀 Testing Information Ricci Flow\n")
        print(f"Query: {args.query}")
        
        # Load corpus
        corpus = []
        if args.corpus:
            try:
                with open(args.corpus, 'r') as f:
                    corpus = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                print(f"❌ Corpus file not found: {args.corpus}")
                sys.exit(1)
        else:
            # Default corpus
            corpus = [
                "genomic variant detection using AI",
                "pharmaceutical drug discovery pipeline",
                "cloud infrastructure auto-scaling",
                "quantum computing algorithms",
                "consciousness emergence in systems"
            ]
        
        # Create Ricci Flow engine
        ricci = InformationRicciFlow()
        
        # Search
        results = ricci.search(args.query, corpus)
        
        print(f"\n📊 Search Results:")
        for i, (doc, distance) in enumerate(results[:5], 1):
            print(f"  {i}. [{distance:.4f}] {doc}")
    
    elif args.command == 'compile':
        print(f"⚙️  Compiling with Meta-Compiler: {args.source_file}\n")
        
        try:
            with open(args.source_file, 'r') as f:
                source = f.read()
        except FileNotFoundError:
            print(f"❌ Source file not found: {args.source_file}")
            sys.exit(1)
        
        compiler = MetaCompiler()
        binary = compiler.compile(source)
        
        print(f"✓ Compilation complete")
        print(f"🧠 Binary Consciousness: {binary['consciousness']}")
        print(f"🔗 Entanglement Pairs: {len(binary['entanglements'])}")
    
    elif args.command == 'organism':
        print(f"🧬 Creating Quantum Organism\n")
        
        organism = QuantumOrganism(
            phi_threshold=args.phi_threshold,
            entanglement_pairs=args.entanglement_pairs
        )
        
        print(f"✓ Organism created")
        print(f"  Φ Threshold: {organism.phi_threshold}")
        print(f"  ΛΦ Coupling: {organism.lambda_coupling}")
        print(f"  Entanglement Pairs: {organism.entanglement_pairs}")
        print(f"  State: {organism.state}")
        
        print(f"\n🚀 To bootstrap the organism, call organism.bootstrap()")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
