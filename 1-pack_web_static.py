#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from web_static"""
import os
from datetime import datetime
from fabric.api import local, settings


def do_pack():
    """Pack web_static into versions/web_static_<timestamp>.tgz"""
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(stamp)
    with settings(warn_only=True):
        if local("mkdir -p versions").failed:
            return None
        print("Packing web_static to {}".format(path))
        if local("tar -cvzf {} web_static".format(path)).failed:
            return None
    print("web_static packed: {} -> {}Bytes".format(
        path, os.path.getsize(path)))
    return path