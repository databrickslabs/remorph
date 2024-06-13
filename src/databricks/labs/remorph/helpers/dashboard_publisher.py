import json
from datetime import timedelta
from pathlib import Path
from typing import Any

from databricks.labs.blueprint.installation import Installation
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import DatabricksError
from databricks.sdk.retries import retried
from databricks.sdk.service.workspace import ObjectInfo


class DashboardPublisher:
    _UPLOAD_TIMEOUT = timedelta(seconds=30)

    def __init__(self, ws: WorkspaceClient, installation: Installation):
        self._ws = ws
        self._installation = installation

    def create(self, dashboard_file: Path, parameters: dict[str, Any] | None = None) -> ObjectInfo:
        if parameters is None:
            parameters = {}

        dashboard_data = self._substitute_params(dashboard_file, parameters)
        status = self._upload_and_get_status(dashboard_data, dashboard_file)
        return status

    @retried(on=[DatabricksError], timeout=_UPLOAD_TIMEOUT)
    def _upload_and_get_status(self, dashboard_data, dashboard_file):
        self._installation.upload(dashboard_file.name, dashboard_data)
        dashboard_workspace_path = f"{self._installation.install_folder()}/{dashboard_file.name}"
        status = self._ws.workspace.get_status(dashboard_workspace_path)
        return status

    def _substitute_params(self, dashboard_file: Path, parameters: dict[str, Any]) -> bytes:
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

        return json.dumps(dashboard_data).encode("utf-8")
