from pathlib import Path
import yaml
from databricks.labs.blueprint.wheels import ProductInfo

class Credentials:
    def __init__(self, product_info: ProductInfo) -> None:
        self._product_info = product_info
        self._credentials: dict[str, Any] = self._load_credentials(self._get_local_version_file_path())

    def _get_local_version_file_path(self) -> Path:
        user_home = f"{Path(__file__).home()}"
        return Path(f"{user_home}/.databricks/labs/{self._product_info.product_name()}/credentials.yml")

    def _load_credentials(self, file_path: Path) -> dict[str, str]:
        with open(file_path, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get(self, source: str) -> dict[str, str]:
        if source in self._credentials:
            return self._credentials[source]
        else:
            raise KeyError(f"source system: {source} credentials not found not in file credentials.yml")
