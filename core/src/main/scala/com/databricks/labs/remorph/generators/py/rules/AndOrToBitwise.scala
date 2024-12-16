package com.databricks.labs.remorph.generators.py.rules

import com.databricks.labs.remorph.{Transformation, TransformationConstructors, intermediate => ir}

// Converts `F.col('a') and F.col('b')` to `F.col('a') & F.col('b')`
class AndOrToBitwise extends ir.Rule[ir.Expression] with TransformationConstructors {
  override def apply(plan: ir.Expression): Transformation[ir.Expression] = ok(plan match {
    case ir.And(left, right) => ir.BitwiseAnd(left, right)
    case ir.Or(left, right) => ir.BitwiseOr(left, right)
    case _ => plan
  })
}
