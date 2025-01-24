from pathlib import Path
import logging
import yaml

from databricks.labs.blueprint.wheels import ProductInfo
from databricks.labs.remorph.connections.env_getter import EnvGetter

logger = logging.getLogger(__name__)


class Credentials:
    def __init__(self, product_info: ProductInfo, env: EnvGetter) -> None:
        self._product_info = product_info
        self._env = env
        self._credentials: dict[str, str] = self._load_credentials(self._get_local_version_file_path())

    def _get_local_version_file_path(self) -> Path:
        user_home = f"{Path(__file__).home()}"
        return Path(f"{user_home}/.databricks/labs/{self._product_info.product_name()}/credentials.yml")

    def _load_credentials(self, file_path: Path) -> dict[str, str]:
        with open(file_path, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load(self, source: str) -> dict[str, str]:
        error_msg = f"source system: {source} credentials not found in file credentials.yml"
        if source in self._credentials:
            value = self._credentials[source]
            if isinstance(value, dict):
                return {k: self._get_secret_value(v) for k, v in value.items()}
            raise KeyError(error_msg)
        raise KeyError(error_msg)

    def _get_secret_value(self, key: str) -> str:
        secret_vault_type = self._credentials.get('secret_vault_type', 'local').lower()
        if secret_vault_type == 'local':
            return key
        if secret_vault_type == 'env':
            try:
                value = self._env.get(str(key))  # Port numbers can be int
            except KeyError:
                logger.debug(f"Environment variable {key} not found Failing back to actual string value")
                return key
            return value

        if secret_vault_type == 'databricks':
            raise NotImplementedError("Databricks secret vault not implemented")

        raise ValueError(f"Unsupported secret vault type: {secret_vault_type}")
