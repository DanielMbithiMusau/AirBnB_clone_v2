#!/usr/bin/python3
"""Function that compresses the web_static folder. """
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")

        now = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
                now.year, now.month, now.day, now.hour, now.minute, now.second)

        command = f"tar -cvzf versions/{archive_name} web_static"
        local(command)

        return f"versions/{archive_name}"

    except:
        return None
