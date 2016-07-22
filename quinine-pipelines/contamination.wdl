task contamination {
  File reads
  File population_vcf
  File sample_vcf
  String mem

  command {
    /opt/toil-scripts/quinine-pipelines.sh contamination --reads ${reads} --population ${population_vcf} --sample-vcf ${sample_vcf} --memory ${mem} --output `pwd`/contamination.txt
  }

  runtime {
    docker: "quay.io/ucsc_cgl/quinine-pipelines"
  }

  output {
    File response = "contamination.txt"
  }

}

workflow wf {
  call contamination
}