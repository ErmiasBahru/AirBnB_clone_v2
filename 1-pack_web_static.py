#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder
"""

from fabric.api import local
from datetime import datetime
from os.path import isdir


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
