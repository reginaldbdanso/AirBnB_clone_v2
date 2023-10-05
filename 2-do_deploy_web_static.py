#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers,
using the function do_deploy
"""
from fabric.api import *
import os.path

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<username>'
env.key_filename = '<path to SSH key>'


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    # Check if archive_path is valid
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory of web server
        put(archive_path, "/tmp/")

        # Get filename without extension
        filename = os.path.basename(archive_path)
        name = os.path.splitext(filename)[0]

        # Create directory for new version of code
        run(f"mkdir -p /data/web_static/releases/{name}/")

        # Uncompress archive to new directory
        run(f"tar -xzf /tmp/{filename} -C /data/web_static/releases/{name}/")

        # Delete archive from web server
        run(f"rm /tmp/{filename}")

        # Move contents of web_static to parent directory
        run("mv /data/web_static/releases/"
            + f"{name}/web_static/* /data/web_static/releases/{name}/")

        # Remove empty web_static directory
        run(f"rm -rf /data/web_static/releases/{name}/web_static")

        # Delete symbolic link
        run("rm -rf /data/web_static/current")

        # Create new symbolic link
        run("ln -s /data/web_static/releases/"
            + f"{name}/ /data/web_static/current")

        print("New version deployed!")
        return True

    except Exception as e:
        return False
