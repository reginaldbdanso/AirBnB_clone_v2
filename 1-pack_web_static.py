#!/usr/bin/python3
"""Generates a .tgz archive from the contents of the web_static folder
of your AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """packs web_static files into .tgz file"""
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        now = datetime.now()
        file_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        local("tar -cvzf versions/{} web_static".format(file_name))
        return "versions/{}".format(file_name)
    except Exception as e:
        return None
