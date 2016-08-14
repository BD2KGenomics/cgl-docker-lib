import argparse
import os
import textwrap

import subprocess

# Using Docker versions from: https://github.com/docker/docker/blob/master/CHANGELOG.md
docker_versions = ['1.7.0',
                   '1.7.1',
                   '1.8.0',
                   '1.8.1',
                   '1.9.0',
                   '1.9.1',
                   '1.10.0',
                   '1.10.1',
                   '1.10.3']

def build(name, tag, version):
    """
    Builds a container given a name, tag, and version of Docker

    :param str name: Name of the image
    :param str tag: Docker tag, consisting of git commit hashes
    :param str version: Docker version
    """
    dirname, filename = os.path.split(os.path.abspath(__file__))
    version_tag = version + '--' + tag
    # Write out Dockerfile
    with open(os.path.join(dirname, 'Dockerfile'), 'w') as f:
        f.write(print_dockerfile(version))
    # Build
    subprocess.check_call(['docker', 'build',
                           '-t', '{}:{}'.format(name, version_tag),
                           dirname])
    # Tag
    subprocess.check_call(['docker', 'tag',
                           '-f', '{}:{}'.format(name, version_tag),
                           '{}:latest'.format(name)])
    os.remove(os.path.join(dirname, 'Dockerfile'))


def push(name, tag, version, latest=False):
    """
    Pushes Docker to our hosting service

    :param str name: Name of the image
    :param str tag: Docker tag, consisting of git commit hashes
    :param str version: Docker version
    :param bool latest: if True, pushes "latest" tag in addition to standard tag
    """
    command = ['docker', 'push', '{}:{}'.format(name, version + '--' + tag)]
    subprocess.check_call(command)
    if latest:
        command[-1] = name + ':latest'
        subprocess.check_call(command)


def print_dockerfile(docker_version, ubuntu_version='14.04', toil_version='3.3.1',
                     toil_scripts_version='2.0.8'):
    return textwrap.dedent("""
    FROM ubuntu:{ubuntu_version}

    # File Author / Maintainer
    MAINTAINER John Vivian <jtvivian@gmail.com>

    RUN apt-get update && apt-get install -y \
        git \
        python-dev \
        python-pip \
        wget \
        curl \
        apt-transport-https \
        ca-certificates

    # Get the Docker binary
    RUN wget https://get.docker.com/builds/Linux/x86_64/docker-{docker_version} -O /usr/local/bin/docker
    RUN chmod u+x /usr/local/bin/docker

    # Install Toil
    RUN pip install toil=={toil_version}

    # Install toil-scripts
    RUN pip install toil-scripts=={toil_scripts_version}

    COPY wrapper.py /opt/pipeline/
    COPY pipelineWrapper.py /opt/pipeline/
    COPY README.md /opt/pipeline/

    ENTRYPOINT ["python", "/opt/pipeline/wrapper.py"]
    CMD ["--help"]
    """.format(ubuntu_version=ubuntu_version, docker_version=docker_version,
               toil_version=toil_version, toil_scripts_version=toil_scripts_version)[1:])


def main():
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('nametag', nargs=2)
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('build', help='Writes out a Dockerfile and builds it.')
    subparsers.add_parser('push', help='Pushes out Dockerfiles')
    args = parser.parse_args()

    name, tag = args.nametag

    # Build containers
    if args.command == 'build':
        for version in docker_versions:
            build(name, tag, version)
    # Push containers
    if args.command == 'push':
        for version in docker_versions:
            if version != docker_versions[-1]:
                push(name, tag, version)
            else:
                push(name, tag, version, latest=True)


if __name__ == '__main__':
    main()
