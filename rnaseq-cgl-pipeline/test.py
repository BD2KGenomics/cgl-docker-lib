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
        out = check_docker_output(command=base + tool, assert_1=False)
        self.assertTrue('Please see the complete documentation' in out)
        self.assertFalse('foo bar' in out)
        # Check for required mirror mounts
        self.assertTrue('No required mirror mount' in check_docker_output(base + sock + tool + args))
        # Check for too many binds to docker socket
        self.assertTrue('Duplicate bind mount' in check_docker_output(
            base + sock + ['-v', '/foo:/var/run/docker.sock'] + mirror + tool + args))
        # Check for mirror mount when input/sample mount is used
        self.assertTrue('No required mirror mount' in check_docker_output(base + sock + sample + inputs + tool + args))
        # Check for more than one mirror mount
        self.assertTrue('Too many mirror mount' in check_docker_output(
            base + sock + mirror + ['-v', '/bar:/bar'] + tool + args))


def check_docker_output(command, assert_1=True):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()
    if assert_1:
        assert process.returncode == 1
    else:
        assert process.returncode == 0
    return output[0]


if __name__ == '__main__':
    unittest.main()
