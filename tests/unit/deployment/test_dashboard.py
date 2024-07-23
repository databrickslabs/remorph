from pathlib import Path
from unittest.mock import create_autospec

from databricks.labs.blueprint.installation import MockInstallation
from databricks.labs.blueprint.installer import InstallState
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import InvalidParameterValue
from databricks.sdk.service.dashboards import Dashboard

from databricks.labs.remorph.deployment.dashboard import DashboardDeployment


def test_deploy_new_dashboard():
    dashboard_file = Path(__file__).parent / Path("../../resources/Remorph-Reconciliation.lvdash.json")
    ws = create_autospec(WorkspaceClient)
    dashboard = Dashboard(
        dashboard_id="9c1fbf4ad3449be67d6cb64c8acc730b",
        display_name="Remorph-Reconciliation",
    )
    ws.lakeview.create.return_value = dashboard
    installation = MockInstallation(is_global=False)
    install_state = InstallState.from_installation(installation)
    name = "Remorph-Reconciliation"
    dashboard_publisher = DashboardDeployment(ws, installation, install_state)
    dashboard_publisher.deploy(name, dashboard_file)
    _, kwargs = ws.lakeview.create.call_args
    assert kwargs["serialized_dashboard"] == dashboard_file.read_text()
    assert install_state.dashboards[name] == dashboard.dashboard_id


def test_deploy_new_dashboard_with_params():
    dashboard_file = Path(__file__).parent / Path("../../resources/Remorph-Reconciliation.lvdash.json")
    substituted_dashboard_file = Path(__file__).parent / Path(
        '../../resources/Remorph-Reconciliation-Substituted.lvdash.json'
    )

    ws = create_autospec(WorkspaceClient)
    dashboard = Dashboard(
        dashboard_id="9c1fbf4ad3449be67d6cb64c8acc730b",
        display_name="Remorph-Reconciliation",
    )
    ws.lakeview.create.return_value = dashboard

    installation = MockInstallation(is_global=False)
    install_state = InstallState.from_installation(installation)
    name = "Remorph-Reconciliation"
    dashboard_publisher = DashboardDeployment(ws, installation, install_state)
    dashboard_params = {
        "catalog": "remorph1",
        "schema": "reconcile1",
    }
    dashboard_publisher.deploy(name, dashboard_file, parameters=dashboard_params)
    _, kwargs = ws.lakeview.create.call_args
    assert kwargs["serialized_dashboard"] == substituted_dashboard_file.read_text()
    assert install_state.dashboards[name] == dashboard.dashboard_id


def test_deploy_new_parameterless_dashboard_with_user_params():
    dashboard_file = Path(__file__).parent / Path("../../resources/Test_Dashboard_No_Param.lvdash.json")
    ws = create_autospec(WorkspaceClient)
    dashboard = Dashboard(
        dashboard_id="8c1fbf4ad3449be67d6cb64c8acc730b",
        display_name="Test_Dashboard_No_Param",
    )
    ws.lakeview.create.return_value = dashboard

    installation = MockInstallation(is_global=False)
    install_state = InstallState.from_installation(installation)
    name = "Test_Dashboard_No_Param"
    dashboard_publisher = DashboardDeployment(ws, installation, install_state)
    dashboard_params = {
        "catalog": "remorph1",
        "schema": "reconcile1",
    }
    dashboard_publisher.deploy(name, dashboard_file, parameters=dashboard_params)
    assert install_state.dashboards[name] == dashboard.dashboard_id


def test_deploy_existing_dashboard():
    dashboard_file = Path(__file__).parent / Path("../../resources/Remorph-Reconciliation.lvdash.json")
    ws = create_autospec(WorkspaceClient)
    dashboard_id = "9c1fbf4ad3449be67d6cb64c8acc730b"
    dashboard = Dashboard(
        dashboard_id=dashboard_id,
        display_name="Remorph-Reconciliation",
    )
    ws.lakeview.update.return_value = dashboard
    name = "Remorph-Reconciliation"
    installation = MockInstallation({"state.json": {"resources": {"dashboards": {name: dashboard_id}}, "version": 1}})
    install_state = InstallState.from_installation(installation)
    dashboard_publisher = DashboardDeployment(ws, installation, install_state)
    dashboard_publisher.deploy(name, dashboard_file)
    _, kwargs = ws.lakeview.update.call_args
    assert kwargs["serialized_dashboard"] == dashboard_file.read_text()
    assert install_state.dashboards[name] == dashboard.dashboard_id


def test_deploy_missing_dashboard():
    dashboard_file = Path(__file__).parent / Path("../../resources/Remorph-Reconciliation.lvdash.json")
    ws = create_autospec(WorkspaceClient)
    dashboard_id = "9c1fbf4ad3449be67d6cb64c8acc730b"
    dashboard = Dashboard(
        dashboard_id=dashboard_id,
        display_name="Remorph-Reconciliation",
    )
    ws.lakeview.create.return_value = dashboard
    ws.lakeview.update.side_effect = InvalidParameterValue("Dashboard not found")
    name = "Remorph-Reconciliation"
    installation = MockInstallation(
        {
            "state.json": {
                "resources": {"dashboards": {name: "8c1fbf4ad3449be67d6cb64c8acc730b"}},
                "version": 1,
            },
        }
    )
    install_state = InstallState.from_installation(installation)
    dashboard_publisher = DashboardDeployment(ws, installation, install_state)
    dashboard_publisher.deploy(name, dashboard_file)
    _, kwargs = ws.lakeview.create.call_args
    assert kwargs["serialized_dashboard"] == dashboard_file.read_text()
    assert install_state.dashboards[name] == dashboard.dashboard_id
