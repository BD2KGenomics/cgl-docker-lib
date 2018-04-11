#!/usr/bin/env python2.7
# John Vivian
import subprocess
import unittest


class TestGDC(unittest.TestCase):
    def test_docker_call(self):
        out, err = check_docker_output(tool='quay.io/ucsc_cgl/gdc-client')
        self.assertTrue('Genomic Data Common' in out)


def check_docker_output(tool):
    command = 'docker run ' + tool
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()
    return output


if __name__ == '__main__':
    unittest.main()
