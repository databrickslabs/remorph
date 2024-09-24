package com.databricks.labs.remorph.integration

import com.databricks.labs.remorph.connections.{EnvGetter, SnowflakeConnectionFactory}
import com.databricks.labs.remorph.discovery.SnowflakeQueryHistory
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeQueryHistoryTest extends AnyWordSpec with Matchers {
  "integration" should {
    "work in happy path" ignore {
      val env = new EnvGetter
      val connFactory = new SnowflakeConnectionFactory(env)
      val conn = connFactory.newConnection() // TODO: wrap with closing logic
      val snow = new SnowflakeQueryHistory(conn)
      val history = snow.history()
      assert(history.queries.nonEmpty)
    }
  }
}
