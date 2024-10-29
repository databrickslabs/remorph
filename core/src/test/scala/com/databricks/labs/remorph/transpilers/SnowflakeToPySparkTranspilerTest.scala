package com.databricks.labs.remorph.transpilers

import org.scalatest.wordspec.AnyWordSpec

class SnowflakeToPySparkTranspilerTest extends AnyWordSpec with TranspilerTestCommon {
  protected val transpiler = new SnowflakeToPySparkTranspiler

  "Snowflake SQL" should {
    "transpile window functions" in {
      s"""SELECT LAST_VALUE(c1)
         |IGNORE NULLS OVER (PARTITION BY t1.c2 ORDER BY t1.c3 DESC
         |RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS dc4
         |FROM t1;""".stripMargin transpilesTo
        """
          |...
          |""".stripMargin
    }
  }
}
