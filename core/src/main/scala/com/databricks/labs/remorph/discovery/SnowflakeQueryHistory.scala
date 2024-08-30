package com.databricks.labs.remorph.discovery

import java.sql.Connection
import java.time.Duration
import scala.collection.mutable.ListBuffer

class SnowflakeQueryHistory(conn: Connection) {
  def history(): QueryHistory = {
    val stmt = conn.createStatement()
    try {
      val rs = stmt.executeQuery(s"""SELECT
           |  QUERY_TEXT,
           |  USER_NAME,
           |  WAREHOUSE_NAME,
           |  START_TIME,
           |  TOTAL_ELAPSED_TIME
           |FROM
           |  SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
           |WHERE
           |  START_TIME > CURRENT_DATE - 30
           |ORDER BY
           |  START_TIME
           |""".stripMargin)
      try {
        val queries = new ListBuffer[ExecutedQuery]()
        while (rs.next()) {
          queries.append(
            ExecutedQuery(
              rs.getTimestamp("START_TIME"),
              rs.getString("QUERY_TEXT"),
              Duration.ofMillis(rs.getLong("TOTAL_ELAPSED_TIME")),
              rs.getString("USER_NAME")))
        }
        QueryHistory(queries)
      } finally {
        rs.close()
      }
    } finally {
      stmt.close()
    }
  }
}
