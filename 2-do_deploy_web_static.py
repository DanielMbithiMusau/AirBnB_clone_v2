#!/usr/bin/python3
"""Distributes an archive to web servers."""
from fabric.api import *
import os


env.hosts = ['54.175.147.63', '	54.165.58.17']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Deploy an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract the archive to /data/web_static/releases/
        filename = archive_path.split("/")[-1]
        directory = "/data/web_static/releases/{}".format(
                filename.split(".")[0])
        run("sudo mkdir -p {}".format(directory))
        run("sudo tar -xzf /tmp/{} -C {} --strip-components=1".format(
            filename, directory))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        run("sudo ln -s {} /data/web_static/current".format(directory))

        return True
    except:
        return False
