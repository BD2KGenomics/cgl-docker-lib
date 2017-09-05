#!/usr/bin/env python2.7
# Trevor Pesout
import subprocess
import tempfile
import unittest


class TestRTGTools(unittest.TestCase):

    def test_docker_call(self):
        out, err = check_docker_output(tool='quay.io/ucsc_cgl/rtg_tools')
        self.assertTrue('RTG Tools 3.8.3' in out)

def check_docker_output(tool):
    command = 'docker run --rm {} version'.format(tool)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()
    return output

if __name__ == '__main__':
    unittest.main()