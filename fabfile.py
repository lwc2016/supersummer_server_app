#encoding=utf-8
from fabric.api import *

env.host = ["47.97.202.200"]
env.user = "root"

def hello():
    print("hello world")

def deployTest():
    with cd("/home/test/supersummer_server_app"):
        run("git pull origin test")
        sudo("supervisorctl restart test_server")
        sudo("supervisorctl status")