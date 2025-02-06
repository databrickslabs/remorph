import pytest
from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.remorph.connections.credential_manager import Credentials
from databricks.labs.remorph.assessments.configure_assessment import ConfigureAssessment
from databricks.labs.remorph.connections.env_getter import EnvGetter



def test_configure_credentials():
    prompts = MockPrompts(
        {
            r"Please enter the source system name \(e\.g\. MSSQL, Snowflake, etc\.\)": "mssql",
            r"Enter secret vault type \(local \| env\)": sorted(['local', 'env']).index("env"),
            r"Enter the database name": "TEST_TSQL_JDBC",
            r"Enter the driver details": "ODBC Driver 18 for SQL Server",
            r"Enter the server or host details": "TEST_TSQL_JDBC",
            r"Enter the port details": "1433",
            r"Enter the user details": "TEST_TSQL_USER",
            r"Enter the password details": "TEST_TSQL_PASS",
        }
    )
    credential = Credentials("remorph", EnvGetter(True))
    source = credential.configure(prompts)
    assert source == "mssql"


@pytest.mark.skip("ignore")
def test_configure_assessment_without_test():
    prompts = MockPrompts(
        {
            r"Please enter the source system name (e.g. MSSQL, Snowflake, etc.)": "mssql",
            r"Enter secret vault type (local | env)": sorted(['local', 'env']).index("env"),
            r"Enter the database name": "TEST_TSQL_JDBC",
            r"Enter the driver details": "ODBC Driver 18 for SQL Server",
            r"Enter the server or host details": "TEST_TSQL_JDBC",
            r"Enter the port details": "1433",
            r"Enter the user details": "TEST_TSQL_USER",
            r"Enter the password details": "TEST_TSQL_PASS",
            r"Do you test the connection to the source system?": "no",
        }
    )
    credential = Credentials("remorph", EnvGetter(True))

    assessment = ConfigureAssessment(product_name="remorph", prompts=prompts, cred_manager=credential)
    assessment.run()
