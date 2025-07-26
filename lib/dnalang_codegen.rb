#!/usr/bin/env ruby
# dnalang-codegen v0.2.0 - Ruby DSL for organism definition and code generation
# Part of the DNA-Lang Autonomous Evolution Platform

require 'json'
require 'time'

module DNALang
  class CodeGenerator
    attr_reader :organism_data, :output

    def initialize(&block)
      @organism_data = {}
      @output = []
      @comments = []
      
      instance_eval(&block) if block_given?
    end

    def comment(text)
      @comments << "# #{text}"
    end

    def organism(name, &block)
      @organism_data[:name] = name
      @organism_data[:created_at] = Time.now.utc.iso8601
      
      organism_builder = OrganismBuilder.new
      organism_builder.instance_eval(&block)
      
      @organism_data.merge!(organism_builder.data)
    end

    def generate
      output = []
      
      # Add header comments
      output += @comments
      output << ""
      
      # Generate organism definition in DNA-Lang format
      output << "ORGANISM #{@organism_data[:name]}"
      output << "{"
      
      # DNA section
      if @organism_data[:dna]
        output << "  DNA {"
        @organism_data[:dna].each do |key, value|
          output << "    #{key}: #{format_value(value)}"
        end
        output << "  }"
        output << ""
      end
      
      # Genome section with genes
      if @organism_data[:genome]
        output << "  GENOME {"
        @organism_data[:genome].each do |gene|
          output += format_gene(gene, 4)
        end
        output << "  }"
        output << ""
      end
      
      # Agents section
      if @organism_data[:agents]
        output << "  AGENTS {"
        @organism_data[:agents].each do |name, config|
          output << "    #{name}: #{config}"
        end
        output << "  }"
      end
      
      output << "}"
      
      # Add metadata as JSON comment
      output << ""
      output << "# Organism Metadata (JSON):"
      output << "# #{@organism_data.to_json}"
      
      output.join("\n")
    end

    private

    def format_value(value)
      case value
      when String
        "\"#{value}\""
      when Numeric
        value.to_s
      when TrueClass, FalseClass
        value.to_s
      else
        "\"#{value}\""
      end
    end

    def format_gene(gene, indent)
      lines = []
      indent_str = " " * indent
      
      lines << "#{indent_str}GENE #{gene[:name]} {"
      lines << "#{indent_str}  purpose: #{format_value(gene[:purpose])}"
      lines << "#{indent_str}  expression_level: #{gene[:expression_level]}"
      
      if gene[:mutations]
        lines << "#{indent_str}  MUTATIONS {"
        gene[:mutations].each do |mutation|
          lines += format_mutation(mutation, indent + 4)
        end
        lines << "#{indent_str}  }"
      end
      
      lines << "#{indent_str}}"
      lines
    end

    def format_mutation(mutation, indent)
      lines = []
      indent_str = " " * indent
      
      lines << "#{indent_str}#{mutation[:name]} {"
      
      if mutation[:trigger_conditions]
        lines << "#{indent_str}  trigger_conditions: ["
        mutation[:trigger_conditions].each do |condition|
          lines << "#{indent_str}    {metric: #{format_value(condition[:metric])}, operator: #{format_value(condition[:operator])}, value: #{condition[:value]}}"
        end
        lines << "#{indent_str}  ]"
      end
      
      if mutation[:methods]
        lines << "#{indent_str}  methods: [#{mutation[:methods].map { |m| format_value(m) }.join(', ')}]"
      end
      
      mutation.each do |key, value|
        next if [:name, :trigger_conditions, :methods].include?(key)
        lines << "#{indent_str}  #{key}: #{format_value(value)}"
      end
      
      lines << "#{indent_str}}"
      lines
    end
  end

  class OrganismBuilder
    attr_reader :data

    def initialize
      @data = {}
    end

    def dna(&block)
      dna_builder = DNABuilder.new
      dna_builder.instance_eval(&block)
      @data[:dna] = dna_builder.data
    end

    def genome(&block)
      genome_builder = GenomeBuilder.new
      genome_builder.instance_eval(&block)
      @data[:genome] = genome_builder.genes
    end

    def agents(&block)
      agents_builder = AgentsBuilder.new
      agents_builder.instance_eval(&block)
      @data[:agents] = agents_builder.data
    end
  end

  class DNABuilder
    attr_reader :data

    def initialize
      @data = {}
    end

    def method_missing(method_name, *args)
      @data[method_name] = args.first
    end
  end

  class GenomeBuilder
    attr_reader :genes

    def initialize
      @genes = []
    end

    def gene(name, &block)
      gene_builder = GeneBuilder.new(name)
      gene_builder.instance_eval(&block)
      @genes << gene_builder.data
    end
  end

  class GeneBuilder
    attr_reader :data

    def initialize(name)
      @data = { name: name, mutations: [] }
    end

    def purpose(text)
      @data[:purpose] = text
    end

    def expression_level(level)
      @data[:expression_level] = level
    end

    def mutations(&block)
      mutations_builder = MutationsBuilder.new
      mutations_builder.instance_eval(&block)
      @data[:mutations] = mutations_builder.mutations
    end
  end

  class MutationsBuilder
    attr_reader :mutations

    def initialize
      @mutations = []
    end

    def method_missing(method_name, *args, &block)
      mutation_builder = MutationBuilder.new(method_name)
      mutation_builder.instance_eval(&block) if block_given?
      @mutations << mutation_builder.data
    end
  end

  class MutationBuilder
    attr_reader :data

    def initialize(name)
      @data = { name: name }
    end

    def trigger_conditions(conditions)
      @data[:trigger_conditions] = conditions
    end

    def methods(method_list)
      @data[:methods] = method_list
    end

    def method_missing(method_name, *args)
      @data[method_name] = args.first
    end
  end

  class AgentsBuilder
    attr_reader :data

    def initialize
      @data = {}
    end

    def method_missing(method_name, *args)
      @data[method_name] = args.first
    end
  end
end