#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to your web servers,
using the function deploy
"""
from fabric.api import *
from os.path import exists
from datetime import datetime
import os

env.hosts = ['34.232.68.72', '52.90.13.69']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


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
        print(e)
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not os.path.exists(archive_path):
        print("File doesn't exist")
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
        run("mv {} {}".format(old, new))

        # run(
        #     "mv /data/web_static/releases/{}/web_static/*
        # /data/web_static/releases/{}/"
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
        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if not archive_path:
        print("Archive not created")
        return False
    print("Deploying new version...")
    return do_deploy(archive_path)
