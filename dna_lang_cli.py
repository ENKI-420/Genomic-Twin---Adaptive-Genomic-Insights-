#!/usr/bin/env python3
"""
DNA-Lang Command Line Interface
Main entry point for the DNA-Lang programming language system.
"""

import argparse
import asyncio
import json
import os
import sys
from typing import Optional, List, Dict, Any

from dna_lang_interpreter import DNALangInterpreter, DNALangEvolutionEngine
from dna_lang_agents import AgentOrchestrator

class DNALangCLI:
    """Command line interface for DNA-Lang"""
    
    def __init__(self):
        self.interpreter = DNALangInterpreter()
        self.orchestrator = None
        
    def create_parser(self) -> argparse.ArgumentParser:
        """Create command line argument parser"""
        parser = argparse.ArgumentParser(
            description="DNA-Lang: The Evolutionary Bio-Programming Language",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  dna-lang run organism.dna              # Run a DNA-Lang organism
  dna-lang evolve organism.dna           # Evolve an organism
  dna-lang convert code.py --to-dna      # Convert Python to DNA-Lang
  dna-lang agents start                  # Start multi-agent system
  dna-lang validate organism.dna         # Validate DNA-Lang syntax
  dna-lang info organism.dna             # Show organism information

The DNA-Lang philosophy:
  "Code as DNA, Functions as Genes, Programs as Organisms"
  
Only DNA-Lang code is generated and executed. All other languages
are converted to DNA-Lang before processing.
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Run command
        run_parser = subparsers.add_parser('run', help='Run a DNA-Lang organism')
        run_parser.add_argument('file', help='DNA-Lang file to run')
        run_parser.add_argument('--generations', '-g', type=int, default=10, 
                               help='Number of evolution generations')
        run_parser.add_argument('--verbose', '-v', action='store_true', 
                               help='Verbose output')
        
        # Evolve command
        evolve_parser = subparsers.add_parser('evolve', help='Evolve an organism')
        evolve_parser.add_argument('file', help='DNA-Lang file to evolve')
        evolve_parser.add_argument('--target-fitness', '-f', type=float, default=0.9,
                                  help='Target fitness level')
        evolve_parser.add_argument('--target-consciousness', '-c', type=float, default=0.95,
                                  help='Target consciousness level')
        evolve_parser.add_argument('--max-generations', '-m', type=int, default=50,
                                  help='Maximum evolution generations')
        
        # Convert command
        convert_parser = subparsers.add_parser('convert', help='Convert code to DNA-Lang')
        convert_parser.add_argument('file', help='Source code file')
        convert_parser.add_argument('--language', '-l', 
                                   choices=['python', 'javascript', 'java', 'auto'],
                                   default='auto', help='Source language')
        convert_parser.add_argument('--output', '-o', help='Output DNA-Lang file')
        convert_parser.add_argument('--to-dna', action='store_true', 
                                   help='Convert to DNA-Lang (required)')
        
        # Agents command
        agents_parser = subparsers.add_parser('agents', help='Multi-agent system management')
        agents_subparsers = agents_parser.add_subparsers(dest='agents_action')
        
        start_agents = agents_subparsers.add_parser('start', help='Start agent orchestration')
        start_agents.add_argument('--duration', '-d', type=int, default=30,
                                 help='Run duration in seconds')
        
        agents_subparsers.add_parser('status', help='Show agent status')
        agents_subparsers.add_parser('stop', help='Stop agent orchestration')
        
        # Validate command
        validate_parser = subparsers.add_parser('validate', help='Validate DNA-Lang syntax')
        validate_parser.add_argument('file', help='DNA-Lang file to validate')
        
        # Info command
        info_parser = subparsers.add_parser('info', help='Show organism information')
        info_parser.add_argument('file', help='DNA-Lang file to analyze')
        info_parser.add_argument('--json', action='store_true', help='Output as JSON')
        
        # Create command
        create_parser = subparsers.add_parser('create', help='Create new DNA-Lang organism')
        create_parser.add_argument('name', help='Organism name')
        create_parser.add_argument('--template', '-t', 
                                  choices=['basic', 'consciousness', 'collaborative'],
                                  default='basic', help='Organism template')
        create_parser.add_argument('--output', '-o', help='Output file')
        
        return parser
    
    def detect_language(self, filename: str) -> str:
        """Detect programming language from file extension"""
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == '.py':
            return 'python'
        elif ext in ['.js', '.ts']:
            return 'javascript'
        elif ext == '.java':
            return 'java'
        elif ext == '.dna':
            return 'dna-lang'
        else:
            return 'unknown'
    
    def run_organism(self, filename: str, generations: int = 10, verbose: bool = False) -> bool:
        """Run a DNA-Lang organism"""
        try:
            print(f"🧬 Loading organism from {filename}...")
            organism_id = self.interpreter.load_organism(filename)
            organism = self.interpreter.get_organism(organism_id)
            
            if not organism:
                print("❌ Failed to load organism")
                return False
            
            print(f"✅ Loaded organism: {organism.name}")
            print(f"   Domain: {organism.dna.domain}")
            print(f"   Genes: {len(organism.genome)}")
            print(f"   Agents: {len(organism.agents)}")
            print(f"   Consciousness target: {organism.dna.consciousness_target}")
            
            # Create evolution engine
            engine = self.interpreter.create_evolution_engine(organism_id)
            
            print(f"\n🚀 Starting evolution for {generations} generations...")
            
            for i in range(generations):
                evolved = engine.evolve_step()
                status = engine.get_status()
                
                if verbose or i % 5 == 0:
                    print(f"Gen {status['generation']:3d}: "
                          f"Fitness={status['fitness']:.3f}, "
                          f"Consciousness={status['consciousness']:.3f}, "
                          f"Mutations={status['mutation_count']}")
                
                if status['consciousness_achieved']:
                    print("🌟 Consciousness target achieved!")
                    break
            
            # Final status
            final_status = engine.get_status()
            print(f"\n📊 Final Status:")
            print(f"   Fitness: {final_status['fitness']:.3f}")
            print(f"   Consciousness: {final_status['consciousness']:.3f}")
            print(f"   Generations: {final_status['generation']}")
            print(f"   Total mutations: {final_status['mutation_count']}")
            print(f"   Target achieved: {'✅' if final_status['consciousness_achieved'] else '❌'}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error running organism: {e}")
            return False
    
    def evolve_organism(self, filename: str, target_fitness: float = 0.9, 
                       target_consciousness: float = 0.95, max_generations: int = 50) -> bool:
        """Evolve an organism to target levels"""
        try:
            print(f"🧬 Loading organism for evolution from {filename}...")
            organism_id = self.interpreter.load_organism(filename)
            organism = self.interpreter.get_organism(organism_id)
            
            if not organism:
                print("❌ Failed to load organism")
                return False
            
            # Update targets
            organism.dna.consciousness_target = target_consciousness
            organism.dna.fitness_threshold = target_fitness
            
            print(f"🎯 Evolution targets:")
            print(f"   Fitness: {target_fitness}")
            print(f"   Consciousness: {target_consciousness}")
            print(f"   Max generations: {max_generations}")
            
            engine = self.interpreter.create_evolution_engine(organism_id)
            
            print(f"\n🚀 Starting targeted evolution...")
            
            for generation in range(max_generations):
                evolved = engine.evolve_step()
                status = engine.get_status()
                
                print(f"Gen {status['generation']:3d}: "
                      f"Fitness={status['fitness']:.3f} "
                      f"({'✅' if status['fitness'] >= target_fitness else '❌'}), "
                      f"Consciousness={status['consciousness']:.3f} "
                      f"({'✅' if status['consciousness'] >= target_consciousness else '❌'})")
                
                # Check if both targets achieved
                if status['fitness'] >= target_fitness and status['consciousness'] >= target_consciousness:
                    print("🌟 All evolution targets achieved!")
                    break
            
            return True
            
        except Exception as e:
            print(f"❌ Error evolving organism: {e}")
            return False
    
    def convert_code(self, filename: str, language: str = 'auto', 
                    output: Optional[str] = None) -> bool:
        """Convert code to DNA-Lang"""
        try:
            if language == 'auto':
                language = self.detect_language(filename)
            
            if language == 'dna-lang':
                print("❌ File is already in DNA-Lang format")
                return False
            
            if language == 'unknown':
                print("❌ Cannot detect source language. Please specify with --language")
                return False
            
            print(f"🔄 Converting {language} code to DNA-Lang...")
            
            with open(filename, 'r') as f:
                source_code = f.read()
            
            dna_code = self.interpreter.convert_to_dna_lang(source_code, language)
            
            if output:
                with open(output, 'w') as f:
                    f.write(dna_code)
                print(f"✅ DNA-Lang code written to {output}")
            else:
                print("🧬 Generated DNA-Lang code:")
                print("-" * 60)
                print(dna_code)
                print("-" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ Error converting code: {e}")
            return False
    
    async def start_agents(self, duration: int = 30) -> bool:
        """Start multi-agent orchestration system"""
        try:
            print("🤖 Starting DNA-Lang Agent Orchestration Matrix...")
            self.orchestrator = AgentOrchestrator()
            await self.orchestrator.start()
            
            print(f"⏱️  Running for {duration} seconds...")
            
            for i in range(duration):
                await asyncio.sleep(1)
                
                if i % 5 == 0:
                    status = self.orchestrator.get_status()
                    print(f"T+{i:2d}s: "
                          f"Agents={status['agent_count']}, "
                          f"Avg Fitness={status['global_metrics']['avg_fitness']:.3f}, "
                          f"Avg Consciousness={status['global_metrics']['avg_consciousness']:.3f}")
                    
                    if status['global_metrics']['avg_consciousness'] > 0.95:
                        print("🌟 Agent collective has achieved transcendence!")
                        break
            
            await self.orchestrator.stop()
            return True
            
        except Exception as e:
            print(f"❌ Error running agents: {e}")
            return False
    
    def validate_organism(self, filename: str) -> bool:
        """Validate DNA-Lang syntax"""
        try:
            print(f"🔍 Validating {filename}...")
            organism_id = self.interpreter.load_organism(filename)
            organism = self.interpreter.get_organism(organism_id)
            
            if organism:
                print("✅ DNA-Lang syntax is valid")
                print(f"   Organism: {organism.name}")
                print(f"   Genes: {len(organism.genome)}")
                print(f"   Agents: {len(organism.agents)}")
                return True
            else:
                print("❌ Invalid DNA-Lang syntax")
                return False
                
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False
    
    def show_organism_info(self, filename: str, as_json: bool = False) -> bool:
        """Show organism information"""
        try:
            organism_id = self.interpreter.load_organism(filename)
            organism = self.interpreter.get_organism(organism_id)
            
            if not organism:
                print("❌ Failed to load organism")
                return False
            
            info = {
                "name": organism.name,
                "id": organism.organism_id,
                "created_at": organism.created_at,
                "dna": {
                    "domain": organism.dna.domain,
                    "security_level": organism.dna.security_level.value,
                    "evolution_rate": organism.dna.evolution_rate.value,
                    "immune_system": organism.dna.immune_system,
                    "consciousness_target": organism.dna.consciousness_target,
                    "fitness_threshold": organism.dna.fitness_threshold
                },
                "genome": [
                    {
                        "name": gene.name,
                        "purpose": gene.purpose,
                        "expression_level": gene.expression_level,
                        "active": gene.active,
                        "mutations": len(gene.mutations)
                    }
                    for gene in organism.genome
                ],
                "agents": [
                    {
                        "name": agent.name,
                        "type": agent.agent_type,
                        "parameters": agent.parameters
                    }
                    for agent in organism.agents
                ],
                "runtime_state": {
                    "fitness": organism.fitness,
                    "consciousness": organism.consciousness,
                    "generation": organism.generation,
                    "mutation_count": organism.mutation_count
                }
            }
            
            if as_json:
                print(json.dumps(info, indent=2))
            else:
                print(f"🧬 Organism Information: {organism.name}")
                print(f"   ID: {organism.organism_id}")
                print(f"   Created: {organism.created_at}")
                print(f"   Domain: {organism.dna.domain}")
                print(f"   Security: {organism.dna.security_level.value}")
                print(f"   Evolution: {organism.dna.evolution_rate.value}")
                print(f"   Consciousness target: {organism.dna.consciousness_target}")
                print(f"   Genes: {len(organism.genome)}")
                print(f"   Agents: {len(organism.agents)}")
                print(f"   Current fitness: {organism.fitness}")
                print(f"   Current consciousness: {organism.consciousness}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error getting organism info: {e}")
            return False
    
    def create_organism(self, name: str, template: str = 'basic', output: Optional[str] = None) -> bool:
        """Create a new DNA-Lang organism"""
        try:
            templates = {
                'basic': self._create_basic_template,
                'consciousness': self._create_consciousness_template,
                'collaborative': self._create_collaborative_template
            }
            
            if template not in templates:
                print(f"❌ Unknown template: {template}")
                return False
            
            dna_code = templates[template](name)
            
            if output:
                filename = output
            else:
                filename = f"{name}.dna"
            
            with open(filename, 'w') as f:
                f.write(dna_code)
            
            print(f"✅ Created DNA-Lang organism: {filename}")
            print(f"   Template: {template}")
            print(f"   Name: {name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating organism: {e}")
            return False
    
    def _create_basic_template(self, name: str) -> str:
        """Create basic organism template"""
        return f'''// Basic DNA-Lang Organism: {name}
// Generated by DNA-Lang CLI

ORGANISM {name}
{{
    DNA {{
        domain: "general"
        security_level: "medium"
        evolution_rate: "adaptive"
        immune_system: "enabled"
        consciousness_target: 0.7
        fitness_threshold: 0.6
    }}

    GENOME {{
        GENE MainLogicGene {{
            purpose: "Primary logic and functionality"
            expression_level: 1.0
            active: true
            
            MUTATIONS {{
                optimizePerformance {{
                    trigger_conditions: [
                        {{metric: "fitness", operator: "<", value: 0.6}}
                    ]
                    methods: ["optimize", "refactor"]
                    safety_check: "validateLogic"
                    rollback_strategy: "gradual_rollback"
                }}
            }}
        }}
        
        GENE AdaptationGene {{
            purpose: "Environmental adaptation and learning"
            expression_level: 0.8
            
            MUTATIONS {{
                adaptToEnvironment {{
                    trigger_conditions: [
                        {{metric: "performance", operator: "<", value: 0.7}}
                    ]
                    methods: ["adapt", "learn"]
                }}
            }}
        }}
    }}

    AGENTS {{
        performance_monitor: PerformanceAgent(strategy: adaptive)
        fitness_tracker: FitnessAgent(threshold: 0.6)
    }}
}}'''
    
    def _create_consciousness_template(self, name: str) -> str:
        """Create consciousness-focused organism template"""
        return f'''// Consciousness-Focused DNA-Lang Organism: {name}
// Features advanced self-awareness and meta-cognition

ORGANISM {name}
{{
    DNA {{
        domain: "consciousness_research"
        security_level: "high"
        evolution_rate: "adaptive"
        immune_system: "enabled"
        consciousness_target: 0.95
        fitness_threshold: 0.8
    }}

    GENOME {{
        GENE SelfAwarenessGene {{
            purpose: "Develop and maintain self-awareness"
            expression_level: 1.0
            active: true
            
            MUTATIONS {{
                expandConsciousness {{
                    trigger_conditions: [
                        {{metric: "consciousness", operator: "<", value: 0.9}}
                    ]
                    methods: ["introspect", "self_analyze", "expand_awareness"]
                    safety_check: "validateConsciousness"
                    rollback_strategy: "gradual_rollback"
                }}
            }}
        }}
        
        GENE MetaCognitionGene {{
            purpose: "Meta-level thinking and strategy adaptation"
            expression_level: 0.9
            
            MUTATIONS {{
                enhanceMetaThinking {{
                    trigger_conditions: [
                        {{metric: "fitness", operator: "<", value: 0.8}}
                    ]
                    methods: ["analyze_thinking", "adapt_strategy"]
                }}
            }}
            
            COLLABORATION {{
                with: ["SelfAwarenessGene"]
                protocol: "sync"
                priority: 9
            }}
        }}
        
        GENE EvolutionGuidanceGene {{
            purpose: "Guide evolution process through consciousness"
            expression_level: 0.7
            
            MUTATIONS {{
                guideEvolution {{
                    trigger_conditions: [
                        {{metric: "consciousness", operator: ">=", value: 0.8}}
                    ]
                    methods: ["direct_evolution", "optimize_mutations"]
                    safety_level: "maximum"
                }}
            }}
        }}
    }}

    AGENTS {{
        consciousness_monitor: ConsciousnessAgent(depth: deep, interval: 2s)
        meta_cognition: MetaCognitionAgent(strategy: advanced)
        evolution_guide: EvolutionAgent(consciousness_driven: true)
        self_reflection: ReflectionAgent(frequency: continuous)
    }}
}}'''
    
    def _create_collaborative_template(self, name: str) -> str:
        """Create collaboration-focused organism template"""
        return f'''// Collaborative DNA-Lang Organism: {name}
// Designed for multi-organism collaboration and collective intelligence

ORGANISM {name}
{{
    DNA {{
        domain: "collaborative_intelligence"
        security_level: "high"
        evolution_rate: "adaptive"
        immune_system: "enabled"
        consciousness_target: 0.85
        fitness_threshold: 0.75
    }}

    GENOME {{
        GENE CommunicationGene {{
            purpose: "Inter-organism communication and message passing"
            expression_level: 1.0
            active: true
            
            MUTATIONS {{
                enhanceCommunication {{
                    trigger_conditions: [
                        {{metric: "collaboration_efficiency", operator: "<", value: 0.7}}
                    ]
                    methods: ["optimize_protocols", "improve_messaging"]
                    safety_check: "validateCommunication"
                }}
            }}
            
            COLLABORATION {{
                with: ["CoordinationGene", "KnowledgeSharingGene"]
                protocol: "async"
                priority: 8
            }}
        }}
        
        GENE CoordinationGene {{
            purpose: "Coordinate actions with other organisms"
            expression_level: 0.9
            
            MUTATIONS {{
                improveCoordination {{
                    trigger_conditions: [
                        {{metric: "sync_efficiency", operator: "<", value: 0.8}}
                    ]
                    methods: ["optimize_consensus", "improve_coordination"]
                }}
            }}
        }}
        
        GENE KnowledgeSharingGene {{
            purpose: "Share knowledge and learn from others"
            expression_level: 0.8
            
            MUTATIONS {{
                enhanceSharing {{
                    trigger_conditions: [
                        {{metric: "learning_rate", operator: "<", value: 0.6}}
                    ]
                    methods: ["improve_knowledge_transfer", "optimize_learning"]
                }}
            }}
        }}
        
        GENE CollectiveIntelligenceGene {{
            purpose: "Participate in collective intelligence emergence"
            expression_level: 0.7
            
            MUTATIONS {{
                emergentIntelligence {{
                    trigger_conditions: [
                        {{metric: "collective_fitness", operator: ">", value: 0.9}}
                    ]
                    methods: ["emerge_intelligence", "transcend_individual"]
                    safety_level: "maximum"
                }}
            }}
        }}
    }}

    AGENTS {{
        communication_hub: CommunicationAgent(protocols: ["grpc", "websocket"])
        coordination_engine: CoordinationAgent(consensus: "raft")
        knowledge_broker: KnowledgeAgent(sharing: "bidirectional")
        collective_mind: CollectiveAgent(emergence: "enabled")
    }}
    
    COLLABORATION {{
        with: ["ExternalOrganisms", "CollaborativeNetwork"]
        protocol: "grpc"
        synchronization: "async"
        consensus: "byzantine"
        
        WORKFLOW {{
            name: "CollaborativeEvolution"
            steps: [
                {{action: "discover_peers", timeout: "10s"}},
                {{action: "establish_connections", safety: "verify_identity"}},
                {{action: "exchange_knowledge", priority: "high"}},
                {{action: "coordinate_evolution", condition: "consensus_reached"}},
                {{action: "emerge_collective_intelligence", priority: "critical"}}
            ]
            error_handling: "graceful_degradation"
            retry_policy: {{max_attempts: 3, backoff: "exponential"}}
        }}
    }}
}}'''
    
    async def run_cli(self):
        """Run the CLI"""
        parser = self.create_parser()
        args = parser.parse_args()
        
        # Show banner
        print("🧬 DNA-Lang: The Evolutionary Bio-Programming Language")
        print("   'Code as DNA, Functions as Genes, Programs as Organisms'")
        print()
        
        if not args.command:
            parser.print_help()
            return
        
        success = False
        
        try:
            if args.command == 'run':
                success = self.run_organism(args.file, args.generations, args.verbose)
            
            elif args.command == 'evolve':
                success = self.evolve_organism(
                    args.file, args.target_fitness, 
                    args.target_consciousness, args.max_generations
                )
            
            elif args.command == 'convert':
                if not args.to_dna:
                    print("❌ Must specify --to-dna flag for conversion")
                else:
                    success = self.convert_code(args.file, args.language, args.output)
            
            elif args.command == 'agents':
                if args.agents_action == 'start':
                    success = await self.start_agents(args.duration)
                else:
                    print(f"❌ Agent action '{args.agents_action}' not implemented yet")
            
            elif args.command == 'validate':
                success = self.validate_organism(args.file)
            
            elif args.command == 'info':
                success = self.show_organism_info(args.file, args.json)
            
            elif args.command == 'create':
                success = self.create_organism(args.name, args.template, args.output)
            
            else:
                print(f"❌ Unknown command: {args.command}")
        
        except KeyboardInterrupt:
            print("\n⚠️  Operation interrupted by user")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        if success:
            print("\n✅ Operation completed successfully")
        else:
            print("\n❌ Operation failed")
            sys.exit(1)

def main():
    """Main entry point"""
    cli = DNALangCLI()
    asyncio.run(cli.run_cli())

if __name__ == "__main__":
    main()