import os
import json
import logging


class EnvGetter:
    def __init__(self, is_debug: bool = False):
        self.env = self._get_debug_env() if is_debug else dict(os.environ)

    def get(self, key: str) -> str:
        if key in self.env:
            return self.env[key]
        raise KeyError(f"not in env: {key}")

    def _get_debug_env(self) -> dict:
        try:
            debug_env_file = f"{os.path.expanduser('~')}/.databricks/debug-env.json"
            with open(debug_env_file, 'r', encoding='utf-8') as file:
                contents = file.read()
            logging.debug(f"Found debug env file: {debug_env_file}")
            raw = json.loads(contents)
            return raw.get("ucws", {})
        except FileNotFoundError:
            return dict(os.environ)
