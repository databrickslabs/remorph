package com.databricks.labs.remorph

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.intermediate.{LogicalPlan, TreeNode}
import org.antlr.v4.runtime.ParserRuleContext

sealed trait Phase

case object Init extends Phase

case class Parsing(source: String, filename: String = "-- test source --") extends Phase

case class BuildingAst(tree: ParserRuleContext, sources: Option[Parsing] = None) extends Phase

case class Optimizing(unoptimizedPlan: LogicalPlan, parsed: Option[BuildingAst] = None) extends Phase

case class Generating(
    optimizedPlan: LogicalPlan,
    currentNode: TreeNode[_],
    totalStatements: Int = 0,
    transpiledStatements: Int = 0,
    ctx: GeneratorContext,
    optimized: Option[Optimizing] = None)
    extends Phase
