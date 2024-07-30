import logging
from importlib.resources import files

from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.installer import InstallState
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import InvalidParameterValue, NotFound

import databricks.labs.remorph.resources
from databricks.labs.remorph.config import ReconcileConfig
from databricks.labs.remorph.deployment.dashboard import DashboardDeployment
from databricks.labs.remorph.deployment.job import JobDeployment
from databricks.labs.remorph.deployment.table import TableDeployment

logger = logging.getLogger(__name__)

_RECON_PREFIX = "Reconciliation"
RECON_JOB_NAME = f"{_RECON_PREFIX} Runner"
RECON_METRICS_DASHBOARD_NAME = f"{_RECON_PREFIX} Metrics"


class ReconDeployment:
    def __init__(
        self,
        ws: WorkspaceClient,
        installation: Installation,
        install_state: InstallState,
        product_info: ProductInfo,
        table_deployer: TableDeployment,
        job_deployer: JobDeployment,
        dashboard_deployer: DashboardDeployment,
    ):
        self._ws = ws
        self._installation = installation
        self._install_state = install_state
        self._product_info = product_info
        self._table_deployer = table_deployer
        self._job_deployer = job_deployer
        self._dashboard_deployer = dashboard_deployer

    def install(self, recon_config: ReconcileConfig | None):
        if not recon_config:
            return
        logger.info("Installing reconcile components.")
        self._deploy_tables(recon_config)
        self._deploy_dashboards(recon_config)
        self._deploy_jobs(recon_config)
        self._install_state.save()
        logger.info("Installation of reconcile components completed successfully.")

    def uninstall(self, recon_config: ReconcileConfig | None):
        if not recon_config:
            return
        logger.info("Uninstalling reconcile components.")
        self._remove_dashboards()
        self._remove_jobs()
        logging.info(
            f"Won't remove reconcile metadata schema `{recon_config.metadata_config.schema}` "
            f"from catalog `{recon_config.metadata_config.catalog}`. Please remove it and the tables inside manually."
        )
        logging.info(
            f"Won't remove configured reconcile secret scope `{recon_config.secret_scope}`. "
            f"Please remove it manually."
        )

    def _deploy_tables(self, recon_config: ReconcileConfig):
        logger.info("Deploying reconciliation metadata tables.")
        catalog = recon_config.metadata_config.catalog
        schema = recon_config.metadata_config.schema
        resources = files(databricks.labs.remorph.resources)
        query_dir = resources.joinpath("reconcile/queries/installation")
        main_table_file = query_dir.joinpath("main.sql")
        metrics_table_file = query_dir.joinpath("metrics.sql")
        details_table_file = query_dir.joinpath("details.sql")

        self._table_deployer.deploy_table_from_ddl_file(catalog, schema, "main", main_table_file)
        self._table_deployer.deploy_table_from_ddl_file(catalog, schema, "metrics", metrics_table_file)
        self._table_deployer.deploy_table_from_ddl_file(catalog, schema, "details", details_table_file)

    def _deploy_dashboards(self, recon_config: ReconcileConfig):
        logger.info("Deploying reconciliation dashboards.")
        self._deploy_recon_metrics_dashboard(RECON_METRICS_DASHBOARD_NAME, recon_config)
        for dashboard_name, dashboard_id in self._get_deprecated_dashboards():
            try:
                logger.info(f"Removing dashboard_id={dashboard_id}, as it is no longer needed.")
                del self._install_state.dashboards[dashboard_name]
                self._ws.lakeview.trash(dashboard_id)
            except (InvalidParameterValue, NotFound):
                logger.warning(f"Dashboard `{dashboard_name}` doesn't exist anymore for some reason.")
                continue

    def _deploy_recon_metrics_dashboard(self, name: str, recon_config: ReconcileConfig):
        dashboard_params = {
            "catalog": recon_config.metadata_config.catalog,
            "schema": recon_config.metadata_config.schema,
        }

        reconcile_dashboard_path = "reconcile/dashboards/Remorph-Reconciliation.lvdash.json"
        dashboard_file = files(databricks.labs.remorph.resources).joinpath(reconcile_dashboard_path)
        logger.info(f"Creating Reconciliation Dashboard `{name}`")
        self._dashboard_deployer.deploy(name, dashboard_file, parameters=dashboard_params)

    def _get_dashboards(self) -> list[tuple[str, str]]:
        return [
            (dashboard_name, dashboard_id)
            for dashboard_name, dashboard_id in self._install_state.dashboards.items()
            if dashboard_name.startswith(_RECON_PREFIX)
        ]

    def _get_deprecated_dashboards(self) -> list[tuple[str, str]]:
        return [
            (dashboard_name, dashboard_id)
            for dashboard_name, dashboard_id in self._install_state.dashboards.items()
            if dashboard_name.startswith(_RECON_PREFIX) and dashboard_name != RECON_METRICS_DASHBOARD_NAME
        ]

    def _remove_dashboards(self):
        logger.info("Removing reconciliation dashboards.")
        for dashboard_name, dashboard_id in self._get_dashboards():
            try:
                logger.info(f"Removing dashboard {dashboard_name} with dashboard_id={dashboard_id}.")
                del self._install_state.dashboards[dashboard_name]
                self._ws.lakeview.trash(dashboard_id)
            except (InvalidParameterValue, NotFound):
                logger.warning(f"Dashboard `{dashboard_name}` doesn't exist anymore for some reason.")
                continue

    def _deploy_jobs(self, recon_config: ReconcileConfig):
        logger.info("Deploying reconciliation jobs.")
        self._job_deployer.deploy_recon_job(RECON_JOB_NAME, recon_config)
        for job_name, job_id in self._get_deprecated_jobs():
            try:
                logger.info(f"Removing job_id={job_id}, as it is no longer needed.")
                del self._install_state.jobs[job_name]
                self._ws.jobs.delete(job_id)
            except (InvalidParameterValue, NotFound):
                logger.warning(f"{job_name} doesn't exist anymore for some reason.")
                continue

    def _get_jobs(self) -> list[tuple[str, int]]:
        return [
            (job_name, int(job_id))
            for job_name, job_id in self._install_state.jobs.items()
            if job_name.startswith(_RECON_PREFIX)
        ]

    def _get_deprecated_jobs(self) -> list[tuple[str, int]]:
        return [
            (job_name, int(job_id))
            for job_name, job_id in self._install_state.jobs.items()
            if job_name.startswith(_RECON_PREFIX) and job_name != RECON_JOB_NAME
        ]

    def _remove_jobs(self):
        logger.info("Removing Reconciliation Jobs.")
        for job_name, job_id in self._get_jobs():
            try:
                logger.info(f"Removing job {job_name} with job_id={job_id}.")
                del self._install_state.jobs[job_name]
                self._ws.jobs.delete(int(job_id))
            except (InvalidParameterValue, NotFound):
                logger.warning(f"{job_name} doesn't exist anymore for some reason.")
                continue
