package com.databricks.labs.remorph.transpilers

import org.scalatest.wordspec.AnyWordSpec

class TsqlToDatabricksTranspilerTest extends AnyWordSpec with TranspilerTestCommon {

  protected final val transpiler = new TSqlToDatabricksTranspiler

  "The TSQL-to-Databricks transpiler" when {
    "transpiling set operations" should {
      val expectedTranslations = Map(
        "SELECT a, b FROM c UNION SELECT x, y FROM z" -> "(SELECT a, b FROM c) UNION (SELECT x, y FROM z);",
        "SELECT a, b FROM c UNION ALL SELECT x, y FROM z" -> "(SELECT a, b FROM c) UNION ALL (SELECT x, y FROM z);",
        "SELECT a, b FROM c EXCEPT SELECT x, y FROM z" -> "(SELECT a, b FROM c) EXCEPT (SELECT x, y FROM z);",
        "SELECT a, b FROM c INTERSECT SELECT x, y FROM z" -> "(SELECT a, b FROM c) INTERSECT (SELECT x, y FROM z);",
        "SELECT a, b FROM c UNION (SELECT x, y FROM z)" -> "(SELECT a, b FROM c) UNION (SELECT x, y FROM z);",
        "(SELECT a, b FROM c) UNION SELECT x, y FROM z" -> "(SELECT a, b FROM c) UNION (SELECT x, y FROM z);",
        "(SELECT a, b FROM c) UNION ALL SELECT x, y FROM z" -> "(SELECT a, b FROM c) UNION ALL (SELECT x, y FROM z);",
        "(SELECT a, b FROM c)" -> "SELECT a, b FROM c;",
        """SELECT a, b FROM c
          |UNION
          |SELECT d, e FROM f
          |UNION ALL
          |SELECT g, h FROM i
          |INTERSECT
          |SELECT j, k FROM l
          |EXCEPT
          |SELECT m, n FROM o""".stripMargin ->
          """(((SELECT a, b FROM c)
            |  UNION
            |  (SELECT d, e FROM f))
            | UNION ALL
            | (SELECT g, h FROM i))
            |INTERSECT
            | ((SELECT j, k FROM l)
            |  EXCEPT
            |  (SELECT m, n FROM o));""".stripMargin)
      expectedTranslations.foreach { case (originalTSql, expectedDatabricksSql) =>
        s"correctly transpile: $originalTSql" in {
          originalTSql transpilesTo expectedDatabricksSql
        }
      }
    }
  }
}
