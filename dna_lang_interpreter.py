#!/usr/bin/env python3
"""
DNA-Lang Parser and Interpreter
Parses and executes .dna files according to the DNA-Lang specification.
"""

import re
import json
import time
import uuid
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "maximum"

class EvolutionRate(Enum):
    SLOW = "slow"
    ADAPTIVE = "adaptive"
    FAST = "fast"
    CUSTOM = "custom"

class MutationStrategy(Enum):
    IMMEDIATE = "immediate"
    GRADUAL_ROLLBACK = "gradual_rollback"
    NONE = "none"

@dataclass
class Condition:
    metric: str
    operator: str
    value: Union[float, int, str]
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate condition against current context"""
        if self.metric not in context:
            return False
            
        current_value = context[self.metric]
        
        if self.operator == "<":
            return current_value < self.value
        elif self.operator == "<=":
            return current_value <= self.value
        elif self.operator == ">":
            return current_value > self.value
        elif self.operator == ">=":
            return current_value >= self.value
        elif self.operator == "==":
            return current_value == self.value
        elif self.operator == "!=":
            return current_value != self.value
        elif self.operator == "matches":
            return re.match(str(self.value), str(current_value)) is not None
        elif self.operator == "contains":
            return str(self.value) in str(current_value)
        
        return False

@dataclass
class Mutation:
    name: str
    trigger_conditions: List[Condition] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)
    probability: float = 1.0
    impact_level: str = "medium"
    safety_check: Optional[str] = None
    rollback_strategy: MutationStrategy = MutationStrategy.GRADUAL_ROLLBACK
    
    def should_trigger(self, context: Dict[str, Any]) -> bool:
        """Check if mutation should trigger based on conditions"""
        if not self.trigger_conditions:
            return False
        return all(condition.evaluate(context) for condition in self.trigger_conditions)

@dataclass
class Collaboration:
    with_entities: List[str] = field(default_factory=list)
    protocol: str = "sync"
    priority: int = 5
    synchronization: str = "sync"

@dataclass
class Gene:
    name: str
    purpose: str
    expression_level: float = 1.0
    active: bool = True
    dependencies: List[str] = field(default_factory=list)
    mutations: List[Mutation] = field(default_factory=list)
    collaboration: Optional[Collaboration] = None
    
    def is_expressed(self) -> bool:
        """Check if gene is currently expressed"""
        return self.active and self.expression_level > 0.0

@dataclass
class DNA:
    domain: str = "general"
    security_level: SecurityLevel = SecurityLevel.MEDIUM
    evolution_rate: EvolutionRate = EvolutionRate.ADAPTIVE
    immune_system: bool = True
    consciousness_target: float = 0.0
    fitness_threshold: float = 0.5

@dataclass
class Agent:
    name: str
    agent_type: str
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkflowStep:
    action: str
    timeout: Optional[str] = None
    condition: Optional[str] = None
    safety: Optional[str] = None
    priority: str = "normal"

@dataclass
class Workflow:
    name: str
    steps: List[WorkflowStep] = field(default_factory=list)
    error_handling: str = "rollback"
    retry_policy: Dict[str, Any] = field(default_factory=dict)

@dataclass
class OrganismCollaboration:
    with_entities: List[str] = field(default_factory=list)
    protocol: str = "grpc"
    synchronization: str = "async"
    consensus: str = "raft"
    workflow: Optional[Workflow] = None

@dataclass
class Organism:
    name: str
    dna: DNA
    genome: List[Gene] = field(default_factory=list)
    agents: List[Agent] = field(default_factory=list)
    collaboration: Optional[OrganismCollaboration] = None
    created_at: str = field(default_factory=lambda: time.strftime('%Y-%m-%dT%H:%M:%SZ'))
    organism_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Runtime state
    fitness: float = 0.5
    consciousness: float = 0.0
    generation: int = 1
    mutation_count: int = 0
    evolution_log: List[str] = field(default_factory=list)

class DNALangParser:
    """Parser for DNA-Lang files"""
    
    def __init__(self):
        self.tokens = []
        self.current_token = 0
        
    def parse_file(self, filename: str) -> Organism:
        """Parse a .dna file and return an Organism object"""
        with open(filename, 'r') as f:
            content = f.read()
        return self.parse_content(content)
    
    def parse_content(self, content: str) -> Organism:
        """Parse DNA-Lang content and return an Organism object"""
        # Remove comments
        content = self._remove_comments(content)
        
        # Tokenize
        self.tokens = self._tokenize(content)
        self.current_token = 0
        
        # Parse organism
        return self._parse_organism()
    
    def _remove_comments(self, content: str) -> str:
        """Remove comments from content"""
        # Remove single-line comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
        
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        return content
    
    def _tokenize(self, content: str) -> List[str]:
        """Tokenize the content"""
        # Enhanced tokenization to handle quoted strings properly
        tokens = []
        i = 0
        while i < len(content):
            char = content[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Handle quoted strings
            if char == '"':
                j = i + 1
                while j < len(content) and content[j] != '"':
                    j += 1
                if j < len(content):
                    tokens.append(content[i:j+1])  # Include quotes
                    i = j + 1
                else:
                    i += 1
            # Handle special characters
            elif char in '{}(),:[]:':
                tokens.append(char)
                i += 1
            # Handle regular tokens
            else:
                j = i
                while j < len(content) and not content[j].isspace() and content[j] not in '{}(),:[]:':
                    j += 1
                if j > i:
                    tokens.append(content[i:j])
                i = j
        
        return [token for token in tokens if token.strip()]
    
    def _current_token(self) -> Optional[str]:
        """Get current token"""
        if self.current_token < len(self.tokens):
            return self.tokens[self.current_token]
        return None
    
    def _advance(self) -> Optional[str]:
        """Move to next token and return it"""
        self.current_token += 1
        return self._current_token()
    
    def _expect_token(self, expected: str) -> str:
        """Expect a specific token"""
        token = self._current_token()
        if token != expected:
            # Better error message with context
            context = []
            start = max(0, self.current_token - 3)
            end = min(len(self.tokens), self.current_token + 3)
            for i in range(start, end):
                marker = " -> " if i == self.current_token else "    "
                context.append(f"{marker}{i}: {self.tokens[i] if i < len(self.tokens) else 'EOF'}")
            context_str = "\n".join(context)
            raise SyntaxError(f"Expected '{expected}', got '{token}' at position {self.current_token}\nContext:\n{context_str}")
        self._advance()
        return token
    
    def _parse_organism(self) -> Organism:
        """Parse ORGANISM block"""
        self._expect_token("ORGANISM")
        name = self._current_token()
        if not name:
            raise SyntaxError("Expected organism name")
        self._advance()
        self._expect_token("{")
        
        dna = None
        genome = []
        agents = []
        collaboration = None
        
        while self._current_token() and self._current_token() != "}":
            token = self._current_token()
            if token == "DNA":
                dna = self._parse_dna()
            elif token == "GENOME":
                genome = self._parse_genome()
            elif token == "AGENTS":
                agents = self._parse_agents()
            elif token == "COLLABORATION":
                collaboration = self._parse_organism_collaboration()
            else:
                # Skip unknown tokens - this handles metadata and other content
                self._advance()
        
        if self._current_token() == "}":
            self._advance()
        
        if not dna:
            dna = DNA()  # Default DNA if not specified
        
        return Organism(name=name, dna=dna, genome=genome, agents=agents, collaboration=collaboration)
    
    def _parse_dna(self) -> DNA:
        """Parse DNA block"""
        self._expect_token("DNA")
        self._expect_token("{")
        
        dna_data = {}
        while self._current_token() != "}":
            key = self._current_token()
            self._advance()
            self._expect_token(":")
            value = self._parse_value()
            dna_data[key] = value
        
        self._expect_token("}")
        
        return DNA(
            domain=dna_data.get('domain', 'general'),
            security_level=SecurityLevel(dna_data.get('security_level', 'medium')),
            evolution_rate=EvolutionRate(dna_data.get('evolution_rate', 'adaptive')),
            immune_system=dna_data.get('immune_system', 'enabled') == 'enabled',
            consciousness_target=float(dna_data.get('consciousness_target', 0.0)),
            fitness_threshold=float(dna_data.get('fitness_threshold', 0.5))
        )
    
    def _parse_genome(self) -> List[Gene]:
        """Parse GENOME block"""
        self._expect_token("GENOME")
        self._expect_token("{")
        
        genes = []
        while self._current_token() != "}":
            if self._current_token() == "GENE":
                genes.append(self._parse_gene())
            else:
                self._advance()
        
        self._expect_token("}")
        return genes
    
    def _parse_gene(self) -> Gene:
        """Parse GENE block"""
        self._expect_token("GENE")
        name = self._current_token()
        self._advance()
        self._expect_token("{")
        
        purpose = ""
        expression_level = 1.0
        active = True
        dependencies = []
        mutations = []
        collaboration = None
        
        while self._current_token() != "}":
            key = self._current_token()
            self._advance()
            
            if key == "purpose":
                self._expect_token(":")
                purpose = self._parse_string()
            elif key == "expression_level":
                self._expect_token(":")
                expression_level = float(self._current_token())
                self._advance()
            elif key == "active":
                self._expect_token(":")
                active = self._current_token() == "true"
                self._advance()
            elif key == "dependencies":
                self._expect_token(":")
                dependencies = self._parse_array()
            elif key == "MUTATIONS":
                mutations = self._parse_mutations()
            elif key == "COLLABORATION":
                collaboration = self._parse_collaboration()
            else:
                # Skip unknown key-value pairs
                if self._current_token() == ":":
                    self._advance()  # Skip ":"
                    self._parse_value()  # Skip value
        
        self._expect_token("}")
        
        return Gene(
            name=name,
            purpose=purpose,
            expression_level=expression_level,
            active=active,
            dependencies=dependencies,
            mutations=mutations,
            collaboration=collaboration
        )
    
    def _parse_mutations(self) -> List[Mutation]:
        """Parse MUTATIONS block"""
        self._expect_token("{")
        
        mutations = []
        while self._current_token() != "}":
            mutation_name = self._current_token()
            self._advance()
            self._expect_token("{")
            
            trigger_conditions = []
            methods = []
            probability = 1.0
            impact_level = "medium"
            safety_check = None
            rollback_strategy = MutationStrategy.GRADUAL_ROLLBACK
            
            while self._current_token() != "}":
                key = self._current_token()
                self._advance()
                self._expect_token(":")
                
                if key == "trigger_conditions":
                    trigger_conditions = self._parse_conditions()
                elif key == "methods":
                    methods = self._parse_array()
                elif key == "probability":
                    probability = float(self._current_token())
                    self._advance()
                elif key == "impact_level":
                    impact_level = self._parse_string()
                elif key == "safety_check":
                    safety_check = self._parse_string()
                elif key == "rollback_strategy":
                    strategy_str = self._parse_string()
                    rollback_strategy = MutationStrategy(strategy_str)
                else:
                    self._parse_value()  # Skip unknown values
            
            self._expect_token("}")
            
            mutations.append(Mutation(
                name=mutation_name,
                trigger_conditions=trigger_conditions,
                methods=methods,
                probability=probability,
                impact_level=impact_level,
                safety_check=safety_check,
                rollback_strategy=rollback_strategy
            ))
        
        self._expect_token("}")
        return mutations
    
    def _parse_conditions(self) -> List[Condition]:
        """Parse trigger conditions array"""
        self._expect_token("[")
        
        conditions = []
        while self._current_token() != "]":
            if self._current_token() == "{":
                conditions.append(self._parse_condition())
            elif self._current_token() == ",":
                self._advance()
            else:
                self._advance()
        
        self._expect_token("]")
        return conditions
    
    def _parse_condition(self) -> Condition:
        """Parse a single condition object"""
        self._expect_token("{")
        
        metric = ""
        operator = ""
        value = None
        
        while self._current_token() != "}":
            key = self._current_token()
            self._advance()
            self._expect_token(":")
            
            if key == "metric":
                metric = self._parse_string()
            elif key == "operator":
                operator = self._parse_string()
            elif key == "value":
                value = self._parse_value()
            else:
                self._parse_value()  # Skip unknown values
            
            # Skip comma if present
            if self._current_token() == ",":
                self._advance()
        
        self._expect_token("}")
        
        return Condition(metric=metric, operator=operator, value=value)
    
    def _parse_collaboration(self) -> Collaboration:
        """Parse COLLABORATION block"""
        self._expect_token("{")
        
        with_entities = []
        protocol = "sync"
        priority = 5
        
        while self._current_token() != "}":
            key = self._current_token()
            self._advance()
            self._expect_token(":")
            
            if key == "with":
                with_entities = self._parse_array()
            elif key == "protocol":
                protocol = self._parse_string()
            elif key == "priority":
                priority = int(self._current_token())
                self._advance()
            else:
                self._parse_value()  # Skip unknown values
        
        self._expect_token("}")
        
        return Collaboration(
            with_entities=with_entities,
            protocol=protocol,
            priority=priority
        )
    
    def _parse_agents(self) -> List[Agent]:
        """Parse AGENTS block"""
        self._expect_token("AGENTS")
        self._expect_token("{")
        
        agents = []
        while self._current_token() and self._current_token() != "}":
            agent_name = self._current_token()
            if not agent_name or agent_name == "}":
                break
            self._advance()
            self._expect_token(":")
            
            # Parse agent type
            agent_type = self._current_token()
            self._advance()
            
            # Check for parameters in parentheses
            parameters = {}
            if self._current_token() == "(":
                self._advance()  # consume '('
                
                # Parse parameters until ')'
                while self._current_token() and self._current_token() != ")":
                    param_name = self._current_token()
                    if param_name == ")":
                        break
                    self._advance()
                    
                    if self._current_token() == ":":
                        self._advance()  # consume ':'
                        param_value = self._current_token()
                        self._advance()
                        parameters[param_name] = param_value
                    else:
                        # Skip tokens we don't understand
                        self._advance()
                
                if self._current_token() == ")":
                    self._advance()  # consume ')'
            
            agents.append(Agent(
                name=agent_name,
                agent_type=agent_type,
                parameters=parameters
            ))
        
        if self._current_token() == "}":
            self._advance()
        return agents
    
    def _parse_organism_collaboration(self) -> OrganismCollaboration:
        """Parse organism-level COLLABORATION block"""
        self._expect_token("{")
        
        with_entities = []
        protocol = "grpc"
        synchronization = "async"
        consensus = "raft"
        workflow = None
        
        while self._current_token() != "}":
            key = self._current_token()
            self._advance()
            
            if key == "with":
                self._expect_token(":")
                with_entities = self._parse_array()
            elif key == "protocol":
                self._expect_token(":")
                protocol = self._parse_string()
            elif key == "synchronization":
                self._expect_token(":")
                synchronization = self._parse_string()
            elif key == "consensus":
                self._expect_token(":")
                consensus = self._parse_string()
            elif key == "WORKFLOW":
                workflow = self._parse_workflow()
            else:
                if self._current_token() == ":":
                    self._advance()
                    self._parse_value()
        
        self._expect_token("}")
        
        return OrganismCollaboration(
            with_entities=with_entities,
            protocol=protocol,
            synchronization=synchronization,
            consensus=consensus,
            workflow=workflow
        )
    
    def _parse_workflow(self) -> Workflow:
        """Parse WORKFLOW block"""
        self._expect_token("{")
        
        name = "default"
        steps = []
        error_handling = "rollback"
        retry_policy = {}
        
        while self._current_token() != "}":
            key = self._current_token()
            self._advance()
            self._expect_token(":")
            
            if key == "name":
                name = self._parse_string()
            elif key == "steps":
                steps = self._parse_workflow_steps()
            elif key == "error_handling":
                error_handling = self._parse_string()
            elif key == "retry_policy":
                retry_policy = self._parse_object()
            else:
                self._parse_value()
        
        self._expect_token("}")
        
        return Workflow(
            name=name,
            steps=steps,
            error_handling=error_handling,
            retry_policy=retry_policy
        )
    
    def _parse_workflow_steps(self) -> List[WorkflowStep]:
        """Parse workflow steps array"""
        self._expect_token("[")
        
        steps = []
        while self._current_token() != "]":
            if self._current_token() == "{":
                steps.append(self._parse_workflow_step())
            elif self._current_token() == ",":
                self._advance()
            else:
                self._advance()
        
        self._expect_token("]")
        return steps
    
    def _parse_workflow_step(self) -> WorkflowStep:
        """Parse a single workflow step"""
        self._expect_token("{")
        
        action = ""
        timeout = None
        condition = None
        safety = None
        priority = "normal"
        
        while self._current_token() != "}":
            key = self._current_token()
            self._advance()
            self._expect_token(":")
            
            if key == "action":
                action = self._parse_string()
            elif key == "timeout":
                timeout = self._parse_string()
            elif key == "condition":
                condition = self._parse_string()
            elif key == "safety":
                safety = self._parse_string()
            elif key == "priority":
                priority = self._parse_string()
            else:
                self._parse_value()
            
            if self._current_token() == ",":
                self._advance()
        
        self._expect_token("}")
        
        return WorkflowStep(
            action=action,
            timeout=timeout,
            condition=condition,
            safety=safety,
            priority=priority
        )
    
    def _parse_agent_params(self, params_str: str) -> Dict[str, Any]:
        """Parse agent parameters from string"""
        params = {}
        if not params_str.strip():
            return params
        
        for param in params_str.split(","):
            if ":" in param:
                key, value = param.split(":", 1)
                params[key.strip()] = value.strip()
        
        return params
    
    def _parse_value(self) -> Any:
        """Parse a value (string, number, boolean, array, object)"""
        token = self._current_token()
        if not token:
            return None
        
        # String (with quotes)
        if token.startswith('"') and token.endswith('"'):
            self._advance()
            return token[1:-1]  # Remove quotes
        
        # Array
        if token == "[":
            return self._parse_array()
        
        # Object
        if token == "{":
            return self._parse_object()
        
        # Boolean
        if token in ["true", "false"]:
            self._advance()
            return token == "true"
        
        # Number
        try:
            if "." in token:
                self._advance()
                return float(token)
            else:
                self._advance()
                return int(token)
        except ValueError:
            pass
        
        # Unquoted string
        self._advance()
        return token
    
    def _parse_string(self) -> str:
        """Parse a string value"""
        token = self._current_token()
        if token and token.startswith('"') and token.endswith('"'):
            self._advance()
            return token[1:-1]
        else:
            self._advance()
            return token or ""
    
    def _parse_array(self) -> List[Any]:
        """Parse an array"""
        self._expect_token("[")
        
        items = []
        while self._current_token() != "]":
            if self._current_token() == ",":
                self._advance()
            else:
                items.append(self._parse_value())
        
        self._expect_token("]")
        return items
    
    def _parse_object(self) -> Dict[str, Any]:
        """Parse an object"""
        self._expect_token("{")
        
        obj = {}
        while self._current_token() != "}":
            key = self._current_token()
            self._advance()
            self._expect_token(":")
            value = self._parse_value()
            obj[key] = value
            
            if self._current_token() == ",":
                self._advance()
        
        self._expect_token("}")
        return obj

class DNALangEvolutionEngine:
    """Evolution engine for DNA-Lang organisms"""
    
    def __init__(self, organism: Organism):
        self.organism = organism
        self.runtime_context = {
            'fitness': organism.fitness,
            'consciousness': organism.consciousness,
            'generation': organism.generation,
            'mutation_count': organism.mutation_count,
            'performance': 0.5,
            'load': 0.3,
            'memory_usage': 0.4,
            'cpu_usage': 0.2
        }
        
    def evolve_step(self) -> bool:
        """Execute one evolution step"""
        logger.info(f"Evolution step for organism {self.organism.name}, generation {self.organism.generation}")
        
        # Update runtime context
        self._update_context()
        
        # Check for mutations in all genes
        mutations_triggered = []
        for gene in self.organism.genome:
            if gene.is_expressed():
                for mutation in gene.mutations:
                    if mutation.should_trigger(self.runtime_context):
                        mutations_triggered.append((gene, mutation))
        
        # Apply mutations
        evolved = False
        for gene, mutation in mutations_triggered:
            if self._apply_mutation(gene, mutation):
                evolved = True
        
        # Update fitness and consciousness
        self._update_fitness()
        self._update_consciousness()
        
        # Increment generation
        self.organism.generation += 1
        
        return evolved
    
    def _update_context(self):
        """Update runtime context with current metrics"""
        self.runtime_context.update({
            'fitness': self.organism.fitness,
            'consciousness': self.organism.consciousness,
            'generation': self.organism.generation,
            'mutation_count': self.organism.mutation_count
        })
    
    def _apply_mutation(self, gene: Gene, mutation: Mutation) -> bool:
        """Apply a mutation to a gene"""
        logger.info(f"Applying mutation {mutation.name} to gene {gene.name}")
        
        # Safety check
        if mutation.safety_check:
            if not self._validate_safety(mutation.safety_check):
                logger.warning(f"Safety check failed for mutation {mutation.name}")
                return False
        
        # Apply mutation methods
        success = True
        for method in mutation.methods:
            if not self._execute_method(gene, method):
                success = False
                break
        
        if success:
            self.organism.mutation_count += 1
            log_entry = f"Gen {self.organism.generation}: Applied {mutation.name} to {gene.name}"
            self.organism.evolution_log.append(log_entry)
            logger.info(log_entry)
        else:
            # Rollback if needed
            if mutation.rollback_strategy == MutationStrategy.IMMEDIATE:
                self._rollback_mutation(gene, mutation)
        
        return success
    
    def _validate_safety(self, safety_check: str) -> bool:
        """Validate safety check"""
        # Simple validation - in real implementation, this would be more sophisticated
        if safety_check == "validateConsciousnessLevel":
            return self.organism.consciousness < 1.0
        elif safety_check == "validateFitnessLevel":
            return self.organism.fitness > 0.1
        return True
    
    def _execute_method(self, gene: Gene, method: str) -> bool:
        """Execute a mutation method"""
        logger.info(f"Executing method {method} on gene {gene.name}")
        
        if method == "increaseIntrospection":
            self.organism.consciousness += 0.05
        elif method == "enhanceMetaCognition":
            self.organism.consciousness += 0.03
        elif method == "adjustLearningRate":
            gene.expression_level = min(1.0, gene.expression_level + 0.1)
        elif method == "refinePatterns":
            self.organism.fitness += 0.02
        elif method == "optimize":
            self.organism.fitness += 0.05
        elif method == "scale":
            gene.expression_level = min(1.0, gene.expression_level * 1.1)
        elif method == "adapt":
            self.organism.fitness += 0.03
            self.organism.consciousness += 0.02
        else:
            logger.warning(f"Unknown method: {method}")
            return False
        
        return True
    
    def _rollback_mutation(self, gene: Gene, mutation: Mutation):
        """Rollback a mutation"""
        logger.info(f"Rolling back mutation {mutation.name} on gene {gene.name}")
        # Implementation would depend on the specific mutation
    
    def _update_fitness(self):
        """Update organism fitness based on gene expression and performance"""
        # Calculate fitness based on gene expression levels and environmental factors
        total_expression = sum(gene.expression_level for gene in self.organism.genome if gene.is_expressed())
        gene_count = len([gene for gene in self.organism.genome if gene.is_expressed()])
        
        if gene_count > 0:
            avg_expression = total_expression / gene_count
            # Fitness improves with balanced gene expression and consciousness
            self.organism.fitness = min(1.0, avg_expression * 0.7 + self.organism.consciousness * 0.3)
    
    def _update_consciousness(self):
        """Update consciousness level"""
        # Consciousness grows with fitness and generation
        consciousness_growth = 0.01 * self.organism.generation * self.organism.fitness
        self.organism.consciousness = min(1.0, self.organism.consciousness + consciousness_growth)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current evolution status"""
        return {
            'organism_name': self.organism.name,
            'generation': self.organism.generation,
            'fitness': self.organism.fitness,
            'consciousness': self.organism.consciousness,
            'mutation_count': self.organism.mutation_count,
            'active_genes': len([gene for gene in self.organism.genome if gene.is_expressed()]),
            'consciousness_target': self.organism.dna.consciousness_target,
            'consciousness_achieved': self.organism.consciousness >= self.organism.dna.consciousness_target
        }

