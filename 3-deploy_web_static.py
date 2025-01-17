#!/usr/bin/python3
"""Script that creates and distributes and archive to web_servers."""
from fabric.api import *
import os
from datetime import datetime


env.hosts = ['54.175.147.63', '54.165.58.17']
env.user = "ubuntu"


def do_pack():
    """Creates a compressed archive"""
    if not os.path.exists("versions"):
        local('mkdir versions')

    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour,
            now.minute, now.second)

    print("Packing web_static to versions/{}".format(archive_name))
    command = "tar -cvzf versions/{} web_static".format(archive_name)
    result = local(command)

    file_size = os.path.getsize("versions/{}".format(archive_name))
    print("web_static packed: versions/{} -> {}Bytes".format(
        archive_name, file_size))

    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None


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

        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """
    Interface for set-up functions
    """
    archive_path = do_pack()

    if archive_path is None:
        return False

    result = do_deploy(archive_path)

    return result
