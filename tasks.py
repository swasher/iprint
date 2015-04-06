# coding: utf-8

from invoke import task, env, run


@task
def test():
    print(pwd.getpwuid(os.getuid())[0])


@task
def dbbrowser():
    run("sqlite_browser -H 192.168.0.208 -p 8089 db.sqlite3 ")
