import json
import os

from databricks.labs.blueprint.cli import App
from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.blueprint.installation import Installation
from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.reconcile.execute import recon
from databricks.labs.remorph.transpiler.execute import morph
from databricks.sdk import WorkspaceClient

remorph = App(__file__)
logger = get_logger(__file__)


def raise_validation_exception(msg: str) -> Exception:
    raise ValueError(msg)


@remorph.command
def transpile(
    w: WorkspaceClient,
    source: str,
    input_sql: str,
    output_folder: str,
    skip_validation: str,
    catalog_name: str,
    schema_name: str,
    mode: str,
):
    """transpiles source dialect to databricks dialect"""
    logger.info(f"user: {w.current_user.me()}")
    installation = Installation.current(w, 'remorph')
    default_config = installation.load(MorphConfig)
    mode = mode if mode else "current"  # not checking for default config as it will always be current

    if source.lower() not in {"snowflake", "tsql"}:
        raise_validation_exception(
            f"Error: Invalid value for '--source': '{source}' is not one of 'snowflake', 'tsql'. "
        )
    if not os.path.exists(input_sql) or input_sql in {None, ""}:
        raise_validation_exception(f"Error: Invalid value for '--input_sql': Path '{input_sql}' does not exist.")
    if output_folder == "":
        output_folder = default_config.output_folder if default_config.output_folder else None
    if skip_validation.lower() not in {"true", "false"}:
        raise_validation_exception(
            f"Error: Invalid value for '--skip_validation': '{skip_validation}' is not one of 'true', 'false'. "
        )
    if mode.lower() not in {"current", "experimental"}:
        raise_validation_exception(
            f"Error: Invalid value for '--mode': '{mode}' " f"is not one of 'current', 'experimental'. "
        )

    sdk_config = default_config.sdk_config if default_config.sdk_config else None
    config = MorphConfig(
        source=source.lower(),
        input_sql=input_sql,
        output_folder=output_folder,
        skip_validation=skip_validation.lower() == "true",  # convert to bool
        catalog_name=catalog_name,
        schema_name=schema_name,
        mode=mode,
        sdk_config=sdk_config,
    )

    status = morph(w, config)

    print(json.dumps(status))


@remorph.command
def reconcile(w: WorkspaceClient, recon_conf: str, conn_profile: str, source: str, report: str):
    """reconciles source to databricks datasets"""
    logger.info(f"user: {w.current_user.me()}")
    if not os.path.exists(recon_conf) or recon_conf in {None, ""}:
        raise_validation_exception(f"Error: Invalid value for '--recon_conf': Path '{recon_conf}' does not exist.")
    if not os.path.exists(conn_profile) or conn_profile in {None, ""}:
        raise_validation_exception(f"Error: Invalid value for '--conn_profile': Path '{conn_profile}' does not exist.")
    if source.lower() not in "snowflake":
        raise_validation_exception(f"Error: Invalid value for '--source': '{source}' is not one of 'snowflake'. ")
    if report.lower() not in {"data", "schema", "all"}:
        raise_validation_exception(
            f"Error: Invalid value for '--report': '{report}' is not one of 'data', 'schema', 'all' "
        )

    recon(recon_conf, conn_profile, source, report)


if __name__ == "__main__":
    remorph()
