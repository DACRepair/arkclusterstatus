import multiprocessing
import re
import string

from ArkClusterStatus.Common import Config, Docker


class ArkCluster:
    _ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    command = Config.get('ark', 'command', default='arkmanager status')

    def _parse_stdio(self, stdio):
        stdio = stdio.decode()
        stdio = stdio.replace('Running command \'status\' for instance \'main\'\n', '')
        stdio = self._ansi_escape.sub('', stdio)
        stdio = ''.join(filter(lambda x: x in set(string.printable), stdio))
        stdio = [x.split(':', 1) for x in stdio.rstrip().split('\n')]
        stdio = {x[0].lstrip().rstrip().replace(' ', '_').lower(): x[1].lstrip().rstrip() for x in stdio}
        return stdio

    def _arkmanager_status(self, exec_id, retr):
        retr[exec_id] = self._parse_stdio(self._docker.run_exec(exec_id))

    @staticmethod
    def _get_dict_key(d: dict, v):
        key = None
        for k, val in d.items():
            if v == val:
                key = k
        return key

    def __init__(self):
        self._docker = Docker

    def get_servers(self):
        return self._docker.get_containers(Config.get('ark', 'filter'))

    def get_status(self):
        mapping = {}
        for container in self.get_servers():
            if container.state == 'running':
                mapping[container.cid] = self._docker.get_exec(container.cid, self.command)[0]

        manager = multiprocessing.Manager()
        retr = manager.dict()

        jobs = []
        for exe_id in mapping.values():
            proc = multiprocessing.Process(target=self._arkmanager_status, args=(exe_id, retr))
            jobs.append(proc)
            proc.start()

        for job in jobs:
            job.join()

        status = []
        while any(status):
            status = []
            for proc in jobs:
                status.append(proc.is_alive())

        for key, value in retr.items():
            mapping[self._get_dict_key(mapping, key)] = value

        return mapping
