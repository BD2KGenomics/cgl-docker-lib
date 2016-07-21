#!/usr/bin/env python2.7

import os
import subprocess
import unittest


class TestADAMPipeline(unittest.TestCase):

    def test_docker_call(self):
        
        # get working directory
        pwd = os.getcwd()
        outfile = '%s/test/outdir/small.processed.bam' % pwd

        # check for output file in ./test and clean if necessary
        if os.path.exists(outfile):
            os.remove(outfile)

        # build commandline
        tool = ['quay.io/ucsc_cgl/adam-pipeline']
        base = ['docker', 'run']
        args = ['--sample', '/%s/test/small.sam' % pwd,
                '--known-sites', '/%s/test/small.vcf' % pwd,
                '--output', '/%s/test/outdir/small.processed.bam' % pwd,
                '--memory', '1']
        mounts = ['-v', '/%s/test/small.sam:/%s/test/small.sam' % (pwd, pwd),
                  '-v', '/%s/test/small.vcf:/%s/test/small.vcf' % (pwd, pwd),
                  '-v', '/%s/test/outdir:/%s/test/outdir' % (pwd, pwd),]

        # Check base call for help menu
        out = subprocess.check_output(base + tool)
        self.assertTrue('Please see the complete documentation' in out)

        # run full command on sample inputs and check for existence of output file
        subprocess.check_call(base + mounts + tool + args)
        self.assertTrue(os.path.exists(outfile))


if __name__ == '__main__':
    unittest.main()
