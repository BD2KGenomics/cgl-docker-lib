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
from glob import glob
from uuid import uuid4

log = logging.getLogger()


class PipelineWrapper(object):
    def __init__(self, name, desc, *inputs):
        """
        :param str name: The name of the command to start the workflow.
        :param str desc: The description of the workflow.
        :param inputs: A series of strings representing the names of local file types that are
            required inputs of the workflow. Note that these names must exactly match arguments
            added in arg_builder.
        """
        self._name = name
        self._desc = desc
        self._input = inputs
        self._args = None
        self._mount = None
        self.config = None
        self._command = []

    def run(self):
        if self._args is None:
            raise DefinitionError('Command line arguments must be defined with arg_builder() in '
                                  'order to run the pipeline.')
        if self.config == None:
            raise DefinitionError('Config must be defined in order to run the pipeline.')
        if self._command == []:
            raise DefinitionError('Command must be defined with command_builder() in order to run '
                                  'the pipeline.')

        try:
            subprocess.check_call(self._command)
        except subprocess.CalledProcessError as e:
            print(e, file=sys.stderr)
            print("The command '%s' failed with message '%s'" % (self._command, e.message),
                  file=sys.stderr)
        finally:
            log.info('Pipeline terminated, changing ownership of output files from root to user.')
            stat = os.stat(self._mount)
            subprocess.check_call(['chown', '-R', '{}:{}'.format(stat.st_uid, stat.st_gid),
                                   self._mount])
            if not self._args.no_clean:
                log.info('Cleaning up temporary directory: {}'.format(self._workdir))
                shutil.rmtree(self._workdir)
            else:
                log.info('Flag "--no-clean" was used, therefore {} was not deleted.'
                         .format(self._workdir))

        return False # let exceptions through


    @contextmanager
    def arg_builder(self):
        """
        Use this context manager to add arguments to an argparse object.
        """
        parser = argparse.ArgumentParser(description=self._desc,
                                         formatter_class=argparse.RawTextHelpFormatter)
        # If no arguments provided, print full help menu
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
        yield parser
        self._args = parser.parse_args()

    @contextmanager
    def command_builder(self):
        """
        Use this context manager to define a command to run the pipeline. A command should be
        defined as a list of strings that when joined on space create a single bash command.
        """
        if self._args is None:
            raise DefinitionError('Args must be defined with arg_builder() before command_builder()'
                                  ' can be invoked.')
        if self.config is None:
            raise DefinitionError('Config must be defined before command_builder() can be invoked.')

        self._prepare_mount()
        # prepare workdir
        self._workdir = os.path.join(self._mount, 'Toil-%s-%s' % (self._name, uuid4()))
        os.makedirs(self._workdir)
        log.info('Temporary directory created: {}'.format(self._workdir))

        # prepare config
        args = vars(self._args)
        args['output_dir'] = self._mount
        self.config = textwrap.dedent(self.config[1:].format(**args))
        config_path = os.path.join(self._workdir, 'config')
        with open(config_path, 'w') as f:
            f.write(self.config)

        if self._args.resume:
            job_store = os.path.join(self._args.resume, 'jobStore')
        else:
            job_store = os.path.join(self._workdir, 'jobStore')

        command = [self._name, 'run', job_store,
                    '--config', config_path,
                    '--workDir', self._workdir,
                    '--retryCount', '1']
        yield self._args, command
        self._command += command

    def _prepare_mount(self):
        """
        Prepares mount and input files.
        """
        assert self._args is not None

        # Get name of most recent running container. If socket is mounted, should be this one.
        try:
            name = subprocess.check_output(['docker', 'ps', '--format', '{{.Names}}']).split('\n')[0]
        except subprocess.CalledProcessError as e:
            raise RuntimeError('No container detected, ensure Docker is being run with: '
                               '"-v /var/run/docker.sock:/var/run/docker.sock" as an argument.'
                               ' \n\n{}'.format(e.message))
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
            require(len(work_mount) == 1, 'Wrong number of mirror mounts provided, see '
                                          'documentation.')

        inputs = []
        for s in self._input:
            if getattr(self._args, s) is None:
                inputs.append(check_for_input(glob(os.path.join(work_mount[0], s + '*')), s))
            else:
                inputs.append(getattr(self._args, s))
        require(all(x.startswith('/') for x in inputs),
            "Inputs must point to a file's full path, "
            "e.g. '/full/path/to/input'. You  provided {}.".format(inputs))
        #require(all(x.startswith('/') for x in self._args.samples),
        #        "Sample inputs must point to a file's full path, "
        #        "e.g. '/full/path/to/sample1.tar'. You provided {}.".format(self._args.samples))

        # Output log information
        log.info('The work mount is: {}'.format(work_mount[0]))
        #log.info('Samples to run: {}'.format('\t'.join(self._args.samples)))
        log.info('Pipeline input locations: \n{}'.format(inputs))
        self._mount = work_mount[0]

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
