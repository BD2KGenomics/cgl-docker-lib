task targeted {
  File reads
  File bait
  File targets
  String mem

  command {
    /opt/toil-scripts/quinine-pipelines.sh targeted --reads ${reads} --bait ${bait} --targets ${targets} --output `pwd`/targeted.txt
  }

  runtime {
    docker: "quay.io/ucsc_cgl/quinine-pipelines"
  }

  output {
    File response = "targeted.txt"
  }

}

workflow wf {
  call targeted
}