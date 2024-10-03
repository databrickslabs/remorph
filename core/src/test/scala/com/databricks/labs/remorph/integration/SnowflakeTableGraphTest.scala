package com.databricks.labs.remorph.integration

import com.databricks.labs.remorph.connections.{EnvGetter, SnowflakeConnectionFactory}
import com.databricks.labs.remorph.discovery.{SnowflakeQueryHistory, SnowflakeTableDefinitions}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakePlanParser
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import com.databricks.labs.remorph.graph.TableGraph

class SnowflakeTableGraphTest extends AnyWordSpec with Matchers {
  "TableGraph" should {
    "retrieve downstream tables correctly" ignore {
      val env = new EnvGetter
      val connFactory = new SnowflakeConnectionFactory(env)
      val conn = connFactory.newConnection()
      val snow = new SnowflakeQueryHistory(conn)
      val history = snow.history()
      val parser = new SnowflakePlanParser()
      val tableDefinition = new SnowflakeTableDefinitions(conn).getAllTableDefinitions

      val tableGraph = new TableGraph(parser)
      tableGraph.buildDependency(history, tableDefinition.toSet)
      // TODO Currently there is not enough example in query history for the integration test to work.
      assert(tableGraph.getRootTables().isEmpty)
    }
  }
}
