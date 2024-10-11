package com.databricks.labs.remorph.parsers
import com.databricks.labs.remorph.parsers.tsql.DataTypeBuilder
import org.antlr.v4.runtime.{ParserRuleContext, Token, Vocabulary}
import org.antlr.v4.runtime.tree.ParseTreeVisitor

/**
 * <p>
 *   An implementation of this class should provide an instance of each of the ParseTreeVisitors
 *   required to build IR and each visitor should be initialized with a reference to the implementation
 *   of this class so that the visitors can call each other without needing to know the specific implementation
 *   of any visitor or creating circular dependencies between them.
 * </p>
 * <p>
 *   Implementations can also supply other shared resources, builders, etc. via the same mechanism
 * </p>
 */
abstract class VisitorCoordinator(val parserVocab: Vocabulary, val ruleNames: Array[String]) {

  // Parse tree visitors
  val astBuilder: ParseTreeVisitor[_]
  val relationBuilder: ParseTreeVisitor[_]
  val expressionBuilder: ParseTreeVisitor[_]
  val dmlBuilder: ParseTreeVisitor[_]
  val ddlBuilder: ParseTreeVisitor[_]

  // A function builder that can be used to build function calls for a particular dialect
  val functionBuilder: FunctionBuilder

  // Common builders that are used across all parsers, but can still be overridden
  val dataTypeBuilder = new DataTypeBuilder

  def ruleName(ctx: ParserRuleContext): String = ruleNames(ctx.getRuleIndex)
  def tokenName(tok: Token): String = parserVocab.getSymbolicName(tok.getType)
}
