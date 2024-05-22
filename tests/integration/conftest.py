import json
import os
import pathlib
import sys
from collections.abc import MutableMapping

import pytest

from databricks.sdk import WorkspaceClient


def _is_in_debug() -> bool:
    return os.path.basename(sys.argv[0]) in [
        "_jb_pytest_runner.py",
        "testlauncher.py",
    ]


@pytest.fixture
def debug_env_name():
    # Alternatively, we could use @pytest.mark.xxx, but
    # not sure how reusable it becomes then.
    #
    # we don't use scope=session, as monkeypatch.setenv
    # doesn't work on a session level
    return "UNKNOWN"


@pytest.fixture
def debug_env(monkeypatch, debug_env_name) -> MutableMapping[str, str]:
    if not _is_in_debug():
        return os.environ
    conf_file = pathlib.Path.home() / ".databricks/debug-env.json"
    if not conf_file.exists():
        return os.environ
    with conf_file.open("r") as f:
        conf = json.load(f)
        if debug_env_name not in conf:
            sys.stderr.write(
                f"""{debug_env_name} not found in ~/.databricks/debug-env.json

            this usually means that you have to add the following fixture to
            conftest.py file in the relevant directory:

            @pytest.fixture
            def debug_env_name():
                return 'ENV_NAME' # where ENV_NAME is one of: {", ".join(conf.keys())}
            """
            )
            msg = f"{debug_env_name} not found in ~/.databricks/debug-env.json"
            raise KeyError(msg)
        for k, v in conf[debug_env_name].items():
            monkeypatch.setenv(k, v)
    return os.environ


@pytest.fixture
def product_info():
    return None, None


@pytest.fixture
def ws(product_info, debug_env) -> WorkspaceClient:
    # Use variables from Unified Auth
    # See https://databricks-sdk-py.readthedocs.io/en/latest/authentication.html
    product_name, product_version = product_info
    return WorkspaceClient(
        host=debug_env["DATABRICKS_HOST"],
        cluster_id=debug_env['DATABRICKS_CLUSTER_ID'],
        product=product_name,
        product_version=product_version,
    )
