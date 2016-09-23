#!/usr/bin/env python2.7
from subprocess import check_output, CalledProcessError, STDOUT
import unittest


class TestS3AM(unittest.TestCase):

    def test_docker_call(self):
        try:
            check_output(['docker', 'run','quay.io/ucsc_cgl/s3am'], stderr=STDOUT)
        except CalledProcessError as e:
            self.assertTrue('usage: s3am [--help] [--version]' in e.output)
        else:
            self.fail('Expected s3am to fail without enough arguments')

if __name__ == '__main__':
    unittest.main()
