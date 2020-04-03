from ArkClusterStatus.Common import Config, Flask

Flask.config['HOST'] = Config.get('web', 'host', '0.0.0.0')
Flask.config['PORT'] = Config.get('web', 'port', '8888', int)
Flask.config['PANEL_CACHE'] = Config.get('web', 'cache', '30', int)
Flask.config['DEBUG'] = Config.get('web', 'debug', "false").lower() == 'true'


@Flask.context_processor
def inject_theme():
    theme = Config.get('web', 'theme', 'darkly')
    if not theme.startswith('http'):
        theme = "https://bootswatch.com/3/{}/bootstrap.min.css".format(theme)
    return dict(theme=theme)
