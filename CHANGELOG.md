# Version changelog

## 0.1.6

* Added serverless validation using lsql library ([#176](https://github.com/databrickslabs/remorph/issues/176)). Workspaceclient object is used with `product` name and `product_version` along with corresponding `cluster_id` or `warehouse_id` as `sdk_config` in `MorphConfig` object.
* Enhanced install script to enforce usage of a warehouse or cluster when `skip-validation` is set to `False` ([#213](https://github.com/databrickslabs/remorph/issues/213)). In this release, the installation process has been enhanced to mandate the use of a warehouse or cluster when the `skip-validation` parameter is set to `False`. This change has been implemented across various components, including the install script, `transpile` function, and `get_sql_backend` function. Additionally, new pytest fixtures and methods have been added to improve test configuration and resource management during testing. Unit tests have been updated to enforce usage of a warehouse or cluster when the `skip-validation` flag is set to `False`, ensuring proper resource allocation and validation process improvement. This development focuses on promoting a proper setup and usage of the system, guiding new users towards a correct configuration and improving the overall reliability of the tool.
* Patch subquery with json column access ([#190](https://github.com/databrickslabs/remorph/issues/190)). The open-source library has been updated with new functionality to modify how subqueries with JSON column access are handled in the `snowflake.py` file. This change includes the addition of a check for an opening parenthesis after the `FROM` keyword to detect and break loops when a subquery is found, as opposed to a table name. This improvement enhances the handling of complex subqueries and JSON column access, making the code more robust and adaptable to different query structures. Additionally, a new test method, `test_nested_query_with_json`, has been introduced to the `tests/unit/snow/test_databricks.py` file to test the behavior of nested queries involving JSON column access when using a Snowflake dialect. This new method validates the expected output of a specific nested query when it is transpiled to Snowflake's SQL dialect, allowing for more comprehensive testing of JSON column access and type casting in Snowflake dialects. The existing `test_delete_from_keyword` method remains unchanged.
* Snowflake `UPDATE FROM` to Databricks `MERGE INTO` implementation ([#198](https://github.com/databrickslabs/remorph/issues/198)). 
* Use Runtime SQL backend in Notebooks ([#211](https://github.com/databrickslabs/remorph/issues/211)). In this update, the `db_sql.py` file in the `databricks/labs/remorph/helpers` directory has been modified to support the use of the Runtime SQL backend in Notebooks. This change includes the addition of a new `RuntimeBackend` class in the `backends` module and an import statement for `os`. The `get_sql_backend` function now returns a `RuntimeBackend` instance when the `DATABRICKS_RUNTIME_VERSION` environment variable is present, allowing for more efficient and secure SQL statement execution in Databricks notebooks. Additionally, a new test case for the `get_sql_backend` function has been added to ensure the correct behavior of the function in various runtime environments. These enhancements improve SQL execution performance and security in Databricks notebooks and increase the project's versatility for different use cases.
* Added Issue Templates for bugs, feature and config ([#194](https://github.com/databrickslabs/remorph/issues/194)). Two new issue templates have been added to the project's GitHub repository to improve issue creation and management. The first template, located in `.github/ISSUE_TEMPLATE/bug.yml`, is for reporting bugs and prompts users to provide detailed information about the issue, including the current and expected behavior, steps to reproduce, relevant log output, and sample query. The second template, added under the path `.github/ISSUE_TEMPLATE/config.yml`, is for configuration-related issues and includes support contact links for general Databricks questions and Remorph documentation, as well as fields for specifying the operating system and software version. A new issue template for feature requests, named "Feature Request", has also been added, providing a structured format for users to submit requests for new functionality for the Remorph project. These templates will help streamline the issue creation process, improve the quality of information provided, and make it easier for the development team to quickly identify and address bugs and feature requests.
* Added Databricks Source Adapter ([#185](https://github.com/databrickslabs/remorph/issues/185)). In this release, the project has been enhanced with several new features for the Databricks Source Adapter. A new `engine` parameter has been added to the `DataSource` class, replacing the original `source` parameter. The `_get_secrets` and `_get_table_or_query` methods have been updated to use the `engine` parameter for key naming and handling queries with a `select` statement differently, respectively. A Databricks Source Adapter for Oracle databases has been introduced, which includes a new `OracleDataSource` class that provides functionality to connect to an Oracle database using JDBC. A Databricks Source Adapter for Snowflake has also been added, featuring the `SnowflakeDataSource` class that handles data reading and schema retrieval from Snowflake. The `DatabricksDataSource` class has been updated to handle data reading and schema retrieval from Databricks, including a new `get_schema_query` method that generates the query to fetch the schema based on the provided catalog and table name. Exception handling for reading data and fetching schema has been implemented for all new classes. These changes provide increased flexibility for working with various data sources, improved code maintainability, and better support for different use cases.
* Added Threshold Query Builder ([#188](https://github.com/databrickslabs/remorph/issues/188)). In this release, the open-source library has added a Threshold Query Builder feature, which includes several changes to the existing functionality in the data source connector. A new import statement adds the `re` module for regular expressions, and new parameters have been added to the `read_data` and `get_schema` abstract methods. The `_get_jdbc_reader_options` method has been updated to accept a `options` parameter of type "JdbcReaderOptions", and a new static method, "_get_table_or_query", has been added to construct the table or query string based on provided parameters. Additionally, a new class, "QueryConfig", has been introduced in the "databricks.labs.remorph.reconcile" package to configure queries for data reconciliation tasks. A new abstract base class QueryBuilder has been added to the query_builder.py file, along with HashQueryBuilder and ThresholdQueryBuilder classes to construct SQL queries for generating hash values and selecting columns based on threshold values, transformation rules, and filtering conditions. These changes aim to enhance the functionality of the data source connector, add modularity, customizability, and reusability to the query builder, and improve data reconciliation tasks.
* Added snowflake connector code ([#177](https://github.com/databrickslabs/remorph/issues/177)). In this release, the open-source library has been updated to add a Snowflake connector for data extraction and schema manipulation. The changes include the addition of the SnowflakeDataSource class, which is used to read data from Snowflake using PySpark, and has methods for getting the JDBC URL, reading data with and without JDBC reader options, getting the schema, and handling exceptions. A new constant, SNOWFLAKE, has been added to the SourceDriver enum in constants.py, which represents the Snowflake JDBC driver class. The code modifications include updating the constructor of the DataSource abstract base class to include a new parameter 'scope', and updating the `_get_secrets` method to accept a `key_name` parameter instead of 'key'. Additionally, a test file 'test_snowflake.py' has been added to test the functionality of the SnowflakeDataSource class. This release also updates the pyproject.toml file to version lock the dependencies like black, ruff, and isort, and modifies the coverage report configuration to exclude certain files and lines from coverage checks. These changes were completed by Ravikumar Thangaraj and SundarShankar89.
* `remorph reconcile` baseline for Query Builder and Source Adapter for oracle as source ([#150](https://github.com/databrickslabs/remorph/issues/150)). 

Dependency updates:

 * Bump sqlglot from 22.4.0 to 22.5.0 ([#175](https://github.com/databrickslabs/remorph/pull/175)).
 * Updated databricks-sdk requirement from <0.22,>=0.18 to >=0.18,<0.23 ([#178](https://github.com/databrickslabs/remorph/pull/178)).
 * Updated databricks-sdk requirement from <0.23,>=0.18 to >=0.18,<0.24 ([#189](https://github.com/databrickslabs/remorph/pull/189)).
 * Bump actions/checkout from 3 to 4 ([#203](https://github.com/databrickslabs/remorph/pull/203)).
 * Bump actions/setup-python from 4 to 5 ([#201](https://github.com/databrickslabs/remorph/pull/201)).
 * Bump codecov/codecov-action from 1 to 4 ([#202](https://github.com/databrickslabs/remorph/pull/202)).
 * Bump softprops/action-gh-release from 1 to 2 ([#204](https://github.com/databrickslabs/remorph/pull/204)).

## 0.1.5

* Added Pylint Checker ([#149](https://github.com/databrickslabs/remorph/issues/149)). This diff adds a Pylint checker to the project, which is used to enforce a consistent code style, identify potential bugs, and check for errors in the Python code. The configuration for Pylint includes various settings, such as a line length limit, the maximum number of arguments for a function, and the maximum number of lines in a module. Additionally, several plugins have been specified to load, which add additional checks and features to Pylint. The configuration also includes settings that customize the behavior of Pylint's naming conventions checks and handle various types of code constructs, such as exceptions, logging statements, and import statements. By using Pylint, the project can help ensure that its code is of high quality, easy to understand, and free of bugs. This diff includes changes to various files, such as cli.py, morph_status.py, validate.py, and several SQL-related files, to ensure that they adhere to the desired Pylint configuration and best practices for code quality and organization.
* Fixed edge case where column name is same as alias name ([#164](https://github.com/databrickslabs/remorph/issues/164)). A recent commit has introduced fixes for edge cases related to conflicts between column names and alias names in SQL queries, addressing issues [#164](https://github.com/databrickslabs/remorph/issues/164) and [#130](https://github.com/databrickslabs/remorph/issues/130). The `check_for_unsupported_lca` function has been updated with two helper functions `_find_aliases_in_select` and `_find_invalid_lca_in_window` to detect aliases with the same name as a column in a SELECT expression and identify invalid Least Common Ancestors (LCAs) in window functions, respectively. The `find_windows_in_select` function has been refactored and renamed to `_find_windows_in_select` for improved code readability. The `transpile` and `parse` functions in the `sql_transpiler.py` file have been updated with try-except blocks to handle cases where a column name matches the alias name, preventing errors or exceptions such as `ParseError`, `TokenError`, and `UnsupportedError`. A new unit test, "test_query_with_same_alias_and_column_name", has been added to verify the fix, passing a SQL query with a subquery having a column alias `ca_zip` which is also used as a column name in the same query, confirming that the function correctly handles the scenario where a column name conflicts with an alias name.
* `TO_NUMBER` without `format` edge case ([#172](https://github.com/databrickslabs/remorph/issues/172)). The `TO_NUMBER without format edge case` commit introduces changes to address an unsupported usage of the `TO_NUMBER` function in Databicks SQL dialect when the `format` parameter is not provided. The new implementation introduces constants `PRECISION_CONST` and `SCALE_CONST` (set to 38 and 0 respectively) as default values for `precision` and `scale` parameters. These changes ensure Databricks SQL dialect requirements are met by modifying the `_to_number` method to incorporate these constants. An `UnsupportedError` will now be raised when `TO_NUMBER` is called without a `format` parameter, improving error handling and ensuring users are aware of the required `format` parameter. Test cases have been added for `TO_DECIMAL`, `TO_NUMERIC`, and `TO_NUMBER` functions with format strings, covering cases where the format is taken from table columns. The commit also ensures that an error is raised when `TO_DECIMAL` is called without a format parameter.

Dependency updates:

 * Bump sqlglot from 21.2.1 to 22.0.1 ([#152](https://github.com/databrickslabs/remorph/pull/152)).
 * Bump sqlglot from 22.0.1 to 22.1.1 ([#159](https://github.com/databrickslabs/remorph/pull/159)).
 * Updated databricks-labs-blueprint[yaml] requirement from ~=0.2.3 to >=0.2.3,<0.4.0 ([#162](https://github.com/databrickslabs/remorph/pull/162)).
 * Bump sqlglot from 22.1.1 to 22.2.0 ([#161](https://github.com/databrickslabs/remorph/pull/161)).
 * Bump sqlglot from 22.2.0 to 22.2.1 ([#163](https://github.com/databrickslabs/remorph/pull/163)).
 * Updated databricks-sdk requirement from <0.21,>=0.18 to >=0.18,<0.22 ([#168](https://github.com/databrickslabs/remorph/pull/168)).
 * Bump sqlglot from 22.2.1 to 22.3.1 ([#170](https://github.com/databrickslabs/remorph/pull/170)).
 * Updated databricks-labs-blueprint[yaml] requirement from <0.4.0,>=0.2.3 to >=0.2.3,<0.5.0 ([#171](https://github.com/databrickslabs/remorph/pull/171)).
 * Bump sqlglot from 22.3.1 to 22.4.0 ([#173](https://github.com/databrickslabs/remorph/pull/173)).

## 0.1.4

* Added conversion logic for Try_to_Decimal without format ([#142](https://github.com/databrickslabs/remorph/pull/142)).
* Identify Root Table for folder containing SQLs ([#124](https://github.com/databrickslabs/remorph/pull/124)).
* Install Script ([#106](https://github.com/databrickslabs/remorph/pull/106)).
* Integration Test Suite ([#145](https://github.com/databrickslabs/remorph/pull/145)).

Dependency updates:

 * Updated databricks-sdk requirement from <0.20,>=0.18 to >=0.18,<0.21 ([#143](https://github.com/databrickslabs/remorph/pull/143)).
 * Bump sqlglot from 21.0.0 to 21.1.2 ([#137](https://github.com/databrickslabs/remorph/pull/137)).
 * Bump sqlglot from 21.1.2 to 21.2.0 ([#147](https://github.com/databrickslabs/remorph/pull/147)).
 * Bump sqlglot from 21.2.0 to 21.2.1 ([#148](https://github.com/databrickslabs/remorph/pull/148)).

## 0.1.3

* Added support for WITHIN GROUP for ARRAY_AGG and LISTAGG functions ([#133](https://github.com/databrickslabs/remorph/pull/133)).
* Fixed Merge "INTO" for delete from syntax ([#129](https://github.com/databrickslabs/remorph/pull/129)).
* Fixed `DATE TRUNC` parse errors ([#131](https://github.com/databrickslabs/remorph/pull/131)).
* Patched Logger function call during wheel file ([#135](https://github.com/databrickslabs/remorph/pull/135)).
* Patched extra call to root path ([#126](https://github.com/databrickslabs/remorph/pull/126)).

Dependency updates:

 * Updated databricks-sdk requirement from ~=0.18.0 to >=0.18,<0.20 ([#134](https://github.com/databrickslabs/remorph/pull/134)).

## 0.1.2

* Fixed duplicate LCA warnings ([#108](https://github.com/databrickslabs/remorph/pull/108)).
* Fixed invalid flagging of LCA usage ([#117](https://github.com/databrickslabs/remorph/pull/117)).

Dependency updates:

 * Bump sqlglot from 20.10.0 to 20.11.0 ([#95](https://github.com/databrickslabs/remorph/pull/95)).
 * Bump sqlglot from 20.11.0 to 21.0.0 ([#122](https://github.com/databrickslabs/remorph/pull/122)).

## 0.1.1

* Added test_approx_percentile and test_trunc  Testcases ([#98](https://github.com/databrickslabs/remorph/pull/98)).
* Updated contributing/developer guide ([#97](https://github.com/databrickslabs/remorph/pull/97)).


## 0.1.0

* Added baseline for Databricks CLI frontend ([#60](https://github.com/databrickslabs/remorph/pull/60)).
* Added custom Databricks dialect test cases and lateral struct parsing ([#77](https://github.com/databrickslabs/remorph/pull/77)).
* Extended Snowflake to Databricks functions coverage ([#72](https://github.com/databrickslabs/remorph/pull/72), [#69](https://github.com/databrickslabs/remorph/pull/69)).
* Added `databricks labs remorph transpile` documentation for installation and usage ([#73](https://github.com/databrickslabs/remorph/pull/73)).

Dependency updates:

 * Bump sqlglot from 20.8.0 to 20.9.0 ([#83](https://github.com/databrickslabs/remorph/pull/83)).
 * Updated databricks-sdk requirement from ~=0.17.0 to ~=0.18.0 ([#90](https://github.com/databrickslabs/remorph/pull/90)).
 * Bump sqlglot from 20.9.0 to 20.10.0 ([#91](https://github.com/databrickslabs/remorph/pull/91)).

## 0.0.1

Initial commit
