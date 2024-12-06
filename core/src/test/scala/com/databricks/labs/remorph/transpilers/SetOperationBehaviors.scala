package com.databricks.labs.remorph.transpilers

import org.scalatest.wordspec.AnyWordSpec

trait SetOperationBehaviors { this: TranspilerTestCommon with AnyWordSpec =>

  protected[this] final def correctlyTranspile(expectedTranspilation: (String, String)): Unit = {
    val (originalTSql, expectedDatabricksSql) = expectedTranspilation
    s"correctly transpile: $originalTSql" in {
      originalTSql transpilesTo expectedDatabricksSql
    }
  }

  protected[this] val expectedSetOperationTranslations: Map[String, String] = Map(
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
        | ((SELECT g, h FROM i)
        |  INTERSECT
        |  (SELECT j, k FROM l)))
        |EXCEPT
        |(SELECT m, n FROM o);""".stripMargin)


  def setOperationsAreTranspiled(): Unit = {
    expectedSetOperationTranslations.foreach(correctlyTranspile)
  }
}
