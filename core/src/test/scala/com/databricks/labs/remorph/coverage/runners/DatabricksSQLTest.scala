package com.databricks.labs.remorph.coverage.runners

import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class DatabricksSQLTest extends AnyWordSpec with Matchers {
  "connectivity works" ignore {
    val env = new EnvGetter()
    val databricksSQL = new DatabricksSQL(env)
    databricksSQL.spark should not be null
  }
}
