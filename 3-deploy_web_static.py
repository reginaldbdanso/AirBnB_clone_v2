#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to your web servers,
using the function deploy
"""
from fabric.api import *
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<username>'
env.key_filename = '<path to SSH key>'


def do_pack():
    """Create a tar archive of the web_static directory"""
    try:
        local("mkdir -p versions")
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = f"versions/web_static_{now}.tgz"
        local(f"tar -cvzf {file_path} web_static")
        return file_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        archive_name = archive_path.split("/")[-1]
        folder_name = "/data/web_static/releases/" + archive_name.split(".")[0]
        run(f"mkdir -p {folder_name}")
        run(f"tar -xzf /tmp/{archive_name} -C {folder_name}")
        run(f"rm /tmp/{archive_name}")
        run(f"mv {folder_name}/web_static/* {folder_name}")
        run(f"rm -rf {folder_name}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {folder_name} /data/web_static/current")
        return True
    except Exception as e:
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