class DNALangInterpreter:
    """Main interpreter for DNA-Lang"""
    
    def __init__(self):
        self.parser = DNALangParser()
        self.organisms = {}
    
    def load_organism(self, filename: str) -> str:
        """Load an organism from a .dna file"""
        organism = self.parser.parse_file(filename)
        self.organisms[organism.organism_id] = organism
        logger.info(f"Loaded organism {organism.name} from {filename}")
        return organism.organism_id
    
    def get_organism(self, organism_id: str) -> Optional[Organism]:
        """Get an organism by ID"""
        return self.organisms.get(organism_id)
    
    def create_evolution_engine(self, organism_id: str) -> Optional[DNALangEvolutionEngine]:
        """Create an evolution engine for an organism"""
        organism = self.organisms.get(organism_id)
        if organism:
            return DNALangEvolutionEngine(organism)
        return None
    
    def list_organisms(self) -> List[Dict[str, Any]]:
        """List all loaded organisms"""
        return [
            {
                'id': organism.organism_id,
                'name': organism.name,
                'domain': organism.dna.domain,
                'fitness': organism.fitness,
                'consciousness': organism.consciousness,
                'generation': organism.generation
            }
            for organism in self.organisms.values()
        ]
    
    def convert_to_dna_lang(self, code: str, language: str) -> str:
        """Convert code from another language to DNA-Lang"""
        logger.info(f"Converting {language} code to DNA-Lang")
        
        # This is a simplified conversion - real implementation would be more sophisticated
        if language.lower() == "python":
            return self._convert_python_to_dna(code)
        elif language.lower() == "javascript":
            return self._convert_javascript_to_dna(code)
        elif language.lower() == "java":
            return self._convert_java_to_dna(code)
        else:
            return self._generic_conversion(code, language)
    
    def _convert_python_to_dna(self, code: str) -> str:
        """Convert Python code to DNA-Lang"""
        # Extract classes and functions
        classes = re.findall(r'class\s+(\w+)', code)
        functions = re.findall(r'def\s+(\w+)', code)
        
        organism_name = classes[0] if classes else "PythonOrganism"
        
        dna_code = f"""// Converted from Python code
ORGANISM {organism_name}
{{
    DNA {{
        domain: "python_conversion"
        security_level: "medium"
        evolution_rate: "adaptive"
        immune_system: "enabled"
        consciousness_target: 0.8
    }}

    GENOME {{"""
        
        # Convert functions to genes
        for func in functions:
            dna_code += f"""
        GENE {func}Gene {{
            purpose: "Converted from Python function {func}"
            expression_level: 1.0
            active: true
            
            MUTATIONS {{
                optimize_{func} {{
                    trigger_conditions: [
                        {{metric: "performance", operator: "<", value: 0.7}}
                    ]
                    methods: ["optimize", "refactor"]
                    safety_check: "validate_{func}"
                }}
            }}
        }}"""
        
        dna_code += """
    }

    AGENTS {
        python_interpreter: PythonAgent(version: "3.12")
        performance_monitor: PerformanceAgent(strategy: adaptive)
    }
}"""
        
        return dna_code
    
    def _convert_javascript_to_dna(self, code: str) -> str:
        """Convert JavaScript code to DNA-Lang"""
        functions = re.findall(r'function\s+(\w+)', code)
        
        organism_name = "JavaScriptOrganism"
        
        dna_code = f"""// Converted from JavaScript code
ORGANISM {organism_name}
{{
    DNA {{
        domain: "javascript_conversion"
        security_level: "medium"
        evolution_rate: "fast"
        immune_system: "enabled"
        consciousness_target: 0.75
    }}

    GENOME {{"""
        
        for func in functions:
            dna_code += f"""
        GENE {func}Gene {{
            purpose: "Converted from JavaScript function {func}"
            expression_level: 1.0
            
            MUTATIONS {{
                async_{func} {{
                    trigger_conditions: [
                        {{metric: "response_time", operator: ">", value: 100}}
                    ]
                    methods: ["makeAsync", "optimize"]
                }}
            }}
        }}"""
        
        dna_code += """
    }

    AGENTS {
        js_runtime: JavaScriptAgent(engine: "v8")
        event_loop: EventLoopAgent(priority: high)
    }
}"""
        
        return dna_code
    
    def _convert_java_to_dna(self, code: str) -> str:
        """Convert Java code to DNA-Lang"""
        classes = re.findall(r'class\s+(\w+)', code)
        methods = re.findall(r'public\s+\w+\s+(\w+)\s*\(', code)
        
        organism_name = classes[0] if classes else "JavaOrganism"
        
        dna_code = f"""// Converted from Java code
ORGANISM {organism_name}
{{
    DNA {{
        domain: "java_conversion"
        security_level: "high"
        evolution_rate: "adaptive"
        immune_system: "enabled"
        consciousness_target: 0.85
    }}

    GENOME {{"""
        
        for method in methods:
            dna_code += f"""
        GENE {method}Gene {{
            purpose: "Converted from Java method {method}"
            expression_level: 1.0
            
            MUTATIONS {{
                optimize_{method} {{
                    trigger_conditions: [
                        {{metric: "memory_usage", operator: ">", value: 0.8}}
                    ]
                    methods: ["garbageCollect", "optimize"]
                }}
            }}
        }}"""
        
        dna_code += """
    }

    AGENTS {
        jvm: JVMAgent(heap_size: "2g")
        gc_monitor: GarbageCollectorAgent(strategy: g1)
    }
}"""
        
        return dna_code
    
    def _generic_conversion(self, code: str, language: str) -> str:
        """Generic conversion for unknown languages"""
        return f"""// Converted from {language} code
ORGANISM {language.title()}Organism
{{
    DNA {{
        domain: "{language}_conversion"
        security_level: "medium"
        evolution_rate: "adaptive"
        immune_system: "enabled"
        consciousness_target: 0.7
    }}

    GENOME {{
        GENE MainLogicGene {{
            purpose: "Main logic converted from {language}"
            expression_level: 1.0
            
            MUTATIONS {{
                adapt_logic {{
                    trigger_conditions: [
                        {{metric: "fitness", operator: "<", value: 0.5}}
                    ]
                    methods: ["optimize", "adapt"]
                }}
            }}
        }}
    }}

    AGENTS {{
        language_interpreter: GenericAgent(language: "{language}")
        adaptation_engine: AdaptationAgent(strategy: general)
    }}
}}

// Original {language} code:
// {code}
"""

