package com.databricks.labs.remorph.coverage.runners

import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlTest extends AnyWordSpec with Matchers {
  "connectivity works" ignore {
    val env = new EnvGetter()
    val tsqlRunner = new TSqlRunner(env)
    val res = tsqlRunner.queryToCSV("SELECT name, database_id, create_date FROM sys.databases")
    res should include("master")
  }
}
