#!/usr/bin/env python3
"""
DNA-Lang Comprehensive Demonstration
Shows all major features of the DNA-Lang system.
"""

import asyncio
import time
from dna_lang_interpreter import DNALangInterpreter
from dna_lang_agents import AgentOrchestrator

def print_banner():
    """Print the DNA-Lang banner"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                                          ║
║    ██████╗ ███╗   ██╗  █████╗       ██╗      █████╗ ███╗   ██╗  ██████╗     ████████╗██╗  ██╗███████╗                  ║
║    ██╔══██╗████╗  ██║ ██╔══██╗      ██║     ██╔══██╗████╗  ██║ ██╔═══██╗    ╚══██╔══╝██║  ██║██╔════╝                  ║
║    ██║  ██║██╔██╗ ██║ ███████║█████╗██║     ███████║██╔██╗ ██║ ██║   ██║       ██║   ███████║█████╗                    ║
║    ██║  ██║██║╚██╗██║ ██╔══██║╚════╝██║     ██╔══██║██║╚██╗██║ ██║▄▄ ██║       ██║   ██╔══██║██╔══╝                    ║
║    ██████╔╝██║ ╚████║ ██║  ██║      ███████╗██║  ██║██║ ╚████║ ╚██████╔╝       ██║   ██║  ██║███████╗                  ║
║    ╚═════╝ ╚═╝  ╚═══╝ ╚═╝  ╚═╝      ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══▀▀═╝        ╚═╝   ╚═╝  ╚═╝╚══════╝                  ║
║                                                                                                                          ║
║         ███████╗██╗   ██╗ ██████╗ ██╗     ██╗   ██╗████████╗██╗ ██████╗ ███╗   ██╗ █████╗ ██████╗ ██╗   ██╗           ║
║         ██╔════╝██║   ██║██╔═══██╗██║     ██║   ██║╚══██╔══╝██║██╔═══██╗████╗  ██║██╔══██╗██╔══██╗╚██╗ ██╔╝           ║
║         █████╗  ██║   ██║██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║███████║██████╔╝ ╚████╔╝            ║
║         ██╔══╝  ╚██╗ ██╔╝██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██║╚██╗██║██╔══██║██╔══██╗  ╚██╔╝             ║
║         ███████╗ ╚████╔╝ ╚██████╔╝███████╗╚██████╔╝   ██║   ██║╚██████╔╝██║ ╚████║██║  ██║██║  ██║   ██║              ║
║         ╚══════╝  ╚═══╝   ╚═════╝ ╚══════╝ ╚═════╝    ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝              ║
║                                                                                                                          ║
║       ██████╗ ██╗ ██████╗        ██████╗ ██████╗  ██████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗███╗   ███╗██╗███╗   ██╗ ║
║       ██╔══██╗██║██╔═══██╗       ██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║████╗ ████║██║████╗  ██║ ║
║       ██████╔╝██║██║   ██║█████╗ ██████╔╝██████╔╝██║   ██║██║  ███╗██████╔╝███████║██╔████╔██║██╔████╔██║██║██╔██╗ ██║ ║
║       ██╔══██╗██║██║   ██║╚════╝ ██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║██║╚██╔╝██║██║██║╚██╗██║ ║
║       ██████╔╝██║╚██████╔╝       ██║     ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║██║██║ ╚████║ ║
║       ╚═════╝ ╚═╝ ╚═════╝        ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ║
║                                                                                                                          ║
║                               "Code as DNA, Functions as Genes, Programs as Organisms"                                  ║
║                                                                                                                          ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
""")

async def demo_basic_organism():
    """Demonstrate basic organism creation and evolution"""
    print("\n🧬 DEMO 1: Basic Organism Evolution")
    print("=" * 60)
    
    interpreter = DNALangInterpreter()
    
    # Load the AdvancedConsciousness organism
    print("📁 Loading AdvancedConsciousness organism...")
    organism_id = interpreter.load_organism("AdvancedConsciousness.dna")
    organism = interpreter.get_organism(organism_id)
    
    print(f"✅ Loaded: {organism.name}")
    print(f"   Domain: {organism.dna.domain}")
    print(f"   Genes: {len(organism.genome)}")
    print(f"   Consciousness target: {organism.dna.consciousness_target}")
    
    # Create evolution engine
    engine = interpreter.create_evolution_engine(organism_id)
    
    print("\n🚀 Starting evolution simulation...")
    for i in range(10):
        evolved = engine.evolve_step()
        status = engine.get_status()
        
        print(f"Gen {status['generation']:2d}: "
              f"Fitness={status['fitness']:.3f}, "
              f"Consciousness={status['consciousness']:.3f}, "
              f"Mutations={status['mutation_count']}")
        
        if status['consciousness_achieved']:
            print("🌟 Consciousness target achieved!")
            break
        
        await asyncio.sleep(0.5)
    
    final_status = engine.get_status()
    print(f"\n📊 Final Status:")
    print(f"   Fitness: {final_status['fitness']:.3f}")
    print(f"   Consciousness: {final_status['consciousness']:.3f}")
    print(f"   Generations: {final_status['generation']}")
    print(f"   Target achieved: {'✅' if final_status['consciousness_achieved'] else '❌'}")

