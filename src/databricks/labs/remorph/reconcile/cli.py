import click

from databricks.labs.remorph.helpers.execution_time import timeit


@click.command("reconcile", no_args_is_help=True)
@click.option("--confpath", help="path of the data-recon config", type=click.Path(exists=True), required=True)
@click.option("--conprofile", help="path of the source connection config", type=click.Path(exists=True), required=True)
@click.option("--source", help="source type", type=click.Choice(["snowflake"], False), required=True)
@click.option(
    "--report",
    help="report type, by default all",
    type=click.Choice(["data", "schema", "all"], False),
    required=False,
    default="all",
)
@timeit
def entry_point(confpath, conprofile, source, report):
    click.echo(confpath)
    click.echo(conprofile)
    click.echo(source)
    click.echo(report)
    # Call the core reconcile function
