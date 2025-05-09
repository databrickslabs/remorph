from ...src.config.settings import settings


def test_databricks_cluster_id():
    assert settings.DATABRICKS_CLUSTER_ID is not None


def test_remorph_metadata_schema():
    assert settings.REMORPH_METADATA_SCHEMA is not None


def test_recon_config_table_name():
    assert settings.RECON_CONFIG_TABLE_NAME is not None


# def test_recon_job_run_details_table_name():
#     assert settings.RECON_JOB_RUN_DETAILS_TABLE_NAME is not None
