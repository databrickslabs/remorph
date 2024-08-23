package com.databricks.labs.remorph.transpilers

import org.scalatest.wordspec.AnyWordSpec

class SnowflakeToDatabricksTranspilerTest extends AnyWordSpec with TranspilerTestCommon {

  protected val transpiler = new SnowflakeToDatabricksTranspiler

  "snowsql commands" should {

    "transpile BANG" in {
      "!set error_flag = true" transpilesTo "--!set error_flag = true;"
      "!define tablename=CENUSTRACKONE" transpilesTo "--!define tablename=CENUSTRACKONE;"
      "!print Include This Text" transpilesTo "--!print Include This Text;"
      "!abort 77589bd1" transpilesTo "--!abort 77589bd1;"
    }

  }

  "Snowflake transpiler" should {

    "transpile queries" in {

      "SELECT * FROM t1 WHERE  col1 != 100;" transpilesTo (
        s"""SELECT
           |  *
           |FROM
           |  t1
           |WHERE
           |  col1 != 100;""".stripMargin
      )

      "SELECT * FROM t1;" transpilesTo
        s"""SELECT
           |  *
           |FROM
           |  t1;""".stripMargin

      "SELECT t1.* FROM t1 INNER JOIN t2 ON t2.c2 = t2.c1;" transpilesTo
        s"""SELECT
           |  t1.*
           |FROM
           |  t1
           |  INNER JOIN t2 ON t2.c2 = t2.c1;""".stripMargin

      "SELECT t1.c2 FROM t1 LEFT OUTER JOIN t2 USING (c2);" transpilesTo
        s"""SELECT
           |  t1.c2
           |FROM
           |  t1
           |  LEFT OUTER JOIN t2
           |USING
           |  (c2);""".stripMargin

      "SELECT c1::DOUBLE FROM t1;" transpilesTo
        s"""SELECT
           |  CAST(c1 AS DOUBLE)
           |FROM
           |  t1;""".stripMargin

      "SELECT JSON_EXTRACT_PATH_TEXT(json_data, path_col) FROM demo1;" transpilesTo
        """SELECT
           |  GET_JSON_OBJECT(json_data, CONCAT('$.', path_col))
           |FROM
           |  demo1;""".stripMargin
    }

    "transpile window functions" in {
      s"""SELECT LAST_VALUE(c1)
        |IGNORE NULLS OVER (PARTITION BY t1.c2 ORDER BY t1.c3 DESC
        |RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS dc4
        |FROM t1;""".stripMargin transpilesTo
        s"""SELECT
           |  LAST_VALUE(c1) IGNORE NULLS OVER (
           |    PARTITION BY
           |      t1.c2
           |    ORDER BY
           |      t1.c3 DESC NULLS FIRST
           |    RANGE
           |      BETWEEN UNBOUNDED PRECEDING
           |      AND CURRENT ROW
           |  ) AS dc4
           |FROM
           |  t1;""".stripMargin
    }

  }

}
