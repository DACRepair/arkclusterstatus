"""
Simple ARK: Survival Evolved CLuster Status Page
"""

import os
import re
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from docker.client import APIClient

# Docker settings
BASE_URL = os.getenv("DOCKER_URL", "unix:///var/run/docker.sock")
CFILTER = os.getenv("CFILTER", "^.*$")
ARKCMD = os.getenv("ARKCMD", "echo $HOSTNAME")

# Web settings
THEME = os.getenv("THEME", "darkly")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8888"))

APP = Flask(__name__)
Bootstrap(APP)

DOCKER = APIClient(base_url=BASE_URL)


def format_output(stdout: str):
    """
    Formats cmd output to html compatable text

    :param stdout:
    :return:
    """
    stdout = stdout.split('\n')
    stdout = [x.lstrip(' ') for x in stdout]
    stdout = "<br />\n".join(stdout)
    return stdout


@APP.route("/")
def index():
    """
    Creates status page.

    :return:
    """
    containers = []
    for container in [x for x in DOCKER.containers(all=True) if re.match(CFILTER, x['Names'][0])]:
        if str(container['Status']).startswith("Up"):
            cmd = DOCKER.exec_create(container['Id'], ARKCMD)
            containers.append({
                "Id": container['Id'],
                "Name": container['Names'][0],
                "Status": container['Status'],
                "Command": format_output(DOCKER.exec_start(cmd['Id']).decode("utf-8")),
                "Color": ""
            })
        else:
            containers.append({
                "Id": container['Id'],
                "Name": container['Names'][0],
                "Status": container['Status'],
                "Command": "",
                "Color": "danger"
            })
    return render_template("index.html", containers=containers, theme=THEME)


APP.run(HOST, PORT)
