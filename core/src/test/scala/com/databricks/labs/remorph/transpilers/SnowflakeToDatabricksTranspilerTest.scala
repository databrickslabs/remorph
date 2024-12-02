package com.databricks.labs.remorph.transpilers

import org.scalatest.wordspec.AnyWordSpec

class SnowflakeToDatabricksTranspilerTest extends AnyWordSpec with TranspilerTestCommon {

  protected val transpiler = new SnowflakeToDatabricksTranspiler

  "transpile TO_NUMBER and TO_DECIMAL" should {
    "transpile TO_NUMBER" in {
      "select TO_NUMBER(EXPR) from test_tbl;" transpilesTo
        """SELECT CAST(EXPR AS DECIMAL(38, 0)) FROM test_tbl
          |  ;""".stripMargin
    }

    "transpile TO_NUMBER with precision and scale" in {
      "select TO_NUMBER(EXPR,38,0) from test_tbl;" transpilesTo
        """SELECT CAST(EXPR AS DECIMAL(38, 0)) FROM test_tbl
          |  ;""".stripMargin
    }

    "transpile TO_DECIMAL" in {
      "select TO_DECIMAL(EXPR) from test_tbl;" transpilesTo
        """SELECT CAST(EXPR AS DECIMAL(38, 0)) FROM test_tbl
          |  ;""".stripMargin
    }
  }

  "snowsql commands" should {

    "transpile BANG with semicolon" in {
      "!set error_flag = true;" transpilesTo
        """/* The following issues were detected:
          |
          |   Unknown command in SnowflakeAstBuilder.visitSnowSqlCommand
          |    !set error_flag = true;
          | */""".stripMargin
    }
    "transpile BANG without semicolon" in {
      "!print Include This Text" transpilesTo
        """/* The following issues were detected:
        |
        |   Unknown command in SnowflakeAstBuilder.visitSnowSqlCommand
        |    !print Include This Text
        | */""".stripMargin
    }
    "transpile BANG with options" in {
      "!options catch=true" transpilesTo
        """/* The following issues were detected:
          |
          |   Unknown command in SnowflakeAstBuilder.visitSnowSqlCommand
          |    !options catch=true
          | */""".stripMargin
    }
    "transpile BANG with negative scenario unknown command" in {
      "!test unknown command".failsTranspilation
    }
    "transpile BANG with negative scenario unknown command2" in {
      "!abc set=abc".failsTranspilation
    }
  }

