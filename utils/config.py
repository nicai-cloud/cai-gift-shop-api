import os
from dotenv import dotenv_values


__config_file_cache = None


class ConfigKeyNotSet(Exception):
    """Raised when a configuration parameter was not found from the available
    configuration sources."""


def get(key):
    """Find the configuration value set at a particular key.

    Looks at the following sources in order:
    1. The environment variables..
    2. A .env file in the current working directory.

    Keys are in all lowercase separated by underscores, for example, database_url. When
    looking for environment variables, the key will be converted to all uppercase, DATABASE_URL.

    Returns a string with the value that was found. If the value was not found in any of the
    sources, a ConfigKeyNotSet exception will be raised.

    """

    env_value = os.getenv(key.upper())

    if env_value is not None:
        return env_value

    global __config_file_cache

    if __config_file_cache is None:
        try:
            __config_file_cache = dotenv_values(".env")
        except FileNotFoundError:
            __config_file_cache = {}

    try:
        return __config_file_cache[key]
    except KeyError:
        pass

    raise ConfigKeyNotSet("A value for the configuration key '{}' was not found.".format(key))