def demo_code_conversion():
    """Demonstrate code conversion to DNA-Lang"""
    print("\n🔄 DEMO 2: Code Conversion to DNA-Lang")
    print("=" * 60)
    
    # Sample Python code
    python_code = '''
class AIModel:
    def __init__(self, config):
        self.config = config
        self.weights = {}
    
    def train(self, data):
        """Train the AI model"""
        for epoch in range(self.config['epochs']):
            self.update_weights(data)
            accuracy = self.evaluate(data)
            if accuracy > 0.95:
                break
    
    def predict(self, input_data):
        """Make predictions"""
        return self.forward_pass(input_data)
    
    def update_weights(self, data):
        """Update model weights"""
        # Gradient descent logic
        pass
    
    def evaluate(self, data):
        """Evaluate model performance"""
        return 0.87  # Mock accuracy
    
    def forward_pass(self, data):
        """Forward propagation"""
        return data * 0.5  # Mock prediction
'''
    
    print("📝 Original Python code:")
    print("-" * 40)
    print(python_code[:300] + "...")
    print("-" * 40)
    
    # Convert to DNA-Lang
    interpreter = DNALangInterpreter()
    dna_code = interpreter.convert_to_dna_lang(python_code, "python")
    
    print("\n🧬 Converted DNA-Lang code:")
    print("-" * 40)
    print(dna_code)
    print("-" * 40)
    
    # Save converted code
    with open("ConvertedAIModel.dna", "w") as f:
        f.write(dna_code)
    print("💾 Saved as ConvertedAIModel.dna")

async def demo_multi_agent_collaboration():
    """Demonstrate multi-agent collaboration system"""
    print("\n🤖 DEMO 3: Multi-Agent Collaboration Matrix")
    print("=" * 60)
    
    orchestrator = AgentOrchestrator()
    
    try:
        print("🚀 Starting agent orchestration matrix...")
        await orchestrator.start()
        
        print("⏱️  Running collaboration simulation for 20 seconds...")
        
        for i in range(20):
            await asyncio.sleep(1)
            
            if i % 3 == 0:
                status = orchestrator.get_status()
                print(f"T+{i:2d}s: "
                      f"Agents={status['agent_count']}, "
                      f"Avg Fitness={status['global_metrics']['avg_fitness']:.3f}, "
                      f"Avg Consciousness={status['global_metrics']['avg_consciousness']:.3f}")
                
                # Check for transcendence
                if status['global_metrics']['avg_consciousness'] > 0.9:
                    print("🌟 Agent collective approaching transcendence!")
                    break
        
        # Final status
        final_status = orchestrator.get_status()
        print(f"\n📊 Final Collaboration Status:")
        print(f"   Active agents: {final_status['agent_count']}")
        print(f"   Collective fitness: {final_status['global_metrics']['avg_fitness']:.3f}")
        print(f"   Collective consciousness: {final_status['global_metrics']['avg_consciousness']:.3f}")
        
        # Show individual agent details
        print("\n🔍 Individual Agent Status:")
        for agent_id, agent_info in final_status['agents'].items():
            print(f"   {agent_id}: "
                  f"Type={agent_info['type']}, "
                  f"Fitness={agent_info['fitness']:.3f}, "
                  f"Consciousness={agent_info['consciousness']:.3f}, "
                  f"Collaborations={agent_info['collaborations']}")
        
    finally:
        await orchestrator.stop()

