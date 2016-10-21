#!/usr/bin/env python2.7
# John Vivian
# 10-14-15
"""
Builds tools whose most recent commit does not exist on our quay.io account.
Runs unittests and pushes image to quay.io.

Dependencies
    Docker (>1.0)
    python2.7

Requires
    ~/.dockercfg (with privileges to quay.io/ucsc_cgl/)
    ~/.cgl-docker-lib (containing the quay.io access token need to authenticate POST requests)
"""

import json
import logging
import os
import subprocess
import requests

# get a log with the most basic config
_log = logging.getLogger(__name__)
logging.basicConfig()

# log all the things
_log.setLevel(9)

def get_updated_tools(repos):
    """
    Compare latest git commit hash of a tool to the existing tag on quay.io.
    """
    updated_tools = set()
    generate_cmd = ['make', 'generate']
    dryrun_cmd = ['make', '-n', 'push']
    for tool in repos:
        
        if not os.path.isdir(os.path.abspath(tool)):
            _log.warn('Tool %s does not exist in cgl-docker-lib. Skipping...', tool)
            continue

        # Load API request for image
        response = requests.get('https://quay.io/api/v1/repository/ucsc_cgl/{}/image/'.format(tool))
        json_data = json.loads(response.text)
        if response.status_code != 200:
            _log.error('Quay.io API Request to view repository: %s, has failed', tool)

        # Fetch quay.io tags and parse for commit hash
        tags = sum([x['tags'] for x in json_data['images'] if x['tags']], [])
        _log.log(5, 'Tool %s has %d tags on quay.io:\n%r', tool, len(tags), tags) # lower level than debug

        # some tools rely on a "make generate" target
        # due to the vaguarities of make, we need to call this before doing the push dry run
        #
        # the tl;dr is that tools that rely on the "make generate" target are running recursive make,
        # and if "make generate" is not run before "make -n push", when "make push" tries to cd into
        # the lower directories to recursively call make, those lower directories won't exist, and
        # make will fail
        try:
            subprocess.check_output(generate_cmd,
                                    cwd=os.path.abspath(tool),
                                    stderr=subprocess.STDOUT)

        except subprocess.CalledProcessError as cpe:

            # we need to inspect the error message here.
            #
            # if the error message from make is that there's no generate target,
            # then we're fine and can ignore the error.
            #
            # if the error is that "make generate" failed, then that's a whole
            # different can of worms
            if 'No rule to make target' in cpe.output:
                
                _log.log(5, 'No generate target for tool %s.', tool)
                pass

            else:

                _log.error('Calling %r on tool %s failed with error code %d! Output:', 
                           generate_cmd, tool, cpe.returncode)
                output_lines = cpe.output.split('\n')
                
                for line in output_lines:
                    _log.debug('%s/%r: %s', tool, generate_cmd, line)
                    
                _log.error('Skipping...')
                continue
                    
        # identify tools that will be built from make push dry run
        try:
            output = subprocess.check_output(dryrun_cmd,
                                             cwd=os.path.abspath(tool),
                                             stderr=subprocess.STDOUT)

        except subprocess.CalledProcessError as cpe:
            _log.error('Calling %r on tool %s failed with error code %d! Output:', 
                       dryrun_cmd, tool, cpe.returncode)
            output_lines = cpe.output.split('\n')

            for line in output_lines:
                _log.debug('%s/%r: %s', tool, dryrun_cmd, line)

            _log.error('Skipping...')

            # set a null output and we'll fall through this loop iteration
            output = None

        if output:
            lines = output.split('\n')
            pushed_tags = []
            added = False
            
            for line in lines:
                # make push may:
                # - rebuild the tool
                # - push a "latest" tag
                #
                # we're interested in the explicit version tag
                if 'push' in line and not 'latest' in line:

                    # we expect the push command to be "docker push toolname:tag", thus we're interested in the 3rd word
                    push_cmd = line.split()
                    if len(push_cmd) != 3:
                        _log.error('Saw badly formatted push command for %s (%r)', tool, push_cmd)

                    # split the toolname/tag on the semicolon to get the tag
                    push_tool_and_tag = push_cmd[2]
                    push_tool, version = push_tool_and_tag.split(':', 1)
                    quay_tool = "quay.io/ucsc_cgl/%s" % tool
                    if push_tool != quay_tool:
                        _log.error('Tool name in push command (%s) did not match expected (%s).', push_tool, quay_tool)
                    pushed_tags.append(version)
                    
                    if version not in tags:
                        updated_tools.add(tool)
                        added = True

            if len(pushed_tags) > 1:
                _log.warn('Saw multiple tags for %s: %r', tool, pushed_tags)
            elif len(pushed_tags) == 0:
                _log.warn('Saw no tags to push for %s.', tool)

            if added:
                _log.info('Added %s to list of updated tools.', tool)
            else:
                _log.info('Did not add %s to list of updated tools.', tool)

        else:
            _log.warn('Skipping tool %s, as it does not exist in cgl-docker-lib.', tool)

    return updated_tools


