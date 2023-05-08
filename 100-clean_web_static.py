#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""
from fabric.api import *


env.hosts = ['54.175.147.63', '	54.165.58.17']
env.user = "ubuntu"


def do_clean(number=0):
    """
    Deletes all unnecessary archives in the versions folder and releases folder.

    Args:
        number (int): The number of archives to keep, including the most recent one.
    """
    number = int(number)
    if number < 1:
        number = 1

    with lcd('./versions'):
        local('ls -1t | tail -n +{} | xargs rm -f'.format(number))

    with cd('/data/web_static/releases'):
        run('ls -1t | tail -n +{} | xargs rm -rf'.format(number))

        with cd('/data/web_static/releases'):
            run('ls -1t | tail -n +{} | xargs rm -rf'.format(number))


def deploy():
    """
    Deploys the latest version of the code to the web servers.
    """
    try:
        archive_path = do_pack()
    except:
        return False

    if not archive_path:
        return False

    return do_deploy(archive_path)


def do_pack():
    """
    Creates a compressed archive of the web_static folder.

    Returns:
        str: The path to the archive file, or None if the archive was not created.
    """
    local('mkdir -p versions')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = 'web_static_{}.tgz'.format(timestamp)
    command = 'tar -cvzf versions/{} web_static'.format(file_name)
    result = local(command)

    if result.failed:
        return None

    return 'versions/{}'.format(file_name)


def do_deploy(archive_path):
    """
    Deploys the latest version of the code to the web servers.

    Args:
        archive_path (str): The path to the archive file to deploy.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = file_name.split('.')[0]
    path = '/data/web_static/releases/{}'.format(name)

    if put(archive_path, '/tmp/{}'.format(file_name)).failed:
        return False

    if run('mkdir -p {}'.format(path)).failed:
        return False

    if run('tar -xzf /tmp/{} -C {}'.format(file_name, path)).failed:
        return False

    if run('mv {}/web_static/* {}/'.format(path, path)).failed:
        return False

    if run('rm -rf {}/web_static'.format(path)).failed:
        return False

    if run('rm /tmp/{}'.format(file_name)).failed:
        return False

    if run('rm /data/web_static/current').failed:
        return False

    if run('ln -s {} /data/web_static/current'.format(path)).failed:
        return False

    return True
