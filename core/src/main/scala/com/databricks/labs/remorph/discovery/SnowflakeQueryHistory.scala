package com.databricks.labs.remorph.discovery

import java.sql.Connection
import java.time.Duration
import scala.collection.mutable.ListBuffer

class SnowflakeQueryHistory(conn: Connection) extends QueryHistoryProvider {
  def history(): QueryHistory = {
    val stmt = conn.createStatement()
    try {
      val rs = stmt.executeQuery(s"""SELECT
           |  QUERY_HASH,
           |  QUERY_TEXT,
           |  USER_NAME,
           |  WAREHOUSE_NAME,
           |  START_TIME,
           |  TOTAL_ELAPSED_TIME
           |FROM
           |  SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
           |WHERE
           |    START_TIME > CURRENT_DATE - 30
           |  AND
           |    QUERY_TEXT != ''  -- Many system queries are empty
           |  AND
           |    QUERY_TEXT != '<redacted>' -- Certain queries are completely redacted
           |  AND
           |    QUERY_TEXT IS NOT NULL
           |ORDER BY
           |  START_TIME
           |""".stripMargin)
      try {
        val queries = new ListBuffer[ExecutedQuery]()
        while (rs.next()) {
          queries.append(
            ExecutedQuery(
              id = rs.getString("QUERY_HASH"),
              source = rs.getString("QUERY_TEXT"),
              timestamp = rs.getTimestamp("START_TIME"),
              duration = Duration.ofMillis(rs.getLong("TOTAL_ELAPSED_TIME")),
              user = Some(rs.getString("USER_NAME")),
              filename = None))
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
