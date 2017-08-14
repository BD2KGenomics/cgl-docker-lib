#!/usr/bin/env python2.7
# @author Frank Austin Nothaft fnothaft@berkeley.edu
import subprocess
import tempfile
import unittest


class TestSNAP(unittest.TestCase):

    def test_docker_call(self):
        out, err = check_docker_output('quay.io/ucsc_cgl/snap:latest')
        self.assertTrue('Welcome to SNAP version 1.0beta.18.' in out)

def check_docker_output(cmd):
    command = 'docker run ' + cmd
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()
    return output

if __name__ == '__main__':
    unittest.main()
