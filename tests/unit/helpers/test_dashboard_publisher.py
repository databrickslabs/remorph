from pathlib import Path
from unittest.mock import create_autospec

from databricks.labs.blueprint.installation import MockInstallation
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ObjectInfo, ObjectType

from databricks.labs.remorph.helpers.dashboard_publisher import DashboardPublisher


def test_create_dashboard():
    installation = MockInstallation(is_global=False)
    workspace_client = create_autospec(WorkspaceClient)
    dashboard_file = Path(__file__).parent / Path('../../resources/Remorph-Reconciliation.lvdash.json')
    expected_dashboard_metadata = ObjectInfo(
        object_type=ObjectType.DASHBOARD,
        path="/Users/first.last@example.com/folder/Remorph-Reconciliation.lvdash.json",
        object_id=7616304051637820,
        resource_id="9c1fbf4ad3449be67d6cb64c8acc730b",
    )

    workspace_client.workspace.get_status.return_value = expected_dashboard_metadata

    dashboard_publisher = DashboardPublisher(workspace_client, installation)
    dashboard_metadata = dashboard_publisher.create(dashboard_file)
    installation.assert_file_uploaded(dashboard_file.name, dashboard_file.read_bytes())
    assert dashboard_metadata == expected_dashboard_metadata


def test_create_dashboard_with_params():
    installation = MockInstallation(is_global=False)
    workspace_client = create_autospec(WorkspaceClient)
    dashboard_params = {
        "catalog": "remorph1",
        "schema": "reconcile1",
    }

    dashboard_file = Path(__file__).parent / Path('../../resources/Remorph-Reconciliation.lvdash.json')
    substituted_dashboard_file = Path(__file__).parent / Path(
        '../../resources/Remorph-Reconciliation-Substituted.lvdash.json'
    )

    dashboard_publisher = DashboardPublisher(workspace_client, installation)
    dashboard_publisher.create(dashboard_file, parameters=dashboard_params)
    installation.assert_file_uploaded(dashboard_file.name, substituted_dashboard_file.read_bytes())
