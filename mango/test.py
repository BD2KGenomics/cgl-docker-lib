#!/usr/bin/env python2.7
# @author Alyssa Morrow akmorrow@berkeley.edu
import subprocess
import tempfile
import unittest


class TestMango(unittest.TestCase):

    def test_docker_call_browser(self):
        out, err = check_docker_output(tool='quay.io/ucsc_cgl/mango')
        self.assertTrue('Using spark-submit=' in out)
        self.assertTrue('Argument "genome" is required' in out)

    def test_docker_call_notebook(self):
        out, err = check_docker_output(tool='--entrypoint=/opt/cgl-docker-lib/mango/bin/mango-notebook quay.io/ucsc_cgl/mango')
        self.assertTrue('Writing notebook server' in out)

def check_docker_output(tool):
    command = 'docker run ' + tool
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()
    return output

if __name__ == '__main__':
    unittest.main()
