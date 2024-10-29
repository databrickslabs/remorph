package com.databricks.labs.remorph.generators.py.rules

import com.databricks.labs.remorph.intermediate._

class DotToFCol extends Rule[Expression] with PyCommon {
  override def apply(plan: Expression): Expression = plan transformUp { case Dot(Id(left, _), Id(right, _)) =>
    F("col", StringLiteral(s"$left.$right") :: Nil)
  }
}
