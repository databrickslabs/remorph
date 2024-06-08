import logging
from dataclasses import replace
from importlib.resources import files

from databricks.labs.blueprint.wheels import ProductInfo
from databricks.labs.lsql.backends import SqlBackend
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute
from databricks.sdk.service.jobs import Task, PythonWheelTask, JobCluster

import databricks.labs.remorph.resources

logger = logging.getLogger(__name__)


class TableDeployer:
    def __init__(self, sql_backend: SqlBackend, catalog: str, schema: str):
        self._sql_backend = sql_backend
        self._catalog = catalog
        self._schema = schema

    def deploy_table(self, table_name: str, relative_filepath: str):
        """
        Deploys a table to the catalog and schema specified in the constructor
        :param table_name: The table to deploy
        :param relative_filepath: DDL file path relative to the resource package
        """
        query = self._load(relative_filepath)
        logger.info(f"Deploying table {table_name} in {self._catalog}.{self._schema}")
        self._sql_backend.execute(query, catalog=self._catalog, schema=self._schema)

    def _load(self, relative_filename: str) -> str:
        sql = files(databricks.labs.remorph.resources).joinpath(relative_filename).read_text()
        return sql


class JobDeployer:
    def __init__(self, workspace_client: WorkspaceClient, product_info: ProductInfo):
        self._ws = workspace_client
        self._product_info = product_info

    def deploy_job(self) -> str:
        job_name = "Remorph_Reconciliation_Job"
        description = "Run the reconciliation process"
        task_key = "run_reconciliation"

        existing_jobs = self._ws.jobs.list(name=job_name)
        for job in existing_jobs:
            if job.settings and job.settings.name == job_name:
                logger.info(f"Job {job_name} already exists")
                return str(job.job_id)

        logger.info("Deploying reconciliation job.")
        version = self._product_info.version()
        tags = {"version": f"v{version}"}
        latest_lts_spark = self._ws.clusters.select_spark_version(latest=True, long_term_support=True)

        response = self._ws.jobs.create(
            name=job_name,
            tags=tags,
            job_clusters=[
                JobCluster(
                    job_cluster_key="Remorph_Reconciliation_Cluster",
                    new_cluster=compute.ClusterSpec(
                        data_security_mode=compute.DataSecurityMode.USER_ISOLATION,
                        spark_conf={},
                        node_type_id=self._get_default_node_type_id(),
                        autoscale=compute.AutoScale(min_workers=2, max_workers=10),
                        spark_version=latest_lts_spark,
                    ),
                )
            ],
            tasks=[
                self._job_recon_task(
                    Task(
                        task_key=task_key,
                        description=description,
                        job_cluster_key="Remorph_Reconciliation_Cluster",
                    ),
                ),
            ],
        )

        return str(response.job_id)

    def _job_recon_task(self, jobs_task: Task) -> Task:
        libraries = [compute.Library(pypi=compute.PythonPyPiLibrary("databricks-labs-remorph"))]
        return replace(
            jobs_task,
            libraries=libraries,
            python_wheel_task=PythonWheelTask(
                package_name="databricks-labs-remorph",
                entry_point="reconcile",
            ),
        )

    def _get_default_node_type_id(self) -> str:
        if self._ws.config.is_azure:
            return "Standard_D8_v3"
        elif self._ws.config.is_aws:
            return "i3.xlarge"
        elif self._ws.config.is_gcp:
            return "n1-standard-8"
        else:
            raise ValueError("Unknown cloud provider.")
