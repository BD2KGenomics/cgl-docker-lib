from __future__ import print_function

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import textwrap
from glob import glob
from uuid import uuid4

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def call_pipeline(mount, args):
    work_dir = os.path.join(mount, 'Toil-RNAseq-' + str(uuid4()))
    os.makedirs(work_dir)
    log.info('Temporary directory created: {}'.format(work_dir))
    config_path = os.path.join(work_dir, 'toil-rnaseq.config')
    job_store = os.path.join(args.resume, 'jobStore') if args.resume else os.path.join(work_dir, 'jobStore')
    with open(config_path, 'w') as f:
        f.write(generate_config(args.star, args.rsem, args.kallisto, mount, args.save_bam, args.save_wiggle))
    command = ['toil-rnaseq', 'run',
               job_store,
               '--config', config_path,
               '--workDir', work_dir,
               '--retryCount', '1']
    if args.resume:
        command.append('--restart')
    if args.cores:
        command.append('--maxCores={}'.format(args.cores))
    command.append('--samples')
    command.extend('file://' + x for x in args.samples)
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(e.message, file=sys.stderr)
    finally:
        log.info('Pipeline terminated, changing ownership of output files from root to user.')
        stat = os.stat(mount)
        subprocess.check_call(['chown', '-R', '{}:{}'.format(stat.st_uid, stat.st_gid), mount])
        if not args.no_clean:
            log.info('Cleaning up temporary directory: {}'.format(work_dir))
            shutil.rmtree(work_dir)
        else:
            log.info('Flag "--no-clean" was used, therefore {} was not deleted.'.format(work_dir))


def generate_config(star_path, rsem_path, kallisto_path, output_dir, disable_cutadapt, save_bam, save_wiggle):
    cutadapt = True if not disable_cutadapt else False
    return textwrap.dedent("""
        star-index: file://{star_path}
        kallisto-index: file://{kallisto_path}
        rsem-ref: file://{rsem_path}
        output-dir: {output_dir}
        cutadapt: {cutadapt}
        fastqc: true
        fwd-3pr-adapter: AGATCGGAAGAG
        rev-3pr-adapter: AGATCGGAAGAG
        ssec:
        gtkey:
        wiggle: {save_wiggle}
        save-bam: {save_bam}
        ci-test:
    """[1:].format(star_path=star_path, rsem_path=rsem_path, kallisto_path=kallisto_path, output_dir=output_dir,
                   cutadapt=cutadapt, save_wiggle=save_wiggle, save_bam=save_bam))


class UserError(Exception):
    pass


def require(expression, message):
    if not expression:
        raise UserError('\n\n' + message + '\n\n')


def check_for_input(tool_input, name):
    require(tool_input, 'Cannot find {0} input, please use --{0} and provide full path to file.'.format(name))
    return tool_input[0]


def main():
    """
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
    # Define argument parser for
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--samples', nargs='+', required=True,
                        help='Absolute path(s) to sample tarballs.')
    parser.add_argument('--star', type=str, default=None,
                        help='Absolute path to STAR index tarball.')
    parser.add_argument('--rsem', type=str, default=None,
                        help='Absolute path to rsem reference tarball.')
    parser.add_argument('--kallisto', type=str, default=None,
                        help='Absolute path to kallisto index (.idx) file.')
    parser.add_argument('--disable-cutadapt', action='store_true', default=False,
                        help='Cutadapt fails if samples are improperly paired. Use this flag to disable cutadapt.')
    parser.add_argument('--save-bam', action='store_true', default='false',
                        help='If this flag is used, genome-aligned bam is written to output.')
    parser.add_argument('--save-wiggle', action='store_true', default='false',
                        help='If this flag is used, wiggle files (.bg) are written to output.')
    parser.add_argument('--no-clean', action='store_true',
                        help='If this flag is used, temporary work directory is not cleaned.')
    parser.add_argument('--resume', type=str, default=None,
                        help='Pass the working directory that contains a job store to be resumed.')
    parser.add_argument('--cores', type=int, default=None,
                        help='Will set a cap on number of cores to use, default is all available cores.')
    args = parser.parse_args()
    # If no arguments provided, print full help menu
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    # Get name of most recent running container. If socket is mounted, should be this one.
    try:
        name = subprocess.check_output(['docker', 'ps', '--format', '{{.Names}}']).split('\n')[0]
    except subprocess.CalledProcessError as e:
        raise RuntimeError('No container detected, ensure Docker is being run with: '
                           '"-v /var/run/docker.sock:/var/run/docker.sock" as an argument. \n\n{}'.format(e.message))
    # Get name of mounted volume
    blob = json.loads(subprocess.check_output(['docker', 'inspect', name]))
    mounts = blob[0]['Mounts']
    # Ensure docker.sock is mounted correctly
    sock_mount = [x['Source'] == x['Destination'] for x in mounts if 'docker.sock' in x['Source']]
    require(len(sock_mount) == 1, 'Missing socket mount. Requires the following: '
                                  'docker run -v /var/run/docker.sock:/var/run/docker.sock')
    # Ensure formatting of command for 2 mount points
    if len(mounts) == 2:
        require(all(x['Source'] == x['Destination'] for x in mounts),
                'Docker Src/Dst mount points, invoked with the -v argument, '
                'must be the same if only using one mount point aside from the docker socket.')
        work_mount = [x['Source'] for x in mounts if 'docker.sock' not in x['Source']]
    else:
        # Ensure only one mirror mount exists aside from docker.sock
        mirror_mounts = [x['Source'] for x in mounts if x['Source'] == x['Destination']]
        work_mount = [x for x in mirror_mounts if 'docker.sock' not in x]
        require(len(work_mount) == 1, 'Wrong number of mirror mounts provided, see documentation.')
    # Look for inputs in work directory
    star = glob(os.path.join(work_mount[0], 'star*'))
    rsem = glob(os.path.join(work_mount[0], 'rsem*'))
    kallisto = glob(os.path.join(work_mount[0], 'kallisto*'))
    if not args.star:
        args.star = check_for_input(star, 'star')
    if not args.rsem:
        args.rsem = check_for_input(rsem, 'rsem')
    if not args.kallisto:
        args.kallisto = check_for_input(kallisto, 'kallisto')
    # If sample is given as relative path, assume it's in the work directory
    if not all(x.startswith('/') for x in args.samples):
        args.samples = [os.path.join(work_mount[0], x) for x in args.samples if not x.startswith('/')]
        log.info('\nSample given as relative path, assuming sample is in work directory: {}'.format(work_mount[0]))
    # Enforce file input standards
    require(all(x.startswith('/') for x in args.samples),
            "Sample inputs must point to a file's full path, "
            "e.g. '/full/path/to/sample1.tar'. You provided {}.".format(args.samples))
    require(all(x.startswith('/') for x in [args.star, args.kallisto, args.rsem]),
            "Sample inputs must point to a file's full path, "
            "e.g. '/full/path/to/sample1.tar'. You  provided {}.".format(args.samples))
    # Output log information
    log.info('The work mount is: {}'.format(work_mount[0]))
    log.info('Samples to run: {}'.format('\t'.join(args.samples)))
    log.info('Pipeline input locations: \n{}\n{}\n{}'.format(args.star, args.rsem, args.kallisto))
    call_pipeline(work_mount[0], args)


if __name__ == '__main__':
    main()
