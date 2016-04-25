#!/usr/bin/env cwl-runner

class: CommandLineTool
description: "A Docker container of the RNA-seq CGL Pipeline."
id: "rnaseq-cgl-pipeline"
label: "RNA-seq CGL Pipeline"

dct:creator:
  "@id": "http://orcid.org/0000-0002-4778-7723"
  foaf:name: John Vivian
  foaf:mbox: "mailto:jtvivian@gmail.com"

requirements:
  - class: DockerRequirement
	dockerPull: "quay.io/ucsc_cgl/rnaseq-cgl-pipeline"
  - { import: node-engine.cwl }

hints:
  - class: ResourceRequirement
	coresMin: 1
	ramMin: 40920
	outdirMin: 512000
	description: "the process requires at leasrt 40G of RAM"

inputs:
  - id: "#star"
	type: string
	description: "Absolute path to the star index tarball"
	inputBinding:
	  position: 1
	  prefix: "--star"

  - id: "#rsem"
	type: string
	description: "Absolute path to the rsem reference tarball"
	inputBinding:
	  position: 2
	  prefix: "--rsem"

  - id: "#star"
	type: string
	description: "Absolute path to the kallisto index file"
	inputBinding:
	  position: 3
	  prefix: "--kallisto"

outputs:
  - id: "#rnaseq-output"
	type: File
	outputBinding:
	  glob: .tar.gz
	description: "A tarball that contains quantification data."

baseCommand: ["--star", "", "--rsem", "", "--kallisto", ""]