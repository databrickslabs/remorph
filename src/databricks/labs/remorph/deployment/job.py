import dataclasses
import logging
from datetime import datetime, timezone, timedelta
from typing import Any

from databricks.sdk.errors import InvalidParameterValue
from databricks.sdk.service import compute
from databricks.sdk.service.jobs import Task, PythonWheelTask, JobCluster, JobSettings

from databricks.labs.remorph.config import ReconcileConfig
from databricks.labs.remorph.contexts.application import WorkspaceContext
from databricks.labs.remorph.deployment.mixins import DeploymentMixin
from databricks.labs.remorph.reconcile.constants import SourceType

logger = logging.getLogger(__name__)


_TEST_JOBS_PURGE_TIMEOUT = timedelta(hours=1, minutes=15)


class JobDeployment(DeploymentMixin):
    def __init__(self, context: WorkspaceContext):
        self._context = context

    def deploy_recon_job(self, name, recon_config: ReconcileConfig):
        logger.info("Deploying reconciliation job.")
        job_id = self._update_or_create_recon_job(name, recon_config)
        logger.info(f"Reconciliation job deployed with job_id={job_id}")
        logger.info(f"Job URL: {self._context.workspace_client.config.host}#job/{job_id}")
        self._context.install_state.save()

    def _update_or_create_recon_job(self, name, recon_config: ReconcileConfig) -> str:
        description = "Run the reconciliation process"
        task_key = "run_reconciliation"

        job_settings = self._recon_job_settings(name, task_key, description, recon_config)
        if name in self._context.install_state.jobs:
            try:
                job_id = int(self._context.install_state.jobs[name])
                logger.info(f"Updating configuration for job `{name}`, job_id={job_id}")
                self._context.workspace_client.jobs.reset(job_id, JobSettings(**job_settings))
                return str(job_id)
            except InvalidParameterValue:
                del self._context.install_state.jobs[name]
                logger.warning(f"Job `{name}` does not exist anymore for some reason")
                return self._update_or_create_recon_job(name, recon_config)

        logger.info(f"Creating new job configuration for job `{name}`")
        new_job = self._context.workspace_client.jobs.create(**job_settings)
        assert new_job.job_id is not None
        self._context.install_state.jobs[name] = str(new_job.job_id)
        return str(new_job.job_id)

    def _recon_job_settings(
        self,
        job_name: str,
        task_key: str,
        description: str,
        recon_config: ReconcileConfig,
    ) -> dict[str, Any]:
        latest_lts_spark = self._context.workspace_client.clusters.select_spark_version(
            latest=True, long_term_support=True
        )
        version = self._context.product_info.version()
        version = version if not self._context.workspace_client.config.is_gcp else version.replace("+", "-")
        tags = {"version": f"v{version}"}
        if self._is_testing():
            # Add RemoveAfter tag for test job cleanup
            date_to_remove = self._get_test_purge_time()
            tags.update({"RemoveAfter": date_to_remove})

        return {
            "name": self.name_prefix(job_name, self._context.installation),
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
                    recon_config,
                ),
            ],
        }

    def _job_recon_task(self, jobs_task: Task, recon_config: ReconcileConfig) -> Task:
        libraries = [
            compute.Library(pypi=compute.PythonPyPiLibrary("databricks-labs-remorph")),
        ]
        source = recon_config.data_source
        if source == SourceType.ORACLE.value:
            # TODO: Automatically fetch a version list for `ojdbc8` and
            #  use the second latest version instead of hardcoding
            libraries.append(
                compute.Library(maven=compute.MavenLibrary("com.oracle.database.jdbc:ojdbc8:23.4.0.24.05")),
            )

        return dataclasses.replace(
            jobs_task,
            libraries=libraries,
            python_wheel_task=PythonWheelTask(
                package_name="databricks_labs_remorph",
                entry_point="reconcile",
            ),
        )

    def _is_testing(self):
        return self._context.product_info.product_name() != "remorph"

    @staticmethod
    def _get_test_purge_time() -> str:
        return (datetime.now(timezone.utc) + _TEST_JOBS_PURGE_TIMEOUT).strftime("%Y%m%d%H")

    def _get_default_node_type_id(self) -> str:
        return self._context.workspace_client.clusters.select_node_type(local_disk=True, min_memory_gb=16)
