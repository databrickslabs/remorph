from unittest.mock import patch

import pytest

from databricks.labs.remorph import cli
from databricks.labs.remorph.config import MorphConfig


class TestCLI:
    def test_transpile_with_invalid_dialect(self):
        with pytest.raises(Exception, match="Error: Invalid value for '--source'"):
            cli.transpile(
                "invalid_dialect",
                "/path/to/sql/file.sql",
                "/path/to/output",
                "true",
                "my_catalog",
                "my_schema",
            )

    def test_transpile_with_invalid_skip_validation(self):
        with patch("os.path.exists", return_value=True), pytest.raises(
            Exception, match="Error: Invalid value for '--skip_validation'"
        ):
            cli.transpile(
                "snowflake",
                "/path/to/sql/file.sql",
                "/path/to/output",
                "invalid_value",
                "my_catalog",
                "my_schema",
            )

    def test_invalid_input_sql(self):
        with patch("os.path.exists", return_value=False), pytest.raises(
            Exception, match="Error: Invalid value for '--input_sql'"
        ):
            cli.transpile(
                "snowflake",
                "/path/to/invalid/sql/file.sql",
                "/path/to/output",
                "true",
                "my_catalog",
                "my_schema",
            )

    def test_transpile_with_valid_input(self):
        source = "snowflake"
        input_sql = "/path/to/sql/file.sql"
        output_folder = "/path/to/output"
        skip_validation = "true"
        catalog_name = "my_catalog"
        schema_name = "my_schema"

        with patch("os.path.exists", return_value=True), patch(
            "databricks.labs.remorph.cli.morph", return_value={}
        ) as mock_morph:
            cli.transpile(source, input_sql, output_folder, skip_validation, catalog_name, schema_name)
            mock_morph.assert_called_once_with(
                MorphConfig(
                    source=source,
                    input_sql=input_sql,
                    output_folder=output_folder,
                    skip_validation=True,
                    catalog_name=catalog_name,
                    schema_name=schema_name,
                )
            )

    def test_transpile_empty_output_folder(self):
        source = "snowflake"
        input_sql = "/path/to/sql/file2.sql"
        output_folder = ""
        skip_validation = "false"
        catalog_name = "my_catalog"
        schema_name = "my_schema"

        with patch("os.path.exists", return_value=True), patch(
            "databricks.labs.remorph.cli.morph", return_value={}
        ) as mock_morph:
            cli.transpile(source, input_sql, output_folder, skip_validation, catalog_name, schema_name)
            mock_morph.assert_called_once_with(
                MorphConfig(
                    source=source,
                    input_sql=input_sql,
                    output_folder=None,
                    skip_validation=False,
                    catalog_name=catalog_name,
                    schema_name=schema_name,
                )
            )

    def test_recon_with_invalid_recon_conf(self, tmp_path):
        with pytest.raises(Exception, match="Error: Invalid value for '--recon_conf'"):
            invalid_recon_conf_path = tmp_path / "invalid_recon_conf"
            valid_conn_profile_path = tmp_path / "valid_conn_profile"
            valid_conn_profile_path.touch()
            source = "snowflake"
            report = "data"
            cli.reconcile(
                str(invalid_recon_conf_path.absolute()),
                str(valid_conn_profile_path.absolute()),
                source,
                report,
            )

    def test_recon_with_invalid_conn_profile(self, tmp_path):
        with pytest.raises(Exception, match="Error: Invalid value for '--conn_profile'"):
            valid_recon_conf_path = tmp_path / "valid_recon_conf"
            valid_recon_conf_path.touch()
            invalid_conn_profile_path = tmp_path / "invalid_conn_profile"
            source = "snowflake"
            report = "data"
            cli.reconcile(
                str(valid_recon_conf_path.absolute()),
                str(invalid_conn_profile_path.absolute()),
                source,
                report,
            )

    def test_recon_with_invalid_source(self):
        recon_conf = "/path/to/recon/conf"
        conn_profile = "/path/to/conn/profile"
        source = "invalid_source"
        report = "data"

        with patch("os.path.exists", return_value=True), pytest.raises(
            Exception, match="Error: Invalid value for '--source'"
        ):
            cli.reconcile(recon_conf, conn_profile, source, report)

    def test_recon_with_invalid_report(self):
        recon_conf = "/path/to/recon/conf"
        conn_profile = "/path/to/conn/profile"
        source = "snowflake"
        report = "invalid_report"

        with patch("os.path.exists", return_value=True), pytest.raises(
            Exception, match="Error: Invalid value for '--report'"
        ):
            cli.reconcile(recon_conf, conn_profile, source, report)

    def test_recon_with_valid_input(self):
        recon_conf = "/path/to/recon/conf"
        conn_profile = "/path/to/conn/profile"
        source = "snowflake"
        report = "data"

        with patch("os.path.exists", return_value=True), patch("databricks.labs.remorph.cli.recon") as mock_recon:
            cli.reconcile(recon_conf, conn_profile, source, report)
            mock_recon.assert_called_once_with(recon_conf, conn_profile, source, report)
