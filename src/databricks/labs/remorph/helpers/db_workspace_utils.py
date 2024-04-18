import logging

from databricks.labs.blueprint.tui import Prompts
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)


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
        logger.debug(f"Found Scope: `{scope_name}` in Databricks Workspace")
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
                logger.debug(f" Creating a new Scope: `{scope_name}`")
                self._ws.secrets.create_scope(scope_name)
            except Exception as ex:
                logger.error(f"Exception while creating Scope: {ex}")
                raise ex

            logger.info(f" Created a new Scope: `{scope_name}`")
        logger.info(f" Using Scope: `{scope_name}`...")

    @property
    def ws(self):
        return self._ws
