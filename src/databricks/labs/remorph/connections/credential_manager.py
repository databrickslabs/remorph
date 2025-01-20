from pathlib import Path
import yaml
from databricks.labs.blueprint.wheels import ProductInfo
import os


class Credentials:
    def __init__(self, product_info: ProductInfo) -> None:
        self._product_info = product_info
        self._credentials: dict[str, str] = self._load_credentials(self._get_local_version_file_path())

    def _get_local_version_file_path(self) -> Path:
        user_home = f"{Path(__file__).home()}"
        return Path(f"{user_home}/.databricks/labs/{self._product_info.product_name()}/credentials.yml")

    def _load_credentials(self, file_path: Path) -> dict[str, str]:
        with open(file_path, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get(self, source: str) -> dict[str, str]:
        error_msg = f"source system: {source} credentials not found in file credentials.yml"
        if source in self._credentials:
            value = self._credentials[source]
            if isinstance(value, dict):
                return {k: self.get_secret_value(v) for k, v in value.items()}
            raise KeyError(error_msg)
        raise KeyError(error_msg)

    def get_secret_value(self, key: str) -> str:
        secret_vault_type = self._credentials.get('secret_vault_type', 'local').lower()
        if secret_vault_type == 'local':
            return key
        elif secret_vault_type == 'env':
            print(f"key: {key}")
            v = os.getenv(str(key))  # Port numbers can be int
            print(v)
            if v is None:
                print(f"Environment variable {key} not found Failing back to actual strings")
                return key
            return v
        elif secret_vault_type == 'databricks':
            raise NotImplementedError("Databricks secret vault not implemented")
        else:
            raise ValueError(f"Unsupported secret vault type: {secret_vault_type}")
