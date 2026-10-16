#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers"""
import os
from fabric.api import env, put, run, settings

env.hosts = ['174.129.179.91', '54.159.207.54']
env.user = 'ubuntu'


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