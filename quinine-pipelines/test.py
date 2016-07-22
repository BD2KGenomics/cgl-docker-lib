#!/usr/bin/env python2.7

import distutils.spawn
import logging
import os
import subprocess
import unittest

_log = logging.getLogger(__name__)

def _cromwell_cmd():

    if "CROMWELL_HOME" in os.environ:
        
        # look in cromwell build artifact directory
        cromwell_target_dir = os.path.join(os.environ["CROMWELL_HOME"],
                                           "target/scala-2.11/")
        dir_contents = os.listdir(cromwell_target_dir)
        
        # do we have any jars?
        jars = []
        for f in dir_contents:
            
            # is this a possible cromwell jar?
            if f.startswith("cromwell") and f.endswith(".jar"):
                jars.append(f)
                
        # we should only have one jar
        if len(jars) == 1:
            return ['java', '-jar', os.path.join(cromwell_target_dir,
                                                 jars[0])]
        elif len(jars) > 1:
            _log.error('Found multiple jars in $CROMWELL_HOME (%s): %r',
                       os.environ["CROMWELL_HOME"],
                       jars)
            return None
            
        else:
            _log.error('Found no jars in $CROMWELL_HOME (%s).', os.environ["CROMWELL_HOME"])
            
    else:
            
        cromwell_exe = distutils.spawn.find_executable("cromwell")
        
        # need to wrap this in a list, if it is not none
        if cromwell_exe is None:
            return None
        else:
            return [cromwell_exe]


class TestQuininePipeline(unittest.TestCase):


    def test_docker_call_help(self):

        # build commandline
        tool = ['quay.io/ucsc_cgl/quinine-pipelines']
        base = ['docker', 'run']

        # Check base call for help menu
        out = subprocess.check_output(base + tool)
        self.assertTrue('usage: metrics.py [-h] {rna,targeted,contamination}' in out)


    def test_docker_call_targeted(self):

        # get working directory
        pwd = os.getcwd()

        # clean up output dir
        outfile = os.path.join(pwd, 'test/targeted.txt')
        if os.path.exists(outfile):
            os.remove(outfile)

        # build commandline
        tool = ['quay.io/ucsc_cgl/quinine-pipelines']
        base = ['docker', 'run']
        mounts = ['-v', '/%s/test:/%s/test' % (pwd, pwd)]
        cmd = ['/opt/toil-scripts/quinine-pipelines.sh',
               'targeted',
               '--reads', '%s/test/small.sam' % pwd,
               '--bait', '%s/test/small.bait.bed' % pwd,
               '--targets', '%s/test/small.targets.bed' % pwd,
               '--output', outfile]

        # Check base call for help menu
        subprocess.check_call(base + mounts + tool + [' '.join(cmd)])

        # read through file and check that each line is in the output
        of = open(outfile)
        out = ''.join(of.readlines())

        for line in open(os.path.join(pwd, 'test/targeted.output')):
            self.assertTrue(line.strip().rstrip() in out)


    @unittest.skipIf(_cromwell_cmd() is None,
                     "Path to cromwell not defined by $CROMWELL_HOME")
    def test_wdl_targeted(self):

        # get working directory
        pwd = os.getcwd()

        # clean up output dir
        outfile = os.path.join(pwd, 'test/targeted.txt')
        if os.path.exists(outfile):
            os.remove(outfile)


        # set up cromwell args
        cmd = _cromwell_cmd() + ["run",
                                  "%s/targeted.wdl" % pwd,
                                  "%s/targeted.workflow.json" % pwd]

        # run cromwell
        out = subprocess.check_output(cmd)
        self.assertTrue('wf.targeted.response' in out)


    def test_docker_call_rna(self):

        # get working directory
        pwd = os.getcwd()

        # clean up output dir
        outfile = os.path.join(pwd, 'test/rna.txt')
        if os.path.exists(outfile):
            os.remove(outfile)

        # build commandline
        tool = ['quay.io/ucsc_cgl/quinine-pipelines']
        base = ['docker', 'run']
        mounts = ['-v', '/%s/test:/%s/test' % (pwd, pwd)]
        cmd = ['/opt/toil-scripts/quinine-pipelines.sh',
               'rna',
               '--reads', '%s/test/small.sam' % pwd,
               '--transcriptome', '%s/test/small.transcripts.gtf' % pwd,
               '--output', outfile]

        # Check base call for help menu
        subprocess.check_call(base + mounts + tool + [' '.join(cmd)])

        # read through file and check that each line is in the output
        of = open(outfile)
        out = ''.join(of.readlines())

        for line in open(os.path.join(pwd, 'test/rna.output')):
            self.assertTrue(line.strip().rstrip() in out)


    @unittest.skipIf(_cromwell_cmd() is None,
                     "Path to cromwell not defined by $CROMWELL_HOME")
    def test_wdl_rna(self):

        # get working directory
        pwd = os.getcwd()

        # clean up output dir
        outfile = os.path.join(pwd, 'test/rna.txt')
        if os.path.exists(outfile):
            os.remove(outfile)


        # set up cromwell args
        cmd = _cromwell_cmd() + ["run",
                                  "%s/rna.wdl" % pwd,
                                  "%s/rna.workflow.json" % pwd]

        # run cromwell
        out = subprocess.check_output(cmd)
        self.assertTrue('wf.rna.response' in out)


    def test_docker_call_contamination(self):

        # get working directory
        pwd = os.getcwd()

        # clean up output dir
        outfile = os.path.join(pwd, 'test/contamination.txt')
        if os.path.exists(outfile):
            os.remove(outfile)

        # build commandline
        tool = ['quay.io/ucsc_cgl/quinine-pipelines']
        base = ['docker', 'run']
        mounts = ['-v', '/%s/test:/%s/test' % (pwd, pwd)]
        cmd = ['/opt/toil-scripts/quinine-pipelines.sh',
               'contamination',
               '--reads', '%s/test/contaminated.sam' % pwd,
               '--sample-vcf', '%s/test/call.vcf' % pwd,
               '--population', '%s/test/population.vcf' % pwd,
               '--output', outfile]

        # Check base call for help menu
        subprocess.check_call(base + mounts + tool + [' '.join(cmd)])

        # read through file and check that each line is in the output
        of = open(outfile)
        out = ''.join(of.readlines())

        for line in open(os.path.join(pwd, 'test/contamination.output')):
            self.assertTrue(line.strip().rstrip() in out)


    @unittest.skipIf(_cromwell_cmd() is None,
                     "Path to cromwell not defined by $CROMWELL_HOME")
    def test_wdl_contamination(self):

        # get working directory
        pwd = os.getcwd()

        # clean up output dir
        outfile = os.path.join(pwd, 'test/contamination.txt')
        if os.path.exists(outfile):
            os.remove(outfile)


        # set up cromwell args
        cmd = _cromwell_cmd() + ["run",
                                  "%s/contamination.wdl" % pwd,
                                  "%s/contamination.workflow.json" % pwd]

        # run cromwell
        out = subprocess.check_output(cmd)
        self.assertTrue('wf.contamination.response' in out)


if __name__ == '__main__':
    unittest.main()
