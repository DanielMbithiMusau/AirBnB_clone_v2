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

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
