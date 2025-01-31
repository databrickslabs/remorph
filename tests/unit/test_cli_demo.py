from pathlib import Path

from databricks.labs.remorph import cli


def test_transpile(mock_workspace_client_cli):
    morpheus_dir = Path(__file__).parent.parent / "resources" / "morpheus"
    transpiler = morpheus_dir / "lsp_config.yml"
    source_dialect = "snowflake"
    input_source = morpheus_dir / "snowflake_files"
    output_folder = morpheus_dir / "transpiled_files"
    error_file = morpheus_dir / "errors.log"
    skip_validation = "true"
    catalog_name = "my_catalog"
    schema_name = "my_schema"
    mode = "current"
    cli.transpile(
                mock_workspace_client_cli,
                str(transpiler.absolute()),
                source_dialect,
                str(input_source.absolute()),
                str(output_folder.absolute()),
                str(error_file.absolute()),
                skip_validation,
                catalog_name,
                schema_name,
                mode,
            )
