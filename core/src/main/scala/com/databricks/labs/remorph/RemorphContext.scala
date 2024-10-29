package com.databricks.labs.remorph

import com.databricks.labs.remorph.intermediate.{LogicalPlan, TreeNode}
import org.antlr.v4.runtime.ParserRuleContext

sealed trait RemorphContext

case object Empty extends RemorphContext

case class Sources(input: String) extends RemorphContext

case class Parsed(tree: ParserRuleContext, sources: Option[Sources] = None) extends RemorphContext

case class Ast(unoptimizedPlan: LogicalPlan, parsed: Option[Parsed] = None) extends RemorphContext

case class Optimized(optimizedPlan: TreeNode[_], ast: Option[Ast] = None) extends RemorphContext

case class Generating(
    currentNode: TreeNode[_],
    totalStatements: Int = 0,
    transpiledStatements: Int = 0,
    optimized: Option[Optimized] = None)
    extends RemorphContext
