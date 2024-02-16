# Version changelog

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
