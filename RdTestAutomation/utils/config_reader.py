import configparser
import os


# This function reads the .ini file
def get_config():
    config = configparser.ConfigParser()

    # Get the absolute path to the config.ini file
    # This goes from this file (config_reader.py) -> 'utils' -> 'RdTestAutomation' -> 'resources' -> 'config.ini'
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..', 'resources', 'config.ini')

    config.read(config_path)
    return config


# This helper function replaces your 'ConfigReader.getProperty("url")'
def get_property(section, key):
    config = get_config()
    return config.get(section, key)


# --- Example of how to test this ---
# (You can run this file directly to test it)
if __name__ == "__main__":
    url = get_property('settings', 'url')
    print(f"The URL is: {url}")