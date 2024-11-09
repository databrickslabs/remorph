package com.databricks.labs.remorph.transpilers
import com.databricks.labs.remorph.{Generating, Optimizing}
import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.py.{LogicalPlanGenerator, Python}
import com.databricks.labs.remorph.intermediate.LogicalPlan

class SnowflakeToPySparkTranspiler extends SnowflakeToDatabricksTranspiler {
  val generator = new PySparkGenerator()

  override protected def generate(optimized: LogicalPlan): Python =
    update {
      case o: Optimizing =>
        Generating(
          optimizedPlan = optimized,
          currentNode = optimized,
          ctx = GeneratorContext(new LogicalPlanGenerator),
          previousPhase = Some(o))
      case _ =>
        Generating(optimizedPlan = optimized, currentNode = optimized, ctx = GeneratorContext(new LogicalPlanGenerator))
    }.flatMap(_ => generator.generate(optimized))
}
