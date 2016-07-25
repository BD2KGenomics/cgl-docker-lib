task adam {
  File in
  File knownSites
  String mem

  command {
    python /opt/adam-pipeline/wrapper.py --known-sites ${knownSites} --sample ${in} --output `pwd`/small.processed.bam --memory ${mem}
  }

  runtime {
    docker: "quay.io/ucsc_cgl/adam-pipeline"
  }

  output {
    File response = "small.processed.bam"
  }

}

workflow wf {
  call adam
}
