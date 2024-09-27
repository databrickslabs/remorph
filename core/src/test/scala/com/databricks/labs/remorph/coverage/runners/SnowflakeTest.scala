package com.databricks.labs.remorph.coverage.runners

import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeTest extends AnyWordSpec with Matchers {
  "connectivity works" ignore {
    val env = new EnvGetter()
    val tsqlRunner = new SnowflakeRunner(env)
    val res = tsqlRunner.queryToCSV("SHOW DATABASES")
    res should include("REMORPH")
  }
}
