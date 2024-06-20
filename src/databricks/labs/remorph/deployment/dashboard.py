import json
import logging
from datetime import timedelta
from importlib.abc import Traversable
from typing import Any

from databricks.sdk.errors import DatabricksError
from databricks.sdk.errors import InvalidParameterValue
from databricks.sdk.retries import retried
from databricks.sdk.service.dashboards import Dashboard

from databricks.labs.remorph.contexts.application import CliContext
from databricks.labs.remorph.deployment.mixins import DeploymentMixin

logger = logging.getLogger(__name__)


class DashboardDeployment(DeploymentMixin):
    _UPLOAD_TIMEOUT = timedelta(seconds=30)

    def __init__(self, context: CliContext):
        self._context = context

    def deploy(self, name: str, dashboard_file: Traversable, parameters: dict[str, Any] | None = None):
        logger.debug(f"Deploying dashboard {name} from {dashboard_file.name}")
        dashboard_data = self._substitute_params(dashboard_file, parameters or {})
        dashboard = self._update_or_create_dashboard(name, dashboard_data, dashboard_file)
        logger.info(f"Dashboard deployed with dashboard_id {dashboard.dashboard_id}")
        logger.info(f"Dashboard URL: {self._context.connect_config.host}/sql/dashboardsv3/{dashboard.dashboard_id}")
        self._context.install_state.save()

    @retried(on=[DatabricksError], timeout=_UPLOAD_TIMEOUT)
    def _update_or_create_dashboard(self, name: str, dashboard_data, dashboard_file) -> Dashboard:
        install_state = self._context.install_state
        if name in install_state.dashboards:
            try:
                dashboard_id = install_state.dashboards[name]
                logger.info(f"Updating dashboard with id={dashboard_id}")
                updated_dashboard = self._context.workspace_client.lakeview.update(
                    dashboard_id,
                    display_name=self.name_prefix(name, self._context.installation),
                    serialized_dashboard=dashboard_data,
                )
                return updated_dashboard
            except InvalidParameterValue:
                del install_state.dashboards[name]
                logger.warning(f"Dashboard {name} does not exist anymore for some reason.")
                return self._update_or_create_dashboard(name, dashboard_data, dashboard_file)
        logger.info(f"Creating new dashboard {name}")
        new_dashboard = self._context.workspace_client.lakeview.create(
            display_name=self.name_prefix(name, self._context.installation),
            parent_path=install_state.install_folder(),
            serialized_dashboard=dashboard_data,
        )
        assert new_dashboard.dashboard_id is not None
        install_state.dashboards[name] = new_dashboard.dashboard_id
        return new_dashboard

    def _substitute_params(self, dashboard_file: Traversable, parameters: dict[str, Any]) -> str:
        if not parameters:
            return dashboard_file.read_text()

        with dashboard_file.open() as f:
            dashboard_data = json.load(f)

        for dataset in dashboard_data.get("datasets", []):
            for param in dataset.get("parameters", []):
                if param["keyword"] in parameters:
                    param["defaultSelection"] = {
                        "values": {
                            "dataType": "STRING",
                            "values": [
                                {"value": parameters[param["keyword"]]},
                            ],
                        },
                    }

        return json.dumps(dashboard_data)
