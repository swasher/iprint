# coding: utf-8
import os
import pwd
#from fabric.api import env, local, run, put
from invoke import task, env, run
import datetime


## settings
#----------------------------------------
# by default, name of github repo matches current directory name
# and owner of repo matches current user
git_repo = os.getcwd().split(os.sep)[-1]
git_user = pwd.getpwuid(os.getuid())[0]

# remote backup server credentials

from iprint.secret_settings import hosts, path, user, key_filename, port

env.hosts = hosts
env.path = path
env.user = user
env.key_filename = key_filename
env.port = port

@task
def test():
    print(pwd.getpwuid(os.getuid())[0])


@task
def dbbrowser():
    run("sqlite_browser -H 192.168.0.208 -p 8089 db.sqlite3 ")
