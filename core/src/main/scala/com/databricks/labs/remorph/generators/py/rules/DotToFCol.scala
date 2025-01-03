package com.databricks.labs.remorph.generators.py.rules

import com.databricks.labs.remorph.{Transformation, TransformationConstructors}
import com.databricks.labs.remorph.intermediate._

class DotToFCol extends Rule[Expression] with PyCommon with TransformationConstructors {
  override def apply(plan: Expression): Transformation[Expression] = plan transformUp {
    case Dot(Id(left, _), Id(right, _)) =>
      ok(F("col", StringLiteral(s"$left.$right") :: Nil))
  }
}
