#!/usr/bin/env python2.7
# John Vivan - jtvivian@gmail.com
import subprocess
import unittest


class TestCheckBiase(unittest.TestCase):

    def test_docker_call(self):
        out, err = check_docker_output(tool='quay.io/ucsc_cgl/checkbias')
        self.assertTrue('Usage: checkBias_2.0.py [options]' in out)

def check_docker_output(tool):
    command = 'docker run ' + tool
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()
    return output

if __name__ == '__main__':
    unittest.main()
