#!/usr/bin/env python2.7
# John Vivan - jtvivian@gmail.com
import os
import subprocess
import unittest


class TestCheckBiase(unittest.TestCase):

    def test_docker_call(self):
        cwd = os.getcwd()
        with open(os.path.join(cwd, 'boto'), 'w') as f:
            f.write('[Credentials]')
        out, err = check_docker_output(tool='quay.io/ucsc_cgl/s3-multipart-download', cwd=cwd)
        self.assertTrue('usage: s3-mp-download' in err)
        os.remove(os.path.join(cwd, 'boto'))

def check_docker_output(tool, cwd):
    command = 'docker run -v {}:/data '.format(cwd).split() + [tool]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.communicate()
    return output

if __name__ == '__main__':
    unittest.main()
