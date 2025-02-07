from pathlib import Path
import logging

import shutil
import yaml


from databricks.labs.blueprint.tui import Prompts


from typing import Protocol

import yaml


from databricks.labs.remorph.connections.env_getter import EnvGetter


logger = logging.getLogger(__name__)


class SecretProvider(Protocol):
    def get_secret(self, key: str) -> str:
        pass



class LocalSecretProvider:
    def get_secret(self, key: str) -> str:
        return key



class EnvSecretProvider:
    def __init__(self, env_getter: EnvGetter):
        self._env_getter = env_getter

    def get_secret(self, key: str) -> str:
        try:
            return self._env_getter.get(str(key))
        except KeyError:
            logger.debug(f"Environment variable {key} not found. Falling back to actual value")
            return key


class DatabricksSecretProvider:
    def get_secret(self, key: str) -> str:
        raise NotImplementedError("Databricks secret vault not implemented")


class CredentialManager:
    def __init__(self, credential_loader: dict, secret_providers: dict):
        self._credentials = credential_loader
        self._secret_providers = secret_providers
        self._default_vault = self._credentials.get('secret_vault_type', 'local').lower()

    def fetch(self, source: str) -> dict:
        if source not in self._credentials:
            raise KeyError(f"Source system: {source} credentials not found")

        value = self._credentials[source]
        if not isinstance(value, dict):
            raise KeyError(f"Invalid credential format for source: {source}")

        return {k: self._get_secret_value(v) for k, v in value.items()}

    def _get_secret_value(self, key: str) -> str:
        provider = self._secret_providers.get(self._default_vault)
        if not provider:
            raise ValueError(f"Unsupported secret vault type: {self._default_vault}")
        return provider.get_secret(key)


def _get_home() -> Path:
    return Path(__file__).home()


def _load_credentials(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Credentials file not found at {path}") from e


def create_credential_manager(product_name: str, env_getter: EnvGetter):
    file_path = Path(f"{_get_home()}/.databricks/labs/{product_name}/.credentials.yml")

    secret_providers = {
        'local': LocalSecretProvider(),
        'env': EnvSecretProvider(env_getter),
        'databricks': DatabricksSecretProvider(),
    }

    loader = _load_credentials(file_path)
    return CredentialManager(loader, secret_providers)


    def configure(self, prompts: Prompts):
        cred_file = self._credential_file
        source = str(prompts.question("Please enter the source system name (e.g. MSSQL, Snowflake, etc.)")).lower()
        logger.info(
            "\n(local | env) \nlocal means values are read as plain text \nenv means values are read "
            "from environment variables fall back to plain text if not variable is not found\n",
        )
        secret_vault_type = str(prompts.choice("Enter secret vault type (local | env)", ["local", "env"])).lower()

        secret_vault_name = None

        # TODO Implement Databricks secret vault

        logger.info("Please refer to the documentation to understand the difference between local and env.")

        # Currently covering only MSSQL
        credentials = {
            "secret_vault_type": secret_vault_type,
            "secret_vault_name": secret_vault_name,
            source: {
                "database": prompts.question("Enter the database name"),
                "driver": prompts.question("Enter the driver details"),
                "server": prompts.question("Enter the server or host details"),
                "port": int(prompts.question("Enter the port details", valid_number=True)),
                "user": prompts.question("Enter the user details"),
                "password": prompts.question("Enter the password details"),
            },
        }

        if cred_file.exists():
            backup_filename = cred_file.with_suffix('.bak')
            shutil.copy(cred_file, backup_filename)
            logger.debug(f"Backup of the existing file created at {backup_filename}")

        with open(cred_file, 'w', encoding='utf-8') as file:
            yaml.dump(credentials, file, default_flow_style=False)

        logger.info("Credential template created for MSSQL.")

        return source
