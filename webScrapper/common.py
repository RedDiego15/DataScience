import yaml

__config = None  #nos va a servir para cachear nuestra config, para no leer a disco a cada rato

def config():
    global __config
    if not __config:
        with open('config.yaml',mode = 'r') as f:
            __config = yaml.safe_load(f)
    return __config


