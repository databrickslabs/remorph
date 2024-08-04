package com.databricks.labs.remorph.transpilers

import org.scalatest.wordspec.AnyWordSpec

class SnowflakeToDatabricksTranspilerTest extends AnyWordSpec with TranspilerTestCommon {

  protected val transpiler = new SnowflakeToDatabricksTranspiler

  "Snowflake transpiler" should {

    "transpile queries" in {

      "SELECT * FROM t1;" transpilesTo "SELECT * FROM t1;"

      "SELECT t1.* FROM t1 INNER JOIN t2 ON t2.c2 = t2.c1;" transpilesTo
        "SELECT t1.* FROM t1 INNER JOIN t2 ON t2.c2 = t2.c1;"

      "SELECT t1.c2 FROM t1 LEFT OUTER JOIN t2 USING (c2);" transpilesTo
        "SELECT t1.c2 FROM t1 LEFT OUTER JOIN t2 USING (c2);"

      "SELECT c1::DOUBLE FROM t1;" transpilesTo "SELECT CAST(c1 AS DOUBLE) FROM t1;"
    }

  }

}
