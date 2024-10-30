package com.databricks.labs.remorph

import com.databricks.labs.remorph.intermediate.{LogicalPlan, TreeNode}
import org.antlr.v4.runtime.ParserRuleContext

sealed trait Phase

case object Init extends Phase

case class SourceCode(source: String, filename: String = "-- test source --") extends Phase

case class Parsed(tree: ParserRuleContext, sources: Option[SourceCode] = None) extends Phase

case class Ast(unoptimizedPlan: LogicalPlan, parsed: Option[Parsed] = None) extends Phase

case class Optimized(optimizedPlan: TreeNode[_], ast: Option[Ast] = None) extends Phase

case class Generating(
    currentNode: TreeNode[_],
    totalStatements: Int = 0,
    transpiledStatements: Int = 0,
    optimized: Option[Optimized] = None)
    extends Phase
