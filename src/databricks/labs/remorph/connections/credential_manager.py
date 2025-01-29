from pathlib import Path
import logging
import shutil
import yaml


from databricks.labs.blueprint.tui import Prompts

from databricks.labs.remorph.connections.env_getter import EnvGetter

logger = logging.getLogger(__name__)


class Credentials:
    def __init__(self, product_name: str, env: EnvGetter) -> None:
        self._product_name = product_name
        self._env = env
        self._credential_file = self._get_local_version_file_path()
        self._credentials: dict[str, str] = self._load_credentials(self._credential_file)

    def _get_local_version_file_path(self) -> Path:
        user_home = f"{Path(__file__).home()}"
        return Path(f"{user_home}/.databricks/labs/{self._product_name}/credentials.yml")

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

    def configure(self, prompts: Prompts):
        cred_file = self._credential_file
        source_details = prompts.question("Please enter the source details:")

        logger.info("Please refer to the documentation to understand the difference between local and env.")

        secret_vault_type = prompts.choice(
            "Enter secret vault type (local | databricks | env)", ["local", "env", "databricks"]
        )
        secret_vault_name = prompts.question("Enter secret vault name (or leave blank for none):")
        # Currently covering only MSSQL
        credentials = {
            "secret_vault_type": secret_vault_type,
            "secret_vault_name": secret_vault_name,
            source_details: {
                "database": prompts.question("Enter the database name:"),
                "driver": prompts.question("Enter the driver details:"),
                "server": prompts.question("Enter the server or host details:"),
                "port": prompts.question("Enter the port details:"),
                "user": prompts.question("Enter the user details:"),
                "password": prompts.question("Enter the password details:"),
            },
        }

        if cred_file.exists():
            backup_filename = cred_file.with_suffix('.bak')
            shutil.copy(cred_file, backup_filename)
            logger.debug(f"Backup of the existing file created at {backup_filename}")

        with open(cred_file, 'w', encoding='utf-8') as file:
            yaml.dump(credentials, file, default_flow_style=False)

        logger.info("Credential template created for MSSQL.")
