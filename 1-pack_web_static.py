#!/usr/bin/python3
"""Generates a .tgz archive from the contents of the web_static folder
of your AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists("versions"):
            local("mkdir -p versions")

        # Create the file name
        now = datetime.now()
        file_name = f"web_static_{now.year}{now.month}{now.day}{now.hour}"
        + f"{now.minute}{now.second}.tgz"

        # Create the archive
        local(f"tar -cvzf versions/{file_name} -C web_static")

        # Return the path to the archive
        return f"versions/{file_name}"
    except Exception as e:
        return None
