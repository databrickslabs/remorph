package com.databricks.labs.remorph.transpilers

import org.scalatest.wordspec.AnyWordSpec

class TsqlToDatabricksTranspilerTest extends AnyWordSpec with TranspilerTestCommon with SetOperationBehaviors {

  protected final val transpiler = new TSqlToDatabricksTranspiler

  "The TSQL-to-Databricks transpiler" when {
    "transpiling set operations" should {
      behave like setOperationsAreTranspiled()
    }
    "mixing CTEs with set operations" should {
      correctlyTranspile(
        """WITH cte1 AS (SELECT a, b FROM c),
          |     cte2 AS (SELECT x, y FROM z)
          |SELECT a, b FROM cte1 UNION SELECT x, y FROM cte2""".stripMargin ->
          """WITH cte1 AS (SELECT a, b FROM c),
            |     cte2 AS (SELECT x, y FROM z)
            |(SELECT a, b FROM cte1) UNION (SELECT x, y FROM cte2);""".stripMargin)
    }
    "transpiling order-by clauses" should {
      val expectedOrderByTranslations: Map[String, String] = Map(
        "SELECT a, b FROM c ORDER BY a, b" -> "SELECT a, b FROM c ORDER BY a, b;",
        "SELECT a, b FROM c ORDER BY 1, 2" -> "SELECT a, b FROM c ORDER BY 1, 2;",
        "SELECT a, b FROM c ORDER BY a OFFSET 1 ROW" -> "SELECT a, b FROM c ORDER BY a OFFSET 1;",
        "SELECT a, b FROM c ORDER BY a OFFSET 10 ROWS" -> "SELECT a, b FROM c ORDER BY a OFFSET 10;",
        "SELECT a, b FROM c ORDER BY a OFFSET 0 ROWS FETCH FIRST 10 ROWS ONLY" ->
          "SELECT a, b FROM c ORDER BY a LIMIT 10 OFFSET 0;",
        "SELECT a, b FROM c ORDER BY a OFFSET 10 ROWS FETCH NEXT 1 ROW ONLY" ->
          "SELECT a, b FROM c ORDER BY a LIMIT 1 OFFSET 10;")
      expectedOrderByTranslations.foreach(correctlyTranspile)
    }
  }
}
