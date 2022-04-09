import json
import os
from dotenv import load_dotenv
from collections import defaultdict

from utils import PROJECT_PATH

# Load environment variables from project/.env file for test purpose
dotenv_file = PROJECT_PATH.joinpath(".env")
if os.path.exists(dotenv_file):
    load_dotenv(dotenv_file, override=False)


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()
        # self.env = self.get_env()
        self.env = "test"
        self._data = defaultdict(dict)
        self.load_config_file()

    def __str__(self):
        return json.dumps(self._data, indent=4, sort_keys=True)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, item):
        if item in self._data:
            return True
        return False

    def get_env(self):
        """Get environment variable"""

        if not (env := os.getenv("ENV")):
            raise EnvironmentError("Not found environment variable: ENV")
        return env

    def load_config_file(self):
        """Get environment config from file"""

        config_file_name = os.path.join(PROJECT_PATH, "config", "envs", f"{self.env}.json")
        with open(config_file_name, "r") as f:
            env_config = f.read()
        file_config = json.loads(env_config)
        self._data.update(file_config)
