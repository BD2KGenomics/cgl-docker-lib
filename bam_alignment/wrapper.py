from __future__ import print_function
import logging
from pipelineWrapper import PipelineWrapper

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

desc = """
Computational Genomics Lab, Genomics Institute, UC Santa Cruz
Dockerized Toil bwa alignment pipeline

General Usage:
docker run -v $(pwd):$(pwd) -v /var/run/docker.sock:/var/run/docker.sock \
quay.io/ucsc_cgl/bwa-alignment --samples sample1.tar

Please read the README.md located in the source directory or at:
    https://github.com/BD2KGenomics/toil-scripts/tree/master/src/toil_scripts/bwa_alignment
    Structure of the BWA pipeline (per sample)
        0 --> 1
    0 = Download sample
    1 = Run BWA-kit
=======================================
Dependencies
Docker
"""
if __name__ == '__main__':
    pipeline = PipelineWrapper('toil-bwa', desc, 'ref')
    with pipeline.arg_builder() as parser:
        parser.add_argument('--samples', nargs='+', required=True,
                        help='Absolute path(s) to samples.')
        parser.add_argument('--ref', type=str, default=None,
                            help='Absolute path to reference fasta file.')
        parser.add_argument('--sort', action='store_true', default='false',
                            help='If this flag is used, sorts bams.')
        parser.add_argument('--trim', action='store_true', default='false',
                            help='If this flag is used, trims adapters.')
        parser.add_argument('--no-clean', action='store_true',
                            help='If this flag is used, temporary work directory is not cleaned.')
        parser.add_argument('--resume', type=str, default=None,
                            help='Pass the working directory that contains a job store to be '
                                 'resumed.')
        parser.add_argument('--cores', type=int, default=None,
                            help='Will set a cap on number of cores to use, default is all '
                                 'available cores.')
    pipeline.config = ("""
        ref: file://{ref}
        output-dir: {output_dir}
        library: Illumina
        platform: Illumina
        program_unit: 12345
        file-size: 50G
        sort: {sort}
        trim: {trim}
        amb: s3://cgl-pipeline-inputs/alignment/hg19.fa.amb
        ann: s3://cgl-pipeline-inputs/alignment/hg19.fa.ann
        bwt: s3://cgl-pipeline-inputs/alignment/hg19.fa.bwt
        pac: s3://cgl-pipeline-inputs/alignment/hg19.fa.pac
        sa: s3://cgl-pipeline-inputs/alignment/hg19.fa.sa
        fai: s3://cgl-pipeline-inputs/alignment/hg19.fa.fai
        ssec:
        rg-line:
        alt:
        mock-mode:""")

    with pipeline.command_builder() as (args, command):
        if args.resume:
            command.append('--restart')
        if args.cores:
            command.append('--maxCores={}'.format(args.cores))
        command.append('--sample')
        command.extend('file://' + x for x in args.samples)
    pipeline.run()
