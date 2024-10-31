package com.databricks.labs.remorph.generators.orchestration

import com.databricks.labs.remorph.{Phase, Transformation}
import com.databricks.labs.remorph.generators.Generator
import com.databricks.labs.remorph.generators.orchestration.rules.converted.{InformationFile, SuccessPy, SuccessSQL}
import com.databricks.labs.remorph.generators.orchestration.rules.{GenerateBundleFile, DefineJob, QueryHistoryToQueryNodes, ReformatCode, TryGeneratePythonNotebook, TryGenerateSQL, TrySummarizeFailures}
import com.databricks.labs.remorph.intermediate.Rules
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.transpilers.{PySparkGenerator, SqlGenerator}

class FileSetGenerator(
    private val parser: PlanParser[_],
    private val sqlGen: SqlGenerator,
    private val pyGen: PySparkGenerator)
    extends Generator[JobNode, FileSet] {
  val rules = Rules(
    new QueryHistoryToQueryNodes(parser),
    new TryGenerateSQL(sqlGen),
    new TryGeneratePythonNotebook(pyGen),
    new TrySummarizeFailures(),
    new ReformatCode(),
    new DefineJob(),
    new GenerateBundleFile())

  override def generate(tree: JobNode): Transformation[Phase, FileSet] = {
    val fileSet = new FileSet()
    rules(tree) foreachUp {
      case SuccessPy(name, code) =>
        fileSet.withFile(s"$name.py", code)
      case SuccessSQL(name, code) =>
        fileSet.withFile(s"$name.sql", code)
      case InformationFile(name, code) =>
        fileSet.withFile(name, code)
      case _ =>
    }
    ok(fileSet)
  }
}
