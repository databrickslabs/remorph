package com.databricks.labs.remorph.integration

import com.databricks.labs.remorph.connections.{EnvGetter, TSqlConnectionFactory}
import com.databricks.labs.remorph.discovery.TSqlTableDefinitions
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlTableDefinationTest extends AnyWordSpec with Matchers {
  "integration" should {
    "get table definitions for TSql" in {
      val conn = new TSqlConnectionFactory(new EnvGetter).newConnection()
      try {
        val sqlTD = new TSqlTableDefinitions(conn)
        val rs = sqlTD.getAllTableDefinitions
        rs should not be empty
      } finally {
        conn.close()
      }
    }

    "get all catalog for TSql" in {
      val conn = new TSqlConnectionFactory(new EnvGetter).newConnection()
      try {
        val sqlTD = new TSqlTableDefinitions(conn)
        val rs = sqlTD.getAllCatalogs
        rs should not be empty
      } finally {
        conn.close()
      }
    }

  }
}