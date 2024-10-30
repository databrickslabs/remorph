package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.{KoResult, OkResult, PartialResult}
import com.databricks.labs.remorph.generators.py.RuffFormatter
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeToPySparkTranspilerTest extends AnyWordSpec with TranspilerTestCommon {
  protected val transpiler = new SnowflakeToPySparkTranspiler
  private val formatter = new RuffFormatter
  override def format(input: String): String = formatter.format(input) match {
    case OkResult(formatted) => formatted
    case KoResult(_, error) => fail(error.msg)
    case PartialResult(output, error) => fail(s"Partial result: $output, error: $error")
  }

  "Snowflake SQL" should {
    "transpile window functions" in {
      s"""SELECT LAST_VALUE(c1)
         |IGNORE NULLS OVER (PARTITION BY t1.c2 ORDER BY t1.c3 DESC
         |RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS dc4
         |FROM t1;""".stripMargin transpilesTo
        """import pyspark.sql.functions as F
          |from pyspark.sql.window import Window
          |
          |spark.table("t1").select(
          |    F.last(F.col("c1"))
          |    .over(
          |        Window.partitionBy(F.col("t1.c2"))
          |        .orderBy(F.col("t1.c3").desc_nulls_first())
          |        .rangeBetween(Window.unboundedPreceding, Window.currentRow)
          |    )
          |    .alias("dc4")
          |)
          |""".stripMargin
    }
  }
}
