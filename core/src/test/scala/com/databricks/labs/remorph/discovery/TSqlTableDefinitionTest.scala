package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.connections.{EnvGetter, TSqlConnectionFactory}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec


class TSqlTableDefinitionTest extends AnyWordSpec with Matchers {
  "integration" should {
    "work in happy path" in {

      val TSqlConnectionFactory = new TSqlConnectionFactory(new EnvGetter)
      val conn = TSqlConnectionFactory.newConnection()
      val tsqlTD = new TSqlTableDefinitions(conn)
      val rs = tsqlTD.getAllTableDefinitions
      println(rs)


    }
  }
}