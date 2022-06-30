import json
import os
from dotenv import load_dotenv

from utils import PROJECT_PATH

dotenv_file = PROJECT_PATH.parent.joinpath(".env")
if os.path.exists(dotenv_file):
    load_dotenv(dotenv_file, override=False)


class AppConfig(dict):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(AppConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self._load_settings()

    def __str__(self):
        return json.dumps(self, indent=4, sort_keys=True)

    def _load_settings(self):
        """Get settings from file"""

        if not (env := os.getenv("ENV")):
            raise EnvironmentError("ENV environment variable is not set")

        config_file_name = os.path.join(PROJECT_PATH, "config", "envs", f"{env}.json")
        with open(config_file_name, "r") as f:
            env_config = f.read()
        self.update(json.loads(env_config))


app_config = AppConfig()
