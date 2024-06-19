import dataclasses
import logging
import os
from datetime import datetime, timedelta, timezone
from importlib.resources import files
from typing import Any

import databricks.labs.remorph.resources
from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.installer import InstallState
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.labs.lsql.backends import SqlBackend
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import InvalidParameterValue
from databricks.sdk.service import compute
from databricks.sdk.service.jobs import Task, PythonWheelTask, JobCluster, JobSettings

logger = logging.getLogger(__name__)

TEST_JOBS_PURGE_TIMEOUT = timedelta(hours=1, minutes=15)


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
    def __init__(
        self,
        workspace_client: WorkspaceClient,
        installation: Installation,
        install_state: InstallState,
        product_info: ProductInfo,
    ):
        self._ws = workspace_client
        self._installation = installation
        self._install_state = install_state
        self._product_info = product_info

    def deploy_job(self) -> str:
        logger.info("Deploying reconciliation job.")
        job_id = self._create_job()
        self._install_state.save()
        logger.info(f"Reconciliation job deployed with job_id={job_id}")
        logger.info(f"Job URL: {self._ws.config.host}#job/{job_id}")
        return job_id

    def _create_job(self) -> str:
        job_name = "Remorph_Reconciliation_Job"
        description = "Run the reconciliation process"
        task_key = "run_reconciliation"

        job_settings = self._job_settings(job_name, task_key, description)
        if job_name in self._install_state.jobs:
            try:
                job_id = int(self._install_state.jobs[job_name])
                logger.info(f"Updating configuration for job={job_name}, job_id={job_id}")
                self._ws.jobs.reset(job_id, JobSettings(**job_settings))
                return str(job_id)
            except InvalidParameterValue:
                del self._install_state.jobs[job_name]
                logger.warning(f"Job={job_name} does not exist anymore for some reason")
                return self._create_job()

        logger.info(f"Creating new job configuration for job={job_name}")
        new_job = self._ws.jobs.create(**job_settings)
        assert new_job.job_id is not None
        self._install_state.jobs[job_name] = str(new_job.job_id)
        return str(new_job.job_id)

    def _name(self, name: str) -> str:
        prefix = os.path.basename(self._installation.install_folder()).removeprefix('.')
        return f"[{prefix.upper()}] {name}"

    def _is_testing(self):
        return self._product_info.product_name() != "remorph"

    @staticmethod
    def _get_test_purge_time() -> str:
        return (datetime.now(timezone.utc) + TEST_JOBS_PURGE_TIMEOUT).strftime("%Y%m%d%H")

    def _job_settings(self, job_name: str, task_key: str, description: str) -> dict[str, Any]:
        latest_lts_spark = self._ws.clusters.select_spark_version(latest=True, long_term_support=True)
        version = self._product_info.version()
        version = version if not self._ws.config.is_gcp else version.replace("+", "-")
        tags = {"version": f"v{version}"}
        if self._is_testing():
            # Add RemoveAfter tag for test job cleanup
            date_to_remove = self._get_test_purge_time()
            tags.update({"RemoveAfter": date_to_remove})

        return {
            "name": self._name(job_name),
            "tags": tags,
            "job_clusters": [
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
            "tasks": [
                self._job_recon_task(
                    Task(
                        task_key=task_key,
                        description=description,
                        job_cluster_key="Remorph_Reconciliation_Cluster",
                    ),
                ),
            ],
        }

    def _job_recon_task(self, jobs_task: Task) -> Task:
        # TODO: fetch a version list for `ojdbc8` and use the second latest version instead of hardcoding
        libraries = [
            compute.Library(pypi=compute.PythonPyPiLibrary("databricks-labs-remorph")),
            compute.Library(maven=compute.MavenLibrary("com.oracle.database.jdbc:ojdbc8:23.4.0.24.05")),
        ]
        return dataclasses.replace(
            jobs_task,
            libraries=libraries,
            python_wheel_task=PythonWheelTask(
                package_name="databricks_labs_remorph",
                entry_point="reconcile",
            ),
        )

    def _get_default_node_type_id(self) -> str:
        return self._ws.clusters.select_node_type(local_disk=True, min_memory_gb=16)
