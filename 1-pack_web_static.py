#!/usr/bin/python3
"""Script that compresses a folder."""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Creates a compressed archive."""
    if not os.path.exists("versions"):
        local('mkdir versions')

    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour,
            now.minute, now.second)

    print(f"Packing web_static to versions/{archive_name}")
    command = f"tar -cvzf versions/{archive_name} web_static"
    result = local(command)

    file_size = os.path.getsize(f"versions/{archive_name}")
    print(f"web_static packed: versions/{archive_name} -> {file_size}Bytes")

    if result.succeeded:
        return f"versions/{archive_name}"
    else:
        return None
