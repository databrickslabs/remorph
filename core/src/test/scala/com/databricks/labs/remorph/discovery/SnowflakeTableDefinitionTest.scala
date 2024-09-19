package com.databricks.labs.remorph.discovery

import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import java.sql.Connection

import com.databricks.labs.remorph.connections.{EnvGetter, SnowflakeConnectionFactory}

class SnowflakeTableDefinitionTest extends AnyWordSpec with Matchers {
  private val env = new EnvGetter
  private val connFactory = new SnowflakeConnectionFactory(env)

  "Snowflake Table Definition Test" should {
    "Test table definition" in {
      withConnection { conn =>
        val snowflakeDefinitions = new SnowflakeTableDefinitions(conn)
        val tableDefinitions = snowflakeDefinitions.getTableDefinitions("REMORPH")
        tableDefinitions should not be empty
      }
    }

    "Test list catalog" in {
      withConnection { conn =>
        val snowflakeDefinitions = new SnowflakeTableDefinitions(conn)
        val catalogs = snowflakeDefinitions.getAllCatalogs
        catalogs should not be empty
      }
    }
  }

  private def withConnection[T](f: Connection => T): T = {
    var conn: Connection = null
    try {
      conn = connFactory.newConnection()
      f(conn)
    } catch {
      case e: Exception =>
        fail(s"Failed to execute database operation: ${e.getMessage}")
    } finally {
      if (conn != null) {
          conn.close()
        }
      }
    }
}