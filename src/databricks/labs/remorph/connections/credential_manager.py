from pathlib import Path
import yaml


class Credentials:

    def __init__(self, product_info, source):
        self._product_info = product_info
        self._credentials = self._load_credentials(self._get_local_version_file_path())

    def _get_local_version_file_path(self):
        user_home = f"{Path(__file__).home()}"
        return Path(f"{user_home}/.databricks/labs/{self._product_info.product_name()}/credentials.yml")

    def _load_credentials(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            return yaml.safe_load(f)



