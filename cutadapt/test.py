#!/usr/bin/env python2.7
# John Vivian
import subprocess
import tempfile
import unittest


class TestCutadapt(unittest.TestCase):

    def test_docker_call(self):
        self.assertEqual(0, docker_call(tool='quay.io/ucsc_cgl/cutadapt',
                                        tool_parameters=[], work_dir=tempfile.gettempdir()))


def docker_call(tool, tool_parameters, work_dir):
    """
    Makes subprocess call of a command to a docker container.
    work_dir MUST BE AN ABSOLUTE PATH or the call will fail.

    Input1: Docker tool to be pulled and run (repo/tool_name)
    Input2: parameters to the Docker tool being called
    Input3: working directory where input files are located
    """
    # base_docker_call = 'sudo docker run -v {}:/data'.format(work_dir)
    base_docker_call = 'docker run -v {}:/data'.format(work_dir)
    call = base_docker_call.split() + [tool] + tool_parameters
    try:
        ret_code = subprocess.check_call(call)
    except subprocess.CalledProcessError:
        raise RuntimeError('docker command returned a non-zero exit status for cmd {}'.format(call))
    except OSError:
        raise RuntimeError('docker not found on system. Install on all nodes.')
    return ret_code

if __name__ == '__main__':
    unittest.main()