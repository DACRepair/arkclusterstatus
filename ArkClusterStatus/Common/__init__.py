from .config import Config
from .docker import Docker
from .flask import AppFlask

Config = Config()
Docker = Docker(Config.get('docker', 'url', "unix:///var/run/docker.sock"))
Flask = AppFlask(__name__)




