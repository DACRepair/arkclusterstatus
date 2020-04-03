import re
from docker.client import APIClient


class Container(object):
    def __init__(self, data):
        self.cid = data.get('Id')
        self.name = data.get('Names')
        if self.name is not None:
            self.name = str(self.name[0]).lstrip("/")
        self.state = data.get('State')
        self.status = data.get('Status')

    def __str__(self):
        return "Container: {}({}) - {}".format(self.cid[0:6], self.name, self.status)

    def __repr__(self):
        return self.__str__()


class Docker:

    def __init__(self, api_url: str = "unix:///var/run/docker.sock"):
        self._client = APIClient(base_url=api_url)

    def get_containers(self, filter: str = '^.*$'):
        containers = [Container(x) for x in self._client.containers(all=True)]
        return [x for x in containers if re.match(filter, x.name)]

    def get_exec(self, container: [str, list], command: str = None):
        if command is None:
            command = 'echo "hello"'

        exe_ids = []
        if isinstance(container, list):
            for item in container:
                exe_ids.append(self._client.exec_create(item, command)['Id'])
        else:
            exe_ids.append(self._client.exec_create(container, command)['Id'])
        return exe_ids

    def run_exec(self, exe_id: str):
        return self._client.exec_start(exe_id)
