package com.databricks.labs.remorph

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.intermediate.{LogicalPlan, TreeNode}
import org.antlr.v4.runtime.ParserRuleContext

sealed trait Phase {
  def previousPhase: Option[Phase]
}

case object Init extends Phase {
  override val previousPhase: Option[Phase] = None
}

case class Parsing(source: String, filename: String = "-- test source --") extends Phase {
  override val previousPhase: Option[Phase] = Some(Init)
}

case class BuildingAst(tree: ParserRuleContext, previousPhase: Option[Parsing] = None) extends Phase

case class Optimizing(unoptimizedPlan: LogicalPlan, previousPhase: Option[BuildingAst] = None) extends Phase

case class Generating(
    optimizedPlan: LogicalPlan,
    currentNode: TreeNode[_],
    totalStatements: Int = 0,
    transpiledStatements: Int = 0,
    ctx: GeneratorContext,
    previousPhase: Option[Optimizing] = None)
    extends Phase

case class TBA() extends Phase {
  override val previousPhase: Option[Phase] = None
}