package com.databricks.labs.remorph.support.tsql

import com.databricks.labs.remorph.coverage.runners.EnvGetter
import com.databricks.labs.remorph.support.ConnectionFactory

import java.sql.{Connection, DriverManager}

class SqlServerConnectionFactory(env: EnvGetter) extends ConnectionFactory {
  // scalastyle:off
  Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver")
  // scalastyle:on

  private val url = env.get("TEST_TSQL_JDBC")
  private val user = env.get("TEST_TSQL_USER")
  private val pass = env.get("TEST_TSQL_PASS")

  override def newConnection(): Connection = DriverManager.getConnection(url, user, pass)
}
