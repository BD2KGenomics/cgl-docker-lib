from __future__ import print_function

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import textwrap
from contextlib import contextmanager

log = logging.getLogger()


class PipelineWrapper(object):
    """
    This class can be used to define wrapper scripts to run specific Toil pipelines in docker
    containers. The purpose of this class is to provide a convenient way to define a command line
    interface for a wrapper script and the logic to use this interface to run a pipeline.
    """
    def __init__(self, name, desc, config):
        """
        :param str name: The name of the command to start the workflow.
        :param str desc: The description of the workflow.
        :param str config: A format string where each key exactly matches the name of an argument
            defined in the arg_builder context manager. Note that dashes in argument names should be
            changed to underscores in this string e.g. 'no-clean' should be 'no_clean'.
        """
        self._name = name
        self._desc = desc
        self._config = config
        self._args = None
        self._command = None

    def run(self):
        """
        Invokes the pipeline with the defined command. Command line arguments, and the command need
        to be set with arg_builder, and command_builder respectively before this method can be
        invoked.
        """
        if self._args is None:
            raise DefinitionError('Command line arguments must be defined with arg_builder() in '
                                  'order to run the pipeline.')
        if self._command is None:
            raise DefinitionError('Command must be defined with command_builder() in order to run '
                                  'the pipeline.')
        try:
            subprocess.check_call(self._command)
        except subprocess.CalledProcessError as e:
            print(e, file=sys.stderr)
        finally:
            log.info('Pipeline terminated, changing ownership of output files from root to user.')
            stat = os.stat(self._mount)
            subprocess.check_call(['chown', '-R', '{}:{}'.format(stat.st_uid, stat.st_gid),
                                   self._mount])
            if self._args.no_clean:
                log.info('Flag "--no-clean" was used, therefore %s was not deleted.', self._workdir)
            else:
                log.info('Cleaning up temporary directory: %s', self._workdir)
                shutil.rmtree(self._workdir)

    @contextmanager
    def arg_builder(self):
        """
        Use this context manager to add arguments to an argparse object with the add_argument
        method. Arguments must be defined before the command is defined. Note that
        no-clean and resume are added upon exit and should not be added in the context manager. For
        more info about these default arguments see below.
        """
        parser = argparse.ArgumentParser(description=self._desc,
                                         formatter_class=argparse.RawTextHelpFormatter)
        # If no arguments provided, print full help menu
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
        yield parser
        # default args
        parser.add_argument('--no-clean', action='store_true',
                            help='If  this flag is used, temporary work directory is not cleaned.')
        parser.add_argument('--resume', action='store_true',
                            help='If  this flag is used, a previously uncleaned workflow in the '
                                 'same directory will be resumed')
        self._args = parser.parse_args()

    @contextmanager
    def command_builder(self):
        """
        Use this context manager to define a command to run the pipeline. A command should be
        defined as a list of strings that when joined on space create a single bash command. This
        context manager yields a list and a parsed args object.

        Note that arguments common between different toil pipelines are added automatically and do
        not need to be added in the context manager. Specifically the yielded list will already
        contain a command of the following scheme:
            <name of pipeline command> run <jobstore path> --config <path> --workDir <path>
            --retryCount <1>

        The --restart argument is added if needed after the context manager exits.
        """
        if self._args is None:
            raise DefinitionError('Args must be defined with arg_builder() before command_builder()'
                                  ' can be invoked.')
        # prepare workdir
        mount = self._prepare_mount()
        self._workdir = os.path.join(mount, 'Toil-%s' % (self._name))
        if os.path.exists(self._workdir):
            if self._args.resume:
                 log.info('Reusing temporary directory: %s', self._workdir)
            else:
                raise UserError('Temporary directory {} already exists. Run with --resume option or'
                                ' remove directory.'.format(self._workdir))
        else:
            os.makedirs(self._workdir)
            log.info('Temporary directory created: %s', self._workdir)

        # prepare config
        args = vars(self._args)
        args['output_dir'] = mount
        self._config = textwrap.dedent(self._config.format(**args))
        args = self._args
        config_path = os.path.join(self._workdir, 'config')
        with open(config_path, 'w') as f:
            f.write(self._config)
        command = [self._name, 'run', os.path.join(self._workdir, 'jobStore'),
                    '--config', config_path,
                    '--workDir', self._workdir,
                    '--retryCount', '1']
        yield args, command
        if args.resume:
            command.append('--restart')
        self._command = command

    def _prepare_mount(self):
        assert self._args is not None
        # Get name of most recent running container. If socket is mounted, should be this one.
        name_command = ['docker', 'ps', '--format', '{{.Names}}']
        try:
            name = subprocess.check_output(name_command).split('\n')[0]
        except subprocess.CalledProcessError as e:
            raise RuntimeError('No container detected, ensure Docker is being run with: '
                               '"-v /var/run/docker.sock:/var/run/docker.sock" as an argument.'
                               ' \n\n{}'.format(e.message))
        # Get name of mounted volume
        blob = json.loads(subprocess.check_output(['docker', 'inspect', name]))
        mounts = blob[0]['Mounts']
        # Ensure docker.sock is mounted correctly
        sock_mnt = [x['Source'] == x['Destination'] for x in mounts if 'docker.sock' in x['Source']]
        require(len(sock_mnt) == 1, 'Missing socket mount. Requires the following: '
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
            require(len(work_mount) == 1, 'Wrong number of mirror mounts provided, see '
                                          'documentation.')
        # Output log information
        log.info('The work mount is: %s', work_mount[0])
        log.info('Samples to run: %s', '\t'.join(self._args.samples))
        self._mount = work_mount[0]
        return self._mount


class UserError(Exception):
    pass


class DefinitionError(Exception):
    pass


def require(expression, message):
    if not expression:
        raise UserError('\n\n' + message + '\n\n')

def check_for_input(tool_input, name):
    require(tool_input, 'Cannot find {0} input, please use --{0} and provide full path to file.'
            .format(name))
    return tool_input[0]
