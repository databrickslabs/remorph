package com.databricks.labs.remorph.parsers.tsql

import org.scalatest.Assertions

import com.databricks.labs.remorph.parsers.intermediate.{NamedTable, Relation, TreeNode}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream, RuleContext}
import org.scalatest.{Assertion, Assertions}

// [TODO]: Need to consolidate for all the dialects.
trait ParserTestCommon { self: Assertions =>

  def astBuilder: TSqlParserBaseVisitor[_]
  protected def parseString[R <: RuleContext](input: String, rule: TSqlParser => R): R = {
    val inputString = CharStreams.fromString(input)
    val lexer = new TSqlLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new TSqlParser(tokenStream)
    val tree = rule(parser)
    // uncomment the following line if you need a peek in the TSql AST
    // println(tree.toStringTree(parser)) // Ignore
    tree
  }

  protected def example[R <: RuleContext](query: String, rule: TSqlParser => R, expectedAst: TreeNode): Assertion = {
    val sfTree = parseString(query, rule)

    val result = astBuilder.visit(sfTree)

    assert(result == expectedAst, s"\nFor input string\n$query\nactual result:\n$result\nexpected\n$expectedAst")
  }

  protected def namedTable(name: String): Relation = NamedTable(name, Map.empty, is_streaming = false)

}
