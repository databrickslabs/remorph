import base64
import logging

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.service.workspace import GetSecretResponse

logger = logging.getLogger(__name__)


class SecretsMixin:
    _ws: WorkspaceClient
    _scope: str

    def _get_secret_if_exists(self, secret_key: str) -> GetSecretResponse | None:
        """Get the secret value given a secret scope & secret key. Log a warning if secret does not exist"""
        try:
            # Return the decoded secret value in string format
            secret = self._ws.secrets.get_secret(self._scope, secret_key)
            assert secret is not None
            return secret
        except NotFound:
            logger.warning(f'secret not found: {self._scope}/{secret_key}')
            return None
