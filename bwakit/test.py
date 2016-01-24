#!/usr/bin/env python2.7
# @author Frank Austin Nothaft fnothaft@berkeley.edu
import subprocess
import tempfile
import unittest


class TestBWAKIT(unittest.TestCase):

    def test_docker_call(self):
        out, err = check_docker_output(tool='quay.io/ucsc_cgl/bwakit:0.7.12')
        self.assertTrue('Map paired-end reads to GRCh38+ALT+decoy+HLA and perform HLA typing:' in out)

def check_docker_output(tool):
    command = 'docker run ' + tool
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()
    return output

if __name__ == '__main__':
    unittest.main()
