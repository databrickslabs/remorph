package com.databricks.labs.remorph.transpilers
import com.databricks.labs.remorph.generators.py.Python
import com.databricks.labs.remorph.intermediate.LogicalPlan

class SnowflakeToPySparkTranspiler extends SnowflakeToDatabricksTranspiler {
  val generator = new PySparkGenerator()

  override protected def generate(optimized: LogicalPlan): Python = generator.generate(optimized)
}
