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
    archive = "versions/web_static_{}.tgz".format(string_date)

    try:
        if not isdir('versions'):
            local("mkdir versions")
        local("tar -cvzf {} web_static".format(archive))
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
        extract_path = "/data/web_static/releases/{}".format(no_ext)
        run("mkdir -p {}".format(extract_path))
        run("tar xzf /tmp/{} -C {}".format(filename, extract_path))
        run("rm /tmp/{}".format(filename))
        run("mv {0}/web_static/* {0}/".format(extract_path))
        run("rm -rf {0}/web_static/".format(extract_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(extract_path))
        return True
    except:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    has_deployed = do_deploy(archive_path)
    return has_deployed
