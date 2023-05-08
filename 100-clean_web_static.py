#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""

from fabric.api import *

env.hosts = ['54.175.147.63', '54.165.58.17']
env.user = "ubuntu"


def do_clean(number=0):
    """
    Deletes all unnecessary archives in the versions
    folder and releases folder.

    Args:
        number (int): The number of archives to keep,
        including the most recent one.
    """
    number = int(number)

    if number < 1:
        number = 1

    with lcd('./versions'):
        local('ls -1t | tail -n +{} | xargs rm -f'.format(number))

    with cd('/data/web_static/releases'):
        run('ls -1t | tail -n +{} | xargs rm -rf'.format(number))

        with cd('/data/web_static/releases'):
            run('ls -1t | tail -n +{} | xargs rm -rf'.format(number))
