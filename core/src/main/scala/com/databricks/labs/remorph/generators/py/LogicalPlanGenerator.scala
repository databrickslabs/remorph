package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.generators.CodeInterpolator
import com.databricks.labs.remorph.{intermediate => ir}

class LogicalPlanGenerator extends BasePythonGenerator[ir.LogicalPlan] {
  // TODO: see if com.databricks.labs.remorph.generators.GeneratorContext.logical is still needed
  override def generate(tree: ir.LogicalPlan): Python = code"..."
}
