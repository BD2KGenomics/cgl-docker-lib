import argparse
import os
import shutil
import subprocess
import json
import logging
from uuid import uuid4

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def call_pipeline(mount, args):
    uuid = 'Toil-RNAseq-' + str(uuid4())
    if not os.path.isdir(mount + uuid):
        os.makedirs(os.path.join(mount, uuid))
    os.environ['PYTHONPATH'] = '/opt/rnaseq-pipeline/src'
    command = ['python', '-m', 'toil_scripts.rnaseq_cgl.rnaseq_cgl_pipeline',
               os.path.join(mount, 'jobStore'),
               '--retryCount', '1',
               '--output-dir', mount,
               '--workDir', os.path.join(mount, uuid),
               '--star-index', 'file://'+ args.star,
               '--rsem-ref', 'file://' + args.rsem,
               '--kallisto-index', 'file://' + args.kallisto,
               '--sample-urls']
    command.extend(['file://' + x for x in args.samples])
    if args.restart:
        command.append('--restart')
    try:
        subprocess.check_call(command)
    finally:
        stat = os.stat(mount)
        subprocess.check_call(['chown', '-R', '{}:{}'.format(stat.st_uid, stat.st_gid), mount])
        shutil.rmtree(os.path.join(mount, uuid))


def main():
    """
    Please see the complete documentation located at:
    https://github.com/BD2KGenomics/cgl-docker-lib/tree/master/rnaseq-cgl-pipeline
    or in the container at:
    /opt/rnaseq-pipeline/README.md

    All samples and inputs must be reachable via Docker "-v" mount points and use
    the Destination path prefix.
    """
    # Define argument parser for
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--star', type=str, required=True,
                        help='Absolute path to STAR index tarball.')
    parser.add_argument('--rsem', type=str, required=True,
                        help='Absolute path to rsem reference tarball.')
    parser.add_argument('--kallisto', type=str, required=True,
                        help='Absolute path to kallisto index (.idx) file.')
    parser.add_argument('--samples', nargs='+', required=True,
                        help='Absolute path(s) to sample tarballs.')
    parser.add_argument('--restart', action='store_true', default=False,
                        help='Add this flag to restart the pipeline. Requires existing job store.')
    args = parser.parse_args()
    # Get name of most recent running container (should be this one)
    name = subprocess.check_output(['docker', 'ps', '--format', '{{.Names}}']).split('\n')[0]
    # Get name of mounted volume
    blob = json.loads(subprocess.check_output(['docker', 'inspect', name]))
    mounts = blob[0]['Mounts']
    # Ensure docker.sock is mounted correctly
    sock_mount = [x['Source'] == x['Destination'] for x in mounts if 'docker.sock' in x['Source']]
    if len(sock_mount) != 1:
        raise IllegalArgumentException('Missing socket mount. Requires the following:'
                                       'docker run -v /var/run/docker.sock:/var/run/docker.sock')
    # Ensure formatting of command for 2 mount points
    if len(mounts) == 2:
        if not all(x['Source'] == x['Destination'] for x in mounts):
            raise IllegalArgumentException('Docker Src/Dst mount points, invoked with the -v argument,'
                                           'must be the same if only using one mount point aside from the '
                                           'docker socket.')
        work_mount = [x['Source'] for x in mounts if 'docker.sock' not in x['Source']]
    else:
        # Ensure only one mirror mount exists aside from docker.sock
        mirror_mounts = [x['Source'] for x in mounts if x['Source'] == x['Destination']]
        work_mount = [x for x in mirror_mounts if 'docker.sock' not in x]
        if len(work_mount) > 1:
            raise IllegalArgumentException('Too many mirror mount points provided, see documentation.')
        if len(work_mount) == 0:
            raise IllegalArgumentException('No required mirror mount point provided, see documentation.')
    # Enforce file input standards
    if not all(x.startswith('/') for x in args.samples):
        raise IllegalArgumentException("Sample inputs must point to a file's full path, e.g. "
                                       "'/full/path/to/sample1.tar'. You provided {}.".format(args.samples))
    if not all(x.startswith('/') for x in [args.star, args.kallisto, args.rsem]):
        raise IllegalArgumentException("Sample inputs must point to a file's full path, e.g. "
                                       "'/full/path/to/sample1.tar'. You  provided {}.".format(args.samples))
    call_pipeline(work_mount[0], args)


class IllegalArgumentException(Exception):
    pass


if __name__ == '__main__':
    main()