  "Snowflake Alter commands" should {

    "ALTER TABLE t1 ADD COLUMN c1 INTEGER" in {
      "ALTER TABLE t1 ADD COLUMN c1 INTEGER;" transpilesTo (
        s"""ALTER TABLE
           |  t1
           |ADD
           |  COLUMN c1 DECIMAL(38, 0);""".stripMargin
      )
    }

    "ALTER TABLE t1 ADD COLUMN c1 INTEGER, c2 VARCHAR;" in {
      "ALTER TABLE t1 ADD COLUMN c1 INTEGER, c2 VARCHAR;" transpilesTo
        s"""ALTER TABLE
           |  t1
           |ADD
           |  COLUMN c1 DECIMAL(38, 0),
           |  c2 STRING;""".stripMargin
    }

    "ALTER TABLE t1 DROP COLUMN c1;" in {
      "ALTER TABLE t1 DROP COLUMN c1;" transpilesTo (
        s"""ALTER TABLE
           |  t1 DROP COLUMN c1;""".stripMargin
      )
    }

    "ALTER TABLE t1 DROP COLUMN c1, c2;" in {
      "ALTER TABLE t1 DROP COLUMN c1, c2;" transpilesTo
        s"""ALTER TABLE
           |  t1 DROP COLUMN c1,
           |  c2;""".stripMargin
    }

    "ALTER TABLE t1 RENAME COLUMN c1 to c2;" in {
      "ALTER TABLE t1 RENAME COLUMN c1 to c2;" transpilesTo
        s"""ALTER TABLE
           |  t1 RENAME COLUMN c1 to c2;""".stripMargin
    }

    "ALTER TABLE s.t1 DROP CONSTRAINT pk" in {
      "ALTER TABLE s.t1 DROP CONSTRAINT pk;" transpilesTo
        s"""ALTER TABLE
           |  s.t1 DROP CONSTRAINT pk;""".stripMargin
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

      "SELECT t1.c2 FROM t1 LEFT JOIN t2 USING (c2);" transpilesTo
        s"""SELECT
           |  t1.c2
           |FROM
           |  t1
           |  LEFT JOIN t2
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

    "transpile select distinct query" in {
      s"""SELECT DISTINCT c1, c2 FROM T1""".stripMargin transpilesTo
        s"""SELECT
           |  DISTINCT c1,
           |  c2
           |FROM
           |  T1;""".stripMargin
    }

    "transpile window functions" in {
      s"""SELECT LAST_VALUE(c1)
        |IGNORE NULLS OVER (PARTITION BY t1.c2 ORDER BY t1.c3 DESC
        |RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS dc4
        |FROM t1;""".stripMargin transpilesTo
        s"""SELECT
           |  LAST(c1) IGNORE NULLS OVER (
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

    "transpile MONTHS_BETWEEN function" in {
      "SELECT MONTHS_BETWEEN('2021-02-01'::DATE, '2021-01-01'::DATE);" transpilesTo
        """SELECT
           |  MONTHS_BETWEEN(CAST('2021-02-01' AS DATE), CAST('2021-01-01' AS DATE), TRUE)
           |  ;""".stripMargin

      """SELECT
        | MONTHS_BETWEEN('2019-03-01 02:00:00'::TIMESTAMP, '2019-02-15 01:00:00'::TIMESTAMP)
        | AS mb;""".stripMargin transpilesTo
        """SELECT
           |  MONTHS_BETWEEN(CAST('2019-03-01 02:00:00' AS TIMESTAMP), CAST('2019-02-15 01:00:00'
           |  AS TIMESTAMP), TRUE) AS mb
           |  ;""".stripMargin
    }

    "transpile ARRAY_REMOVE function" in {
      "SELECT ARRAY_REMOVE([1, 2, 3], 1);" transpilesTo
        "SELECT ARRAY_REMOVE(ARRAY(1, 2, 3), 1);"

      "SELECT ARRAY_REMOVE([2, 3, 4.11::DOUBLE, 4, NULL], 4);" transpilesTo
        "SELECT ARRAY_REMOVE(ARRAY(2, 3, CAST(4.11 AS DOUBLE), 4, NULL), 4);"

      // TODO - Enable this test case once the VARIANT casting is implemented.
      // In Snow, if the value to remove is a VARCHAR,
      // it is required to cast the value to VARIANT.
      // "SELECT ARRAY_REMOVE(['a', 'b', 'c'], 'a'::VARIANT);" transpilesTo
      // "SELECT ARRAY_REMOVE(ARRAY('a', 'b', 'c'), 'a');"
    }
    "transpile ARRAY_SORT function" in {
      "SELECT ARRAY_SORT([0, 2, 4, NULL, 5, NULL], TRUE, True);" transpilesTo
        """SELECT
          |  SORT_ARRAY(ARRAY(0, 2, 4, NULL, 5, NULL))
          |  ;""".stripMargin

      "SELECT ARRAY_SORT([0, 2, 4, NULL, 5, NULL], FALSE, False);" transpilesTo
        """SELECT
          |  SORT_ARRAY(ARRAY(0, 2, 4, NULL, 5, NULL), false)
          |  ;""".stripMargin

      "SELECT ARRAY_SORT([0, 2, 4, NULL, 5, NULL], TRUE, FALSE);" transpilesTo
        """SELECT
          |  ARRAY_SORT(
          |    ARRAY(0, 2, 4, NULL, 5, NULL),
          |    (left, right) -> CASE
          |      WHEN left IS NULL
          |      AND right IS NULL THEN 0
          |      WHEN left IS NULL THEN 1
          |      WHEN right IS NULL THEN -1
          |      WHEN left < right THEN -1
          |      WHEN left > right THEN 1
          |      ELSE 0
          |    END
          |  )
          |  ;""".stripMargin

      "SELECT ARRAY_SORT([0, 2, 4, NULL, 5, NULL], False, true);" transpilesTo
        """SELECT
          |  ARRAY_SORT(
          |    ARRAY(0, 2, 4, NULL, 5, NULL),
          |    (left, right) -> CASE
          |      WHEN left IS NULL
          |      AND right IS NULL THEN 0
          |      WHEN left IS NULL THEN -1
          |      WHEN right IS NULL THEN 1
          |      WHEN left < right THEN 1
          |      WHEN left > right THEN -1
          |      ELSE 0
          |    END
          |  )
          |  ;""".stripMargin

      "SELECT ARRAY_SORT([0, 2, 4, NULL, 5, NULL], TRUE, 1 = 1);".failsTranspilation
      "SELECT ARRAY_SORT([0, 2, 4, NULL, 5, NULL], 1 = 1, TRUE);".failsTranspilation
    }

    "GROUP BY ALL" in {
      "SELECT car_model, COUNT(DISTINCT city) FROM dealer GROUP BY ALL;" transpilesTo
        "SELECT car_model, COUNT(DISTINCT city) FROM dealer GROUP BY ALL;"
    }

  }

  "Snowflake transpile function with optional brackets" should {

    "SELECT CURRENT_DATE, CURRENT_TIMESTAMP, CURRENT_TIME, LOCALTIME, LOCALTIMESTAMP FROM t1" in {
      s"""SELECT CURRENT_DATE, CURRENT_TIMESTAMP, CURRENT_TIME,
         |LOCALTIME, LOCALTIMESTAMP FROM t1""".stripMargin transpilesTo (
        s"""SELECT
           |  CURRENT_DATE(),
           |  CURRENT_TIMESTAMP(),
           |  DATE_FORMAT(CURRENT_TIMESTAMP(), 'HH:mm:ss'),
           |  DATE_FORMAT(CURRENT_TIMESTAMP(), 'HH:mm:ss'),
           |  CURRENT_TIMESTAMP()
           |FROM
           |  t1;""".stripMargin
      )
    }

    "SELECT CURRENT_TIMESTAMP(1) FROM t1 where dt < CURRENT_TIMESTAMP" in {
      s"""SELECT CURRENT_TIMESTAMP(1) FROM t1 where dt < CURRENT_TIMESTAMP""".stripMargin transpilesTo (
        s"""SELECT
           |  DATE_FORMAT(CURRENT_TIMESTAMP(), 'yyyy-MM-dd HH:mm:ss.SSS')
           |FROM
           |  t1
           |WHERE
           |  dt < CURRENT_TIMESTAMP();""".stripMargin
      )
    }

    "SELECT CURRENT_TIME(1) FROM t1 where dt < CURRENT_TIMESTAMP()" in {
      s"""SELECT CURRENT_TIME(1) FROM t1 where dt < CURRENT_TIMESTAMP()""".stripMargin transpilesTo (
        s"""SELECT
           |  DATE_FORMAT(CURRENT_TIMESTAMP(), 'HH:mm:ss')
           |FROM
           |  t1
           |WHERE
           |  dt < CURRENT_TIMESTAMP();""".stripMargin
      )
    }

    "SELECT LOCALTIME() FROM t1 where dt < LOCALTIMESTAMP" in {
      s"""SELECT LOCALTIME() FROM t1 where dt < LOCALTIMESTAMP()""".stripMargin transpilesTo (
        s"""SELECT
           |  DATE_FORMAT(CURRENT_TIMESTAMP(), 'HH:mm:ss')
           |FROM
           |  t1
           |WHERE
           |  dt < CURRENT_TIMESTAMP();""".stripMargin
      )
    }
  }

  "Snowflake Execute commands" should {

    "EXECUTE TASK task1;" in {
      "EXECUTE TASK task1;" transpilesTo
        """/* The following issues were detected:
          |
          |   Execute Task is not yet supported
          |    EXECUTE TASK task1
          | */""".stripMargin
    }
  }

  "Snowflake MERGE commands" should {

    "MERGE;" in {
      """MERGE INTO target_table AS t
        |USING source_table AS s
        |ON t.id = s.id
        |WHEN MATCHED AND s.status = 'active' THEN
        |  UPDATE SET t.value = s.value AND status = 'active'
        |WHEN MATCHED AND s.status = 'inactive' THEN
        |  DELETE
        |WHEN NOT MATCHED THEN
        |  INSERT (id, value, status) VALUES (s.id, s.value, s.status);""".stripMargin transpilesTo
        s"""MERGE INTO target_table AS t
           |USING source_table AS s
           |ON t.id = s.id
           |WHEN MATCHED AND s.status = 'active' THEN
           |  UPDATE SET t.value = s.value AND status = 'active'
           |WHEN MATCHED AND s.status = 'inactive' THEN
           |  DELETE
           |WHEN NOT MATCHED THEN
           |  INSERT (id, value, status) VALUES (s.id, s.value, s.status);""".stripMargin
    }
  }

  "Expressions in CTE" in {
    """WITH
      |    a AS (1),
      |    b AS (2),
      |    t (d, e) AS (SELECT 4, 5),
      |    c AS (3)
      |SELECT
      |    a + b,
      |    a * c,
      |    a * t.d
      |FROM t;""".stripMargin transpilesTo
      """WITH
        |    t (d, e) AS (SELECT 4, 5)
        |SELECT
        |    1 + 2,
        |    1 * 3,
        |    1 * t.d
        |FROM
        |    t;""".stripMargin
  }

  "Batch statements" should {
    "survive invalid SQL" in {
      """
        |CREATE TABLE t1 (x VARCHAR);
        |SELECT x y z;
        |SELECT 3 FROM t3;
        |""".stripMargin transpilesTo ("""
        |CREATE TABLE t1 (x STRING);
        |/* The following issues were detected:
        |
        |   Unparsed input - ErrorNode encountered
        |    Unparsable text: SELECTxyz
        | */
        |/* The following issues were detected:
        |
        |   Unparsed input - ErrorNode encountered
        |    Unparsable text: SELECT
        |    Unparsable text: x
        |    Unparsable text: y
        |    Unparsable text: z
        |    Unparsable text: parser recovered by ignoring: SELECTxyz;
        | */
        | SELECT
        |  3
        |FROM
        |  t3;""".stripMargin, false)

    }
  }

}
