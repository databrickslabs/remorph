from unittest.mock import create_autospec

from databricks.labs.blueprint.installation import MockInstallation
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import InvalidParameterValue
from databricks.sdk.service.jobs import Job

from databricks.labs.remorph.config import RemorphConfigs
from databricks.labs.remorph.contexts.application import CliContext
from databricks.labs.remorph.deployment.job import JobDeployment


def test_deploy_new_job():
    ws = create_autospec(WorkspaceClient)
    job = Job(job_id=1234)
    ws.jobs.create.return_value = job
    ctx = CliContext(ws)
    installation = MockInstallation(is_global=False)
    ctx.replace(installation=installation)
    name = "Recon Job"
    job_deployer = JobDeployment(ctx)
    job_deployer.deploy_recon_job(name)
    ws.jobs.create.assert_called_once()
    assert ctx.install_state.jobs[name] == str(job.job_id)


def test_deploy_existing_job():
    ws = create_autospec(WorkspaceClient)
    ws.config.is_gcp = True
    job_id = 1234
    job = Job(job_id=job_id)
    name = "Recon Job"
    ctx = CliContext(ws)
    installation = MockInstallation({"state.json": {"resources": {"jobs": {name: job_id}}, "version": 1}})
    ctx.replace(
        product_info=ProductInfo.for_testing(RemorphConfigs),
        installation=installation,
    )
    job_deployer = JobDeployment(ctx)
    job_deployer.deploy_recon_job(name)
    ws.jobs.reset.assert_called_once()
    assert ctx.install_state.jobs[name] == str(job.job_id)


def test_deploy_missing_job():
    ws = create_autospec(WorkspaceClient)
    job_id = 1234
    job = Job(job_id=job_id)
    ws.jobs.create.return_value = job
    ws.jobs.reset.side_effect = InvalidParameterValue("Job not found")
    name = "Recon Job"
    ctx = CliContext(ws)
    installation = MockInstallation({"state.json": {"resources": {"jobs": {name: 5678}}, "version": 1}})
    ctx.replace(installation=installation)
    job_deployer = JobDeployment(ctx)
    job_deployer.deploy_recon_job(name)
    ws.jobs.create.assert_called_once()
    assert ctx.install_state.jobs[name] == str(job.job_id)
