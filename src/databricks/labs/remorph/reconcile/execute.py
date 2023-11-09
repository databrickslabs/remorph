from databricks.labs.remorph.helpers.execution_time import timeit


@timeit
def recon(recon_conf, conn_profile, source, report):
    # Ignore T201
    print(recon_conf)  # noqa: T201
    print(conn_profile)  # noqa: T201
    print(source)  # noqa: T201
    print(report)  # noqa: T201
    pass
