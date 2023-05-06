#!/usr/bin/python3
"""Function that compresses the web_static folder. """
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    try:
        if not os.path.exists("versions"):
            local('mkdir versions')

        now = datetime.now()
        f = "%Y%m%d%H%M%S"
        archive_name = "web_static_{}.tgz".format(now.strftime(f))

        command = f"tar -cvzf versions/{archive_name} web_static"
        local(command)

        return f"versions/{archive_name}"

    except:
        return None
