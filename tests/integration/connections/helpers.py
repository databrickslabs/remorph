from urllib.parse import urlparse
from databricks.labs.remorph.connections.credential_manager import create_credential_manager
from databricks.labs.remorph.connections.database_manager import DatabaseManager
from .debug_envgetter import TestEnvGetter


def get_db_manager(product_name: str, source: str) -> DatabaseManager:
    env = TestEnvGetter(True)
    config = create_credential_manager(product_name, env).get_credentials(source)

    # Some JDBC connection strings separate hostname and query params
    # by semicolons, while others use ampersands
    if ";" in config["server"]:
        base_url, params = config["server"].replace("jdbc:", "", 1).split(";", 1)
    elif "?" in config["server"]:
        base_url, params = config["server"].replace("jdbc:", "", 1).split("?", 1)
    else:  # There are no query params
        base_url = config["server"].replace("jdbc:", "", 1)
        params = None

    url_parts = urlparse(base_url)
    server = url_parts.hostname
    config["server"] = server

    if params:
        # Some JDBC connection strings separate params by semicolons
        # while others separate by ampersands
        if ";" in params:
            query_param_sep = ";"
        elif "&" in params:
            query_param_sep = "&"
        else:
            raise ValueError("Unknown param separator in JDBC connection string.")

        for param in params.split(query_param_sep):
            split_param = param.split("=", 1)
            # Only pull out necessary connection params
            if split_param[0] in {"database", "warehouse", "user"}:
                config[split_param[0]] = split_param[1]

    return DatabaseManager(source, config)
