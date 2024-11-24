package com.databricks.labs.remorph

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.intermediate.{LogicalPlan, RemorphError, TreeNode}
import org.antlr.v4.runtime.ParserRuleContext

sealed trait Phase {
  def previousPhase: Option[Phase]
  def recordError(error: RemorphError): Phase
}

case object Init extends Phase {
  override val previousPhase: Option[Phase] = None

  override def recordError(error: RemorphError): Init.type = this
}

case class Parsing(
    source: String,
    filename: String = "-- test source --",
    encounteredErrors: Seq[RemorphError] = Seq.empty)
    extends Phase {
  override val previousPhase: Option[Phase] = Some(Init)

  override def recordError(error: RemorphError): Parsing =
    copy(encounteredErrors = this.encounteredErrors :+ error)
}

case class BuildingAst(
    tree: ParserRuleContext,
    previousPhase: Option[Parsing] = None,
    encounteredErrors: Seq[RemorphError] = Seq.empty)
    extends Phase {
  override def recordError(error: RemorphError): BuildingAst =
    copy(encounteredErrors = this.encounteredErrors :+ error)
}

case class Optimizing(
    unoptimizedPlan: LogicalPlan,
    previousPhase: Option[BuildingAst] = None,
    encounteredErrors: Seq[RemorphError] = Seq.empty)
    extends Phase {
  override def recordError(error: RemorphError): Optimizing =
    this.copy(encounteredErrors = this.encounteredErrors :+ error)
}

case class Generating(
    optimizedPlan: LogicalPlan,
    currentNode: TreeNode[_],
    ctx: GeneratorContext,
    totalStatements: Int = 0,
    transpiledStatements: Int = 0,
    previousPhase: Option[Optimizing] = None,
    encounteredErrors: Seq[RemorphError] = Seq.empty)
    extends Phase {
  override def recordError(error: RemorphError): Generating =
    copy(encounteredErrors = this.encounteredErrors :+ error)
}