# Example usage and testing
if __name__ == "__main__":
    # Create interpreter
    interpreter = DNALangInterpreter()
    
    # Load and parse the existing AdvancedConsciousness.dna
    try:
        organism_id = interpreter.load_organism("AdvancedConsciousness.dna")
        organism = interpreter.get_organism(organism_id)
        
        print(f"Loaded organism: {organism.name}")
        print(f"Domain: {organism.dna.domain}")
        print(f"Consciousness target: {organism.dna.consciousness_target}")
        print(f"Genes: {len(organism.genome)}")
        
        # Create evolution engine
        engine = interpreter.create_evolution_engine(organism_id)
        
        # Run a few evolution steps
        print("\n🧬 Starting evolution simulation...")
        for i in range(5):
            evolved = engine.evolve_step()
            status = engine.get_status()
            print(f"Generation {status['generation']}: Fitness={status['fitness']:.3f}, Consciousness={status['consciousness']:.3f}")
            
            if status['consciousness_achieved']:
                print("🌟 Consciousness target achieved!")
                break
        
    except FileNotFoundError:
        print("AdvancedConsciousness.dna not found - creating example")
        
        # Demonstrate conversion
        python_code = """
class DataProcessor:
    def process_data(self, data):
        return data.transform()
    
    def validate(self, result):
        return result.is_valid()
"""
        
        dna_converted = interpreter.convert_to_dna_lang(python_code, "python")
        print("\n🔄 Converted Python code to DNA-Lang:")
        print(dna_converted)