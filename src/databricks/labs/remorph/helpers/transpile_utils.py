import json
import logging
import os

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound, PermissionDenied

from databricks.labs.blueprint.installation import Installation, SerdeError
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.remorph.config import MorphConfig, SQLGLOT_DIALECTS, DIALECTS
from databricks.labs.remorph.transpiler.execute import morph

logger = logging.getLogger(__name__)


def raise_validation_exception(msg: str) -> Exception:
    raise ValueError(msg)


class TranspileUtils:
    def __init__(
        self,
        w: WorkspaceClient,
        installation: Installation,
        prompts: Prompts = Prompts(),
    ):
        self._ws = w
        self._installation = installation
        self._prompts = prompts

    def _load_config(self) -> MorphConfig | None:
        transpile_config = None
        try:
            logger.info("Loading MorphConfig `config.yml` from Databricks Workspace...")
            transpile_config = self._installation.load(MorphConfig)
        except NotFound as err:
            logger.warning(f"Cannot find previous `transpile` installation: {err}")
        except (PermissionDenied, SerdeError, ValueError, AttributeError):
            logger.warning(f"Existing installation at {self._installation.install_folder()} is corrupted. Skipping...")

        reconfigure_msg = "Please use `remorph install` to re-configure ** transpile ** module"

        #   Re-configure `transpile` module:
        #    * when there is no `config.yml` config on Databricks workspace OR
        #    * when there is a `config.yml` config and user wants to overwrite it
        if not transpile_config:
            logger.error(f"Transpile `config.yml` not found / corrupted on Databricks Workspace.\n{reconfigure_msg}")
            return None
        if self._prompts.confirm(
            f"Would you like to overwrite workspace `Transpile Config` values:\n" f" {transpile_config.__dict__}?"
        ):
            logger.info(reconfigure_msg)
            return None

        return transpile_config

    def run(self):

        transpile_config = self._load_config()

        assert transpile_config, "Error: Cannot load Transpile `config.yml` from Databricks Workspace"

        if transpile_config.source.lower() not in SQLGLOT_DIALECTS:
            raise_validation_exception(
                f"Error: Invalid value for '--source': '{transpile_config.source}' is not one of {DIALECTS}. "
            )

        if not os.path.exists(transpile_config.input_sql) or transpile_config.input_sql in {None, ""}:
            raise_validation_exception(
                f"Error: Invalid value for '--input_sql':" f" Path '{transpile_config.input_sql}' does not exist."
            )

        if transpile_config.mode not in {"current", "experimental"}:
            raise_validation_exception(
                f"Error: Invalid value for '--mode': '{transpile_config.mode}' "
                f"is not one of 'current', "
                f"'experimental'."
            )

        config = MorphConfig(
            source=transpile_config.source.lower(),
            input_sql=transpile_config.input_sql,
            output_folder=transpile_config.output_folder,
            skip_validation=transpile_config.skip_validation,
            catalog_name=transpile_config.catalog_name,
            schema_name=transpile_config.schema_name,
            mode=transpile_config.mode,
            sdk_config=transpile_config.sdk_config,
        )

        status = morph(self._ws, config)

        print(json.dumps(status))
