from __future__ import print_function
import logging
from pipelineWrapper import PipelineWrapperBuilder
import os


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

config = """ref: file://{ref}
amb: file://{amb}
ann: file://{ann}
bwt: file://{bwt}
pac: file://{pac}
sa: file://{sa}
fai: file://{fai}
sort: {sort}
trim: {trim}
output-dir: {output_dir}
library: ILLUMINA
platform: ILLUMINA
program_unit: 12345
file_size: 1G
ssec:
rg-line:
alt:
suffix:
"""

if __name__ == '__main__':
    wrapper = PipelineWrapperBuilder('toil-bwa', desc, config)
    parser = wrapper.get_args()
    parser.add_argument('--samples', nargs='+', default=None,
                       help='Space delimited sample UUID and fastq files in the format: uuid url1 [url2].')
    parser.add_argument('--manifest', type=str, default=None,
                        help='Create manifest to pass uuid/urls in --sample for sample data.')
    parser.add_argument('--output-dir', type=str, required=True, default=None,
                        help='If this flag is used, will store output in this directory.')
    parser.add_argument('--ref', type=str, default=None,
                        help='Absolute path to reference fasta file.')
    parser.add_argument('--amb', type=str, default=None,
                        help='Absolute path to reference fasta file.')
    parser.add_argument('--ann', type=str, default=None,
                        help='Absolute path to reference fasta file.')
    parser.add_argument('--bwt', type=str, default=None,
                        help='Absolute path to reference fasta file.')
    parser.add_argument('--pac', type=str, default=None,
                        help='Absolute path to reference fasta file.')
    parser.add_argument('--sa', type=str, default=None,
                        help='Absolute path to reference fasta file.')
    parser.add_argument('--fai', type=str, default=None,
                        help='Absolute path to reference fasta file.')
    parser.add_argument('--sort', action='store_true', default='false',
                        help='If this flag is used, sorts bams.')
    parser.add_argument('--trim', action='store_true', default='false',
                        help='If this flag is used, trims adapters.')
    parser.add_argument('--cores', type=int, default=None,
                        help='Will set a cap on number of cores to use, default is all '
                             'available cores.')

    args = parser.parse_args()
    command = []
    if args.cores:
        command.append('--maxCores={}'.format(args.cores))

    if args.manifest:
        command.append('--manifest')
        command.append(args.manifest)
    elif args.samples:
        command.append('--manifest')

        uuid, urls = args.samples[0], args.samples[1:]

        string = uuid
        for url in urls:
            string += '\tfile://' + url

        filename = "manifest.tsv"
        with open(filename, 'w') as outfile:
            outfile.write(string)

        command.append(filename)
    else:
        # Display error for not providing either manifest or sample
        print("Must provide either a manifest samples in the form of 'UUID url1 [url2]'", file=sys.stderr)

    wrapper.run(args, command)
