package com.databricks.labs.remorph.integration

import com.databricks.labs.remorph.connections.{EnvGetter, SnowflakeConnectionFactory}
import com.databricks.labs.remorph.discovery.SnowflakeTableDefinitions
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeTableDefinitionTest extends AnyWordSpec with Matchers {
  "integration" should {
    "get table definitions for snowflake" in {
      val env = new EnvGetter
      val connFactory = new SnowflakeConnectionFactory(env)
      val conn = connFactory.newConnection()
      try {
        val snow = new SnowflakeTableDefinitions(conn)
        val rs = snow.getAllTableDefinitions
        rs should not be empty
      } finally {
        conn.close()
      }
    }
  }
}
