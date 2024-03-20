# Version changelog

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
