import os
import yaml

def load_config():
    config = {}
    # This counts on this service being run from make
    configFilePath = "{}/config.yaml".format(os.environ.get('PWD'))
    # Load the configuration file and set the defaults for the code
    try:
        with open(configFilePath) as file:
            yamlConfig = yaml.load(file)

        for item in ['SERVER', 'CLIENT', 'TESTSERVER', 'TESTCLIENT']:
            config[item] = yamlConfig.get(item, {})

    except Exception as e:
        print(e)
        print("Warning: No 'config.yaml' present.")
        return []

    return config
