package com.databricks.labs.remorph.transpilers
import com.databricks.labs.remorph.Result
import com.databricks.labs.remorph.intermediate.LogicalPlan

class SnowflakeToPySparkTranspiler extends SnowflakeToDatabricksTranspiler {
  val generator = new PySparkGenerator()

  override protected def generate(optimized: LogicalPlan): Result[String] = generator.generate(optimized)
}
