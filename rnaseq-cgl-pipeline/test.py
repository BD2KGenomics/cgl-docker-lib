#!/usr/bin/env python2.7
# John Vivian
import subprocess
import unittest


class TestRNASeqPipeline(unittest.TestCase):

    def test_docker_call(self):
        tool = ['quay.io/ucsc_cgl/rnaseq-cgl-pipeline']
        base = ['docker', 'run']
        args = ['--star=/foo', '--rsem=/foo', '--kallisto=/foo', '--samples=/foo']
        sock = ['-v', '/var/run/docker.sock:/var/run/docker.sock']
        mirror = ['-v', '/foo:/foo']
        sample = ['-v', '/bar:/samples']
        inputs = ['-v', '/foobar:/inputs']
        # Check base call for help menu
        out = check_docker_output(command=base + tool)
        self.assertTrue('Please see the complete documentation' in out)
        self.assertFalse('foo bar' in out)
        # Check for not enough mirror mounts
        self.assertTrue('IllegalArgumentException' in check_docker_output(base + sock + tool + args))
        # Check for too many binds to docker socket
        self.assertTrue('Duplicate bind mount' in check_docker_output(
            base + sock + ['-v', '/foo:/var/run/docker.sock'] + mirror + tool + args))
        # Check for mirror mount when input/sample mount is used
        self.assertTrue('IllegalArgumentException' in check_docker_output(base + sock + sample + inputs + tool + args))
        # Check for more than one mirror mount
        self.assertTrue('IllegalArgumentException' in check_docker_output(
            base + sock + mirror +  ['-v', '/bar:/bar'] + tool + args))


def check_docker_output(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()
    return output[0]


class IllegalArgumentException(Exception):
    pass

if __name__ == '__main__':
    unittest.main()
