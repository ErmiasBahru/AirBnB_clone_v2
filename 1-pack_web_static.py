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
    archive = f"versions/web_static_{string_date}.tgz"

    try:
        if not isdir('versions'):
            local("mkdir versions")
        local(f"tar -cvzf {archive} web_static")
        return archive
    except:
        return None
