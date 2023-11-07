import click

from databricks.labs.remorph.helpers.execution_time import timeit


@click.command("transpile", no_args_is_help=True)
@click.option("--source", help="Input SQL Dialect Type", type=click.Choice(["snowflake", "tsql"], False))
@click.option("--input-sql", help="Input SQL Folder or File", type=click.Path(exists=True))
@click.option(
    "--output-folder", help="Output Location For Storing Transpiled Code", type=click.Path(exists=False), default=None
)
@click.option(
    "--skip-validation",
    help="Validate Transpiled Code, default True validation skipped, False validate",
    type=click.BOOL,
    default=True,
)
@click.option(
    "--validation-mode",
    help="Specifies the Validation Mode either Spark Local or Databricks using Databricks Connect",
    type=click.Choice(["LOCAL_REMOTE", "DATABRICKS"], False),
    default="LOCAL_REMOTE",
)
@click.option(
    "--catalog-nm",
    help="Catalog Name Applicable only when Validation Mode is `DATABRICKS`",
    type=click.STRING,
    default="transpiler_test",
)
@click.option(
    "--schema-nm",
    help="Schema Name Applicable only when Validation Mode is `DATABRICKS`",
    type=click.STRING,
    default="convertor_test",
)
@timeit
def entry_point(source, input_sql, output_folder, skip_validation, validation_mode, catalog_nm, schema_nm):
    click.echo(source)
    click.echo(input_sql)
    click.echo(output_folder)
    click.echo(skip_validation)
    click.echo(validation_mode)
    click.echo(catalog_nm)
    click.echo(schema_nm)
    # Call the core transpile function