package com.databricks.labs.remorph.linter

import org.antlr.v4.runtime.tree.ParseTreeWalker
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}
import mainargs._

object Main {
  def main(args: Array[String]): Unit = {
    val exitCode = ParserForMethods(this).runOrExit(args) match {
      case Right(value: Int) => value
      case Left(error) =>
        // scalastyle:off println
        println(error)
        // scalastyle:on
        1 // Failure
    }
    sys.exit(exitCode)
  }

  @main
  def run(
      @arg(short = 'i', name = "inputpath", doc = "Source path of g4 grammar files")
      sourceDir: os.Path,
      @arg(short = 'o', name = "outputpath", doc = "Report output path")
      outputPath: os.Path): Int = {
    try {
      val ruleTracker = new RuleTracker
      val orphanedRule = new OrphanedRule(ruleTracker)

      val input =
        """parser grammar Test;
        a : 'a' ;
        b : 'b' ;
        c : 'c' ;
        d: a b;"""
      val inputStream = CharStreams.fromString(input)
      val lexer = new ANTLRv4Lexer(inputStream)
      val tokens = new CommonTokenStream(lexer)
      val parser = new ANTLRv4Parser(tokens)
      val tree = parser.grammarSpec()
      val walker = new ParseTreeWalker()
      walker.walk(orphanedRule, tree)
      val summary = ruleTracker.reconcileRules()
      val output = ujson.write(summary.toJSON)
      println(output)

      0 // Success
    } catch {
      case e: Exception =>
        e.printStackTrace()
        1 // Failure
    }
  }
}
