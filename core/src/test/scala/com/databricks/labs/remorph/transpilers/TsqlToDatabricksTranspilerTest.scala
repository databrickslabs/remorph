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
  }
}
