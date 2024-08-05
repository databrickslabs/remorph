import logging
from datetime import timedelta
from pathlib import Path

from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.installer import InstallState
from databricks.sdk import WorkspaceClient
from databricks.sdk.retries import retried
from databricks.sdk.errors import InvalidParameterValue, NotFound, DatabricksError

from databricks.sdk.service.dashboards import LifecycleState
from databricks.labs.lsql.dashboards import DashboardMetadata, Dashboards

from databricks.labs.remorph.config import ReconcileMetadataConfig

logger = logging.getLogger(__name__)


class DashboardDeployment:
    _UPLOAD_TIMEOUT = timedelta(seconds=30)

    def __init__(
        self,
        ws: WorkspaceClient,
        installation: Installation,
        install_state: InstallState,
    ):
        self._ws = ws
        self._installation = installation
        self._install_state = install_state

    def _handle_existing_dashboard(self, dashboard_id: str, display_name: str, parent_path: str) -> str | None:
        try:
            dashboard = self._ws.lakeview.get(dashboard_id)
            if dashboard.lifecycle_state is None:
                raise NotFound(f"Dashboard life cycle state: {display_name} ({dashboard_id})")
            if dashboard.lifecycle_state == LifecycleState.TRASHED:
                logger.info(f"Recreating trashed dashboard: {display_name} ({dashboard_id})")
                return None  # Recreate the dashboard if it is trashed (manually)

        except (NotFound, InvalidParameterValue):
            logger.info(f"Recovering invalid dashboard: {display_name} ({dashboard_id})")
            try:
                dashboard_path = f"{parent_path}/{display_name}.lvdash.json"
                self._ws.workspace.delete(dashboard_path)  # Cannot recreate dashboard if file still exists
                logger.debug(f"Deleted dangling dashboard {display_name} ({dashboard_id}): {dashboard_path}")
            except NotFound:
                pass
            return None  # Recreate the dashboard if it's reference is corrupted (manually)
        return dashboard_id  # Update the existing dashboard

    def deploy(
        self,
        name: str,
        folder: Path,
        config: ReconcileMetadataConfig,
    ):
        """Create a dashboard from Queries inside folder"""
        logger.info(f"Deploying dashboard {name} from {folder}")
        parent_path = f"{self._installation.install_folder()}/dashboards"

        metadata = DashboardMetadata.from_path(folder).replace_database(
            database=f"hive_metastore.{config.schema}",
            database_to_replace="inventory",
        )

        metadata.display_name = self._name_with_prefix(metadata.display_name)

        reference = f"{folder.parent.stem}_{folder.stem}".lower()
        dashboard_id = self._install_state.dashboards.get(reference)
        if dashboard_id is not None:
            dashboard_id = self._handle_existing_dashboard(dashboard_id, metadata.display_name, parent_path)

        # dashboard_data = self._substitute_params(dashboard_file, parameters or {})
        dashboard_id = self._update_or_create_dashboard(name, dashboard_id, metadata, parent_path)
        logger.info(f"Dashboard deployed with dashboard_id {dashboard_id}")
        logger.info(f"Dashboard URL: {self._ws.config.host}/sql/dashboardsv3/{dashboard_id}")
        self._install_state.save()

    @retried(on=[DatabricksError], timeout=_UPLOAD_TIMEOUT)
    def _update_or_create_dashboard(
        self,
        name: str,
        dashboard_id: str,
        metadata: DashboardMetadata,
        parent_path: str,
    ) -> str:

        dashboard = Dashboards(self._ws).create_dashboard(
            metadata,
            dashboard_id=dashboard_id,
            parent_path=parent_path,
            warehouse_id=self._ws.config.warehouse_id,
            publish=True,
        )
        assert dashboard.dashboard_id is not None
        self._install_state.dashboards[name] = dashboard.dashboard_id
        return dashboard.dashboard_id

    def _name_with_prefix(self, name: str) -> str:
        prefix = self._installation.product()
        return f"[{prefix.upper()}] {name}"
