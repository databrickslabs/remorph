package com.databricks.labs.remorph.transpilers

import org.scalatest.wordspec.AnyWordSpec

class SnowflakeToDatabricksTranspilerTest extends AnyWordSpec with TranspilerTestCommon {

  protected val transpiler = new SnowflakeToDatabricksTranspiler

  "Snowflake non ansi join" should{

    "transpile non ansi join" in {
      "SELECT T1.d, T2.c FROM T1, T2 WHERE T1.x = T2.x(+)" transpilesTo
        s"""SELECT
           |  T1.d,
           |  T2.c
           |FROM
           |  T1
           |  LEFT JOIN T2
           |ON
           |  T1.x = T2.x;""".stripMargin
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

  }

}
