import os
from dotenv import load_dotenv
from databricks.connect.session import DatabricksSession


class Settings:
    def __init__(self):
        load_dotenv()
        self.DATABRICKS_CLUSTER_ID = os.getenv('DATABRICKS_CLUSTER_ID')
        self.REMORPH_METADATA_SCHEMA = os.getenv('REMORPH_METADATA_SCHEMA')
        self.RECON_CONFIG_TABLE_NAME = os.getenv('RECON_CONFIG_TABLE_NAME')
        self.RECON_JOB_RUN_DETAILS_TABLE_NAME = os.getenv('RECON_JOqB_RUN_DETAILS_TABLE_NAME')
        # self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.spark = DatabricksSession.builder.clusterId(self.DATABRICKS_CLUSTER_ID).getOrCreate()


settings = Settings()
