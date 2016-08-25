from __future__ import print_function
import logging
from pipelineWrapper import PipelineWrapper

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


desc = """
Computational Genomics Lab, Genomics Institute, UC Santa Cruz
Dockerized Toil RNA-seq pipeline

RNA-seq fastqs are combined, aligned, and quantified with 2 different methods (RSEM and Kallisto)

General Usage:
docker run -v $(pwd):$(pwd) -v /var/run/docker.sock:/var/run/docker.sock \
quay.io/ucsc_cgl/rnaseq-cgl-pipeline --samples sample1.tar

Please see the complete documentation located at:
https://github.com/BD2KGenomics/cgl-docker-lib/tree/master/rnaseq-cgl-pipeline
or inside the container at: /opt/rnaseq-pipeline/README.md


Structure of RNA-Seq Pipeline (per sample)

              3 -- 4 -- 5
             /          |
  0 -- 1 -- 2 ---- 6 -- 8
             \          |
              7 ---------

0 = Download sample
1 = Unpack/Merge fastqs
2 = CutAdapt (adapter trimming)
3 = STAR Alignment
4 = RSEM Quantification
5 = RSEM Post-processing
6 = Kallisto
7 = FastQC
8 = Consoliate output and upload to S3
=======================================
Dependencies
Docker
"""
config = """star-index: file://{star}
kallisto-index: file://{kallisto}
rsem-ref: file://{rsem}
output-dir: {output_dir}
cutadapt: true
fastqc: true
fwd-3pr-adapter: AGATCGGAAGAG
rev-3pr-adapter: AGATCGGAAGAG
ssec:
gtkey:
wiggle: {save_wiggle}
save-bam: {save_bam}
ci-test:"""
if __name__ == '__main__':
    pipeline = PipelineWrapper('toil-rnaseq', desc, config)
    # define arguments
    with pipeline.arg_builder() as parser:
        parser.add_argument('--samples', nargs='+', required=True,
                        help='Absolute path(s) to sample tarballs.')
        parser.add_argument('--star', type=str, default=None,
                            help='Absolute path to STAR index tarball.')
        parser.add_argument('--rsem', type=str, default=None,
                            help='Absolute path to rsem reference tarball.')
        parser.add_argument('--kallisto', type=str, default=None,
                            help='Absolute path to kallisto index (.idx) file.')
        parser.add_argument('--save-bam', action='store_true', default='false',
                            help='If this flag is used, genome-aligned bam is written to output.')
        parser.add_argument('--save-wiggle', action='store_true', default='false',
                            help='If this flag is used, wiggle files (.bg) are written to output.')
        parser.add_argument('--cores', type=int, default=None,
                            help='Will set a cap on number of cores to use, default is all '
                                 'available cores.')

    with pipeline.command_builder() as (args, command):
        if args.cores:
            command.append('--maxCores={}'.format(args.cores))
        command.append('--samples')
        command.extend('file://' + x for x in args.samples)
    pipeline.run()
