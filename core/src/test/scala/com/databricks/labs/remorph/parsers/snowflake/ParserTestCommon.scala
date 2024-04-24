package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate.{NamedTable, Relation, TreeNode}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream, RuleContext}
import org.scalatest.{Assertion, Assertions}

trait ParserTestCommon { self: Assertions =>

  def astBuilder: SnowflakeParserBaseVisitor[_]
  protected def parseString[R <: RuleContext](input: String, rule: SnowflakeParser => R): R = {
    val inputString = CharStreams.fromString(input)
    val lexer = new SnowflakeLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokenStream)
    val tree = rule(parser)
    // uncomment the following line if you need a peek in the Snowflake AST
    // println(tree.toStringTree(parser))
    tree
  }

  protected def example[R <: RuleContext](
      query: String,
      rule: SnowflakeParser => R,
      expectedAst: TreeNode): Assertion = {
    val sfTree = parseString(query, rule)

    val result = astBuilder.visit(sfTree)

    assert(result == expectedAst, s"\nFor input string\n$query\nactual result:\n$result\nexpected\n$expectedAst")
  }

  protected def namedTable(name: String): Relation = NamedTable(name, Map.empty, is_streaming = false)

}
