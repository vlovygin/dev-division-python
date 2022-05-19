import json
import os
from dotenv import load_dotenv

from utils import PROJECT_PATH

# Load environment variables from project/.env file for test purpose
dotenv_file = PROJECT_PATH.joinpath(".env")
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
        self.load_config_file()

    def __str__(self):
        return json.dumps(self, indent=4, sort_keys=True)

    def load_config_file(self):
        """Get environment config from file"""

        # if not (env := os.getenv("ENV")):
        #     raise EnvironmentError("Not found environment variable: ENV")

        # for dev-division course purpose
        env = "test"

        config_file_name = os.path.join(PROJECT_PATH, "config", "envs", f"{env}.json")
        with open(config_file_name, "r") as f:
            env_config = f.read()
        self.update(json.loads(env_config))


app_config = AppConfig()
