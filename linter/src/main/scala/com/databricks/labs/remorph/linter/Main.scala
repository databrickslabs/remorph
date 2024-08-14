package com.databricks.labs.remorph.linter

import mainargs.{ParserForMethods, TokensReader, arg, main}
import org.antlr.v4.runtime.tree.ParseTreeWalker
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}

import java.time.Instant

object Main {

  implicit object PathRead extends TokensReader.Simple[os.Path] {
    def shortName: String = "path"
    def read(strs: Seq[String]): Either[String, os.Path] = Right(os.Path(strs.head, os.pwd))
  }

  private def getCurrentCommitHash: Option[String] = {
    val gitRevParse = os.proc("/usr/bin/git", "rev-parse", "--short", "HEAD").call(os.pwd)
    if (gitRevParse.exitCode == 0) {
      Some(gitRevParse.out.trim())
    } else {
      None
    }
  }

  private def timeToEpochNanos(instant: Instant) = {
    val epoch = Instant.ofEpochMilli(0)
    java.time.Duration.between(epoch, instant).toNanos
  }

  @main
  def run(
      @arg(short = 'i', doc = "Source path of g4 grammar files")
      sourceDir: os.Path,
      @arg(short = 'o', doc = "Report output path")
      outputPath: os.Path,
      @arg(short = 'c', doc = "Write errors to console")
      toConsole: Boolean): Unit = {
    try {

      val now = Instant.now
      val project = "remorph-core"
      val commitHash = getCurrentCommitHash
      val grammarSource = new NestedFiles(sourceDir.toNIO)

      val outputFilePath = outputPath / s"${project}-lint-grammar-${timeToEpochNanos(now)}.jsonl"
      os.makeDir.all(outputPath)

      var exitCode = 0

      grammarSource.listGrammars.foreach { grammar =>
        val ruleTracker = new RuleTracker
        val orphanedRule = new OrphanedRule(ruleTracker)
        val inputStream = CharStreams.fromPath(grammar.inputFile.toPath)
        val lexer = new ANTLRv4Lexer(inputStream)
        val tokens = new CommonTokenStream(lexer)
        val parser = new ANTLRv4Parser(tokens)
        val tree = parser.grammarSpec()
        val walker = new ParseTreeWalker()
        walker.walk(orphanedRule, tree)

        val header = ReportEntryHeader(
          project = project,
          commit_hash = commitHash,
          version = "latest",
          timestamp = now.toString,
          file = os.Path(grammar.inputFile).relativeTo(sourceDir).toString)
        val summary = ruleTracker.reconcileRules()
        val reportEntryJson = ReportEntry(header, summary).asJson
        os.write.append(outputFilePath, ujson.write(reportEntryJson, indent = -1) + "\n")

        if (summary.hasIssues) {
          exitCode = 1
        }

        // If a local build, and there were problems, then we may wish to print the report
        // to the console so developers see it
        // scalastyle:off
        if (toConsole) {
          val sourceLines = os.read(os.Path(grammar.inputFile)).linesIterator.toList

          if (summary.hasIssues) {
            println("\nIssues found in grammar: " + grammar.inputFile)
            if (summary.orphanedRuleDef.nonEmpty) {
              println("Orphaned rules (rules defined but never used):")
              summary.orphanedRuleDef.foreach { rule =>
                println(s"  ${rule.ruleName} defined at line ${rule.lineNo}:")
                sourceLines.slice(rule.lineNo - 1, rule.lineNo + 1).foreach { line =>
                  println("    " + line)
                }
                println()
              }
            }
            if (summary.undefinedRules.nonEmpty) {
              println("Undefined rules (rules referenced but never defined):")
              summary.undefinedRules.foreach { rule =>
                println(s"\n  ${rule.ruleName} used at line ${rule.lineNo}, col ${rule.charStart}")
                println("    " + sourceLines(rule.lineNo - 1))
                println(" " * (4 + rule.charStart) + "^" * (rule.charEnd - rule.charStart))
              }
            }
          }
        }
        // scalastyle:on
      }
      if (exitCode != 0) {
        sys.exit(exitCode)
      }
    } catch {
      case e: Exception =>
        e.printStackTrace()
        sys.exit(1)
    }
  }

  def main(args: Array[String]): Unit = ParserForMethods(this).runOrExit(args)
}
