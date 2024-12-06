package com.databricks.labs.remorph.connections

import java.sql.{Connection, DriverManager}

class TSqlConnectionFactory(env: EnvGetter) {

  Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver")
  private[this] val jdbcUrl = env.get("TEST_TSQL_JDBC")
  private[this] val username = env.get("TEST_TSQL_USER")
  private[this] val password = env.get("TEST_TSQL_PASS")

  def newConnection(): Connection = DriverManager.getConnection(jdbcUrl, username, password)
}
