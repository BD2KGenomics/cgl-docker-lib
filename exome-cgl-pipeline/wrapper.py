from __future__ import print_function
import logging
from pipelineWrapper import PipelineWrapperBuilder

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

desc = """
Computational Genomics Lab, Genomics Institute, UC Santa Cruz
Dockerized Toil exome var pipeline

General Usage:
docker run -v $(pwd):$(pwd) -v /var/run/docker.sock:/var/run/docker.sock \
quay.io/ucsc_cgl/exome-var --normal normal1.tar --tumor tumor1.tar

   Please read the README.md located in the source directory or at:
    https://github.com/BD2KGenomics/toil-scripts/tree/master/src/toil_scripts/exome_variant_pipeline
    Structure of variant pipeline (per sample)
           1 2 3 4          14 -------
           | | | |          |        |
        0 --------- 5 ----- 15 -------- 17
                    |       |        |
                   ---      16 -------
                   | |
                   6 7
                   | |
                   8 9
                   | |
                  10 11
                   | |
                  12 13
    0 = Start node
    1 = reference index
    2 = reference dict
    3 = normal bam index
    4 = tumor bam index
    5 = pre-processing node / DAG declaration
    6,7 = RealignerTargetCreator
    8,9 = IndelRealigner
    10,11 = BaseRecalibration
    12,13 = PrintReads
    14 = MuTect
    15 = Pindel
    16 = MuSe
    17 = Consolidate Output and move/upload results
=======================================
Dependencies
Docker
"""

config = ("""reference: file://{reference}
phase: file://{phase}
mills: file://{mills}
dbsnp: file://{dbsnp}
cosmic: file://{cosmic}
output-dir: {output_dir}
run-mutect: {run_mutect}
run-pindel: {run_pindel}
run-muse: {run_muse}
preprocessing: {preprocess}
ssec:
gtkey:
ci-test: {ci_test}""")

if __name__ == '__main__':
    wrapper = PipelineWrapperBuilder('toil-exome', desc, config)
    parser = wrapper.get_args()
    parser.add_argument('--normal', type=str, required=True,
                        help='Path for the normal BAM. The UUID for the sample must be given '
                             'with the "--uuid" flag.')
    parser.add_argument('--tumor', type=str, required=True,
                        help='Path for the tumor BAM. The UUID for the sample must be given '
                             'with the "--uuid" flag.')
    parser.add_argument('--uuid', type=str, required=True,
                        help='Provide the UUID of a sample when using the"--tumor" and '
                             '"--normal" option.')
    parser.add_argument('--reference', type=str, required=True, default=None,
                        help='Absolute path to reference genome.')
    parser.add_argument('--phase', type=str, required=True, default=None,
                        help='Absolute path to phase indels VCF.')
    parser.add_argument('--mills', type=str, required=True, default=None,
                        help='Absolute path to Mills indel VCF.')
    parser.add_argument('--dbsnp', type=str, required=True, default=None,
                        help='Absolute path to dbsnp VCF.')
    parser.add_argument('--cosmic', type=str, required=True, default=None,
                        help='Absolute path to cosmic VCF.')
    parser.add_argument('--output-dir', type=str, required=True, default=None,
                        help='If this flag is used, will store output in this directory.')
    parser.add_argument('--run-mutect', action='store_true', default='false',
                        help='If this flag is used, will run MuTect to do mutation calls.')
    parser.add_argument('--run-pindel', action='store_true', default='false',
                        help='If this flag is used, will run pindel to analyze indel.')
    parser.add_argument('--run-muse', action='store_true', default='false',
                        help='If this flag is used, will run MuSe to do mutation calls.')
    parser.add_argument('--preprocess', action='store_true', default='false',
                        help='If this flag is used, will perform indel realignment and base '
                             'quality score recalibration.')
    parser.add_argument('--ci-test', action='store_true', default='false',
                        help='If this flag is used, will run continuous integration testing.')
    parser.add_argument('--cores', type=int, default=None,
                        help='Will set a cap on number of cores to use, default is all '
                             'available cores.')

    args = parser.parse_args()
    command = []
    if args.cores:
        command.append('--maxCores={}'.format(args.cores))
    command.append('--normal')
    command.append('file://%s' % args.normal)
    command.append('--tumor')
    command.append('file://%s' % args.tumor)
    command.append('--uuid')
    command.append(args.uuid)

    wrapper.run(args, command)
