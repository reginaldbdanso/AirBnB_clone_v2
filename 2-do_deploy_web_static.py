#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers,
using the function do_deploy
"""
from fabric.api import env, put, run
import os

env.hosts = ['34.232.68.72', '52.90.13.69']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension>
        # on the web server

        # get the archive file name
        file_name = archive_path.split("/")[-1]
        # get the folder name without the extension
        folder_name = file_name.split(".")[0]
        run("mkdir -p /data/web_static/releases/{}/".format(folder_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            file_name, folder_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))
        # move all the files to parent folder
        old = "/data/web_static/releases/{}/web_static/*".format(folder_name)
        new = "/data/web_static/releases/{}/".format(folder_name)
        run(f'mv {old} {new}')

        # run(
        #     "mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/"
        #     .format(folder_name, folder_name))
        # Delete empty folder after moving content
        run("rm -rf /data/web_static/releases/{}/web_static".format(
            folder_name))

        # Delete symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new the symbolic link /data/web_static/current on
        # the web server, linked to the new version of your code
        # (/data/web_static/releases/<archive filename without extension>)
        run(
            "ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(folder_name))

        return True

    except Exception as e:
        return False
