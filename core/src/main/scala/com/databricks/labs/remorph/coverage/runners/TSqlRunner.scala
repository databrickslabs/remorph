package com.databricks.labs.remorph.coverage.runners

import java.sql.DriverManager

class TSqlRunner(env: EnvGetter) {
  // scalastyle:off
  Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver")
  // scalastyle:on

  private val url = env.get("TEST_TSQL_JDBC")
  private val user = env.get("TEST_TSQL_USER")
  private val pass = env.get("TEST_TSQL_PASS")
  private val connection = DriverManager.getConnection(url, user, pass)
  private val dumper = new CsvDumper(connection)

  def queryToCSV(query: String): String = dumper.queryToCSV(query)

  def close() {
    connection.close()
  }
}
