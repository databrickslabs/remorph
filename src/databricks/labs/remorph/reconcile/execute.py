from databricks.labs.remorph.helpers.execution_time import timeit


@timeit
def recon(recon_conf, conn_profile, source, report):
    # Ignore T201
    print(recon_conf)
    print(conn_profile)
    print(source)
    print(report)
    pass
