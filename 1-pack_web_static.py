#!/usr/bin/python3
"""Script that compresses a folder."""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Creates a compressed archive of the web_static folder.


    Returns:
        If the archive was created succesfully, returns the path to
        the archive. Otherwise, returns None.
    """
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
