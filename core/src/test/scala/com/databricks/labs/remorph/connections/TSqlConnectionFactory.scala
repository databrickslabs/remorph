package com.databricks.labs.remorph.connections

import java.sql.{Connection, DriverManager}

class TSqlConnectionFactory(env: EnvGetter) {

  Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver")
  private val jdbcUrl = env.get("TEST_TSQL_JDBC")
  private val username = env.get("TEST_TSQL_USER")
  private val password = env.get("TEST_TSQL_PASS")

  def newConnection(): Connection = DriverManager.getConnection(jdbcUrl, username, password)
}
