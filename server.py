"""
Simple ARK: Survival Evolved CLuster Status Page
"""

from ArkClusterStatus.webserver import Flask
from ArkClusterStatus.arkcluster import ArkCluster
from flask import render_template

ark_cluster = ArkCluster()


@Flask.route('/')
@Flask.cache.cached(timeout=Flask.config['PANEL_CACHE'])
def index():
    servers = ark_cluster.get_servers()
    statuses = ark_cluster.get_status()

    items = []
    for server in servers:
        status = statuses.get(server.cid)
        if status is not None:
            if status.get('server_running') == 'Yes' and status.get('server_listening') == 'Yes':
                color = ""
            elif status.get('server_running') == 'Yes' and status.get('server_listening') == 'No':
                color = "warning"
            else:
                color = "danger"

            server_status = ""
            if status.get('server_running') == 'Yes':
                server_status += "Running "
            if status.get('server_listening') == 'Yes':
                server_status += "Listening "
            if status.get('server_online') == 'Yes':
                server_status += "Online"
            status['server_status'] = server_status
        else:
            color = 'danger'

        items.append({
            'Name': server.name,
            'Status': server.status,
            'ArkManager': status,
            'Color': color
        })
    return render_template('index.html', containers=items)


if __name__ == "__main__":
    Flask.run()
