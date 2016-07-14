#!/usr/bin/env python2.7

import os
import subprocess
import unittest


class TestADAMPipeline(unittest.TestCase):

    def test_docker_call(self):
        
        # get working directory
        pwd = os.getcwd()
        outfile = '%s/test/small.processed.bam' % pwd

        # check for output file in ./test and clean if necessary
        if os.path.exists(outfile):
            os.remove(outfile)

        # build commandline
        tool = ['quay.io/ucsc_cgl/adam-pipeline']
        base = ['docker', 'run']
        args = ['--sample', '/%s/test/small.sam' % pwd,
                '--known-sites', '/%s/test/small.vcf' % pwd,
                '--memory', '1']
        sock = ['-v', '/var/run/docker.sock:/var/run/docker.sock']
        mirror = ['-v', '/%s/test:/%s/test' % (pwd, pwd)]

        # Check base call for help menu
        out = subprocess.check_output(base + tool)
        self.assertTrue('Please see the complete documentation' in out)

        # run full command on sample inputs and check for existence of output file
        subprocess.check_call(base + sock + mirror + tool + args)
        self.assertTrue(os.path.exists(outfile))


if __name__ == '__main__':
    unittest.main()
