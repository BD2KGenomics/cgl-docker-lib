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
        args = ['python', '/opt/adam-pipeline/wrapper.py',
                '--sample', '/%s/test/small.sam' % pwd,
                '--known-sites', '/%s/test/small.vcf' % pwd,
                '--output', '/%s/test/small.processed.bam' % pwd,
                '--memory', '1']
        mounts = ['-v', '/%s/test:/%s/test' % (pwd, pwd)]

        # Check base call for help menu
        out = subprocess.check_output(base + tool)
        self.assertTrue('Please see the complete documentation' in out)

        # run full command on sample inputs and check for existence of output file
        out = subprocess.check_output(base + mounts + tool + [" ".join(args)])
        self.assertTrue(os.path.exists(outfile))


    @unittest.skipIf(_cromwell_cmd() is None,
                     "Path to cromwell not defined by $CROMWELL_HOME")
    def test_wdl_call(self):

        # get working directory
        pwd = os.getcwd()
        outfile = '%s/test/small.processed.bam' % pwd

        # check for output file in ./test and clean if necessary
        if os.path.exists(outfile):
            os.remove(outfile)

        # set up cromwell args
        cmd = _cromwell_cmd() + ["run",
                                  "%s/workflow.wdl" % pwd,
                                  "%s/workflow.json" % pwd]

        # run cromwell
        subprocess.check_call(cmd)
        self.assertTrue(os.path.exists(outfile))
        

if __name__ == '__main__':
    unittest.main()
