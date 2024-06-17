package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.intermediate.TreeNode
import org.antlr.v4.runtime.tree.ParseTreeVisitor
import org.antlr.v4.runtime._
import org.scalatest.{Assertion, Assertions}

trait ParserTestCommon[P <: Parser] { self: Assertions =>

  protected def makeLexer(chars: CharStream): TokenSource
  protected def makeParser(tokens: TokenStream): P
  protected def makeErrHandler(chars: String): ErrorCollector = new DefaultErrorCollector
  protected def astBuilder: ParseTreeVisitor[_]
  protected var errHandler: ErrorCollector = _

  protected def parseString[R <: RuleContext](input: String, rule: P => R): R = {
    val inputString = CharStreams.fromString(input)
    val lexer = makeLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = makeParser(tokenStream)
    errHandler = makeErrHandler(input)
    parser.removeErrorListeners()
    parser.addErrorListener(errHandler)
    val tree = rule(parser)

    // uncomment the following line if you need a peek in the Snowflake/TSQL AST
    // println(tree.toStringTree(parser))
    tree
  }

  protected def example[R <: RuleContext](query: String, rule: P => R, expectedAst: TreeNode): Assertion = {
    val sfTree = parseString(query, rule)
    if (errHandler != null && errHandler.errorCount != 0) {
      errHandler.logErrors()
      fail(s"${errHandler.errorCount} errors found in the input string")
    }

    val result = astBuilder.visit(sfTree)

    assert(result == expectedAst, s"\nFor input string\n$query\nactual result:\n$result\nexpected\n$expectedAst")
  }

}
