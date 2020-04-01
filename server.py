"""
Simple ARK: Survival Evolved CLuster Status Page
"""

import os
import re
import string
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from docker.client import APIClient

# Docker settings
# BASE_URL = os.getenv("DOCKER_URL", "unix:///var/run/docker.sock")
BASE_URL = "tcp://home.sgtcanadian.com:27777"
CFILTER = os.getenv("CFILTER", "^Ark-.*$")

# Web settings
THEME = os.getenv("THEME", "darkly")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8888"))

flask = Flask(__name__)
Bootstrap(flask)

docker_client = APIClient(base_url=BASE_URL)
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

status_text = """
Server Name: {server_name}<br />
Server Status: {server_status}<br />
Players: {players} ({active_players} Active)<br />
<br />
ARK Servers: <a href="{arkservers_link}">{arkservers_link}</a><br />
Steam Connect: <a href="{steam_connect_link}">{steam_connect_link}</a>
""".lstrip().rstrip()


def parse_stdio(stdio):
    stdio = stdio.decode()
    stdio = stdio.replace('Running command \'status\' for instance \'main\'\n', '')
    stdio = ansi_escape.sub('', stdio)
    stdio = ''.join(filter(lambda x: x in set(string.printable), stdio))
    stdio = [x.split(':', 1) for x in stdio.rstrip().split('\n')]
    stdio = {x[0].lstrip().rstrip().replace(' ', '_').lower(): x[1].lstrip().rstrip() for x in stdio}
    return stdio


@flask.route("/")
def index():
    """
    Creates status page.

    :return:
    """
    containers = []
    for container in [x for x in docker_client.containers(all=True) if re.match(CFILTER, x['Names'][0].lstrip("/"))]:
        if str(container['Status']).startswith("Up"):
            try:
                cmd = docker_client.exec_start(docker_client.exec_create(container['Id'], "arkmanager status")['Id'])
                cmd = parse_stdio(cmd)
            except:
                cmd = {}

            server_status = ""
            if cmd.get('server_running') == 'Yes':
                server_status += "Running "
            if cmd.get('server_listening') == 'Yes':
                server_status += "Listening "
            if cmd.get('server_online') == 'Yes':
                server_status += "Online"
            server_status = server_status.rstrip().lstrip()
            server_status = dict(
                server_name=cmd.get("server_name"),
                active_players=cmd.get("active_players"),
                players=cmd.get("players"),
                arkservers_link=cmd.get("arkservers_link"),
                steam_connect_link=cmd.get("steam_connect_link"),
                server_status=server_status
            )

            if cmd.get('server_running') == 'Yes' and cmd.get('server_listening') == 'Yes':
                color = ""
            elif cmd.get('server_running') == 'Yes' and cmd.get('server_listening') == 'No':
                color = "warning"
            else:
                color = "danger"

            containers.append({
                "Id": container['Id'],
                "Name": container['Names'][0],
                "Status": container['Status'],
                "Command": status_text.format(**server_status) if server_status.get(
                    "server_name") is not None else "Please Wait...",
                "Color": color
            })
        else:
            containers.append({
                "Id": container['Id'],
                "Name": container['Names'][0],
                "Status": container['Status'],
                "Command": "Container Offline",
                "Color": "danger"
            })
    return render_template("index.html", containers=containers, theme=THEME)


flask.run(HOST, PORT)
