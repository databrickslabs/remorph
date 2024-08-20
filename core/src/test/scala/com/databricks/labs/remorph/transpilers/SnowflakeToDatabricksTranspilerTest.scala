package com.databricks.labs.remorph.transpilers

import org.scalatest.wordspec.AnyWordSpec

class SnowflakeToDatabricksTranspilerTest extends AnyWordSpec with TranspilerTestCommon {

  protected val transpiler = new SnowflakeToDatabricksTranspiler

  "Snowflake transpiler" should {

    "transpile queries" in {

      /* Test BANG ! command */
      "!set error_flag = true" transpilesTo "--!set error_flag = true;"
      "!define tablename=CENUSTRACKONE" transpilesTo "--!define tablename=CENUSTRACKONE;"
      "!print Include This Text" transpilesTo "--!print Include This Text;"
      "!abort 77589bd1" transpilesTo "--!abort 77589bd1;"
      "SELECT * FROM employees WHERE department_id != 10;" transpilesTo
        "SELECT * FROM employees WHERE department_id != 10;"
      /* Test BANG command END */

      "SELECT * FROM t1;" transpilesTo "SELECT * FROM t1;"

      "SELECT t1.* FROM t1 INNER JOIN t2 ON t2.c2 = t2.c1;" transpilesTo
        "SELECT t1.* FROM t1 INNER JOIN t2 ON t2.c2 = t2.c1;"

      "SELECT t1.c2 FROM t1 LEFT OUTER JOIN t2 USING (c2);" transpilesTo
        "SELECT t1.c2 FROM t1 LEFT OUTER JOIN t2 USING (c2);"

      "SELECT c1::DOUBLE FROM t1;" transpilesTo "SELECT CAST(c1 AS DOUBLE) FROM t1;"
    }

  }

}