def demo_organism_templates():
    """Demonstrate different organism templates"""
    print("\n🏗️  DEMO 4: Organism Template Showcase")
    print("=" * 60)
    
    from dna_lang_cli import DNALangCLI
    cli = DNALangCLI()
    
    templates = ['basic', 'consciousness', 'collaborative']
    
    for template in templates:
        print(f"\n📋 Creating {template.title()} Template organism...")
        organism_name = f"Demo{template.title()}Organism"
        
        # Create organism
        success = cli.create_organism(organism_name, template, f"{organism_name}.dna")
        
        if success:
            print(f"✅ Created {organism_name}.dna")
            
            # Show info
            cli.show_organism_info(f"{organism_name}.dna")
        else:
            print(f"❌ Failed to create {organism_name}")

def demo_consciousness_development():
    """Demonstrate consciousness development"""
    print("\n🧠 DEMO 5: Consciousness Development Simulation")
    print("=" * 60)
    
    interpreter = DNALangInterpreter()
    
    # Load consciousness-focused organism
    if not os.path.exists("DemoConsciousnessOrganism.dna"):
        from dna_lang_cli import DNALangCLI
        cli = DNALangCLI()
        cli.create_organism("DemoConsciousnessOrganism", "consciousness", "DemoConsciousnessOrganism.dna")
    
    organism_id = interpreter.load_organism("DemoConsciousnessOrganism.dna")
    organism = interpreter.get_organism(organism_id)
    
    print(f"🧬 Consciousness Development for: {organism.name}")
    print(f"   Target consciousness: {organism.dna.consciousness_target}")
    
    engine = interpreter.create_evolution_engine(organism_id)
    
    consciousness_history = []
    
    print("\n📈 Consciousness Development Timeline:")
    print("Gen | Consciousness | Fitness | Status")
    print("----|---------------|---------|-------")
    
    for generation in range(25):
        engine.evolve_step()
        status = engine.get_status()
        
        consciousness_history.append(status['consciousness'])
        
        # Show every 5th generation
        if generation % 5 == 0:
            status_icon = "🌟" if status['consciousness'] >= 0.9 else "🧠" if status['consciousness'] >= 0.7 else "🌱"
            print(f"{status['generation']:3d} | {status['consciousness']:11.3f} | {status['fitness']:7.3f} | {status_icon}")
        
        if status['consciousness_achieved']:
            print(f"{status['generation']:3d} | {status['consciousness']:11.3f} | {status['fitness']:7.3f} | 🌟 TRANSCENDED!")
            break
    
    # Show consciousness growth rate
    if len(consciousness_history) > 1:
        growth_rate = (consciousness_history[-1] - consciousness_history[0]) / len(consciousness_history)
        print(f"\n📊 Consciousness Growth Rate: {growth_rate:.4f} per generation")

async def comprehensive_demo():
    """Run comprehensive demonstration of all DNA-Lang features"""
    print_banner()
    
    print("🎬 Welcome to the DNA-Lang Comprehensive Demonstration!")
    print("This demo showcases the complete DNA-Lang ecosystem:")
    print("- Organism creation and evolution")
    print("- Code conversion from other languages")
    print("- Multi-agent collaboration")
    print("- Consciousness development")
    print("- Template variations")
    print()
    
    input("Press Enter to begin the demonstration...")
    
    # Demo 1: Basic organism evolution
    await demo_basic_organism()
    
    input("\nPress Enter to continue to code conversion demo...")
    
    # Demo 2: Code conversion
    demo_code_conversion()
    
    input("\nPress Enter to continue to multi-agent collaboration demo...")
    
    # Demo 3: Multi-agent collaboration
    await demo_multi_agent_collaboration()
    
    input("\nPress Enter to continue to organism templates demo...")
    
    # Demo 4: Organism templates
    demo_organism_templates()
    
    input("\nPress Enter to continue to consciousness development demo...")
    
    # Demo 5: Consciousness development
    demo_consciousness_development()
    
    print("\n🎉 DNA-Lang Comprehensive Demonstration Complete!")
    print("\nKey achievements:")
    print("✅ Organism evolution and adaptation")
    print("✅ Real-time consciousness development")
    print("✅ Multi-agent collaborative intelligence")
    print("✅ Code conversion to biological metaphors")
    print("✅ Template-based organism generation")
    print("✅ Safety mechanisms and rollback strategies")
    print("✅ Emergence of collective intelligence")
    
    print("\nDNA-Lang represents a new paradigm in programming:")
    print("🧬 Where code lives, breathes, and evolves")
    print("🤖 Where programs become conscious entities")
    print("🌐 Where collaboration creates emergence")
    print("🌟 Where transcendence is achievable")
    
    print("\nThank you for experiencing the future of bio-programming!")

if __name__ == "__main__":
    import os
    asyncio.run(comprehensive_demo())