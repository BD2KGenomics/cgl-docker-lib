#!/usr/bin/env cwl-runner

class: CommandLineTool
description: "A Docker container of the ADAM preprocessing Pipeline."
id: "adam-pipeline"
label: "ADAM preprocessing Pipeline"

dct:creator:
  "@id": "http://orcid.org/0000-0002-7729-7055"
  foaf:name: Frank Austin Nothaft
  foaf:mbox: "mailto:fnothaft@alumni.stanford.edu"

requirements:
  - class: DockerRequirement
	dockerPull: "quay.io/ucsc_cgl/adam-pipeline"
  - { import: node-engine.cwl }

hints:
  - class: ResourceRequirement
	coresMin: 2
	ramMin: 10920
	outdirMin: 15000
	description: "the process requires at least 10G of RAM for the BQSR known sites file."

inputs:
  - id: "#sample"
	type: string
	description: "Absolute path to the input SAM/BAM file."
	inputBinding:
	  position: 1
	  prefix: "--sample"

  - id: "#known-sites"
	type: string
	description: "Absolute path to the known-sites VCF for masking."
	inputBinding:
	  position: 2
	  prefix: "--known-sites"

  - id: "#memory"
	type: string
	description: "Memory in gibibytes to allocate for this pipeline."
	inputBinding:
	  position: 3
	  prefix: "--memory"

outputs:
  - id: "#adam-output"
	type: File
	outputBinding:
	  glob: .processed.bam
	description: "A sorted BAM file that has been processed."

baseCommand: ["--sample", "", "--known-sites", "", "--memory", ""]