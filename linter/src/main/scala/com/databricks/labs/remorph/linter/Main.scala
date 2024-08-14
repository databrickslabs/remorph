package com.databricks.labs.remorph.linter

import org.antlr.v4.runtime.tree.ParseTreeWalker
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}
import mainargs._

object Main {

  implicit object PathRead extends TokensReader.Simple[os.Path] {
    def shortName: String = "path"
    def read(strs: Seq[String]): Either[String, os.Path] = Right(os.Path(strs.head, os.pwd))
  }

  @main
  def run(
      @arg(short = 'i', doc = "Source path of g4 grammar files")
      sourceDir: os.Path,
      @arg(short = 'o', doc = "Report output path")
      outputPath: os.Path): Unit = {
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
      // scalastyle:off println
      println(output)
      // scalastyle:on println
    } catch {
      case e: Exception =>
        e.printStackTrace()
    }
  }

  def main(args: Array[String]): Unit = ParserForMethods(this).runOrExit(args)
}
