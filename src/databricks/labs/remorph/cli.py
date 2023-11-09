import json
import logging
import os
import sys

from databricks.labs.remorph.reconcile.execute import recon
from databricks.labs.remorph.transpiler.execute import morph

logger = logging.getLogger("databricks.labs.remorph")


def raise_validation_exception(msg):
    raise Exception(msg)


def transpile(source, input_sql, output_folder, skip_validation, validation_mode, catalog_nm, schema_nm):
    """Error: Invalid value for '--source': 'snowflakes' is not one of 'snowflake', 'tsql'."""
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
    if validation_mode.upper() not in ("LOCAL_REMOTE", "DATABRICKS"):
        raise_validation_exception(
            f"Error: Invalid value for '--validation_mode': '{validation_mode}' is not one of 'true', 'false'. "
        )

    morph(
        source.lower(),
        input_sql,
        output_folder,
        skip_validation.lower(),
        validation_mode.upper(),
        catalog_nm,
        schema_nm,
    )


def reconcile(recon_conf, conn_profile, source, report):
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


MAPPING = {
    "transpile": transpile,
    "reconcile": reconcile,
}


def main(raw):
    payload = json.loads(raw)
    command = payload["command"]
    if command not in MAPPING:
        msg = f"cannot find command: {command}"
        raise KeyError(msg)
    flags = payload["flags"]
    log_level = flags.pop("log_level")
    if log_level != "disabled":
        databricks_logger = logging.getLogger("databricks")
        databricks_logger.setLevel(log_level.upper())

    kwargs = {k.replace("-", "_"): v for k, v in flags.items()}
    MAPPING[command](**kwargs)


if __name__ == "__main__":
    main(*sys.argv[1:])
