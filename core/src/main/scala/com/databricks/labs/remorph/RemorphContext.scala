package com.databricks.labs.remorph

import com.databricks.labs.remorph.intermediate.{LogicalPlan, TreeNode}
import org.antlr.v4.runtime.ParserRuleContext

sealed trait RemorphContext

case class Raw(input: String) extends RemorphContext

case class Parsed(input: String, tree: ParserRuleContext) extends RemorphContext

case class Visited(input: String, tree: ParserRuleContext, unoptimizedPlan: LogicalPlan) extends RemorphContext

case class Optimized(input: String, tree: ParserRuleContext, unoptimizedPlan: LogicalPlan, optimizedPlan: LogicalPlan)
    extends RemorphContext

case class Generating(
    input: String,
    tree: ParserRuleContext,
    unoptimizedPlan: LogicalPlan,
    optimizedPlan: LogicalPlan,
    currentNode: TreeNode[_],
    totalStatements: Int,
    transpiledStatements: Int)
    extends RemorphContext
