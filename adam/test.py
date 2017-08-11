#!/usr/bin/env python2.7
# @author Frank Austin Nothaft fnothaft@berkeley.edu
import subprocess
import tempfile
import unittest


class TestADAM(unittest.TestCase):

    def test_docker_call(self):
        out, err = check_docker_output(tool='quay.io/ucsc_cgl/adam')
        self.assertTrue('ADAM_MAIN=org.bdgenomics.adam.cli.ADAMMain' in out)
        self.assertTrue('view : View certain reads from an alignment-record file.' in out)

def check_docker_output(tool):
    command = 'docker run ' + tool
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()
    return output

if __name__ == '__main__':
    unittest.main()
