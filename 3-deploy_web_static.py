#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder and deploys an archive to your web
servers
"""
from fabric.api import local, run, put, env
from datetime import datetime
from os.path import isdir, isfile, basename

env.hosts = ['3.227.3.77', '3.235.226.255']


def do_pack():
    """ Creates a .tgz archive from web_static folder"""
    string_date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive = f"versions/web_static_{string_date}.tgz"

    try:
        if not isdir('versions'):
            local("mkdir versions")
        local(f"tar -cvzf {archive} web_static")
        return archive
    except:
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if not isfile(archive_path):
        return False
    filename = basename(archive_path)

    try:
        no_ext = filename.split(".")[0]
        put(archive_path, "/tmp/")
        extract_path = f"/data/web_static/releases/{no_ext}"
        run(f"mkdir -p {extract_path}")
        run(f"tar xzf /tmp/{filename} -C {extract_path}")
        run(f"rm /tmp/{filename}")
        run("mv {0}/web_static/* {0}/".format(extract_path))
        run("rm -rf {0}/web_static/".format(extract_path))
        run("rm -rf /data/web_static/current")
        run(f"ln -s {extract_path} /data/web_static/current")
        return True
    except:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    return False if archive_path is None else do_deploy(archive_path)
