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
import os
import subprocess
import requests
import json


def get_updated_tools(repos):
    """
    Compare latest git commit hash of a tool to the existing tag on quay.io.
    Since tools are tagged with the motif: <version>--<commit hash>, we can determine
    what tools have been modified.
    """
    updated_tools = set()
    for tool in repos:
        # Load API request for image
        response = requests.get('https://quay.io/api/v1/repository/ucsc_cgl/{}/image/'.format(tool))
        json_data = json.loads(response.text)
        assert response.status_code == 200, 'Quay.io API Request to view repository: {}, has failed'.format(tool)
        # Fetch quay.io tags and parse for commit hash
        tags = sum([x['tags'] for x in json_data['images'] if x['tags']], [])
        tags = {str(x).split('--')[1] for x in tags if not x == 'latest'}
        # Fetch last commit hash for tool using `git log`
        p = subprocess.Popen(['git', 'log', '--pretty=oneline', '-n', '1', '--', tool], stdout=subprocess.PIPE)
        commit, comment = p.stdout.read().split(" ", 1)
        if commit not in tags:
            updated_tools.add(tool)
    return updated_tools


def get_repos():
    """
    Return list of existing repositories on quay.io
    """
    response = requests.get('https://quay.io/api/v1/repository?public=true&namespace=ucsc_cgl')
    repo_data = json.loads(response.text)
    assert response.status_code == 200, 'Quay.io API request to view repositories failed.'
    repos = {str(x[u'name']) for x in repo_data['repositories']}
    return repos


def run_make(tools_to_build, cmd, err):
    """
    For each tool, run a (make) command with an error message if it fails
    """
    for tool in tools_to_build:
        print '\nTool: {}\n'.format(tool)
        ret_code = subprocess.check_call(cmd, cwd=os.path.abspath(tool))
        assert ret_code == 0, err.format(tool)


def make_repos_public(tools_to_build, credentials):
    """
    For each tool, submit a POST request to make the tool repository public
    using credentials loaded in ~/.cgl-docker-lib.
    """
    with open(credentials, 'r') as f:
        token = f.read().strip()
    for tool in tools_to_build:
        print 'Making tool: {} a publically visible repository.'.format(tool)
        url = 'https://quay.io/api/v1/repository/ucsc_cgl/{}/changevisibility'.format(tool)
        payload = {'visibility': 'public'}
        headers = {'Authorization': 'Bearer {}'.format(token), 'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        assert response.status_code == 200, 'POST call failed. Code: {}. 403 = bad token'.format(response.status_code)


def main():
    # Determine what tools to build
    tools = {x for x in os.listdir('.') if os.path.isdir(x) and not x.startswith('.')}
    repos = get_repos()
    updated_tools = get_updated_tools(repos)
    tools_to_build = (tools - repos).union(updated_tools)
    print 'Building Tools: ' + ' '.join(tools_to_build)
    # Build, test, and push tools to quay.io/ucsc_cgl/
    cmds = [["make"], ["make", "test"], ["make", "push"]]
    errs = ['Tool: {}, failed to build', 'Tool: {}, failed unittest', 'Tool: {}, failed push to quay.io']
    for cmd, err in zip(*[cmds, errs]):
        run_make(tools_to_build, cmd, err)
    credentials = os.path.join(os.path.expanduser('~'), '.cgl-docker-lib')
    make_repos_public(tools_to_build, credentials=credentials)


if __name__ == '__main__':
    main()