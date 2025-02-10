import yaml
from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.remorph.assessments.configure_assessment import ConfigureAssessment


def test_configure_credentials(tmp_path):
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
            r"Do you test the connection to the source system?": "no",
        }
    )
    file = tmp_path / ".credentials.yml"
    assessment = ConfigureAssessment(product_name="remorph", prompts=prompts, credential_file=file)
    assessment.run()

    expected_credentials = {
        'secret_vault_type': 'env',
        'secret_vault_name': None,
        'mssql': {
            'database': 'TEST_TSQL_JDBC',
            'driver': 'ODBC Driver 18 for SQL Server',
            'server': 'TEST_TSQL_JDBC',
            'port': 1433,
            'user': 'TEST_TSQL_USER',
            'password': 'TEST_TSQL_PASS',
        },
    }

    with open(file, 'r', encoding='utf-8') as file:
        credentials = yaml.safe_load(file)

    assert credentials == expected_credentials
