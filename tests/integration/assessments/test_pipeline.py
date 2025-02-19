from urllib.parse import urlparse

import pytest
from databricks.labs.remorph.assessments.pipeline import PipelineClass

from databricks.labs.remorph.connections.credential_manager import create_credential_manager
from databricks.labs.remorph.connections.database_manager import DatabaseManager

from ..connections.debug_envgetter import TestEnvGetter


@pytest.fixture()
def extractor(mock_credentials):
    env = TestEnvGetter(True)
    config = create_credential_manager("remorph", env).get_credentials("mssql")

    # since the kv has only URL so added explicit parse rules
    base_url, params = config['server'].replace("jdbc:", "", 1).split(";", 1)

    url_parts = urlparse(base_url)
    server = url_parts.hostname
    query_params = dict(param.split("=", 1) for param in params.split(";") if "=" in param)
    database = query_params.get("database", "" "")
    config['server'] = server
    config['database'] = database

    return DatabaseManager("mssql", config)


@pytest.fixture(scope="module")
def pipeline_config():
    config_path = "resources/assessments/pipeline_config.yml"
    return PipelineClass.load_config_from_yaml(config_path)


def test_run_pipeline(extractor, pipeline_config):
    pipeline = PipelineClass(config=pipeline_config, executor=extractor)
    pipeline.execute()
    assert 1 == 1
