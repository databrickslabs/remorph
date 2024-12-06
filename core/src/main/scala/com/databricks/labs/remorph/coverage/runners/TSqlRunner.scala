package com.databricks.labs.remorph.coverage.runners

import java.sql.DriverManager

class TSqlRunner(env: EnvGetter) {
  // scalastyle:off
  Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver")
  // scalastyle:on

  private[this] val url = env.get("TEST_TSQL_JDBC")
  private[this] val user = env.get("TEST_TSQL_USER")
  private[this] val pass = env.get("TEST_TSQL_PASS")
  private[this] val connection = DriverManager.getConnection(url, user, pass)
  private[this] val dumper = new CsvDumper(connection)

  def queryToCSV(query: String): String = dumper.queryToCSV(query)

  def close() {
    connection.close()
  }
}
