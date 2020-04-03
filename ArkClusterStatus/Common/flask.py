import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_caching import Cache


class AppFlask(Flask):
    def __init__(self, *args, **kwargs):
        super(AppFlask, self).__init__(*args, **kwargs)
        self.template_folder = os.path.normpath(os.getcwd() + "/templates")

        Bootstrap(self)

        self.config["CACHE_TYPE"] = "simple"
        self.config["CACHE_DEFAULT_TIMEOUT"] = 300
        self.cache = Cache(self)

    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        host = host if host is not None else self.config.get('HOST')
        host = host if host is not None else '0.0.0.0'

        port = port if port is not None else self.config.get('PORT')
        port = port if port is not None else 8888
        return super(AppFlask, self).run(host, port, debug, load_dotenv, **options)
