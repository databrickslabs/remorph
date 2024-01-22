import json
import os

from databricks.labs.blueprint.cli import App
from databricks.labs.blueprint.entrypoint import get_logger
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph import __about__
from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.reconcile.execute import recon
from databricks.labs.remorph.transpiler.execute import morph

remorph = App(__file__)
logger = get_logger(__file__)


def raise_validation_exception(msg: str) -> Exception:
    raise Exception(msg)


@remorph.command(is_unauthenticated=True)
def transpile(
    source: str,
    input_sql: str,
    output_folder: str,
    skip_validation: str,
    catalog_name: str,
    schema_name: str,
):
    """transpiles source dialect to databricks dialect"""

    if source.lower() not in ("snowflake", "tsql"):
        raise_validation_exception(
            f"Error: Invalid value for '--source': '{source}' is not one of 'snowflake', 'tsql'. "
        )
    if not os.path.exists(input_sql) or input_sql in (None, ""):
        raise_validation_exception(f"Error: Invalid value for '--input_sql': Path '{input_sql}' does not exist.")
    if output_folder == "":
        output_folder = None
    if skip_validation.lower() not in ("true", "false"):
        raise_validation_exception(
            f"Error: Invalid value for '--skip_validation': '{skip_validation}' is not one of 'true', 'false'. "
        )

    config = MorphConfig(
        source=source.lower(),
        input_sql=input_sql,
        output_folder=output_folder,
        skip_validation=skip_validation.lower() == "true",  # convert to bool
        catalog_name=catalog_name,
        schema_name=schema_name,
    )

    status = morph(config)

    print(json.dumps(status))


@remorph.command(is_unauthenticated=True)
def reconcile(recon_conf: str, conn_profile: str, source: str, report: str):
    """reconciles source to databricks datasets"""

    if not os.path.exists(recon_conf) or recon_conf in (None, ""):
        raise_validation_exception(f"Error: Invalid value for '--recon_conf': Path '{recon_conf}' does not exist.")
    if not os.path.exists(conn_profile) or conn_profile in (None, ""):
        raise_validation_exception(f"Error: Invalid value for '--conn_profile': Path '{conn_profile}' does not exist.")
    if source.lower() not in "snowflake":
        raise_validation_exception(f"Error: Invalid value for '--source': '{source}' is not one of 'snowflake'. ")
    if report.lower() not in ("data", "schema", "all"):
        raise_validation_exception(
            f"Error: Invalid value for '--report': '{report}' is not one of 'data', 'schema', 'all' "
        )

    recon(recon_conf, conn_profile, source, report)


if __name__ == "__main__":
    version = __about__.__version__
    ws = WorkspaceClient(product="remorph", product_version=version)
    ws.current_user.me()
    logger.info(f"user: {ws.current_user.me()}")
    remorph()
