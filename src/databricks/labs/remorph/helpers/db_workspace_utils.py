from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.blueprint.tui import Prompts
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors.platform import ResourceDoesNotExist

logger = get_logger(__file__)


class DatabricksSecretsClient:
    def __init__(self, ws: WorkspaceClient, prompts: Prompts):
        self._ws = ws
        self._prompts = prompts

    def _scope_exists(self, scope_name: str) -> bool:
        scope_exists = scope_name in [scope.name for scope in self._ws.secrets.list_scopes()]

        if not scope_exists:
            logger.error(
                f"Error: Cannot find Secret Scope: `{scope_name}` in Databricks Workspace"
                f"Use `remorph configure-secrets` to setup Scope and Secrets"
            )
            return False
        return True

    def get_or_create_scope(self, scope_name: str):
        """
        Get or Create a new Scope in Databricks Workspace
        :param scope_name:
        """
        scope_exists = self._scope_exists(scope_name)
        if not scope_exists:
            allow_scope_creation = self._prompts.confirm("Do you want to create a new one?")
            if not allow_scope_creation:
                msg = "Scope is needed to store Secrets in Databricks Workspace"
                raise SystemExit(msg)

            try:
                logger.debug(f" Creating a new Scope `{scope_name}`")
                self._ws.secrets.create_scope(scope_name)
            except Exception as ex:
                logger.error(f"Exception while creating Scope: {ex}")
                raise ex

            logger.info(f" Created a new Scope `{scope_name}`")
        logger.info(f" Using Scope `{scope_name}` to store Secrets")

    def secret_key_exists(self, scope_name: str, secret_key: str) -> bool:
        try:
            self._ws.secrets.get_secret(scope_name, secret_key)
            logger.info(f"Found Secret key `{secret_key}` in Scope `{scope_name}`")
            return True
        except ResourceDoesNotExist:
            logger.debug(f"Secret key `{secret_key}` not found in Scope `{scope_name}`")
            return False

    def delete_secret(self, scope_name: str, secret_key: str):
        try:
            logger.debug(f"Deleting Secret: *{secret_key}* in Scope: `{scope_name}`")
            self._ws.secrets.delete_secret(scope=scope_name, key=secret_key)
        except Exception as ex:
            logger.error(f"Exception while deleting Secret `{secret_key}`: {ex}")
            raise ex

    def store_secret(self, scope_name: str, secret_key: str, secret_value: str):
        try:
            logger.debug(f"Storing Secret: *{secret_key}* in Scope: `{scope_name}`")
            self._ws.secrets.put_secret(scope=scope_name, key=secret_key, string_value=secret_value)
        except Exception as ex:
            logger.error(f"Exception while storing Secret `{secret_key}`: {ex}")
            raise ex

    def store_connection_secrets(self, scope_name: str, conn_details: tuple[str, dict[str, str]]):
        engine = conn_details[0]
        secrets = conn_details[1]

        logger.debug(f"Storing `{engine}` Connection Secrets in Scope: `{scope_name}`")

        for key, value in secrets.items():
            secret_key = engine + '_' + key
            if self.secret_key_exists(scope_name, secret_key):
                overwrite_secret = self._prompts.confirm(f"Do you want to overwrite `{secret_key}`?")
                if overwrite_secret:
                    self.delete_secret(scope_name, secret_key)
                    logger.debug(f"Deleted Secret: *{secret_key}* in Scope: `{scope_name}`")
                    self.store_secret(scope_name, secret_key, value)
                    logger.info(f"Overwritten Secret: *{secret_key}* in Scope: `{scope_name}`")
            else:
                self.store_secret(scope_name, secret_key, value)
                logger.info(f"Stored Secret: *{secret_key}* in Scope: `{scope_name}`")

    @property
    def ws(self):
        return self._ws