def get_repos():
    """
    Return list of existing repositories on quay.io
    """
    response = requests.get('https://quay.io/api/v1/repository?public=true&namespace=ucsc_cgl')
    repo_data = json.loads(response.text)
    if response.status_code != 200:
        raise RuntimeError('Quay.io API request to view repositories failed with code %d.' % response.statusCode)
    repos = {str(x[u'name']) for x in repo_data['repositories']}
    return repos


# TODO: This is garbage. Fix this try/catch
def run_make(tools_to_build, cmd, err):
    """
    For each tool, run a (make) command with an error message if it fails
    """
    for tool in tools_to_build:
        _log.info('Running "%s" for tool %s.', cmd, tool)
        try:
            subprocess.check_output(cmd,
                                    cwd=os.path.abspath(tool),
                                    stderr=subprocess.STDOUT)
            _log.info('Running "%s" for tool %s succeeded!', cmd, tool)
        except subprocess.CalledProcessError as cpe:
            _log.error('Running "%s" for tool %s FAILED with code %d! Output:',
                       cmd, tool, cpe.returncode)
            output_lines = cpe.output.split('\n')

            for line in output_lines:
                _log.debug('%s/%s: %s', tool, cmd, line)

            if cmd == 'make':
                raise RuntimeError, err.format(tool)
            # If a test fails, an assertion will be thrown. Sometimes "make test" returns non-zero exit codes.
            pass


def make_repos_public(tools_to_build, credentials):
    """
    For each tool, submit a POST request to make the tool repository public
    using credentials loaded in ~/.cgl-docker-lib.
    """
    with open(credentials, 'r') as f:
        token = f.read().strip()
    for tool in tools_to_build:
        _log.info('Making tool: %s a publically visible repository.', tool)
        url = 'https://quay.io/api/v1/repository/ucsc_cgl/{}/changevisibility'.format(tool)
        payload = {'visibility': 'public'}
        headers = {'Authorization': 'Bearer {}'.format(token), 'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code != 200:
            _log.error('POST call to make %s public failed. Code: %d. 403 = bad token',
                       tool,
                       response.status_code)
        else:
            _log.info('Succeeded in making %s public!', tool)

def main():
    push = building_on_master()
    if push:
        _log.info('We are building the master branch, so we will push updated containers.')
    # Determine what tools to build
    tools = {x for x in os.listdir('.') if os.path.isdir(x) and not x.startswith('.')}
    repos = get_repos()
    updated_tools = get_updated_tools(repos)
    tools_to_build = (tools - repos).union(updated_tools)
    _log.info('Building %d tools out of %d: %s',
              len(tools_to_build), len(repos), '\n'.join(tools_to_build))
    # Build, test, and push tools to quay.io/ucsc_cgl/
    cmds = [["make"], ["make", "test"]]
    errs = ['Tool: {}, failed to build', 'Tool: {}, failed unittest']
    if push:
        cmds.append(["make", "push"])
        errs.append('Tool: {}, failed push to quay.io')
    for cmd, err in zip(*[cmds, errs]):
        run_make(tools_to_build, cmd, err)
    # TBD: Making repos public requires admin privileges which I'd rather not grant Jenkins
    if False:
        credentials = os.path.join(os.path.expanduser('~'), '.cgl-docker-lib')
        make_repos_public(tools_to_build, credentials=credentials)


def building_on_master():
    master_sha1 = subprocess.check_output(['git', 'rev-parse', '--verify', 'remotes/origin/master']).strip()
    head_sha1 = subprocess.check_output(['git', 'rev-parse', '--verify', 'HEAD']).strip()
    _log.info('Got sha1 of %s for remote/origin/master, sha1 of %s for local HEAD.', master_sha1, head_sha1)
    return (head_sha1 == master_sha1)


if __name__ == '__main__':
    main()
