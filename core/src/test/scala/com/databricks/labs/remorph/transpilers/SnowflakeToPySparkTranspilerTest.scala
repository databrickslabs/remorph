package com.databricks.labs.remorph.transpilers

import org.scalatest.wordspec.AnyWordSpec

class SnowflakeToPySparkTranspilerTest extends AnyWordSpec with TranspilerTestCommon {
  protected val transpiler = new SnowflakeToPySparkTranspiler
  protected override val reformat = false

  "Snowflake SQL" should {
    "transpile window functions" in {
      s"""SELECT LAST_VALUE(c1)
         |IGNORE NULLS OVER (PARTITION BY t1.c2 ORDER BY t1.c3 DESC
         |RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS dc4
         |FROM t1;""".stripMargin transpilesTo
        """import pyspark.sql.functions as F
          |from pyspark.sql.window import Window
          |spark.table('t1').select(Window.partitionBy(F.col('t1.c2')).orderBy(F.col('t1.c3').desc_nulls_first()).rangeBetween(Window.unboundedPreceding, Window.currentRow).alias('dc4'))
          |""".stripMargin
    }
  }
}
