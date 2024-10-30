package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.{intermediate => ir}

class LogicalPlanGenerator extends BasePythonGenerator[ir.LogicalPlan] {
  // TODO: see if com.databricks.labs.remorph.generators.GeneratorContext.logical is still needed
  override def generate(ctx: GeneratorContext, tree: ir.LogicalPlan): Python = py"..."
}
