package com.databricks.labs.remorph.transpilers

import org.scalatest.wordspec.AnyWordSpec

class TsqlToDatabricksTranspilerTest extends AnyWordSpec with TranspilerTestCommon {

  protected final val transpiler = new TSqlToDatabricksTranspiler

  "The TSQL-to-Databricks transpiler" when {
    "transpiling set operations" should {
      val expectedTranslations = Map(
        "(SELECT a, b from c) UNION SELECT x, y FROM z" -> "(SELECT a, b from c) UNION (SELECT x, y from z);",
        "(SELECT a, b from c) UNION ALL SELECT x, y FROM z" -> "(SELECT a, b from c) UNION ALL (SELECT x, y from z);",
        "(SELECT a, b FROM c)" -> "SELECT a, b FROM c;")
      expectedTranslations.foreach { case (originalTSql, expectedDatabricksSql) =>
        s"correctly transpile: $originalTSql" in {
          originalTSql transpilesTo expectedDatabricksSql
        }
      }
    }
  }
}
