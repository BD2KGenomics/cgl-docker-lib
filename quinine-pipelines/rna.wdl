task rna {
  File reads
  File transcriptome
  String mem

  command {
    /opt/toil-scripts/quinine-pipelines.sh rna --reads ${reads} --transcriptome ${transcriptome} --memory ${mem} --output `pwd`/rna.txt
  }

  runtime {
    docker: "quay.io/ucsc_cgl/quinine-pipelines"
  }

  output {
    File response = "rna.txt"
  }

}

workflow wf {
  call rna
}