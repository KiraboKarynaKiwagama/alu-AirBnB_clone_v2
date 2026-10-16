#!/usr/bin/python3
"""Fabric script that creates and distributes an archive"""
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once, settings

env.hosts = ['174.129.179.91', '54.159.207.54']
env.user = 'ubuntu'


@runs_once
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


def do_deploy(archive_path):
    """Deploy archive_path to the web servers, True on success"""
    if not os.path.isfile(archive_path):
        return False
    fname = os.path.basename(archive_path)
    name = fname.split('.')[0]
    rel = "/data/web_static/releases/{}/".format(name)
    cmds = [
        "mkdir -p {}".format(rel),
        "tar -xzf /tmp/{} -C {}".format(fname, rel),
        "rm /tmp/{}".format(fname),
        "mv {0}web_static/* {0}".format(rel),
        "rm -rf {}web_static".format(rel),
        "rm -rf /data/web_static/current",
        "ln -s {} /data/web_static/current".format(rel),
    ]
    with settings(warn_only=True):
        if put(archive_path, "/tmp/{}".format(fname)).failed:
            return False
        for cmd in cmds:
            if run(cmd).failed:
                return False
    print("New version deployed!")
    return True


def deploy():
    """Create and distribute an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)