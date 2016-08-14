#!/usr/bin/env python2.7
import subprocess
import sys
import unittest


class TestRNASeqPipeline(unittest.TestCase):

    def test_docker_call(self):
        # print sys.argv
        tool = ['quay.io/ucsc_cgl/rnaseq-cgl-pipeline:1.9.1--{}'.format(tag)]
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
        self.assertTrue('Wrong number of mirror mounts' in check_docker_output(base + sock + tool + args))
        # Check for mirror mount when input/sample mount is used
        self.assertTrue('Wrong number of mirror mounts' in
                        check_docker_output(base + sock + sample + inputs + tool + args))
        # Check for more than one mirror mount
        self.assertTrue('Wrong number of mirror mounts' in check_docker_output(
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
    tag = sys.argv[1]
    del sys.argv[1]

    unittest.main()
