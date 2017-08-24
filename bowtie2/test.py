#!/usr/bin/env python2.7
# @author Frank Austin Nothaft fnothaft@berkeley.edu
import subprocess
import tempfile
import unittest


class TestBowtie2(unittest.TestCase):

    def test_docker_call(self):
        out, err = check_docker_output('quay.io/ucsc_cgl/bowtie2:latest')
        self.assertTrue('Bowtie 2 version 2.3.2' in out)

def check_docker_output(cmd):
    command = 'docker run ' + cmd
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()
    return output

if __name__ == '__main__':
    unittest.main()
