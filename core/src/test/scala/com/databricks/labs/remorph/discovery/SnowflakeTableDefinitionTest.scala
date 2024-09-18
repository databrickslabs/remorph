package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.connections.{EnvGetter, SnowflakeConnectionFactory}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

import java.sql.Connection
class SnowflakeTableDefinitionTest extends AnyWordSpec with Matchers {
  "Snowflake Table Definition Test" should {
    "work in happy path" in {
      val env = new EnvGetter
      val connFactory = new SnowflakeConnectionFactory(env)
      var conn: Connection = null
      try {
        conn = connFactory.newConnection()
        val snow = new SnowflakeTableDefinition(conn)
        snow.getTableDefinitions("SNOWFLAKE")
      } catch {
        case e: Exception => e.printStackTrace()
      } finally {
        if (conn != null) conn.close()
      }

    }
  }
}
