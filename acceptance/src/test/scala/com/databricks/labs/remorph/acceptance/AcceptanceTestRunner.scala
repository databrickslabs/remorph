package com.databricks.labs.remorph.acceptance

import com.databricks.labs.remorph.parsers.{ErrorCollector, ProductionErrorCollector}
import com.databricks.labs.remorph.parsers.intermediate.TreeNode
import com.databricks.labs.remorph.parsers.snowflake.{SnowflakeAstBuilder, SnowflakeParserTestCommon}
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.{Assertion, Assertions}

import java.io.File
import java.nio.file.{Files, Path, Paths}
import scala.collection.JavaConverters.asScalaIteratorConverter
import scala.io.Source
import scala.util.control.NonFatal

case class AcceptanceTest(testName: String, inputFile: File)

trait AcceptanceTestSource {
  def listTests: Seq[AcceptanceTest]
}

class NestedFiles(root: Path) extends AcceptanceTestSource {
  def listTests: Seq[AcceptanceTest] = {
    val files =
      Files
        .walk(root)
        .iterator()
        .asScala
        .filter(f => Files.isRegularFile(f))
        .toSeq

    val sqlFiles = files.filter(_.getFileName.toString.endsWith(".sql"))
    sqlFiles.map(p => AcceptanceTest(root.relativize(p).toString, p.toFile))
  }
}

trait QueryExtractor {
  def extractQuery(file: File): String
}

object CommentBasedQueryExtractor extends QueryExtractor {
  override def extractQuery(file: File): String = {
    val source = Source.fromFile(file)
    val indexedLines = source.getLines().zipWithIndex.toSeq
    source.close()
    val startIndex = indexedLines.find(_._1 == "-- snowflake sql:").map(_._2).get
    val endIndex = indexedLines.find(_._1 == "-- databricks sql:").map(_._2).get
    indexedLines.map(_._1).slice(startIndex + 1, endIndex).mkString("\n")
  }
}

trait QueryRunner {
  def runQuery(query: String): Assertion
}

sealed trait TestOutcome
case object Success extends TestOutcome
case class SyntaxError(message: String) extends TestOutcome
case class SemanticError(unresolved: TreeNode) extends TestOutcome

class IsResolvedAsSnowflakeQueryRunner(override protected val astBuilder: SnowflakeAstBuilder)
    extends QueryRunner
    with SnowflakeParserTestCommon
    with Assertions {

  override def makeErrHandler(chars: String): ErrorCollector =
    new ProductionErrorCollector(chars, "")
  override def runQuery(query: String): Assertion = {
    val result =
      try {
        astBuilder.visit(parseString(query, _.snowflake_file()))
      } catch {
        case NonFatal(e) =>
          val formattedErrors = errHandler.formatErrors
          val msg = if (formattedErrors.nonEmpty) {
            formattedErrors.mkString("\n")
          } else {
            Option(e.getMessage).getOrElse(s"Unexpected exception of class ${e.getClass} was thrown")
          }
          fail(msg)
      }
    if (result.toString.contains("Unresolved")) {
      fail(s"Translated query contains unresolved bits: $result")
    } else {
      succeed
    }
  }

}
case class AcceptanceTestConfig(
    testFileSource: AcceptanceTestSource,
    queryExtractor: QueryExtractor,
    queryRunner: QueryRunner)

abstract class AcceptanceTestRunner(config: AcceptanceTestConfig) extends AnyFlatSpec {

  private def runAcceptanceTest(acceptanceTest: AcceptanceTest) = {
    val q = config.queryExtractor.extractQuery(acceptanceTest.inputFile)
    config.queryRunner.runQuery(q)
  }

  config.testFileSource.listTests.foreach { test =>
    registerTest(test.testName) {
      runAcceptanceTest(test)
    }

  }

}

class SnowflakeAcceptanceSuite
    extends AcceptanceTestRunner(
      AcceptanceTestConfig(
        new NestedFiles(Paths.get("../tests/resources/functional/snowflake")),
        CommentBasedQueryExtractor,
        new IsResolvedAsSnowflakeQueryRunner(new SnowflakeAstBuilder)))
